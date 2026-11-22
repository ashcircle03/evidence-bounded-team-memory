import json
from copy import deepcopy

from team_memory.records import preserving, grouped, graph
from team_memory.adapters.legacy import public_source
from evaluation.record_groups.evaluate import transport


def source(text):
    return public_source(dict(owner='jo', observed_at='2026-01-01T00:00:00Z',
                              source=dict(speaker='jo', location='test://preserving', text=text)))


def raw(*rows):
    return json.dumps({'extractions': [
        {role: quote, role + '_attributes': {'claim_group': group, 'stance': stance}}
        for role, quote, group, stance in rows
    ]})


def test_mixed_stance_is_not_collapsed(tmp_path):
    s = source('We could try the motor. The trial is not approved.')
    output = raw(('claim', 'We could try the motor', 'a', 'proposal'),
                 ('claim', 'The trial is not approved', 'a', 'observation'))
    old = grouped.compile_graph(s, output, canonical=True)
    assert old['claims'][0]['stance'] == 'unknown'
    new = preserving.compile_graph(s, output)
    assert [a['stance'] for a in new['claims'][0]['assertions']] == ['proposal', 'observation']
    assert new['units'] == old['units']
    assert all(new['claims'][0][r] == old['claims'][0][r] for r in graph.ROLES)
    transport(dict(s, record_graph=new), tmp_path)


def test_one_bad_span_does_not_erase_valid_records(tmp_path):
    s = source('Stop the pump because the seal leaks. The room is cold.')
    output = raw(('claim', 'Stop the pump', 'a', 'decision'),
                 ('basis', 'the seal leaks', 'a', 'unknown'),
                 ('time', 'tomorrow', 'a', 'unknown'),
                 ('claim', 'The room is cold', 'b', 'observation'))
    assert preserving.compile_graph(s, output)['status'] == 'failed'
    new = preserving.compile_graph(s, output, isolate_invalid=True)
    assert new['status'] == 'partial' and len(new['claims']) == 2
    assert new['claims'][0]['basis'] and not new['claims'][0]['time']
    assert new['diagnostics'][0]['path'] == 'extractions[2]'
    transport(dict(s, record_graph=new), tmp_path)


def test_unaligned_root_never_reparents_context():
    s = source('The seal leaks. Keep the door shut.')
    output = raw(('claim', 'The motor works', 'a', 'observation'),
                 ('basis', 'The seal leaks', 'a', 'unknown'),
                 ('claim', 'Keep the door shut', 'b', 'decision'))
    new = preserving.compile_graph(s, output, isolate_invalid=True)
    assert new['status'] == 'partial' and len(new['claims']) == 1
    assert not new['claims'][0]['basis']


def test_repeated_time_is_unresolved_not_nearest_matched():
    s = source('The pump stopped at noon. The lamp started at noon.')
    output = raw(('claim', 'The pump stopped', 'a', 'observation'),
                 ('time', 'at noon', 'a', 'unknown'),
                 ('claim', 'The lamp started', 'b', 'observation'))
    new = preserving.compile_graph(s, output, isolate_invalid=True)
    assert new['status'] == 'partial' and len(new['claims']) == 2
    assert not new['claims'][0]['time']
    assert 'Ambiguous' in new['diagnostics'][0]['reason']


def test_wrong_role_is_not_semantically_rewritten():
    s = source('Use paper to avoid blocking the task.')
    output = raw(('claim', 'Use paper', 'a', 'decision'),
                 ('condition', 'to avoid blocking the task', 'a', 'unknown'))
    new = preserving.compile_graph(s, output, isolate_invalid=True)
    assert new['claims'][0]['condition'] and not new['claims'][0]['basis']


def test_spans_can_cross_sentence_tokenizer_boundary(tmp_path):
    s = source('We will store reports, notes, etc. in the future. Compare the providers.')
    output = raw(('claim', 'Compare the providers', 'a', 'decision'),
                 ('basis', 'We will store reports, notes, etc. in the future', 'a', 'unknown'))
    new = preserving.compile_graph(s, output, isolate_invalid=True)
    assert new['status'] == 'annotated'
    transport(dict(s, record_graph=new), tmp_path)


def test_action_contract_preserves_source_prompt_and_examples():
    s = source('The timer stopped yesterday.')
    output = raw(('claim', 'The timer stopped', 'a', 'observation'))
    prompts = []
    def generate(system, prompt):
        prompts.append((system, prompt))
        return output
    grouped.construct_aligned(deepcopy(s), generate, model='test')
    preserving.construct(deepcopy(s), generate, model='test')
    assert prompts[0][1] == prompts[1][1]
    assert 'who performed it' in prompts[1][0]


def test_default_does_not_silently_enable_partial_recovery():
    s = source('The timer stopped yesterday.')
    output = raw(('claim', 'The timer stopped', 'a', 'observation'),
                 ('time', 'tomorrow', 'a', 'unknown'))
    default = preserving.construct(s, lambda *_: output, model='test')
    opted_in = preserving.construct(s, lambda *_: output, model='test', isolate_invalid=True)
    assert default['record_graph']['status'] == 'failed'
    assert opted_in['record_graph']['status'] == 'partial'


def test_table_rows_retain_repeated_cells_at_distinct_offsets():
    text = '| Scope | Result |\r\n|---|---|\r\n| Lab A | Passed |\r\n| Lab B | Pending |\r\n| Lab A | Passed |\r\n'
    s = source(text)
    def unexpected(*args):
        raise AssertionError('Table issued model request')
    result = preserving.construct(s, unexpected, model='test')['record_graph']
    assert [r['cells'][1]['quote'] for r in result['layout']] == ['Passed','Pending','Passed']
    assert [r['cells'][0]['start'] for r in result['layout']] == [
        text.index('Lab A'), text.index('Lab B'), text.rindex('Lab A')]
    graph.validate_graph(s, result)
