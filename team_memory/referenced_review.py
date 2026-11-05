"""Follow a uniquely attributed regression to its source and collect independent text witnesses."""
import re

from . import contrast_review as contrast
from .evidence import FOLLOWUP
from .pair_selection import paragraphs
from .retrieval import rank,words

# A positive causal attribution and an ID must be adjacent. A bare citation, a
# reference to an unaffected earlier version, or a hash elsewhere is insufficient.
CAUSE = re.compile(r"\b(?:regression\s+(?:(?:was\s+)?introduced\s+)?(?:by|in|with|from)|"
                  r"(?:bug|breakage|failure)\s+(?:was\s+)?(?:caused|introduced)\s+by|"
                  r"segfaults?\s+starting\s+with)\s+(?:my\s+(?:recent\s+)?|commit\s+|the\s+commit\s+)?"
                  r"(?P<ref>(?:https?://[^\s)]+/commit/)?[0-9a-f]{7,40})\b",re.I)
REF_TITLE = re.compile(r"\b[0-9a-f]{7,40}\s*\([^)]{1,240}\)",re.I)
REASON = (
    "A verified reference in the new report attributes the regression to the earlier decision. "
    "Describe its concrete failure only within the reported condition, in one short sentence "
    "for the author. State what was done and what specifically went wrong. Do not repeat "
    "commit identifiers, infer motives, or turn a conditional into a universal statement."
)


def handles(text):
    refs=[]
    for m in CAUSE.finditer(text):
        prefix=text[max(0,m.start()-55):m.start()]
        if re.search(r"\b(?:no|not (?:a|the)|not caused by a|not a known)\s+$",prefix,re.I):
            continue
        refs.append(m.group("ref").lower().rsplit("/",1)[-1])
    return set(refs)


def assess(previous, sid, incoming, goal, generate):
    text=incoming["source"]["text"]
    refs=handles(text)
    if not refs:
        return contrast.assess(previous,sid,incoming,goal,generate)
    by_ref={}
    for ref in refs:
        ids=[k for k,(doc,_) in previous.items()
             if re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}",doc["source"]["location"].rsplit("/",1)[-1],re.I)
             and doc["source"]["location"].rsplit("/",1)[-1].lower().startswith(ref)]
        if len(ids)!=1:
            return {"action":"keep","basis":"attributed decision absent or ambiguous among earlier records"}
        by_ref[ref]=ids[0]
    if len(set(by_ref.values()))!=1:
        return {"action":"keep","basis":"report names multiple causes; no unique decision"}
    key=next(iter(by_ref.values()))
    new=paragraphs(sid,(incoming,"source_only"))
    target=paragraphs(key,previous[key])
    if not new or not target:return {"action":"keep","basis":"no source passages"}
    def substantive(p):
        clean=REF_TITLE.sub("",p.quote)
        clean=re.sub(r"\b[0-9a-f]{7,40}\b","",clean,flags=re.I)
        tokens=set(words(clean))-{"fix","fixe","regression","introduc","commit","caus","recent","patch"}
        return len(tokens)>=4
    body=[p for p in (new[1:] or new) if substantive(p)]
    if not body:return {"action":"keep","basis":"attribution has no independent report text"}
    reason_ctx={"goal":goal,"earlier_subject":target[0].quote,"report_subject":new[0].quote}
    update=contrast.witness(generate,contrast.REPORT,reason_ctx,contrast.shortlist(body,target[0].quote))
    old_ctx=dict(goal=goal,report=update.quote,record_topic=target[0].quote)
    old=contrast.witness(generate,contrast.EARLIER,old_ctx,contrast.shortlist(target[1:] or target,update.quote))
    pair=dict(earlier_topic=target[0].quote,earlier=old.quote,incoming=update.quote)
    reason=generate(REASON,contrast.encoded(pair)).strip()
    if not reason:return {"action":"invalid_output"}
    r=dict(action="reassess",previous=old.cite(),incoming=update.cite(),prior_rationale=old.cite(),rationale=reason,
           reviewer=previous[key][0]["owner"],next_step=FOLLOWUP["REASSESS"])
    # Keep an exact, independently resolvable witness for the direction of attribution.
    match=next((p for p in new if handles(p.quote)&refs),None)
    if match is None:
        return {"action":"keep","basis":"attribution crosses a source boundary"}
    r["attribution"]=match.cite()
    others={k:v[0]["source"]["text"] for k,v in previous.items() if k!=key and v[0]["source"]["text"].strip()}
    if others:
        competing=(rank(text,others) or sorted(others))[0]
        candidates=paragraphs(competing,previous[competing])
        foil=contrast.witness(generate,contrast.EARLIER,dict(goal=goal,report=update.quote,record_topic=candidates[0].quote),
                              contrast.shortlist(candidates[1:] or candidates,update.quote))
        diff=generate(contrast.DIFFERENCE,contrast.encoded(dict(pair,other=foil.quote))).strip()
        if not diff:return {"action":"invalid_output"}
        r.update(alternative=foil.cite(),distinction=diff)
    return r
