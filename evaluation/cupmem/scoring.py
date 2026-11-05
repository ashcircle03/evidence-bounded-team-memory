"""Evaluator-only adapters for frozen team diagnostics, with no model calls.

``FrozenScorer.score_qa`` accepts native free text separately from a common
cited-reader answer. The cited schema is the existing timeline schema:
``{kind, answers: [{source_id, location, speaker, start, end, quote, answer,
status, condition: witness-or-null}]}``. Native answers are strings or the
original ``{answer, brief_rationale}`` object. Alias coverage is only a diagnostic
for native answers; it is never sufficient to establish correctness.

``score_proposals`` accepts an explicit shared-review interface with
``{kind, previous: witness, incoming: witness, reason}``, and an explicit
``trigger='write'|'prompted'``. Native CUPMem UPDATE/WEAKEN/etc. operations must
instead use ``audit_native_updates``: they are not silently mapped to review
proposals. Only frozen designated incoming/repeat events are labeled; earlier
arrivals are UNLABELED, never automatic negative examples.
An empty proposal list means a valid explicit no-proposal output. Callers must
retain parsing/execution failures separately, never coerce them to an empty list.

Blind semantic cards omit method/model/arm identifiers. Ratings are separate
objects keyed by card_id, with ``ok: bool``, nonempty ``reason`` and ``reviewer``,
and ``reviewer_type: human|model``. Missing ratings remain unknown. A model rating
is explicitly reported as such; it is never described as human adjudication.
The module does not rate its own cards or judge reasons with keyword rules.

Scripted owner actions are evaluator-only. ``applied_reviews`` contains actual
adapter receipts, not merely the scripts: script_sha256, actor, choice,
proposal_id, evidence_ref and applied=True. Their existence is not inferred from
an answer. The caller must bind those receipts to its execution audit. The fixed
timeline gold is never edited when owner approval was not reached. Its score,
the unreachable-approved-state flag, and QA against actual no-review state are
reported separately.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

from evaluation.timeline.score import contains_answer, grade_qa
from team_memory.store import digest as source_id
from .transfer_inputs import ROOT, verify_freeze


KINDS = {"reconsider", "coexist", "conflict", "correction"}
ALERT_KINDS = {"reconsider", "conflict", "correction"}


def _bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def _read(path):
    return json.loads(Path(path).read_text())


def _joint(*values):
    if any(value is False for value in values):
        return False
    return None if any(value is None for value in values) else True


def check_witness(witness, sources):
    """Check exact source identity, visible scope, attribution and literal span."""
    errors = []
    if not isinstance(witness, dict):
        return {"valid": False, "errors": ["witness_schema"]}
    sid = witness.get("source_id")
    env = sources.get(sid) if isinstance(sid, str) else None
    if env is None:
        return {"valid": False, "errors": ["source_not_visible"]}
    source = env["source"]
    for field in ("location", "speaker"):
        if witness.get(field) != source[field]:
            errors.append(field)
    quote, start, end = (witness.get(field) for field in ("quote", "start", "end"))
    if not isinstance(quote, str) or not quote:
        errors.append("empty_or_missing_quote")
    if (type(start) is not int or type(end) is not int
            or not 0 <= start < end <= len(source["text"])):
        errors.append("span")
    elif source["text"][start:end] != quote:
        errors.append("quote_span_mismatch")
    return {"valid": not errors, "errors": errors}


def _answer_schema(answer):
    if not isinstance(answer, dict) or not isinstance(answer.get("kind"), str) or not isinstance(answer.get("answers"), list):
        return False
    for row in answer["answers"]:
        if not isinstance(row, dict) or not all(isinstance(row.get(k), str) for k in ("source_id", "answer", "quote", "status")):
            return False
        condition = row.get("condition")
        if condition is not None and (not isinstance(condition, dict) or not isinstance(condition.get("quote"), str)):
            return False
    return True


def _blind_witness(value):
    return ({k: deepcopy(value[k]) for k in ("source_id", "location", "speaker", "start", "end", "quote") if k in value}
            if isinstance(value, dict) else deepcopy(value))


def _blind_answer(answer, output_mode):
    if output_mode == "native":
        return ({k: deepcopy(answer[k]) for k in ("answer", "brief_rationale") if k in answer}
                if isinstance(answer, dict) else answer)
    if not isinstance(answer, dict):
        return deepcopy(answer)
    rows = []
    for row in answer.get("answers", []) if isinstance(answer.get("answers"), list) else []:
        if not isinstance(row, dict):
            rows.append(deepcopy(row))
            continue
        item = _blind_witness(row)
        item.update({k: deepcopy(row[k]) for k in ("answer", "status") if k in row})
        if "condition" in row:
            item["condition"] = _blind_witness(row["condition"])
        rows.append(item)
    return {"kind": answer.get("kind"), "answers": rows}


def check_cited_answer(answer, sources):
    if not _answer_schema(answer):
        return {"valid": False, "errors": ["answer_schema"], "citations": []}
    checks, errors = [], []
    for index, row in enumerate(answer["answers"]):
        result = check_witness(row, sources)
        if not row["answer"].strip():
            result["valid"] = False
            result["errors"].append("empty_answer")
        condition = row.get("condition")
        if condition:
            result["condition"] = check_witness(condition, sources)
            if condition.get("source_id") != row["source_id"]:
                result["condition"]["valid"] = False
                result["condition"]["errors"].append("condition_source_differs")
            result["valid"] &= result["condition"]["valid"]
        checks.append(dict(answer_index=index, **result))
        if not result["valid"]:
            errors.append("citation_" + str(index))
    return {"valid": not errors, "errors": errors, "citations": checks}


def semantic_card(task, body, ratings=None):
    """Create a method-blinded card and read an explicit external rating only."""
    card = dict(task=task, **deepcopy(body))
    cid = sha256(_bytes(card)).hexdigest()
    rating = (ratings or {}).get(cid)
    if rating is None:
        result = {"status": "pending", "ok": None, "reviewer_type": None}
    else:
        if (not isinstance(rating, dict) or type(rating.get("ok")) is not bool
                or not all(isinstance(rating.get(k), str) and rating[k].strip() for k in ("reason", "reviewer"))
                or rating.get("reviewer_type") not in {"human", "model"}):
            raise ValueError("Malformed semantic rating for " + cid)
        result = dict(status="rated", **deepcopy(rating))
    return {"card_id": cid, "card": card, "rating": result}


def _legacy_mechanical(answer, sides, sources):
    """All frozen sides must retain their own source/answer/condition binding."""
    if not _answer_schema(answer):
        return {"correct": False, "errors": ["answer_schema"], "side_coverage": []}
    coverage, eligible = [], set()
    for side in sides:
        locations = side.get("locations", [side.get("location")])
        matching = []
        for index, row in enumerate(answer["answers"]):
            env = sources.get(row["source_id"])
            if not env or env["source"]["location"] not in locations:
                continue
            condition_text = row["quote"] + " " + ((row.get("condition") or {}).get("quote", ""))
            condition = side.get("condition")
            if (any(contains_answer(row["answer"], a) for a in side["aliases"])
                    and (not condition or contains_answer(condition_text, condition))):
                matching.append(index)
                eligible.add(index)
        coverage.append({"matched_answer_indices": matching, "covered": bool(matching)})
    errors = []
    if not all(side["covered"] for side in coverage):
        errors.append("missing_or_misbound_side")
    if eligible != set(range(len(answer["answers"]))):
        errors.append("unmatched_extra_answer")
    return {"correct": not errors, "errors": errors, "side_coverage": coverage}


class FrozenScorer:
    def __init__(self, root=ROOT):
        self.root = Path(root)
        frozen = verify_freeze(self.root)
        folder = self.root / "evaluation/cupmem"
        actor_file = folder / "transfer-inputs.json"
        manifest = _read(folder / "transfer-inputs.manifest.json")
        if sha256(actor_file.read_bytes()).hexdigest() != manifest["actor_sha256"]:
            raise ValueError("Transfer actor artifact changed")
        if manifest["source_files"] != frozen["source_files"]:
            raise ValueError("Transfer manifest does not match frozen sources")
        self.manifest = manifest
        actor = _read(actor_file)
        self.cases = {suite: {case["case_id"]: case for case in actor[suite]} for suite in ("git", "timeline")}
        self.keys = {"git": _read(self.root / "evaluation/design_review/key.json"),
                     "timeline": _read(self.root / "evaluation/timeline/final-key.json")}
        legacy_file = folder / "legacy-inputs.json"
        legacy_manifest = _read(folder / "legacy-inputs-manifest.json")
        if sha256(legacy_file.read_bytes()).hexdigest() != legacy_manifest["sha256"]:
            raise ValueError("Legacy input artifact changed")
        self.legacy = _read(legacy_file)
        self.legacy_cases = {case["id"]: case for case in self.legacy["cases"]}
        self.key_hashes = dict(frozen["source_files"])
        self.key_hashes["evaluation/cupmem/legacy-inputs.json"] = legacy_manifest["sha256"]

    def _event(self, suite, case_id, event_id, required_op):
        case = self.cases[suite][case_id]
        index = next(i for i, e in enumerate(case["events"]) if e["event_id"] == event_id)
        event = case["events"][index]
        if event["op"] != required_op:
            raise ValueError("Wrong checkpoint operation")
        sources = {source_id(e["source"]): e["source"] for e in case["events"][:index + 1] if e["op"] == "ingest"}
        return event, sources, self.manifest[suite][case_id]

    def _qa_context(self, suite, case_id, query_id):
        if suite == "legacy":
            case = self.legacy_cases[case_id]
            if query_id not in (None, case_id):
                raise ValueError("Legacy case has one original question")
            ids = self.legacy["histories"][case["history_id"]]["historical_source_ids"]
            sources = {sid: self.legacy["documents"][sid] for sid in ids}
            key = self.legacy["evaluation_only"][case_id]
            return case["question"], sources, key["expected_sides"], key, None, "legacy"
        event, sources, entry = self._event(suite, case_id, query_id, "ask")
        if suite == "git":
            return event["question"], sources, [], None, entry, "supplementary_git_no_fixed_qa_key"
        label = entry["queries"][query_id]["original_label"]
        key = self.keys[suite][entry["key_id"]]["qa"][label]
        sides = [{"source_id": row["source_id"], "location": sources[row["source_id"]]["source"]["location"],
                  "aliases": row["aliases"], "condition": row["condition"], "status": row["status"]}
                 for row in key["answers"]]
        group = "natural_timeline" if label.startswith("natural_") else "synthetic_timeline"
        return event["question"], sources, sides, key, entry, group

    def _review_state(self, entry, query_id, key, applied_reviews):
        if entry is None or query_id not in entry.get("queries", {}):
            return {"required_owner_reviews": 0, "applied_owner_reviews": 0,
                    "desired_workflow_state_reached": True, "unreachable_approved_state": False}
        query_index = entry["queries"][query_id].get("original_step_index", -1)
        required = [r for r in entry["deferred_reviews"] if r["original_step_index"] < query_index]
        applied = []
        for receipt in applied_reviews:
            if not isinstance(receipt, dict):
                raise ValueError("Owner-action receipt must be an object")
            matches = [r for r in required if r["script_sha256"] == receipt.get("script_sha256")]
            if not matches:
                raise ValueError("Owner-action receipt is not a preceding fixed review")
            script = matches[0]["script"]
            if (receipt.get("applied") is not True or receipt.get("actor") != script["actor"]
                    or receipt.get("choice") != script["choice"]
                    or not all(isinstance(receipt.get(k), str) and receipt[k] for k in ("proposal_id", "evidence_ref"))):
                raise ValueError("Owner-action receipt lacks actual application evidence")
            applied.append(receipt["script_sha256"])
        if len(applied) != len(set(applied)):
            raise ValueError("Duplicate owner-action receipt")
        reached = len(applied) == len(required)
        needs_approved = bool(key and any(row.get("status", "").startswith("approved_") for row in key.get("answers", [])))
        return {"required_owner_reviews": len(required), "applied_owner_reviews": len(applied),
                "desired_workflow_state_reached": reached,
                "fixed_key_requires_approved_state": needs_approved,
                "unreachable_approved_state": needs_approved and not reached,
                "receipt_validation": "structural binding only; execution audit must verify evidence_ref and actual generated proposal"}

    def score_qa(self, suite, case_id, query_id, answer, *, output_mode, applied_reviews=(), ratings=None):
        if suite not in {"git", "timeline", "legacy"} or output_mode not in {"native", "cited"}:
            raise ValueError("Unsupported suite or QA output mode")
        question, sources, sides, key, entry, group = self._qa_context(suite, case_id, query_id)
        workflow = self._review_state(entry, query_id, key, applied_reviews)
        if output_mode == "native":
            if isinstance(answer, str):
                text = answer
            elif isinstance(answer, dict) and isinstance(answer.get("answer"), str):
                text = answer["answer"]
            else:
                raise ValueError("Native QA must retain the actual free-form answer")
            aliases = [any(contains_answer(text, alias) for alias in side["aliases"]) for side in sides]
            fixed = {"status": "not_applicable_native_free_form", "correct": None}
            citations = {"status": "native_has_no_formal_citation_interface", "valid": None}
        else:
            text = "\n".join(row["answer"] for row in answer.get("answers", [])
                             if isinstance(row, dict) and isinstance(row.get("answer"), str)) if isinstance(answer, dict) and isinstance(answer.get("answers"), list) else ""
            aliases = [any(contains_answer(text, alias) for alias in side["aliases"]) for side in sides]
            citations = check_cited_answer(answer, sources)
            if suite == "timeline":
                fixed = grade_qa(answer, key) if _answer_schema(answer) else {"correct": False, "errors": ["answer_schema"]}
                fixed = dict(status="unchanged_frozen_timeline_grade_qa", **fixed)
            elif suite == "legacy":
                fixed = dict(status="frozen_legacy_side_binding", **_legacy_mechanical(answer, sides, sources))
            else:
                fixed = {"status": "unlabeled_no_fixed_git_qa_key", "correct": None}
        # Cards contain evaluator-selected reference sources, not a new model input.
        selected = {sid for sid, env in sources.items()
                    if any(sid == side.get("source_id") or env["source"]["location"] in side.get("locations", [side.get("location")]) for side in sides)}
        if output_mode == "cited" and isinstance(answer, dict) and isinstance(answer.get("answers"), list):
            selected.update(row.get("source_id") for row in answer.get("answers", []) if isinstance(row, dict))
        if not sides:
            selected = set(sources)
        reference_sources = [{"source_id": sid, **sources[sid]} for sid in sorted(selected) if sid in sources]
        body = dict(question=question, candidate=_blind_answer(answer, output_mode), reference_sides=sides,
                    reference_sources=reference_sources,
                    criterion="Judge answer truth, negation, subject/action/condition, all required sides, and whether each cited quote entails its answer. A matching alias or a literal quote alone is insufficient. Respect the stated reference statuses; do not invent approval.",
                    reference_selection="evaluator-only frozen references plus candidate cited sources; not supplied to either answer model")
        semantic = semantic_card("qa_fixed_reference_entailment", body, ratings)
        unearned = bool(output_mode == "cited" and _answer_schema(answer)
                        and workflow["applied_owner_reviews"] == 0
                        and any(row["status"].startswith("approved_") for row in answer["answers"]))
        actual = None
        if not workflow["desired_workflow_state_reached"]:
            # Do not repurpose the desired approved-state key as actual-state
            # truth. Include the complete visible prefix, including the old
            # report omitted by an answer that prematurely promoted a correction.
            actual_body = dict(question=question, candidate=_blind_answer(answer, output_mode),
                               visible_sources=[{"source_id": sid, **env} for sid, env in sources.items()],
                               criterion="Judge QA against the ACTUAL state: the planned owner review did not occur. Do not treat any correction as owner-approved. Retain unresolved original and proposed reports with their conditions. The frozen desired-state score is separate and must not be rewritten. Judge citation entailment independently of alias matching.",
                               actual_owner_approval_applied=False,
                               reference_selection="complete source prefix visible at this checkpoint; no desired-state key substituted")
            actual = semantic_card("qa_actual_no_review_state", actual_body, ratings)
        sem_ok = semantic["rating"]["ok"]
        fixed_joint = (_joint(fixed["correct"], citations["valid"], sem_ok) if output_mode == "cited"
                       else _joint(all(aliases), sem_ok)) if key else None
        actual_ok = (_joint(citations["valid"], not unearned, actual["rating"]["ok"])
                     if actual is not None and output_mode == "cited" else actual["rating"]["ok"] if actual else None)
        return dict(suite=suite, case_id=case_id, query_id=query_id, group=group, output_mode=output_mode,
                    fixed_key=fixed, citation_mechanics=citations,
                    alias_diagnostic={"side_coverage": aliases, "all_present": all(aliases) if sides else None,
                                      "meaning": "necessary lexical check only; not semantic correctness"},
                    semantic=semantic, fixed_reference_joint_correct=fixed_joint,
                    source_grounded_qa=_joint(citations["valid"], sem_ok) if output_mode == "cited" else sem_ok,
                    native_answer_semantic_correct=sem_ok if output_mode == "native" else None,
                    workflow=workflow, unearned_approval_claim=unearned,
                    actual_no_review_semantic=actual, actual_no_review_joint_correct=actual_ok,
                    key_changed=False)

    def audit_native_updates(self, suite, case_id, event_id, updates):
        self._event(suite, case_id, event_id, "ingest")
        return dict(suite=suite, case_id=case_id, event_id=event_id,
                    status="native_operations_unmapped_not_shared_review_proposals",
                    updates=deepcopy(updates), grounded_review=None, false_alerts=None,
                    limitation="Native memory operations require their own source audit; do not equate UPDATE/WEAKEN/INVALIDATE with owner-review proposals.")

    def score_proposals(self, suite, case_id, event_id, proposals, *, trigger, ratings=None):
        if suite not in {"git", "timeline"} or trigger not in {"write", "prompted"} or not isinstance(proposals, list):
            raise ValueError("Explicit shared-review proposals and detection trigger required")
        event, sources, entry = self._event(suite, case_id, event_id, "ingest")
        key = self.keys[suite][entry["key_id"]]
        incoming = source_id(event["source"])
        if suite == "timeline":
            coverage = "repeat" if incoming == key.get("repeat_source") else "incoming" if incoming == key["new"] else "unlabeled"
            old_id, new_id = key["old"], key["new"]
            expected_kind = key["expected_relation"]
            expected_review = key["expected_review"]
            criterion = key["reason_criterion"]
        else:
            all_events = self.cases[suite][case_id]["events"]
            last_source_event = [e for e in all_events if e["op"] == "ingest"][-1]
            coverage = "incoming" if event_id == last_source_event["event_id"] else "unlabeled"
            old_id = next((sid for sid, env in sources.items() if env["source"]["location"] == key["earlier"]), None)
            new_id = next((sid for sid, env in sources.items() if env["source"]["location"] == key["report"]), None)
            expected_review = key["expected"] == "review"
            expected_kind = "reconsider" if expected_review else None
            criterion = key["rubric"] + " Alternative distinction: " + key["distinction"]
        if coverage == "unlabeled":
            criterion = "This arrival has no frozen target/relation label. Audit only support from currently visible source evidence; do not use a later report or infer a negative label. This card cannot establish fixed-key review recall or false-positive rate."
        elif coverage == "repeat":
            criterion = "The frozen repeated-arrival case expects zero additional review alerts. Judge whether the proposed reason introduces a new, source-supported change; repetition alone does not supply new evidence. Report this separately from first-arrival positives and negatives."
        rows = []
        for proposal in proposals:
            if not isinstance(proposal, dict):
                raise ValueError("Proposal must be an explicit shared-review object")
            kind = proposal.get("kind")
            if not isinstance(kind, str) or kind not in KINDS:
                raise ValueError("Proposal kind must use the explicit shared-review schema, not native operations")
            old, new = proposal.get("previous"), proposal.get("incoming")
            old_check, new_check = check_witness(old, sources), check_witness(new, sources)
            old_sid = old.get("source_id") if isinstance(old, dict) else None
            new_sid = new.get("source_id") if isinstance(new, dict) else None
            reason_valid = isinstance(proposal.get("reason"), str) and bool(proposal["reason"].strip())
            literal = old_check["valid"] and new_check["valid"]
            arrival_bound = new_sid == incoming and old_sid != incoming
            expected_pair = old_sid == old_id and new_sid == new_id
            kind_correct = kind == expected_kind and kind in KINDS
            mechanical = literal and arrival_bound and expected_pair and kind_correct and reason_valid
            body = dict(proposal={"kind": kind, "previous": _blind_witness(old),
                                  "incoming": _blind_witness(new), "reason": proposal.get("reason")}, criterion=criterion,
                        sources=[{"source_id": sid, **sources[sid]} for sid in dict.fromkeys((old_sid, new_sid)) if sid in sources],
                        instruction="Explain whether the quoted source evidence supports this exact relation and reason, including subject/action/condition. Different conditions may coexist; same-condition incompatibility, explicit correction, and reconsideration of a decision are distinct. Do not infer correctness from topic overlap or quotation validity.")
            card = semantic_card("shared_review_reasoning", body, ratings)
            grounded = (_joint(mechanical, card["rating"]["ok"]) if coverage == "incoming"
                        else False if coverage == "repeat" else None)
            rows.append(dict(kind=kind, alert=kind in ALERT_KINDS, citation_mechanics={"previous": old_check, "incoming": new_check},
                             arrival_bound=arrival_bound, expected_pair=expected_pair if coverage == "incoming" else None,
                             expected_kind=kind_correct if coverage == "incoming" else None,
                             reason_present=reason_valid, semantic=card, grounded_relation=grounded))
        labeled = coverage == "incoming"
        eligible = [row["grounded_relation"] for row in rows if row["alert"]]
        grounded_review = (True if True in eligible else None if None in eligible else False) if labeled and expected_review else None
        return dict(suite=suite, case_id=case_id, event_id=event_id, trigger=trigger,
                    interface="explicit_shared_review_proposals_not_native_memory_operations",
                    label_coverage=coverage, expected_relation=expected_kind if labeled else None,
                    expected_review=expected_review if labeled else None, proposals=rows,
                    grounded_review=grounded_review,
                    false_alerts_on_review_negatives=sum(r["alert"] for r in rows) if labeled and not expected_review else 0,
                    wrong_relation_on_review_positives=sum(r["alert"] and r["expected_kind"] is False for r in rows) if labeled and expected_review else 0,
                    wrong_target_on_review_positives=sum(r["alert"] and r["expected_pair"] is False for r in rows) if labeled and expected_review else 0,
                    repeat_arrival_alerts=sum(r["alert"] for r in rows) if coverage == "repeat" else 0,
                    unlabeled_proposals=len(rows) if coverage == "unlabeled" else 0,
                    interpretation="Only trigger=write is a proactive shared-review result. Native CUPMem operations and prompted judgments remain separate.")


def summarize_proposals(rows):
    """Keep pending semantics, event coverage and detection trigger distinct."""
    groups = defaultdict(list)
    for row in rows:
        groups[(row["suite"], row["trigger"])].append(row)
    output = []
    for (suite, trigger), selected in sorted(groups.items()):
        incoming = [r for r in selected if r["label_coverage"] == "incoming"]
        positives = [r for r in incoming if r["expected_review"]]
        output.append(dict(suite=suite, trigger=trigger, labeled_incoming=len(incoming),
                           required_reviews=len(positives),
                           grounded_reviews_confirmed=sum(r["grounded_review"] is True for r in positives),
                           grounded_reviews_pending=sum(r["grounded_review"] is None for r in positives),
                           grounded_reviews_failed=sum(r["grounded_review"] is False for r in positives),
                           false_alerts_on_review_negatives=sum(r["false_alerts_on_review_negatives"] for r in selected),
                           wrong_relation_on_review_positives=sum(r["wrong_relation_on_review_positives"] for r in selected),
                           wrong_target_on_review_positives=sum(r["wrong_target_on_review_positives"] for r in selected),
                           repeat_arrival_alerts=sum(r["repeat_arrival_alerts"] for r in selected),
                           unlabeled_events=sum(r["label_coverage"] == "unlabeled" for r in selected)))
    return output
