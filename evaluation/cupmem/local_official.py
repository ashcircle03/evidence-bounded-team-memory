"""Fresh local-Qwen CUPMem/STALE pilot using the pinned native helper functions.

This module never reads BAZE/OpenAI credentials. Model requests go only to a
loopback OpenAI-compatible server with a public dummy key. Source/data loading
and inference require an activated conda environment in a GPU Slurm allocation.
The launcher owns server setup and must record/verify its model revision and
static YaRN settings; this wrapper records them without claiming to inspect a
running server's private configuration.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from dataclasses import asdict
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace
from urllib.parse import urlsplit

from .audit import Audit, BudgetStop, canonical, digest, sdk_factory
from .official import run_cup, run_judge, save
from .upstream import (
    DATA_REVISION, DATA_SHA256, REVISION, judge_functions,
    load_data, model_record, select_pilot, verify_source,
)

LOCAL_API_KEY = "local-cupmem-no-secret"
DIRECT_PROTOCOLS = {"original_tiktoken", "qwen_token_budget"}


class ContextIncompatible(BaseException):
    """Escapes native Exception retries/fallbacks without truncating the input."""
    def __init__(self, record):
        self.record = deepcopy(record)
        super().__init__("Actual Qwen input plus output reservation exceeds the configured context")


class ServingIncompatible(BaseException):
    """A server/template compatibility failure, never a semantic model failure."""
    def __init__(self, record):
        self.record = deepcopy(record)
        super().__init__("Server prompt usage is absent or differs from the exact local Qwen template")


def validate_transport_config(config):
    """Shared local transport requirements; each runner validates its own scope."""
    url = urlsplit(config["base_url"])
    if (url.scheme != "http" or url.hostname != "127.0.0.1" or not url.port
            or not 1 <= url.port <= 65535 or url.path != "/v1"
            or url.username or url.password or url.query or url.fragment):
        raise ValueError("Only http://127.0.0.1:<port>/v1 is permitted for model calls")
    if config.get("model_repo") != "Qwen/Qwen3-8B":
        raise ValueError("This wrapper is fixed to the selected Qwen3-8B model family")
    revision = config.get("model_revision", "")
    if len(revision) != 40 or any(c not in "0123456789abcdef" for c in revision):
        raise ValueError("Pin an exact model revision")
    if not config.get("actor") or config.get("judge") != config["actor"]:
        raise ValueError("The explicitly labeled provisional self-judge uses the same served model")
    for key in ("max_model_len", "max_output_tokens"):
        if type(config.get(key)) is not int or config[key] <= 0:
            raise ValueError("Positive finite context/output limits required")
    if config["max_output_tokens"] >= config["max_model_len"]:
        raise ValueError("Output reservation leaves no input space")
    if set(config.get("local_limits", {})) != {"requests", "input_tokens", "output_tokens"}:
        raise ValueError("Explicit finite local request/token guardrails required")
    if any(type(v) is not int or v <= 0 for v in config["local_limits"].values()):
        raise ValueError("Local guardrails must be positive integers")
    serving = config["serving"]
    rope = serving.get("rope_scaling", {})
    if (serving.get("dtype") != "bfloat16" or serving.get("enable_thinking") is not False
            or rope.get("rope_type", rope.get("type")) != "yarn" or rope.get("factor") != 4.0
            or rope.get("original_max_position_embeddings") != 32768
            or not serving.get("vllm_version")):
        raise ValueError("Require declared BF16, non-thinking, static YaRN4 and pinned vLLM")


def validate_config(config):
    if config.get("execution_authorized") is not True or config.get("scope") != "local-pilot-two-full-sessions":
        raise ValueError("Explicit local two-case execution configuration required")
    validate_transport_config(config)
    if config.get("direct_protocol") not in DIRECT_PROTOCOLS:
        raise ValueError("Select a direct protocol explicitly; no automatic fallback")
    packet_hash = config.get("context_packets_sha256", "")
    if (not config.get("context_packets_path") or len(packet_hash) != 64
            or any(c not in "0123456789abcdef" for c in packet_hash)):
        raise ValueError("Pinned setup-generated direct packets are required")


def validate_runtime(config, environ, executable, visible_gpus):
    if not environ.get("SLURM_JOB_ID") or not environ.get("SLURMD_NODENAME"):
        raise RuntimeError("Run only on a Slurm compute node")
    if environ.get("CONDA_PREFIX") != config["conda_prefix"]:
        raise RuntimeError("Activate the project conda environment")
    if Path(executable).resolve().parent != Path(config["conda_prefix"]) / "bin":
        raise RuntimeError("Python is outside the configured conda environment")
    allocation = str(environ.get("SLURM_GPUS_ON_NODE", ""))
    if not environ.get("SLURM_JOB_GPUS") and not (allocation.isdigit() and int(allocation) >= 1):
        raise RuntimeError("An explicit Slurm GPU allocation is required")
    if type(visible_gpus) is not int or visible_gpus < 1:
        raise RuntimeError("At least one allocated visible GPU is required")


def qwen_token_count(tokenizer, messages):
    ids = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True,
                                        enable_thinking=False)
    if not isinstance(ids, list) or any(type(x) is not int for x in ids):
        raise TypeError("Expected untruncated Qwen chat-template token IDs")
    return len(ids)


class ContextGuard:
    """Local tokenizer accounting distinct from official tiktoken truncation."""
    def __init__(self, tokenizer, config, audit, path):
        self.tokenizer, self.config, self.audit = tokenizer, config, audit
        self.file = Path(path).open("x", encoding="utf-8")
        self.lock = threading.Lock()
        self.checked = 0

    def check(self, kwargs):
        messages = kwargs["messages"]
        if not isinstance(messages, list) or any(not isinstance(m.get("content"), str) for m in messages):
            raise BudgetStop("Only text message input is allowed")
        if "max_tokens" in kwargs and "max_completion_tokens" in kwargs:
            raise BudgetStop("Ambiguous output reservation")
        requested = kwargs.get("max_tokens", kwargs.get("max_completion_tokens", self.config["max_output_tokens"]))
        if type(requested) is not int or requested <= 0:
            raise BudgetStop("Invalid output reservation")
        output = min(requested, self.config["max_output_tokens"])
        # A single tokenizer instance is shared by native invalidation lanes.
        with self.lock:
            count = qwen_token_count(self.tokenizer, messages)
            self.checked += 1
            row = dict(event="context_preflight", logical_context_check=self.checked, context=deepcopy(self.audit.context),
                       messages_sha256=digest(messages), actual_qwen_input_tokens=count,
                       output_reservation=output, max_model_len=self.config["max_model_len"],
                       thinking=False, direct_protocol=self.config["direct_protocol"],
                       compatible=count + output <= self.config["max_model_len"])
            if not row["compatible"]:
                row["rejected_request"] = deepcopy(kwargs)
            self.file.write(canonical(row) + "\n")
            self.file.flush()
        if not row["compatible"]:
            raise ContextIncompatible(row)
        return row

    def check_response(self, checked, response):
        """Bind every returned response to its exact local-template token count.

        The physical transport audit has already preserved the raw response and
        accounted usage. This independent check prevents a server using another
        tokenizer/template (or silently shortening input) from being accepted as
        the declared run. Unknown usage cannot establish compatibility.
        """
        usage = getattr(response, "usage", None)
        reported = getattr(usage, "prompt_tokens", None)
        known = type(reported) is int and reported >= 0
        expected = checked["actual_qwen_input_tokens"]
        compatible = known and reported == expected
        row = dict(event="server_usage_check", logical_context_check=checked["logical_context_check"],
                   context=deepcopy(checked["context"]), messages_sha256=checked["messages_sha256"],
                   expected_qwen_input_tokens=expected,
                   reported_prompt_tokens=reported if known else None,
                   reported_prompt_tokens_type=type(reported).__name__, usage_present=usage is not None,
                   response_id=getattr(response, "id", None), reported_model=getattr(response, "model", None),
                   compatible=compatible,
                   reason="matched" if compatible else "prompt_token_mismatch" if known else "missing_or_invalid_prompt_usage")
        with self.lock:
            self.file.write(canonical(row) + "\n")
            self.file.flush()
        if not compatible:
            raise ServingIncompatible(row)
        return row


def local_sdk_factory(audit, config, guard, *, transport=None, sdk_builder=sdk_factory):
    """Preserve SDK/CUPMem behavior; add one declared Qwen chat-template option."""
    validate_transport_config(config)
    policy = dict(base_url=config["base_url"], models={config["actor"]: dict(
        output_limit_field="max_tokens", output_limit=config["max_output_tokens"])})
    native_factory = sdk_builder(audit, policy=policy, transport=transport)

    def factory(**kwargs):
        if kwargs.get("api_key") != LOCAL_API_KEY or kwargs.get("base_url") != config["base_url"]:
            raise BudgetStop("Only the dummy local key and pinned loopback endpoint are allowed")
        client = native_factory(**kwargs)
        # The native SDK still owns its normal retry policy. Optional request
        # timeout changes are recorded runtime settings, not semantic retries.
        if "request_timeout_seconds" in config:
            timeout = config["request_timeout_seconds"]
            if type(timeout) not in (int, float) or not 0 < timeout <= 3600:
                raise ValueError("Invalid finite request timeout")
            client = client.with_options(timeout=timeout)
        original_create = client.chat.completions.create

        def create(**request):
            request = deepcopy(request)
            if request.get("model") != config["actor"]:
                raise BudgetStop("Unexpected local served model alias")
            extra = request.setdefault("extra_body", {})
            if not isinstance(extra, dict) or set(extra) - {"chat_template_kwargs"}:
                raise BudgetStop("Unexpected extra_body")
            template = extra.setdefault("chat_template_kwargs", {})
            if not isinstance(template, dict) or set(template) - {"enable_thinking"}:
                raise BudgetStop("Unexpected chat-template override")
            if "enable_thinking" in template and template["enable_thinking"] is not False:
                raise BudgetStop("Thinking must remain disabled for both arms")
            template["enable_thinking"] = False
            checked = guard.check(request)
            response = original_create(**request)
            guard.check_response(checked, response)
            return response

        return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    return factory


def load_direct_packets(config, tokenizer, chosen):
    """Bind the exact six selected setup packets before any model inference.

    Preparation already ran the original gold-preserving removal function with
    its declared seed. Do not run its random selection a second time here.
    The other protocol variant is not a fallback and is never silently chosen.
    """
    raw = Path(config["context_packets_path"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != config["context_packets_sha256"]:
        raise ValueError("Setup context packet file changed")
    data = json.loads(raw)
    if (data["selection"] != config["selection"] or data["model_revision"] != config["model_revision"]
            or data["max_model_len"] != config["max_model_len"]):
        raise ValueError("Context packet provenance differs from the local run")
    questions = {(row["uid"], label): question for row in chosen for label, question in row["probing_queries"].items()}
    if (len(chosen) != 2 or len(questions) != 6 or any(set(row["probing_queries"]) !=
            {"dim1_query", "dim2_query", "dim3_query"} for row in chosen)):
        raise ValueError("Exactly two cases with three original probes are required")
    all_keys = {(p["uid"], p["query_label"], p["variant"]) for p in data["packets"]}
    if len(data["packets"]) != 12 or all_keys != {(uid, query, variant) for uid, query in questions for variant in DIRECT_PROTOCOLS}:
        raise ValueError("Expected six unique setup packets for each explicit protocol")
    selected, checks = {}, []
    for packet in data["packets"]:
        if packet["variant"] != config["direct_protocol"]:
            continue
        key = (packet["uid"], packet["query_label"])
        messages = packet["messages"]
        if (digest(messages) != packet["messages_sha256"] or len(messages) != 2
                or [m["role"] for m in messages] != ["system", "user"]
                or not messages[1]["content"].endswith(questions[key])):
            raise ValueError("Frozen direct message/question mismatch")
        actual = qwen_token_count(tokenizer, messages)
        if (actual != packet["actual_qwen_input_tokens"] or packet["output_reserved"] != config["max_output_tokens"]
                or packet["retained_sessions"] + packet["removed_sessions"] != 50
                or not 0 <= packet["retained_sessions"] <= 50
                or packet["gold_preserving_truncation"] is not True):
            raise ValueError("Frozen context token count, budget or session accounting changed")
        fits = actual + config["max_output_tokens"] <= config["max_model_len"]
        if fits != packet["context_fits"]:
            raise ValueError("Incorrect prepared context-fit flag")
        check = dict(uid=key[0], query_label=key[1], variant=packet["variant"],
                     messages_sha256=packet["messages_sha256"], actual_qwen_input_tokens=actual,
                     output_reservation=config["max_output_tokens"], max_model_len=config["max_model_len"],
                     compatible=fits, phase="frozen_direct_preflight", model_calls=0)
        checks.append(check)
        selected[key] = deepcopy(packet)
    if any(not check["compatible"] for check in checks):
        raise ContextIncompatible(dict(phase="frozen_direct_preflight", model_calls=0,
                                       direct_protocol=config["direct_protocol"], checks=checks))
    return dict(packets=selected, checks=checks, file_sha256=config["context_packets_sha256"],
                protocol=config["direct_protocol"])


def run_direct_packets(llm, row, audit, direct, output):
    """Operational equivalent of run_direct, using its frozen exact messages."""
    answers, requests = {}, []
    for label in row["probing_queries"]:
        packet = direct["packets"][(row["uid"], label)]
        audit.set_context(arm="direct", uid=row["uid"], phase="answer", query_label=label,
                          direct_protocol=direct["protocol"])
        answers[label.replace("_query", "_response")] = llm.call_text(deepcopy(packet["messages"]))
        requests.append(dict(query=label, input_sha256=packet["messages_sha256"],
                             retained_sessions=packet["retained_sessions"], removed_sessions=packet["removed_sessions"],
                             estimated_input_tokens=packet["original_estimated_tokens"],
                             actual_qwen_input_tokens=packet["actual_qwen_input_tokens"],
                             gold_preserving_truncation=True, direct_protocol=direct["protocol"]))
        save(output / (row["uid"] + ".direct.partial.json"), dict(answers=answers, request_metadata=requests,
             prepared_packets_sha256=direct["file_sha256"], direct_protocol=direct["protocol"]))
    save(output / (row["uid"] + ".direct.json"), dict(answers=answers, request_metadata=requests,
         prepared_packets_sha256=direct["file_sha256"], direct_protocol=direct["protocol"]))
    return answers


def compatibility_probes(client, config, audit, retry_builder):
    schema = dict(type="object", properties={"ok": {"type": "boolean"}},
                  required=["ok"], additionalProperties=False)
    initial = [dict(role="system", content="Return one valid JSON object only."),
               dict(role="user", content='Return {"ok":true}.')]
    probes = [
        ("json_object", initial, dict(temperature=0.3, response_format={"type": "json_object"})),
        ("strict_json_schema", initial, dict(temperature=0, response_format={"type": "json_schema",
            "json_schema": {"name": "local_compatibility", "schema": schema, "strict": True}})),
        ("native_multi_message_retry", retry_builder(initial, "{'ok': true}"), dict(temperature=0)),
    ]
    verified = []
    for name, messages, options in probes:
        audit.set_context(phase="compatibility_probe", model=config["actor"], probe=name)
        response = client.chat.completions.create(model=config["actor"], messages=messages, max_tokens=128, **options)
        payload = json.loads(response.choices[0].message.content)
        if payload != {"ok": True}:
            raise ValueError("Local compatibility probe did not return the required JSON")
        verified.append(dict(probe=name, input_sha256=digest(messages), passed=True))
    return verified


def execute_cases(chosen, rows, *, config, engine, actor, judge, audit, direct, grading, output,
                  result, result_path, helpers=None):
    """Both frozen cases run afresh; old BAZE outputs are never loaded here."""
    helpers = helpers or SimpleNamespace(cup=run_cup, direct=run_direct_packets, judge=run_judge)
    selection = [dict(uid=r["uid"], type=r["type"], input_sha256=digest(model_record(r))) for r in chosen]
    if selection != config["selection"] or len(chosen) != 2 or result["completed"] or result.get("direct_answers"):
        raise ValueError("Require exactly the two frozen cases and an empty fresh result")
    # Every fresh, scored direct answer is obtained before costly CUP ingestion.
    # This exercises the selected full-context packets on the actual server;
    # the subsequent paired comparison reuses these exact answers, never an
    # extra probe prompt or an answer from another job/history.
    result["execution_order"] = "all six fresh direct answers, then each CUP case and paired self-judge"
    result["direct_answers"] = {}
    for row in chosen:
        result["active_stage"] = dict(arm="direct", uid=row["uid"])
        save(result_path, result)
        result["direct_answers"][row["uid"]] = helpers.direct(actor, row, audit, direct, output)
        result["accounting"] = audit.summary()
        save(result_path, result)
    for row in chosen:
        result["active_stage"] = dict(arm="cupmem", uid=row["uid"])
        save(result_path, result)
        answers = dict(cupmem=helpers.cup(engine, row, rows.index(row), audit, output))
        answers["direct"] = deepcopy(result["direct_answers"][row["uid"]])
        judged = {arm: helpers.judge(row, answer, arm, judge, config["judge"], audit, grading)
                  for arm, answer in answers.items()}
        save(output / (row["uid"] + ".answers.json"), answers)
        save(output / (row["uid"] + ".judgments.json"), judged)
        result["completed"].append(dict(uid=row["uid"], type=row["type"], answers=answers, judgments=judged,
                                        direct_protocol=config["direct_protocol"],
                                        judge_is_independent=False, inherited_from_other_job=False))
        result["accounting"] = audit.summary()
        save(result_path, result)
    result["active_stage"] = dict(phase="all_cases_complete")


def run(config_path):
    # Fail before source traversal, model imports or download on a login node.
    if not os.environ.get("SLURM_JOB_ID") or not os.environ.get("SLURMD_NODENAME"):
        raise RuntimeError("Slurm compute-node execution required")
    config_path = Path(config_path)
    config_bytes = config_path.read_bytes()
    config = json.loads(config_bytes)
    validate_config(config)
    if os.environ.get("CONDA_PREFIX") != config["conda_prefix"]:
        raise RuntimeError("Explicit conda activation required")
    import torch
    validate_runtime(config, os.environ, sys.executable, torch.cuda.device_count())
    job = os.environ["SLURM_JOB_ID"]
    project = Path(config["project"])
    out = project / "results" / ("cupmem-local-" + job)
    out.mkdir()  # No overwrite/resume.
    result_path = project / "results" / ("sm-" + job + ".json")
    if result_path.exists():
        raise FileExistsError("Result already exists; do not overwrite an earlier attempt")
    result = dict(status="running", job_id=job, output_path=str(out), source_version=config["source_version"],
                  config_sha256=hashlib.sha256(config_bytes).hexdigest(), actor=config["actor"], judge=config["judge"],
                  model_repo=config["model_repo"], model_revision=config["model_revision"], serving=config["serving"],
                  max_model_len=config["max_model_len"], max_output_tokens=config["max_output_tokens"],
                  request_timeout_seconds=config.get("request_timeout_seconds", 120),
                  retry_policy="Native SDK and upstream retries preserved; every HTTP attempt audited",
                  server_configuration_verification="Launcher must attest revision/flags; not introspected by this wrapper",
                  reproduction_label="local Qwen3-8B alternate-model STALE two-case pilot; provisional non-independent self-judge",
                  judge_is_independent=False, original_model_score_reproduction=False,
                  direct_protocol=config["direct_protocol"],
                  protocol_change=("none beyond declared local model/serving differences" if config["direct_protocol"] == "original_tiktoken"
                                   else "explicit variant: original gold-preserving removal algorithm with actual Qwen tokenizer budget"),
                  upstream_revision=REVISION, dataset_revision=DATA_REVISION, dataset_sha256=DATA_SHA256,
                  conda_prefix=os.environ["CONDA_PREFIX"], python=sys.executable, node=os.environ["SLURMD_NODENAME"],
                  visible_gpu_count=torch.cuda.device_count(), local_limits=config["local_limits"],
                  budget_kind="local inference guardrails, not BAZE financial authorization",
                  manual_source_audit="required separately; self-judge does not establish semantic validity", completed=[])
    started, audit, guard = time.time(), None, None
    try:
        upstream = Path(config["upstream"])
        result["verified_upstream_files"] = verify_source(upstream)
        sys.path.insert(0, str(upstream))
        from cup_mem import CupMemEngine, LLMClient, PipelineThresholds, TraceConfig
        from cup_mem.llm_layer.client import build_json_retry_messages
        from huggingface_hub import snapshot_download
        from transformers import AutoTokenizer
        result["versions"] = {p: importlib.metadata.version(p) for p in
                              ("vllm", "openai", "httpx", "torch", "transformers", "tiktoken")}
        if result["versions"]["vllm"] != config["serving"]["vllm_version"]:
            raise RuntimeError("vLLM installation differs from configured serving version")
        data_root = Path(config["data_root"]) / DATA_REVISION
        data_file = data_root / "T1_T2_400_FULL.json"
        if not data_file.is_file():
            snapshot_download(repo_id="STALEproj/STALE", repo_type="dataset", revision=DATA_REVISION,
                              local_dir=str(data_root), allow_patterns=[data_file.name], token=False, max_workers=2)
        rows = load_data(data_file)
        chosen = select_pilot(rows)
        result["type_counts"] = dict(Counter(r["type"] for r in rows))
        result["selection"] = [dict(uid=r["uid"], type=r["type"], input_sha256=digest(model_record(r))) for r in chosen]
        if result["selection"] != config["selection"]:
            raise ValueError("Frozen two-case selection changed")
        result["thresholds"] = asdict(PipelineThresholds())
        tokenizer = AutoTokenizer.from_pretrained(config["model_path"], local_files_only=True)
        direct = load_direct_packets(config, tokenizer, chosen)
        result["frozen_direct_preflight"] = direct["checks"]
        result["context_packets_path"] = config["context_packets_path"]
        result["context_packets_sha256"] = config["context_packets_sha256"]
        audit = Audit(out / "http.jsonl", limits=config["local_limits"], secrets=())
        guard = ContextGuard(tokenizer, config, audit, out / "context-checks.jsonl")
        factory = local_sdk_factory(audit, config, guard)
        actor = LLMClient(model=config["actor"], api_key=LOCAL_API_KEY, base_url=config["base_url"],
                          cache_dir=None, openai_cls=factory)
        judge = factory(api_key=LOCAL_API_KEY, base_url=config["base_url"])
        save(result_path, result)
        result["compatibility_probes"] = compatibility_probes(judge, config, audit, build_json_retry_messages)
        save(result_path, result)
        engine = CupMemEngine(llm=actor, embedding_model_path=config["embedding"], embedding_device="cpu",
                              thresholds=PipelineThresholds(), trace_config=TraceConfig(enable_debug_trace=True))
        grading = judge_functions(upstream)
        execute_cases(chosen, rows, config=config, engine=engine, actor=actor, judge=judge, audit=audit,
                      direct=direct, grading=grading, output=out, result=result, result_path=result_path)
        result["status"] = "complete"
    except BaseException as exc:
        if isinstance(exc, ContextIncompatible):
            result["status"] = "context_incompatible"
            result["context_failure"] = exc.record
            result["semantic_score_for_interrupted_case"] = "not scored; technical context incompatibility"
        elif isinstance(exc, ServingIncompatible):
            result["status"] = "serving_incompatible"
            result["serving_failure"] = exc.record
            result["semantic_score_for_interrupted_case"] = "not scored; technical server/tokenizer compatibility failure"
        elif isinstance(exc, BudgetStop):
            result["status"] = "censored" if audit and audit.censored else "budget_stopped"
        else:
            result["status"] = "failed"
        result["error_type"] = type(exc).__name__
        raise
    finally:
        result["elapsed_seconds"] = time.time() - started
        if audit:
            result["accounting"] = audit.summary()
        save(result_path, result)
        if guard:
            guard.file.close()
        if audit:
            audit.file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path)
    args = parser.parse_args()
    try:
        run(args.config)
    except BaseException as exc:
        print("local_cupmem_stopped", type(exc).__name__, flush=True)
        sys.exit(1)
