"""Test a selected pair for a specific change before asking its owner to review."""
import json
import re
from statistics import fmean

from .evidence import FOLLOWUP
from .pair_selection import select

CHANGE = (
    "Do the records show that the EARLIER decision needs checking under a specific condition? "
    "Look for a counterexample, a change to a premise, or a measured difference relevant to "
    "that very decision. Merely changing the same software is insufficient. "
    "Use the explicit time roles even when REPORT comes first. Answer Yes or No."
)
SEPARATE = (
    "Can the REPORT be fully accounted for as an independent change, confirmation, or "
    "background information that leaves the EARLIER decision's rationale and scope intact? "
    "A concrete exception to that decision makes the answer No. "
    "Use the explicit time roles even when REPORT comes first. Answer Yes or No."
)
FOCUS = (
    "Does the REPORT sentence state a specific circumstance and changed behavior, observation "
    "or requirement that bears on the EARLIER decision? An incidental implementation detail, "
    "unrelated cost, generic assertion of a fix, or proposed future work is insufficient. "
    "Answer Yes or No."
)
EXPLAIN = (
    "Write a brief review request for the original author. State the earlier behavior, the "
    "particular circumstance revealed by the report, and what must be rechecked in that "
    "circumstance. Prefer the reported failure or exception over a detail about the fix. "
    "Use the selected sentence as a lead and check it against the full report passage. "
    "Do not infer that other conditions are safe. Answer in one sentence, using only these records."
)


def fields(goal, earlier, report, report_first=False):
    records = [("EARLIER", earlier), ("REPORT", report)]
    if report_first:
        records.reverse()
    return json.dumps(dict([("goal", goal), *records]), ensure_ascii=False)


def relation(earlier, report, goal, margin, report_first=False):
    votes = []
    for reverse in (report_first, not report_first):
        content = fields(goal, earlier, report, reverse)
        votes.append(margin(CHANGE, content) - margin(SEPARATE, content))
    return fmean(votes)


def explain(pair, goal, generate):
    old, new = pair.old.quote, pair.new.quote
    candidates = re.split(r"(?<=[.!?])\s+(?=[A-Z가-힣\x60])", new)
    focus = max(candidates, key=lambda sentence: generate.evidence_margin(
        FOCUS, fields(goal, old, sentence)))
    content = json.dumps(dict(goal=goal, earlier=old, report=new, selected_report_sentence=focus),
                         ensure_ascii=False)
    return generate(EXPLAIN, content).strip(), focus


def adjudicate(pair, previous, goal, generate, *, report_first=False):
    if pair is None:
        return {"action": "keep", "basis": "no pair of source passages"}
    score = relation(pair.old.quote, pair.new.quote, goal, generate.evidence_margin, report_first)
    if score <= 0:
        return {"action": "keep", "basis": "the selected pair did not favor a specific change"}
    reason, focus = explain(pair, goal, generate)
    if not reason:
        return {"action": "invalid_output"}
    return dict(action="reassess", previous=pair.old.cite(), incoming=pair.new.cite(),
                prior_rationale=pair.old.cite(), rationale=reason, change_sentence=focus,
                reviewer=previous[pair.old.sid][0]["owner"], next_step=FOLLOWUP["REASSESS"])


def assess(previous, sid, incoming, goal, generate):
    pair = select(previous, sid, incoming, goal, generate.evidence_margin)
    return adjudicate(pair, previous, goal, generate)
