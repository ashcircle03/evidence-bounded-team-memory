"""Create method-masked rationale cards and score released judgments separately from oracle pairs."""
from hashlib import sha256
import json
from .diagnose import HERE,OUT
from evaluation.decision_records.build import read,save


def prepare():
    result=read(OUT/"comparison.json")
    annotations=read(HERE/"key.json")
    inputs={c["id"]:c for c in read(HERE/"inputs.json")}
    cards={}; rows={}
    for cid,data in result["rows"].items():
        expected=annotations[cid]
        case=inputs[cid]
        for regime,group in data.items():
            for mode,methods in group.items():
                actual=methods if regime=="fixed" else {mode:methods}
                for method,v in actual.items():
                    rowid="/".join((cid,regime,mode,method))
                    if regime=="fixed":
                        action=(v if method=="original" else v["result"])["action"]
                        reason=v["forced_reason"]
                        a,b=case["fixed_old"],case["fixed_new"]
                    else:
                        action=v["action"];reason=v.get("rationale","")
                        a,b=v.get("previous",{}),v.get("incoming",{})
                    authorized=lambda w,typ,source:w.get("location")==expected[source] and w.get("quote") in expected.get(typ,[])
                    correct_pair=(expected["label"]=="pos" and authorized(a,"allowed_old","previous") and authorized(b,"allowed_new","incoming"))
                    hid=None
                    if reason and expected["label"]=="pos":
                        card=dict(criterion=expected["rubric"],earlier=a.get("quote",""),incoming=b.get("quote",""),reason=reason)
                        hid=sha256(json.dumps(card,sort_keys=True).encode()).hexdigest()[:12]
                        cards[hid]=card
                    rows[rowid]=dict(case=cid,regime=regime,mode=mode,method=method,label=expected["label"],action=action,
                                     correct_pair=correct_pair,card=hid,reason=reason,old=a,new=b)
    return rows,cards


def margins():
    from team_memory.fixed_review import fields, relation, CHANGE, SEPARATE, FOCUS
    from team_memory.sync import DEFAULT_GOAL
    from .focus_control import build as focus_probes
    calls=read(OUT/"comparison.json")
    key=read(HERE/"key.json")
    def lookup(s,x):
        h=sha256((s+"\n"+x).encode()).hexdigest()
        return calls["calls"][h]["value"]
    stages={}
    for c in read(HERE/"inputs.json"):
        cid=c["id"];a=c["fixed_old"]["quote"];b=c["fixed_new"]["quote"]
        layers={}
        for flip,tag in ((False,"earlier-first"),(True,"report-first")):
            x=fields(DEFAULT_GOAL,a,b,flip);yes=lookup(CHANGE,x);no=lookup(SEPARATE,x)
            layers[tag]=dict(change=yes,independent=no,contrast=yes-no)
        row=dict(margin=relation(a,b,DEFAULT_GOAL,lookup),by_order=layers)
        if key[cid]["label"]=="pos":
            result=calls["rows"][cid]["end_to_end"]["fixed-review"]
            old,new=result.get("previous",{}),result.get("incoming",{})
            doc_ok=old.get("location")==key[cid]["previous"]
            row["selected"]=dict(correct_old_document=doc_ok,
                old_ok=doc_ok and old.get("quote") in key[cid]["allowed_old"],
                new_ok=new.get("location")==key[cid]["incoming"] and new.get("quote") in key[cid]["allowed_new"],
                earlier=old.get("quote"),incoming=new.get("quote"))
        stages[cid]=row
    focus=[]
    for p in focus_probes():
        x=json.loads(p["content"]);sentence=x["selected_report_sentence"]
        if sentence:focus.append([lookup(FOCUS,fields(DEFAULT_GOAL,x["earlier"],sentence)),sentence])
    return dict(cases=stages,checkout_focus=focus)


def finish():
    rows,cards=prepare()
    save(OUT/"stage-scores.json",margins())
    save(OUT/"blind-cards.json",dict(sorted(cards.items())))
    if not (OUT/"ratings.json").exists():return
    ratings=read(OUT/"ratings.json")
    assert set(ratings)==set(cards)
    for row in rows.values():
        row["correct_reason"]=bool(row["card"] and ratings[row["card"]]["ok"])
        row["grounded"]=row["action"]=="reassess" and row["correct_pair"] and row["correct_reason"]
    save(OUT/"cases.json",rows)
    sums={}
    for k,row in rows.items():
        c=row["case"];split="new" if c.startswith("git-") else "cross" if c.startswith("cross-") else "dev"
        arm=f"{split}/{row['regime']}/"+(row["mode"]+"/" if row["regime"]=="fixed" else "")+row["method"]
        agg=sums.setdefault(arm,{key:[] for key in ("positive","negative","requested","false_positive","correct_reason","grounded","correct_pair")})
        positive=row["label"]=="pos"
        agg["positive" if positive else "negative"].append(c)
        if row["action"]=="reassess":agg["requested" if positive else "false_positive"].append(c)
        for metric in ("correct_reason","grounded","correct_pair"):
            if row[metric]:agg[metric].append(c)
    save(OUT/"counts.json",sums)


if __name__=="__main__":finish()
