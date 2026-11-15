"""Retrieval stage split: same nodes and order as before, repeatable bundles, replaceable candidates.

Real LlamaIndex/BM25 with mock embeddings and a stub decoder; not retrieval quality.
"""
from pathlib import Path
import unittest

from tests import test_reference_qa as reference
from tests import test_reference_module_adapters as adapters


@unittest.skipUnless(reference.AVAILABLE, 'reference dependencies and tokenizer required')
class RetrievalStageTests(unittest.TestCase):
    setUp = adapters.ModuleFlowTests.setUp
    compare = adapters.ModuleFlowTests.compare
    respond = adapters.ModuleFlowTests.respond
    make = adapters.ModuleFlowTests.make
    call = adapters.ModuleFlowTests.call
    source = adapters.ModuleFlowTests.source

    def catalogue(self):
        from team_memory.reference_qa import ReferenceQA
        service = ReferenceQA(self.temp.name, profile='team', **self.options)
        service.import_history([reference.ReferenceQAIntegration.source(
            self, f'Catalogue entry keynumber{i} is a preserved record.', f'test:catalogue/{i}') for i in range(20)])
        return service, service._index(service.store.load('sources'))

    def test_fusion_matches_the_previous_inline_retriever(self):
        from llama_index.core.retrievers import QueryFusionRetriever
        from team_memory.readers.retrieval_stages import LlamaIndexCandidates, StagedRetriever
        service, index = self.catalogue()
        for question in ('Catalogue entry keynumber7 is a preserved record.', 'preserved record', 'unrelated words'):
            # The construction ReferenceQA.ask used before the split.
            old = QueryFusionRetriever([index.as_retriever(similarity_top_k=4), service.sparse], llm=self.llm,
                similarity_top_k=8, num_queries=1, mode='reciprocal_rerank', use_async=False).retrieve(question)
            staged = StagedRetriever(LlamaIndexCandidates(index, 4, sparse=service.sparse, use_sparse=True),
                                     llm=self.llm, fused_top_k=8)
            new = staged.retrieve(question)
            self.assertEqual([(n.node.node_id, n.node.hash, n.score) for n in new],
                             [(n.node.node_id, n.node.hash, n.score) for n in old])
            record = staged.last
            self.assertEqual(list(record['candidates']), ['dense', 'sparse'])
            self.assertEqual([c.rank for c in record['candidates']['dense']], [1, 2, 3, 4])
            self.assertEqual([c.node_id for c in record['fused']], [n.node.node_id for n in new])
            # Channel scores are kept as retrieved, not the RRF scores fusion writes back.
            sparse = service.sparse.retrieve(question)
            self.assertEqual([(c.node_id, c.score) for c in record['candidates']['sparse']],
                             [(n.node.node_id, n.score) for n in sparse])

    def test_standard_profile_keeps_a_single_dense_channel(self):
        from team_memory.readers.retrieval_stages import LlamaIndexCandidates, StagedRetriever
        _, index = self.catalogue()
        staged = StagedRetriever(LlamaIndexCandidates(index, 4), llm=self.llm)
        new = staged.retrieve('preserved record')
        old = index.as_retriever(similarity_top_k=4).retrieve('preserved record')
        self.assertEqual([(n.node.node_id, n.score) for n in new], [(n.node.node_id, n.score) for n in old])
        self.assertEqual(list(staged.last['candidates']), ['dense'])

    def test_same_snapshot_and_question_give_the_same_bundle(self):
        path = Path(self.temp.name) / 'repeat'
        g = self.make(path)
        self.call(g.records, 'record.append', dict(source=self.source('Keep one writer because v4 permits one writer. Archive is Orion.'),
                                                   expected_revision=0, idempotency_key='old'))
        self.call(g, 'gateway.ingest', dict(source=self.source('v5 permits four writers.', 'jun', 'test:new'),
                                            expected_revision=1, idempotency_key='new'))
        snapshot = g.records.snapshot()
        payload = dict(snapshot=snapshot, query=dict(text='What changed?', time_scope='current', as_of=None, conditions=[]),
                       max_evidence=10)
        first = self.call(g.retrieval, 'evidence.retrieve', payload)
        second = self.call(g.retrieval, 'evidence.retrieve', payload)
        restarted = self.call(self.make(path).retrieval, 'evidence.retrieve', payload)
        self.assertEqual(first['status'], 'ok', first)
        self.assertEqual(first, second)
        self.assertEqual(first, restarted)
        self.assertIn('review_state', [e['kind'] for e in first['data']['evidence']])
        self.assertEqual(self.calls, [])


if __name__ == '__main__':
    unittest.main()
