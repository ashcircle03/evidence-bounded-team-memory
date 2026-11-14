"""Shared mechanical conversion; no new relation or answer model."""
from copy import deepcopy
from pathlib import Path
import json
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


def evidence_from(w,snapshot,number):
    if w.get('evidence_type')=='review_state':
        return dict(id=f'e{number}',kind='review_state',source_id=None,
                    state_record=dict(proposal_id=w['proposal_id'],snapshot_id=snapshot['id'],text=w['quote']),
                    start=0,end=len(w['quote']),quote=w['quote'],owner=None,speaker=None,
                    observed_at=None,location=None,conditions=[])
    source=next(s for s in snapshot['sources'] if s['id']==w['source_id'])
    return dict(id=f'e{number}',kind='source',source_id=w['source_id'],state_record=None,
                start=w['start'],end=w['end'],quote=w['quote'],
                **{k:source[k] for k in ('owner','speaker','observed_at','location')},conditions=[])


def witnesses_from(bundle):
    check_bundle(bundle)
    props={p['id']:p for p in bundle['snapshot']['proposals']}
    output=[]
    for e in bundle['evidence']:
        if e['kind']=='review_state':
            w=state_witness(bundle['snapshot'],props[e['state_record']['proposal_id']])
            w.update(start=e['start'],end=e['end'],quote=e['quote'])
        else:w={k:e[k] for k in ('source_id','start','end','quote','location','speaker','observed_at')}
        output.append(w)
    return output


def context_from(bundle,reader):
    # Only state relationships actually carried by the bundle reach generation.
    ids={e['state_record']['proposal_id'] for e in bundle['evidence'] if e['kind']=='review_state'}
    linked=[p for p in reader.review_relations if p['id'] in ids]
    return dict(temporal_scope='current',relations=deepcopy(linked)) if linked else None
