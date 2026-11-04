"""Recover dated Git objects and construct distinct source-only final episodes."""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import subprocess

from evaluation.revision.final_cases import ORDINARY, COUNTER, SCOPED, CONTROL, REAL
from evaluation.team_pilot.pilot import envelope, write
from team_memory.store import digest, timestamp

REV = "683c54c999c301c2cd6f715c411407c413b1d84e"
MODULES = "gc help credential fetch merge push format notes grep pack diff commit clone rebase tag status init protocol branch log apply pull".split()
PEOPLE = "Eli Kim Ivo Cy Fia Max Uma Tao Lou Dan".split()


def build(repo):
    def git(*args):
        return subprocess.check_output(["git", "--git-dir", str(repo), *args], text=True).rstrip("\n")

    docs, ids, cases, keys = {}, {}, [], {}
    clock = timestamp(git("show", "-s", "--format=%cI", REV))

    def add(text, location, author, when):
        e = envelope(text, location, author, when)
        k = digest(e)
        docs[k] = e
        return k

    def note(text, author, when):
        return add(text, "trial://worklog/" + digest([author, text]), author, when)

    for mod in MODULES:
        path = f"Documentation/config/{mod}.adoc"
        lines = git("show", f"{REV}:{path}").splitlines()
        starts = [i for i, s in enumerate(lines) if re.match(r"^`?[\w.-]+(?:<[^>]+>[\w.*-]*)?`?::$", s)]
        for index, i in enumerate(starts):
            end = starts[index+1] if index+1 < len(starts) else len(lines)
            loc = f"https://github.com/git/git/blob/{REV}/{path}#L{i+1}-L{end}"
            name = lines[i].strip(":`")
            ids[name] = add("\n".join(lines[i:end]), loc, "Git documentation contributors", clock)
    manual = list(ids.values())
    next_day = (datetime.fromisoformat(clock) + timedelta(days=1)).isoformat()
    reminders = [note(f"The release review calendar reserves {d} as its only meeting day.", author, next_day)
                 for d, author in [("Tuesday","Mina"), ("Friday","Luis")]]

    def qa(cid, question, history, phase, kind, sides, when, arms):
        cases.append(dict(id=cid, task="qa", question=question, history=history, as_of=when, arms=arms))
        keys[cid] = dict(phase=phase, origin=kind, sides=[dict(location=docs[k]["source"]["location"], aliases=alias, condition=cond)
                                                             for k,alias,cond in sides])
        for k,alias,cond in sides:
            assert any(v.casefold() in docs[k]["source"]["text"].casefold() for v in alias) and (not cond or cond in docs[k]["source"]["text"])

    for i,(name, q, aliases) in enumerate(ORDINARY,1):
        for phase, extra, when, arms in [("ordinary", [], clock, ["simple","premise","legacy"]),
                      ("unrelated",reminders,next_day,["simple","premise"])]:
            qa(f"q{i:02}-{phase}",q,manual+extra,phase,"public_git" if not extra else "controlled",[(ids[name],aliases,None)],when,arms)
    for i, (name,q,aliases,other,alts) in enumerate(COUNTER):
        k = note(other,PEOPLE[i],next_day)
        qa(f"d{i+1:02}",q,manual+[k],"disputed","controlled_with_public_source",
           [(ids[name],aliases,None),(k,alts,None)],next_day,["simple","premise"])
    field = []
    for i, (q,one,a,c,two,b,d) in enumerate(SCOPED):
        field.append([note(one,PEOPLE[i],next_day),note(two,PEOPLE[i+5],next_day)])
    for i, (q,one,a,c,two,b,d) in enumerate(SCOPED):
        qa(f"d{i+6:02}",q,[k for pair in field for k in pair]+manual,"conditional","controlled",
           [(field[i][0],[a],c),(field[i][1],[b],d)],next_day,["simple","premise"])

    earlier = [note(old,author,"2024-05-10T09:00:00Z") for author,old,*_ in CONTROL]
    def review(cid, prior, incoming, history, actions, a, b, why, provenance):
        when = docs[incoming]["observed_at"]
        cases.append(dict(id=cid,task="review",history=history,incoming=incoming,as_of=when,arms=["simple","premise"]))
        keys[cid] = dict(phase="positive" if actions != ["keep"] else "negative",origin=provenance,
                         prior=docs[prior]["source"]["location"] if prior else None,
                         incoming=docs[incoming]["source"]["location"],old_cue=a,new_cue=b,actions=actions,reason=why)
    for i,(owner,old,new,actions,a,b,why) in enumerate(CONTROL):
        k = note(new,PEOPLE[i%len(PEOPLE)],"2024-05-12T14:00:00Z")
        review(f"r{i+1:02}",earlier[i],k,earlier,actions,a,b,why,"controlled")

    def commit(name):
        sha, who, when, body = git("show","-s","--format=%H%x00%an%x00%cI%x00%B",name).split("\x00",3)
        # Retain the full subject and body; drop contributor email trailers at the end.
        body = re.split(r"(?m)^(?:Signed-off-by|Acked-by|Reviewed-by|Helped-by|Reported-by|Co-authored-by):", body)[0].rstrip()
        return add(body, f"https://github.com/git/git/commit/{sha}", who, when)

    for i,(old,new,actions,a,b,why) in enumerate(REAL):
        prior = commit(old) if old else None
        inc = commit(new)
        anc = git("rev-list","--no-merges","-n","18",new+"^").splitlines()
        when = docs[inc]["observed_at"]
        history = [k for k in map(commit,anc) if docs[k]["observed_at"] < when][:12]
        if prior:
            git("merge-base","--is-ancestor",old,new)
            if prior not in history:
                history.append(prior)
        # Sort by immutable ID, so an explicitly linked older decision never gets a privileged position.
        review(f"r{i+15:02}",prior,inc,sorted(set(history)),actions,a,b,why,"public_git")
    return dict(documents=docs,cases=cases),keys


if __name__ == "__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ("repo","data","keys"):
        ap.add_argument(name,type=Path)
    a=ap.parse_args()
    data,keys=build(a.repo)
    write(a.data,data)
    write(a.keys,keys)
