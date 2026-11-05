"""Run the production selector with recorded model scores or prepare its complete calls."""
import json
from hashlib import sha256
from pathlib import Path
from evaluation.decision_records.build import read,save
from evaluation.decision_records.packets import assemble,display,packet
from evaluation.decision_records.followup import INSTRUCTION
from team_memory.pair_selection import select, assess
from team_memory.store import digest,source_envelope
from team_memory.sync import DEFAULT_GOAL

HERE=Path(__file__).resolve().parent
RESULT=HERE.parents[1]/"results/pair_selection"

def envelope(raw):
    return source_envelope(dict(owner=raw["author"],observed_at=raw["time"],source=dict(location=raw["location"],speaker=raw["author"],text=raw["text"])))

def streams(data):
    for c in data["cases"]:
        for order in ("forward","reverse"):
            docs=[envelope(doc) for topic in c["topics"] for doc in data["notes"][topic]["raw"]]
            if order=="reverse":
                docs.reverse()
            yield c,order,{digest(e):(e,"source_only") for e in docs},envelope(c["incoming"])

def joint(data):
    out=[]
    for c,order,_,_ in streams(data):
        old,new,_=assemble(c,data)
        if order=="reverse":
            # Preserve evidence identifiers while reversing complete documents; paragraphs retain chronology.
            docids=list(dict.fromkeys(k.rsplit(".",1)[0] for k in old))
            old={k:v for docid in reversed(docids) for k,v in old.items() if k.rsplit(".",1)[0]==docid}
        payload=dict(old=display(old),incoming=display(new),notes=[])
        p=packet(c["id"]+"/"+order,INSTRUCTION,payload,160)
        p["choices"]=[["review","keep"],list(old),list(new)]
        out.append(p)
    return out

def scores_and_reasons(data, measured=None, generated=None):
    recorded={x["id"]:x for x in measured["calls"]} if measured else {}
    reasons={x["id"]:x for x in generated["calls"]} if generated else {}
    requests=[]; outputs={}
    for c,order,history,incoming in streams(data):
        name=c["id"]+"/"+order; counter=0; sid=digest(incoming)
        def call(instruction,content,is_reason=False):
            nonlocal counter
            sig=sha256((instruction+"\n"+content).encode()).hexdigest()
            if is_reason:
                key=name+"/reason"
            else:
                counter+=1
                key=name+"/"+str(counter)
            pkt=dict(id=key,sha256=sig,system=instruction,content=content,max_output_tokens=96 if is_reason else 1)
            if is_reason or not measured: requests.append(pkt)
            known=reasons if is_reason else recorded
            if (generated if is_reason else measured) is not None:
                assert known[key]["sha256"]==sig
                return known[key]["raw"] if is_reason else known[key]["margin"]
            return "pending" if is_reason else 0.0
        margin=lambda s,x:call(s,x)
        if measured is None:
            select(history,sid,incoming,DEFAULT_GOAL,margin)
            continue
        # select() and assess() are the ordinary pull implementation, not a scoring-only branch.
        def explain(s,x):return call(s,x,True)
        explain.evidence_margin=margin
        result=assess(history,sid,incoming,DEFAULT_GOAL,explain)
        counter=0
        best=select(history,sid,incoming,DEFAULT_GOAL,margin)
        assert best
        outputs[name]=dict(result=result,chosen_old=best.old.cite(),chosen_new=best.new.cite(),
                           document_margin=best.document_margin,support_margin=best.support_margin)
    return requests,outputs

if __name__=="__main__":
    import sys
    d=read(HERE/"corpus.json")
    if sys.argv[1]=="initial":
        save(Path("/private/tmp/pair-joint.json"),joint(d))
        save(Path("/private/tmp/pair-scores.json"),scores_and_reasons(d)[0])
    else:
        measured=read(RESULT/"margins.json")
        if sys.argv[1]=="reason":
            qs,rows=scores_and_reasons(d,measured)
            save(Path("/private/tmp/pair-reasons.json"),qs)
        else:
            qs,rows=scores_and_reasons(d,measured,read(RESULT/"generations.json"))
            save(RESULT/"pairwise.json",rows)
