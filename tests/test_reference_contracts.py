"""Exercise actual adapter boundaries; no model/network inference."""
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
import json
from pathlib import Path
from threading import RLock
from types import SimpleNamespace
import unittest
from unittest.mock import patch


class ReferenceContracts(unittest.TestCase):
    def setUp(self):
        import nltk
        nltk.data.path.insert(0,str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))
        self.w=[dict(source_id='a',speaker='Mira',location='test:a',start=0,end=37,
                     quote='Amber is recorded. Blue is recorded.')]

    def test_actual_vendor_timeout_never_writes_response_stdout(self):
        from team_memory.reference_qa import ReferenceQA,format_response
        from team_memory.reference_checked import ConflictCheckedQA
        class Broken:
            def chat(self,*a,**k):raise TimeoutError('injected')
        service=object.__new__(ConflictCheckedQA);service.lock=RLock();service.llm=Broken()
        draft=format_response('What?','Amber [1].',self.w);stdout=StringIO()
        with redirect_stdout(stdout),patch.object(ReferenceQA,'ask',return_value=draft),self.assertLogs(level='WARNING'):
            result=service.ask('What?')
        self.assertEqual(stdout.getvalue(),'')
        self.assertEqual(result['answers'],draft['answers'])
        self.assertEqual(result['status'],'partial')
        self.assertEqual(result['stage_failures'][0]['stage'],'document_review')

    def test_malformed_quote_and_prior_incomplete_review_remain_partial(self):
        from team_memory.reference_qa import format_response
        from team_memory.reference_quotes import add_quote_citations
        from team_memory.reference_attributed import repair_omitted_answer
        class Reply:
            def __init__(self,s):self.s=s
            def chat(self,*a,**k):return SimpleNamespace(message=SimpleNamespace(content=self.s))
        before=format_response('What?','Amber is recorded. Answer: amber [1].',self.w)
        result=add_quote_citations('What?',before,Reply('invalid'))
        self.assertEqual(result['status'],'partial');self.assertEqual(result['raw'],before['raw'])
        self.assertEqual(result['stage_failures'][0]['stage'],'quote_attribution')
        previous=format_response('What?','Amber [1].',self.w+[dict(self.w[0],source_id='b')])
        previous.update(status='partial',warnings=['incomplete'],draft_raw=previous['raw'],revised=True,
                        document_judgments=[dict(source_id='a',label='ERROR'),dict(source_id='b',label='CONTRADICTS')])
        result=repair_omitted_answer('What?',previous,Reply('Amber [1]. Blue [2].'))
        self.assertTrue(result['aqa_candidate_accepted']);self.assertEqual(result['status'],'partial')
        self.assertIn('incomplete',result['warnings'])

    def test_judge_tokens_at_actual_http_boundary(self):
        import httpx
        from llama_index.llms.openai_like import OpenAILike
        from team_memory.reference_checked import _LocalJudgeClient
        seen=[]
        def respond(request):
            seen.append(json.loads(request.content))
            return httpx.Response(200,json=dict(id='fake',object='chat.completion',created=0,model='test',
                choices=[dict(index=0,message=dict(role='assistant',content='ok'),finish_reason='stop')],
                usage=dict(prompt_tokens=1,completion_tokens=1,total_tokens=2)))
        with httpx.Client(transport=httpx.MockTransport(respond)) as client:
            llm=OpenAILike(model='test',api_base='http://localhost:1/v1',api_key='fake',is_chat_model=True,
                          max_tokens=1024,http_client=client,max_retries=0)
            _LocalJudgeClient(llm).create(messages=[dict(role='user',content='test')])
            self.assertEqual(seen[0]['max_tokens'],4096);self.assertEqual(llm.max_tokens,1024)

    def test_cli_reserves_stdout_for_one_json_per_request(self):
        from team_memory.reference_qa import main
        class Service:
            def __init__(self,*a,**k):print('index preparation')
            def import_history(self,records):print('library progress');return dict(status='ok')
            def ask(self,question):print('retrieval warning');raise TimeoutError('injected')
        def components(*a):print('initialization progress');return {}
        stdout=StringIO();stderr=StringIO()
        requests='{"operation":"import_history","records":[]}\n{"operation":"ask","question":"Q"}\ninvalid\n'
        argv=['reference_qa','--store','fake','--model-path','fake','--embedding-path','fake','--api-base','http://127.0.0.1:1/v1']
        with patch('sys.argv',argv),patch('sys.stdin',StringIO(requests)),patch('sys.stdout',stdout),patch('sys.stderr',stderr),patch('team_memory.reference_qa.local_components',components),patch('team_memory.reference_qa.ReferenceQA',Service):main()
        rows=[json.loads(line) for line in stdout.getvalue().splitlines()]
        self.assertEqual([r['status'] for r in rows],['ok','error','error'])
        self.assertIn('initialization progress',stderr.getvalue());self.assertIn('retrieval warning',stderr.getvalue())

    def test_two_claims_in_same_original_keep_distinct_evidence(self):
        from team_memory.reference_claims import finish_claims
        selection=json.dumps(dict(segments=[dict(source_id=1,quote='Amber is recorded.'),dict(source_id=1,quote='Blue is recorded.')]))
        class Decoder:
            def chat(self,*a):return SimpleNamespace(message=SimpleNamespace(content=json.dumps(dict(claims=[dict(text='Amber',evidence=[1]),dict(text='Blue',evidence=[2])]))))
        result=finish_claims('What?',selection,self.w,Decoder())
        self.assertEqual(result['status'],'ok');self.assertEqual(len(result['answers']),2)
        self.assertEqual([c['evidence_ids'] for c in result['claims']],[[1],[2]])
        self.assertNotEqual(result['claims'][0]['evidence'][0]['start'],result['claims'][1]['evidence'][0]['start'])
        self.assertEqual(result['claims'][0]['evidence'],result['answers'][0]['evidence'])

    def test_unclaimed_span_and_fake_span_are_visible(self):
        from team_memory.reference_claims import finish_claims
        selection=json.dumps(dict(segments=[dict(source_id=1,quote='Amber is recorded.'),dict(source_id=1,quote='Blue is recorded.')]))
        class Decoder:
            def chat(self,*a):return SimpleNamespace(message=SimpleNamespace(content='{"claims":[{"text":"Amber","evidence":[1]}]}'))
        result=finish_claims('What?',selection,self.w,Decoder())
        self.assertEqual(result['status'],'partial');self.assertEqual(result['unclaimed_evidence_ids'],[2])
        invalid=finish_claims('What?','{"segments":[{"source_id":1,"quote":"invented"}]}',self.w,Decoder())
        self.assertEqual(invalid['citation_sources'],[]);self.assertEqual(invalid['status'],'partial')


if __name__=='__main__':unittest.main()
