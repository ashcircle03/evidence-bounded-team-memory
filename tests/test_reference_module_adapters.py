"""Real storage/retrieval/reader adapters with a stub decoder; not model scores."""
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from tests import test_reference_qa as reference
from team_memory.adapters.base import request
from team_memory.adapters.legacy import public_source
from team_memory.contracts.ports import CallContext
from team_memory.contracts.validation import validate_exchange


@unittest.skipUnless(reference.AVAILABLE,'reference dependencies and tokenizer required')
class ModuleFlowTests(unittest.TestCase):
    def setUp(self):
        reference.ReferenceQAIntegration.setUp(self)
        import nltk
        nltk.data.path.insert(0,str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))
        self.context=CallContext('demo','hana',frozenset(['records:read','records:write','records:import',
            'review:vote','relations:compare','evidence:read','answer:generate']))
        self.compare_calls=[]
        self.responder=self.respond

    def compare(self,system,content):
        self.compare_calls.append(content);d=json.loads(content)
        return json.dumps(dict(relations=[dict(kind='reconsider',target=d['earlier'][0]['id'],
            old_sentence_ids=[0],new_sentence_ids=[0],reason='v5 removes the old writer constraint.')]))

    def respond(self,body):
        text='\n'.join(m['content'] for m in body['messages'])
        if 'SUPPORTS' in text and 'IRRELEVANT' in text:return '{"answer":"SUPPORTS"}'
        blocks=re.findall(r'Source (\d+):\n(.*?)(?=\nSource \d+:|$)',text,re.S)
        if 'Was review approved?' in text:
            number=next(n for n,b in blocks if 'status=approved' in b)
            return f'Review is authorized; the existing decision and facts are not replaced [{number}].'
        number=next(n for n,b in blocks if 'Archive is Orion.' in b)
        return f'Archive is Orion [{number}].'

    def make(self,path):
        from team_memory.adapters.runtime import connect_v2
        from team_memory.readers.attribution import AttributedQA
        return connect_v2(path,workspace_id='demo',reader_factory=lambda store:AttributedQA(store,**self.options),generate=self.compare)

    def call(self,port,op,payload,context=None):
        req=request(op,payload,workspace_id='demo',request_id='test-'+op)
        response=port.handle(req,context=context or self.context)
        validate_exchange(req,response)
        return response

    def source(self,text,owner='hana',location='test:old'):
        return public_source(dict(owner=owner,observed_at='2026-11-14T00:00:00Z',
            source=dict(speaker=owner,location=location,text=text)))

    def ask(self,gateway,text):
        return self.call(gateway,'gateway.ask',dict(query=dict(text=text,time_scope='current',as_of=None,conditions=[]),snapshot_id=None))

    def test_save_reconsider_approve_restart_and_qa_are_connected(self):
        path=Path(self.temp.name)/'modules';g=self.make(path)
        old=self.source('Keep one writer because v4 permits one writer. Archive is Orion.')
        self.assertEqual(self.call(g.records,'record.append',dict(source=old,expected_revision=0,idempotency_key='old'))['status'],'ok')
        new=self.source('v5 permits four writers.','jun','test:new')
        ingested=self.call(g,'gateway.ingest',dict(source=new,expected_revision=1,idempotency_key='new'))
        self.assertEqual(ingested['status'],'ok',ingested)
        pid=ingested['data']['proposal_ids'][0]
        pending=self.ask(g,'What is the archive?')
        self.assertEqual(pending['status'],'ok',pending)
        self.assertIn('Orion',pending['data']['answer']['claims'][0]['text'])
        snapshot=g.records.snapshot();calls=len(self.compare_calls)
        again=self.ask(g,'What is the archive?')
        self.assertEqual(g.records.snapshot(),snapshot)
        self.assertEqual(len(self.compare_calls),calls)
        review=self.call(g,'gateway.review',dict(proposal_id=pid,choice='approve',expected_revision=snapshot['revision'],idempotency_key='vote'))
        self.assertEqual(review['status'],'ok',review)
        g=self.make(path)
        after=self.ask(g,'What is the archive?')
        self.assertEqual(after['data']['answer']['claims'],again['data']['answer']['claims'])
        approved=self.ask(g,'Was review approved?')
        self.assertEqual(approved['status'],'ok',approved)
        claim=approved['data']['answer']['claims'][0]
        self.assertEqual(claim['kind'],'state')
        self.assertIn('not replaced',claim['text'])
        self.assertEqual(g.records.snapshot()['sources'],snapshot['sources'])
        self.assertEqual(g.records.snapshot()['proposals'][0]['effect'],'authorize_reconsideration')
        self.assertTrue(any('authorize_reconsideration' in str(c['messages']) for c in self.calls))

    def test_ingest_failure_preserves_source_and_explicit_retry_resumes(self):
        g=self.make(Path(self.temp.name)/'partial')
        self.call(g.records,'record.append',dict(source=self.source('Archive is Orion.'),expected_revision=0,idempotency_key='old'))
        original=g.relations.generate
        def fail(*_):raise TimeoutError('injected')
        g.relations.generate=fail
        payload=dict(source=self.source('v5 permits four writers.','jun','test:new'),expected_revision=1,idempotency_key='new')
        failed=self.call(g,'gateway.ingest',payload)
        self.assertEqual(failed['status'],'partial');self.assertEqual(len(g.records.snapshot()['sources']),2)
        before=g.records.snapshot();answer=self.ask(g,'What is the archive?')
        self.assertEqual(answer['status'],'ok');self.assertEqual(g.records.snapshot(),before)
        g.relations.generate=original
        retried=self.call(g,'gateway.ingest',payload)
        self.assertEqual(retried['status'],'ok',retried)
        calls=len(self.compare_calls);count=len(g.records.chain())
        replay=self.call(g,'gateway.ingest',payload)
        self.assertEqual(replay['data']['proposal_ids'],retried['data']['proposal_ids'])
        self.assertEqual(len(g.records.chain()),count);self.assertEqual(len(self.compare_calls),calls)

    def test_split_reader_matches_v2_prompt_answer_and_evidence_without_state(self):
        from team_memory.service import TeamMemoryService
        from team_memory.readers.attribution import AttributedQA
        root=Path(self.temp.name)/'paired'
        v2=TeamMemoryService(root,reader=AttributedQA(root,**self.options),generate=self.compare)
        v2.import_history([dict(owner='hana',observed_at='2026-11-14T00:00:00Z',source=dict(speaker='hana',location='test',text='Archive is Orion.'))])
        original=v2.ask('What is the archive?');calls=deepcopy(self.calls);self.calls.clear()
        g=self.make(root);actual=self.ask(g,'What is the archive?')
        self.assertEqual(actual['status'],'ok',actual)
        self.assertEqual(''.join(c['text'] for c in actual['data']['answer']['claims']),original['raw'])
        self.assertEqual(self.calls,calls)
        e=actual['data']['bundle']['evidence'][0];w=original['answers'][0]['evidence'][0]
        for key in ('source_id','start','end','quote','speaker','observed_at','location'):self.assertEqual(e[key],w[key])

    def test_retrieval_has_no_generation_and_answering_has_no_retrieval(self):
        from unittest.mock import patch
        g=self.make(Path(self.temp.name)/'isolated')
        self.call(g.records,'record.append',dict(source=self.source('Archive is Orion.'),expected_revision=0,idempotency_key='old'))
        snapshot=g.records.snapshot()
        result=self.call(g.retrieval,'evidence.retrieve',dict(snapshot=snapshot,
            query=dict(text='What is the archive?',time_scope='current',as_of=None,conditions=[]),max_evidence=10))
        self.assertEqual(self.calls,[])
        with patch('team_memory.readers.retrieval.ReferenceQA._index',side_effect=AssertionError('must not search')):
            answer=self.call(g.answering,'answer.generate',dict(bundle=result['data']))
        self.assertEqual(answer['status'],'ok',answer);self.assertEqual(g.records.snapshot(),snapshot)

    def test_forged_snapshot_is_rejected_before_model_call(self):
        g=self.make(Path(self.temp.name)/'forged')
        self.call(g.records,'record.append',dict(source=self.source('Archive is Orion.'),expected_revision=0,idempotency_key='old'))
        snapshot=g.records.snapshot();snapshot['sources'][0]['text']='Archive is changed.'
        result=self.call(g.retrieval,'evidence.retrieve',dict(snapshot=snapshot,
            query=dict(text='What archive?',time_scope='current',as_of=None,conditions=[]),max_evidence=10))
        self.assertEqual(result['errors'][0]['code'],'EVIDENCE_INVALID');self.assertEqual(self.calls,[])

    def test_correction_keeps_unrelated_answer_and_only_changes_assertion(self):
        g=self.make(Path(self.temp.name)/'correction')
        self.call(g.records,'record.append',dict(source=self.source('The timeout is 10 seconds. Archive is Orion.'),expected_revision=0,idempotency_key='old'))
        def compare(_,content):
            d=json.loads(content)
            return json.dumps(dict(relations=[dict(kind='correction',target=d['earlier'][0]['id'],
                old_sentence_ids=[0,1],new_sentence_ids=[0],old_assertion_id=0,new_assertion_id=0,
                reason='Explicit correction of timeout only.')]))
        g.relations.generate=compare
        result=self.call(g,'gateway.ingest',dict(source=self.source('I correct the timeout to 20 seconds.','jun','test:new'),expected_revision=1,idempotency_key='new'))
        self.assertEqual(result['status'],'ok',result)
        pending=self.ask(g,'What is the archive?');snapshot=g.records.snapshot()
        p=snapshot['proposals'][0]
        self.assertEqual(p['candidate']['previous_assertion']['quote'],'The timeout is 10 seconds.')
        self.assertNotIn('Orion',p['candidate']['previous_assertion']['quote'])
        self.call(g,'gateway.review',dict(proposal_id=p['id'],choice='approve',expected_revision=snapshot['revision'],idempotency_key='vote'))
        after=self.ask(g,'What is the archive?')
        self.assertEqual(after['data']['answer']['original_text'],pending['data']['answer']['original_text'])
        self.assertEqual(g.records.snapshot()['sources'],snapshot['sources'])
        self.assertEqual(g.records.snapshot()['proposals'][0]['effect'],'replace_assertion')
        self.assertTrue(any('superseded_assertion' in str(c['messages']) for c in self.calls))

    def test_conflict_keeps_separate_answers_and_evidence(self):
        g=self.make(Path(self.temp.name)/'conflict')
        self.call(g.records,'record.append',dict(source=self.source('The timeout is 10 seconds.'),expected_revision=0,idempotency_key='old'))
        def compare(_,content):
            d=json.loads(content)
            return json.dumps(dict(relations=[dict(kind='conflict',target=d['earlier'][0]['id'],
                old_sentence_ids=[0],new_sentence_ids=[0],reason='Incompatible timeouts under the same settings.')]))
        g.relations.generate=compare
        self.call(g,'gateway.ingest',dict(source=self.source('The timeout is 20 seconds.','jun','test:new'),expected_revision=1,idempotency_key='new'))
        def respond(body):
            text='\n'.join(m['content'] for m in body['messages'])
            if 'SUPPORTS' in text and 'IRRELEVANT' in text:return '{"answer":"SUPPORTS"}'
            blocks=re.findall(r'Source (\d+):\n(.*?)(?=\nSource \d+:|$)',text,re.S)
            a=next(n for n,b in blocks if 'The timeout is 10 seconds.' in b)
            b=next(n for n,b in blocks if 'The timeout is 20 seconds.' in b)
            return f'Hana reports 10 seconds [{a}]. Jun reports 20 seconds [{b}].'
        self.responder=respond
        result=self.ask(g,'What timeouts are reported?')
        self.assertEqual(result['status'],'ok',result)
        answer=result['data']['answer'];self.assertEqual(answer['outcome'],'conflict')
        self.assertEqual(len(answer['claims']),2)
        self.assertNotEqual(answer['claims'][0]['evidence_ids'],answer['claims'][1]['evidence_ids'])

    def test_unattributed_sentence_is_retained_and_marked_partial(self):
        g=self.make(Path(self.temp.name)/'unattributed')
        self.call(g.records,'record.append',dict(source=self.source('Archive is Orion.'),expected_revision=0,idempotency_key='old'))
        def respond(body):
            text='\n'.join(m['content'] for m in body['messages'])
            if 'SUPPORTS' in text and 'IRRELEVANT' in text:return '{"answer":"SUPPORTS"}'
            if 'substring_quote' in text: return '{"answer":[]}'
            return 'Uncited assertion. Archive is Orion [1].'
        self.responder=respond
        result=self.ask(g,'What is the archive?')
        self.assertEqual(result['status'],'partial',result)
        self.assertEqual(result['data']['answer']['original_text'],'Uncited assertion. Archive is Orion [1].')
        self.assertEqual(result['data']['answer']['unattributed'][0]['text'],'Uncited assertion. ')

    def test_invalid_model_output_is_error_not_no_relation(self):
        g=self.make(Path(self.temp.name)/'invalid-model')
        self.call(g.records,'record.append',dict(source=self.source('Archive is Orion.'),expected_revision=0,idempotency_key='old'))
        g.relations.generate=lambda *_:'not json'
        out=self.call(g,'gateway.ingest',dict(source=self.source('A report.','jun','test:new'),expected_revision=1,idempotency_key='new'))
        self.assertEqual(out['status'],'partial')
        self.assertEqual(out['errors'][0]['code'],'MODEL_OUTPUT_INVALID')
        self.assertEqual(len(g.records.snapshot()['sources']),2)

    def test_evidence_budget_does_not_hide_state_and_generate_anyway(self):
        g=self.make(Path(self.temp.name)/'budget')
        self.call(g.records,'record.append',dict(source=self.source('Keep one writer in v4. Archive is Orion.'),expected_revision=0,idempotency_key='old'))
        self.call(g,'gateway.ingest',dict(source=self.source('v5 permits four writers.','jun','test:new'),expected_revision=1,idempotency_key='new'))
        g.max_evidence=1;calls=len(self.calls)
        answer=self.ask(g,'What is the archive?')
        self.assertEqual(answer['status'],'partial',answer)
        self.assertEqual(answer['data']['answer']['outcome'],'abstained')
        self.assertEqual(len(self.calls),calls)

    def test_stripping_review_state_is_rejected_before_generation(self):
        g=self.make(Path(self.temp.name)/'missing-state')
        self.call(g.records,'record.append',dict(source=self.source('Keep one writer in v4. Archive is Orion.'),expected_revision=0,idempotency_key='old'))
        self.call(g,'gateway.ingest',dict(source=self.source('v5 permits four writers.','jun','test:new'),expected_revision=1,idempotency_key='new'))
        snapshot=g.records.snapshot()
        bundle=self.call(g.retrieval,'evidence.retrieve',dict(snapshot=snapshot,
            query=dict(text='What changed?',time_scope='current',as_of=None,conditions=[]),max_evidence=10))['data']
        bundle['evidence']=[e for e in bundle['evidence'] if e['kind']=='source']
        before=len(self.calls)
        answer=self.call(g.answering,'answer.generate',{'bundle':bundle})
        self.assertEqual(answer['status'],'partial')
        self.assertEqual(answer['errors'][0]['code'],'EVIDENCE_INVALID')
        self.assertEqual(len(self.calls),before)

    def test_concurrent_retrieval_shares_cache_without_state_or_model_writes(self):
        from concurrent.futures import ThreadPoolExecutor
        g=self.make(Path(self.temp.name)/'concurrent-search')
        self.call(g.records,'record.append',dict(source=self.source('Archive is Orion.'),expected_revision=0,idempotency_key='old'))
        snapshot=g.records.snapshot()
        payload=dict(snapshot=snapshot,query=dict(text='What is the archive?',time_scope='current',as_of=None,conditions=[]),max_evidence=10)
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(lambda _:self.call(g.retrieval,'evidence.retrieve',payload),range(2)))
        self.assertEqual([r['status'] for r in results],['ok','ok'])
        self.assertEqual(results[0]['data'],results[1]['data'])
        self.assertEqual(self.calls,[]);self.assertEqual(g.records.snapshot(),snapshot)
