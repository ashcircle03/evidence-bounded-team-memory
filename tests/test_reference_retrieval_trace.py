"""Per-request retrieval traces and error codes; failures never become no_hits.

Real LlamaIndex/BM25 with mock embeddings and a stub decoder; not retrieval quality.
"""
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tests import test_reference_qa as reference
from tests import test_reference_module_adapters as adapters
from tests import test_reference_retrieval_budget as budget


@unittest.skipUnless(reference.AVAILABLE, 'reference dependencies and tokenizer required')
class RetrievalTraceTests(unittest.TestCase):
    setUp = adapters.ModuleFlowTests.setUp
    compare = adapters.ModuleFlowTests.compare
    respond = adapters.ModuleFlowTests.respond
    make = adapters.ModuleFlowTests.make
    call = adapters.ModuleFlowTests.call
    source = adapters.ModuleFlowTests.source
    conflict_with_unrelated_record = budget.EvidenceBudgetTests.conflict_with_unrelated_record
    retrieve = budget.EvidenceBudgetTests.retrieve

    @staticmethod
    def traces(g):
        return sorted((Path(g.retrieval.cache_root) / 'traces').glob('*.json'))

    def test_trace_is_written_and_repeats_except_timings(self):
        g = self.conflict_with_unrelated_record()
        first = self.retrieve(g, 3)
        [path] = self.traces(g)
        before = json.loads(path.read_text(encoding='utf-8'))
        self.retrieve(g, 3)
        self.assertEqual(self.traces(g), [path])
        after = json.loads(path.read_text(encoding='utf-8'))
        timings = before.pop('timings_ms')
        after.pop('timings_ms')
        self.assertEqual(before, after)
        self.assertLessEqual({'index', 'candidates', 'fusion', 'review_expansion', 'review_state', 'citations',
                              'spans', 'budget'}, set(timings))

        pid = g.records.snapshot()['proposals'][0]['id']
        self.assertEqual(before['candidate_source']['name'], 'llama-index-dense-bm25')
        self.assertEqual(list(before['candidates']), ['dense', 'sparse'])
        for item in before['candidates']['dense'] + before['candidates']['sparse'] + before['fused']:
            self.assertLessEqual({'rank', 'score', 'source_id', 'start', 'end'}, set(item))
        self.assertEqual(before['review_expansion']['proposal_ids'], [pid])
        self.assertEqual(before['review_state'], [pid])
        self.assertEqual([s['proposal_id'] for s in before['review_state_evidence']], [pid])
        self.assertEqual([d['reason'] for d in before['budget']['dropped']], ['below_budget_priority'])
        self.assertEqual(before['final_evidence_ids'], [e['id'] for e in first['data']['evidence']])
        self.assertEqual(before['outcome'], {'status': 'partial', 'codes': ['BUDGET_EXCEEDED']})
        self.assertIsNone(before['failure'])

    def test_withheld_proposal_sides_are_explained(self):
        g = self.conflict_with_unrelated_record()
        self.retrieve(g, 2)
        [path] = self.traces(g)
        dropped = json.loads(path.read_text(encoding='utf-8'))['budget']['dropped']
        pid = g.records.snapshot()['proposals'][0]['id']
        self.assertEqual(sorted((d['reason'], d['proposal_id']) for d in dropped),
                         [('proposal_sides_did_not_fit', pid)] * 2)

    def test_candidate_failure_is_retrieval_failed_not_no_hits(self):
        g = self.conflict_with_unrelated_record()
        with patch('team_memory.readers.retrieval_stages.LlamaIndexCandidates.retrieve',
                   side_effect=RuntimeError('secret-token-123')):
            result = self.retrieve(g, 10)
        self.assertEqual(result['status'], 'error', result)
        self.assertIsNone(result['data'])
        self.assertEqual([e['code'] for e in result['errors']], ['RETRIEVAL_FAILED'])
        [path] = self.traces(g)
        text = path.read_text(encoding='utf-8')
        trace = json.loads(text)
        self.assertEqual(trace['failure'], {'stage': 'candidates', 'exception': 'RuntimeError'})
        self.assertEqual(trace['outcome'], {'status': 'error', 'codes': ['RETRIEVAL_FAILED']})
        self.assertNotIn('secret-token-123', text)

    def test_unprepared_index_is_index_stale(self):
        from team_memory.readers.indexing import IndexNotReady
        g = self.conflict_with_unrelated_record()
        with patch('team_memory.readers.indexing.load', side_effect=IndexNotReady('not prepared')):
            result = self.retrieve(g, 10)
        self.assertEqual([e['code'] for e in result['errors']], ['INDEX_STALE'])
        self.assertIsNone(result['data'])
        [path] = self.traces(g)
        trace = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(trace['failure'], {'stage': 'index', 'exception': 'IndexNotReady'})
        self.assertEqual(trace['outcome']['codes'], ['INDEX_STALE'])

    def test_unwritable_trace_fails_the_request(self):
        g = self.conflict_with_unrelated_record()
        with patch('team_memory.adapters.retrieval.write_trace', side_effect=OSError('disk full')):
            result = self.retrieve(g, 10)
        self.assertEqual(result['status'], 'error', result)
        self.assertEqual([e['code'] for e in result['errors']], ['IO_FAILURE'])


if __name__ == '__main__':
    unittest.main()
