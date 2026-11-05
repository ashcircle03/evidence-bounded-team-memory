"""Remove arm identities for semantic review and validate raw citations before scoring."""
import argparse
import json
import re
from hashlib import sha256
from pathlib import Path
from evaluation.decision_records.build import read, save
from evaluation.decision_records.packets import assemble, judgments


def parse(raw):
    s=raw.strip()
    if s.startswith("```") and s.endswith("```"):
        s=re.sub(r"^```(?:json)?\s*|\s*```$","",s,flags=re.I)
    try:
        v=json.loads(s)
    except ValueError:
        return {}
    return v if isinstance(v,dict) else {}


def prepare(data,writer,reader,expected_packets=None):
    mapping={c["id"]:c for c in data["cases"]}
    packets = judgments(data,writer) if expected_packets is None else expected_packets
    expected={p["id"]:p for p in packets}
    outputs=reader["calls"]
    assert len(expected)==len(outputs)==len({r["id"] for r in outputs})
    cards, links={},{}
    for r in outputs:
        uid=r["id"]
        assert expected[uid]["sha256"]==r["sha256"]
        cid,arm=uid.split("/")
        c=mapping[cid];old,new,extra=assemble(c,data)
        ans=parse(r["raw"])
        if c["task"]=="qa":
            src=extra|old|new
            evidence=src.get(str(ans.get("source")))
            valid=bool(isinstance(ans.get("answer"),str) and ans["answer"].strip() and evidence)
            scoped=valid and evidence["location"] in c["correct_locations"]
            quotes={"source":evidence}
            intent=None
        else:
            a,b=old.get(str(ans.get("old"))),new.get(str(ans.get("new")))
            intent=ans.get("action")
            valid=bool(intent in ("review","keep") and a and b and isinstance(ans.get("reason"),str) and ans["reason"].strip())
            scoped=valid and a["location"] in {x["location"] for x in data["notes"][c["target"]]["raw"]} and intent==c["action"]
            quotes={"old":a,"new":b}
        card=dict(case=cid,task=c["task"],expected=c.get("action",c.get("aliases")),criterion=c.get("rubric",c.get("question")),
                  raw=r["raw"],parsed=ans,valid=valid,eligible=bool(scoped),cited=quotes)
        key=sha256(json.dumps(card,sort_keys=True).encode()).hexdigest()[:12]
        cards[key]=card; links[uid]=key
    return dict(sorted(cards.items())),links


if __name__=="__main__":
    p=argparse.ArgumentParser()
    for n in ("cases","writer","reader","dest"):
        p.add_argument(n,type=Path)
    a=p.parse_args()
    cards,links=prepare(read(a.cases),read(a.writer),read(a.reader))
    save(a.dest/"cards.json",cards);save(a.dest/"links.json",links)
