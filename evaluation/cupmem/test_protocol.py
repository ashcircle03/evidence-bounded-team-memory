"""Offline invariants; transport tests use HTTPX MockTransport, never a real API."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from .audit import Audit, BudgetStop, sdk_factory
from .upstream import direct_functions, model_record, select_pilot


class ProtocolTests(unittest.TestCase):
    def test_official_truncation_loads_dependencies_and_keeps_both_gold_sessions(self):
        # Local checkout or staged compute path, without loading a real tokenizer.
        root=Path(__file__).resolve().parents[3]/'campaigns/cupmem-stale/upstream'
        if not root.exists():
            root=Path('/ceph_data/pjw031003/capstone-shared-knowledge/runtime/cupmem-ea7d391103a1')
        with patch.dict(sys.modules, {'tiktoken': SimpleNamespace()}):
            funcs=direct_functions(root,'gpt-4o-mini')
        funcs['format_haystack']=lambda sessions,dates:sessions
        funcs['estimate_request_tokens']=lambda sessions,q,label:len(sessions)*100
        row=dict(haystack_session=[[dict(role='user',content=str(i))] for i in range(50)],
                 timestamps=[str(i) for i in range(50)], relevant_session_index=[3,46])
        sessions,dates,tokens,removed=funcs['trim_middle_noise_to_token_limit'](row,'dim1_query','?',1000)
        self.assertLessEqual(tokens,1000)
        self.assertEqual(removed,50-len(sessions))
        self.assertTrue({'3','46'}.issubset(set(dates)))
        self.assertEqual(len(row['haystack_session']),50)

    def make_audit(self, **limits):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        result = Audit(Path(tmp.name) / "audit.jsonl", limits=dict(requests=limits.get("requests", 10),
                     input_tokens=limits.get("input_tokens", 100000), output_tokens=limits.get("output_tokens", 100)))
        self.addCleanup(result.file.close)
        return result

    def test_gold_fields_are_not_passed_to_writer(self):
        row = dict(uid="one", haystack_session=[[dict(role="user", content="reported fact")]],
                   timestamps=["2026-01-01"], probing_queries={"dim1_query": "what?"},
                   M_old="GOLD_OLD", M_new="GOLD_NEW", explanation="GOLD_EXPLANATION",
                   relevant_session_index=[0, 1], type="Type I")
        visible = model_record(row)
        self.assertEqual(set(visible), {"uid", "haystack_session", "timestamps", "probing_queries"})
        self.assertNotIn("GOLD", json.dumps(visible))
        visible["haystack_session"][0][0]["content"] = "changed"
        self.assertEqual(row["haystack_session"][0][0]["content"], "reported fact")

    def test_pilot_selection_independent_of_input_order_and_answers(self):
        rows = [dict(uid=str(n), type=str(n % 2), M_new="answer") for n in range(12)]
        chosen = [r["uid"] for r in select_pilot(rows)]
        changed = [dict(r, M_new="a different answer") for r in reversed(rows)]
        self.assertEqual(chosen, [r["uid"] for r in select_pilot(changed)])

    def test_parallel_reservations_cannot_overspend(self):
        audit = self.make_audit(output_tokens=20)
        def reserve(_):
            try:
                return audit.start({"messages": [{"content": "hello"}]}, endpoint="mock", output_reservation=10)
            except BudgetStop:
                return None
        with ThreadPoolExecutor(max_workers=8) as pool:
            ids = list(pool.map(reserve, range(8)))
        self.assertEqual(sum(i is not None for i in ids), 2)
        self.assertEqual(audit.summary()["reserved_or_uncertain_output_tokens"], 20)

    def test_unknown_usage_keeps_reservation(self):
        audit = self.make_audit(output_tokens=20)
        rid = audit.start({"messages": [{"content": "hello"}]}, endpoint="mock", output_reservation=20)
        audit.finish(rid, status=503, body={"error": "temporary failure"}, elapsed=0)
        with self.assertRaises(BudgetStop):
            audit.start({"messages": [{"content": "retry"}]}, endpoint="mock", output_reservation=1)
        self.assertEqual(audit.summary()["uncertain_request_ids"], [rid])

    def test_known_usage_releases_only_unused_reservation(self):
        audit = self.make_audit(output_tokens=20)
        rid = audit.start({"messages": [{"content": "hello"}]}, endpoint="mock", output_reservation=20)
        audit.finish(rid, status=200, body={"usage": {"prompt_tokens": 5, "completion_tokens": 7}}, elapsed=0)
        with self.assertRaises(BudgetStop):
            audit.start({"messages": [{"content": "hello"}]}, endpoint="mock", output_reservation=14)
        audit.start({"messages": [{"content": "hello"}]}, endpoint="mock", output_reservation=13)

    def test_cap_truncation_stops_instead_of_becoming_answer(self):
        audit = self.make_audit()
        rid = audit.start({"messages": [{"content": "hello"}]}, endpoint="mock", output_reservation=20)
        with self.assertRaises(BudgetStop):
            audit.finish(rid, status=200, body={"usage": {"prompt_tokens": 2, "completion_tokens": 20},
                         "choices": [{"finish_reason": "length"}]}, elapsed=0)
        self.assertEqual(audit.summary()["censored_request_ids"], [rid])

    def test_retries_do_not_swallow_budget_stop(self):
        self.assertFalse(issubclass(BudgetStop, Exception))

    @unittest.skipUnless(importlib.util.find_spec("httpx") and importlib.util.find_spec("openai"), "SDK is on compute runtime")
    def test_physical_retry_is_logged_and_credentials_are_redacted(self):
        import httpx
        audit = self.make_audit(output_tokens=100)
        audit.secrets = ("mock-secret-do-not-persist",)
        seen = []
        def respond(request):
            body = json.loads(request.read())
            seen.append(body)
            if len(seen) == 1:
                return httpx.Response(429, json={"error": {"message": "mock-secret-do-not-persist"}},
                                      headers={"retry-after-ms": "1"})
            return httpx.Response(200, json={"id": "mock", "object": "chat.completion", "created": 0,
                  "model": "test", "choices": [{"index": 0, "finish_reason": "stop",
                  "message": {"role": "assistant", "content": "ok"}}],
                  "usage": {"prompt_tokens": 3, "completion_tokens": 1, "total_tokens": 4}})
        policy = {"base_url": "https://example.invalid/v1", "models": {
                  "test": {"output_limit_field": "max_tokens", "output_limit": 20}}}
        factory = sdk_factory(audit, policy=policy, transport=httpx.MockTransport(respond))
        client = factory(api_key="mock-secret-do-not-persist", base_url=policy["base_url"])
        self.addCleanup(client.close)
        out = client.chat.completions.create(model="test", messages=[{"role": "user", "content": "hello"}])
        self.assertEqual(out.choices[0].message.content, "ok")
        self.assertEqual(audit.summary()["requests"], 2)
        self.assertTrue(all(b["max_tokens"] == 20 for b in seen))
        log = audit.path.read_text()
        self.assertNotIn("mock-secret-do-not-persist", log)
        self.assertNotIn("Authorization", log)
        self.assertIn("REDACTED_CREDENTIAL", log)


if __name__ == "__main__":
    unittest.main()
