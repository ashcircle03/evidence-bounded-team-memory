"""Audit harness contracts and reproducible limitations, not model accuracy."""
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from evaluation.reference_audit.run import claim_review, digest, parse_claims
from team_memory.reference_checked import missing_opposing_sources
from team_memory.reference_qa import format_response


def test_source_coverage_can_hide_omitted_alternative():
    # The document contains two answers; only one has been answered. This is
    # intentionally a characterization of the current trigger, not a fix.
    w = dict(source_id='one', quote='A says 23ms; B says31ms.', location='x', speaker='A',start=0,end=27)
    answer = format_response('Latency?', 'A measured23ms [1].', [w])
    answer['document_judgments'] = [dict(source_id='one', label='CONTRADICTS')]
    assert missing_opposing_sources(answer) == []


def test_decomposition_formats_and_explicit_failure():
    assert parse_claims('Claims: A said X.\nClaims: B said Y under Z.') == ['A said X.','B said Y under Z.']
    assert parse_claims('Claims:\n1. A did not approve X.\n2. X remains pending.') == ['A did not approve X.','X remains pending.']
    with pytest.raises(ValueError):
        parse_claims('Claims:')


def test_claim_review_is_claim_by_document_and_keeps_draft():
    ws = [dict(source_id='a', quote='X is10. Y is20.', speaker='A',location='a', start=0,end=15),
          dict(source_id='b', quote='Y is30.', speaker='B',location='b',start=0,end=7)]
    draft = format_response('X and Y?', 'X is10. Y is20 [1].', ws)
    before = deepcopy(draft); calls = []

    class LLM:
        def chat(self, messages):
            content = messages[-1].content
            text = 'Claims: X is10.\nClaims: Y is20.' if content.startswith('Instruction: Break down') else 'X is10 [1]; Y is20 [1] or30 [2].'
            return SimpleNamespace(message=SimpleNamespace(content=text))

    def judge(client, document, claim, question, model):
        calls.append((document,claim))
        label = 'CONTRADICTS' if 'B\n' in document and claim=='Y is20.' else 'SUPPORTS'
        return '{"answer":"'+label+'"}'

    reader = SimpleNamespace(llm=LLM(),active_review_context=None)
    with patch('team_memory.reference_checked.evaluate_document_support',side_effect=judge):
        answer=claim_review(reader,'X and Y?',draft)
    assert len(calls)==4
    assert {c for _,c in calls}=={'X is10.','Y is20.'}
    assert answer['revised'] and answer['cs_count']==0.5
    assert answer['draft_raw']==before['raw'] and draft==before
    assert digest(answer['citation_sources'])==digest(ws)


def test_evidence_hash_includes_state_author_date_and_order():
    packet=dict(witnesses=[dict(quote='x',speaker='A',observed_at='2026-01-01')],review_context={'status':'pending'})
    changed=deepcopy(packet); changed['review_context']['status']='approved'
    assert digest(packet)!=digest(changed)
    changed=deepcopy(packet); changed['witnesses'][0]['speaker']='B'
    assert digest(packet)!=digest(changed)
