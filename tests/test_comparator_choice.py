"""Frozen experiment boundaries, not model correctness."""
import json
from pathlib import Path
import tempfile
import unittest
from team_memory.service import TeamMemoryService
from team_memory.source_store import SourceStore
from team_memory import timeline
from evaluation.comparator_choice.prepare import oracle_inputs,HERE,ROOT


class ComparatorChoiceTests(unittest.TestCase):
    def setUp(self):
        import nltk
        nltk.data.path.insert(0,str(ROOT/'.cache/reference-nltk'))
    def test_oracle_uses_exact_source_selector_and_does_not_change_facts(self):
        class Reader:
            def __init__(self,p):self.store=SourceStore(p)
            def import_history(self,rows):return dict(status='ok',source_ids=[self.store.capture_source(x) for x in rows])
        for case in oracle_inputs()['cases']:
            with self.subTest(case=case['id']),tempfile.TemporaryDirectory() as root:
                def generate(_,content):
                    row=dict(case['selector'],target=json.loads(content)['earlier'][0]['id'])
                    return json.dumps(dict(relations=[row]))
                service=TeamMemoryService(root,reader=Reader(root),generate=generate)
                service.import_history(case['initial']);p=service.ingest(case['incoming'])['proposals'][0]
                self.assertEqual(p['kind'],'reconsider')
                service.review(p['id'],p['reviewer'],'approve')
                for span in (p['previous'],p['incoming']):
                    self.assertEqual(timeline.assertion_status(span,span['quote'],timeline.proposals(service.store)),'reported')
    def test_comparison_packets_share_inputs_and_production_code(self):
        a=ROOT/'results/comparator-choice/compare-8b-v1/runtime'
        b=ROOT/'results/comparator-choice/compare-14b-v1/runtime'
        self.assertEqual((a/'inputs.json').read_bytes(),(b/'inputs.json').read_bytes())
        ca,cb=[json.loads((p/'config.json').read_text()) for p in (a,b)]
        self.assertEqual(ca['code_sha256'],cb['code_sha256'])
        self.assertEqual(ca['expected_comparisons'],31)
        self.assertEqual(ca['expected_qa'],0)
        for p in (a,b):
            script=(p/'run.sbatch').read_text()
            self.assertIn('--time=12:00:00',script);self.assertIn('conda activate',script)
            self.assertNotIn('--nodelist',script)
            self.assertFalse((p/'new-key.json').exists())
    def test_new_case_source_locations_do_not_encode_target_relation(self):
        rows=json.loads((HERE/'compare-inputs.json').read_text())['cases']
        for c in rows:
            if c['split']!='new_authored':continue
            for env in c['initial']+[c['incoming']]:
                self.assertRegex(env['source']['location'],r'^authored-choice://[a-f0-9]{16}/[12]$')


if __name__=='__main__':unittest.main()
