from .paths import HERE,OUT
from evaluation.decision_records.build import read

def render(here=HERE,out=OUT):
    rows=read(out/"cases.json");key=read(here/"key.json");ratings=read(out/"ratings.json")
    lines=["# 보고별 재검토와 구별 근거","",
           "원문 혼합과 같은 보고의 음성 대조를 함께 표시했다. 표시가 가려진 자료, 단일 후보, 역순의 결과까지 포함한 전체 원출력은 [cases.json](cases.json)에 있다.",""]
    for cid,c in key.items():
        if c["scenario"]!="mixed" or c["view"]!="raw":continue
        near=next(k for k,v in key.items() if v["topic"]==c["topic"] and v["scenario"]=="no-match" and v["view"]=="raw")
        lines+=["## "+c["topic"],"",c["rubric"],"",c["distinction"],"",f"[과거 결정]({c['earlier']}) · [비슷한 결정]({c['alternative']}) · [새 보고]({c['report']})",""]
        for m in ("simple","pairwise","fixed-review","contrast-review","referenced-review","fixed-witnesses"):
            if cid+"/"+m not in rows:continue
            r=rows[cid+"/"+m];res=r["result"];neg=rows[near+"/"+m]
            lines+=[f"**{m}** · 과거 대상 {'선택' if r['target'] else '누락'} · 혼합 {r['action']} · 무관한 두 후보 {neg['action']}",""]
            for f in ("previous","incoming","alternative","attribution"):
                if f in res:lines+=["- "+{"previous":"과거 결정","incoming":"새 보고","alternative":"비슷한 결정","attribution":"귀속 표현"}[f]+" — "+" ".join(res[f]["quote"].split())]
            for f,idkey in (("rationale","rationale_card"),("distinction","distinction_card")):
                if f in res:
                    lines+=["",res[f]]
                    if r[idkey]:lines+=["","판정 — "+ratings[r[idkey]]["note"]]
            lines+=[""]
    (out/"cases.ko.md").write_text("\n".join(lines)+"\n")
    hist=read(out/"qa-historical.json")
    lines=["# 이전 QA 성공 문항 재검증",""]
    for cid,r in hist.items():
        ans=r["after"]
        lines+=["## "+cid,"",r["question"],"",f"원래 파서 출력 일치 · {r['identical']}",""]
        for a in ans.get("answers",[ans] if "answer" in ans else []):
            lines+=["- "+a["answer"]+" · "+a["location"],"  > "+" ".join(a["quote"].split())]
        lines+=[""]
    (out/"qa.ko.md").write_text("\n".join(lines)+"\n")
if __name__=="__main__":render()
