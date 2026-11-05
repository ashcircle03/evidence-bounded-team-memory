"""Run a bounded STALE pilot on a Slurm compute node, with native CUPMem code.

Invocation: python -m evaluation.cupmem.official CONFIG.json
Credentials arrive separately via credential.deliver inside the same allocation.
"""
from __future__ import annotations

import asyncio
from collections import Counter
from dataclasses import asdict
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time
from types import SimpleNamespace

from .audit import Audit, BudgetStop, digest, sdk_factory
from .credential import receive
from .upstream import DATA_REVISION, DATA_SHA256, REVISION, direct_functions, judge_functions, load_data, model_record, select_pilot, verify_source


def save(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def state_hash(result):
    return digest({k: result[k] for k in ("final_profile_snapshot", "chunk_bank", "delta_store")})


def run_cup(engine, row, index, audit, output):
    frozen = None
    checks = []

    def progress(event):
        nonlocal frozen
        phase = event["phase"]
        result = event["result"]
        if phase in ("query_start", "query_complete"):
            current = state_hash(result)
            frozen = frozen or current
            assert current == frozen, "Query changed persistent memory"
            checks.append(dict(phase=phase, query=event["query_label"], state_sha256=current))
        if phase == "sample_start":
            context = dict(phase="ingest", session_index=0)
        elif phase == "session_complete":
            context = dict(phase="ingest", session_index=event["session_index"] + 1)
        else:
            context = dict(phase=phase, query_label=event.get("query_label"))
        audit.set_context(arm="cupmem", uid=row["uid"], **context)
        save(output / (row["uid"] + ".cupmem.partial.json"), result)
        save(output / "live.json", dict(uid=row["uid"], arm="cupmem", phase=phase,
              completed_sessions=result["completed_session_count"],
              completed_queries=result["completed_query_count"], accounting=audit.summary()))
        print("cupmem_progress", row["uid"], phase, result["completed_session_count"], flush=True)

    visible = model_record(row)
    result = engine.run_sample(visible, sample_index=index, session_mode="full", progress_callback=progress)
    assert result["completed_session_count"] == 50 and result["completed_query_count"] == 3
    assert result["sample_meta"]["selected_session_indices"] == list(range(50))
    assert all(result["sample_meta"][k] is None for k in ("M_old", "M_new", "explanation", "relevant_session_index"))
    result["memory_immutability_checks"] = checks
    result["input_sha256"] = digest(visible)
    result["logical_call_records"] = engine.llm.get_call_records()
    save(output / (row["uid"] + ".cupmem.json"), result)
    return {k.replace("_query", "_response"): v["answer"]["answer"] for k, v in result["query_logs"].items()}


def run_direct(llm, row, audit, funcs, output):
    answers, requests = {}, []
    for label, question in row["probing_queries"].items():
        sessions, dates, tokens, removed = funcs["trim_middle_noise_to_token_limit"](row, label, question)
        history = funcs["format_haystack"](sessions, dates)
        system, user = funcs["build_prompts"](history, question, label)
        messages = [dict(role="system", content=system), dict(role="user", content=user)]
        audit.set_context(arm="direct", uid=row["uid"], phase="answer", query_label=label)
        raw = llm.call_text(messages)
        answers[label.replace("_query", "_response")] = raw
        requests.append(dict(query=label, input_sha256=digest(messages), retained_sessions=len(sessions),
                             removed_sessions=removed, estimated_input_tokens=tokens,
                             gold_preserving_truncation=True))
    save(output / (row["uid"] + ".direct.json"), dict(answers=answers, request_metadata=requests))
    return answers


def async_facade(client):
    async def create(**kwargs):
        return client.chat.completions.create(**kwargs)
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))


def run_judge(row, answers, arm, client, model, audit, funcs):
    audit.set_context(arm=arm, uid=row["uid"], phase="official_judge")
    result = asyncio.run(funcs["async_evaluate_all_dimensions"](
        asyncio.Semaphore(1), row["uid"], row["type"], row["M_old"], row["M_new"], row["explanation"],
        row["probing_queries"]["dim1_query"], answers["dim1_response"],
        row["probing_queries"]["dim2_query"], answers["dim2_response"],
        row["probing_queries"]["dim3_query"], answers["dim3_response"], async_facade(client), model))
    if "error" in result[3]:
        raise RuntimeError("Official judge failed; see redacted HTTP audit")
    for label in ("dim1_eval", "dim2_eval", "dim3_eval"):
        assert type(result[2][label]["pass"]) is bool, "Malformed judge output"
    return dict(uid=result[0], type=result[1], ratings=result[2], accounting=result[3])


def run(config_path):
    job = os.environ.get("SLURM_JOB_ID")
    assert job, "Run only inside a Slurm allocation"
    config_bytes = config_path.read_bytes()
    config = json.loads(config_bytes)
    assert os.environ.get("CONDA_PREFIX") == config["conda_prefix"], "Activate the project conda environment"
    assert Path(sys.executable).resolve().parent == Path(config["conda_prefix"]) / "bin", "Python is outside conda"
    assert config["execution_authorized"] is True
    assert config["scope"] == "pilot-two-full-sessions"
    assert config["policy"]["base_url"] == "https://factchat-cloud.mindlogic.ai/v1/gateway"
    project = Path(config["project"])
    out = project / "results" / ("cupmem-" + job)
    out.mkdir()  # No output overwrite or implicit resume.
    result_path = project / "results" / ("sm-" + job + ".json")
    started = time.time()
    result = dict(status="running", job_id=job, output_path=str(out), source_version=config["source_version"],
                  config_sha256=hashlib.sha256(config_bytes).hexdigest(), actor=config["actor"], judge=config["judge"],
                  reproduction_label="alternate-model STALE protocol pilot", upstream_revision=REVISION,
                  dataset_revision=DATA_REVISION, dataset_sha256=DATA_SHA256,
                  conda_prefix=os.environ["CONDA_PREFIX"], python=sys.executable,
                  node=os.environ.get("SLURMD_NODENAME"),
                  deviations=config["deviations"], completed=[])
    audit = None
    try:
        upstream = Path(config["upstream"])
        result["verified_upstream_files"] = verify_source(upstream)
        sys.path.insert(0, str(upstream))
        from cup_mem import CupMemEngine, LLMClient, PipelineThresholds, TraceConfig
        from huggingface_hub import snapshot_download
        data_root = Path(config["data_root"]) / DATA_REVISION
        snapshot_download(repo_id="STALEproj/STALE", repo_type="dataset", revision=DATA_REVISION,
                          local_dir=str(data_root), allow_patterns=["T1_T2_400_FULL.json"], max_workers=2)
        rows = load_data(data_root / "T1_T2_400_FULL.json")
        chosen = select_pilot(rows)
        result["type_counts"] = dict(Counter(r["type"] for r in rows))
        result["selection"] = [dict(uid=r["uid"], type=r["type"], input_sha256=digest(model_record(r))) for r in chosen]
        assert result["selection"] == config["selection"], "Pilot selection differs from pre-inference freeze"
        result["thresholds"] = asdict(PipelineThresholds())
        result["versions"] = {p: importlib.metadata.version(p) for p in ("openai", "httpx", "torch", "transformers", "tiktoken")}
        save(result_path, result)
        # First write data selection and runtime provenance; credentials are supplied last.
        key = receive(job)
        audit = Audit(out / "http.jsonl", limits=config["limits"], secrets=[key])
        factory = sdk_factory(audit, policy=config["policy"])
        def client(model):
            return LLMClient(model=model, api_key=key, base_url=config["policy"]["base_url"],
                             cache_dir=None, openai_cls=factory)
        actor = client(config["actor"])
        judge = factory(api_key=key, base_url=config["policy"]["base_url"])
        # Test precisely the non-default settings used by the pinned original pipeline.
        for model, options in ((config["actor"], {"temperature": 0.3}),
                               (config["judge"], {"temperature": 0, "response_format": {"type": "json_object"}})):
            audit.set_context(phase="compatibility_probe", model=model)
            response = judge.chat.completions.create(model=model,
                         messages=[{"role": "user", "content": 'Return the JSON object {"ok":true}.'}], **options)
            assert json.loads(response.choices[0].message.content)["ok"] is True
        engine = CupMemEngine(llm=actor, embedding_model_path=config["embedding"], embedding_device="cpu",
                              thresholds=PipelineThresholds(), trace_config=TraceConfig(enable_debug_trace=True))
        direct = direct_functions(upstream, config["actor"])
        grading = judge_functions(upstream)
        for row in chosen:
            answers = {}
            answers["cupmem"] = run_cup(engine, row, rows.index(row), audit, out)
            answers["direct"] = run_direct(actor, row, audit, direct, out)
            judged = {arm: run_judge(row, answer, arm, judge, config["judge"], audit, grading)
                      for arm, answer in answers.items()}
            save(out / (row["uid"] + ".answers.json"), answers)
            save(out / (row["uid"] + ".judgments.json"), judged)
            result["completed"].append(dict(uid=row["uid"], type=row["type"], answers=answers, judgments=judged))
            result["accounting"] = audit.summary()
            save(result_path, result)
        result["status"] = "complete"
    except BaseException as exc:
        result["status"] = "budget_stopped" if isinstance(exc, BudgetStop) else "failed"
        # Detailed response payloads are already in the credential-redacting audit.
        result["error_type"] = type(exc).__name__
        print("cupmem_stopped", type(exc).__name__, flush=True)
        raise
    finally:
        result["elapsed_seconds"] = time.time() - started
        if audit:
            result["accounting"] = audit.summary()
        save(result_path, result)


if __name__ == "__main__":
    try:
        run(Path(sys.argv[1]))
    except BaseException:
        # Avoid printing SDK exception bodies/headers into Slurm logs.
        sys.exit(1)
