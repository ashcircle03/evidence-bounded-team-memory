"""Contracts and failure recovery, not model-accuracy tests."""
import json,unittest
from copy import deepcopy
from types import SimpleNamespace
from pathlib import Path


class ReferenceJointTests(unittest.TestCase):
    def setUp(self):
        import nltk
        nltk.data.path.insert(0,str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))
        self.w=[dict(source_id='doc',speaker='A',location='test:doc',start=10,end=50,quote='Amber was recorded.\nBlue was also recorded.')]

    def test_claims_with_same_document_remain_separate(self):
        from team_memory.reference_joint import format_joint
        raw=json.dumps(dict(answers=[dict(answer='First record: amber',citations=[dict(source_id=1,quote='Amber was recorded.')]),dict(answer='Second record: blue',citations=[dict(source_id=1,quote='Blue was also recorded.')])]))
        out=format_joint('What was recorded?',raw,self.w)
        self.assertEqual(len(out['answers']),2)
        self.assertEqual(out['status'],'ok')
        self.assertEqual(out['claims'][1]['quoted_spans'][0]['start'],30)

    def test_invalid_source_and_quote_are_distinct(self):
        from team_memory.reference_joint import format_joint
        out=format_joint('What?',json.dumps(dict(answers=[dict(answer='Amber',citations=[dict(source_id=1,quote='Invented quote.')])])),self.w)
        self.assertEqual(out['status'],'partial')
        self.assertEqual(out['answers'][0]['evidence'],self.w)
        self.assertEqual(out['claims'][0]['quoted_spans'],[])
        self.assertIn('quote_not_located',out['warnings'])
        bad=format_joint('What?',json.dumps(dict(answers=[dict(answer='Amber',citations=[dict(source_id=99,quote='Amber was recorded.')])])),self.w)
        self.assertEqual(bad['answers'][0]['evidence'],[])
        self.assertIn('out_of_range_source',bad['warnings'])

    def test_schema_prompt_and_empty_answer(self):
        from team_memory.reference_joint import joint_template,format_joint
        prompt=joint_template().format(context_str='Source 1: amber',query_str='What?')
        self.assertIn('Source 1: amber',prompt)
        self.assertIn('QuotedAnswer',prompt)
        self.assertEqual(format_joint('What?','{"answers":[]}',self.w)['status'],'insufficient')
        self.assertEqual(format_joint('What?','broken',self.w)['status'],'error')

    def test_optional_quote_timeout_keeps_original_answer(self):
        from team_memory.reference_qa import format_response
        from team_memory.reference_quotes import add_quote_citations
        before=format_response('What?', 'Amber. Answer: amber [1].',self.w)
        saved=deepcopy(before)
        class Broken:
            def chat(self,m):raise TimeoutError('injected')
        out=add_quote_citations('What?',before,Broken())
        self.assertEqual(out['answers'],before['answers'])
        self.assertEqual(out['raw'],before['raw'])
        self.assertEqual(out['status'],'partial')
        self.assertEqual(out['stage_failures'][0]['stage'],'quote_attribution')
        self.assertEqual(before,saved)

    def test_optional_repair_timeout_keeps_original_answer(self):
        from team_memory.reference_qa import format_response
        from team_memory.reference_attributed import repair_omitted_answer
        before=format_response('What?','Amber [1].',self.w)
        before.update(document_judgments=[dict(source_id='other',label='CONTRADICTS')],draft_raw=before['raw'],revised=True)
        class Broken:
            def chat(self,m):raise TimeoutError('injected')
        out=repair_omitted_answer('What?',before,Broken())
        self.assertEqual(out['answers'],before['answers'])
        self.assertEqual(out['raw'],before['raw'])
        self.assertEqual(out['stage_failures'][0]['stage'],'aqa_repair')


if __name__=='__main__':unittest.main()
