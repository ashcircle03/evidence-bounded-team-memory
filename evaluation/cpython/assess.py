"""Score immutable external snapshots, optionally replay every real Qwen call against its hash."""
import argparse
import gzip
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from probe import run
from team_memory.store import source_envelope

HERE=Path(__file__).resolve().parent
def sha(b):
    return hashlib.sha256(b).hexdigest()

def grade_reader(reader,key,source):
    value = reader.get("answer","")
    return (reader.get("location")==source["location"] and reader.get("field")=="quote"
            and reader.get("quote")==source["text"] and bool(value)
            and value in source["text"] and bool(re.search(key["match"],value,re.I|re.S)))

def evaluate(ranks, result=None):
    freeze=json.loads((HERE/"freeze.json").read_text())
    for file,h in freeze["sha256"].items():
        assert sha((HERE/file).read_bytes())==h
    keys=json.loads((HERE/"key.json").read_text())
    packets=json.loads(gzip.decompress((HERE/"packets.json.gz").read_bytes()))
    snapshots=json.loads(gzip.decompress((HERE/"inputs.json.gz").read_bytes()))
    report={"independent_labels":False,"retrieval":[],"goals":[],"qa":[],"gpu":None}
    outputs={}
    if result:
        assert result["status"]=="complete" and len(result["rows"])==24
        assert result["packets_sha256"]==sha((HERE/"packets.json.gz").read_bytes())
        assert result["device"].startswith("cuda") and result["dtype"]=="torch.bfloat16"
        calls=iter(result["calls"]);replayed=[]
        def replay(kind):
            def read(system,content):
                row=next(calls)
                assert row["kind"]==kind and sha((system+"\n"+content).encode())==row["sha256"]
                assert row["tokens"]<=8192
                return row["output"]
            return read
        run(packets,replay("choice"),replay("qa"),replayed.append)
        assert replayed==result["rows"] and next(calls,None) is None
        outputs={(r["event"],r.get("goal",r.get("kind")),r.get("phase",r.get("arm"))):r for r in replayed}
        assert len(outputs)==24
        report["gpu"]={k:result[k] for k in ("job_id","model","revision","device","dtype")}
        report["gpu"]["verified_calls"]=len(result["calls"])
        # Action calls for each goal are physically emitted direct / recheck / masked / revealed.
        # The 2-pass plain comparator includes the initial direct read.
        action_calls=[r for r in result["calls"] if r["kind"]=="choice"]
        assert len(action_calls)==20
        report["gpu"]["action_input_tokens"]={arm:sum(r["tokens"] for i,r in enumerate(action_calls) if i%4 in slots)
                                                for arm,slots in (("direct",[0]),("checked",[0,1]),("module",[2,3]))}
    for s,p in zip(snapshots,packets):
        id_=s["id"];assert id_==p["id"]
        k=keys[id_];target=str(k["target"])
        old=s["history"][target]["source"]
        pool=ranks[id_]
        metrics={"event":id_,"n":pool["documents"],"target":target,"target_link":old["location"],"incoming":s["incoming"]["source"]["location"]}
        for stage in ("raw","masked"):
            r=pool[stage];simple=r["plain_rank"]
            metrics[stage]={"plain":simple[0],"plain_gold_rank":simple.index(target)+1 if target in simple else None,
                            "module":r["module_top1"]}
        metrics["module_decision_quote"]=p["module"]["decision"]["quote"] if p["module"] else None
        metrics["module_reason_quote"]=(p["module"].get("reason") or {}).get("quote") if p["module"] else None
        report["retrieval"].append(metrics)
        for g,goal in p["goals"]:
            expected=k["actions"][g]
            item={"event":id_,"goal":g,"expected":expected,"predictions":None}
            if result:
                preds={}
                for arm in ("direct","checked","module"):
                    row=outputs[id_,g,arm];v=row["action"]
                    v={"compare":"request_comparison","ongoing":"attach_to_existing","unclear":"needs_context","blocked":"retain_constraint"}.get(v,v)
                    selected=metrics["raw"]["module" if arm=="module" else "plain"]
                    preds[arm]={"selected":selected,"action":v,"action_ok":v in expected,
                                "joint":v in expected and selected==target,
                                "strict_joint":v in (["request_comparison"] if g=="opt_in" else expected) and selected==target}
                item["predictions"]=preds
            report["goals"].append(item)
        for q in p["qa"]:
            qk=k["qa"][q["kind"]];n=str(qk["pep"]);env=s["incoming"] if int(n)==s["pep"] else s["history"][n]
            src=source_envelope(env)["source"]
            item={"event":id_,"kind":q["kind"],"phase":q["phase"],"question":q["question"],
                  "target":n,"source_in_top3":n in q["selected"],"source_contains_gold":bool(re.search(qk["match"],src["text"],re.I|re.S)),
                  "model_ok":None}
            if result:
                rr=outputs[id_,q["kind"],q["phase"]]["reader"]
                item.update(model_ok=grade_reader(rr,qk,src),answer=rr.get("answer",rr.get("status")),citation=rr.get("location"))
            report["qa"].append(item)
    if result:
        report["joint_hits"]={a:sum(g["predictions"][a]["joint"] for g in report["goals"]) for a in ("direct","checked","module")}
    return report

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("ranks",type=Path);ap.add_argument("output",type=Path);ap.add_argument("--run",type=Path)
    a=ap.parse_args()
    report=evaluate(json.loads(a.ranks.read_text()),json.loads(a.run.read_text()) if a.run else None)
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
