"""Prepare separate raw inputs and scoring keys from QA-SRL Gold development data."""
import argparse
import csv
import json
from pathlib import Path


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def prepare(checkout, output):
    output.mkdir(parents=True, exist_ok=True)
    inputs, keys, mismatches = [], [], []
    for corpus in ("wikinews", "wikipedia"):
        sentences = read_rows(checkout / "data/sentences" / f"{corpus}.dev.full.csv")
        texts = {row["qasrl_id"]: row["tokens"] for row in sentences}
        gold = read_rows(checkout / "data/gold" / f"{corpus}.dev.gold.csv")
        for doc_id in sorted({row["qasrl_id"] for row in gold}):
            inputs.append({"id": doc_id, "text": texts[doc_id]})
        for row in gold:
            doc_id = row["qasrl_id"]
            tokens = texts[doc_id].split()
            ranges = row["answer_range"].split("~!~")
            answers = row["answer"].split("~!~")
            if len(ranges) != len(answers):
                raise ValueError(f"Unpaired ranges in {doc_id}")
            for span, answer in zip(ranges, answers):
                start, end = map(int, span.split(":"))
                if not 0 <= start < end <= len(tokens):
                    raise ValueError(f"Invalid span in {doc_id}")
                if " ".join(tokens[start:end]) != answer.strip():
                    mismatches.append({"id": doc_id, "span": span, "answer": answer})
            keys.append({field: row[field] for field in (
                "qasrl_id", "verb_idx", "verb", "question", "answer_range", "answer",
                "is_redundant", "wh", "subj", "obj", "obj2", "aux", "prep",
                "verb_prefix", "is_passive", "is_negated", "verb_slot_inflection")})
    if len({row["id"] for row in inputs}) != len(inputs):
        raise ValueError("Duplicate input ID")
    for name, rows in (("inputs", inputs), ("gold", keys), ("span_mismatches", mismatches)):
        with (output / f"{name}.jsonl").open("x", encoding="utf-8") as stream:
            for row in rows:
                print(json.dumps(row, ensure_ascii=False), file=stream)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    prepare(args.checkout, args.output)
