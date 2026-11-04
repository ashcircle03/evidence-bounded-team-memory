"""Render navigable per-event outcomes from replayed predictions and adjudicated scores."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from evaluation.revision.score import actual,norm
from evaluation.team_pilot.pilot import write


def report(data,keys,rows,summary,packets,recording,folder):
    lookup={r["id"]:r["result"] for r in rows}
    id_to_packet={p["id"]:p for p in packets}
    compute=defaultdict(Counter)
    review_search={}
    for call in recording["calls"]:
        key=call["id"]
        if key not in id_to_packet:continue
        case,arm,_=key.split("/")
        compute[arm].update(calls=1,input_tokens=call["input_tokens"],output_tokens=call["output_tokens"])
        if keys[case]["phase"]!="positive":continue
        k=keys[case]
        src=json.loads(id_to_packet[key]["content"])
        def found(items,location,cue):
            return any(i["source"]==location and any(norm(cue) in norm(t) for t in
                       (i["excerpts"].values() if "excerpts" in i else [i["excerpt"]])) for i in items)
        review_search[case+"/"+arm]=[found(src["previous"],k["prior"],k["old_cue"]),
                found(src.get("incoming",src.get("new")),k["incoming"],k["new_cue"])]
    write(folder/"cost-and-review-inputs.json",dict(compute=compute,positive_input_coverage=review_search))

    lines=["# 문항별 결과", "", "✓는 답과 근거 또는 재검토 대상·새 근거·조치가 함께 맞았다는 뜻이다. 유지는 명시적으로 기존 결정을 유지한 경우다. 오류는 유효한 답이나 조치를 전달하지 못한 경우다. 과거·신규 원문 전체는 재생 명령의 `--show 사건/방식`으로 확인할 수 있다. [원출력](outputs.json) · [답과 실제 인용 구절](final-outcomes.json) · [재생 명령](../../evaluation/revision/README.md)", ""]
    def cell(name):
        if name not in lookup:return "—"
        result=lookup[name]
        ok=summary["decisions"][name]["correct"]
        if result.get("action"):
            value={"retest":"재시험","reassess":"전제 재평가","keep":"유지","invalid_output":"출력 오류"}[result["action"]]
        else:
            values=actual(result)
            value=" / ".join(x["answer"].replace("|","∣").replace("\n"," ").replace("`","") + (" ("+x["condition"]+")" if "condition" in x else "") for x in values)
            value=value or {"invalid_output":"출력 오류","invalid_citation":"인용 오류","insufficient":"근거 부족"}.get(result.get("status"),str(result.get("status")))
        return ("✓ " if ok else "✗ ") + value
    qa=[c for c in data["cases"] if c["task"]=="qa"]
    for section,cc in [("일반 QA", [c for c in qa if keys[c["id"]]["phase"]=="ordinary"]),
             ("같은 질문에 무관한 충돌 추가",[c for c in qa if keys[c["id"]]["phase"]=="unrelated"]),
             ("답이 갈리거나 조건에 따라 다른 QA",[c for c in qa if c["id"].startswith("d")])]:
        lines+=["## "+section,"","| 사건 및 질문 | 기대 답 | 단순 검색 | 새 모듈 | 기존 QA 리더 |","|---|---|---|---|---|"]
        for c in cc:
            name=c["id"];sides=keys[name]["sides"]
            ans=" / ".join((f"[{s['aliases'][0]}]({s['location']})" if s["location"].startswith("https:") else s["aliases"][0]) + (f" ({s['condition']})" if s["condition"] else "") for s in sides)
            lines.append("| "+" | ".join([name+" · "+c["question"],ans,*(cell(name+"/"+a) for a in ["simple","premise","legacy"])])+" |")
        lines.append("")
    lines+=["## 재검토","","공개 Git의 세 양성 보고에는 과거 커밋에 대한 명시적 참조가 있다. 각 사건에는 당시 과거 기록 12~13개 또는 통제 기록 14개가 주어졌다. 정답 열은 채점용으로만 사용했다.","","| 사건과 새 근거 | 사전 정답 및 이유 | 단순 검색 | 새 모듈 |","|---|---|---|---|"]
    for c in data["cases"]:
        if c["task"]!="review":continue
        name=c["id"];key=keys[name];src=data["documents"][c["incoming"]]["source"]
        title=src["text"].splitlines()[0]
        if src["location"].startswith("https:"):title=f"[{title}]({src['location']})"
        lines.append("| "+" | ".join([name+" · "+title,"/".join(key["actions"])+" · "+key["reason"],cell(name+"/simple"),cell(name+"/premise")])+" |")
    (folder/"cases.ko.md").write_text("\n".join(lines)+"\n")


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    for name in ("source","keys","rows","scores","packets","recording","outdir"):ap.add_argument(name,type=Path)
    a=ap.parse_args()
    report(*(json.loads(p.read_text()) for p in [a.source,a.keys,a.rows,a.scores,a.packets,a.recording]),a.outdir)
