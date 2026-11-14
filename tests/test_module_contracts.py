"""Collaboration contracts: fixed examples and adversarial boundary violations."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from team_memory.contracts.conformance import fixture_factory, run_case, pointer
from team_memory.contracts.schema import build_schema
from team_memory.contracts.validation import (
    ContractError, check_answer, check_bundle, check_snapshot, validate, validate_exchange,
)

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT/'examples/contracts/cases.json').read_text())


def case(name):
    return deepcopy(next(c for c in CASES if c['name'] == name))


@pytest.mark.parametrize('scenario', CASES, ids=lambda c:c['name'])
def test_shared_contract_fixture(scenario):
    run_case(scenario, fixture_factory(scenario))


def test_generated_schema_and_examples_are_current():
    schema = build_schema()
    Draft202012Validator.check_schema(schema)
    assert schema == json.loads((ROOT/'team_memory/contracts/schema.json').read_text())
    spec = importlib.util.spec_from_file_location('contract_examples',ROOT/'examples/contracts/build_examples.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.build() == CASES
    assert {c['response']['module'] for c in CASES} == {'records','relations','retrieval','answering','gateway'}


@pytest.mark.parametrize('mutation', [
    'missing_author','wrong_date','invalid_date','fake_quote','bool_offset','wrong_state',
    'stale_state','duplicate_id','no_hits_with_evidence','unknown_unresolved',
])
def test_rejects_corrupted_evidence(mutation):
    bundle = case('answer-pending-keeps-current')['request']['payload']['bundle']
    e = bundle['evidence'][0]
    if mutation == 'missing_author': del e['speaker']
    elif mutation == 'wrong_date': e['observed_at']='2026-11-03T09:00:00Z'
    elif mutation == 'invalid_date': e['observed_at']='2026-02-31T09:00:00Z'
    elif mutation == 'fake_quote': e['quote']='not the original'
    elif mutation == 'bool_offset': e['start']=False
    elif mutation == 'wrong_state': bundle['evidence'][-1]['state_record']['text']='approved'
    elif mutation == 'stale_state': bundle['evidence'][-1]['state_record']['snapshot_id']='old-snapshot'
    elif mutation == 'duplicate_id': bundle['evidence'][1]['id']=e['id']
    elif mutation == 'no_hits_with_evidence': bundle['coverage']='no_hits'
    elif mutation == 'unknown_unresolved': bundle['unresolved_proposal_ids']=['missing']
    with pytest.raises(ContractError): check_bundle(bundle)


@pytest.mark.parametrize('mutation', ['pending_effect','reconsider_replace','wrong_reviewer','wide_correction'])
def test_rejects_state_authority_expansion(mutation):
    snap=case('answer-pending-keeps-current')['setup']['snapshot']
    p=snap['proposals'][0]
    if mutation == 'pending_effect': p['effect']='replace_assertion'
    elif mutation == 'wrong_reviewer': p['reviewer']='jun'
    elif mutation == 'wide_correction': p['candidate']['previous_assertion']['end']=999
    else:
        p.update(status='approved',effect='replace_assertion')
        p['candidate'].update(kind='reconsider',previous_assertion=None,incoming_assertion=None)
    with pytest.raises(ContractError): check_snapshot(snap)


@pytest.mark.parametrize('mutation', ['missing_cite','unknown_cite','state_only_fact','source_only_state','wrong_snapshot','duplicate_claim'])
def test_rejects_claim_evidence_mismatch(mutation):
    c=case('answer-pending-keeps-current'); answer=c['response']['data']
    if mutation=='missing_cite': answer['claims'][0]['evidence_ids']=[]
    elif mutation=='unknown_cite': answer['claims'][0]['evidence_ids']=['invented']
    elif mutation=='state_only_fact': answer['claims'][0]['evidence_ids']=['e-state']
    elif mutation=='source_only_state': answer['claims'][1]['evidence_ids']=['e-s-old']
    elif mutation=='wrong_snapshot': answer['snapshot_id']='other'
    else: answer['claims'][1]['id']=answer['claims'][0]['id']
    with pytest.raises(ContractError): check_answer(answer,c['request']['payload']['bundle'])


def test_dropping_conflicting_alternative_is_not_success():
    c=case('answer-conflict-both-alternatives')
    c['response']['data']['claims'].pop()
    with pytest.raises(ContractError): validate_exchange(c['request'],c['response'])


def test_failure_cannot_be_disguised_as_successful_empty_comparison():
    c=case('relations-model-timeout')
    c['response'].update(status='ok',data={'snapshot_id':'snap-3','candidates':[]})
    with pytest.raises(ContractError): validate_exchange(c['request'],c['response'])


def test_records_cannot_return_partial_commit():
    c=case('records-owner-approval')
    c['response']['status']='partial'
    c['response']['errors']=[dict(code='IO_FAILURE',message='write failed',retryable=False,item_id=None)]
    with pytest.raises(ContractError): validate_exchange(c['request'],c['response'])


def test_historical_query_requires_time():
    c=case('gateway-read-only-ask')
    c['request']['payload']['query']['time_scope']='historical'
    with pytest.raises(ContractError): validate('request',c['request'])


def test_receipt_cannot_point_to_another_object():
    c=case('records-owner-approval')
    c['response']['data']['object_id']='not-the-requested-proposal'
    with pytest.raises(ContractError): validate_exchange(c['request'],c['response'])


def test_actor_is_not_accepted_from_untrusted_json():
    c=case('records-owner-approval')
    c['request']['payload']['actor']='hana'
    with pytest.raises(ContractError): validate('request',c['request'])


def test_model_candidate_cannot_approve_itself():
    c=case('relations-exact-correction')
    c['response']['data']['candidates'][0]['status']='approved'
    with pytest.raises(ContractError): validate_exchange(c['request'],c['response'])


def test_input_mutation_is_detected():
    c=case('gateway-read-only-ask'); subject=fixture_factory(c)
    original=subject.port.handle
    def bad(request, *, context):
        result=original(request,context=context)
        request['payload']['query']['conditions']=[]
        return result
    subject.port.handle=bad
    with pytest.raises(ContractError,match='mutated'): run_case(c,subject)


def test_read_only_side_effect_is_detected():
    c=case('answer-pending-keeps-current'); subject=fixture_factory(c)
    original=subject.port.handle
    def bad(request, *, context):
        result=original(request,context=context)
        subject.port.state['revision']+=1
        return result
    subject.port.handle=bad
    with pytest.raises(ContractError,match='authoritative state'): run_case(c,subject)


def test_receipt_without_commit_is_detected():
    c=case('records-append-idempotent'); subject=fixture_factory(c)
    subject.observe_state=lambda: c['setup']['snapshot']
    with pytest.raises(ContractError,match='not committed'): run_case(c,subject)


def test_retry_with_second_commit_is_detected():
    c=case('records-append-idempotent'); subject=fixture_factory(c)
    original=subject.port.handle
    def bad(request, *, context):
        result=original(request,context=context)
        if subject.port.calls > 1: subject.port.state['revision']+=1
        return result
    subject.port.handle=bad
    with pytest.raises(ContractError,match='second mutation'): run_case(c,subject)


def test_json_pointer_escaping_and_list():
    assert pointer({'a/b':{'~key':[7]}},'/a~1b/~0key/0')==7


def test_structural_validation_is_not_semantic_entailment():
    c=case('answer-pending-keeps-current')
    c['response']['data']['claims'][0]['text']='Unsupported 999ms claim.'
    # Exact offsets/IDs are still valid. A separate semantic test must catch this.
    validate_exchange(c['request'],c['response'])
    with pytest.raises(ContractError): run_case(c,fixture_factory(c))


def test_lossless_answer_keeps_unattributed_text_without_borrowed_citations():
    c=case('answer-pending-keeps-current');answer=c['response']['data']
    text=answer['claims'][0]['text'];tail=' Uncited extra statement.'
    answer['claims']=answer['claims'][:1]
    answer['claims'][0]['answer_span']=dict(start=0,end=len(text))
    answer.update(original_text=text+tail,unattributed=[dict(start=len(text),end=len(text+tail),text=tail)])
    check_answer(answer,c['request']['payload']['bundle'])
    answer['unattributed']=[]
    with pytest.raises(ContractError,match='lost'):check_answer(answer,c['request']['payload']['bundle'])
