"""Offline tests: no tokenizer download, server, credentials, or model inference."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from evaluation.cupmem.audit import BudgetStop, digest
from evaluation.cupmem.local_official import (
    ContextGuard, ContextIncompatible, ServingIncompatible, DIRECT_PROTOCOLS, LOCAL_API_KEY,
    compatibility_probes, execute_cases, load_direct_packets, local_sdk_factory,
    qwen_token_count, run_direct_packets, validate_config, validate_runtime,
)
from evaluation.cupmem.upstream import model_record


def config():
    return dict(execution_authorized=True, scope="local-pilot-two-full-sessions",
                base_url="http://127.0.0.1:8141/v1", actor="qwen-local", judge="qwen-local",
                model_repo="Qwen/Qwen3-8B", model_revision="b968826d9c46dd6066d109eabc6255188de91218",
                conda_prefix="/test/conda", direct_protocol="original_tiktoken",
                context_packets_path="/test/packets.json", context_packets_sha256="0" * 64,
                max_model_len=131072, max_output_tokens=8192,
                local_limits=dict(requests=10000, input_tokens=100000000, output_tokens=10000000),
                serving=dict(dtype="bfloat16", enable_thinking=False, vllm_version="0.8.5.post1",
                             rope_scaling=dict(rope_type="yarn", factor=4.0, original_max_position_embeddings=32768)))


class Tokenizer:
    def __init__(self, count=30):
        self.count = count
        self.calls = []

    def apply_chat_template(self, messages, **kwargs):
        self.calls.append((deepcopy(messages), kwargs))
        count = self.count(messages) if callable(self.count) else self.count
        return [1] * count


class AuditStub:
    def __init__(self):
        self.context = {}

    def set_context(self, **kwargs):
        self.context = kwargs

    def summary(self):
        return dict(requests=0)


class SDKBuilder:
    def __init__(self, response='{"ok":true}', prompt_tokens=30):
        self.requests, self.clients, self.options = [], [], []
        self.response = response
        self.prompt_tokens = prompt_tokens
        self.include_usage = True

    def __call__(self, audit, *, policy, transport):
        self.policy, self.audit, self.transport = policy, audit, transport

        def factory(**kwargs):
            self.clients.append(kwargs)

            def create(**request):
                self.requests.append(request)
                return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=self.response))],
                                       usage=SimpleNamespace(prompt_tokens=self.prompt_tokens) if self.include_usage else None,
                                       id="fake-response-" + str(len(self.requests)), model=request["model"])

            client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
            def with_options(**options):
                self.options.append(options)
                return client
            client.with_options = with_options
            return client
        return factory


def rows():
    return [dict(uid="case-" + str(i), type="T" + str(i),
                 haystack_session=[[dict(role="user", content="session " + str(j))] for j in range(50)],
                 timestamps=["time" + str(j) for j in range(50)],
                 probing_queries={"dim" + str(j) + "_query": "Question " + str(i) + "/" + str(j) + "?"
                                  for j in range(1, 4)}, M_old="GOLD-OLD", M_new="GOLD-NEW", explanation="GOLD")
            for i in (1, 2)]


def selection(chosen):
    return [dict(uid=r["uid"], type=r["type"], input_sha256=digest(model_record(r))) for r in chosen]


def write_packets(path, conf, chosen, *, counts=None, mutate=None):
    counts = counts or {v: 30 for v in DIRECT_PROTOCOLS}
    packets = []
    for variant in sorted(DIRECT_PROTOCOLS):
        for row in chosen:
            for label, question in row["probing_queries"].items():
                messages = [dict(role="system", content="Original system for " + label),
                            dict(role="user", content=variant + "\nFull frozen history\n" + question)]
                packets.append(dict(uid=row["uid"], query_label=label, variant=variant,
                                    messages=messages, messages_sha256=digest(messages),
                                    original_estimated_tokens=20, actual_qwen_input_tokens=counts[variant],
                                    output_reserved=conf["max_output_tokens"],
                                    context_fits=counts[variant] + conf["max_output_tokens"] <= conf["max_model_len"],
                                    retained_sessions=48, removed_sessions=2, gold_preserving_truncation=True))
    value = dict(selection=selection(chosen), model_revision=conf["model_revision"],
                 max_model_len=conf["max_model_len"], packets=packets)
    if mutate:
        mutate(value)
    path.write_text(json.dumps(value))
    conf.update(selection=selection(chosen), context_packets_path=str(path),
                context_packets_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    return value


class LocalOfficialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.conf, self.audit = config(), AuditStub()

    def guard(self, tokenizer=None):
        guard = ContextGuard(tokenizer or Tokenizer(), self.conf, self.audit, self.path / "context.jsonl")
        self.addCleanup(guard.file.close)
        return guard

    def test_explicit_config_only_loopback_and_finite_local_limits(self):
        validate_config(self.conf)
        for replacement in [dict(base_url="http://localhost:8141/v1"), dict(base_url="https://127.0.0.1:8141/v1"),
                            dict(base_url="http://127.0.0.1:8141/v1?forward=remote"),
                            dict(base_url="http://name:secret@127.0.0.1:8141/v1"),
                            dict(execution_authorized=False), dict(direct_protocol="auto"),
                            dict(judge="remote-model"), dict(context_packets_sha256=""),
                            dict(local_limits=dict(requests=0, input_tokens=3, output_tokens=3))]:
            with self.subTest(replacement=replacement), self.assertRaises(ValueError):
                validate_config({**self.conf, **replacement})

    def test_compute_gpu_conda_gate(self):
        env = dict(SLURM_JOB_ID="1", SLURMD_NODENAME="g1", SLURM_JOB_GPUS="0", CONDA_PREFIX="/test/conda")
        validate_runtime(self.conf, env, "/test/conda/bin/python", 1)
        for overrides, executable, gpu in [({"SLURM_JOB_ID": ""}, "/test/conda/bin/python", 1),
                ({"SLURMD_NODENAME": ""}, "/test/conda/bin/python", 1),
                ({"CONDA_PREFIX": "/other"}, "/test/conda/bin/python", 1),
                ({"SLURM_JOB_GPUS": ""}, "/test/conda/bin/python", 1),
                ({}, "/usr/bin/python", 1), ({}, "/test/conda/bin/python", 0)]:
            with self.subTest(overrides=overrides, gpu=gpu), self.assertRaises(RuntimeError):
                validate_runtime(self.conf, {**env, **overrides}, executable, gpu)

    def test_non_thinking_injection_preserves_messages_schema_temperature_and_retries(self):
        builder = SDKBuilder()
        self.conf["request_timeout_seconds"] = 900
        tokenizer = Tokenizer()
        factory = local_sdk_factory(self.audit, self.conf, self.guard(tokenizer), sdk_builder=builder,
                                    transport="fake transport")
        client = factory(api_key=LOCAL_API_KEY, base_url=self.conf["base_url"])
        messages = [dict(role="system", content="system"), dict(role="user", content="query"),
                    dict(role="assistant", content="invalid old output"), dict(role="user", content="native retry")]
        request = dict(model=self.conf["actor"], messages=messages, temperature=0.3,
                       response_format=dict(type="json_schema", json_schema=dict(name="x", strict=True, schema={})))
        original = deepcopy(request)
        client.chat.completions.create(**request)
        self.assertEqual(request, original)
        self.assertEqual(builder.requests[0], {**original, "extra_body": {"chat_template_kwargs": {"enable_thinking": False}}})
        self.assertEqual(builder.clients, [dict(api_key=LOCAL_API_KEY, base_url=self.conf["base_url"])])
        self.assertNotIn("max_retries", builder.clients[0])
        self.assertEqual(builder.options, [{"timeout": 900}])
        self.assertEqual(builder.transport, "fake transport")
        self.assertEqual(builder.policy["models"][self.conf["actor"]]["output_limit"], 8192)
        self.assertEqual(tokenizer.calls[0][1], dict(tokenize=True, add_generation_prompt=True, enable_thinking=False))

    def test_no_real_key_endpoint_model_or_extra_body_override(self):
        builder = SDKBuilder()
        factory = local_sdk_factory(self.audit, self.conf, self.guard(), sdk_builder=builder)
        for kwargs in [dict(api_key="different", base_url=self.conf["base_url"]),
                       dict(api_key=LOCAL_API_KEY, base_url="http://127.0.0.2:8141/v1")]:
            with self.assertRaises(BudgetStop):
                factory(**kwargs)
        client = factory(api_key=LOCAL_API_KEY, base_url=self.conf["base_url"])
        base = dict(model=self.conf["actor"], messages=[dict(role="user", content="q")])
        for override in [dict(model="another"), dict(extra_body={"messages": []}),
                         dict(extra_body={"chat_template_kwargs": {"enable_thinking": True}}),
                         dict(extra_body={"chat_template_kwargs": {"other": "override"}})]:
            with self.assertRaises(BudgetStop):
                client.chat.completions.create(**{**base, **override})
        self.assertEqual(builder.requests, [])

    def test_context_boundary_and_overflow_never_reaches_sdk(self):
        self.conf.update(max_model_len=100, max_output_tokens=20)
        tokenizer = Tokenizer(80)
        builder = SDKBuilder(prompt_tokens=80)
        guard = self.guard(tokenizer)
        client = local_sdk_factory(self.audit, self.conf, guard, sdk_builder=builder)(
            api_key=LOCAL_API_KEY, base_url=self.conf["base_url"])
        request = dict(model=self.conf["actor"], messages=[dict(role="user", content="exact")])
        client.chat.completions.create(**request)
        tokenizer.count = 81
        with self.assertRaises(ContextIncompatible) as caught:
            client.chat.completions.create(**request)
        self.assertNotIsInstance(caught.exception, Exception)
        self.assertEqual(len(builder.requests), 1)
        logs = [json.loads(line) for line in (self.path / "context.jsonl").read_text().splitlines()]
        preflights = [r for r in logs if r["event"] == "context_preflight"]
        self.assertEqual([r["compatible"] for r in preflights], [True, False])
        self.assertEqual(preflights[1]["rejected_request"]["messages"], request["messages"])

    def test_returned_server_usage_must_match_exact_template_before_answer_is_accepted(self):
        builder = SDKBuilder(prompt_tokens=30)
        guard = self.guard(Tokenizer(30))
        client = local_sdk_factory(self.audit, self.conf, guard, sdk_builder=builder)(
            api_key=LOCAL_API_KEY, base_url=self.conf["base_url"])
        request = dict(model=self.conf["actor"], messages=[dict(role="system", content="original"),
                       dict(role="user", content="question"), dict(role="assistant", content="invalid JSON"),
                       dict(role="user", content="unchanged native retry")])
        client.chat.completions.create(**request)
        builder.prompt_tokens = 29
        with self.assertRaises(ServingIncompatible) as caught:
            client.chat.completions.create(**request)
        self.assertNotIsInstance(caught.exception, Exception)
        failure = caught.exception.record
        self.assertEqual(failure["reason"], "prompt_token_mismatch")
        self.assertEqual(failure["expected_qwen_input_tokens"], 30)
        self.assertEqual(failure["reported_prompt_tokens"], 29)
        self.assertEqual(failure["messages_sha256"], digest(request["messages"]))
        self.assertEqual(failure["response_id"], "fake-response-2")
        self.assertEqual(len(builder.requests), 2)
        checks = [json.loads(line) for line in (self.path / "context.jsonl").read_text().splitlines()
                  if json.loads(line)["event"] == "server_usage_check"]
        self.assertEqual([r["compatible"] for r in checks], [True, False])
        self.assertEqual(checks[-1], failure)

    def test_missing_or_invalid_server_prompt_usage_is_explicit_incompatibility(self):
        builder = SDKBuilder()
        client = local_sdk_factory(self.audit, self.conf, self.guard(), sdk_builder=builder)(
            api_key=LOCAL_API_KEY, base_url=self.conf["base_url"])
        request = dict(model=self.conf["actor"], messages=[dict(role="user", content="question")])
        for include, count in ((False, 30), (True, None), (True, True), (True, -1)):
            builder.include_usage, builder.prompt_tokens = include, count
            with self.subTest(include_usage=include, prompt_tokens=count), self.assertRaises(ServingIncompatible) as caught:
                client.chat.completions.create(**request)
            self.assertEqual(caught.exception.record["reason"], "missing_or_invalid_prompt_usage")
            self.assertIsNone(caught.exception.record["reported_prompt_tokens"])
            self.assertEqual(caught.exception.record["usage_present"], include)

    def test_packet_binding_checks_all_six_and_keeps_exact_bytes(self):
        chosen = rows()
        packets = write_packets(self.path / "packets.json", self.conf, chosen)
        tokenizer = Tokenizer()
        direct = load_direct_packets(self.conf, tokenizer, chosen)
        self.assertEqual(len(direct["checks"]), 6)
        self.assertEqual(len(tokenizer.calls), 6)
        expected = {(p["uid"], p["query_label"]): p for p in packets["packets"] if p["variant"] == "original_tiktoken"}
        self.assertEqual(direct["packets"], expected)
        self.assertTrue(all(c["model_calls"] == 0 for c in direct["checks"]))

    def test_incompatible_primary_never_falls_back_to_smaller_variant(self):
        chosen = rows()
        self.conf.update(max_model_len=100, max_output_tokens=20)
        counts = dict(original_tiktoken=81, qwen_token_budget=50)
        write_packets(self.path / "packets.json", self.conf, chosen, counts=counts)
        tokenizer = Tokenizer(lambda messages: counts[messages[1]["content"].splitlines()[0]])
        with self.assertRaises(ContextIncompatible) as caught:
            load_direct_packets(self.conf, tokenizer, chosen)
        self.assertEqual(len(caught.exception.record["checks"]), 6)
        self.assertEqual(len(tokenizer.calls), 6)
        self.assertTrue(all("original_tiktoken" in msg[1]["content"] for msg, _ in tokenizer.calls))
        self.conf["direct_protocol"] = "qwen_token_budget"
        direct = load_direct_packets(self.conf, tokenizer, chosen)
        self.assertEqual(len(direct["packets"]), 6)
        self.assertEqual(direct["protocol"], "qwen_token_budget")

    def test_changed_file_missing_packet_token_count_or_question_refused(self):
        chosen = rows()
        path = self.path / "packets.json"
        write_packets(path, self.conf, chosen)
        path.write_text(path.read_text() + " ")
        with self.assertRaisesRegex(ValueError, "file changed"):
            load_direct_packets(self.conf, Tokenizer(), chosen)
        mutations = [lambda v: v["packets"].pop(),
                     lambda v: v["packets"].__setitem__(1, deepcopy(v["packets"][0])),
                     lambda v: v["packets"][0].__setitem__("actual_qwen_input_tokens", 31),
                     lambda v: v["packets"][0].__setitem__("removed_sessions", 1),
                     lambda v: v["selection"][0].__setitem__("input_sha256", "bad")]
        for mutate in mutations:
            write_packets(path, self.conf, chosen, mutate=mutate)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                load_direct_packets(self.conf, Tokenizer(), chosen)
        write_packets(path, self.conf, chosen)
        chosen[0]["probing_queries"]["dim1_query"] = "changed question"
        with self.assertRaisesRegex(ValueError, "question mismatch"):
            load_direct_packets(self.conf, Tokenizer(), chosen)

    def test_direct_uses_frozen_messages_and_saves_partial_before_failure(self):
        chosen = rows()
        write_packets(self.path / "packets.json", self.conf, chosen)
        direct = load_direct_packets(self.conf, Tokenizer(), chosen)
        calls = []
        def call(messages):
            calls.append(deepcopy(messages))
            return "answer-" + str(len(calls))
        result = run_direct_packets(SimpleNamespace(call_text=call), chosen[0], self.audit, direct, self.path)
        self.assertEqual(list(result), ["dim1_response", "dim2_response", "dim3_response"])
        for label, sent in zip(chosen[0]["probing_queries"], calls):
            self.assertEqual(sent, direct["packets"][(chosen[0]["uid"], label)]["messages"])
        self.assertEqual(json.loads((self.path / "case-1.direct.json").read_text())["answers"], result)
        def interrupted(messages):
            calls.append(messages)
            if len(calls) == 2:
                raise ContextIncompatible(dict(test=True))
            return "first preserved"
        calls.clear()
        with self.assertRaises(ContextIncompatible):
            run_direct_packets(SimpleNamespace(call_text=interrupted), chosen[1], self.audit, direct, self.path)
        partial = json.loads((self.path / "case-2.direct.partial.json").read_text())
        self.assertEqual(partial["answers"], {"dim1_response": "first preserved"})
        self.assertFalse((self.path / "case-2.direct.json").exists())

    def test_fresh_both_cases_native_helpers_and_partial_progress(self):
        chosen, calls = rows(), []
        self.conf["selection"] = selection(chosen)
        result = dict(completed=[])
        def cup(engine, row, index, audit, output):
            calls.append(("cup", row["uid"], index))
            return {"answer": "native"}
        def direct(actor, row, audit, funcs, output):
            calls.append(("direct", row["uid"]))
            return {"answer": "raw"}
        def judge(row, answers, arm, client, model, audit, funcs):
            calls.append(("judge", row["uid"], arm))
            return {"provisional": True}
        kwargs = dict(config=self.conf, engine=object(), actor=object(), judge=object(), audit=self.audit,
                      direct={}, grading={}, output=self.path, result=result, result_path=self.path / "result.json",
                      helpers=SimpleNamespace(cup=cup, direct=direct, judge=judge))
        execute_cases(chosen, chosen, **kwargs)
        self.assertEqual(calls[:2], [("direct", "case-1"), ("direct", "case-2")])
        self.assertEqual([r for r in calls if r[0] == "direct"], calls[:2])
        self.assertEqual([r[1] for r in calls if r[0] == "cup"], ["case-1", "case-2"])
        self.assertEqual(len(result["completed"]), 2)
        self.assertTrue(all(not r["judge_is_independent"] and not r["inherited_from_other_job"] for r in result["completed"]))
        with self.assertRaises(ValueError):
            execute_cases(chosen, chosen, **kwargs)
        result["completed"] = []
        with self.assertRaises(ValueError):
            execute_cases(chosen, chosen, **kwargs)
        result["direct_answers"] = {}
        def fail_second(*args):
            if args[1]["uid"] == "case-2":
                raise BudgetStop("finite limit")
            return cup(*args)
        kwargs["helpers"] = SimpleNamespace(cup=fail_second, direct=direct, judge=judge)
        with self.assertRaises(BudgetStop):
            execute_cases(chosen, chosen, **kwargs)
        self.assertEqual([r["uid"] for r in result["completed"]], ["case-1"])
        self.assertEqual(len(json.loads((self.path / "result.json").read_text())["completed"]), 1)
        self.assertEqual(result["direct_answers"], {"case-1": {"answer": "raw"}, "case-2": {"answer": "raw"}})

    def test_all_direct_answers_precede_cup_and_direct_failure_prevents_ingestion(self):
        chosen, calls = rows(), []
        self.conf["selection"] = selection(chosen)
        result = dict(completed=[])
        def cup(*args):
            calls.append("cup")
            raise AssertionError("CUP must not start after a direct failure")
        def direct(actor, row, *args):
            calls.append(row["uid"])
            if row["uid"] == "case-2":
                raise ContextIncompatible(dict(phase="direct", input_sha256="frozen"))
            return dict(dim1_response="saved", dim2_response="saved", dim3_response="saved")
        with self.assertRaises(ContextIncompatible):
            execute_cases(chosen, chosen, config=self.conf, engine=None, actor=None, judge=None,
                          audit=self.audit, direct={}, grading={}, output=self.path, result=result,
                          result_path=self.path / "result.json", helpers=SimpleNamespace(cup=cup, direct=direct, judge=None))
        self.assertEqual(calls, ["case-1", "case-2"])
        saved = json.loads((self.path / "result.json").read_text())
        self.assertEqual(saved["completed"], [])
        self.assertEqual(list(saved["direct_answers"]), ["case-1"])
        self.assertEqual(saved["active_stage"], dict(arm="direct", uid="case-2"))

    def test_probe_json_object_schema_and_exact_retry_shape(self):
        builder = SDKBuilder()
        client = local_sdk_factory(self.audit, self.conf, self.guard(), sdk_builder=builder)(
            api_key=LOCAL_API_KEY, base_url=self.conf["base_url"])
        retry_inputs = []
        def retry_builder(messages, failed):
            retry_inputs.append((deepcopy(messages), failed))
            return messages + [dict(role="assistant", content=failed), dict(role="user", content="unchanged native retry")]
        probes = compatibility_probes(client, self.conf, self.audit, retry_builder)
        self.assertEqual(len(probes), 3)
        self.assertEqual(builder.requests[0]["response_format"], {"type": "json_object"})
        self.assertTrue(builder.requests[1]["response_format"]["json_schema"]["strict"])
        self.assertNotIn("response_format", builder.requests[2])
        self.assertEqual([m["role"] for m in builder.requests[2]["messages"]], ["system", "user", "assistant", "user"])
        self.assertEqual(builder.requests[2]["messages"][:2], retry_inputs[0][0])
        self.assertTrue(all(r["max_tokens"] == 128 for r in builder.requests))
        builder.response = '{"ok":false}'
        with self.assertRaises(ValueError):
            compatibility_probes(client, self.conf, self.audit, retry_builder)


if __name__ == "__main__":
    unittest.main()
