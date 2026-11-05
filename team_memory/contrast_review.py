"""Compare earlier decisions against the same report, including a no-match alternative."""
import json
from statistics import fmean

from .evidence import FOLLOWUP
from .pair_selection import paragraphs
from .retrieval import rank


REPORT = (
    "Select the original passage that most precisely states the new observation: under which "
    "condition, which operation produces what behavior? Prefer the actual symptom and its cause "
    "over a citation, commit attribution, heading, or implementation aside. Return the letter."
)
EARLIER = (
    "Select the passage that explains the behavior or assumption THIS earlier record establishes, "
    "on the part of the system closest to the report. If it handles a different operation, select "
    "its actual operation rather than words it shares with the report. Return the letter."
)
MATCH = (
    "Identify the one earlier decision for which this report gives concrete grounds to reopen "
    "the decision. Match the specific operation, precondition and consequence. An actual bug "
    "in the same subsystem can leave both decisions intact. Choose the independent option "
    "if neither decision, or no unique decision, is implicated. Return the letter."
)
REASON = (
    "Write one precise sentence for the earlier decision's owner. Name the earlier operation "
    "and the observed condition that now makes that operation fail or require a new test. "
    "Use only the two quoted passages. Do not recite commit history or invent an exception."
)
DIFFERENCE = (
    "What operation does the other decision address, and how does that differ from the specific "
    "operation in the incoming report? Answer in one short sentence using the quotations. "
    "Do not invent a change to the other decision."
)
NONE = "Independent or insufficient evidence: no unique earlier decision needs review."


def encoded(value):
    return json.dumps(value, ensure_ascii=False)


def choose(reader, instruction, context, options):
    """Give every option each letter and physical position once before comparing logits."""
    count = len(options)
    if count == 1:
        return 0
    scores = [[] for _ in options]
    for shift in range(count):
        perm = list(range(shift, count)) + list(range(shift))
        choices = {chr(65 + pos): options[idx] for pos, idx in enumerate(perm)}
        values = reader.option_scores(instruction, encoded(dict(context, choices=choices)), count)
        for idx, value in zip(perm, values, strict=True):
            scores[idx].append(float(value))
    means = list(map(fmean, scores))
    maximum = max(means)
    # The abstention option is last for the decision calls, so a tie does not open a review.
    return max(idx for idx, value in enumerate(means) if value == maximum)


def shortlist(items, query):
    if len(items) <= 5:
        return items
    quotes = {str(i): p.quote for i, p in enumerate(items)}
    priority = [0, 1, *(int(k) for k in rank(query, quotes)), *range(len(items))]
    return [items[i] for i in sorted(list(dict.fromkeys(priority))[:5])]


def witness(reader, instruction, context, options):
    return options[choose(reader, instruction, context, [p.quote for p in options])]


def assess(previous, sid, incoming, goal, generate):
    report = paragraphs(sid, (incoming, "source_only"))
    plain = incoming["source"]["text"]
    docs = {k: v[0]["source"]["text"] for k, v in previous.items() if v[0]["source"]["text"].strip()}
    if not docs or not report:
        return {"action": "keep", "basis": "no comparable source passages"}
    ranked = rank(plain, docs)
    keys = list(dict.fromkeys(ranked + sorted(docs)))[:2]
    blocks = [shortlist(paragraphs(k, previous[k]), plain) for k in keys]
    context = dict(goal=goal, incoming="\n\n".join(p.quote for p in shortlist(report, " ".join(docs[k] for k in keys))))
    # First establish relevance using whole-document excerpts. Then try to reproduce the
    # assignment with three original witnesses stripped of surrounding context.
    documents = ["\n\n".join(p.quote for p in spans) for spans in blocks]
    target = choose(generate, MATCH, context, documents + [NONE])
    if target == len(keys):
        return {"action": "keep", "basis": "no unique decision in the document comparison"}
    new = witness(generate, REPORT, {"goal": goal}, shortlist(report, " ".join(documents)))
    old = [witness(generate, EARLIER, dict(goal=goal, report=new.quote, record_topic=spans[0].quote), spans)
           for spans in blocks]
    reproduced = choose(generate, MATCH, dict(goal=goal, incoming=new.quote), [p.quote for p in old] + [NONE])
    if reproduced != target:
        return {"action": "keep", "basis": "the exact passages did not reproduce the document judgment"}
    prior = old[target]
    relation = dict(earlier=prior.quote, incoming=new.quote)
    reason = generate(REASON, encoded(relation)).strip()
    if not reason:
        return {"action": "invalid_output"}
    result = dict(action="reassess", previous=prior.cite(), incoming=new.cite(),
                  prior_rationale=prior.cite(), rationale=reason, reviewer=previous[prior.sid][0]["owner"],
                  next_step=FOLLOWUP["REASSESS"])
    if len(old) == 2:
        other = old[1-target]
        contrast = generate(DIFFERENCE, encoded(dict(relation, other=other.quote))).strip()
        if not contrast:
            return {"action": "invalid_output"}
        result.update(alternative=other.cite(), distinction=contrast)
    return result
