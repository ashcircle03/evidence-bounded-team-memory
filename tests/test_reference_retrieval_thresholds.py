"""Optional score thresholds for "not in the records"; off by default.

Real LlamaIndex/BM25 with mock embeddings and a stub decoder. The threshold values
here only exercise the switch; real values are chosen later from development data.
"""
import json
from pathlib import Path
import unittest

from tests import test_reference_qa as reference
from tests import test_reference_module_adapters as adapters
from tests import test_reference_retrieval_budget as budget

HIGH, LOW = 1e9, -1e9


@unittest.skipUnless(reference.AVAILABLE, 'reference dependencies and tokenizer required')
class ScoreThresholdTests(unittest.TestCase):
    setUp = adapters.ModuleFlowTests.setUp
    compare = adapters.ModuleFlowTests.compare
    respond = adapters.ModuleFlowTests.respond
    make = adapters.ModuleFlowTests.make
    call = adapters.ModuleFlowTests.call
    source = adapters.ModuleFlowTests.source
    conflict_with_unrelated_record = budget.EvidenceBudgetTests.conflict_with_unrelated_record
    retrieve = budget.EvidenceBudgetTests.retrieve

    def gated(self, g, dense, sparse):
        g.retrieval.min_dense_score, g.retrieval.min_sparse_score = dense, sparse
        return self.retrieve(g, 10)

    def trace(self, g):
        [path] = (Path(g.retrieval.cache_root) / 'traces').glob('*.json')
        return json.loads(path.read_text(encoding='utf-8'))

    def test_default_is_off_and_low_thresholds_change_nothing(self):
        g = self.conflict_with_unrelated_record()
        self.assertEqual((g.retrieval.min_dense_score, g.retrieval.min_sparse_score), (None, None))
        off = self.retrieve(g, 10)
        self.assertNotIn('thresholds', self.trace(g))
        self.assertEqual(self.gated(g, LOW, LOW), off)

    def test_high_thresholds_give_no_hits_not_an_error(self):
        g = self.conflict_with_unrelated_record()
        result = self.gated(g, HIGH, HIGH)
        self.assertEqual(result['status'], 'ok', result)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['data']['coverage'], 'no_hits')
        self.assertEqual(result['data']['evidence'], [])
        self.assertEqual(result['data']['unresolved_proposal_ids'], [])
        trace = self.trace(g)
        self.assertEqual(trace['thresholds']['minimum'], {'dense': HIGH, 'sparse': HIGH})
        self.assertTrue(trace['thresholds']['excluded'])
        self.assertTrue(all({'channel', 'rank', 'score', 'source_id'} <= set(item)
                            for item in trace['thresholds']['excluded']))
        self.assertEqual(trace['candidate_source']['name'], 'llama-index-dense-bm25+thresholds')
        self.assertEqual(self.calls, [])

    def test_only_a_channel_with_a_threshold_can_let_a_candidate_pass(self):
        g = self.conflict_with_unrelated_record()
        off = self.retrieve(g, 10)
        # Dense gate only: BM25 hits cannot vouch, so nothing passes.
        self.assertEqual(self.gated(g, HIGH, None)['data']['coverage'], 'no_hits')
        # BM25 gate only, set low: every BM25 candidate passes and keeps its dense rank too.
        self.assertEqual(self.gated(g, None, LOW)['data'], off['data'])

    def test_thresholds_must_be_numbers(self):
        from team_memory.adapters.retrieval import RetrievalAdapter
        for bad in ('high', True):
            with self.assertRaises(ValueError):
                RetrievalAdapter('demo', None, self.temp.name, snapshot_loader=None, min_dense_score=bad)


if __name__ == '__main__':
    unittest.main()
