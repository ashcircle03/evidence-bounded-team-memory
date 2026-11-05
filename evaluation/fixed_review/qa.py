"""Independent original-batch QA generations and live-proposal/control replays."""
from pathlib import Path
import json
from hashlib import sha256
import sys
import tempfile

from evaluation.decision_records.build import read,save
from evaluation.pair_selection.batch_replay import recover
from evaluation.pair_selection.qa import packets, JOBS
from evaluation.pair_selection.qa_replay import historical
from team_memory.store import Store, capture
from team_memory.evidence import ask, active_sources
from .diagnose import OUT,HERE


def build():
    rows=[x for x in recover() if JOBS[x["id"].split("/")[1]][1] is not None]
    live=read(OUT/"comparison.json")
    for c in read(HERE/"inputs.json"):
        cid=c["id"]
        if cid not in live["qa"]:continue
        with tempfile.TemporaryDirectory() as tmp:
            store=Store(Path(tmp))
            for e in c["prior"]+[c["incoming"]]:capture(store,e)
            for arm in ("control","pulled"):
                q=live["qa"][cid]["question"]
                def reader(system,content):
                    sig=sha256((system+"\n"+content).encode()).hexdigest()
                    assert sig in live["qa_calls"]
                    uid=f"probe/{cid}/{arm}"
                    rows.append(dict(id=uid,system=system,content=content,sha256=sig,layout=uid,slot=0,
                                     max_output_tokens=64))
                    return live["qa_calls"][sig]["value"]
                result=ask(active_sources(store),q,reader,"simple")
                assert result==live["qa"][cid]["baseline" if arm=="control" else "candidate"]
    from .diagnose import diagnostics
    for packet in diagnostics():
        uid="explanation-control/"+packet["id"]
        rows.append(dict(packet,id=uid,layout=uid,slot=0))
    return rows


def score():
    log=read(OUT/"qa-generations.json")
    shots={r["id"]:r for r in log["calls"]}
    _,ref=packets()
    hist=historical(ref,shots)
    save(OUT/"qa-historical.json",hist)
    save(OUT/"explanation-singletons.json",{k:v for k,v in shots.items() if k.startswith("explanation-control/")})
    original=read(OUT/"comparison.json")
    outcome={}
    for c in read(HERE/"inputs.json"):
        cid=c["id"]
        if cid not in original["qa"]:continue
        with tempfile.TemporaryDirectory() as tmp:
            store=Store(Path(tmp))
            for env in c["prior"]+[c["incoming"]]:capture(store,env)
            q=original["qa"][cid]["question"];res={}
            for arm in ("control","pulled"):
                def reader(s,x):
                    r=shots["probe/"+cid+"/"+arm]
                    assert sha256((s+"\n"+x).encode()).hexdigest()==r["sha256"]
                    return r["raw"]
                res[arm]=ask(active_sources(store),q,reader,"simple")
            res["question"]=q;res["context"]=original["qa"][cid]["context"]
            outcome[cid]=res
    save(OUT/"qa-probes.json",outcome)
    print("Historical complete matches",sum(v["identical"] for v in hist.values()),len(hist))


if __name__=="__main__":
    if len(sys.argv)>1:save(Path(sys.argv[1]),build())
    else:score()
