"""Evidence assembly for review state: retrieval's part of F05.

When a retrieved record is linked to a correction or conflict proposal, add the
other endpoint and the review state as typed, citable evidence. Moved verbatim
from readers/context.py (expand_review_context, assertion_reviews) and
readers/state_citations.py (review_sources, render_snapshot); answering imports
them from here.
"""
from copy import deepcopy
import json

from llama_index.core.schema import NodeWithScore, TextNode

from team_memory.review.state import proposals, relation_span, valid_assertion_spans, valid_witness


def assertion_reviews(witness, context):
    """Expose exact assertion status; never mark the entire document obsolete."""
    from team_memory.review.state import assertion_status
    rows = []
    for relation in (context or {}).get('relations', []):
        if relation['kind'] != 'correction':
            continue
        for side in ('previous', 'incoming'):
            span = relation_span(relation,side)
            if span['source_id'] == witness['source_id'] and max(span['start'],witness['start']) < min(span['end'],witness['end']):
                rows.append(dict(span, proposal_id=relation['id'], side=side,
                    status=assertion_status(span,span['quote'],context['relations']),
                    review_status=relation['status']))
    return rows


def expand_review_context(nodes, sources, relations, temporal_scope):
    """Follow validated links from retrieved sources, preserving both endpoints.

    Retrieval remains upstream dense/BM25 RRF. Expanding linked originals is the
    existing practical _packet rule, restricted here to exact reviewed spans.
    """
    selected = deepcopy(list(nodes))
    visible = {n.node.metadata['source_id'] for n in selected}
    candidates = [r for r in relations
                  if all(valid_witness(r.get(k, {}), sources) for k in ('previous', 'incoming'))
                  and valid_assertion_spans(r, sources)]
    linked = []
    while True:
        added = [r for r in candidates if r not in linked and
                 {r['previous']['source_id'], r['incoming']['source_id']} & visible]
        if not added:
            break
        linked.extend(added)
        for r in added:
            for key in ('previous', 'incoming'):
                w = r[key]
                visible.add(w['source_id'])
                if any(n.node.metadata['source_id'] == w['source_id'] and
                       n.node.metadata['parent_start'] <= w['start'] and
                       w['end'] <= n.node.metadata['parent_end'] for n in selected):
                    continue
                env = sources[w['source_id']]
                metadata = dict(source_id=w['source_id'], parent_start=w['start'], parent_end=w['end'],
                                record_author=env['source']['speaker'], recorded_at=env['observed_at'])
                node = TextNode(text=w['quote'], metadata=metadata,
                    excluded_embed_metadata_keys=list(metadata),
                    excluded_llm_metadata_keys=['source_id', 'parent_start', 'parent_end'])
                selected.append(NodeWithScore(node=node, score=None))
    context = dict(temporal_scope=temporal_scope, relations=deepcopy(linked)) if linked else None
    if context:
        for item in selected:
            node = item.node
            w = dict(source_id=node.metadata['source_id'], start=node.metadata['parent_start'],
                     end=node.metadata['parent_end'])
            reviews = assertion_reviews(w, context)
            if reviews:
                node.metadata['reviewed_assertions'] = json.dumps([
                    dict(quote=r['quote'], status=r['status'], review_status=r['review_status'])
                    for r in reviews], ensure_ascii=False)
                node.excluded_embed_metadata_keys = list(node.metadata)
    return selected, context


def review_sources(store, context):
    if not context:
        return []
    # The module adapter reads one immutable contract snapshot. Reuse its typed
    # state evidence in every stage instead of creating a second authority.
    snapshot=getattr(store,'contract_snapshot',None)
    if snapshot is not None:
        from team_memory.adapters.legacy import state_witness
        current={p['id']:p for p in proposals(store)}
        exported={p['id']:p for p in snapshot['proposals']}
        result=[]
        for linked in context['relations']:
            if current.get(linked['id'])!=linked:raise ValueError('Frozen review context mismatch')
            result.append(state_witness(snapshot,exported[linked['id']]))
        return result
    current = {p['id']: p for p in proposals(store)}
    votes = store.load('timeline_votes')
    sources = store.load('sources')
    output = []
    for linked in context['relations']:
        p = current.get(linked['id'])
        if p != linked:
            raise ValueError('Review state changed during answer generation')
        relevant_votes = {vid: v for vid, v in votes.items() if v.get('proposal') == p['id']
                          and v.get('actor') == p['reviewer'] and v.get('choice') in ('approve', 'reject')}
        snapshot = dict(schema='review-snapshot/v2' if p['kind']=='reconsider' else 'review-snapshot/v1', proposal=deepcopy(p), votes=relevant_votes,
                        source_ids=sorted(sources), temporal_scope=context['temporal_scope'])
        sid = store.put('review_snapshots', snapshot)
        text = render_snapshot(snapshot)
        # No event time invented: historical vote objects never recorded one.
        output.append(dict(source_id='review:'+sid, evidence_type='review_state', snapshot_id=sid,
            proposal_id=p['id'], vote_ids=sorted(relevant_votes), record_snapshot=snapshot,
            location='review_snapshots/'+sid+'.json', speaker='timeline state reducer',
            observed_at=None, start=0, end=len(text), quote=text))
    return output


def render_snapshot(snapshot):
    """Versioned rendering keeps previously cited snapshot offsets stable."""
    if snapshot['schema'] not in ('review-snapshot/v1','review-snapshot/v2'):
        raise ValueError('Unknown review snapshot schema')
    p=snapshot['proposal'];relevant_votes=snapshot['votes']
    noun = dict(correction='correction', reconsider='reconsideration proposal',
                conflict='conflict proposal', coexist='coexistence proposal')[p['kind']]
    state = dict(pending=f'The {noun} is pending. No valid owner approval or rejection is present in this snapshot.',
                 approved=f'The {noun} has been approved.',
                 rejected=f'The {noun} has been rejected.',
                 review_conflict=f'The {noun} has conflicting owner votes; approval is unresolved.')[p['status']]
    old,new = relation_span(p,'previous'),relation_span(p,'incoming')
    text = (f"Proposal {p['id']}; kind: {p['kind']}; reviewer: {p['reviewer']}.\n"
            f"Earlier assertion by {old['speaker']}: {old['quote']}\n"
            f"Incoming assertion by {new['speaker']}: {new['quote']}\n"
            f"{state}\nThe original report remains stored as historical evidence; it has not been erased.\n")
    if p['kind'] == 'correction' and p['status'] == 'pending':
        text += 'The original assertion has not been rejected or superseded by this pending correction. The proposed change remains unresolved.\n'
    if p['kind'] == 'correction' and p['status'] in ('rejected','review_conflict'):
        text += 'The proposed correction was not applied. The earlier assertion has not been superseded by this proposal.\n'
    if p['kind'] == 'reconsider' and snapshot['schema']=='review-snapshot/v2':
        text += ('This proposal requests re-examination of the earlier decision in light of the incoming report. '
                 'Approval authorizes that review only. This proposal does not replace any factual assertion, '
                 'overturn the earlier decision, or establish that a new experiment succeeded.\n')
    for vid, vote in sorted(relevant_votes.items()):
        text += f"Vote {vid}: {vote['actor']} recorded {vote['choice']} for proposal {p['id']}.\n"
    return text
