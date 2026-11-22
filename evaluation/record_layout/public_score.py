"""Score raw-document extraction. Gold never reaches either generation process."""
import argparse
from collections import Counter, defaultdict
import hashlib
from contextlib import redirect_stdout
from functools import lru_cache
import json
import os
from pathlib import Path
import re
import sys

from team_memory.records.arguments import with_arguments
from evaluation.record_layout.score import edges
from evaluation.record_layout.score_predicate import unique_span


def metrics(tp, fp, fn):
    return dict(tp=tp, fp=fp, fn=fn, precision=tp/(tp+fp) if tp+fp else None,
                recall=tp/(tp+fn) if tp+fn else None, f1=2*tp/(2*tp+fp+fn) if tp+fp+fn else None)


def read_lines(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def baseline_raw_edges(text, calls, verbs):
    """Read grouped Qwen rows before the production compiler, including ungrounded output."""
    result = set()
    roles = {"subject":"R1", "time":"when", "basis":"why", "condition":"condition"}
    for number, call in enumerate(calls):
        try:
            extractions = json.loads(call["output"])["extractions"]
        except (KeyError, ValueError, TypeError):
            continue
        groups = defaultdict(list)
        for entry in extractions:
            for kind in ("claim", *roles):
                if kind in entry:
                    group = entry.get(kind+"_attributes", {}).get("claim_group")
                    if isinstance(entry[kind], str):
                        groups[group].append((kind,entry[kind]))
                    break
        for group, items in groups.items():
            claims = [v for k,v in items if k=="claim"]
            for kind, value in items:
                if kind not in roles:
                    continue
                loc = unique_span(text,value)
                for claim in claims or [""]:
                    anchor = unique_span(text,claim)
                    matches = [v for v in verbs if anchor and anchor[0]<=v[0] and v[1]<=anchor[1]]
                    p = matches[0] if len(matches)==1 else anchor
                    if p and loc:
                        result.add((*p,*loc,roles[kind]))
                    else:
                        result.add(("unresolved",number,group,claim,value,roles[kind]))
    return result


def main(cache, reference, current, official):
    from qanom.annotations.decode_encode_answers import Question
    from qanom.evaluation.roles import question_to_sem_role
    from qanom.question_info import get_slots
    sys.path.insert(0,str(official/"scripts"))
    import paraphrases
    # The pinned release imports a missing name. Keep the author's comparison function.
    paraphrases.get_paraphrase_score = paraphrases.is_paraphrase
    from evaluate import evaluate
    from common import Question as GoldQuestion, Role

    @lru_cache(maxsize=32768)
    def parse(template):
        try:
            return get_slots(template, True, True, True) or {}
        except (KeyError, IndexError, ValueError, TypeError):
            return {}

    def role(slots):
        if not slots.get("wh"):
            return "unknown"
        return question_to_sem_role(Question.from_slots(**slots)).value

    gold = defaultdict(set)
    author_gold = defaultdict(list)
    docs = {s["id"]:s["text"] for s in json.loads((cache/"panel.json").read_text())["documents"]}
    token_spans = {sid:[m.span() for m in re.finditer(r"\S+", t)] for sid,t in docs.items()}
    for row in read_lines(cache/"gold.jsonl"):
        sid = row["qasrl_id"]
        words = token_spans[sid]
        idx = int(row["verb_idx"])
        slots = dict(row, text=row["question"], is_passive=row["is_passive"]=="True",is_negated=row["is_negated"]=="True")
        rng = [tuple(map(int, a.split(":"))) for a in row["answer_range"].split("~!~")]
        for a,b in rng:
            gold[sid].add((*words[idx],words[a][0],words[b-1][1],role(slots)))
        author_gold[sid,idx].append(Role(GoldQuestion(**slots),rng))

    author_pred = defaultdict(list)
    reference_run=json.loads(reference.read_text())
    assert reference_run["status"]=="complete" and set(reference_run["rows"])==set(docs)
    assert reference_run["input"]==hashlib.sha256((cache/"panel.json").read_bytes()).hexdigest()
    base_rows = {x["id"]:x for x in read_lines(current)} if current else {}
    if current:
        assert set(base_rows)==set(docs)
    conditions = {r["id"]:r for r in json.loads((cache/"requirements.json").read_text())["cases"]}
    counts = defaultdict(Counter)
    rejected = Counter()
    detection = defaultdict(Counter)
    by_role = defaultdict(Counter)
    raw_counts = defaultdict(Counter)
    costs = Counter()
    for sid,text in docs.items():
        rows = reference_run["rows"][sid]
        stored = with_arguments(dict(text=text), rows, reference_run["model"])["record_arguments"]["links"]
        n_raw = sum(len(q["answers"]) for row in rows for q in row["qas"])
        rejected["raw_answer_mentions"] += n_raw
        rejected["distinct_stored_links"] += len(stored)
        ref, base, ref_conditions, base_conditions = set(), set(), set(), set()
        base_heads = set()
        verbs = {tuple(r["predicate"]) for r in rows}
        ungrounded = {(tuple(row["predicate"]), qa["question"], answer)
                      for row in rows for qa in row["qas"] for answer in qa["answers"]
                      if unique_span(text,answer) is None}
        for link in stored:
            p,x=link["predicate"],link["argument"]
            a,b,c,d=p["start"],p["end"],x["start"],x["end"]
            slots=parse(link.get("role_template","")) if link.get("role_template") else {}
            ref.add((a,b,c,d,role(slots)))
            if slots.get("wh")=="when" and re.match(r"^(if|unless)\b",x["quote"],re.I):
                ref_conditions.add((a,b,c,d))
            if sid in conditions or not slots:
                continue
            tokens=token_spans[sid]
            pi=next((i for i,v in enumerate(tokens) if v==(a,b)),None)
            ai=next((i for i,v in enumerate(tokens) if v[0]==c),None)
            bi=next((i for i,v in enumerate(tokens) if v[1]==d),None)
            if None not in (pi,ai,bi):
                fields=dict(slots,text=link["role_question"])
                for k in list(fields):
                    if fields[k]=="_":fields[k]=""
                author_pred[sid,pi].append(Role(GoldQuestion(**fields),[(ai,bi+1)]))
        if current:
            graph = base_rows[sid]["graph"]
            for call in base_rows[sid]["calls"]:
                costs.update({k:v for k,v in call["usage"].items() if type(v) is int})
            units={u["id"]:u for u in graph["units"]}
            for claim in graph["claims"]:
                for assertion in claim.get("assertions",[{"unit_ids":claim["claim"]}]):
                    ids=assertion["unit_ids"]
                    a,b=units[ids[0]]["start"],units[ids[-1]]["end"]
                    heads=[w for w in verbs if a<=w[0] and w[1]<=b]
                    # Never use the gold predicate to resolve a broad claim.
                    head=heads[0] if len(heads)==1 else (a,b)
                    base_heads.add(head)
                    for k,r in (("subject","R1"),("time","when"),("basis","why"),("condition","condition")):
                        runs=[]
                        for uid in claim[k]:
                            u=units[uid]
                            if runs and not text[runs[-1][1]:u["start"]].strip():
                                runs[-1]=(runs[-1][0],u["end"])
                            else:
                                runs.append((u["start"],u["end"]))
                        base.update((*head,c,d,r) for c,d in runs)
            base_conditions={(a,b,c,d) for a,b,c,d,r in edges(graph,text) if r=="condition"}
        arms={"reference":ref, "current":base, "candidate":base|ref} if current else {"reference":ref}
        if sid in conditions:
            cond=conditions[sid]
            x=text.index(cond["condition"]);y=x+len(cond["condition"])
            a=text.index(cond["action"]);b=a+len(cond["action"])
            preds={"reference":ref_conditions,"current":base_conditions,"candidate":ref_conditions|base_conditions}
            for name in arms:
                pred=preds[name]
                hits=sum(a<=p<q<=b and (s,e)==(x,y) for p,q,s,e in pred)
                counts["condition_"+name].update(tp=int(hits>0),fp=len(pred)-int(hits>0),fn=int(hits==0))
        else:
            truth=gold[sid]
            before = {"reference": ref | ungrounded}
            if current:
                before["current"] = baseline_raw_edges(text,base_rows[sid]["calls"],verbs)
                before["candidate"] = before["reference"] | before["current"]
            for name,pred in before.items():
                raw_counts[name].update(tp=len(truth&pred),fp=len(pred-truth),fn=len(truth-pred))
            for name,pred in arms.items():
                for label in {e[-1] for e in truth|pred}:
                    actual={e for e in truth if e[-1]==label}
                    proposed={e for e in pred if e[-1]==label}
                    by_role[name+"/"+label].update(tp=len(actual&proposed),fp=len(proposed-actual),fn=len(actual-proposed))
                counts[name].update(tp=len(truth&pred),fp=len(pred-truth),fn=len(truth-pred))
            gv={e[:2] for e in truth}
            for name, heads in (("reference",verbs),("current",base_heads),("candidate",base_heads|verbs)):
                if name in arms:
                    detection[name].update(tp=len(heads&gv),fp=len(heads-gv),fn=len(gv-heads))
    author=[[0,0,0],[0,0,0]]
    with open(os.devnull,"w") as silent, redirect_stdout(silent):
        for key,truth in author_gold.items():
            scores=evaluate(author_pred[key],truth)
            for i in range(2):
                for j,num in enumerate(scores[i].as_tuple()):author[i][j]+=num
    return dict(raw_exact={k:metrics(**v) for k,v in raw_counts.items()},
                by_role={k:metrics(**v) for k,v in by_role.items()},exact={k:metrics(**v) for k,v in counts.items()},predicates={k:metrics(**v) for k,v in detection.items()},
                author_gold_predicate_scores={k:metrics(*v) for k,v in zip(("unlabelled","labelled"),author)},
                reference_alignment=rejected,current_usage=costs)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for name in ("cache","reference","official"):
        parser.add_argument(name,type=Path)
    parser.add_argument("--current",type=Path)
    a=parser.parse_args()
    print(json.dumps(main(a.cache,a.reference,a.current,a.official),indent=2))
