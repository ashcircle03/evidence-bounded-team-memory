"""Run prepared prompts only. No keys, ranking code or annotations enter the GPU job."""

import argparse
import hashlib
import json
from pathlib import Path
import time


def infer(packets_path, model_path, output, job_id):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required")
    raw = packets_path.read_bytes()
    packets = json.loads(raw)
    if len(packets) != 104 or len({r["id"] for r in packets}) != 104:
        raise ValueError("unexpected input count")
    tokenizer = AutoTokenizer.from_pretrained(
        model_path, local_files_only=True, padding_side="left"
    )
    model = (
        AutoModelForCausalLM.from_pretrained(
            model_path, local_files_only=True, torch_dtype=torch.bfloat16
        )
        .to("cuda")
        .eval()
    )
    items = []
    for p in packets:
        sha = hashlib.sha256((p["system"] + "\n" + p["content"]).encode()).hexdigest()
        if p["sha256"] != sha:
            raise ValueError("changed prompt")
        messages = [
            {"role": "system", "content": p["system"]},
            {"role": "user", "content": p["content"]},
        ]
        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        ids = tokenizer(prompt).input_ids
        if len(ids) > 8192:
            raise ValueError("input exceeds frozen limit")
        items.append((p, ids))
    items.sort(key=lambda x: (len(x[1]), x[0]["id"]))
    calls = []
    before = time.monotonic()
    with output.with_suffix(".partial.jsonl").open("x", encoding="utf8") as partial:
        for i in range(0, len(items), 4):
            block = items[i : i + 4]
            batch = tokenizer.pad(
                {"input_ids": [ids for _, ids in block]},
                padding=True,
                return_tensors="pt",
            ).to("cuda")
            with torch.inference_mode():
                generation = model.generate(
                    **batch,
                    do_sample=False,
                    max_new_tokens=64,
                    pad_token_id=tokenizer.eos_token_id,
                )
            for (p, ids), tail in zip(
                block, generation[:, batch.input_ids.size(1) :].tolist()
            ):
                if tokenizer.eos_token_id in tail:
                    tail = tail[: tail.index(tokenizer.eos_token_id) + 1]
                row = dict(
                    id=p["id"],
                    sha256=p["sha256"],
                    raw=tokenizer.decode(tail, skip_special_tokens=True),
                    input_tokens=len(ids),
                    output_tokens=len(tail),
                )
                calls.append(row)
                partial.write(json.dumps(row, ensure_ascii=False) + "\n")
            partial.flush()
            print(len(calls), "/", len(items), flush=True)
    report = dict(
        status="complete",
        job_id=job_id,
        model="Qwen2.5-3B-Instruct",
        revision="aa8e72537993ba99e69dfaafa59ed015b17504d1",
        dtype=str(model.dtype),
        device=torch.cuda.get_device_name(0),
        generation_seconds=round(time.monotonic() - before, 2),
        input_sha256=hashlib.sha256(raw).hexdigest(),
        calls=calls,
    )
    tmp = output.with_suffix(".tmp")
    tmp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    tmp.replace(output)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("packets", type=Path)
    ap.add_argument("model")
    ap.add_argument("output", type=Path)
    ap.add_argument("job")
    a = ap.parse_args()
    infer(a.packets, a.model, a.output, a.job)
