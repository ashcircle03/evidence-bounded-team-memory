"""Previously passed two-sided QA, frozen separately before its own predictions."""
from pathlib import Path
import json
from evaluation.decision_records.build import ROOT,HERE,GIT,read,save
from evaluation.decision_records.packets import judgments,packet
from evaluation.revision.build_final import build as old_build

SYS = """Answer the question from the supplied raw passages. When different sources disagree about the same fact, report both claims and say the disagreement is unresolved. When conditions explain different answers, connect each answer to its condition. Give the short answer and supporting raw passage ID for each claim. Notes can help interpret the sources. Write JSON with keys status and answers, where answers is a list of objects with keys value, condition and source."""

def recover(data):
    corpus,keys=old_build(GIT); ds=corpus["documents"]
    prev=read(ROOT/"results/revision/scored.json")["decisions"]
    pilot=read(ROOT/"evaluation/team_pilot/cases.json")["qa"]
    prior=read(ROOT/"results/revision/regression-outcomes.json")
    out=[]
    for cid,base in [("d01","q01"),("d07","q02"),("pep-572-conflict","pep-572"),("pep-618-conflict","pep-618")]:
        prototype=next(c for c in data["cases"] if c["id"]==base)
        if cid.startswith("d"):
            assert prev[cid+"/premise"]["correct"]
            case=next(c for c in corpus["cases"] if c["id"]==cid)
            sides=keys[cid]["sides"]; keys_by_loc={e["source"]["location"]:e["source"] for e in ds.values()}
            raw=[keys_by_loc[s["location"]] for s in sides]
            question=case["question"];status="conditional" if cid=="d07" else "unresolved"
        else:
            n=int(cid.split("-")[1]);key=next(c for c in pilot if c["pep"]==n)
            question=key["question"]; status="unresolved"
            previous=next(r["result"] for r in prior if r["id"]=="old-"+cid+"/premise")
            assert previous["status"]=="unresolved" and len(previous["answers"])==2
            counter=next(a for a in previous["answers"] if a["location"].startswith("casebook://"))
            reference=next(x for x in prototype["raw"] if x["location"] in prototype["correct_locations"])
            raw=[reference,{"location":counter["location"],"text":key["counter"],"speaker":counter["speaker"]}]
            sides=[dict(location=reference["location"],aliases=key["answers"],condition=None),dict(location=counter["location"],aliases=key["other"],condition=None)]
        if len(out)%2:raw=raw[::-1]
        out.append(dict(id=cid,task="qa",group="prior_multisource",question=question,raw=raw,
                        incoming=prototype["incoming"],topics=prototype["topics"],
                        sides=sides,expected_status=status,previously_correct=True))
    return {"notes":data["notes"],"cases":out}

def inputs(d,writer):
    out=[]
    for p in judgments(d,writer):
        out.append(packet(p["id"], SYS, json.loads(p["content"]),160))
    return out

if __name__=="__main__":
    d=recover(read(HERE/"frozen.json"));save(HERE/"multisource.json",d)
    save(Path("/private/tmp/dr-multi-qa.json"),inputs(d,read(ROOT/"results/decision_records/writer.json")))
