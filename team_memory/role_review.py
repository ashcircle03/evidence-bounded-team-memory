"""Bind factual review statements to exact source spans, preserving agents and polarity."""
import re

from . import contrast_review as contrast
from . import referenced_review
from .role_binding import bind

ROLES = {
    "subject": "the actor, function or entity whose behavior is asserted",
    "action": "the asserted predicate, including direction, negation and its object",
    "condition": "the trigger, input or affected execution context limiting that action",
}
ALIGN = (
    "For the requested role, copy a short literal fragment from the CLAIM and a short literal "
    "fragment from a SOURCE passage which proves that role, preserving who did what to whom. "
    "Use just one line: claim fragment ||| source fragment. No quotation wrappers or commentary. "
    "Copy text verbatim; do not translate. If the role is missing or unsupported, answer NONE."
)
ENTAIL = (
    "Judge the WHOLE claim only from the source passages. Every assertion, including an added "
    "option, caller/callee relationship, polarity, condition or speculative consequence, must "
    "be warranted. A correct main point does not excuse an ungrounded addition. Return the letter."
)
VERDICTS = ["All assertions are supported by the supplied sources.", "At least one assertion is unsupported."]
EXTRACT = """Copy a short substring from the observation in answer to the question. Preserve spelling and negation.
Example observation: In read-only mode, the cache cannot store entries on disk.
Which entity performs or undergoes the action? the cache
What does it do or fail to do? cannot store entries on disk
Under what condition or on which input/path? In read-only mode
Return only the substring from the actual observation."""
ROLE_QUESTIONS = {
    "subject": "Which named entity performs or undergoes the reported action?",
    "action": "What does that entity do or fail to do? Include the object and the direction.",
    "condition": "Under what specific condition or on which input or execution path?",
}
FOCUS = (
    "Choose the passage that states the actual behavior and its specific triggering condition "
    "without changing the subject, direction, polarity or scope. Prefer a concrete exception "
    "or observation to a citation, speculation, or implementation aside. Return the letter."
)
FLAGS = re.compile(r"(?<![\w-])--?[A-Za-z][\w-]*")
CALL = r"[A-Za-z_][\w]*\(\)"
NESTED = re.compile(r"("+CALL+r")\s+(?:from within|inside|within|in)\s+("+CALL+r")")


def clean(text):
    return " ".join(text.split())


def locate(text, fragment):
    fragment = clean(fragment)
    if len(fragment) >= 2 and (fragment[0], fragment[-1]) in (('"','"'),("“","”"),("'","'"),("`","`")) and fragment not in clean(text):
        fragment = fragment[1:-1]
    if not fragment or fragment.upper()=="NONE":
        return None
    pattern = r"\s+".join(re.escape(word) for word in fragment.split())
    if fragment[0].isalnum():
        pattern = r"(?<![\w-])" + pattern
    if fragment[-1].isalnum():
        pattern += r"(?![\w-])"
    matches = list(re.finditer(pattern, text))
    if len(matches)!=1:
        return None
    m=matches[0]
    return {"start":m.start(),"end":m.end(),"quote":m.group()}


def evidence_link(witness, local):
    return dict(witness,start=witness["start"]+local["start"],end=witness["start"]+local["end"],quote=local["quote"])


def unsupported_details(claim, passages):
    text=" ".join(clean(p["quote"]) for p in passages)
    flags=set(FLAGS.findall(claim))-set(FLAGS.findall(text))
    issues=["option absent from evidence: "+v for v in sorted(flags)]
    for inner,outer in NESTED.findall(claim):
        nesting=re.escape(inner)+r"\s+(?:from within|inside|within|in)\s+"+re.escape(outer)
        calls=re.escape(outer)+r"\s+(?:calls?|invokes?)\s+"+re.escape(inner)
        if not re.search(nesting+"|"+calls,text):
            issues.append("unsupported nesting: "+inner+" in "+outer)
    return issues


def audit(claim, passages, generate):
    facts=[clean(p["quote"]) for p in passages]
    result={}
    missing=unsupported_details(claim,passages)
    for role,task in ROLES.items():
        ctx=dict(claim=claim,role=task,sources=facts)
        line=generate(ALIGN,contrast.encoded(ctx)).strip().split("|||")
        if len(line)!=2:
            continue
        assertion=locate(claim,line[0])
        links=[evidence_link(p,span) for p in passages if (span:=locate(p["quote"],line[1]))]
        if assertion and len(links)==1:
            result[role]=dict(assertion=assertion,evidence=links[0])
    identical=[p for p in passages[-1:] if locate(p["quote"],claim)]
    if len(identical)==1 and len(result)!=len(ROLES):
        parent=identical[0]
        occurrence=locate(parent["quote"],claim)
        for role,w in role_spans(evidence_link(parent,occurrence),generate).items():
            assertion=locate(claim,w["quote"])
            if assertion:
                result[role]=dict(assertion=assertion,evidence=w)
    supported=bool(identical) or contrast.choose(generate,ENTAIL,dict(claim=claim,sources=facts),VERDICTS)==0
    new_action = result.get("action",{}).get("evidence",{}).get("source_id") == passages[-1]["source_id"]
    return dict(accepted=supported and new_action and not missing and len(result)==len(ROLES),roles=result,
                unsupported=missing,whole_claim_supported=supported)


def citation_prefix_end(text):
    header = re.match(r"(?:this fixes|fix(?:es)?)\s+a\s+regression\b.{0,120}?\b[0-9a-f]{7,40}\s*\(", text, re.S | re.I)
    if not header:
        return 0
    depth = 1
    for pos in range(header.end(), len(text)):
        if text[pos] == "(":
            depth += 1
        elif text[pos] == ")":
            depth -= 1
            if depth == 0:
                separator = re.match(r"[:,]\s+", text[pos+1:])
                return pos + 1 + separator.end() if separator else 0
    return 0


def core_passage(witness,context,generate):
    text=witness["quote"]
    # Strip attribution headers only at an explicit grammatical boundary. The ID
    # remains available in the upstream attribution witness.
    start = citation_prefix_end(text)
    # Short witnesses fit intact. Losing a neighboring sentence can remove the
    # antecedent of a pronoun or the precondition of the observed failure.
    if len(text)-start<=640:
        return evidence_link(witness,dict(start=start,end=len(text),quote=text[start:]))
    sentences=list(re.finditer(r"\S.*?(?:[.!?](?=\s+[A-Z\x60])|\Z)",text[start:],re.S))
    options=[]
    for i,m in enumerate(sentences[:5]):
        if not m.group().strip():continue
        # Keep an adjacent result with its premise; do not split off negation or a
        # subordinate clause and do not combine fragments across source boundaries.
        end=sentences[i+1].end() if i+1<len(sentences) else m.end()
        options.append(evidence_link(witness,dict(start=start+m.start(),end=start+end,quote=text[start+m.start():start+end])))
    if not options:return witness
    selected=contrast.choose(generate,FOCUS,context,[clean(p["quote"]) for p in options])
    return options[selected]


def role_spans(observation,generate):
    bound = bind(observation["quote"])
    if bound:
        return {role: evidence_link(observation, match) for role, match in bound.items()}
    spans={}
    for role in ROLES:
        prompt="Observation: "+clean(observation["quote"])+"\nQuestion: "+ROLE_QUESTIONS[role]+"\nExact substring:"
        raw=generate(EXTRACT,prompt).strip()
        match=locate(observation["quote"],raw)
        if not match and raw.endswith("."):
            match=locate(observation["quote"],raw[:-1])
        if match:
            spans[role]=evidence_link(observation,match)
    if len({(w["start"], w["end"]) for w in spans.values()}) != len(spans):
        return {}
    return spans


def revise(result,generate):
    if result.get("action") not in ("reassess","retest"):return result
    past,new=result["previous"],result["incoming"]
    checked=audit(result["rationale"],[past,new],generate)
    # An accepted paraphrase can be published with its complete ledger. If it lacks
    # a valid mapping, construct the factual part from one contiguous source excerpt.
    if checked["accepted"]:
        rationale=result["rationale"];ledger=checked["roles"];mode="verified"
    else:
        observation=core_passage(new,dict(prior=clean(past["quote"])),generate)
        roles=role_spans(observation,generate)
        if set(roles)!=set(ROLES):
            return dict(action="keep",basis="incomplete role evidence for the reported change")
        prior=core_passage(past,dict(report=clean(observation["quote"])),generate)
        prefix="Revisit the earlier decision reported as “"+clean(prior["quote"])+"”. The incoming evidence gives the reason. "
        rationale=prefix+observation["quote"]
        ledger={k:dict(evidence=w,assertion=dict(start=len(prefix)+w["start"]-observation["start"],
                     end=len(prefix)+w["end"]-observation["start"],quote=w["quote"])) for k,w in roles.items()}
        mode="source-bound"
    answer=dict(result,rationale=rationale,role_evidence=ledger,explanation_mode=mode)
    # Ground the contrast in its own record; never allow an unrelated claim about
    # the report to be attributed to the alternative's owner.
    if "alternative" in answer:
        other=core_passage(answer["alternative"],dict(report=clean(new["quote"])),generate)
        relevant=core_passage(new,dict(alternative=clean(other["quote"])),generate)
        answer["distinction"]="The alternative addresses “"+clean(other["quote"])+"”, while the new report concerns “"+clean(relevant["quote"])+"”."
    return answer


def assess(previous,sid,incoming,goal,generate):
    return revise(referenced_review.assess(previous,sid,incoming,goal,generate),generate)


def valid_ledger(item):
    ledger=item.get("role_evidence")
    if not isinstance(ledger,dict) or set(ledger)!=set(ROLES):return False
    if not isinstance(item.get("rationale"),str):return False
    for link in ledger.values():
        if not isinstance(link,dict):return False
        a=link.get("assertion");e=link.get("evidence")
        if not isinstance(a,dict) or not isinstance(e,dict):return False
        if not all(type(v.get(k)) is int for v in (a,e) for k in ("start","end")):return False
        if not 0<=a["start"]<a["end"]<=len(item["rationale"]) or item["rationale"][a["start"]:a["end"]]!=a.get("quote"):return False
        parents=(item["previous"],item["incoming"])
        if not any(e.get("source_id")==p["source_id"] and e.get("location")==p["location"] and e.get("speaker")==p["speaker"]
                   and p["start"]<=e["start"]<e["end"]<=p["end"] and
                   p["quote"][e["start"]-p["start"]:e["end"]-p["start"]]==e.get("quote") for p in parents):return False
    return True
