"""The retrieval adapter bridges each verified snapshot to the v2 reader once.

Real LlamaIndex/BM25 with mock embeddings and a stub decoder; output must not change.
"""
from threading import RLock
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from tests import test_reference_qa as reference
from tests import test_reference_module_adapters as adapters
from tests import test_reference_retrieval_budget as budget


@unittest.skipUnless(reference.AVAILABLE, 'reference dependencies and tokenizer required')
class ReaderReuseTests(unittest.TestCase):
    setUp = adapters.ModuleFlowTests.setUp
    compare = adapters.ModuleFlowTests.compare
    respond = adapters.ModuleFlowTests.respond
    make = adapters.ModuleFlowTests.make
    call = adapters.ModuleFlowTests.call
    source = adapters.ModuleFlowTests.source
    conflict_with_unrelated_record = budget.EvidenceBudgetTests.conflict_with_unrelated_record
    retrieve = budget.EvidenceBudgetTests.retrieve

    def test_same_snapshot_bridges_once_and_answers_the_same(self):
        from team_memory.adapters import retrieval
        g = self.conflict_with_unrelated_record()
        with patch.object(retrieval, 'reader_for', wraps=retrieval.reader_for) as bridge:
            first = self.retrieve(g, 10)
            second = self.retrieve(g, 3)
            third = self.retrieve(g, 10)
            self.assertEqual(bridge.call_count, 1)
            self.assertEqual(first, third)
            self.assertEqual(second['data']['coverage'], 'incomplete')
            # A new snapshot is bridged on its own. (The fixture's evidence.prepare after
            # record.append bridges separately and is not part of this cache.)
            self.call(g.records, 'record.append', dict(source=self.source('A later note.', location='test:later'),
                expected_revision=g.records.snapshot()['revision'], idempotency_key='later'))
            before = bridge.call_count
            self.retrieve(g, 10)
            self.retrieve(g, 10)
            self.assertEqual(bridge.call_count, before + 1)
        self.assertEqual(self.calls, [])

    def test_threshold_gate_does_not_stick_to_the_shared_reader(self):
        g = self.conflict_with_unrelated_record()
        off = self.retrieve(g, 10)
        g.retrieval.min_dense_score = g.retrieval.min_sparse_score = 1e9
        self.assertEqual(self.retrieve(g, 10)['data']['coverage'], 'no_hits')
        reader = g.retrieval.reader(g.records.snapshot())
        self.assertFalse(hasattr(reader, 'candidate_source'))
        g.retrieval.min_dense_score = g.retrieval.min_sparse_score = None
        self.assertEqual(self.retrieve(g, 10), off)

    def test_only_the_latest_readers_are_kept(self):
        from team_memory.adapters import retrieval
        adapter = retrieval.RetrievalAdapter('demo', None, self.temp.name, snapshot_loader=None)
        with patch.object(retrieval, 'reader_for', side_effect=lambda *_: SimpleNamespace(lock=RLock())):
            readers = [adapter.reader(dict(id=f's{i}')) for i in range(retrieval.READER_CACHE_SIZE + 2)]
            self.assertIs(adapter.reader(dict(id=f's{retrieval.READER_CACHE_SIZE + 1}')), readers[-1])
        self.assertEqual(list(adapter._readers), [f's{i}' for i in range(2, retrieval.READER_CACHE_SIZE + 2)])


if __name__ == '__main__':
    unittest.main()
