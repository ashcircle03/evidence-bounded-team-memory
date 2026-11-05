"""Resolve raw citations and create blinded semantic cards before counting accepted proposals."""
import json
from hashlib import sha256
from collections import defaultdict
from evaluation.decision_records.build import read,save
from .paths import HERE,OUT

REVIEW={"reassess","retest"}


def card(cards,kind,criterion,citations,answer):
    content=dict(task=kind,criterion=criterion,source=citations,answer=answer)
    h=sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()[:12]
    cards[h]=content
    return h


def matches(source,allowed,loc):
    return bool(source and source["location"]==loc and
                any(source["quote"].strip() and source["quote"] in text for text in allowed))


def collect(here=HERE,out=OUT):
    raw=read(out/"comparison.json");keys=read(here/"key.json")
    inputs={r["id"]:r for r in read(here/"inputs.json")}
    data={};cards={}
    for cid,methods in raw["results"].items():
        case=keys[cid];docs={d["source"]["location"]:d["source"] for d in inputs[cid]["prior"]+[inputs[cid]["incoming"]]}
        for name,record in methods.items():
            r=record["result"];a=r.get("previous");n=r.get("incoming");f=r.get("alternative")
            for w in (a,n,f,r.get("attribution")):
                if w:
                    s=docs[w["location"]]
                    assert s["text"][w["start"]:w["end"]]==w["quote"] and s["speaker"]==w["speaker"]
            target=bool(a and a["location"]==case["earlier"])
            pair=matches(a,case["old"],case["earlier"]) and matches(n,case["new"],case["report"])
            other=matches(f,case["foil"],case["alternative"])
            rid=did=None
            if pair and r.get("rationale"):
                rid=card(cards,"changed condition",case["rubric"],[a["quote"],n["quote"]],r["rationale"])
            if other and target and n and r.get("distinction"):
                did=card(cards,"difference from alternative",case["distinction"],[a["quote"],n["quote"],f["quote"]],r["distinction"])
            data[cid+"/"+name]=dict(cid=cid,topic=case["topic"],view=case["view"],scenario=case["scenario"],
                                     method=name,action=r["action"],opened=r["action"] in REVIEW,target=target,pair=pair,
                                     other=other,rationale_card=rid,distinction_card=did,result=r)
        for rev,normal in (("contrast-reversed","contrast-review"),("referenced-reversed","referenced-review")):
            if rev in methods:
                assert methods[rev]["result"]==methods[normal]["result"],cid
    if (out/"fixed-witnesses.json").exists():
        from .auxiliary import build
        fixed=read(out/"fixed-witnesses.json")["results"]
        for row in build():
            cid=row["id"];case=keys[cid];v=fixed[cid]
            opened=bool(v);target=opened and v["location"]==case["earlier"]
            rid=did=None
            r=dict(action="keep")
            if opened:
                prior,alt=sorted(row["earlier"],key=lambda x:x["location"]!=v["location"])
                r=dict(action="reassess",previous=dict(location=prior["location"],quote=prior["text"]),
                       alternative=dict(location=alt["location"],quote=alt["text"]),
                       incoming=dict(location=case["report"],quote=row["report"]),rationale=v["reason"],distinction=v["distinction"])
                if target:
                    rid=card(cards,"changed condition",case["rubric"],[prior["text"],row["report"]],v["reason"])
                    did=card(cards,"difference from alternative",case["distinction"],[prior["text"],row["report"],alt["text"]],v["distinction"])
                    assert prior["text"] in case["old"] and row["report"] in case["new"] and alt["text"] in case["foil"]
            data[cid+"/fixed-witnesses"]=dict(cid=cid,topic=case["topic"],view=case["view"],scenario=case["scenario"],
                method="fixed-witnesses",action=r["action"],opened=opened,target=target,pair=target,other=target,
                rationale_card=rid,distinction_card=did,result=r)
    return data,cards


def run(here=HERE,out=OUT):
    rows,cards=collect(here,out);save(out/"blind-cards.json",dict(sorted(cards.items())))
    if not (out/"ratings.json").exists():return
    rates=read(out/"ratings.json");assert set(rates)==set(cards)
    sums=defaultdict(lambda:defaultdict(list))
    for v in rows.values():
        ok=lambda name:bool(v[name] and rates[v[name]]["ok"])
        v["grounded"]=v["opened"] and v["pair"] and ok("rationale_card")
        v["contrast"]=v["grounded"] and v["other"] and ok("distinction_card")
        metrics=sums["/".join(v[k] for k in ("view","scenario","method"))]
        for k in ("opened","target","pair","other","grounded","contrast"):
            if v[k]:metrics[k].append(v["topic"])
        metrics["n"].append(v["topic"])
        if v["action"]=="keep":metrics["keep"].append(v["topic"])
        elif not v["opened"]:metrics["invalid"].append(v["topic"])
    save(out/"cases.json",rows);save(out/"counts.json",sums)


if __name__=="__main__":run()
