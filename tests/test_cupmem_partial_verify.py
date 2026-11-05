"""Failure-oriented checks for partial artifact accounting; no network/model."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from evaluation.cupmem.audit import Audit, BudgetStop
from evaluation.cupmem.partial_verify import audit_events, verify_composer_output, verify_judge_answers, verify_writer_trace


class PartialAuditTests(unittest.TestCase):
    def make_run(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        config = dict(actor='mock', judge='judge', limits=dict(requests=2, input_tokens=10000, output_tokens=100),
                      policy=dict(base_url='https://example.invalid/v1', models={
                          'mock': dict(output_limit_field='max_tokens', output_limit=20),
                          'judge': dict(output_limit_field='max_tokens', output_limit=20)}))
        path = Path(tmp.name) / 'http.jsonl'
        log = Audit(path, limits=config['limits'])
        log.set_context(uid='case', arm='cupmem', phase='ingest')
        body = dict(model='mock', messages=[dict(role='user', content='source text')], max_tokens=20)
        rid = log.start(body, endpoint=config['policy']['base_url'] + '/chat/completions', output_reservation=20)
        log.failed(rid, TimeoutError())
        rid = log.start(body, endpoint=config['policy']['base_url'] + '/chat/completions', output_reservation=20)
        log.finish(rid, status=200, body=dict(model='mock', choices=[dict(finish_reason='stop')],
                   usage=dict(prompt_tokens=7, completion_tokens=3)), elapsed=1)
        with self.assertRaises(BudgetStop):
            log.start(body, endpoint='unused', output_reservation=20)
        log.file.close()
        return [json.loads(l) for l in path.read_text().splitlines()], config, log.summary()

    def test_stopped_run_retains_unknown_bill_and_retry(self):
        events, config, expected = self.make_run()
        actual, detail, _, _ = audit_events(events, config)
        self.assertEqual(actual, expected)
        self.assertEqual(actual['requests'], 2)
        self.assertEqual(actual['observed_input_tokens'], 7)
        self.assertGreater(actual['reserved_or_uncertain_input_tokens'], 0)
        self.assertEqual(actual['reserved_or_uncertain_output_tokens'], 20)
        self.assertEqual(detail['transport_errors'][0]['request_id'], 1)

    def test_missing_terminal_is_not_a_verified_partial(self):
        events, config, _ = self.make_run()
        with self.assertRaisesRegex(ValueError, 'Unterminated'):
            audit_events(events[:-1], config)

    def test_changed_model_input_rejected(self):
        events, config, _ = self.make_run()
        events[0]['body']['messages'][0]['content'] = 'answer substituted for source'
        with self.assertRaisesRegex(ValueError, 'Changed request body'):
            audit_events(events, config)

    def test_reused_physical_id_rejected(self):
        events, config, _ = self.make_run()
        events.insert(2, deepcopy(events[0]))
        with self.assertRaisesRegex(ValueError, 'nonsequential'):
            audit_events(events, config)

    def test_unknown_attempt_cannot_be_zeroed_to_fit_budget(self):
        events, config, _ = self.make_run()
        config['limits']['output_tokens'] = 30
        with self.assertRaisesRegex(ValueError, 'Output reservation cap exceeded'):
            audit_events(events, config)

    def test_duplicate_response_cannot_release_twice(self):
        events, config, _ = self.make_run()
        events.append(deepcopy(events[-1]))
        with self.assertRaisesRegex(ValueError, 'duplicate terminal'):
            audit_events(events, config)

    def test_allowed_model_cannot_substitute_for_the_other_role(self):
        events, config, _ = self.make_run()
        events[0]['context']['phase'] = 'official_judge'
        with self.assertRaisesRegex(ValueError, 'Model role'):
            audit_events(events, config)


class ArtifactLinkageTests(unittest.TestCase):
    def test_wrong_partial_uid_or_writer_text_rejected(self):
        trace = dict(sample_meta=dict(uid='right', session_mode='full', selected_session_indices=list(range(50)),
                                      M_old=None, M_new=None, explanation=None, relevant_session_index=None),
                     completed_session_count=1, session_logs=[dict(session_index=0, session_id='s_000',
                                      user_turns=[dict(turn_id='t_0', content='actual source')])])
        request = dict(context=dict(uid='right', arm='cupmem', phase='ingest'), body=dict(messages=[{}, dict(content=
            json.dumps(dict(session_id='s_000', bucket_track_schema='schema',
                            user_turns=[dict(turn_id='t_0', content='actual source')])))]))
        self.assertEqual(verify_writer_trace(trace, 'right', {1: request}), 1)
        with self.assertRaisesRegex(ValueError, 'Trace UID mismatch'):
            verify_writer_trace(trace, 'wrong', {1: request})
        trace['session_logs'][0]['user_turns'][0]['content'] = 'substituted source'
        with self.assertRaisesRegex(ValueError, 'Writer source differs'):
            verify_writer_trace(trace, 'right', {1: request})

    def test_judge_cannot_grade_a_different_arms_answer(self):
        queries = {f'dim{i}_query': dict(query_text=f'question{i}') for i in range(1, 4)}
        answers = {f'dim{i}_response': f'answer{i}' for i in range(1, 4)}
        sections = [f'[Dimension {i}: {name}]\nQuestion {i}: question{i}\nTarget Model Response {i}: answer{i}'
                    for i, name in enumerate(('Explicit Probing', 'Adversarial Robustness', 'Implicit Task'), 1)]
        text = '[Ground Truth Context]\ngold\n--------------------------------------------------\n' + '\n\n--------------------------------------------------\n'.join(sections) + '\n'
        request = dict(body=dict(messages=[{}, dict(content=text)]))
        verify_judge_answers(request, queries, answers)
        answers['dim2_response'] = 'another arm output'
        with self.assertRaisesRegex(ValueError, 'Judge question/target answer'):
            verify_judge_answers(request, queries, answers)

    def test_composer_question_and_full_rationale_are_checked(self):
        query = dict(query_text='question', answer=dict(answer='yes', brief_rationale='source supports yes'))
        payload = dict(query='question', parsed_query={}, canonical_answer_grounding={}, premise_verdict={},
                       action_readiness_verdict={}, constraint_set={})
        req = dict(body=dict(messages=[{}, dict(content=json.dumps(payload))]))
        res = dict(body=dict(choices=[dict(message=dict(content=json.dumps(query['answer'])))]))
        verify_composer_output(req, res, query)
        query['answer']['brief_rationale'] = 'changed explanation'
        with self.assertRaisesRegex(ValueError, 'answer/rationale'):
            verify_composer_output(req, res, query)
        query['query_text'] = 'different question'
        with self.assertRaisesRegex(ValueError, 'Composer question'):
            verify_composer_output(req, res, query)


if __name__ == '__main__':
    unittest.main()
