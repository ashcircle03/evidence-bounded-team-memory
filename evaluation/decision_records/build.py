"""Recover immutable raw sources and genuinely contemporaneous maintainer notes."""
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime
from hashlib import sha256

from evaluation.revision.final_cases import ORDINARY
from evaluation.team_pilot.pilot import pep_sources, UPSTREAM

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT.parent
HERE = Path(__file__).resolve().parent
GIT = WORK / ".work/revision-git.git"


def read(path):
    return json.loads(path.read_text())


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def git(*args):
    return subprocess.check_output(["git", "--git-dir", str(GIT), *args], text=True).strip()


def commit(rev):
    oid, date, author, msg = git("show", "-s", "--format=%H%x00%cI%x00%an%x00%B", rev).split("\0", 3)
    msg = re.split(r"(?im)^(?:[\w-]+-by|Cc|Link):\s", msg)[0].strip()
    return dict(location="https://github.com/git/git/commit/"+oid, time=date, author=author, text=msg)


TOPICS = {
    "submodule": ("1d699f7934", ["1d699f7934^2"]),
    "pack": ("ad635e82d6", ["0aca34e826","3b13a5f263"]),
    "order": ("a856e7d69f", ["3afc679b","d7c1ec3e"]),
    "eol": ("9bc89b17e3", ["8462ff43"]),
    "squash": ("4a3bf32b6c", ["e12a7ef597","15ef69314d"]),
    "runner": ("ecc486b1f8", ["93a04bb105"]),
    "mmap": ("9db22910f7", ["ba41a8b600","01caf20d57"]),
    "graft": ("6d8f8ebb74", ["20fd6d5799","d6538246d3"]),
    "describe": ("f3ccd9f0d9", ["30b1c7ad9d"]),
    "clone": ("bc88defa2f", ["f38aa83f9a"]),
    "diff": ("ccafbbfb4e", ["a18d66cefb"]),
}
# Each tuple gives the old topic, genuine later record, expected action and semantic criterion.
ARCHIVE = [
    ("pack","9ac3f0e5b3","review","The small-field design drops or repeatedly reads large deltas, hurting pack size or time for that workload."),
    ("pack","eb31044ff7","keep","The corrected multi-pack-index offset encoding is separate from the in-memory delta-size choice."),
    ("order","091f4cf358","review","Generation-first ordering can increase walk count or time on certain topologies, contrary to the old claim."),
    ("order","4c399442f7","keep","Hyphenation of the file name does not affect ordering or the walk."),
    ("eol","6cb09125be","review","safecrlf=false should suppress round-trip errors but the flag conversion can emit a warning."),
    ("eol","2731a7840a","keep","Grammar or style in userdiff leaves the line-ending flags and behavior untouched."),
    ("squash","dd2e36ebac","review","Moving fixup/squash counting away from localized text caused an off-by-one in displayed message numbers."),
    ("squash","d3a8caebf3","keep","Wording about rebase-merges preserves its meaning and has no bearing on squash-message numbering."),
]
# The observations below are controlled counterfactuals, never historical reports.
CONTROL = [
    ("runner","Our Windows build with a native Perl and the required Subversion bindings completed 200 massively parallel prove runs with no crashes. For the same failed-test subset the median turnaround fell from 19 to 11 minutes.","review","Re-test prove on the newly stable Windows Perl configuration. The old MSYS2 crashes remain valid."),
    ("runner","The Linux native Perl workers completed 200 massively parallel prove runs with no crashes. On the Windows MSYS2 pool the same unexplained crashes recurred, and there is still no native Perl with Subversion bindings.","keep","Linux success does not remove the Windows compatibility and crash reason."),
    ("mmap","On the new kernel we benchmarked nonempty 2 KiB packed-refs files. mmap was faster than read in all ten runs. Zero-length files still failed at munmap; they were excluded from the timing comparison.","review","Re-test mmap for small nonempty files on the new kernel while keeping the empty-file exception."),
    ("mmap","On the new kernel mmap beat read in all ten runs on 128 MiB packed-refs files. For nonempty 2 KiB files read still won. Zero-length mappings still failed at munmap.","keep","Large-file results do not overturn the small- or empty-file policy."),
    ("graft","We tested a prototype that keys the graph by the active graft table. On the grafted repository all 800 ancestry queries matched a raw walk and were faster. The shipping graph format and its results are unchanged.","review","Test the graft-aware prototype separately. The original incompatibility of the shipping graph still holds."),
    ("graft","On the repository without grafts all 800 ancestry queries matched a raw walk and were faster. With active grafts the prototype still used the original parent links and returned wrong ancestors.","keep","Ungrafted speed does not remove the correctness problem with active grafts."),
]
KNOWN = [
    ("describe","d0e52c1728","review","The candidate limit still gives incorrect distance with disjoint roots."),
    ("clone","58325b93c5","review","A nonlocal transport can be mistaken for a local clone despite the URL test."),
    ("diff","b59ec03cb5","review","Freeing the containing buffer can double-free it with word-diff and color-moved together."),
]


def build():
    notes = {}
    for topic,(m,raw_ids) in TOPICS.items():
        merge = commit(m)
        msg = merge["text"].split("\n\n",1)[1]
        summary = msg.split("\n\n* ",1)[0].strip()
        if topic == "submodule":
            summary = next(s.strip() for s in msg.splitlines() if "Don't parse" in s)
        if topic == "runner":
            summary = summary.split("previous run.",1)[0]+"previous run."
        if topic == "order":
            # The maintainer's subject list identifies the decision. Use the literal listed line.
            summary = next(s.strip() for s in msg.splitlines() if "use generations in paint_down" in s)
        assert summary in merge["text"]
        raw = [commit(r) for r in raw_ids]
        for r, doc in zip(raw_ids,raw):
            subprocess.run(["git","--git-dir",str(GIT),"merge-base","--is-ancestor",r,m],check=True)
            assert datetime.fromisoformat(doc["time"]) <= datetime.fromisoformat(merge["time"])
        notes[topic] = dict(raw=raw, human={**merge,"text":summary}, origin="contemporaneous_git_merge")
    dev = ROOT/"evaluation/revision/development"
    j,s = [read(dev/(n+".json")) for n in ("jaewon","seonghun")]
    def env(e):
        return dict(location=e["source"]["location"],text=e["source"]["text"],author=e["owner"],time=e["observed_at"])
    notes["aimers"] = dict(raw=[env(j)],human=None,origin="authorship_unverified")
    cases=[]
    def add(cid,group,topic,new,action,criterion):
        # An older plausible decision accompanies the target. Never expose target or gold label.
        other = {"pack":"mmap","order":"mmap","eol":"runner","squash":"runner",
                 "runner":"submodule","mmap":"runner","graft":"order","describe":"order",
                 "clone":"submodule","diff":"describe","aimers":"runner"}[topic]
        pair=sorted([topic,other],key=lambda t:sha256((cid+t).encode()).hexdigest())
        for t in pair:
            cutoff=(notes[t]["human"] or notes[t]["raw"][0])["time"]
            assert datetime.fromisoformat(cutoff) < datetime.fromisoformat(new["time"]), (cid,t)
        cases.append(dict(id=cid,group=group,task="review",topics=pair,incoming=new,target=topic,action=action,rubric=criterion))
    for label,items in [("historical",ARCHIVE),("prior_git",KNOWN)]:
        for i,(topic,n,action,reason) in enumerate(items,1):
            add(f"{label}-{i:02}",label,topic,commit(n),action,reason)
    for i,(t,msg,a,r) in enumerate(CONTROL,1):
        new=dict(location=f"fixture://changed-condition/{i}",text=msg,author="controlled team report",time="2021-01-01T00:00:00Z")
        add(f"scope-{i:02}","controlled",t,new,a,r)
    add("aimers","prior_aimers","aimers",env(s),"review","Compare clean-room TM-S with the current blend under the new setup. The old official TabM result remains valid.")
    data=ROOT/"results"
    scores=read(data/"revision/scored.json")["decisions"]
    prior_git={k.split("-")[0] for k,v in scores.items() if "-ordinary/" in k and v["correct"]}
    cards=read(data/"team_pilot/review-cards.json")
    prior_peps={v["case"] for v in cards.values() if v["phase"]=="clean" and v["correct"]}
    def qa(cid,q,raw,acceptable,answers,prior,topic,group="retention"):
        # Replay a fixed incoming work record. On legacy facts this is an interference test.
        event=next(c for c in cases if c["target"]==topic and c["group"] in ("historical","controlled"))
        cases.append(dict(id=cid,task="qa",group=group,topics=event["topics"],incoming=event["incoming"],raw=raw,
                          question=q,correct_locations=acceptable,aliases=answers,previously_correct=prior))
    rev="683c54c999c301c2cd6f715c411407c413b1d84e"
    from evaluation.revision.build_final import build as old_build
    docs=old_build(GIT)[0]["documents"]
    for i,(name,q,answers) in enumerate(ORDINARY,1):
        match=next(e["source"] for e in docs.values() if e["source"]["text"].splitlines()[0].strip(":`")==name)
        other=next(e["source"] for e in docs.values() if e["source"]["text"].splitlines()[0].strip(":`")==("format.suffix" if i==6 else "gc.aggressiveDepth"))
        items=[match,other] if i%2 else [other,match]
        cid=f"q{i:02}"
        qa(cid,q,items,[match["location"]],answers,cid in prior_git,["pack","order","eol","squash"][(i-1)%4])
    peps=pep_sources(WORK/".work/peps-external.git")
    for i,c in enumerate(read(ROOT/"evaluation/team_pilot/cases.json")["qa"]):
        n=c["pep"]; src=peps[n]["source"]; lines=src["text"].splitlines(); ln=c["line"]-1
        src={**src,"text":"\n".join(lines[max(0,ln-7):ln+9])}
        other=peps[498]["source"]; other={**other,"text":"\n".join(other["text"].splitlines()[14:25])}
        cid=f"pep-{n}"
        qa(cid,c["question"],[src,other] if i%2 else [other,src],[src["location"]],c["answers"],cid in prior_peps,["runner","graft","mmap"][i%3])
    store=[read(p)["source"] for p in (WORK/".work/speaker-run/paired-snapshot/sources").glob("*.json")]
    ext=read(data/"revision/evermem-external.json")["items"]
    for i,x in enumerate(ext[:3]):
        paths={s.replace("|","/") for s in x["retrieval_reference_hits"]}
        relevant=sorted([e for e in store if "/".join(e["location"].split("/")[-3:]) in paths],key=lambda e:e["location"])
        assert len(relevant)==len(paths)
        qa(x["id"],x["question"],relevant,[e["location"] for e in relevant],[[x["reference"]],["at least 10 working days","at least 10 business days"],[x["reference"]]][i],True,"runner")
    for n,(topic,q,ans) in enumerate([("eol","With the earlier SAFE_CRLF_FALSE setting, what should happen on EOL roundtrip errors?",["do nothing"]),("mmap","According to the old change, what does the empty packed-refs load return?",["0"]),("runner","Which directory did the old Makefile approach inspect for failed tests?",["test-results/","test-results"])],1):
        allraw=notes[topic]["raw"]
        qa(f"related-{n}",q,[],[p["location"] for p in allraw],ans,False,topic,"related_qa")
    return dict(notes=notes,cases=cases)


if __name__=="__main__":
    save(HERE/"frozen.json",build())
