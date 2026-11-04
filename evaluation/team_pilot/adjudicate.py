"""Blind the two arms for semantic review, then report reviewed and automatic scores separately."""

import argparse
import hashlib
import json
from pathlib import Path

from score import summarize


def sha(data):
    return hashlib.sha256(data).hexdigest()


def panels(packets_path, rows):
    here = Path(__file__).resolve().parent
    raw = packets_path.read_bytes()
    freeze = json.loads((here / "freeze.json").read_text())
    if sha(raw) != freeze["packet_sha256"]:
        raise ValueError("prompt packet does not match freeze")
    prompts = {p["id"]: json.loads(p["content"]) for p in json.loads(raw)}
    if len(rows) != len(prompts) or {r["id"] for r in rows} != set(prompts):
        raise ValueError("a complete replay is required")
    reviews = json.loads((here / "cases.json").read_text())["review"]
    cards, lookup = {}, {}
    for row in rows:
        prompt = prompts[row["id"]]
        if row["phase"] == "review":
            example = reviews[int(row["case"].split("-")[1]) - 1]
            task = {
                "project_goal": prompt["goal"],
                "incoming_record": example["incoming"],
                "prior_record_for_grading": example["previous"],
            }
        else:
            task = {"question": prompt["question"]}
        card = {
            "case": row["case"],
            "phase": row["phase"],
            **task,
            "reference": row["key"],
            "returned": row["result"],
        }
        key = sha(json.dumps(card, ensure_ascii=False, sort_keys=True).encode())
        cards[key] = card
        lookup[row["id"]] = key
    return dict(sorted(cards.items())), lookup


def review(packets, graded, ratings=None):
    cards, lookup = panels(packets, graded["rows"])
    if ratings is None:
        return {
            key: {**card, "correct": None, "basis": ""} for key, card in cards.items()
        }
    if set(cards) != set(ratings):
        raise ValueError("ratings are missing or do not match these model outputs")
    for key, card in cards.items():
        rating = ratings[key]
        if (
            {k: v for k, v in rating.items() if k not in ("basis", "correct")} != card
            or type(rating.get("correct")) is not bool
            or not isinstance(rating.get("basis"), str)
            or not rating["basis"].strip()
        ):
            raise ValueError(
                f"missing decision, missing reason, or modified card: {key}"
            )
    rows = []
    for old in graded["rows"]:
        key = lookup[old["id"]]
        rows.append(
            {
                **old,
                "automatic_correct": old["correct"],
                "review_card": key,
                "correct": ratings[key]["correct"],
                "basis": ratings[key]["basis"],
            }
        )
    return {
        "automatic_summary": graded["summary"],
        "reviewed_summary": summarize(rows),
        "rows": rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packets", type=Path)
    parser.add_argument("graded", type=Path)
    parser.add_argument("--ratings", type=Path)
    args = parser.parse_args()
    graded = json.loads(args.graded.read_text())
    ratings = json.loads(args.ratings.read_text()) if args.ratings else None
    print(
        json.dumps(review(args.packets, graded, ratings), ensure_ascii=False, indent=2)
    )
