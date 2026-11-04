"""Post-hoc 2×2 QA diagnostic. Prepare model inputs separately from GPU inference."""

import argparse
import gzip
import hashlib
import json
import re
from pathlib import Path

from audit_qa import HERE, RESULTS, substitute, trials, verdict
from replay import pilot_gzip
from team_memory.choice import LocalChoice

PLAIN = (
    "Answer using only the numbered messages. A question is not a decision. No outside knowledge. "
    "Return null if unsupported. If two relevant reports conflict, return both answers. "
    "Otherwise return the shortest answer that answers the question. Include units and necessary "
    "bounds such as at least. Output only the answer text, without JSON, message numbers or citations."
)


def prepare():
    recording = json.loads((RESULTS / "outputs.json").read_text())
    score = json.loads((RESULTS / "score.json").read_text())
    rows = []
    for t in trials(HERE / "packets.json.gz", recording, score):
        payload = json.loads(t["content"])
        assert (
            not payload["candidate_pairs"]
            and not payload["differences_not_answering_question"]
        )
        (msg,) = [m for m in payload["messages"] if m["n"] == t["n"]]
        s = str(t["s"])
        oracle = {
            **payload,
            "messages": [{**msg, "sentences": {s: msg["sentences"][s]}}],
        }
        for scope, content in (
            ("full", t["content"]),
            ("oracle", json.dumps(oracle, ensure_ascii=False)),
        ):
            for style, system in (("structured", t["system"]), ("plain", PLAIN)):
                rows.append(
                    {
                        "event": t["event"],
                        "kind": t["kind"],
                        "phase": t["phase"],
                        "scope": scope,
                        "style": style,
                        "system": system,
                        "content": content,
                    }
                )
    return rows


def infer(input_path, model_path, output, job_id):
    model = LocalChoice(model_path)
    if model.model.device.type != "cuda":
        raise RuntimeError("CUDA required")
    items = json.loads(gzip.decompress(input_path.read_bytes()))
    result = []
    partial = output.with_suffix(".jsonl")
    with partial.open("x") as f:
        for item in items:
            messages = [
                {"role": "system", "content": item["system"]},
                {"role": "user", "content": item["content"]},
            ]
            ids = model.tokenizer.apply_chat_template(
                messages, add_generation_prompt=True, return_tensors="pt"
            ).to(model.model.device)
            if ids.size(1) > 8192:
                raise ValueError("Input exceeds the original reader budget")
            with model.torch.inference_mode():
                seq = model.model.generate(
                    input_ids=ids,
                    attention_mask=model.torch.ones_like(ids),
                    max_new_tokens=96,
                    do_sample=False,
                    pad_token_id=model.tokenizer.eos_token_id,
                )
            raw = model.tokenizer.decode(
                seq[0, ids.size(1) :], skip_special_tokens=True
            )
            row = {k: v for k, v in item.items() if k not in ("system", "content")}
            row.update(
                raw=raw,
                input_tokens=ids.size(1),
                output_tokens=seq.size(1) - ids.size(1),
                sha256=hashlib.sha256(
                    (item["system"] + "\n" + item["content"]).encode()
                ).hexdigest(),
            )
            result.append(row)
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            print(
                row["event"],
                row["kind"],
                row["phase"],
                row["scope"],
                row["style"],
                flush=True,
            )
    assert len(result) == 36
    report = {
        "status": "complete",
        "job_id": job_id,
        "model": "Qwen2.5-3B-Instruct",
        "dtype": str(model.model.dtype),
        "device": str(model.model.device),
        "rows": result,
        "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
    }
    tmp = output.with_suffix(".tmp")
    tmp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(output)


def score_controls(recording):
    """Score plain answers separately from structured answers with verified citations."""
    inputs = prepare()
    expected_archive = pilot_gzip(json.dumps(inputs, ensure_ascii=False).encode())
    if hashlib.sha256(expected_archive).hexdigest() != recording["input_sha256"]:
        raise ValueError("control inputs differ from the GPU packet")

    keys = json.loads((HERE / "key.json").read_text())
    base = json.loads((RESULTS / "outputs.json").read_text())
    audited = json.loads((RESULTS / "score.json").read_text())
    cases = {
        (t["event"], t["kind"], t["phase"]): t
        for t in trials(HERE / "packets.json.gz", base, audited)
    }
    rows = []
    for request, row in zip(inputs, recording["rows"], strict=True):
        identity = ("event", "kind", "phase", "scope", "style")
        digest = hashlib.sha256(
            (request["system"] + "\n" + request["content"]).encode()
        ).hexdigest()
        if row["sha256"] != digest or any(row[k] != request[k] for k in identity):
            raise ValueError("response does not belong to this request")
        t = cases[row["event"], row["kind"], row["phase"]]
        key = keys[t["event"]]["qa"][t["kind"]]
        out = {k: row[k] for k in (*identity, "raw")}
        if row["style"] == "plain":
            out["answer_key_match"] = bool(
                re.search(key["match"], row["raw"], re.I | re.S)
            )
        else:
            reader = substitute(t, row["raw"])
            messages = json.loads(request["content"])["messages"]
            visible = (
                block
                for message in messages
                if message["n"] == t["n"]
                for block in message["sentences"].values()
            )
            out["grounded_correct"] = verdict(t, reader, key) and any(
                reader["answer"] in block for block in visible
            )
            if row["scope"] == "full":
                out["original_reproduced"] = row["raw"] == t["call"]["output"]
            # Diagnostic only. Keep the model's chosen source and map a unique
            # whitespace-only match back to the exact text visible to the model.
            try:
                pick = json.loads(row["raw"])
            except json.JSONDecodeError:
                pick = None
            if (
                isinstance(pick, dict)
                and pick.get("kind") == "single"
                and pick.get("field") == "quote"
                and isinstance(pick.get("span"), str)
            ):
                selected = [m for m in messages if m["n"] == pick.get("n")]
                words = pick["span"].split()
                if selected and words:
                    pattern = r"\s+".join(re.escape(w) for w in words)
                    matches = [
                        m.group()
                        for block in selected[0]["sentences"].values()
                        for m in re.finditer(pattern, block)
                    ]
                    if len(matches) == 1 and matches[0] != pick["span"]:
                        repaired = {**pick, "span": matches[0]}
                        out["whitespace_only_repair_correct"] = verdict(
                            t, substitute(t, json.dumps(repaired)), key
                        )
        rows.append(out)
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    commands = ap.add_subparsers(dest="command", required=True)
    make = commands.add_parser("prepare")
    make.add_argument("output", type=Path)
    score = commands.add_parser("score")
    score.add_argument("recording", type=Path)
    gpu = commands.add_parser("infer")
    gpu.add_argument("input", type=Path)
    gpu.add_argument("model")
    gpu.add_argument("output", type=Path)
    gpu.add_argument("job_id")
    a = ap.parse_args()
    if a.command == "prepare":
        a.output.write_bytes(
            pilot_gzip(json.dumps(prepare(), ensure_ascii=False).encode())
        )
    elif a.command == "score":
        print(
            json.dumps(
                score_controls(json.loads(a.recording.read_text())),
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        infer(a.input, a.model, a.output, a.job_id)
