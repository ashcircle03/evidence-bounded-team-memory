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
