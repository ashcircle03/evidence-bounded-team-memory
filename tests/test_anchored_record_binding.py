import json
from team_memory.records import anchored_binding, preserving


def fixture():
    source = dict(id='s', owner='a', speaker='a', observed_at='2026-01-01T00:00:00Z',
                  location='test', text='When the gate is shut, keep the trolley idle because the cable is loose. The shelf is green.')
    rows = [dict(claim='keep the trolley idle', claim_attributes=dict(claim_group='a', stance='decision')),
            dict(claim='The shelf is green', claim_attributes=dict(claim_group='b', stance='observation'))]
    return source, rows


def run(links, extra=()):
    s, rows = fixture(); raw = json.dumps(dict(extractions=rows+list(extra)))
    g, trace = anchored_binding.bind(s, raw, json.dumps(dict(links=links)), model='test')
    return s, raw, g, trace


def link(**changes):
    s, _ = fixture()
    result = dict(target='a', role='basis', quote='the cable is loose', evidence_quote=s['text'].split('. ')[0]+'.')
    result.update(changes); return result


def test_fixed_assertions_and_stances_survive_new_context():
    s, raw, g, trace = run([link()])
    old = json.loads(raw)['extractions']; new = json.loads(trace['candidate_raw'])['extractions']
    assert [x for x in new if 'claim' in x] == old
    assert new[-1]['basis'] == 'the cable is loose'
    assert new[-1]['basis_attributes']['basis_kind'] == 'stated'
    assert not trace['fallback'] and not trace['rejected'] and g['status'] == 'annotated'


def test_empty_proposal_does_not_delete_old_fields():
    extra = dict(condition='When the gate is shut', condition_attributes=dict(claim_group='a', stance='unknown'))
    s, raw, g, trace = run([], [extra])
    assert json.loads(trace['candidate_raw']) == json.loads(raw)
    assert g['claims'] == preserving.compile_graph(s, raw)['claims']


def test_reject_new_target_or_state_authority():
    for item in [link(target='new'), dict(link(), approved=True)]:
        s, raw, g, trace = run([item])
        assert trace['fallback'] and g == preserving.compile_graph(s, raw, model='test')


def test_reject_ungrounded_or_target_free_evidence():
    for item in [link(quote='the motor is broken'), link(target='b'), link(evidence_quote='the cable is loose')]:
        _, raw, _, trace = run([item])
        assert len(trace['rejected']) == 1
        assert json.loads(trace['candidate_raw']) == json.loads(raw)


def test_same_role_longer_source_span_replaces_only_contained_fragment():
    extra = dict(condition='the gate is shut', condition_attributes=dict(claim_group='a', stance='unknown'))
    _, _, _, trace = run([link(role='condition', quote='When the gate is shut')], [extra])
    rows = json.loads(trace['candidate_raw'])['extractions']
    assert [r['condition'] for r in rows if 'condition' in r] == ['When the gate is shut']
    assert trace['accepted'][0]['replaced_fragments'] == 1


def test_shared_context_requires_explicit_edges_and_preserves_other_role():
    s, _ = fixture()
    extra = dict(condition='the cable is loose', condition_attributes=dict(claim_group='a', stance='unknown'))
    _, _, _, trace = run([link(), link(target='b', evidence_quote=s['text'])], [extra])
    rows = json.loads(trace['candidate_raw'])['extractions']
    assert {r['basis_attributes']['claim_group'] for r in rows if 'basis' in r} == {'a', 'b'}
    assert any('condition' in r for r in rows)
    # Exact provenance cannot prove semantic attachment. This deliberately bad
    # but source-grounded relation remains visible to the fixed semantic scorer.

