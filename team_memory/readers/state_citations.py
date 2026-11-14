"""Citable views of existing proposal/vote records, not inferred approvals.

Reuse timeline's reducer and the existing LangChain literal-quote attribution.
A pending state is a snapshot of absence of a valid vote, not a fabricated event.
Snapshots remain addressable after future votes change the current view.
"""
from copy import deepcopy
from team_memory.storage.objects import digest
from team_memory.review.state import proposals, relation_span


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
