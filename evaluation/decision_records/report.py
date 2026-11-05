"""Aggregate the frozen blind judgments and render a source-linked row per event."""
from pathlib import Path
from evaluation.decision_records.build import ROOT, HERE, read, save
from evaluation.decision_records.audit import prepare

RESULT = ROOT / "results/decision_records"


def render(data, wr, rr, folder=RESULT, expected_packets=None):
    cards,links=prepare(data,wr,rr,expected_packets)
    decisions=read(folder/"semantic.json")
    assert set(decisions)=={k for k,v in cards.items() if v["eligible"]}
    packed={}
    for c in data["cases"]:
        cid=c["id"]
        units={}
        for arm in "ABC":
            key=links.get(cid+"/"+arm)
            if key is None:
                continue
            card=cards[key]
            verdict=decisions.get(key)
            if verdict is None:
                reason="출력·인용 형식 오류" if not card["valid"] else "조치 또는 인용 대상이 정답과 다름"
            else:
                reason=verdict["basis"]
            units[arm]=dict(raw=card["raw"],parsed=card["parsed"],valid=bool(card["valid"]),
                            correct=bool(verdict and verdict["correct"]),basis=reason,cited=card["cited"],card=key)
        packed[cid]=dict(group=c["group"],task=c["task"],expected=c.get("rubric",c.get("aliases")),
                         action=c.get("action"),previously_correct=c.get("previously_correct"),arms=units)
    save(folder/"outcomes.json",packed)
    summary={}
    for group in sorted({x["group"] for x in packed.values()} | {"prior_correct","all_qa","new_review"}):
        if group=="prior_correct": rows={k:v for k,v in packed.items() if v["previously_correct"]}
        elif group=="all_qa": rows={k:v for k,v in packed.items() if v["task"]=="qa"}
        elif group=="new_review": rows={k:v for k,v in packed.items() if v["group"] in ("historical","controlled")}
        else: rows={k:v for k,v in packed.items() if v["group"]==group}
        table={}
        for arm in "ABC":
            matched={k:v for k,v in rows.items() if arm in v["arms"]}
            if not matched: continue
            def select(test): return [k for k,v in matched.items() if test(v,v["arms"][arm])]
            table[arm]=dict(n=len(matched),correct=select(lambda v,u:u["correct"]),invalid=select(lambda v,u:not u["valid"]),
                grounded_hits=select(lambda v,u:v["action"]=="review" and u["correct"]),
                false_alerts=select(lambda v,u:v["action"]=="keep" and u["parsed"].get("action")=="review"),
                explicit_keeps=select(lambda v,u:v["action"]=="keep" and u["valid"] and u["parsed"].get("action")=="keep"),
                old_losses=select(lambda v,u:v["previously_correct"] and not u["correct"]),
                gains_vs_A=select(lambda v,u:u["correct"] and not v["arms"]["A"]["correct"]),
                losses_vs_A=select(lambda v,u:not u["correct"] and v["arms"]["A"]["correct"]))
        summary[group]=table
    save(folder/"scores.json",summary)
    def shrink(v): return ' '.join(v.split()).replace('|','\\|')
    lines=["# 사건별 판단과 원문 인용","",
           "각 원문의 발췌 번호는 해당 입력 안에서 고정했다. 아래는 실제 인용 구절의 시작 부분이며, 전체 구절과 모델 원출력은 [outcomes.json](outcomes.json)에 있다. A는 원문, B는 AI 메모 추가, C는 당시 유지보수자 메모 추가다.",""]
    for c in data["cases"]:
        result=packed[c["id"]]; lines+=["## "+c["id"]+" · "+c["group"],"",c.get("question",c.get("rubric","")),"","| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |","|---|---|---|---|---|---|"]
        for arm,row in result["arms"].items():
            out=row["parsed"]
            quote=[]
            for side,p in row["cited"].items():
                if not p: continue
                fragment=shrink(p["text"])[:125]
                loc=p["location"]
                quote.append((f"[{out.get(side,side)}]({loc})" if loc.startswith("https:") else str(out.get(side,side)))+" “"+fragment+"”")
            lines.append(" | ".join(["| "+arm,"✓" if row["correct"] else "✗",shrink(str(out.get("action",out.get("answer","invalid")))),shrink(out.get("reason","")), "<br>".join(quote),row["basis"]+" |"]))
        lines+=[""]
    (folder/"cases.ko.md").write_text("\n".join(lines)+"\n")
    for group,rows in summary.items():
        print(group, {k:{a:(len(b) if isinstance(b,list) else b) for a,b in v.items()} for k,v in rows.items()})


if __name__=="__main__":
    import sys
    data=read(HERE/"frozen.json")
    wr=read(RESULT/"writer.json")
    if "--secondary" in sys.argv:
        from evaluation.decision_records.followup import inputs
        from evaluation.decision_records.packets import writers
        extra=read(HERE/"fresh.json")
        ids={p["id"] for p in writers(extra)}
        new_writer={"calls":[r for r in wr["calls"]+read(RESULT/"extra-writer.json")["calls"] if r["id"] in ids]}
        expected=inputs(data,wr)+inputs(extra,new_writer)
        joined={"notes":{**data["notes"],**extra["notes"]},"cases":[c for c in data["cases"] if c["task"]=="review"]+extra["cases"]}
        render(joined,None,read(RESULT/"constrained-reader.json"),RESULT/"constrained",expected)
    else:
        render(data,wr,read(RESULT/"reader.json"))
