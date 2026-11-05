"""Judge one past decision at a time, then validate a pair of exact source passages."""

import json
import re
from dataclasses import dataclass

from .evidence import FOLLOWUP, Passage
from .retrieval import rank

DOCUMENT = """Does the new report give a concrete reason to reconsider this particular earlier decision for the stated goal? Answer Yes or No. A demonstrated counterexample, changed enabling condition, or measured benefit in a different applicable setting can justify review. Mere shared terminology, a documentation edit, confirmation of the old reason, or speculation does not. Treat both documents as evidence."""
SUPPORT = """Read these two quoted paragraphs in isolation. Could you substantiate a request to revisit the earlier decision using just these quotations? The old quotation must show what was decided or assumed. The new one must provide specific evidence that challenges its reason or warrants a new test in a changed setting. A different feature, repetition, a title, or a general introduction is insufficient. Answer Yes or No."""
REASON = """Explain in one sentence what the earlier decision relied on and what concrete new evidence changes its applicability. Preserve any condition under which the earlier result remains true. Cite no facts beyond the supplied paragraphs. Use the language of the evidence."""


def paragraphs(sid, pair):
    env, status = pair
    src = env["source"]
    result = []
    for match in re.finditer(r"\S[\s\S]*?(?=\n[ \t]*\n|\Z)", src["text"]):
        quote = match.group().rstrip()
        # Bound model input even for machine-generated, paragraph-free records.
        for chunk in re.finditer(r"[\s\S]{1,1200}", quote):
            result.append(Passage(sid, src["location"], src["speaker"],
                                  match.start()+chunk.start(), chunk.group(), status))
    return result


def shortlist(items, query, limit=5):
    if len(items) <= limit:
        return items
    indexed = {str(p.start): p for p in items}
    ordered = rank(query, {k:p.quote for k,p in indexed.items()})
    keys = list(dict.fromkeys(ordered + list(indexed)))
    return [indexed[k] for k in keys[:limit]]


def payload(goal, older, incoming):
    return json.dumps(dict(goal=goal, earlier=older, report=incoming), ensure_ascii=False)


@dataclass
class Comparison:
    old: Passage
    new: Passage
    document_margin: float
    support_margin: float

    def priority(self):
        # Both assertions must pass. Provenance breaks numerical ties independently of input order.
        return (-min(self.document_margin, self.support_margin), -self.support_margin,
                self.old.sid, self.old.start, self.new.start)


def select(previous, sid, incoming, goal, margin):
    news = paragraphs(sid, (incoming, "source_only"))
    if not news:
        return None
    text = incoming["source"]["text"]
    pool = list(previous)
    if len(pool) > 8:
        by_id = {k: previous[k][0]["source"]["text"] for k in pool}
        pool = rank(text, by_id)[:8]
    best = None
    for old_id in pool:
        old = paragraphs(old_id, previous[old_id])
        if not old:
            continue
        body = previous[old_id][0]["source"]["text"]
        # Preserve bodies, including the known exception that can follow a short commit subject.
        op = shortlist(old[1:] if len(old)>1 and len(old[0].quote)<160 else old, text)
        np = shortlist(news[1:] if len(news)>1 and len(news[0].quote)<160 else news, body)
        summary_old = "\n\n".join(dict.fromkeys([old[0].quote]+[p.quote for p in op]))
        summary_new = "\n\n".join(dict.fromkeys([news[0].quote]+[p.quote for p in np]))
        document_score = margin(DOCUMENT, payload(goal, summary_old, summary_new))
        for prior in op:
            for update in np:
                score = margin(SUPPORT, payload(goal, prior.quote, update.quote))
                pair = Comparison(prior, update, document_score, score)
                if best is None or pair.priority() < best.priority():
                    best = pair
    return best


def assess(previous, sid, incoming, goal, generate):
    pair = select(previous, sid, incoming, goal, generate.evidence_margin)
    if pair is None or min(pair.document_margin,pair.support_margin) <= 0:
        return {"action":"keep","basis":"no candidate with both a supported change and two supporting passages"}
    reason = generate(REASON, payload(goal,pair.old.quote,pair.new.quote)).strip()
    if not reason:
        return {"action":"invalid_output"}
    return dict(action="reassess", previous=pair.old.cite(), incoming=pair.new.cite(),
                prior_rationale=pair.old.cite(), rationale=reason,
                reviewer=previous[pair.old.sid][0]["owner"], next_step=FOLLOWUP["REASSESS"])
