"""Publish paired outcomes with original excerpts, released explanations and rating notes."""
from evaluation.decision_records.build import read
from .diagnose import OUT,HERE


def render():
    rows=read(OUT/"cases.json")
    ratings=read(OUT/"ratings.json")
    keys=read(HERE/"key.json")
    def judgment(v):
        if v["action"]=="keep":
            return "보류" if v["label"]=="neg" else "재검토 누락"
        if v["label"]=="neg":return "오탐"
        return "적중" if v["grounded"] else "문단 오류" if not v["correct_pair"] else "설명 오류"
    lines=["# Git 사례별 재검토 판정","",
           "고정 조건의 설명은 보류한 경우에도 별도 호출해 채점했다. 실사용 조건에서 보류한 행에는 전달한 설명이나 인용이 없다.",""]
    for cid,key in keys.items():
        lines+=["## "+cid,"",key["rubric"],"",f"[과거 원문]({key['previous']}) · [새 보고]({key['incoming']})",""]
        for regime in ("fixed","end_to_end"):
            subset=[v for v in rows.values() if v["case"]==cid and v["regime"]==regime]
            if not subset:continue
            lines+=["### "+("고정한 근거" if regime=="fixed" else "원문 전체에서 출발"),""]
            for v in subset:
                title=v["method"]+(" · "+v["mode"] if regime=="fixed" else "")
                lines+=[f"**{title}** · {judgment(v)}",""]
                if v["reason"]:
                    lines+=[v["reason"],""]
                if v["card"]:lines+=["설명 채점 — "+ratings[v["card"]]["note"],""]
                if v["old"] and (regime=="end_to_end" or v==subset[0]):
                    lines+=["- 과거 — "+" ".join(v["old"]["quote"].split()),"- 신규 — "+" ".join(v["new"]["quote"].split()),""]
    (OUT/"cases.ko.md").write_text("\n".join(lines))
    q=read(OUT/"qa-historical.json")
    lines=["# 기존 성공 QA의 답과 인용","","문항마다 당시에 성공했던 설정을 복원했다. 동일 여부는 파서가 반환한 상태·답·인용·위치를 모두 비교했다.",""]
    for cid,row in q.items():
        lines+=["## "+cid,"",row["question"],"",f"이전과 동일 — {row['identical']}",""]
        slots=[("복원 결과",row["after"])] if row["identical"] else [("이전",row["before"]),("이번",row["after"])]
        for name,state in slots:
            lines+=[name+" · "+state.get("status",""),""]
            for a in state.get("answers",[state] if "answer" in state else []):
                lines+=[f"- {a['answer']} · {a['location']}","  > "+" ".join(a['quote'].split())]
            lines+=[""]
    (OUT/"qa.ko.md").write_text("\n".join(lines))


if __name__=="__main__":render()
