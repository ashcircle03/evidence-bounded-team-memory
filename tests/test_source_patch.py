"""Real RFC6902/ingest boundary tests; these do not establish LLM accuracy."""
import json
from pathlib import Path
import tempfile
import unittest
from copy import deepcopy

from team_memory.source_patch import apply_delta, compare_sources


class SourcePatchTests(unittest.TestCase):
    def setUp(self):
        import nltk
        nltk.data.path.insert(0, str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))
        self.record = dict(target='old', record_type='decision', subject='store', attribute='writer limit',
            value='1 writer', conditions='v1', sentence_ids=[0], assertion_id=0, decision_sentence_ids=[0])
        self.update = dict(record_id='R0', patches=[dict(op='replace', path='/value', value='4 writers')],
            evidence_mode='independent_report', sentence_ids=[0], assertion_id=0, reason='Changed writer limit.')

    def test_decision_endpoint_cannot_become_correction(self):
        r=deepcopy(self.record)
        result=apply_delta(r,dict(self.update,evidence_mode='explicit_correction'))
        self.assertEqual(result['kind'],'reconsider');self.assertEqual(r,self.record)
        self.assertEqual(result['before']['value'],'1 writer')
        self.assertEqual(result['after']['value'],'4 writers')

    def test_identity_patch_and_unchanged_premise_are_noops(self):
        for update in (dict(self.update,patches=[],evidence_mode='unchanged'),
                       dict(self.update,patches=[dict(op='replace',path='/value',value='1 writer')]),
                       dict(self.update,patches=[dict(op='replace',path='/conditions',value='v2')])):
            self.assertIsNone(apply_delta(self.record,update)['kind'])

    def test_identity_deletion_and_nonupdate_cannot_authorize_change(self):
        bad=[dict(self.update,patches=[dict(op='replace',path='/record_type',value='fact')]),
             dict(self.update,patches=[dict(op='remove',path='/value')]),
             dict(self.update,evidence_mode='unrelated'),dict(self.update,evidence_mode='unknown')]
        for u in bad:
            with self.assertRaises(ValueError):apply_delta(self.record,u)

    def test_fact_scope_and_explicit_correction_gate(self):
        fact=dict(self.record,record_type='fact',decision_sentence_ids=[])
        self.assertEqual(apply_delta(fact,self.update)['kind'],'conflict')
        self.assertEqual(apply_delta(fact,dict(self.update,evidence_mode='explicit_correction'))['kind'],'correction')
        diff=dict(self.update,patches=self.update['patches']+[dict(op='replace',path='/conditions',value='v2')])
        self.assertEqual(apply_delta(fact,diff)['kind'],'coexist')

    def test_causal_extraction_exact_witness_and_complete_update_accounting(self):
        request=dict(earlier=[dict(id='old',source=dict(text='We deferred writes because v1 permits 1 writer.'))],
            incoming=dict(id='new',source=dict(text='v2 permits 4 writers.')))
        calls=[]
        def generate(system,content):
            d=json.loads(content);calls.append(d)
            return json.dumps(dict(records=[self.record]) if 'incoming' not in d else dict(updates=[self.update]))
        result=json.loads(compare_sources(generate,json.dumps(request)))
        self.assertEqual(len(calls),2);self.assertNotIn('incoming',calls[0])
        p=result['relations'][0];self.assertEqual(p['kind'],'reconsider')
        self.assertEqual(p['old_quote'],request['earlier'][0]['source']['text'])
        self.assertEqual(p['new_quote'],request['incoming']['source']['text'])
        self.assertEqual(result['comparison_audit'][0]['delta']['after']['value'],'4 writers')
        def omit(system,content):return json.dumps(dict(records=[self.record]) if 'incoming' not in json.loads(content) else dict(updates=[]))
        failed=json.loads(compare_sources(omit,json.dumps(request)))
        self.assertIsNone(failed['relations']);self.assertIn('exactly one',failed['selection_error'])

    def test_invalid_delta_is_failed_receipt_not_successful_negative(self):
        from team_memory.source_store import SourceStore,source_envelope
        from team_memory import timeline
        def env(t,day):return source_envelope(dict(owner='A',observed_at=f'2026-01-0{day}T00:00:00Z',source=dict(text=t,speaker='A',location='test')))
        with tempfile.TemporaryDirectory() as root:
            store=SourceStore(root)
            timeline.ingest(store,env('Old.',1),lambda *_:'{"relations":[]}')
            r=timeline.ingest(store,env('New.',2),lambda *_:'{"relations":null,"selection_error":"Invalid patch","comparison_audit":[{"outcome":"invalid"}]}')
            self.assertTrue(r['errors']);self.assertEqual(r['proposals'],[])
            self.assertEqual(r['comparison_audit'],[dict(outcome='invalid')])
            self.assertEqual(timeline.receipts(store)[-1]['errors'],r['errors'])


if __name__ == '__main__':unittest.main()
