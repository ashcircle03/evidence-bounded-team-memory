"""Rebuild the previously published pilot as a regression-only set for the frozen new reader."""
import argparse
import json
from pathlib import Path

from evaluation.team_pilot.pilot import AUTHORS, DEFAULT_GOAL, DEVELOPMENT, HERE, dev_sources, envelope, pep_sources, write
from team_memory.store import digest

def build(peps, ever):
    docs, cases = {}, []
    def add(env):
        key = digest(env)
        docs[key] = env
        return key
    book = json.loads((HERE/"cases.json").read_text())
    manuals = [add(env) for env in pep_sources(peps).values()]
    for i,c in enumerate(book["qa"]):
        n = c["pep"]
        other = add(envelope(c["counter"],f"casebook://messages/{digest(c['counter'])}",AUTHORS[i]))
        noise = [add(envelope(f"The calendar reserves {day} as the only meeting day for the PEP {n} integration review.",
                    f"casebook://calendar/{n}/{j}", AUTHORS[i+j])) for j,day in enumerate(("Monday","Thursday"))]
        for phase,extra in [("clean",[]),("unrelated",noise),("conflict",[other])]:
            cases.append(dict(id=f"old-pep-{n}-{phase}",task="qa",phase=phase,history=manuals+extra,
                              question=c["question"],as_of="2026-11-03T12:00:00Z",arms=["premise"]))
    old = [add(envelope(c["previous"],f"casebook://decisions/{digest(c['previous'])}",AUTHORS[i])) for i,c in enumerate(book["review"])]
    for i,c in enumerate(book["review"]):
        new = add(envelope(c["incoming"],f"casebook://observations/{digest(c['incoming'])}",AUTHORS[(i+7)%len(AUTHORS)],"2026-11-04T12:00:00Z"))
        cases.append(dict(id=f"old-review-{i+1:02}",task="review",history=old,incoming=new,goal=DEFAULT_GOAL,
                          as_of=docs[new]["observed_at"],arms=["premise"]))
    existing = dev_sources(ever)
    docs.update({k:v[0] for k,v in existing.items()})
    for name,q,_,_ in DEVELOPMENT:
        cases.append(dict(id="old-"+name,task="qa",history=list(existing),as_of="2025-02-01T00:00:00Z",arms=["premise"],question=q))
    return dict(documents=docs,cases=cases)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    for k in ("peps","ever","output"):
        p.add_argument(k,type=Path)
    a=p.parse_args()
    write(a.output,build(a.peps,a.ever))
