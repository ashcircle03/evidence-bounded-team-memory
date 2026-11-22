"""Shared mechanical conversion; no new relation or answer model."""
from copy import deepcopy
from pathlib import Path
import json
from team_memory.records.arguments import visible_arguments
from team_memory.review import state
from team_memory.contracts.validation import check_bundle
from .legacy import FrozenStore,native_objects,state_witness


def query_text(query):
    return query['text']+ ('\nRequested conditions (data): '+json.dumps(query['conditions'],ensure_ascii=False)
                           if query['conditions'] else '')


def reader_for(factory,cache_root,snapshot):
    store=FrozenStore(Path(cache_root)/'views'/snapshot['id'],native_objects(snapshot),snapshot)
    reader=factory(store)
    reader.store=store
    reader.index_dir=Path(cache_root)/'index'
    reader.review_relations=state.proposals(store)
    reader.temporal_scope='current'
    return reader


def evidence_from(w,snapshot,number,sources=None):
    """sources: optional {source_id: source} map of this snapshot, to avoid a scan per evidence."""
    if w.get('evidence_type')=='review_state':
        return dict(id=f'e{number}',kind='review_state',source_id=None,
                    state_record=dict(proposal_id=w['proposal_id'],snapshot_id=snapshot['id'],text=w['quote']),
                    start=0,end=len(w['quote']),quote=w['quote'],owner=None,speaker=None,
                    observed_at=None,location=None,conditions=[])
    source=sources[w['source_id']] if sources is not None else next(s for s in snapshot['sources'] if s['id']==w['source_id'])
    from team_memory.records.graph import describe
    description=describe(source,w['start'],w['end'])
    conditions=list(dict.fromkeys(u['quote'] for c in description['claims'] for u in c['condition'])) if description else []
    return dict(id=f'e{number}',kind='source',source_id=w['source_id'],state_record=None,
                start=w['start'],end=w['end'],quote=w['quote'],
                **{k:source[k] for k in ('owner','speaker','observed_at','location')},conditions=conditions)


def claim_views(evidence, snapshot):
    """Resolve source-local claim references from the immutable snapshot.

    Views are private generation inputs. Public citations retain the retrieval ID
    and, for a claim-specific view, its exact stored claim ID.
    """
    from team_memory.records.graph import describe, ROLES

    sources = {s['id']: s for s in snapshot['sources']}
    views = []
    used = {e['id'] for e in evidence}
    for hit in evidence:
        if hit['kind'] != 'source':
            views.append(hit)
            continue
        source = sources[hit['source_id']]
        hit = dict(hit, **visible_arguments(source, hit['start'], hit['end']))
        context = describe(source, hit['start'], hit['end'])
        claims = context['claims'] if context else []
        if not claims:
            views.append(hit)
            continue
        delivered = []
        for claim in claims:
            spans = [span for role in ROLES for span in claim[role]]
            start = min(s['start'] for s in spans)
            end = max(s['end'] for s in spans)
            key = hit['id'] + '/' + claim['id']
            while key in used:
                key += '/'
            used.add(key)
            from team_memory.records.layout import visible_layout
            structure = visible_layout(source, hit['start'], hit['end'])
            rows = [r for r in structure if r['start'] < end and start < r['end']]
            arguments = visible_arguments(source, max(hit["start"], start), min(hit["end"], end))
            delivered.extend(arguments.get("record_arguments", {}).get("links", []))
            views.append(dict(hit, **arguments, layout=rows, id=key, evidence_id=hit['id'], record_claim=claim,
                              start=start, end=end, quote=source['text'][start:end],
                              conditions=list(dict.fromkeys(s['quote'] for s in claim['condition']))))
        # Retain the retrieved passage for unstructured content, without
        # attributing the pooled conditions to everything in that passage.
        represented = {s['id'] for c in claims for role in ROLES for s in c[role]}
        missing_arguments = any(link not in delivered for link in hit.get('record_arguments', {}).get('links', []))
        if missing_arguments or set(context['unassigned_unit_ids']) - represented or context['extraction_status'] != 'annotated':
            views.append(dict(hit, conditions=[]))
    return views


def witnesses_from(bundle):
    check_bundle(bundle)
    props={p['id']:p for p in bundle['snapshot']['proposals']}
    output=[]
    for e in bundle['evidence']:
        if e['kind']=='review_state':
            w=state_witness(bundle['snapshot'],props[e['state_record']['proposal_id']])
            w.update(start=e['start'],end=e['end'],quote=e['quote'])
        else:w={k:e[k] for k in ('source_id','start','end','quote','location','speaker','observed_at')}
        if e['kind']=='source':
            from team_memory.records.graph import describe
            source=next(s for s in bundle['snapshot']['sources'] if s['id']==e['source_id'])
            w.update(visible_arguments(source,e['start'],e['end']))
            description=describe(source,e['start'],e['end'])
            if e['conditions'] and not (description and len(description['claims']) > 1):
                w['conditions']=list(e['conditions'])
            if description is not None:w['record_context']=description
        output.append(w)
    return output


def context_from(bundle,reader):
    # Only state relationships actually carried by the bundle reach generation.
    ids={e['state_record']['proposal_id'] for e in bundle['evidence'] if e['kind']=='review_state'}
    linked=[p for p in reader.review_relations if p['id'] in ids]
    return dict(temporal_scope='current',relations=deepcopy(linked)) if linked else None
