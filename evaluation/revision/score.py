"""Apply the pre-registered per-case key, with separately recorded semantic adjudications."""
from collections import defaultdict
import argparse
import hashlib
import json
from pathlib import Path
import re

from evaluation.team_pilot.pilot import write


def norm(text):
    return " ".join(text.casefold().replace("`","").split()).strip(" .'\"")


def actual(r):
    if "answers" in r:
        return r["answers"]
    if "location" in r and "answer" in r:
        return [r]
    return []


def check(key, r):
    if key["phase"] in ("positive","negative"):
        if r["action"] not in key["actions"]:
            return False
        if r["action"] == "keep":
            return True
        return (r["previous"]["location"] == key["prior"] and r["incoming"]["location"] == key["incoming"]
                and norm(key["old_cue"]) in norm(r["previous"]["quote"] + " " + r.get("prior_rationale",{}).get("quote",""))
                and norm(key["new_cue"]) in norm(r["incoming"]["quote"]))
    rows = actual(r)
    if len(rows) != len(key["sides"]):
        return False
    if key["phase"] == "disputed" and r.get("status") != "unresolved":
        return False
    for side in key["sides"]:
        match = [v for v in rows if v["location"] == side["location"]]
        if len(match) != 1:
            return False
        a = match[0]
        if norm(a["answer"]) not in set(map(norm, side["aliases"])):
            return False
        if side["condition"] and norm(side["condition"]) not in norm(a.get("condition","") + " " + a["answer"]):
            return False
    return True


def prepare(keys, rows):
    cards, links = {}, {}
    for row in rows:
        case, arm = row["id"].rsplit("/",1)
        result = row["result"]
        # Remove model / arm names and internal IDs, keep all evidence and the user-visible action.
        content = dict(case=case, key=keys[case], result=result)
        key = hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()[:16]
        cards[key] = dict(**content, exact=check(keys[case],result))
        links[row["id"]] = key
    return dict(sorted(cards.items())), links


def score(keys, rows, overrides):
    cards,links=prepare(keys,rows)
    if set(overrides)-set(cards):
        raise ValueError("unknown review card")
    detail={}
    counts=defaultdict(lambda:defaultdict(lambda:dict(total=0,correct=0,delivered=0,keep=0,invalid=0)))
    for name,key in links.items():
        card=cards[key]
        case,arm=name.rsplit("/",1)
        correct=overrides.get(key,{}).get("correct",card["exact"])
        action=card["result"].get("action")
        detail[name]=dict(card=key,correct=correct,exact=card["exact"])
        for group in (keys[case]["phase"], keys[case]["phase"]+"/"+keys[case]["origin"]):
            c=counts[group][arm]; c["total"]+=1;c["correct"]+=int(correct)
            c["delivered"]+=int(action in ("retest","reassess"));c["keep"]+=int(action=="keep");c["invalid"]+=int(action=="invalid_output")
    pairs={}
    for group in ("ordinary","disputed","conditional","positive","negative"):
        cs=[k for k,v in keys.items() if v["phase"]==group]
        for ref in (["simple","legacy"] if group=="ordinary" else ["simple"]):
            gains=[x for x in cs if detail[x+"/premise"]["correct"] and not detail[x+"/"+ref]["correct"]]
            losses=[x for x in cs if not detail[x+"/premise"]["correct"] and detail[x+"/"+ref]["correct"]]
            pairs[group+"/"+ref]=dict(gains=gains,losses=losses)
    for arm in ("simple","premise"):
        pairs["unrelated/"+arm]=[x for x,v in keys.items() if v["phase"]=="ordinary" and detail[x+"/"+arm]["correct"]
                                  and not detail[x.replace("-ordinary","-unrelated")+"/"+arm]["correct"]]
    return dict(counts=counts,paired=pairs,decisions=detail)


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    for n in ("keys","outcomes","output"): ap.add_argument(n,type=Path)
    ap.add_argument("--overrides",type=Path)
    ap.add_argument("--cards",action="store_true")
    a=ap.parse_args()
    k,r=(json.loads(p.read_text()) for p in [a.keys,a.outcomes])
    overrides=json.loads(a.overrides.read_text()) if a.overrides else {}
    write(a.output,prepare(k,r)[0] if a.cards else score(k,r,overrides))
