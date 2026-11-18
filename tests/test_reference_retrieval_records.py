"""Opt-in records-aligned retrieval: claim-span index units (B1) and the condition filter (B2).

Real LlamaIndex/BM25 with mock embeddings and stub extractors. These tests check
wiring and rules only; retrieval quality is not measured here.
"""
import json
from pathlib import Path
import unittest

from tests import test_reference_qa as reference
from tests import test_reference_module_adapters as adapters

TEXT = 'Only with dataset v1. The tuned lr is 0.01. Archive is Orion. We meet weekly.'


def extractor(*claims):
    return lambda *_: json.dumps({'claims': [dict(claim=c, condition=k, basis=[], time=[], subject=[],
                                                  stance='observation') for c, k in claims]})


@unittest.skipUnless(reference.AVAILABLE, 'reference dependencies and tokenizer required')
class RecordIndexTests(unittest.TestCase):
    setUp = adapters.ModuleFlowTests.setUp
    compare = adapters.ModuleFlowTests.compare
    respond = adapters.ModuleFlowTests.respond
    make = adapters.ModuleFlowTests.make
    call = adapters.ModuleFlowTests.call
    source = adapters.ModuleFlowTests.source

    def graph_source(self, text=TEXT, claims=(([1], [0]),), owner='hana', location='test:old'):
        from team_memory.records.graph import construct
        return construct(self.source(text, owner, location), extractor(*claims), model='test-stub')

    def team_reader(self):
        from team_memory.reference_qa import ReferenceQA
        return ReferenceQA(Path(self.temp.name) / 'reader', profile='team', **self.options)

    def test_claim_group_spans_then_leftover_sentences(self):
        from team_memory.readers.indexing import record_index_spans
        units = [dict(id=f'u{i}', start=a, end=b) for i, (a, b) in enumerate([(0, 21), (22, 43), (44, 61), (62, 77)])]
        graph = dict(units=units, claims=[dict(claim=['u1'], condition=['u0'], basis=[], time=[], subject=[])])
        self.assertEqual(record_index_spans(graph, TEXT, len, 100), [(0, 43), (44, 61), (62, 77)])
        self.assertEqual(TEXT[0:43], 'Only with dataset v1. The tuned lr is 0.01.')
        # A claim group longer than the limit falls back to its own sentences.
        self.assertEqual(record_index_spans(graph, TEXT, len, 30), [(0, 21), (22, 43), (44, 61), (62, 77)])
        far = dict(units=units, claims=[dict(claim=['u3'], condition=['u0'], basis=[], time=[], subject=[])])
        # A group spans the original text between its sentences; unused sentences stay indexed too.
        self.assertEqual(record_index_spans(far, TEXT, len, 100), [(0, 77), (22, 43), (44, 61)])

    def test_record_nodes_carry_the_chunk_node_metadata(self):
        from team_memory.adapters.legacy import envelope
        from team_memory.readers.indexing import RECORD_INDEX_UNIT, document_nodes
        reader = self.team_reader()
        source = self.graph_source()
        chunk = document_nodes(reader, source['id'], envelope(source))
        reader.index_config['index_unit'] = RECORD_INDEX_UNIT
        record = document_nodes(reader, source['id'], envelope(source))
        self.assertEqual([n.get_content() for n in record],
                         ['Only with dataset v1. The tuned lr is 0.01.', 'Archive is Orion.', 'We meet weekly.'])
        for node in record:
            self.assertEqual(set(node.metadata), set(chunk[0].metadata))
            self.assertEqual(node.excluded_llm_metadata_keys, chunk[0].excluded_llm_metadata_keys)
            self.assertEqual(node.excluded_embed_metadata_keys, chunk[0].excluded_embed_metadata_keys)
            self.assertEqual(node.ref_doc_id, source['id'])
            self.assertEqual(TEXT[node.metadata['parent_start']:node.metadata['parent_end']], node.get_content())

    def test_index_key_follows_the_graph_only_in_records_mode(self):
        from copy import deepcopy
        from team_memory.adapters.legacy import envelope
        from team_memory.readers.indexing import RECORD_INDEX_UNIT, specification
        reader = self.team_reader()
        source = self.graph_source()
        changed = deepcopy(source)
        changed['record_graph']['claims'] = []
        one, two = {source['id']: envelope(source)}, {source['id']: envelope(changed)}
        self.assertEqual(specification(reader, one), specification(reader, two))
        reader.index_config['index_unit'] = RECORD_INDEX_UNIT
        self.assertNotEqual(specification(reader, one), specification(reader, two))

    # B1 through the adapters, with index_unit='records' in the reader factory.

    def make_records(self, path):
        from team_memory.adapters.runtime import connect_v2
        from team_memory.readers.attribution import AttributedQA
        g = connect_v2(path, workspace_id='demo', generate=self.compare,
                       reader_factory=lambda store: AttributedQA(store, index_unit='records', **self.options))
        if not hasattr(self, 'preparers'):
            self.preparers = {}
        self.preparers[g.records] = g.retrieval
        return g

    def append(self, g, source, key):
        result = self.call(g.records, 'record.append', dict(source=source, expected_revision=g.records.snapshot()['revision'],
                                                             idempotency_key=key))
        self.assertEqual(result['status'], 'ok', result)

    def retrieve(self, g, text, conditions=()):
        return self.call(g.retrieval, 'evidence.retrieve', dict(snapshot=g.records.snapshot(),
            query=dict(text=text, time_scope='current', as_of=None, conditions=list(conditions)), max_evidence=10))

    def test_records_unit_is_opt_in_and_retrieves_claim_spans(self):
        from team_memory.reference_qa import ReferenceQA
        self.assertNotIn('index_unit', ReferenceQA(Path(self.temp.name) / 'plain', **self.options).index_config)
        with self.assertRaises(ValueError):
            ReferenceQA(Path(self.temp.name) / 'bad', index_unit='words', **self.options)
        g = self.make_records(Path(self.temp.name) / 'records')
        self.append(g, self.graph_source(), 'graph')
        self.append(g, self.source('A note without records structure.', location='test:plain'), 'plain')
        reader = g.retrieval.reader(g.records.snapshot())
        index = reader._index(reader.store.load('sources'))
        self.assertEqual(sorted(n.get_content() for n in index.docstore.docs.values()),
                         sorted(['Only with dataset v1. The tuned lr is 0.01.', 'Archive is Orion.', 'We meet weekly.',
                                 'A note without records structure.']))
        result = self.retrieve(g, 'What is the tuned lr?')
        self.assertEqual(result['status'], 'ok', result)
        self.assertTrue(result['data']['evidence'])
        self.assertEqual(self.calls, [])

    # B2: the condition filter on the default chunk index.

    def conditioned(self):
        g = self.make(Path(self.temp.name) / 'conditions')
        self.append(g, self.graph_source(), 'v1')
        self.append(g, self.graph_source('With dataset v2. The tuned lr is 0.1.', location='test:v2'), 'v2')
        self.append(g, self.source('Archive is Orion.', location='test:plain'), 'plain')
        return g

    @staticmethod
    def locations(result):
        return sorted({e['location'] for e in result['data']['evidence'] if e['kind'] == 'source'})

    def test_condition_filter_drops_only_explicitly_different_conditions(self):
        g = self.conditioned()
        off = self.retrieve(g, 'What is the tuned lr?', ['dataset v1'])
        self.assertEqual(self.locations(off), ['test:old', 'test:plain', 'test:v2'])
        g.retrieval.condition_filter = True
        on = self.retrieve(g, 'What is the tuned lr?', ['Dataset  V1'])
        self.assertEqual(on['status'], 'ok', on)
        self.assertEqual(self.locations(on), ['test:old', 'test:plain'])  # v2 states another condition
        traces = [json.loads(p.read_text(encoding='utf-8')) for p in (Path(g.retrieval.cache_root) / 'traces').glob('*.json')]
        [trace] = [t for t in traces if 'condition_filter' in t]
        self.assertEqual(trace['condition_filter']['requested'], ['Dataset  V1'])
        self.assertEqual({item['source_id'] for item in trace['condition_filter']['excluded']},
                         {s['id'] for s in g.records.snapshot()['sources'] if s['location'] == 'test:v2'})

    def test_condition_filter_without_conditions_changes_nothing(self):
        g = self.conditioned()
        off = self.retrieve(g, 'What is the tuned lr?')
        g.retrieval.condition_filter = True
        self.assertEqual(self.retrieve(g, 'What is the tuned lr?'), off)
        with self.assertRaises(ValueError):
            from team_memory.adapters.retrieval import RetrievalAdapter
            RetrievalAdapter('demo', None, self.temp.name, snapshot_loader=None, condition_filter='yes')


if __name__ == '__main__':
    unittest.main()
