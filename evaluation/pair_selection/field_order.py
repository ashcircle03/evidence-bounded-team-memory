"""Stress test which document Qwen reads first within a pair, keeping temporal roles fixed."""
from hashlib import sha256
import json

from evaluation.decision_records.build import read, save
from evaluation.decision_records.packets import assemble, passages
from .score import label
from .trial import HERE, RESULT, scores_and_reasons, streams
from team_memory.pair_selection import select
from team_memory.store import digest
from team_memory.sync import DEFAULT_GOAL


def changed(content, flipped):
    doc = json.loads(content)
    assert list(doc) == ["goal", "earlier", "report"]
    if flipped:
        doc = {"goal": doc["goal"], "report": doc["report"], "earlier": doc["earlier"]}
    return json.dumps(doc, ensure_ascii=False)


def packets(data):
    original, _ = scores_and_reasons(data)
    result = []
    for p in original:
        if "/forward/" not in p["id"]:
            continue
        for variant in ("earlier-first", "report-first"):
            content = changed(p["content"], variant=="report-first")
            result.append(dict(p, id=variant+"/"+p["id"], layout=variant, peer=p["id"],
                               content=content, sha256=sha256((p["system"]+"\n"+content).encode()).hexdigest()))
    return result


def score():
    data = read(HERE / "corpus.json")
    key = read(HERE / "key.json")
    shots = {r["id"]: r for r in read(RESULT / "field-margins.json")["calls"]}
    primary = read(RESULT/"cases.json")
    rows = {}
    for case, order, history, incoming in streams(data):
        if order != "forward":
            continue
        cid = case["id"]
        old, new, _ = assemble(case, data)
        target = passages(data["notes"][case["target"]]["raw"], "T")
        result = {}
        for arm in ("earlier-first", "report-first"):
            counter=0
            def margin(instruction, content):
                nonlocal counter
                counter+=1
                row=shots[f"{arm}/{cid}/forward/{counter}"]
                encoded=changed(content, arm=="report-first")
                assert sha256((instruction+"\n"+encoded).encode()).hexdigest()==row["sha256"]
                return row["margin"]
            best=select(history,digest(incoming),incoming,DEFAULT_GOAL,margin)
            a,b=label(old,best.old.cite()),label(new,best.new.cite())
            ko,kn=key.get(cid,([],[]))
            result[arm]=dict(old=a,new=b,action="review" if min(best.document_margin,best.support_margin)>0 else "keep",
                             correct_pair=any(old[a]==target["T."+k] for k in ko) and int(b.split(".")[-1]) in kn)
        r=primary[f"{cid}/forward/pairwise"]
        base=(r["old_id"],r["new_id"],r["action"])
        def decision(v):return v["old"],v["new"],v["action"]
        rows[cid]=dict(group=case["group"],expected=case["action"],**result,
                       stable=decision(result["earlier-first"])==decision(result["report-first"]),
                       reproduces_primary=decision(result["earlier-first"])==base)
    save(RESULT/"field-order.json",rows)
    return rows


if __name__=="__main__":
    import sys
    from pathlib import Path
    if len(sys.argv)>1:save(Path(sys.argv[1]),packets(read(HERE/"corpus.json")))
    else:score()
