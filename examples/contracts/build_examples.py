"""Small synthetic collaboration fixtures, NOT a benchmark or model outputs.

Run from repository root: python examples/contracts/build_examples.py
All expected semantic choices below are handwritten for these synthetic stories.
"""

from copy import deepcopy as copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from team_memory.contracts.ports import VERSION
from team_memory.contracts.schema import OPERATIONS
from team_memory.contracts.validation import render_state

HERE = Path(__file__).resolve().parent


def build():
    old = dict(id='s-old', owner='hana', speaker='Hana', observed_at='2026-11-01T09:00:00Z',
               location='report.md#L1', text='v1 / CPU: latency 120ms. 담당자는 Hana다.')
    new = dict(id='s-new', owner='jun', speaker='Jun', observed_at='2026-11-02T09:00:00Z',
               location='correction.md#L1', text='v1 / CPU: latency 90ms. Earlier 120ms was a typo; correct only latency.')

    def span(source, quote=None):
        quote = quote or source['text']
        start = source['text'].index(quote)
        return dict(source_id=source['id'], start=start, end=start+len(quote), quote=quote)

    candidate = dict(kind='correction', previous=span(old), incoming=span(new),
                     reason='The report explicitly corrects latency under the same v1 / CPU condition.',
                     previous_assertion=span(old, '120ms'), incoming_assertion=span(new, '90ms'))
    proposal = dict(id='p-correction', candidate=candidate, reviewer='hana',
                    status='pending', effect='none', decided_at=None)
    snapshot = dict(id='snap-3', revision=3, as_of='2026-11-02T10:00:00Z',
                    sources=[old, new], proposals=[proposal])
    query = dict(text='What is the currently accepted latency for v1 / CPU?',
                 time_scope='current', as_of=None, conditions=['v1', 'CPU'])

    def evidence(source, quote=None, eid=None):
        return dict(id=eid or 'e-'+source['id'], kind='source', state_record=None,
                    **span(source, quote), **{k:source[k] for k in ('owner','speaker','observed_at','location')},
                    conditions=['v1', 'CPU'])

    def state_evidence(snap):
        text = render_state(snap['proposals'][0], snap['id'])
        return dict(id='e-state', kind='review_state', source_id=None,
                    state_record=dict(proposal_id=snap['proposals'][0]['id'], snapshot_id=snap['id'], text=text),
                    start=0, end=len(text), quote=text, owner=None, speaker=None,
                    observed_at=None, location=None, conditions=[])

    bundle = dict(snapshot=snapshot, query=query, evidence=[evidence(old), evidence(new), state_evidence(snapshot)],
                  coverage='hits', unresolved_proposal_ids=['p-correction'])

    def claim(text, ids, kind='reported_fact', cid='c1', group=None):
        return dict(id=cid, text=text, kind=kind, evidence_ids=ids,
                    conditions=['v1', 'CPU'], alternative_group=group)

    answer = dict(snapshot_id=snapshot['id'], outcome='answered', reason=None, claims=[
        claim('The recorded latency is 120ms.', ['e-s-old']),
        claim('The 90ms correction is pending, so it has not replaced 120ms.',
              ['e-s-old', 'e-s-new', 'e-state'], 'state', 'c2')])
    cases = []

    def case(name, operation, payload, data, *, seed=None, status='ok', code=None,
             principal='hana', unchanged=True, expect=(), retry=False):
        common = dict(contract_version=VERSION, request_id=name, workspace_id='demo')
        response = dict(**common, module=OPERATIONS[operation], operation=operation,
                        status=status, data=data, errors=[] if code is None else [dict(
                            code=code, message='Synthetic fixture: '+code, retryable=False, item_id=None)])
        cases.append(copy(dict(name=name, setup={'snapshot':seed or snapshot},
            context=dict(workspace_id='demo', principal_id=principal,
                         capabilities=['records:read','records:write','review:vote','relations:compare',
                                       'evidence:read','answer:generate']),
            request=dict(**common, operation=operation, payload=payload), response=response,
            expect=[{'path':'/status','equals':status}, *expect], state_unchanged=unchanged,
            retry_identically=retry)))

    def equals(path, value):
        return {'path':path, 'equals':value}

    case('records-read', 'snapshot.get', {'snapshot_id':None}, snapshot,
         expect=[equals('/data', snapshot)])
    seed = copy(snapshot); seed.update(id='snap-1', revision=1, sources=[old], proposals=[])
    appended = copy(seed); appended.update(id='snap-2', revision=2, sources=[old,new])
    case('records-append-idempotent', 'record.append',
         dict(source=new, idempotency_key='append-new', expected_revision=1),
         dict(snapshot=appended, object_id='s-new', replayed=False), seed=seed, principal='jun',
         unchanged=False, retry=True, expect=[equals('/data/snapshot/sources',[old,new])])
    case('records-proposal-pending', 'proposal.submit',
         dict(candidate=candidate, idempotency_key='propose-correction', expected_revision=2),
         dict(snapshot=snapshot, object_id='p-correction', replayed=False), seed=appended,
         unchanged=False, expect=[equals('/data/snapshot/proposals/0/status','pending'),
                                  equals('/data/snapshot/proposals/0/effect','none')])
    approved = copy(snapshot)
    approved.update(id='snap-4', revision=4)
    approved['proposals'][0].update(status='approved', effect='replace_assertion', decided_at='2026-11-02T10:00:00Z')
    case('records-owner-approval', 'review.apply',
         dict(proposal_id='p-correction', choice='approve', idempotency_key='vote-1', expected_revision=3),
         dict(snapshot=approved, object_id='p-correction', replayed=False), unchanged=False, retry=True,
         expect=[equals('/data/snapshot/sources',snapshot['sources']),
                 equals('/data/snapshot/proposals/0/effect','replace_assertion'),
                 equals('/data/snapshot/proposals/0/candidate/previous_assertion',span(old,'120ms'))])
    for name, principal, rev, code in [('unauthorized-review','jun',3,'FORBIDDEN'),
                                      ('stale-review','hana',2,'STALE_SNAPSHOT')]:
        case(name, 'review.apply', dict(proposal_id='p-correction',choice='approve',
             idempotency_key=name,expected_revision=rev), None, principal=principal,
             status='invalid',code=code,expect=[equals('/errors/0/code',code)])
    case('relations-exact-correction', 'relations.compare',
         dict(snapshot=snapshot,incoming_source_id='s-new',history_source_ids=['s-old']),
         dict(snapshot_id=snapshot['id'],candidates=[candidate]),
         expect=[equals('/data/candidates',[candidate])])
    # The same two texts under different measurement conditions must coexist.
    other = copy(snapshot); other['sources'][1]['text']='v2 / GPU: latency 90ms.'
    other['proposals']=[]
    coexist = dict(kind='coexist',previous=span(other['sources'][0]), incoming=span(other['sources'][1]),
                   reason='Different version and hardware; these measurements can coexist.',
                   previous_assertion=None,incoming_assertion=None)
    case('relations-different-conditions', 'relations.compare',
         dict(snapshot=other,incoming_source_id='s-new',history_source_ids=['s-old']),
         dict(snapshot_id=other['id'],candidates=[coexist]), seed=other,
         expect=[equals('/data/candidates/0/kind','coexist')])
    case('relations-model-timeout', 'relations.compare',
         dict(snapshot=snapshot,incoming_source_id='s-new',history_source_ids=['s-old']),
         None,status='error',code='MODEL_TIMEOUT',expect=[equals('/errors/0/code','MODEL_TIMEOUT')])
    case('retrieval-keeps-metadata-and-state','evidence.retrieve',
         dict(snapshot=snapshot,query=query,max_evidence=4), bundle,
         expect=[equals('/data/coverage','hits'),equals('/data/unresolved_proposal_ids',['p-correction']),
                 equals('/data/evidence',bundle['evidence'])])
    empty = copy(bundle); empty.update(coverage='no_hits',evidence=[],unresolved_proposal_ids=[])
    case('retrieval-no-hits-is-not-db-absence','evidence.retrieve',
         dict(snapshot=snapshot,query=query,max_evidence=4),empty,
         expect=[equals('/data/coverage','no_hits')])
    case('retrieval-failed-is-not-no-hits','evidence.retrieve',
         dict(snapshot=snapshot,query=query,max_evidence=4),None,status='error',code='RETRIEVAL_FAILED',
         expect=[equals('/errors/0/code','RETRIEVAL_FAILED')])
    case('answer-pending-keeps-current','answer.generate',{'bundle':bundle},answer,
         expect=[equals('/data/claims',answer['claims'])])
    approved_bundle = copy(bundle); approved_bundle['snapshot']=approved
    approved_bundle['evidence'][-1]=state_evidence(approved)
    approved_bundle['unresolved_proposal_ids']=[]
    approved_answer = dict(snapshot_id=approved['id'],outcome='answered',reason=None,claims=[
        claim('The approved latency is 90ms.', ['e-s-new','e-state'],'state'),
        claim('Hana remains the owner.', ['e-s-old'],'reported_fact','c2')])
    case('answer-approved-changes-only-latency','answer.generate',{'bundle':approved_bundle},approved_answer,
         seed=approved,expect=[equals('/data/claims',approved_answer['claims'])])
    abstained = dict(snapshot_id=snapshot['id'],outcome='abstained',claims=[],reason='No retrieved evidence supports an answer.')
    case('answer-no-evidence-abstains','answer.generate',{'bundle':empty},abstained,
         expect=[equals('/data/outcome','abstained'),equals('/data/claims',[])])
    conflict = copy(snapshot)
    conflict['sources'][1]['text']='v1 / CPU: latency 90ms. Repeated measurement.'
    cp = conflict['proposals'][0]
    cp['candidate'].update(kind='conflict',incoming=span(conflict['sources'][1]),
                            previous_assertion=None,incoming_assertion=None,
                            reason='Incompatible measurements under the stated same conditions.')
    cb = copy(bundle); cb['snapshot']=conflict
    cb['evidence']=[evidence(conflict['sources'][0]),evidence(conflict['sources'][1]),state_evidence(conflict)]
    ca = dict(snapshot_id=conflict['id'],outcome='conflict',reason=None,claims=[
        claim('Hana reports 120ms.',['e-s-old'],group='latency'),
        claim('Jun reports 90ms.',['e-s-new'],cid='c2',group='latency')])
    case('answer-conflict-both-alternatives','answer.generate',{'bundle':cb},ca,seed=conflict,
         expect=[equals('/data/outcome','conflict'),equals('/data/claims',ca['claims'])])
    owner_bundle=copy(cb); owner_bundle['query']['text']='Who owns the report?'
    owner_answer=dict(snapshot_id=conflict['id'],outcome='answered',reason=None,
                      claims=[claim('Hana owns the report.',['e-s-old'])])
    case('answer-unrelated-conflict-does-not-block','answer.generate',{'bundle':owner_bundle},owner_answer,
         seed=conflict,expect=[equals('/data/outcome','answered')])
    reconsider=copy(approved)
    reconsider['sources'][0]['text']='v1 crashes with parallel hooks; keep single-threaded execution.'
    reconsider['sources'][1]['text']='v2 fixes parallel hook invocation. Please reconsider the single-threaded decision.'
    rp=reconsider['proposals'][0]
    rp['candidate'].update(kind='reconsider', previous=span(reconsider['sources'][0]),
                           incoming=span(reconsider['sources'][1]), previous_assertion=None,incoming_assertion=None,
                           reason='Changed version may remove the premise behind the earlier decision.')
    rp['effect']='authorize_reconsideration'
    rb=copy(bundle); rb.update(snapshot=reconsider,unresolved_proposal_ids=[])
    rb['evidence']=[evidence(s) for s in reconsider['sources']]+[state_evidence(reconsider)]
    rb['query']=dict(text='Does approval mean parallel execution is now the adopted decision?',
                     time_scope='current',as_of=None,conditions=['hook invocation'])
    rb['evidence'][0]['conditions']=['v1','parallel hook invocation']
    rb['evidence'][1]['conditions']=['v2','parallel hook invocation']
    ra=dict(snapshot_id=reconsider['id'],outcome='conditional',reason=None,claims=[
        claim('Review is authorized; no changed execution decision or successful experiment is recorded.',
              ['e-s-old','e-s-new','e-state'],'state')])
    ra['claims'][0]['conditions']=['hook invocation']
    case('answer-reconsider-is-not-correction','answer.generate',{'bundle':rb},ra,seed=reconsider,
         expect=[equals('/data/outcome','conditional'),equals('/data/claims',ra['claims'])])
    case('gateway-read-only-ask','gateway.ask',dict(query=query,snapshot_id=snapshot['id']),
         dict(bundle=bundle,answer=answer),expect=[equals('/data/answer/claims',answer['claims'])])
    case('gateway-rejects-unauthorized-review','gateway.review',
         dict(proposal_id='p-correction',choice='approve',idempotency_key='bad-vote',expected_revision=3),
         None,principal='jun',status='invalid',code='FORBIDDEN',expect=[equals('/errors/0/code','FORBIDDEN')])
    case('gateway-ingest-keeps-source-on-comparison-failure','gateway.ingest',
         dict(source=new,idempotency_key='append-new',expected_revision=1),
         dict(receipt=dict(snapshot=appended,object_id='s-new',replayed=False),proposal_ids=[]),
         seed=seed,principal='jun',status='partial',code='MODEL_TIMEOUT',unchanged=False,
         expect=[equals('/data/receipt/snapshot/sources',[old,new]),equals('/errors/0/code','MODEL_TIMEOUT')])
    rejected=copy(snapshot); rejected.update(id='snap-rejected',revision=4)
    rejected['proposals'][0].update(status='rejected',decided_at='2026-11-02T10:00:00Z')
    rejected_bundle=copy(bundle); rejected_bundle.update(snapshot=rejected,unresolved_proposal_ids=[])
    rejected_bundle['evidence'][-1]=state_evidence(rejected)
    rejected_answer=dict(snapshot_id=rejected['id'],outcome='answered',reason=None,claims=[
        claim('The recorded latency remains 120ms.',['e-s-old']),
        claim('The proposed 90ms correction was rejected.',['e-s-new','e-state'],'state','c2')])
    case('answer-rejected-does-not-promote-new-value','answer.generate',{'bundle':rejected_bundle},rejected_answer,
         seed=rejected,expect=[equals('/data/claims',rejected_answer['claims'])])
    return cases


if __name__ == '__main__':
    (HERE/'cases.json').write_text(json.dumps(build(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
