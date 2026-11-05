"""Independent audit rejects changed actual inputs, usage and response bindings."""
from copy import deepcopy
import unittest

from evaluation.cupmem.audit import digest
from evaluation.cupmem.local_verify import serving_checks


class ServingEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.config = dict(actor='Qwen3-8B', max_model_len=131072, direct_protocol='qwen_token_budget')
        messages = [dict(role='user', content='Exact original text')]
        context = dict(uid='fixed-case', arm='direct', phase='answer', query_label='dim1_query')
        self.pre = dict(event='context_preflight', logical_context_check=1, context=context,
                        messages_sha256=digest(messages), actual_qwen_input_tokens=120000,
                        output_reservation=8192, max_model_len=131072, thinking=False,
                        direct_protocol='qwen_token_budget', compatible=True)
        self.check = dict(event='server_usage_check', logical_context_check=1, context=context,
                          messages_sha256=digest(messages), expected_qwen_input_tokens=120000,
                          reported_prompt_tokens=120000, usage_present=True, compatible=True,
                          response_id='local-response-1', reported_model='Qwen3-8B')
        self.requests = {1: dict(context=context, body=dict(messages=messages, max_tokens=8192,
                            chat_template_kwargs=dict(enable_thinking=False)))}
        self.terminal = {1: dict(event='response', status=200, body=dict(id='local-response-1',
                           model='Qwen3-8B', usage=dict(prompt_tokens=120000)))}

    def call(self, rows=None, requests=None, terminal=None):
        return serving_checks(rows or [self.pre, self.check], requests or self.requests,
                              terminal or self.terminal, self.config)

    def test_exact_long_input_bound_to_physical_return(self):
        self.assertEqual(self.call()['verified_successful_responses'], 1)

    def test_changed_input_thinking_count_and_model_are_rejected(self):
        for kind in ('text', 'thinking', 'count', 'model', 'response_id'):
            requests, terminal = deepcopy(self.requests), deepcopy(self.terminal)
            if kind == 'text':
                requests[1]['body']['messages'][0]['content'] += ' silently changed'
            elif kind == 'thinking':
                requests[1]['body']['chat_template_kwargs']['enable_thinking'] = True
            elif kind == 'count':
                terminal[1]['body']['usage']['prompt_tokens'] -= 1
            elif kind == 'model':
                terminal[1]['body']['model'] = 'another-model'
            else:
                terminal[1]['body']['id'] = 'unbound-response'
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.call(requests=requests, terminal=terminal)

    def test_successful_response_cannot_reuse_another_calls_check(self):
        requests, terminal = deepcopy(self.requests), deepcopy(self.terminal)
        requests[2], terminal[2] = deepcopy(requests[1]), deepcopy(terminal[1])
        with self.assertRaises(ValueError):
            self.call(requests=requests, terminal=terminal)

    def test_transport_retry_is_not_an_invented_returned_response(self):
        requests = {1: deepcopy(self.requests[1]), 2: deepcopy(self.requests[1])}
        terminal = {1: dict(event='transport_error', error_type='ReadTimeout'), 2: deepcopy(self.terminal[1])}
        self.assertEqual(self.call(requests=requests, terminal=terminal)['verified_successful_responses'], 1)

    def test_orphan_changed_or_missing_usage_check_rejected(self):
        for kind in ('orphan', 'changed_input', 'changed_count', 'missing_usage'):
            check = deepcopy(self.check)
            if kind == 'orphan': check['logical_context_check'] = 2
            elif kind == 'changed_input': check['messages_sha256'] = '0' * 64
            elif kind == 'changed_count': check['expected_qwen_input_tokens'] -= 1
            else: check['usage_present'] = False
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.call(rows=[self.pre, check])


if __name__ == '__main__':
    unittest.main()
