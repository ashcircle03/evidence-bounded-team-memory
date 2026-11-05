"""Export the already frozen team diagnostics without supplying their answer key.

Run locally (no inference): ``python -m evaluation.cupmem.transfer_inputs``.
The actor file contains source arrivals and existing questions only. The separate
``transfer-inputs.manifest.json`` is EVALUATOR-ONLY: it holds original case/query
labels, key locations, and the 12 simulated owner-review actions. Never serialize
that manifest into a model request.

One attributed source envelope becomes one user turn in one CUPMem session. This
is a team-record input adapter, not STALE's native conversational data. Metadata
and text are preserved literally; CUPMem's original personal-memory ontology is
unchanged. Query checkpoints are not user turns and future reports/questions are
not visible to the writer. ``native_record_at`` produces a prefix for diagnostics;
an efficient runner should use process_session/answer_query incrementally and
check that answering does not mutate persistent memory.

Reviews are deliberately absent from the actor event stream. At the original
review position, a runner may consult the manifest and ``review_gate`` to select
an ALREADY GENERATED, pending, correctly attributed proposal. The gate neither
creates a proposal nor writes an approval to memory. Native CUPMem has no owner
review interface, so its default gate result is unsupported and later QA remains
on its unapproved state. An explicitly labeled approval adapter can apply an
owner action only after the gate succeeds and must log the actual proposal and
model-request provenance. A prompted review judgment is not proactive detection.

All fixtures are previously exposed diagnostics. In particular, the hidden Git
view is copied verbatim from its frozen, already masked text; we do not remask it
or call it an unseen holdout. The preserved six Git questions are supplementary
to the 140 timeline QA checkpoints and the separate legacy-20 reconstruction.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

from team_memory.store import digest as source_id
from team_memory.timeline import valid_witness


ROOT = Path(__file__).resolve().parents[2]
FREEZE = "evaluation/cupmem/transfer-source-freeze.json"
GIT_INPUT = "evaluation/design_review/inputs.json"
TIMELINE_INPUT = "evaluation/timeline/final.json"


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def opaque_id(*parts):
    # These identifiers never expose condition, expected relation, or view labels.
    return sha256(encoded(list(parts)))[:24]


def verify_freeze(root):
    frozen = json.loads((root / FREEZE).read_text())
    for name, expected in frozen["source_files"].items():
        if sha256((root / name).read_bytes()) != expected:
            raise ValueError("Frozen transfer source changed: " + name)
    return frozen


def envelope_only(envelope):
    """Reject extra normalized/gold fields rather than forwarding unknown fields."""
    if set(envelope) != {"owner", "observed_at", "source"}:
        raise ValueError("Unexpected source-envelope fields")
    if set(envelope["source"]) != {"speaker", "location", "text"}:
        raise ValueError("Unexpected source fields")
    values = [envelope["owner"], envelope["observed_at"], *envelope["source"].values()]
    if not all(isinstance(value, str) and value for value in values):
        raise ValueError("Source metadata and text must be nonempty strings")
    return copy.deepcopy(envelope)


def attributed_session(envelope):
    """Only this exact projection goes to CUPMem's session writer."""
    return [{"role": "user", "content": encoded(envelope_only(envelope)).decode()}]


def native_record_at(case, event_index):
    """Return full raw history through one event, with only its current question.

    This does not apply review scripts or expose evaluator metadata. It is also a
    reference for direct-baseline history: both arms see identical source turns.
    """
    if not 0 <= event_index < len(case["events"]):
        raise IndexError(event_index)
    events = case["events"][:event_index + 1]
    sources = [event["source"] for event in events if event["op"] == "ingest"]
    current = events[-1]
    queries = {current["event_id"]: current["question"]} if current["op"] == "ask" else {}
    return {
        "uid": case["case_id"],
        "haystack_session": [attributed_session(source) for source in sources],
        "timestamps": [source["observed_at"] for source in sources],
        "probing_queries": queries,
    }


def review_gate(script, proposals, visible_sources, *, approval_adapter=False):
    """Select existing exact-source proposals; never manufacture owner approval.

    ``proposals`` must be actual arm outputs with recorded request provenance,
    not gold targets turned into proposals. The runner enforces that provenance.
    Matching follows the frozen timeline's kind/pair/quote-contains criteria and
    additionally validates literal witnesses, source visibility, pending status,
    history, and original-owner attribution. Returned IDs are candidates for the
    separate owner-action adapter, not evidence that an action was performed.
    """
    if not approval_adapter:
        return {"status": "unsupported_native_owner_review", "proposal_ids": []}
    if script.get("op") != "review" or script.get("choice") not in {"approve", "reject"}:
        raise ValueError("Invalid evaluator owner action")
    previous, incoming = script["previous"], script["incoming"]
    if previous not in visible_sources or incoming not in visible_sources:
        return {"status": "deferred_sources_not_visible", "proposal_ids": []}
    if script["actor"] != visible_sources[previous]["owner"]:
        return {"status": "rejected_wrong_owner", "proposal_ids": []}
    matched = []
    for proposal in proposals:
        old, new = proposal.get("previous", {}), proposal.get("incoming", {})
        if not all(valid_witness(w, visible_sources) for w in (old, new)):
            continue
        if (proposal.get("kind") == script["kind"]
                and old["source_id"] == previous and new["source_id"] == incoming
                and previous in proposal.get("history", [])
                and incoming not in proposal.get("history", [])
                and proposal.get("reviewer") == script["actor"]
                and proposal.get("status") == "pending"
                and script["old_contains"] in old["quote"]
                and script["new_contains"] in new["quote"]
                and isinstance(proposal.get("id"), str) and proposal["id"]):
            matched.append(proposal["id"])
    return {
        "status": "eligible_existing_proposal" if matched else "deferred_no_matching_proposal",
        "proposal_ids": sorted(set(matched)),
    }


def export_git(rows):
    cases, mapping = [], {}
    for row in rows:
        if set(row) - {"id", "prior", "incoming", "qa"}:
            raise ValueError("Unexpected Git case fields")
        cid = opaque_id(GIT_INPUT, row["id"])
        events, sources = [], []
        for index, env in enumerate([*row["prior"], row["incoming"]]):
            env = envelope_only(env)
            events.append({"op": "ingest", "event_id": opaque_id(cid, index), "source": env})
            sources.append({"source_id": source_id(env), "source_sha256": sha256(encoded(env)),
                            "original_role": "incoming" if index == len(row["prior"]) else "prior"})
        queries = {}
        if "qa" in row:
            qid = opaque_id(cid, len(events))
            events.append({"op": "ask", "event_id": qid, "question": row["qa"]})
            queries[qid] = {"original_label": "qa", "source": GIT_INPUT}
        cases.append({"case_id": cid, "events": events})
        mapping[cid] = {"original_id": row["id"], "source": GIT_INPUT,
                        "key_file": "evaluation/design_review/key.json", "key_id": row["id"],
                        "sources": sources, "queries": queries, "deferred_reviews": []}
    return cases, mapping


def export_timeline(rows):
    cases, mapping = [], {}
    for row in rows:
        if set(row) != {"id", "steps"}:
            raise ValueError("Unexpected timeline case fields")
        cid = opaque_id(TIMELINE_INPUT, row["id"])
        events, queries, sources, reviews = [], {}, [], []
        for index, step in enumerate(row["steps"]):
            eid = opaque_id(cid, index)
            if step["op"] == "ingest":
                env = envelope_only(step["source"])
                events.append({"op": "ingest", "event_id": eid, "source": env})
                sources.append({"source_id": source_id(env), "source_sha256": sha256(encoded(env)),
                                "event_id": eid, "original_step_index": index})
            elif step["op"] == "ask":
                events.append({"op": "ask", "event_id": eid, "question": step["question"]})
                queries[eid] = {"original_label": step["id"], "original_step_index": index}
            elif step["op"] == "review":
                reviews.append({"original_step_index": index,
                                "after_event_id": events[-1]["event_id"] if events else None,
                                "script": copy.deepcopy(step), "script_sha256": sha256(encoded(step))})
            else:
                raise ValueError("Unknown timeline operation")
        cases.append({"case_id": cid, "events": events})
        mapping[cid] = {"original_id": row["id"], "source": TIMELINE_INPUT,
                        "key_file": "evaluation/timeline/final-key.json", "key_id": row["id"],
                        "sources": sources, "queries": queries, "deferred_reviews": reviews}
    return cases, mapping


def build(root=ROOT):
    frozen = verify_freeze(root)
    git, git_map = export_git(json.loads((root / GIT_INPUT).read_text()))
    timeline, timeline_map = export_timeline(json.loads((root / TIMELINE_INPUT).read_text()))
    actors = {"schema": "cupmem-transfer-raw-v1", "git": git, "timeline": timeline}
    counts = {"git_cases": len(git), "timeline_streams": len(timeline)}
    for name, rows in (("git", git), ("timeline", timeline)):
        ops = Counter(event["op"] for case in rows for event in case["events"])
        counts[name + "_source_arrivals"] = ops["ingest"]
        counts[name + "_qa_checkpoints"] = ops["ask"]
    counts["deferred_owner_reviews"] = sum(len(m["deferred_reviews"]) for m in timeline_map.values())
    if counts != {"git_cases": 60, "timeline_streams": 20, "git_source_arrivals": 180,
                  "git_qa_checkpoints": 6, "timeline_source_arrivals": 100,
                  "timeline_qa_checkpoints": 140, "deferred_owner_reviews": 12}:
        raise ValueError("Unexpected frozen transfer counts: " + repr(counts))
    if len({case["case_id"] for case in git + timeline}) != 80:
        raise ValueError("Duplicate opaque case IDs")
    manifest = {
        "schema": "cupmem-transfer-evaluator-manifest-v1",
        "audience": "evaluator_only_never_model_input",
        "purpose": "previously exposed diagnostic cases; no held-out performance claim",
        "actor_file": "evaluation/cupmem/transfer-inputs.json",
        "actor_sha256": sha256(encoded(actors)),
        "exporter_sha256": sha256(Path(__file__).read_bytes()),
        "source_freeze_sha256": sha256((root / FREEZE).read_bytes()),
        "source_files": frozen["source_files"], "counts": counts,
        "git": git_map, "timeline": timeline_map,
        "execution_rules": [
            "Use attributed_session only for ingests; do not ingest QA questions or model answers.",
            "Process sources in original arrival order and never reveal future source text.",
            "Direct and CUPMem arms receive identical raw source history at each checkpoint.",
            "Keep cases independent; opaque IDs never expose mixed/no-match or raw/hidden labels.",
            "Preserve frozen hidden-view redactions and original author/date/location/text verbatim.",
            "Native CUPMem has no owner-review API: record unsupported, do not inject approval.",
            "Any labeled approval adapter must pass review_gate on actual arm proposals, log their model-request provenance, then record the owner action separately.",
            "A skipped scripted review makes later QA a no-review state, not a post-approval QA failure.",
            "A query explicitly asking for review is prompted review, not proactive write-time detection.",
            "Natural QA, synthetic workflow QA, supplementary Git QA and legacy20 are distinct result groups.",
        ],
    }
    return actors, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    actors, manifest = build(args.root)
    folder = args.root / "evaluation/cupmem"
    (folder / "transfer-inputs.json").write_bytes(encoded(actors))
    (folder / "transfer-inputs.manifest.json").write_bytes(encoded(manifest))
    print(json.dumps({"status": "fixtures_exported_no_inference", **manifest["counts"],
                      "actor_sha256": manifest["actor_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
