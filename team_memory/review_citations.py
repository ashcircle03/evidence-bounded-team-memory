"""Citable views of existing proposal/vote records, not inferred approvals.

Reuse timeline's reducer and the existing LangChain literal-quote attribution.
A pending state is a snapshot of absence of a valid vote, not a fabricated event.
Snapshots remain addressable after future votes change the current view.
"""
from copy import deepcopy
from .store import digest
from .timeline import proposals


def review_sources(store, context):
    if not context:
        return []
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
        snapshot = dict(schema='review-snapshot/v1', proposal=deepcopy(p), votes=relevant_votes,
                        source_ids=sorted(sources), temporal_scope=context['temporal_scope'])
        sid = store.put('review_snapshots', snapshot)
        noun = dict(correction='correction', reconsider='reconsideration proposal',
                    conflict='conflict proposal', coexist='coexistence proposal')[p['kind']]
        state = dict(pending=f'The {noun} is pending. No valid owner approval or rejection is present in this snapshot.',
                     approved=f'The {noun} has been approved.',
                     rejected=f'The {noun} has been rejected.',
                     review_conflict=f'The {noun} has conflicting owner votes; approval is unresolved.')[p['status']]
        text = (f"Proposal {p['id']}; kind: {p['kind']}; reviewer: {p['reviewer']}.\n"
                f"Earlier assertion by {p['previous']['speaker']}: {p['previous']['quote']}\n"
                f"Incoming assertion by {p['incoming']['speaker']}: {p['incoming']['quote']}\n"
                f"{state}\nThe original report remains stored as historical evidence; it has not been erased.\n")
        if p['kind'] == 'correction' and p['status'] == 'pending':
            text += 'The original assertion has not been rejected or superseded by this pending correction. The proposed change remains unresolved.\n'
        for vid, vote in sorted(relevant_votes.items()):
            text += f"Vote {vid}: {vote['actor']} recorded {vote['choice']} for proposal {p['id']}.\n"
        # No event time invented: historical vote objects never recorded one.
        output.append(dict(source_id='review:'+sid, evidence_type='review_state', snapshot_id=sid,
            proposal_id=p['id'], vote_ids=sorted(relevant_votes), record_snapshot=snapshot,
            location='review_snapshots/'+sid+'.json', speaker='timeline state reducer',
            observed_at=None, start=0, end=len(text), quote=text))
    return output
