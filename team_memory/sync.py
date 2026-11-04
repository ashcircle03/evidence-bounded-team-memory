"""Review newly pulled source objects; only an original owner's vote closes a proposal."""

import fcntl
import os
from pathlib import Path
import subprocess
import tempfile

from .evidence import FOLLOWUP, active_sources, assess
from .retrieval import rank
from .store import digest


DEFAULT_GOAL = "Identify prior project decisions whose rationale should be revisited in light of new evidence."


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def followups(store):
    sources = store.load("sources")
    votes = list(store.load("followup_votes").values())
    result = []
    for pid, item in store.load("followups").items():
        old, new = item["previous"], item["incoming"]
        prior, incoming = (sources.get(w["source_id"]) for w in (old, new))
        if not prior or not incoming or prior["observed_at"] >= incoming["observed_at"]:
            continue
        valid = item["reviewer"] == prior["owner"] and item.get(
            "next_step"
        ) == FOLLOWUP.get(item["action"].upper())
        for w, env in ((old, prior), (new, incoming)):
            src = env["source"]
            valid &= (
                0 <= w["start"] < w["end"] <= len(src["text"])
                and w["quote"] == src["text"][w["start"] : w["end"]]
                and w["location"] == src["location"]
                and w["speaker"] == src["speaker"]
            )
        if not valid:
            continue
        choices = {
            v["choice"]
            for v in votes
            if v.get("proposal") == pid and v.get("actor") == prior["owner"]
        }
        status = {
            frozenset(): "pending",
            frozenset(["approve"]): "approved_review",
            frozenset(["reject"]): "rejected",
        }.get(frozenset(choices), "review_conflict")
        result.append(dict(item, id=pid, proposal=pid, kind="followup", status=status))
    return result


def vote(store, pid, basis, actor, decision):
    row = next((x for x in followups(store) if x["id"] == pid), None)
    if (
        not row
        or basis != pid
        or row["reviewer"] != actor
        or decision not in ("approve", "reject")
    ):
        raise ValueError("review requires exact proposal and original owner")
    new_status = "approved_review" if decision == "approve" else "rejected"
    if row["status"] == new_status:
        return row
    if row["status"] != "pending":
        raise ValueError("proposal is already closed or disputed")
    store.put("followup_votes", dict(proposal=pid, actor=actor, choice=decision))
    return dict(row, status=new_status)


def relevant_followups(store, question):
    candidates = {
        row["id"]: row
        for row in followups(store)
        if row["status"] in ("pending", "approved_review")
    }
    ordered = rank(
        question,
        {
            pid: r["previous"]["quote"] + " " + r["incoming"]["quote"]
            for pid, r in candidates.items()
        },
    )
    return [candidates[pid] for pid in ordered[:3]]


def assess_arrivals(store, arrivals, goal, generate, strategy):
    live = active_sources(store)
    output = []
    for sid in arrivals:
        if sid not in live:
            continue
        incoming = live[sid][0]
        previous = {
            key: pair
            for key, pair in live.items()
            if pair[0]["observed_at"] < incoming["observed_at"]
        }
        result = assess(previous, sid, incoming, goal, generate, strategy)
        if result["action"] in ("retest", "reassess"):
            pid = store.put("followups", dict(result, goal=goal, strategy=strategy))
            result = dict(result, id=pid)
        output.append(dict(source_id=sid, result=result))
    return output


def pull(store, goal, generate, strategy):
    """A private cursor survives an interrupted model call, even after Git advanced HEAD."""
    parent = store.root.resolve()
    while not parent.exists():
        parent = parent.parent
    root = Path(git(parent, "rev-parse", "--show-toplevel"))
    subdir = store.root.resolve().relative_to(root)
    cursor_name = "team-memory-pull-" + digest(
        {"store": str(subdir), "goal": goal, "strategy": strategy}
    )
    cursor = Path(
        git(root, "rev-parse", "--path-format=absolute", "--git-path", cursor_name)
    )
    with cursor.with_suffix(".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        return _pull_locked(store, goal, generate, strategy, root, subdir, cursor)


def _pull_locked(store, goal, generate, strategy, root, subdir, cursor):
    old = (
        cursor.read_text().strip()
        if cursor.exists()
        else git(root, "rev-parse", "HEAD")
    )
    if not cursor.exists():
        cursor.write_text(old)
    git(root, "pull", "--ff-only")
    head = git(root, "rev-parse", "HEAD")
    subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", old, head], check=True
    )
    path = subdir / "sources"
    diff = git(
        root, "diff", "--diff-filter=A", "--name-only", old, head, "--", str(path)
    )
    added = [
        Path(name).stem
        for name in diff.splitlines()
        if Path(name).parent == path and name.endswith(".json")
    ]
    results = assess_arrivals(store, added, goal, generate, strategy)
    with tempfile.NamedTemporaryFile(dir=cursor.parent, mode="w", delete=False) as f:
        f.write(head)
    os.replace(f.name, cursor)
    return dict(
        previous_head=old, head=head, arrivals=results, proposals=followups(store)
    )
