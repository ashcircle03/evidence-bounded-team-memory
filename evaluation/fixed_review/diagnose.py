"""Separate gate order sensitivity from the explanation when a review is forced."""
import json
from hashlib import sha256
from pathlib import Path

from team_memory.pair_selection import DOCUMENT, SUPPORT, REASON, payload
from team_memory.sync import DEFAULT_GOAL
from evaluation.decision_records.build import read, save, ROOT, WORK
from evaluation.pair_selection.field_order import changed

HERE = Path(__file__).resolve().parent
OUT = ROOT / "results/fixed_review"
LAST = ROOT / "results/pair_selection"


def diagnostics():
    reviews=read(LAST/"cases.json")
    old_inputs=read(WORK/"campaigns/speakermem-dev/source/records-read-v13/packets.json")
    results={r["id"]:r for r in read(LAST/"field-margins.json")["calls"]}
    traces={}; requests=[]
    for cid in ("unseen-1p","unseen-2p","unseen-3p","unseen-4p"):
        r=reviews[cid+"/forward/pairwise"]
        old,new=r["old"]["text"],r["new"]["text"]
        traces[cid]={}
        # The document gate uses the entire document summaries; identify the current source
        # by matching its exact old paragraph and its associated SUPPORT block.
        for arm in ("earlier-first","report-first"):
            doc=None
            for pkt in old_inputs:
                if not pkt["id"].startswith(arm+"/"+cid+"/forward/"):continue
                if pkt["system"]==DOCUMENT:doc=pkt
                elif pkt["system"]==SUPPORT and json.loads(pkt["content"])==json.loads(payload(DEFAULT_GOAL,old,new)):
                    assert old in json.loads(doc["content"])["earlier"]
                    for p in (doc,pkt):assert results[p["id"]]["sha256"]==p["sha256"]
                    traces[cid][arm]=dict(document=results[doc["id"]]["margin"],support=results[pkt["id"]]["margin"])
                    break
            assert arm in traces[cid]
        variants={"intact":new}
        if cid=="unseen-2p":
            i=new.index("As the new test");j=new.index("This fixes")
            variants.update(no_cost=new[:i].strip()+" "+new[j:],no_exception=new[i:],cost_first=new[i:j]+new[:i]+new[j:])
        for name,txt in variants.items():
            for arm in ("earlier-first","report-first"):
                content=changed(payload(DEFAULT_GOAL,old,txt),arm=="report-first")
                req=dict(id=f"{cid}/{name}/{arm}",system=REASON,content=content,max_output_tokens=96)
                req["sha256"]=sha256((REASON+"\n"+content).encode()).hexdigest()
                requests.append(req)
    save(OUT/"gate-diagnosis.json",traces)
    return requests


if __name__=="__main__":save(Path("/private/tmp/fixed-diagnosis.json"),diagnostics())
