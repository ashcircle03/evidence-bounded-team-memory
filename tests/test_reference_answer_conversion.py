"""Regression checks on fixed cited drafts through the official answering port."""
import unittest
from tests.test_reference_qa import AVAILABLE


@unittest.skipUnless(AVAILABLE, 'reference dependencies and tokenizer required')
class AnswerConversionTests(unittest.TestCase):
    def test_scope_and_conflict_ownership(self):
        from evaluation.answering_port.conversion import run
        rows = {r['case']: r for r in run()}
        self.assertTrue(all(row['raw_preserved'] for row in rows.values()))
        pending = rows['answer-pending-keeps-current']
        self.assertEqual(pending['conditions_at_generation'], [['v1', 'CPU'], ['v1', 'CPU'], []])
        self.assertEqual([c['conditions'] for c in pending['claims']], [['v1', 'CPU']] * 2)
        self.assertEqual([c['kind'] for c in pending['claims']], ['reported_fact', 'state'])
        self.assertIn('e-state', pending['claims'][1]['evidence_ids'])
        self.assertEqual(rows['answer-conflict-both-alternatives']['outcome'], 'conflict')
        for name in ('answer-unrelated-conflict-does-not-block', 'disjoint-quotes'):
            self.assertEqual(rows[name]['outcome'], 'answered')
            self.assertTrue(all(c['alternative_group'] is None for c in rows[name]['claims']))

        self.assertEqual(rows['answer-reconsider-is-not-correction']['outcome'], 'answered')
        direct = rows['answer-hook-v1']
        comparison = rows['answer-hook-by-version']
        self.assertEqual(direct['outcome'], 'answered')
        self.assertEqual(comparison['outcome'], 'conditional')
        expected = [(['v1', 'parallel hook invocation'], ['e-s-old']),
                    (['v2', 'parallel hook invocation'], ['e-s-new'])]
        for row, pairs in [(direct, expected[:1]), (comparison, expected)]:
            self.assertEqual([(c['conditions'], c['evidence_ids']) for c in row['claims']], pairs)
            for c in row['claims']:
                span = c['answer_span']
                self.assertEqual(c['text'], row['draft'][span['start']:span['end']])

    def test_grounding_and_generated_equivalence(self):
        from team_memory.readers.scoped import CitedFact, ScopedDraft, public_answer
        rows = [
            dict(id='old', kind='source', quote='Run failed.', conditions=['old']),
            dict(id='new', kind='source', quote='No successful completion.', conditions=['new']),
        ]
        packet = dict(snapshot={'id':'snapshot'}, evidence=rows)
        claims = [CitedFact(fact=r['quote'], evidence_id=r['id'], substring_quote=[r['quote']]) for r in rows]
        draft = ScopedDraft(claims=claims,comparison='Both fail.',same_answer=True,reason='')
        response = public_answer(draft, packet)
        self.assertEqual(response['outcome'], 'answered')
        self.assertEqual([c['evidence_ids'] for c in response['claims']], [['old'], ['new']])
        claims[0].substring_quote = ['imaginary']
        with self.assertRaises(ValueError):
            public_answer(draft, packet)

    def test_scoped_answer_resolves_the_selected_source_span(self):
        import json
        from types import SimpleNamespace
        from unittest.mock import Mock
        from team_memory.readers.scoped import generate_scoped, public_answer

        evidence = [dict(id='e1', kind='source', conditions=['archive'],
                         quote='등록됨.\n원본은 반환했다.', speaker='Kim', observed_at=None)]
        decision = dict(claims=[dict(fact='원본은 어떻게 됐나?', evidence_id='e1',
                                     substring_quote=['변형된 구절'])],
                        comparison='Single scope.', same_answer=True, reason='')
        raw = dict(claims=[dict(answer='원본을 반환했다.', evidence_id='e1')])
        model = Mock()

        def generate():
            model.chat.side_effect = [SimpleNamespace(message=SimpleNamespace(content=json.dumps(obj)))
                                      for obj in (decision, raw)]
            return generate_scoped(model, {'text': '원본은 어떻게 됐나?'}, evidence)

        draft = generate()
        self.assertEqual(draft.claims[0].substring_quote, [evidence[0]['quote']])
        result = public_answer(draft, dict(snapshot={'id': 's'}, evidence=evidence))
        self.assertEqual(result['claims'][0]['text'], raw['claims'][0]['answer'])
        self.assertEqual(result['claims'][0]['evidence_ids'], ['e1'])
        raw['claims'][0]['evidence_id'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'each selected evidence ID'):
            generate()
