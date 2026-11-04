"""Conservative automatic grading; record any semantic adjudication separately by case."""

import argparse
from collections import defaultdict
import json
from pathlib import Path


def normalized(s):
    return " ".join(s.casefold().replace("`", "").split()).strip(" .'\":,")


def grade(r):
    key, result = r["key"], r["result"]
    if r["phase"] == "review":
        if key["actions"] == ["keep"]:
            return result["action"] == "keep"
        if result["action"] not in key["actions"]:
            return False
        old, new = result["previous"], result["incoming"]
        return (
            old["location"] == key["location"]
            and new["location"] == key["new_location"]
            and key["old_cue"].casefold() in old["quote"].casefold()
            and key["new_cue"].casefold() in new["quote"].casefold()
        )
    answers = result.get("answers", [])
    if len(answers) != len(key):
        return False
    for k in key:
        hits = [a for a in answers if a["location"] == k["location"]]
        if len(hits) != 1:
            return False
        a = hits[0]
        if normalized(a["answer"]) not in {normalized(alias) for alias in k["answers"]}:
            return False
        # The production resolver has already authenticated each quote and answer
        # against its source; interpretation of a title or incidental mention needs review.
    return True


def summarize(rows):
    grouped = defaultdict(dict)
    for r in rows:
        phase = r["phase"]
        if phase == "review":
            phase = "negative" if r["key"]["actions"] == ["keep"] else "positive"
        grouped[phase].setdefault(r["case"], {})[r["arm"]] = r["correct"]
    report = {}
    for phase, cases in grouped.items():
        report[phase] = dict(
            total=len(cases),
            simple=sum(c["simple"] for c in cases.values()),
            candidate=sum(c["candidate"] for c in cases.values()),
            gains=[k for k, c in cases.items() if c["candidate"] and not c["simple"]],
            losses=[k for k, c in cases.items() if c["simple"] and not c["candidate"]],
        )
    report["paired_distraction_losses"] = {
        a: [
            k
            for k, c in grouped["clean"].items()
            if c[a] and not grouped["unrelated"][k][a]
        ]
        for a in ("simple", "candidate")
    }
    report["false_positives"] = {
        a: [
            r["case"]
            for r in rows
            if r["phase"] == "review"
            and r["arm"] == a
            and r["key"]["actions"] == ["keep"]
            and r["result"]["action"] in ("retest", "reassess")
        ]
        for a in ("simple", "candidate")
    }
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("outcomes", type=Path)
    ap.add_argument("output", type=Path)
    a = ap.parse_args()
    rows = json.loads(a.outcomes.read_text())
    for r in rows:
        r["correct"] = grade(r)
    a.output.write_text(
        json.dumps(
            dict(summary=summarize(rows), rows=rows), ensure_ascii=False, indent=2
        )
        + "\n"
    )
