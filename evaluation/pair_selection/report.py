"""Human-readable paired outcomes, including the excerpts selected in both orders."""
from evaluation.decision_records.build import read,save
from .trial import HERE,RESULT


def short(text,n=110):
    return " ".join(str(text).split()).replace("|","\\|")[:n]

def cite(k,p):
    stem=f"[{k}]({p['location']})" if p["location"].startswith("https://") else k
    return stem+" “"+short(p["text"])+"”"

def answers(r):
    return r.get("answers", [r] if "answer" in r else [])

def render():
    d=read(HERE/"corpus.json"); rows=read(RESULT/"cases.json");ratings=read(RESULT/"ratings.json")
    lines=["# 재검토 사건별 결과","","문단 번호는 원래 순서의 위치를 가리킨다. 줄임표 없는 원출력·양측 인용·정오와 역순 결과는 [cases.json](cases.json)에 있다. 근거 조합은 채점 전에 고정했다. 보류 시 후보 선택은 진단용 내부 점수이며 사용자에게 전달한 인용으로 세지 않았다.",""]
    for c in d["cases"]:
        cid=c["id"]
        lines+=["## "+cid+" · "+c["group"],"",f"기대 판단은 {c['action']}이다. {c['rubric']}","",
                "| 방식 · 순서 | 판단 | 선택한 과거 문단 | 선택한 신규 문단 | 모델 설명 | 판정 |",
                "|---|---|---|---|---|---|"]
        for m in ("joint","pairwise"):
            for direction in ("forward","reverse"):
                r=rows[f"{cid}/{direction}/{m}"]
                if c["action"]=="keep":
                    why="유지" if r["action"]=="keep" else "오탐"
                elif r["action"]!="review":why="재검토 누락"
                elif not r["target_ok"]:why="잘못된 과거 결정"
                elif not r["pair_ok"]:why="지정된 지지 문단을 인용하지 못함"
                else:why=ratings[r["card"]]["basis"]
                lines.append("| "+" | ".join([m+" · "+direction,r["action"],cite(r["old_id"],r["old"]),cite(r["new_id"],r["new"]),short(r["reason"],245),why])+" |")
        lines.append("")
    (RESULT/"cases.ko.md").write_text("\n".join(lines))
    qa=read(RESULT/"qa-historical.json")
    matched=read(RESULT/"qa-matched-historical.json")
    lines=["# 과거에 실제 맞힌 QA 20건의 회귀 검사","",
           "원래 해당 문항을 맞힌 모델 구성·원문·검색 결과·문항별 호출을 복원해 재추론하고 실제 응답을 동일한 QA 파서에 전달했다. 문항마다 원래 맞힌 구성이 다르다. 모델 성적의 분모로 사용하지 않는다.","",
           "혼합 배치에서는 기존 문항들을 함께 묶었다. 원래 배치에서는 호출마다 이전 이웃 샘플, 순서, 패딩 길이, 출력 상한을 복원했다. 일치는 상태·답·근거 인용과 출처를 포함한 파서 출력 전체의 동일성을 뜻한다.","",
           "| 문항 · 구성 | 질문 | 원래 답과 인용 | 혼합 배치 | 원래 배치 복원 |","|---|---|---|---|---|"]
    def render_answer(r):
        return "<br>".join(short(a["answer"],70)+" · "+cite("출처",dict(location=a["location"],text=a["quote"])) for a in answers(r)) or short(r.get("status"))
    for k,v in qa.items():
        assert v["before"] == matched[k]["before"]
        def outcome(row):
            return "동일" if row["identical"] else render_answer(row["after"])+" ("+row["after"].get("status","")+" · 달라짐)"
        lines.append("| "+" | ".join([k,short(v["question"],190),render_answer(v["before"]),outcome(v),outcome(matched[k])])+" |")
    lines+=["","[혼합 배치의 답과 인용](qa-historical.json) · [원래 배치를 복원한 답과 인용](qa-matched-historical.json) · [복원 후 달라진 원출력](qa-matched-raw-differences.json) · [같은 받은편지함 90개 응답의 혼합 배치 비교](qa-same-inbox.json) · [Git pull 뒤 기록된 모델 호출 재생](integration.json) · [계산 노드의 실시간 Git pull과 QA](live.json)"]
    (RESULT/"qa.ko.md").write_text("\n".join(lines)+"\n")

if __name__=="__main__":render()
