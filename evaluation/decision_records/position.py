"""Cross displayed order with ID assignment, using archived A inputs without decision notes."""
from pathlib import Path
import json
from evaluation.decision_records.build import read, save
from evaluation.decision_records.packets import packet

CASES=("historical-01","historical-03","scope-01","fresh-05")
def cross(rows):
    out=[];mapping={}
    for cid in CASES:
        original=next(p for p in rows if p["id"]==cid+"/A")
        for reverse in (False,True):
            for rename in (False,True):
                p=json.loads(original["content"])
                groups=[[x for x in p["old"] if x["id"].startswith(f"O{i}.")] for i in (1,2)]
                if reverse:groups.reverse()
                p["old"]=[x for g in groups for x in g]
                orig={}
                for row in p["old"]:
                    old=row["id"]
                    if rename:row["id"]=("O2" if old.startswith("O1.") else "O1")+old[2:]
                    orig[row["id"]]=old
                uid=f"{cid}/{int(reverse)}{int(rename)}"
                q=packet(uid,original["system"],p,original["max_output_tokens"])
                q["choices"]=[["review","keep"],[x["id"] for x in p["old"]],[x["id"] for x in p["incoming"]]]
                mapping[uid]=dict(original=orig,first=p["old"][0]["id"].split(".")[0],reverse=reverse,rename=rename)
                out.append(q)
    return out,mapping

if __name__=="__main__":
    rows=read(Path("../campaigns/speakermem-dev/source/records-read-v2/packets.json"))
    req,mp=cross(rows)
    save(Path("/private/tmp/dr-position.json"),req)
    save(Path("results/decision_records/position-map.json"),mp)
