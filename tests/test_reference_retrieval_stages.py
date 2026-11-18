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

    def test_trace_records_stages_and_only_the_exception_type(self):
        import json
        from team_memory.readers.retrieval_stages import CandidateSource, LlamaIndexCandidates, StagedRetriever, Trace
        service, index = self.catalogue()
        trace = Trace()
        StagedRetriever(LlamaIndexCandidates(index, 4, sparse=service.sparse, use_sparse=True), llm=self.llm,
                        fused_top_k=8, trace=trace).retrieve('preserved record')
        self.assertEqual(set(trace.data), {'candidate_source', 'candidates', 'fused'})
        self.assertEqual(set(trace.timings_ms), {'candidates', 'fusion'})
        self.assertEqual(list(trace.data['candidates']), ['dense', 'sparse'])
        self.assertIsNone(trace.failure)
        json.dumps(trace.data)  # serialisable as written

        class Broken(CandidateSource):
            name, version = 'broken', '1'

            def retrieve(self, query_bundle):
                raise RuntimeError('secret-token-123')
        failed = Trace()
        with self.assertRaises(RuntimeError):
            StagedRetriever(Broken(), llm=self.llm, trace=failed).retrieve('anything')
        self.assertEqual(failed.failure, {'stage': 'candidates', 'exception': 'RuntimeError'})
        self.assertNotIn('secret-token-123', json.dumps([failed.data, failed.failure]))

    def test_citation_split_matches_the_upstream_engine(self):
        from llama_index.core.node_parser import SentenceSplitter
        from llama_index.core.query_engine import CitationQueryEngine
        from llama_index.core.schema import MetadataMode, NodeWithScore, TextNode
        from team_memory.readers.retrieval_stages import citation_nodes
        service, index = self.catalogue()
        nodes = index.as_retriever(similarity_top_k=4).retrieve('preserved record')
        long_text = ' '.join(f'Sentence {i} keeps a long record going.' for i in range(400))
        nodes.append(NodeWithScore(node=TextNode(text=long_text, metadata=dict(record_author='a', source_id='x')), score=0.5))
        nodes.append(NodeWithScore(node=TextNode(text='State text.', metadata=dict(record_author='r', evidence_type='review_state'),
                                                 excluded_llm_metadata_keys=['source_id']), score=None))
        for mode, chunk in ((MetadataMode.LLM, 1024), (MetadataMode.NONE, 64)):
            splitter = SentenceSplitter(chunk_size=chunk, chunk_overlap=0, include_metadata=False,
                                        tokenizer=lambda t: self.tokenizer.encode(t, add_special_tokens=False))
            engine = CitationQueryEngine(index.as_retriever(), llm=self.llm, text_splitter=splitter, metadata_mode=mode)
            expected = engine._create_citation_nodes(nodes)
            actual = citation_nodes(splitter, mode, nodes)
            self.assertGreater(len(actual), len(nodes))  # the long node is split
            self.assertEqual(
                [(n.score, n.node.get_content(metadata_mode=MetadataMode.NONE), n.node.metadata,
                  n.node.start_char_idx, n.node.end_char_idx, n.node.get_metadata_str(mode=MetadataMode.LLM)) for n in actual],
                [(n.score, n.node.get_content(metadata_mode=MetadataMode.NONE), n.node.metadata,
                  n.node.start_char_idx, n.node.end_char_idx, n.node.get_metadata_str(mode=MetadataMode.LLM)) for n in expected])

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

    def test_candidate_source_is_replaceable(self):
        from llama_index.core.schema import NodeWithScore
        from team_memory.readers.retrieval_stages import CandidateSource
        service, index = self.catalogue()
        chosen = next(n for n in index.docstore.docs.values() if 'keynumber13 ' in n.get_content())

        class Fixed(CandidateSource):
            name, version = 'fixed-test', '1'

            def retrieve(self, query_bundle):
                return {'dense': [NodeWithScore(node=chosen, score=1.0)]}

        service.candidate_source = lambda _index: Fixed()
        witnesses = service.ask('Anything at all?', retrieve_only=True)['witnesses']
        self.assertEqual([w['source_id'] for w in witnesses], [chosen.metadata['source_id']])
        self.assertEqual(self.calls, [])


if __name__ == '__main__':
    unittest.main()
