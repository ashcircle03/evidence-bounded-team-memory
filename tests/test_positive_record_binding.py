import json
from team_memory.records import positive_binding


def span(text,quote):
    a=text.index(quote)
    return dict(text=quote,start=a,end=a+len(quote),confidence=.9)


def fixture():
    s=dict(id='s',owner='a',speaker='a',observed_at='2026-01-01T00:00:00Z',location='test',text='Use K because it is dry. Use J when wet.')
    return s,json.dumps(dict(extractions=[
        dict(claim='Use K',claim_attributes=dict(claim_group='a',stance='decision')),
        dict(condition='it is dry',condition_attributes=dict(claim_group='a',stance='unknown')),
        dict(claim='Use J',claim_attributes=dict(claim_group='b',stance='proposal'))]))


def test_missing_prediction_is_not_a_negative_judgment():
    s,raw=fixture()
    _,t=positive_binding.bind(s,raw,dict(statement=[dict(claim=span(s['text'],'Use K'),condition=[],basis=[])]),model='test')
    assert json.loads(t['candidate_raw'])==json.loads(raw)


def test_exact_explicit_other_role_retypes_without_losing_content():
    s,raw=fixture()
    _,t=positive_binding.bind(s,raw,dict(statement=[dict(claim=span(s['text'],'Use K'),condition=[],basis=[span(s['text'],'it is dry')])]),model='test')
    rr=json.loads(t['candidate_raw'])['extractions']
    assert not any('condition' in r for r in rr)
    assert rr[-1]['basis']=='it is dry' and len(t['retyped'])==1


def test_shared_context_does_not_delete_other_claim_link():
    s,raw=fixture()
    _,t=positive_binding.bind(s,raw,dict(statement=[dict(claim=span(s['text'],'Use J'),condition=[span(s['text'],'it is dry')],basis=[])]),model='test')
    rr=json.loads(t['candidate_raw'])['extractions']
    assert {r['condition_attributes']['claim_group'] for r in rr if 'condition' in r}=={'a','b'}
