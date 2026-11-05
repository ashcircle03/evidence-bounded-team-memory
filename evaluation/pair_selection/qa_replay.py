"""Run archived Qwen generations back through the actual QA readers and citation resolvers."""
import json
from evaluation.decision_records.build import ROOT,WORK,GIT,read,save
from evaluation.revision.build_final import build as git_cases
from evaluation.revision.regression import build as regression
from evaluation.revision.run import build as run
from evaluation.team_pilot.pilot import bundle, dev_sources, pep_sources, call_hash
from team_memory.evidence import ask
from .qa import JOBS,FINAL,EVER,packets
from .trial import RESULT

PEPS=WORK/".work/peps-external.git"
STORE=WORK/".work/speaker-run/paired-snapshot"

def historical(ref,rerun):
    finals,_=git_cases(GIT)
    old=regression(PEPS,STORE)
    sources=dev_sources(STORE);dev_docs={k:env for k,(env,_) in sources.items()}
    qs=read(ROOT/"evaluation/revision/development/ever-questions.json")["answers"]
    dev=dict(documents=dev_docs,cases=[dict(id=q["id"],task="qa",question=q["question"],as_of="2025-02-01T00:00:00Z",history=list(dev_docs)) for q in qs])
    def get(uid,original):
        p=ref[uid]["original"] if original else rerun[uid]
        assert p["sha256"]==ref[uid]["original"]["sha256"]
        return dict(p,id=uid.split("/",2)[-1])
    rows={}
    for (ver,names) in [("revision-final-v1",FINAL),("revision-dev-v3",EVER)]:
        for group in names:
            cid,arm=group.split("/")
            ds=dev if ver=="revision-dev-v3" else old if cid.startswith("old-") else finals
            case=next(c for c in ds["cases"] if c["id"]==cid)
            full=dict(documents=ds["documents"],cases=[dict(case,arms=[arm])])
            ids=[k for k,v in ref.items() if v["version"]==ver and v["group"]==group]
            pair=[]
            for orig in (True,False):
                _,out=run(full,{"calls":[get(k,orig) for k in ids]})
                pair.append(out[0]["result"])
            rows[group]=dict(question=case["question"],before=pair[0],after=pair[1],identical=pair[0]==pair[1])
    uid="qa/pull-pilot-v1/pep-680/clean/candidate"
    docs=bundle(list(pep_sources(PEPS).values()))
    question=next(q["question"] for q in read(ROOT/"evaluation/team_pilot/cases.json")["qa"] if q["pep"]==680)
    out=[]
    for orig in (True,False):
        row=get(uid,orig)
        def generate(s,x):
            assert call_hash(s,x)==row["sha256"];return row["raw"]
        out.append(ask(docs,question,generate,"candidate"))
    rows["pep-680/clean/candidate"]=dict(question=question,before=out[0],after=out[1],identical=out[0]==out[1])
    return rows

def evaluate():
    _,ref=packets(); after={r["id"]:r for r in read(RESULT/"generations.json")["calls"] if r["id"].startswith("qa/")}
    assert set(after)==set(ref)
    historical_rows=historical(ref,after)
    same_inbox={}
    for uid,v in ref.items():
        if JOBS[v["version"]][1] is not None:continue
        before=v["original"];now=after[uid]
        assert before["sha256"]==now["sha256"]
        same_inbox[uid]=dict(identical=before["raw"]==now["raw"],before=before["raw"],after=now["raw"])
    save(RESULT/"qa-historical.json",historical_rows)
    save(RESULT/"qa-same-inbox.json",same_inbox)
    print("historical differences",[k for k,v in historical_rows.items() if not v["identical"]])
    print("same-inbox differences",[k for k,v in same_inbox.items() if not v["identical"]])

if __name__=="__main__":evaluate()
