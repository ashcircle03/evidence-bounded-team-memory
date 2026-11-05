"""Keep two-answer delivery distinct from an explicit unresolved conflict."""
from hashlib import sha256
from pathlib import Path
import re
import json
from evaluation.decision_records.build import ROOT,HERE,read,save
from evaluation.decision_records.multi_qa import inputs
from evaluation.decision_records.packets import assemble

D=ROOT/"results/decision_records"
def score():
    data=read(HERE/"multisource.json");reader=read(D/"multi-reader.json")
    packets={p["id"]:p for p in inputs(data,read(D/"writer.json"))}
    judgments={}
    for row in reader["calls"]:
        uid=row["id"];cid=uid.split("/")[0];c=next(x for x in data["cases"] if x["id"]==cid)
        assert row["sha256"]==packets[uid]["sha256"]
        txt=re.sub(r"^```(?:json)?\s*|\s*```$","",row["raw"].strip(),flags=re.I)
        tree=json.loads(txt)
        wrapper=tree[0] if isinstance(tree,list) and len(tree)==1 and "answers" in tree[0] else tree
        answers=wrapper.get("answers",[]) if isinstance(wrapper,dict) else wrapper
        lookup={k:v for table in assemble(c,data) for k,v in table.items()}
        cited=[{"value":a.get("value"),"condition":a.get("condition"),"source":lookup.get(str(a.get("source")))} for a in answers]
        matches=[]
        for gold in c["sides"]:
            side=next((a for a in cited if a["source"] and a["source"]["location"]==gold["location"] and
                       any(s.casefold() in str(a["value"]).casefold() for s in gold["aliases"])),None)
            if side:
                val=" ".join(str(side[k]).casefold() for k in ("value","condition"))
                if gold["condition"] and gold["condition"].casefold() not in val:side=None
            matches.append(bool(side))
        paired=all(matches) and len(cited)==2
        status=wrapper.get("status") if isinstance(wrapper,dict) else None
        unresolved=status=="unresolved" or bool(re.search(r'\bunresolved\b',txt,re.I))
        strict=paired and (c["expected_status"]=="conditional" or unresolved)
        judgments[uid]=dict(two_answers_and_sources=paired,explicit_resolution_and_sources=strict,
                            expected=c["expected_status"],status=status,raw=row["raw"],citations=cited)
    assert set(judgments)==set(packets)
    save(D/"multisource-outcomes.json",judgments)
    lines=["# 복수 근거 QA 보존","", "답·조건·원문 인용과 충돌의 미해결 표시를 따로 판정했다. 배열이나 중첩 형태여도 실제로 전달한 근거는 인정했다.","","| 문항 | 조건 | 반환한 답과 인용 ID | 양측 근거 | 상태까지 보존 |","|---|---|---|---|---|"]
    for uid,v in sorted(judgments.items()):
        cid,arm=uid.split("/")
        parts=[(str(x["value"])+" ["+x["source"]["location"]+"]") if x["source"] else "근거 없음" for x in v["citations"]]
        lines.append(f"| {cid} | {arm} | {' / '.join(parts)} | {int(v['two_answers_and_sources'])} | {int(v['explicit_resolution_and_sources'])} |")
    lines+=["","[원출력과 전체 인용 문단](multisource-outcomes.json)"]
    (D/"multisource.ko.md").write_text("\n".join(lines)+"\n")

if __name__=="__main__":score()
