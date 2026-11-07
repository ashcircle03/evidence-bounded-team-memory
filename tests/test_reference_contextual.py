"""Source-context integrity and metadata retrieval; no semantic model grading."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import unittest


HAS_REFERENCE = importlib.util.find_spec('llama_index') is not None


@unittest.skipUnless(HAS_REFERENCE, 'optional reference dependencies')
class ContextualTests(unittest.TestCase):
    def test_highlight_retains_author_date_condition_and_original_offsets(self):
        from team_memory.reference_contextual import answer_from_sources
        text = '@Ben The adapter finished Friday. With the legacy flag, failures are retried.'
        sources = [dict(source_id='record', quote=text, speaker='Ana',
            observed_at='2025-03-17 09:00:00', location='test:record', start=7, end=7+len(text))]
        requests = []
        responses = iter([
            json.dumps(dict(segments=[dict(source_id=1, quote='failures are retried.')])),
            json.dumps(dict(answers=[dict(answer='The legacy flag enables retries.',
                citations=[dict(source_id=1, quote='With the legacy flag, failures are retried.')])])),
        ])
        class Decoder:
            def chat(self, messages):
                requests.append(messages[0].content)
                return SimpleNamespace(message=SimpleNamespace(content=next(responses)))
        result = answer_from_sources('When are failures retried?', sources, Decoder())
        self.assertIn(text, requests[1])
        self.assertIn('"record_author": "Ana"', requests[1])
        self.assertIn('2025-03-17 09:00:00', requests[1])
        self.assertEqual(result['claims'][0]['evidence'], result['answers'][0]['evidence'])
        span = result['claims'][0]['quoted_spans'][0]
        self.assertEqual(text[span['start']-7:span['end']-7], span['quote'])

    def test_final_citations_cannot_refer_to_unshown_source(self):
        from team_memory.reference_contextual import answer_from_sources
        sources = [dict(source_id=str(i), quote=f'Record {i}.', speaker='Ana',
            location=f'test:{i}', start=0, end=9) for i in [1,2]]
        responses = iter(['{"segments":[{"source_id":2,"quote":"Record 2."}]}',
            '{"answers":[{"answer":"Unsupported","citations":[{"source_id":2,"quote":"Record 2."}]}]}'])
        class Decoder:
            def chat(self, messages):
                return SimpleNamespace(message=SimpleNamespace(content=next(responses)))
        result = answer_from_sources('Which record?', sources, Decoder())
        self.assertEqual(result['selection_records'][0]['retrieval_source_number'], 2)
        self.assertEqual(result['selection_records'][0]['source_id'], 1)
        self.assertEqual(result['answers'][0]['evidence'], [])
        self.assertIn('out_of_range_source', result['warnings'])

    def test_search_key_can_find_author_without_inventing_body_text(self):
        import nltk
        nltk.data.path.insert(0, str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))
        from llama_index.core.llms import MockLLM
        from team_memory.reference_retrieval import FeedbackRetriever
        class Tokenizer:
            def encode(self, text, **kwargs):
                return list(range(len(text.split())))
        sources = [dict(source_id=str(i), quote='The review is finished.',
            speaker=name, observed_at='2025-01-01', location=f'test:{i}',
            start=0, end=23) for i,name in enumerate(['Mira','Leo','Nora'])]
        retriever = FeedbackRetriever(sources, Tokenizer(), MockLLM(), top_k=1)
        found = retriever.witnesses(retriever.metadata.retrieve('Nora'))
        self.assertEqual(found[0]['speaker'], 'Nora')
        self.assertEqual(found[0]['quote'], 'The review is finished.')
        self.assertNotIn('Nora', found[0]['quote'])
