import json
from pathlib import Path
import unittest

from team_memory.decision_patch import compare_sources,EXTRACT,UPDATE,local_generator


class DecisionPatchTests(unittest.TestCase):
    def setUp(self):
        import nltk
        nltk.data.path.insert(0,str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))
        self.request=dict(earlier=[dict(id='old',source=dict(text='We deferred launch because the permit was absent. The owner is Ren.'))],
                          incoming=dict(id='new',source=dict(text='The permit is now granted. The owner is Tao.')))
        self.changed=dict(decision_id='D0',assessment='changed',patches=[dict(op='replace',path='/basis',
            value=dict(source_id='new',sentence_ids=[0]))])
        self.correction=dict(kind='correction',target='old',old_sentence_ids=[0],new_sentence_ids=[0],
            old_assertion_id=0,new_assertion_id=0,reason='Wrong relation from baseline.')
        self.calls=[]
    def generate(self,updates=None,extra=None):
        def reply(system,content):
            data=json.loads(content);self.calls.append((system,data))
            if system==EXTRACT:
                self.assertNotIn('incoming',data)
                return json.dumps(dict(sources=[dict(target='old',decisions=[dict(decision_sentence_ids=[0],basis_sentence_ids=[0])])]))
            if system==UPDATE:return json.dumps(dict(updates=updates or [self.changed]))
            return json.dumps(dict(relations=[self.correction]+(extra or [])))
        return reply
    def test_verified_decision_endpoint_cannot_receive_baseline_correction(self):
        out=json.loads(compare_sources(self.generate(),json.dumps(self.request)))
        self.assertEqual([x['kind'] for x in out['relations']],['reconsider'])
        p=out['relations'][0]
        self.assertIn('permit was absent',p['reason']);self.assertIn('permit is now granted',p['reason'])
        self.assertEqual(len(out['suppressed_decision_candidates']),1)
        self.assertEqual(p['state_delta']['before']['decision'],p['state_delta']['after']['decision'])
    def test_unchanged_basis_suppresses_false_positive_without_parse_failure(self):
        out=json.loads(compare_sources(self.generate([dict(decision_id='D0',assessment='unchanged',patches=[])]),json.dumps(self.request)))
        self.assertEqual(out['relations'],[]);self.assertNotIn('selection_error',out)
        self.assertEqual(out['comparison_audit'][0]['outcome'],'unchanged')
    def test_unrelated_fact_in_same_source_still_reaches_owner_review(self):
        extra=dict(self.correction,old_sentence_ids=[1],new_sentence_ids=[1],old_assertion_id=1,new_assertion_id=1)
        out=json.loads(compare_sources(self.generate(extra=[extra]),json.dumps(self.request)))
        self.assertEqual({x['kind'] for x in out['relations']},{'correction','reconsider'})
        fact=next(x for x in out['relations'] if x['kind']=='correction')
        self.assertEqual(fact['old_assertion'],'The owner is Ren.')
    def test_changing_action_or_missing_decision_is_a_visible_failure(self):
        bad=dict(self.changed,patches=[dict(op='replace',path='/decision',value=dict(source_id='new',sentence_ids=[0]))])
        out=json.loads(compare_sources(self.generate([bad]),json.dumps(self.request)))
        self.assertIsNone(out['relations']);self.assertIn('Only basis',out['selection_error'])
    def test_guided_json_reaches_http_without_changing_nonthinking_or_qa(self):
        import httpx
        from llama_index.llms.openai_like import OpenAILike
        seen=[]
        def response(request):
            seen.append(json.loads(request.content))
            return httpx.Response(200,json=dict(id='fake',object='chat.completion',created=0,model='test',
                choices=[dict(index=0,message=dict(role='assistant',content='{}'),finish_reason='stop')],
                usage=dict(prompt_tokens=1,completion_tokens=1,total_tokens=2)))
        with httpx.Client(transport=httpx.MockTransport(response)) as client:
            llm=OpenAILike(model='test',api_base='http://localhost:1/v1',api_key='fake',is_chat_model=True,
                max_tokens=1024,http_client=client,max_retries=0,
                additional_kwargs=dict(extra_body=dict(chat_template_kwargs=dict(enable_thinking=False))))
            generate=local_generator(llm)
            schema=dict(type='object',properties={})
            generate.structured('system','user',schema);generate('system','user')
            self.assertEqual(seen[0]['guided_json'],schema)
            self.assertEqual(seen[0]['chat_template_kwargs'],dict(enable_thinking=False))
            self.assertNotIn('guided_json',seen[1]);self.assertEqual(llm.max_tokens,1024)


if __name__=='__main__':unittest.main()
