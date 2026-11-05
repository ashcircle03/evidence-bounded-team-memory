"""Render self-contained, per-case source and answer comparisons from scored output."""
from evaluation.decision_records.build import read
from .verify import OUT,HERE

def flat(s):
    return " ".join(s.split())

def main():
    key=read(HERE/"key.json")
    data=read(OUT/"cases.json")
    development=read(OUT/"development-final.json")["results"]
    inputs=read(HERE/"dev-inputs.json")
    lines=["# 개발 사례별 설명 검사", "", "각 원문 조각의 문자 범위는 개발 결과 JSON에 저장했다. 대조 문장의 순서는 기존 설명, 정확한 의역, 반대로 바꾼 의역, 사실인 원문 발췌다."]
    for row in inputs:
        d=development[row["id"]];fixed=d["revised"]
        lines+=["", "## "+row["id"],"","> "+flat(row["result"]["incoming"]["quote"]),""]
        for claim,a in zip(row["claims"],d["checks"]):
            lines+=["- "+("허용" if a["accepted"] else "보류")+" · "+claim]
            if a["unsupported"]:lines+=["  - "+", ".join(a["unsupported"])]
        lines+=["","수리 후 "+fixed["action"]]
        for k,v in fixed.get("role_evidence",{}).items():
            e=v["evidence"];lines+=["- "+k+" · "+flat(e["quote"])+f" · [{e['start']}, {e['end']})"]
    (OUT/"development.ko.md").write_text("\n".join(lines)+"\n")
    lines=["# 새 Git 사례별 비교","", "각 링크는 원본 Git 커밋, 아래 구절은 실제 모델이 선택한 구절이다."]
    for cid,k in key.items():
        if k["scenario"]!="mixed" or k["view"]!="raw":continue
        lines+=["",f"## {k['topic']}","",f"[과거 결정]({k['earlier']}) · [새 보고]({k['report']}) · [대조 결정]({k['alternative']})","",k["rubric"]]
        for method in ("simple","referenced-review","role-review"):
            c=data[cid+"/"+method];r=c["result"]
            lines+=["",f"### {method}","",f"{c['action']} · 대상 {c['target']} · 두 구절 {c['pair']} · 조건 설명 {c['grounded']} · 대조까지 {c['contrast']}"]
            if r.get("basis"):lines+=["",r["basis"]]
            for w in ("previous","incoming","alternative"):
                if r.get(w):lines+=["",w+" · "+flat(r[w]["quote"])]
            for w in ("rationale","distinction"):
                if r.get(w):lines+=["",w+" · "+flat(r[w])]
            for role,v in r.get("role_evidence",{}).items():
                lines+=["- "+role+" · "+flat(v["evidence"]["quote"])]
    (OUT/"cases.ko.md").write_text("\n".join(lines)+"\n")
    lines=["# QA 답과 출처 재검증",""]
    for q,v in read(OUT/"qa-historical.json").items():
        lines+=["",f"## {q}","",v["question"],"",f"원래 결과와 답·인용 일치 · {v['identical']}"]
        for a in v["after"].get("answers",[v["after"]]):
            lines+=["","- "+a.get("answer",a.get("status",""))+" · "+a.get("location",""),"  > "+flat(a.get("quote",""))]
    for q,v in read(OUT/"comparison.json")["qa"].items():
        lines+=["","## Git pull · "+key[q]["topic"],"",v["question"]]
        for side,item in zip(("원문만 있는 복제본","pull한 복제본"),v["answers"]):
            lines+=["",side+" · "+item["out"].get("status","")]
            for a in item["out"].get("answers",[]):lines+=["- "+a["answer"]+" · "+a["location"],"  > "+flat(a["quote"])]
    (OUT/"qa.ko.md").write_text("\n".join(lines)+"\n")
if __name__=="__main__":main()
