"""Replay two recorded Qwen replies while real Git moves evidence and owner review."""

import argparse
import json
from pathlib import Path
import tempfile

from pilot import AUTHORS, DEFAULT_GOAL, HERE, call_hash, envelope, pep_sources
from team_memory.demo import git, publish
from team_memory.evidence import active_sources, ask
from team_memory.store import Store, capture, digest
from team_memory.sync import followups, pull, relevant_followups, vote


def replay(peps):
    run = json.loads((HERE.parents[1] / "results/team_pilot/outputs.json").read_text())
    calls = {r["sha256"]: r for r in run["calls"]}
    used = []

    def generate(system, content):
        row = calls[call_hash(system, content)]
        used.append(row["sha256"])
        return row["raw"]

    cases = json.loads((HERE / "cases.json").read_text())
    question = next(q["question"] for q in cases["qa"] if q["pep"] == 615)
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        author, teammate = root / "author", root / "teammate"
        git(root, "init", "--bare", "--initial-branch=main", "origin.git")
        git(root, "clone", "origin.git", "author")
        a, b = Store(author / "records"), Store(teammate / "records")
        for i, past in enumerate(cases["review"]):
            text = past["previous"]
            capture(
                a, envelope(text, f"casebook://decisions/{digest(text)}", AUTHORS[i])
            )
        for env in pep_sources(peps).values():
            capture(Store(author / "peps"), env)
        git(author, "add", "peps")
        publish(author)
        git(root, "clone", "origin.git", "teammate")
        qa = ask(active_sources(Store(teammate / "peps")), question, generate, "simple")
        new = cases["review"][0]["incoming"]
        capture(
            b,
            envelope(
                new,
                f"casebook://observations/{digest(new)}",
                AUTHORS[7],
                "2026-11-04T12:00:00Z",
            ),
        )
        publish(teammate)
        (row,) = pull(a, DEFAULT_GOAL, generate, "simple")["proposals"]
        publish(author)
        git(teammate, "pull", "--ff-only")
        (pending,) = relevant_followups(
            b, "Why revisit adaptive packing on single-tenant queues?"
        )
        assert pending["id"] == row["id"] and pending["status"] == "pending"
        approved = vote(a, row["id"], row["proposal"], AUTHORS[0], "approve")
        publish(author)
        git(teammate, "pull", "--ff-only")
        assert followups(b) == [approved] and approved["status"] == "approved_review"
        assert len(b.load("sources")) == 21 and qa["answers"][0]["answer"] == "tzdata"
        expected = {r["id"]: r["sha256"] for r in run["calls"]}
        assert used == [
            expected["pep-615/clean/simple"],
            expected["review-01/review/simple"],
        ]
        return {
            "job_id": run["job_id"],
            "question": question,
            "qa": qa,
            "before_owner_review": pending,
            "after_owner_review": approved["status"],
            "sources_retained": 21,
            "matched_prompt_hashes": used,
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bare_peps", type=Path)
    print(
        json.dumps(replay(parser.parse_args().bare_peps), ensure_ascii=False, indent=2)
    )
