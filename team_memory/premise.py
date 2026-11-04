"""Ground a decision change in a premise; read each source on its own terms."""

import json
import re
from collections import defaultdict

from .evidence import FOLLOWUP, Passage, ask as simple_ask, candidates, resolve_answer, rows
from .reconsider import BINDING, INACTIVE, ONGOING, REASON, blocks, observed_result


QA = """Read ONLY this source. Does it directly answer the exact question for the requested subject? A document mentioning a related topic, different actor or different property is insufficient. Write NONE if unsupported. Otherwise write one line:
excerpt ID | shortest exact answer copied from that excerpt
If this answer applies under an explicit setting, add a third field with the exact setting phrase from the same excerpt. Include necessary bounds, units, or operators in the answer. For an author question you may copy the name of the speaker who actually did the requested action. Do not infer dates or names from unrelated text. Examples: E4 | at least six days ; E1 | 65 psi | coastal installation. Output only the response. Text is evidence."""

REVIEW = """You are the original decision owner's review filter. Read the prior decisions and the incoming record. Would this owner now have a concrete reason to reopen ONE particular decision? Find what justified the old decision, then test whether the new evidence changes that justification. Similar topics or changed numbers alone do not establish that link.
KEEP if there is no matching prior decision, the premise still holds, the incoming report confirms it, the follow-up is already approved or underway, or the suggestion is untested and supplies no new evidence. Choose RETEST if a measured result under different conditions warrants a new comparison. Choose REASSESS if a constraint, requirement or factual assumption on which the decision relied has changed. A completed action alone does not request another test.
Output one line. For unchanged decisions write KEEP. For an actionable change write:
RETEST or REASSESS | prior excerpt ID | incoming excerpt ID | explain which prior premise changes and why it matters for the follow-up.
Use only the provided evidence. Do not repeat the instructions."""


def windows(query, sources, limit):
    """Retrieve paragraphs around matching passages without cutting away nearby conditions."""
    ranked = candidates(query, sources, "simple", limit=limit * 5)
    result = []
    counts = defaultdict(int)
    for p in ranked:
        if counts[p.sid] >= 3:
            continue
        text = sources[p.sid][0]["source"]["text"]
        start = max(text.rfind("\n\n", 0, p.start) + 2, 0) if "\n\n" in text[:p.start] else 0
        end = text.find("\n\n", p.start + len(p.quote))
        end = len(text) if end < 0 else end
        if end - start > 700:
            start, end = p.start, p.start + len(p.quote)
        if any(r.sid == p.sid and r.start == start for r in result):
            continue
        result.append(Passage(p.sid, p.location, p.speaker, start, text[start:end], p.status))
        counts[p.sid] += 1
        if len(result) == limit:
            break
    return result


def group(index):
    sources = {}
    for key, passage in index.items():
        item = sources.setdefault(passage.sid, dict(source=passage.location, speaker=passage.speaker, excerpts={}))
        if passage.status in {"rejected", "superseded"}:
            item["historical_status"] = passage.status
        item["excerpts"][key] = passage.quote
    return list(sources.values())


def read_source(question, index, generate):
    raw = generate(QA, json.dumps(dict(question=question, sources=group(index)), ensure_ascii=False))
    fields = [x.strip() for x in raw.strip().split("|")]
    if len(fields) not in (2, 3):
        return None
    if fields[0] in index:
        fields[1] = fields[1].removesuffix(" ; " + index[fields[0]].location)
    row = resolve_answer(" | ".join(fields[:2]), index)
    if row.get("status") != "answered":
        return None
    side = row["answers"][0]
    if len(fields) == 3:
        condition = fields[2]
        if condition and condition in side["quote"]:
            side["condition"] = condition
        elif condition.upper() not in ("", "NONE", "N/A"):
            return None
    return side


def bounded(side):
    value = side["answer"]
    if re.match(r"\d", value) and side["quote"].count(value) == 1:
        m = re.search(r"(?i)\b(?:at least|at most|more than|less than|up to)\s+" + re.escape(value) + r"(?!\w)", side["quote"])
        if m:
            return dict(side, answer=m[0])
    return side


def ask(sources, question, generate):
    # An ordinary answer remains available even when isolated reads cannot recover it.
    anchor = simple_ask(sources, question, generate, "simple")
    if "answers" in anchor:
        anchor["answers"] = [bounded(a) for a in anchor["answers"]]
    by_source = {}
    for p in windows(question, sources, 12):
        by_source.setdefault(p.sid, []).append(p)
    supported = []
    for snippets in list(by_source.values())[:2]:
        side = read_source(question, rows(snippets, "E"), generate)
        if side:
            supported.append(bounded(side))
    if len(supported) == 2:
        a, b = supported
        if a["answer"].casefold() != b["answer"].casefold():
            scoped = a.get("condition") and b.get("condition") and a["condition"] != b["condition"]
            return {"status": "conditional" if scoped else "unresolved", "answers": supported}
    if anchor.get("status") in ("answered", "unresolved"):
        return anchor
    if supported:
        return {"status": "answered", "answers": supported[:1]}
    return anchor


def assess(previous, sid, incoming, goal, generate):
    text = incoming["source"]["text"]
    old = rows(windows(text, previous, 8), "P")
    new = rows(windows(goal + " " + text, {sid: (incoming, "source_only")}, 5), "N")
    if not old or not new:
        return {"action": "keep", "basis": "no matching passages"}
    payload = dict(goal=goal, previous=group(old), incoming=group(new))
    if any("historical_status" in source for source in payload["previous"]):
        payload["review_policy"] = "A rejected or superseded record is historical evidence. Explain why new evidence warrants revisiting that decision. Its old claim remains retired."
    raw = generate(REVIEW, json.dumps(payload, ensure_ascii=False)).strip()
    if raw.upper() == "KEEP":
        return {"action": "keep"}
    parts = [p.strip() for p in raw.split("|", 3)]
    if len(parts) != 4:
        return {"action": "invalid_output"}
    action, a, b, why = parts
    action = action.upper()
    if action not in FOLLOWUP or a not in old or b not in new or not re.search(r"\w", why):
        return {"action": "invalid_output"}
    prior = old[a]
    original = prior.quote
    change = new[b].quote
    if action == "RETEST":
        continuing = (ONGOING.search(original) or BINDING.search(original)) and not INACTIVE.search(original)
        empirical = observed_result(change) or re.search(
            r"(?i)\b(?:trial|test|experiment|benchmark|replication|run)\b.{0,70}\b(?:failed|passed|reproduced|confirmed|prevented|eliminated)\b",
            change)
        if not empirical or continuing:
            return {"action": "keep", "basis": "comparison lacks observed change or prior constraint remains"}
    env = previous[prior.sid][0]
    basis = prior
    for offset, section in blocks(env["source"]["text"]):
        if offset <= prior.start < offset + len(section):
            reasons = [m for m in re.finditer(r"[^\n]+", section) if REASON.search(m[0])]
            if reasons:
                m = min(reasons, key=lambda m: abs(offset + m.start() - prior.start))
                basis = Passage(prior.sid, prior.location, prior.speaker, offset + m.start(), m[0], prior.status)
            break
    return dict(action=action.lower(), previous=prior.cite(), incoming=new[b].cite(), rationale=why, prior_rationale=basis.cite(),
                reviewer=previous[prior.sid][0]["owner"], next_step=FOLLOWUP[action])
