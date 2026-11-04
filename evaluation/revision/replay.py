"""Verify the frozen final and regression request streams and materialize human-readable traces."""
import argparse
import hashlib
import json
from pathlib import Path

from evaluation.revision.run import build, History
from evaluation.revision.score import norm
from evaluation.team_pilot.pilot import bundle, write
from team_memory.qa import answer


def qa_passages(packet, case, data):
    content=json.loads(packet["content"])
    if "evidence" in content:
        return [(e["source"],e["excerpt"]) for e in content["evidence"]]
    if "sources" in content:
        return [(src["source"],text) for src in content["sources"] for text in src["excerpts"].values()]
    if "messages" in content:
        source=bundle(data["documents"][k] for k in case["history"])
        refs=answer(History(source),case["question"])["citations"]
        return [(refs[msg["n"]-1]["location"]," ".join(msg["sentences"].values())) for msg in content["messages"]]
    return []


def verify(final, regression, recording, output):
    here=Path(__file__).resolve().parent
    freeze=json.loads((here/"freeze.json").read_text())
    keys=json.loads((here/"final-key.json").read_text())
    total=[]
    rows=[]
    coverage={}
    for tag,data in [("final",final),("regression",regression)]:
        generated=build(data)[0]
        names={p["id"] for p in generated}
        log=dict(recording,calls=[c for c in recording["calls"] if c["id"] in names])
        packets,outcomes=build(data,log)
        if packets!=generated:
            raise ValueError("unexpected adaptive final input")
        total.extend(packets)
        rows.extend(outcomes)
        write(output/(tag+"-outcomes.json"),outcomes)
        if tag=="final":
            cases={c["id"]:c for c in data["cases"]}
            for p in packets:
                cid,arm,_=p["id"].split("/")
                if "sides" not in keys[cid]:continue
                src=qa_passages(p,cases[cid],data)
                flags=coverage.setdefault(cid+"/"+arm,[False]*len(keys[cid]["sides"]))
                for i,side in enumerate(keys[cid]["sides"]):
                    flags[i] |= any(loc==side["location"] and any(norm(a) in norm(text) for a in side["aliases"])
                                    and (side["condition"] is None or norm(side["condition"]) in norm(text)) for loc,text in src)
    if {p["id"]:p["sha256"] for p in total}!=freeze["prompt_sha256"]:
        raise ValueError("frozen input hash mismatch")
    blob=(json.dumps(total,ensure_ascii=False,indent=2)+"\n").encode()
    if hashlib.sha256(blob).hexdigest()!=recording["input_sha256"] or recording["input_sha256"]!=freeze["packet_sha256"]:
        raise ValueError("recording or combined packet file differs from freeze")
    if len(set(c["id"] for c in recording["calls"]))!=len(total) or len(recording["calls"])!=len(total):
        raise ValueError("missing or duplicate predictions")
    write(output/"coverage.json",coverage)
    print(f"Replayed {len(total)} frozen calls; {len(rows)} item/arm outcomes.")
    return total,rows


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    for n in ("final","regression","recording","output"):ap.add_argument(n,type=Path)
    ap.add_argument("--show",help="show all system/user inputs, responses and citations for a case/arm ID")
    a=ap.parse_args()
    a.output.mkdir(exist_ok=True,parents=True)
    final,reg,log=(json.loads(p.read_text()) for p in (a.final,a.regression,a.recording))
    prompts,rows=verify(final,reg,log,a.output)
    if a.show:
        out=next(r for r in rows if r["id"]==a.show)
        index={c["id"]:c for c in log["calls"]}
        print(json.dumps(dict(outcome=out,trace=[dict(p,output=index[p["id"]]) for p in prompts if p["id"] in out["calls"]]),ensure_ascii=False,indent=2))
