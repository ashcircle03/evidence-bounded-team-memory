import json
from team_memory.records import context_contract


def setup():
    source = dict(id='s', owner='a', speaker='a', observed_at='2026-01-01T00:00:00Z',
        location='test', text='For damp tools, use the oven because the air is warm. The heater is active.')
    raw = json.dumps(dict(extractions=[
        dict(claim='For damp tools, use the oven', claim_attributes=dict(claim_group='a', stance='decision')),
        dict(claim='The heater is active', claim_attributes=dict(claim_group='b', stance='observation'))]))
    return source, raw


def apply(quote, role='condition'):
    s, raw = setup()
    return context_contract.bind(s, raw, json.dumps(dict(links=[dict(target='a', role=role,
        quote=quote, evidence_quote=s['text'])])), model='test')


def test_reject_self_edge_and_oversized_context_containing_root():
    for q in ('For damp tools, use the oven', 'For damp tools, use the oven because the air is warm'):
        g, t = apply(q)
        assert len(t['endpoint_rejections']) == 1
        assert not any('condition' in r for r in json.loads(t['candidate_raw'])['extractions'])


def test_allow_inline_qualifier_as_proper_subspan_of_target():
    _, t = apply('For damp tools')
    assert not t['endpoint_rejections']
    assert json.loads(t['candidate_raw'])['extractions'][-1]['condition'] == 'For damp tools'


def test_do_not_reject_evidence_just_because_it_is_another_assertion():
    _, t = apply('The heater is active', 'basis')
    assert not t['endpoint_rejections']
    assert json.loads(t['candidate_raw'])['extractions'][-1]['basis'] == 'The heater is active'
    # The contract permits distinct endpoints; semantic truth is evaluated apart.
