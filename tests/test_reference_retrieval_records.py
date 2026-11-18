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


if __name__ == '__main__':
    unittest.main()
