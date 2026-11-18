"""Join/authority contracts, not a substitute for real learned-head evaluation."""
import json
from team_memory.records import learned_binding as lb


def span(text, quote):
    start=text.index(quote)
    return dict(text=quote,start=start,end=start+len(quote),confidence=0.9)


def fixture():
    source=dict(id='s',owner='a',speaker='a',observed_at='2026-01-01T00:00:00Z',location='test',
                text='Use K because it is dry. Use J when wet.')
    rows=[dict(claim='Use K',claim_attributes=dict(claim_group='a',stance='decision')),
          dict(condition='it is dry',condition_attributes=dict(claim_group='a',stance='unknown')),
          dict(claim='Use J',claim_attributes=dict(claim_group='b',stance='proposal'))]
    return source,json.dumps(dict(extractions=rows))


def test_changes_only_matched_context_and_keeps_claims():
    s,raw=fixture()
    prediction=dict(statement=[dict(claim=span(s['text'],'Use K'),condition=[],basis=[span(s['text'],'it is dry')])])
    graph,trace=lb.bind(s,raw,prediction,model='test')
    assert graph['status']=='annotated' and not trace['fallback']
    rows=json.loads(trace['candidate_raw'])['extractions']
    assert [x for x in rows if 'claim' in x]==[x for x in json.loads(raw)['extractions'] if 'claim' in x]
    assert not any('condition' in x for x in rows)
    assert rows[-1]['basis']=='it is dry'


def test_no_nearest_or_substring_anchor_join():
    s,raw=fixture()
    prediction=dict(statement=[dict(claim=span(s['text'],'K'),condition=[],basis=[span(s['text'],'it is dry')])])
    _,trace=lb.bind(s,raw,prediction,model='test')
    assert trace['changed_groups']==[]


def test_shared_field_can_attach_to_multiple_claims():
    s,raw=fixture()
    prediction=dict(statement=[dict(claim=span(s['text'],c),condition=[],basis=[span(s['text'],'it is dry')]) for c in ['Use K','Use J']])
    _,trace=lb.bind(s,raw,prediction,model='test')
    rows=json.loads(trace['candidate_raw'])['extractions']
    assert len([r for r in rows if 'basis' in r])==2


def test_native_abstention_not_hidden_by_old_edges():
    s,raw=fixture()
    _,trace=lb.bind(s,raw,dict(statement=[dict(claim=span(s['text'],'Use K'),condition=[],basis=[])]),model='test')
    assert not any('condition' in r or 'basis' in r for r in json.loads(trace['candidate_raw'])['extractions'])


def test_duplicate_anchors_are_not_silently_combined():
    s,raw=fixture();r=dict(claim=span(s['text'],'Use K'),condition=[],basis=[])
    _,trace=lb.bind(s,raw,dict(statement=[r,r]),model='test')
    assert trace['changed_groups']==[] and trace['ambiguous_groups']==['a']


def test_unfaithful_span_rejected():
    s,raw=fixture();a=span(s['text'],'Use K');a['text']='Use X'
    _,trace=lb.bind(s,raw,dict(statement=[dict(claim=a,condition=[],basis=[])]),model='test')
    assert trace['changed_groups']==[]
