import json
import unittest
from team_memory.reference_demonstrated import demonstrations, select, generate, retrieve, direct
from tests.test_reference_connected import source, Decoder


class DemonstratedTests(unittest.TestCase):
    def test_original_demo_spans_and_sentence_links_roundtrip(self):
        for demo in demonstrations():
            sources = [source(i, s['text']) for i,s in enumerate(demo['sources'], 1)]
            llm = Decoder(json.dumps(demo['selection']), json.dumps(dict(sentences=demo['sentences'])))
            selection = select(demo['question'], sources, llm)
            output = generate(demo['question'], sources, selection, llm)
            self.assertEqual(output['status'], 'ok')
            self.assertEqual(len(output['answers']), len(demo['sentences']))
            self.assertEqual([c['text'] for c in output['claims']], [s['answer'] for s in demo['sentences']])

    def test_bad_source_not_silently_reassigned(self):
        llm = Decoder(json.dumps(dict(highlights=[dict(source_id=1, quote='Other source.')], missing_queries=[])))
        result = select('Q', [source(1, 'First.'), source(2, 'Other source.')], llm)
        self.assertEqual(result['highlights'], [])
        self.assertEqual(result['warnings'], ['selection_quote_not_located'])

    def test_invalid_answer_link_not_promoted(self):
        selection = dict(highlights=[dict(source_id=1, quote='Fact.')], warnings=[])
        llm = Decoder(json.dumps(dict(sentences=[dict(answer='Unbacked.', highlight_ids=[2])])))
        result = generate('Q', [source(1, 'Fact.')], selection, llm)
        self.assertEqual(result['answers'], [])
        self.assertEqual(result['status'], 'partial')

    def test_new_source_requires_new_selection_and_stops_on_duplicate(self):
        initial = [source(1, 'First.')]
        extra = source(2, 'Second.')
        selection = dict(highlights=[], missing_queries=['missing'], warnings=[])
        llm = Decoder(json.dumps(dict(highlights=[dict(source_id=2, quote='Second.')],
                                     missing_queries=['missing'])))
        sources, selected, trace = retrieve('Q', initial, selection, llm, lambda q:[extra])
        self.assertEqual(sources, initial+[extra])
        self.assertEqual(selected['highlights'][0]['source_id'], 2)
        self.assertEqual(len(llm.requests), 1)
        self.assertEqual(len(trace), 1)
        self.assertEqual(json.loads(llm.requests[0][-1].content)['sources'][1]['text'], 'Second.')

    def test_examples_cannot_be_cited_as_instance_sources(self):
        llm = Decoder(json.dumps(dict(answers=[dict(answer='Demo.', citations=[dict(source_id=2, quote='Demo.')])])))
        result = direct('Q', [source(1, 'Only actual source.')], llm)
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['answers'][0]['evidence'], [])


if __name__ == '__main__':
    unittest.main()
