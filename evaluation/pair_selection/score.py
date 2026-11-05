"""Validate both offsets and separately score order stability, target identity and evidence."""
from hashlib import sha256
import json
from evaluation.decision_records.build import read,save
from evaluation.decision_records.packets import passages,assemble
from evaluation.pair_selection.trial import HERE,RESULT,joint

def label(old,citation):
    for k,p in old.items():
        if p["location"]==citation["location"] and citation["quote"] and citation["quote"] in p["text"]:
            return k
    raise ValueError("Citation does not resolve to a raw paragraph")

def assess(data):
    joint_calls=read(RESULT/"joint.json")["calls"]
    hashes={p["id"]:p["sha256"] for p in joint(data)}
    assert len(joint_calls)==len(hashes) and all(x["sha256"]==hashes[x["id"]] for x in joint_calls)
    baseline={p["id"]:json.loads(p["raw"]) for p in joint_calls}
    newer=read(RESULT/"pairwise.json")
    keys=read(HERE/"key.json");blind={};table={}
    assert set(keys)=={c["id"] for c in data["cases"] if c["action"]=="review"}
    for c in data["cases"]:
        old,new,_=assemble(c,data);cid=c["id"]
        target=passages(data["notes"][c["target"]]["raw"],"T")
        target_locs={p["location"] for p in target.values()};positive=c["action"]=="review"
        gold_old,gold_new=keys.get(cid,([],[]))
        assert all("T."+v in target for v in gold_old) and all(f"N.1.{v}" in new for v in gold_new)
        for ordering in ("forward","reverse"):
            tag=cid+"/"+ordering
            for method in ("joint","pairwise"):
                if method=="joint":
                    o=baseline[tag]; a,b=o["old"],o["new"];act=o["action"];reason=o["reason"]
                else:
                    o=newer[tag]
                    a,b=label(old,o["chosen_old"]),label(new,o["chosen_new"])
                    r=o["result"]; act={"reassess":"review","retest":"review"}.get(r["action"],r["action"])
                    reason=r.get("rationale",r.get("basis",""))
                prior,later=old[a],new[b]
                target_ok=prior["location"] in target_locs
                old_ok=any(prior==target["T."+v] for v in gold_old)
                new_ok=int(b.split(".")[-1]) in gold_new
                eligible=positive and act=="review" and old_ok and new_ok
                h=None
                if eligible:
                    card=dict(case=cid,criterion=c["rubric"],old=prior["text"],new=later["text"],reason=reason)
                    h=sha256(json.dumps(card,sort_keys=True).encode()).hexdigest()[:12];blind[h]=card
                table[f"{tag}/{method}"]=dict(case=cid,group=c["group"],method=method,order=ordering,
                     expected=c["action"],action=act,old_id=a,new_id=b,old=prior,new=later,
                     reason=reason,target_ok=target_ok,old_ok=old_ok,new_ok=new_ok,pair_ok=old_ok and new_ok,card=h)
    return table,blind

def summarize(rows,ratings):
    summary={}
    for method in ("joint","pairwise"):
        for group in sorted({r["group"] for r in rows.values()}):
            subset=[r for r in rows.values() if r["method"]==method and r["group"]==group and r["order"]=="forward"]
            res={k:[] for k in ("pos","neg","forward_hit","both_hit","stable","stable_target_positive","both_pairs","both_target","false_positive","false_positive_reverse","action_hit","action_hit_reverse")}
            for r in subset:
                cid=r["case"];s=rows[f"{cid}/reverse/{method}"];pos=r["expected"]=="review"
                res["pos" if pos else "neg"].append(cid)
                stable=(r["action"],r["old_id"],r["new_id"])==(s["action"],s["old_id"],s["new_id"])
                if stable:res["stable"].append(cid)
                if pos:
                    if r["action"]=="review":res["action_hit"].append(cid)
                    if s["action"]=="review":res["action_hit_reverse"].append(cid)
                    if r["target_ok"] and s["target_ok"]:res["both_target"].append(cid)
                    if stable and r["target_ok"]:res["stable_target_positive"].append(cid)
                    if r["pair_ok"] and s["pair_ok"] and stable:res["both_pairs"].append(cid)
                    if r["grounded"]:res["forward_hit"].append(cid)
                    if r["grounded"] and s["grounded"] and stable:res["both_hit"].append(cid)
                else:
                    if r["action"]=="review":res["false_positive"].append(cid)
                    if s["action"]=="review":res["false_positive_reverse"].append(cid)
            summary[f"{group}/{method}"]=res
    return summary

if __name__=="__main__":
    table,cards=assess(read(HERE/"corpus.json"))
    save(RESULT/"blind-cards.json",dict(sorted(cards.items())))
    if (RESULT/"ratings.json").exists():
        ratings=read(RESULT/"ratings.json")
        assert set(cards)==set(ratings)
        for v in table.values():
            v["grounded"]=bool(v["card"] and ratings[v["card"]]["pass"])
        save(RESULT/"cases.json",table);save(RESULT/"counts.json",summarize(table,ratings))
