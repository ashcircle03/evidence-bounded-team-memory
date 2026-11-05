"""Reconstruct the original Qwen batch peers, row positions, caps and padding lengths."""
from itertools import groupby
from pathlib import Path
from .qa import CAMPAIGN,JOBS,packets
from .trial import RESULT
from .qa_replay import historical
from evaluation.decision_records.build import read,save


def recover():
    _,refs=packets();result=[]
    for version,(job,_) in JOBS.items():
        candidates=read(CAMPAIGN/"source"/version/"packets.json")
        old={r["id"]:r for r in read(CAMPAIGN/"results"/f"sm-{job}.json")["calls"]}
        def cap(p):return p.get("max_output_tokens",64 if version=="pull-pilot-v1" else 192)
        ordered=sorted(candidates,key=lambda p:(cap(p),old[p["id"]]["input_tokens"],p["id"]))
        for lim,group in groupby(ordered,key=cap):
            same=list(group)
            for i in range(0,len(same),4):
                block=same[i:i+4];prefix="qa/"+version+"/"
                if not any(prefix+p["id"] in refs for p in block):continue
                for slot,p in enumerate(block):
                    row=old[p["id"]]
                    assert row["sha256"]==p["sha256"]
                    result.append(dict(p,id=prefix+p["id"],group=prefix+p.get("group",p["id"]),layout=f"{version}/{lim}/{i}",
                                       slot=slot,max_output_tokens=lim,archived_input_tokens=row["input_tokens"]))
    return result

def check():
    _,refs=packets();log=read(RESULT/"qa-original-batches.json")
    shots={r["id"]:r for r in log["calls"]};r=historical(refs,shots)
    save(RESULT/"qa-matched-historical.json",r)
    drift={}
    for uid,v in refs.items():
        now=shots[uid];before=v["original"]
        assert now["sha256"]==before["sha256"] and now["input_tokens"]==before["input_tokens"]
        if before["raw"]!=now["raw"]:
            drift[uid]=dict(before=before["raw"],after=now["raw"])
    save(RESULT/"qa-matched-raw-differences.json",drift)
    print("historical differences",[k for k,v in r.items() if not v["identical"]],"raw differences",list(drift))

if __name__=="__main__":
    import sys
    if len(sys.argv)>1:check()
    else:save(Path("/private/tmp/pair-original-batches.json"),recover())
