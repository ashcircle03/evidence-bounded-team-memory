"""Prepare label-free Qwen requests and replay logged generations through the same APIs."""
import argparse
import json
from pathlib import Path

from evaluation.team_pilot.pilot import bundle, call_hash, write
from team_memory.evidence import ask, assess
from team_memory.qa import answer, read_answer
from team_memory.store import digest, timestamp
from team_memory.sync import DEFAULT_GOAL


class History:
    """Read-only storage over the exact raw records visible at decision time."""
    def __init__(self, sources):
        self.sources = {k: env for k, (env, _) in sources.items()}

    def load(self, kind):
        return self.sources if kind == "sources" else {}


def build(data, recording=None):
    packets, outcomes = [], []
    logged = {row["id"]: row for row in recording["calls"]} if recording else {}
    for case in data["cases"]:
        docs = data["documents"]
        history = [docs[k] for k in case["history"]]
        if any(timestamp(e["observed_at"]) > timestamp(case["as_of"]) for e in history):
            raise ValueError(f"future source in {case['id']}")
        sources = bundle(history)
        for arm in case["arms"]:
            prefix = f"{case['id']}/{arm}"
            calls = []
            split_read = case["task"] != "review" and arm == "premise"

            def generate(system, content):
                key = f"{prefix}/{len(calls) + 1}"
                sha = call_hash(system, content)
                calls.append(key)
                packets.append(dict(id=key, sha256=sha, system=system, content=content, group=prefix, max_output_tokens=64 if split_read else 192))
                if recording is None:
                    return "NONE"
                if logged[key]["sha256"] != sha:
                    raise ValueError(f"changed prompt {key}")
                return logged[key]["raw"]

            if case["task"] == "review":
                new = docs[case["incoming"]]
                if timestamp(new["observed_at"]) != timestamp(case["as_of"]) or any(timestamp(e["observed_at"]) >= timestamp(new["observed_at"]) for e in history):
                    raise ValueError("incoming evidence is out of order")
                result = assess(sources, digest(new), new, case.get("goal", DEFAULT_GOAL), generate, arm)
            elif arm == "legacy":
                q = case["question"]
                result = read_answer(answer(History(sources), q), q, generate)
                result = result.get("reader", {"status": result["status"]})
            else:
                result = ask(sources, case["question"], generate, arm)
            if len(calls) > (3 if split_read else 1):
                raise ValueError(f"{prefix} exceeds the comparison budget")
            outcomes.append(dict(id=prefix, calls=calls, result=result))
    if len({p["id"] for p in packets}) != len(packets):
        raise ValueError("duplicate prompts")
    if recording is not None and (set(logged) != {p["id"] for p in packets} or len(logged) != len(recording["calls"])):
        raise ValueError("recording does not cover exactly the prepared calls")
    return packets, outcomes


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("casebook", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--recording", type=Path)
    a = ap.parse_args()
    log = json.loads(a.recording.read_text()) if a.recording else None
    prompts, rows = build(json.loads(a.casebook.read_text()), log)
    write(a.output, rows if log else prompts)
