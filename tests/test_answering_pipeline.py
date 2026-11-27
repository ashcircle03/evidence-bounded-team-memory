"""Mechanical conflict-side check in answering.pipeline.claims_from_result (no model)."""
import pytest

pytest.importorskip('nltk')
from team_memory.answering.pipeline import claims_from_result

A = 'Retention is 30 days.'
B = 'Retention is 90 days.'


def case(raw, cited, *, unresolved=True, assertions=True):
    """Two sources state conflicting values; cited = witnesses the answer's [n] points to."""
    witnesses = [dict(source_id='s1', start=0, end=len(A), quote=A),
                 dict(source_id='s2', start=0, end=len(B), quote=B)]
    evidence = [dict(id=f'e{i+1}', kind='source', source_id=w['source_id'], start=w['start'], end=w['end'],
                     quote=w['quote'], conditions=[]) for i, w in enumerate(witnesses)]
    sides = dict(previous=dict(source_id='s1', start=0, end=len(A)), incoming=dict(source_id='s2', start=0, end=len(B)))
    proposal = dict(id='p1', candidate=dict(kind='conflict', **sides,
                                            previous_assertion=sides['previous'] if assertions else None,
                                            incoming_assertion=sides['incoming'] if assertions else None))
    bundle = dict(evidence=evidence, snapshot=dict(proposals=[proposal]),
                  unresolved_proposal_ids=['p1'] if unresolved else [], query=dict(conditions=[]))
    result = dict(raw=raw, citation_sources=[witnesses[i] for i in cited])
    answer = dict(snapshot_id='snap', outcome='abstained', claims=[], reason='none')
    answer, errors = claims_from_result(answer, bundle, witnesses, evidence, result, [])
    return answer, [e for e in errors if e['item_id'] == 'p1']


def test_both_sides_cited_separately_is_conflict_without_issue():
    answer, issues = case('One record says 30 days [1]. Another says 90 days [2].', [0, 1])
    assert answer['outcome'] == 'conflict' and not issues


def test_one_side_cited_is_flagged():
    answer, issues = case('Retention is 30 days [1].', [0])
    assert answer['outcome'] == 'answered'
    assert [e['code'] for e in issues] == ['UNSUPPORTED_CLAIM']


def test_both_sides_in_one_claim_is_flagged():
    answer, issues = case('Retention is 30 or 90 days [1][2].', [0, 1])
    assert answer['outcome'] == 'answered' and len(issues) == 1


def test_neither_side_cited_is_not_flagged():
    answer, issues = case('Nothing relevant [1].', [], unresolved=True)
    assert not issues


def test_resolved_conflict_is_not_checked():
    answer, issues = case('Retention is 30 days [1].', [0], unresolved=False)
    assert answer['outcome'] == 'answered' and not issues


def test_passage_level_conflict_is_not_checked():
    # Without assertion spans a cited passage may support an unrelated fact in it.
    answer, issues = case('Retention is 30 days [1].', [0], assertions=False)
    assert answer['outcome'] == 'answered' and not issues


# ---- strategy selection in run_strategies (S0 / S1 / S2 of the evaluation plan) ----
def _reader(cls):
    """An instance without the index/model constructor; only generate_evidence is used."""
    from threading import Lock
    r = object.__new__(cls)
    r.generate_evidence = lambda question, witnesses, review: dict(raw='draft [1].', citation_sources=[])
    r.lock = Lock()
    return r


def test_plain_reference_reader_skips_citation_repair(monkeypatch):
    from team_memory.answering import pipeline
    from team_memory.answering.generation import ReferenceQA
    calls = []
    monkeypatch.setattr(pipeline, 'attach_citations', lambda reader, q, result: calls.append(reader) or result)
    result = pipeline.run_strategies(_reader(ReferenceQA), 'q', [], None)
    assert result['raw'] == 'draft [1].' and calls == []


def test_cited_reader_keeps_citation_repair(monkeypatch):
    from team_memory.answering import pipeline
    from team_memory.answering.strategies.attribution import CitedSourceQA
    calls = []
    monkeypatch.setattr(pipeline, 'attach_citations', lambda reader, q, result: calls.append(reader) or result)
    reader = _reader(CitedSourceQA)
    pipeline.run_strategies(reader, 'q', [], None)
    assert calls == [reader]


def test_non_reference_readers_keep_previous_behaviour(monkeypatch):
    """Readers that are not ReferenceQA (test decoders, adapters) still get citation repair."""
    from team_memory.answering import pipeline
    calls = []
    monkeypatch.setattr(pipeline, 'attach_citations', lambda reader, q, result: calls.append(reader) or result)

    class Decoder:
        def generate_evidence(self, question, witnesses, review):
            return dict(raw='x', citation_sources=[])
    reader = Decoder()
    pipeline.run_strategies(reader, 'q', [], None)
    assert calls == [reader]


# ---- citation numbers (pilot: "[1,4,5,7]" was read as uncited) ----
def test_citation_numbers_accept_lists_and_labels():
    from team_memory.answering.generation import citation_numbers, has_citation
    assert citation_numbers('A [1]. B [2, 3]. C [1,4,5]. D [Source 6].') == [1, 2, 3, 1, 4, 5, 6]
    assert citation_numbers('x [2; 7]', source_labels=False) == [2, 7]
    assert has_citation('A penitentiary [2,3,6].') and not has_citation('No citation here.')
    assert citation_numbers('[a] [1-2] (3)') == []   # only numbers and number lists


def test_list_citation_owns_its_sentence():
    answer, issues = case('One record says 30 days [1, 2].', [0, 1])
    assert answer['claims'] and set(answer['claims'][0]['evidence_ids']) == {'e1', 'e2'}


# ---- scoped answer falls back to the regular path when its draft fails a check ----
def test_scoped_rejection_falls_back_to_regular_answer(monkeypatch, tmp_path):
    from threading import Lock
    from team_memory.adapters import answering as port
    calls = []
    monkeypatch.setattr(port, 'use_scoped', lambda *a: True)
    def reject(*a):
        raise ValueError('Conditional answer requires at least two grounded scopes')
    monkeypatch.setattr(port, 'public_answer', reject)
    monkeypatch.setattr(port, 'run_strategies', lambda reader, q, w, r: calls.append('regular') or dict(raw='', citation_sources=[]))
    monkeypatch.setattr(port, 'claims_from_result', lambda answer, *a: (dict(answer, outcome='answered'), []))
    monkeypatch.setattr(port, 'claim_views', lambda *a: [])
    class Reader:
        lock = Lock()
        def generate_scoped(self, query, views):
            return None
    monkeypatch.setattr(port, 'reader_for', lambda *a: Reader())
    monkeypatch.setattr(port, 'witnesses_from', lambda b: [dict(source_id='s', start=0, end=1, quote='x')])
    monkeypatch.setattr(port, 'context_from', lambda *a: None)
    monkeypatch.setattr(port.AnsweringAdapter, 'verify_snapshot', lambda self, s: None)
    adapter = port.AnsweringAdapter('w', None, tmp_path, snapshot_loader=lambda sid: None)
    bundle = dict(snapshot=dict(id='snap', sources=[], proposals=[]), query=dict(text='q', time_scope='current', conditions=[]),
                  evidence=[], coverage='hits', unresolved_proposal_ids=[])
    monkeypatch.setattr(port, 'evidence_problem', lambda b: None)
    data, errors = adapter.execute('answer.generate', dict(bundle=bundle), None)
    assert calls == ['regular'] and data['outcome'] == 'answered'


def test_team_prompt_states_the_answer_format():
    from team_memory.answering.strategies.checking import ConflictCheckedQA, ANSWER_FORMAT
    qa, refine = ConflictCheckedQA._team_templates(object.__new__(ConflictCheckedQA))
    assert ANSWER_FORMAT in qa.template and ANSWER_FORMAT in refine.template


# ---- review-state attachment and condition-scoped outcome ----
def _review_bundle(status='approved'):
    old, new = 'Retention is 30 days.', 'Retention is corrected to 90 days.'
    evidence = [dict(id='e1', kind='source', source_id='s1', start=0, end=len(old), quote=old, conditions=[]),
                dict(id='e2', kind='source', source_id='s2', start=0, end=len(new), quote=new, conditions=[]),
                dict(id='e3', kind='review_state', source_id=None, start=0, end=5, quote='state',
                     state_record=dict(proposal_id='p1'), conditions=[])]
    proposal = dict(id='p1', status=status, candidate=dict(kind='correction',
        previous=dict(source_id='s1', start=0, end=len(old)), incoming=dict(source_id='s2', start=0, end=len(new))))
    bundle = dict(evidence=evidence, snapshot=dict(proposals=[proposal]), unresolved_proposal_ids=[], query=dict(conditions=[]))
    witnesses = [dict(source_id=e['source_id'], start=e['start'], end=e['end'], quote=e['quote']) for e in evidence]
    return bundle, witnesses, evidence


def test_claim_on_reviewed_record_also_cites_its_state():
    bundle, witnesses, evidence = _review_bundle()
    result = dict(raw='Retention is 90 days after the correction [2].', citation_sources=witnesses)
    answer, _ = claims_from_result(dict(snapshot_id='s', outcome='abstained', claims=[], reason='x'),
                                   bundle, witnesses, evidence, result, [])
    c = answer['claims'][0]
    assert c['evidence_ids'] == ['e2', 'e3'] and c['kind'] == 'reported_fact'


def test_claims_with_different_record_conditions_make_a_conditional_answer():
    a, b = 'v1: latency 120ms.', 'v2: latency 90ms.'
    evidence = [dict(id='e1', kind='source', source_id='s1', start=0, end=len(a), quote=a, conditions=['v1']),
                dict(id='e2', kind='source', source_id='s2', start=0, end=len(b), quote=b, conditions=['v2'])]
    bundle = dict(evidence=evidence, snapshot=dict(proposals=[]), unresolved_proposal_ids=[], query=dict(conditions=[]))
    witnesses = [dict(source_id=e['source_id'], start=0, end=e['end'], quote=e['quote']) for e in evidence]
    result = dict(raw='For v1 the latency is 120ms [1]. For v2 it is 90ms [2].', citation_sources=witnesses)
    answer, _ = claims_from_result(dict(snapshot_id='s', outcome='abstained', claims=[], reason='x'),
                                   bundle, witnesses, evidence, result, [])
    assert answer['outcome'] == 'conditional'
    same = dict(result, raw='The latency is 120ms [1].')
    answer, _ = claims_from_result(dict(snapshot_id='s', outcome='abstained', claims=[], reason='x'),
                                   bundle, witnesses, evidence, same, [])
    assert answer['outcome'] == 'answered'
