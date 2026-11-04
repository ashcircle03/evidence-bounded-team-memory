"""Replay job 119252, locate each witness in its reader prompt, and test the citation path."""

import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path

from assess import grade_reader
from team_memory.qa import read_answer

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parents[1] / "results" / "cpython"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def trials(packet_path, recording, score):
    packed = packet_path.read_bytes()
    if sha(packed) != recording["packets_sha256"]:
        raise ValueError("packet hash differs from the recorded GPU input")
    calls = iter(c for c in recording["calls"] if c["kind"] == "qa")
    recorded = {
        (r["event"], r["kind"], r["phase"]): r
        for r in recording["rows"]
        if r["arm"] == "qa"
    }
    annotations = {(r["event"], r["kind"], r["phase"]): r for r in score["qa"]}
    seen = set()
    for packet in json.loads(gzip.decompress(packed)):
        for q in packet["qa"]:
            key = (packet["id"], q["kind"], q["phase"])
            prior = next(calls)
            request = []

            def replay(system, content):
                if sha((system + "\n" + content).encode()) != prior["sha256"]:
                    raise ValueError(f"prompt mismatch for {key}")
                request.append((system, content))
                return prior["output"]

            outcome = read_answer(copy.deepcopy(q["evidence"]), q["question"], replay)
            if outcome["reader"] != recorded[key]["reader"] or key in seen:
                raise ValueError(f"reader replay differs for {key}")
            seen.add(key)
            ((system, content),) = request
            payload = json.loads(content)
            annotated = annotations[key]
            (n,) = [
                i
                for i, c in enumerate(q["evidence"]["citations"], 1)
                if c["location"] == annotated["expected_source"]
            ]
            (msg,) = [m for m in payload["messages"] if m["n"] == n]
            gold = annotated["gold_evidence"]["text"]
            (s,) = [int(k) for k, text in msg["sentences"].items() if gold in text]
            yield {
                "event": key[0],
                "kind": key[1],
                "phase": key[2],
                "q": q,
                "system": system,
                "content": content,
                "call": prior,
                "n": n,
                "s": s,
                "gold": gold,
                "target_url": annotated["expected_source"],
                "reader": outcome["reader"],
            }
    if next(calls, None) is not None or seen != set(recorded):
        raise ValueError("incomplete replay")


def substitute(trial, raw):
    q = trial["q"]
    return read_answer(copy.deepcopy(q["evidence"]), q["question"], lambda *_: raw)[
        "reader"
    ]


def verdict(trial, reader, answer_key):
    (src,) = [
        c
        for c in trial["q"]["evidence"]["citations"]
        if c["location"] == trial["target_url"]
    ]
    return grade_reader(
        reader, answer_key, {"text": src["quote"], "location": src["location"]}
    )


def repair_checks(trial, pick, matches, answer_key):
    """Try alternate encodings of what the model actually selected, without adding gold text."""
    if not isinstance(pick, dict):
        return []
    checks = []

    def evaluate_change(change, modified):
        reader = substitute(trial, json.dumps(modified))
        checks.append(
            {
                "change": change,
                "submitted": modified,
                "returned": reader["status"],
                "grounded_correct": verdict(trial, reader, answer_key),
            }
        )

    if "side1" in pick and "side2" in pick:
        evaluate_change(
            "name the two sides as requested by the parser",
            {"kind": "conflict", "sides": [pick["side1"], pick["side2"]]},
        )
    elif "span" in pick and len(matches) == 1:
        locations = matches[0]["whitespace_normalized"]
        if len(locations) == 1:
            n, s = locations[0]
            evaluate_change(
                "single quote with its source number",
                {"kind": "single", "n": n, "field": "quote", "span": pick["span"]},
            )
            evaluate_change(
                "point to the unique source block containing that quote",
                {"kind": "single", "n": n, "s": s},
            )
    return checks


def audit(trial, answer_key):
    payload = json.loads(trial["content"])
    oracle = {
        "kind": "single",
        "n": trial["n"],
        "field": "quote",
        "span": trial["gold"],
    }
    passed = verdict(trial, substitute(trial, json.dumps(oracle)), answer_key)
    if not passed:
        raise ValueError("gold text failed the original validator or scorer")
    pick = json.loads(trial["call"]["output"])
    candidates = []
    if isinstance(pick, dict):
        if "span" in pick:
            candidates.append(pick)
        candidates.extend(
            v for v in pick.values() if isinstance(v, dict) and "span" in v
        )
    matches = []
    for candidate in candidates:
        span = candidate["span"]
        exact = []
        whitespace = []
        for m in payload["messages"]:
            for s, text in m["sentences"].items():
                if span in text:
                    exact.append([m["n"], int(s)])
                if " ".join(span.split()) in " ".join(text.split()):
                    whitespace.append([m["n"], int(s)])
        matches.append(
            {
                "claimed_n": candidate.get("n"),
                "span": span,
                "exact": exact,
                "whitespace_normalized": whitespace,
            }
        )
    return {
        "event": trial["event"],
        "kind": trial["kind"],
        "phase": trial["phase"],
        "gold_n": trial["n"],
        "gold_s": trial["s"],
        "gold_span": trial["gold"],
        "prompt_sha256": trial["call"]["sha256"],
        "input_tokens": trial["call"]["tokens"],
        "output_tokens": trial["call"]["output_tokens"],
        "raw": trial["call"]["output"],
        "returned": trial["reader"].get("status"),
        "candidate_pairs": payload["candidate_pairs"],
        "reported_span_matches": matches,
        "repairs": repair_checks(trial, pick, matches, answer_key),
        "gold_passes_original_path": passed,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dump-inputs",
        type=Path,
        help="write the exact system and user strings to a local JSONL",
    )
    args = parser.parse_args()
    recording = json.loads((RESULTS / "outputs.json").read_text())
    score = json.loads((RESULTS / "score.json").read_text())
    keys = json.loads((HERE / "key.json").read_text())
    report, inputs = [], []
    for t in trials(HERE / "packets.json.gz", recording, score):
        report.append(audit(t, keys[t["event"]]["qa"][t["kind"]]))
        inputs.append(
            {k: t[k] for k in ("event", "kind", "phase", "system", "content")}
        )
    if args.dump_inputs:
        args.dump_inputs.parent.mkdir(exist_ok=True, parents=True)
        args.dump_inputs.write_text(
            "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in inputs)
        )
    print(json.dumps(report, ensure_ascii=False, indent=2))
