import json
from types import SimpleNamespace
import unittest

from team_memory.reference_connected import answer_from_sources, append_sources, bind_plan


def source(i, text, author='Ana'):
    return dict(source_id=str(i), quote=text, speaker=author, observed_at='2025-01-01',
                location=f'test:{i}', start=7, end=7+len(text))


class Decoder:
    def __init__(self, *responses):
        self.responses = iter(responses)
        self.requests = []

    def chat(self, messages):
        self.requests.append(messages)
        return SimpleNamespace(message=SimpleNamespace(content=next(self.responses)))


class ConnectedTests(unittest.TestCase):
    def test_unselected_sources_survive_and_ids_do_not_change_after_search(self):
        sources = [source(1, 'Task started Monday.'), source(2, 'Task ended Friday.')]
        new = source(3, 'The delivery was accepted Saturday.', 'Ben')
        plan = json.dumps(dict(groups=[dict(citations=[dict(source_id=1,
            quote='Task started Monday.')], purpose='Start date')], missing_queries=['delivery acceptance']))
        answer = json.dumps(dict(answers=[dict(answer='The task ended Friday.',
            citations=[dict(source_id=2, quote='Task ended Friday.')])]))
        llm = Decoder(plan, answer)
        result = answer_from_sources('When did it end? Begin with the option letter.', sources,
                                     llm, lambda q: [sources[0], new])
        final = json.loads(llm.requests[1][1].content)
        self.assertEqual([r['source_id'] for r in final['sources']], [1,2,3])
        self.assertEqual(final['sources'][1]['text'], sources[1]['quote'])
        self.assertEqual(final['sources'][2]['record_author'], 'Ben')
        self.assertEqual(result['answers'][0]['evidence'], [sources[1]])
        self.assertEqual(result['claims'][0]['evidence'], result['answers'][0]['evidence'])
        self.assertEqual(llm.requests[0][0].role.value, 'system')

    def test_plan_failure_does_not_delete_original_context_or_hide_failure(self):
        sources = [source(1, 'A permits retries.'), source(2, 'B forbids retries.')]
        answer = dict(answers=[dict(answer=w['quote'], citations=[dict(source_id=i,
            quote=w['quote'])]) for i,w in enumerate(sources,1)])
        llm = Decoder('I cannot produce the plan.', json.dumps(answer))
        result = answer_from_sources('What do A and B say?', sources, llm,
            lambda q: self.fail('Malformed plan must not trigger speculative searches'))
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(len(result['answers']), 2)
        self.assertIn('plan_parse_error', result['warnings'])
        self.assertEqual(len(json.loads(llm.requests[1][1].content)['sources']), 2)

    def test_invalid_quote_cannot_become_verified_plan(self):
        raw = json.dumps(dict(groups=[dict(purpose='Wrong', citations=[dict(
            source_id=1, quote='not in record')])], missing_queries=[]))
        plan, warnings = bind_plan(raw, [source(1, 'Actual source.')])
        self.assertEqual(plan['groups'], [])
        self.assertEqual(warnings, ['plan_quote_not_located'])

    def test_accumulation_is_bounded_and_preserves_distinct_spans(self):
        original = [source(0, 'First.')]
        extra = [source(i, f'Record {i}.') for i in range(1, 20)]
        merged = append_sources(original, original+extra+extra)
        self.assertEqual(len(merged), 9)
        self.assertEqual(merged[0], original[0])
        self.assertEqual(original, [source(0, 'First.')])

    def test_source_can_have_multiple_conflicting_answers_and_multi_source_claim(self):
        sources = [source(1, 'Mode A takes two days. Mode B takes four days.'),
                   source(2, 'Delivery adds one day.')]
        plan = dict(groups=[], missing_queries=[])
        answer = dict(answers=[dict(answer='Mode A with delivery takes three days.', citations=[
            dict(source_id=1, quote='Mode A takes two days.'),
            dict(source_id=2, quote='Delivery adds one day.')]),
            dict(answer='Mode B takes four days.', citations=[
                dict(source_id=1, quote='Mode B takes four days.')])])
        result = answer_from_sources('How long?', sources, Decoder(json.dumps(plan), json.dumps(answer)))
        self.assertEqual(len(result['claims']), 2)
        self.assertEqual(len(result['claims'][0]['evidence']), 2)
        self.assertEqual(result['claims'][1]['quoted_spans'][0]['quote'], 'Mode B takes four days.')
