"""Pinned source/data checks and side-effect-free loading of official evaluator functions."""
import ast
import asyncio
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
import random
import time

REVISION = "ea7d391103a151927cd29d2f01d87597a782bdcb"
DATA_REVISION = "617c51dc200b5ab09970834144c7e51c77959af0"
DATA_SHA256 = "5f3ec375179e20e2e94469e018189188f34e2e7e5f21cbecbd99fcfa648c1876"


def verify_source(root):
    manifest = json.loads((root / "UPSTREAM_MANIFEST.json").read_text())
    assert manifest["revision"] == REVISION
    for entry in manifest["files"]:
        raw = (root / entry["path"]).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        assert actual == entry["git_blob_sha1"], entry["path"]
    return len(manifest["files"])


def load_data(path):
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == DATA_SHA256
    obj = json.loads(raw)
    rows = obj if isinstance(obj, list) else obj["data"]
    assert len(rows) == 400 and len({r["uid"] for r in rows}) == 400
    assert all(len(r["haystack_session"]) == len(r["timestamps"]) == 50 for r in rows)
    assert all(set(r["probing_queries"]) == {"dim1_query", "dim2_query", "dim3_query"} for r in rows)
    return rows


def select_pilot(rows):
    """One deterministic UID-hash selection from each type, never by answer quality."""
    types = sorted({r["type"] for r in rows})
    assert len(types) == 2
    return [min((r for r in rows if r["type"] == t),
                key=lambda r: hashlib.sha256(("cupmem-pilot-v1:" + r["uid"]).encode()).hexdigest()) for t in types]


def model_record(row):
    # A new object, not a shallow reference to an evaluator record.
    return copy.deepcopy({k: row[k] for k in ("uid", "haystack_session", "timestamps", "probing_queries")})


def definitions(path, names, namespace):
    tree = ast.parse(path.read_text())
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in names]
    assert {n.name for n in nodes} == set(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), namespace)
    return namespace


def direct_functions(root, model):
    import tiktoken
    names = ["format_haystack", "get_encoder", "num_tokens_from_messages", "build_prompts",
             "estimate_request_tokens", "trim_middle_noise_to_token_limit"]
    return definitions(root / "STALE/Evaluation/run_target_model.py", names,
                       dict(copy=copy, random=random, tiktoken=tiktoken, EVAL_MODEL=model, INPUT_TOKEN_LIMIT=125440))


def judge_functions(root):
    prompt_file = root / "STALE/Evaluation/judge_prompts.py"
    # This pinned file contains only the original constant prompt assignment.
    tree = ast.parse(prompt_file.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "SYSTEM_PROMPT_ALL_IN_ONE_JUDGE" for t in n.targets))
    prompt = ast.literal_eval(node.value)
    return definitions(root / "STALE/Evaluation/full_eval_performance.py",
                       ["normalize_usage", "async_evaluate_all_dimensions"],
                       dict(json=json, re=re, time=time, SYSTEM_PROMPT_ALL_IN_ONE_JUDGE=prompt))
