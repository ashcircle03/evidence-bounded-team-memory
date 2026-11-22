"""Retrospective audit of frozen public outputs. Supply the QANom checkout on PYTHONPATH."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from qanom.annotations.decode_encode_answers import Question
from qanom.evaluation.roles import question_to_sem_role
from evaluation.record_layout.public_score import baseline_raw_edges, read_lines
from evaluation.record_layout.score_predicate import unique_span
from evaluation.record_layout.score import edges

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / ".cache/records-public-gold-dev-v1"
RESULTS = ROOT / "results/record-layout"
ROLES = {"subject": "R1", "time": "when", "basis": "why", "condition": "condition"}


def groups(text, calls):
    out = defaultdict(list)
    for i, call in enumerate(calls):
        try:
            entries = json.loads(call["output"])["extractions"]
        except (ValueError, KeyError):
            continue
        for row in entries:
            for k in ("claim", *ROLES):
                if isinstance(row.get(k), str):
                    loc = unique_span(text, row[k])
                    if loc:
                        out[i, row.get(k+"_attributes", {}).get("claim_group")].append((k,*loc))
    return list(out.values())


def main():
    text = {d["id"]:d["text"] for d in json.loads((DATA/"panel.json").read_text())["documents"]}
    predictions = {d["id"]:d for d in read_lines(ROOT/".cache/answer-versions/records-current-124911.jsonl")}
    verbs = json.loads((DATA/"detected.json").read_text())
    gold = defaultdict(dict)
    for row in read_lines(DATA/"gold.jsonl"):
        sid = row["qasrl_id"]
        words = list(re.finditer(r"\S+",text[sid]))
        role = question_to_sem_role(Question.from_slots(**dict(row, text=row["question"],
                is_passive=row["is_passive"]=="True",is_negated=row["is_negated"]=="True"))).value
        for span in row["answer_range"].split("~!~"):
            a,b=map(int,span.split(":"))
            gold[sid][(*words[int(row["verb_idx"])].span(),words[a].start(),words[b-1].end(),role)] = row["question"]
    total = Counter()
    by_role = defaultdict(Counter)
    examples = defaultdict(list)
    rows=[]
    for sid, links in gold.items():
        t=text[sid]
        calls=predictions[sid]["calls"]
        grouped=groups(t,calls)
        strict=baseline_raw_edges(t,calls,{tuple(v["span"]) for v in verbs[sid]["verbs"]})
        for key,question in links.items():
            p,q,a,b,role=key
            related=[g for g in grouped if any(k=="claim" and i<=p<q<=j for k,i,j in g)]
            near=[(k,i,j) for g in related for k,i,j in g]
            all_fields=[v for g in grouped for v in g]
            if key in strict: category="strict"
            elif any(ROLES.get(k)==role and (i,j)==(a,b) for k,i,j in near): category="predicate_alignment"
            elif any(k!="claim" and (i,j)==(a,b) for k,i,j in near): category="other_field_exact"
            elif any(i<=a<b<=j for k,i,j in near): category="same_group_contains"
            elif any(i<=a<b<=j for k,i,j in all_fields): category="elsewhere_contains"
            else: category="no_full_span"
            total[category]+=1
            by_role[role][category]+=1
            rows.append([sid,*key,category])
            if len(examples[category])<4:
                examples[category].append(dict(id=sid,question=question,verb=t[p:q],answer=t[a:b],
                    output=[(k,t[i:j]) for k,i,j in near],text=t))
    conditions=[]
    for c in json.loads((DATA/"requirements.json").read_text())["cases"]:
        sid,t=c["id"],c["text"]
        a=t.index(c["action"]);b=a+len(c["action"])
        i=t.index(c["condition"]);j=i+len(c["condition"])
        current=predictions[sid]
        hit=any(a<=p<q<=b and (i,j)==(x,y) and r=="condition" for p,q,x,y,r in edges(current["graph"],t))
        gs=groups(t,current["calls"])
        explicit=any(any(k=="condition" and (x,y)==(i,j) for k,x,y in g)
                     and any(k=="claim" and a<=x<y<=b for k,x,y in g) for g in gs)
        conditions.append(dict(**c,stored_hit=hit,raw_hit=explicit,
                        output=[[(k,t[x:y]) for k,x,y in g] for g in gs],
                        raw=[json.loads(r["output"]) for r in current["calls"]]))
    assert len(rows)==8838 and total["strict"]==194
    report=dict(counts=total,by_role=by_role,examples=examples,conditions=conditions,links=rows)
    (RESULTS/"public-raw-audit.json").write_text(json.dumps(report,ensure_ascii=False))
    print(total)
    print('condition raw/stored',Counter((c['raw_hit'],c['stored_hit']) for c in conditions))
    for c in conditions:
        if not c["stored_hit"]:
            print(c["id"],c["condition"],'|',c["action"],'|',c["output"])
if __name__=="__main__":
    main()
