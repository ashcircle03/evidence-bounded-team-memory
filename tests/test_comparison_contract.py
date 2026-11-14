"""Deterministic inter-module contracts, not model classification scores."""
import json
from pathlib import Path
import tempfile
import unittest

from team_memory import timeline as t
from team_memory.store import Store, digest
from team_memory.source_comparison import compare_sources
from tests.test_timeline import env


class ComparisonContractTests(unittest.TestCase):
    def setUp(self):
        import nltk
        nltk.data.path.insert(0,str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'shared';self.store=Store(self.root)
        self.old=env('The limit is 10 seconds. The archive is Orion.')
        self.new=env('I correct the limit to 20 seconds. The archive is Orion.',day=2)
        t.ingest(self.store,self.old,lambda *_:'{}')

    def row(self,**overrides):
        return dict(dict(kind='correction',target=digest(self.old),old_sentence_ids=[0,1],
                    new_sentence_ids=[0,1],old_assertion_id=0,new_assertion_id=0,
                    reason='Explicit limit correction.'),**overrides)

    def ingest(self,rows):
        return t.ingest(self.store,self.new,
            lambda _,content:compare_sources(lambda *_:json.dumps(dict(relations=rows)),content))

    def test_malformed_reconsider_does_not_erase_correction_in_either_order(self):
        bad=self.row(kind='reconsider',old_sentence_ids=[99])
        for order in ([self.row(),bad],[bad,self.row()]):
            with self.subTest(order=order):
                root=Path(self.temp.name)/str(len(list(Path(self.temp.name).iterdir())))
                self.store=Store(root);t.ingest(self.store,self.old,lambda *_:'{}')
                receipt=self.ingest(order)
                self.assertEqual(len(receipt['proposals']),1)
                self.assertEqual(receipt['errors'][0]['stage'],'selection')
                p=t.proposals(self.store)[0];self.assertEqual(p['kind'],'correction')
                t.review(self.store,p['id'],'A','approve')
                self.assertEqual(t.assertion_status(t.witness(self.old,self.old['source']['text']),
                    '10 seconds',t.proposals(self.store)),'superseded_assertion')
                self.assertEqual(t.assertion_status(t.witness(self.old,self.old['source']['text']),
                    'Orion',t.proposals(self.store)),'reported')

    def test_selected_second_occurrence_survives_restart(self):
        self.old=env('The limit is 10 seconds. Later report. The limit is 10 seconds.')
        self.store=Store(Path(self.temp.name)/'repeated');t.ingest(self.store,self.old,lambda *_:'{}')
        receipt=self.ingest([self.row(old_sentence_ids=[2],old_assertion_id=2)])
        self.assertFalse(receipt['errors'])
        p=t.proposals(Store(self.store.root))[0]
        self.assertEqual(p['previous']['start'],self.old['source']['text'].rindex('The limit'))
        self.assertEqual(p['previous_assertion'],p['previous'])
        t.review(self.store,p['id'],'A','approve')
        first=t.witness(self.old,'The limit is 10 seconds.')
        self.assertEqual(t.assertion_status(first,'10 seconds',t.proposals(self.store)),'reported')
        self.assertEqual(t.assertion_status(p['previous'],'10 seconds',t.proposals(self.store)),'superseded_assertion')

    def test_forged_or_boolean_span_is_rejected(self):
        for span in (dict(start=True,end=24),dict(start=1,end=25)):
            with self.assertRaises(ValueError):t.witness(self.old,'The limit is 10 seconds.',span=span)

    def test_duplicate_targets_reject_both_without_suppressing_other_kind(self):
        rows=[self.row(),self.row(),self.row(kind='reconsider')]
        receipt=self.ingest(rows)
        self.assertEqual([p['kind'] for p in t.proposals(self.store)],['reconsider'])
        self.assertEqual(len(receipt['errors']),2)

    def test_timeout_is_persisted_not_retried_or_counted_as_negative(self):
        calls=[]
        def fail(*_):calls.append(1);raise TimeoutError('test timeout')
        first=t.ingest(self.store,self.new,fail)
        self.assertEqual(first['errors'][0]['stage'],'comparison_call')
        self.assertIn(digest(self.new),self.store.load('sources'))
        self.assertTrue(t.ingest(self.store,self.new,fail)['replayed'])
        self.assertEqual(calls,[1])

    def test_whole_malformed_output_remains_failure(self):
        r=t.ingest(self.store,self.new,lambda *_:'not json')
        self.assertTrue(r['errors']);self.assertEqual(r['proposals'],[])


if __name__=='__main__':unittest.main()
