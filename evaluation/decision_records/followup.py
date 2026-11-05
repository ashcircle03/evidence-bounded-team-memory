"""New cases and a fixed categorical readout following the unusable action format."""
import json
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from evaluation.decision_records.build import HERE, ROOT, commit, git, read, save
from evaluation.decision_records.packets import assemble, display, packet, writers, judgments

INSTRUCTION = """Does this incoming work change the reason for any past choice enough to reopen or test it? A sound original observation may still hold under its conditions. An update on the same topic alone is insufficient. Select exactly one action (review or keep), the single most informative OLD passage and NEW passage, then explain the specific relation in one sentence. Cite raw passages rather than notes. A constrained form records your choices as action, old, new, reason. Compare all past choices before selecting."""

def fresh():
    prior=read(HERE/"frozen.json")
    notes={k:prior["notes"][k] for k in ("runner","mmap")}
    for t,m,olds in [("hunk","436d18f2d0",["2b8ea7f3c7","436d18f2d0^2"]),("verbosity","157ee05061",["a56771a668d"])]:
        c=commit(m)
        summary=c["text"].split("\n\n",1)[1].split("\n\n* ",1)[0].strip()
        raw=[commit(r) for r in olds]
        for r,doc in zip(olds,raw):
            git("merge-base","--is-ancestor",r,m)
            assert datetime.fromisoformat(doc["time"])<=datetime.fromisoformat(c["time"])
        notes[t]=dict(raw=raw,human={**c,"text":summary},origin="contemporaneous_git_merge")
    samples=[
        ("hunk","f4d35a6b49","review","Recount missed empty context lines when an editor strips their leading space."),
        ("hunk","af91b0230c","keep","Moving the excludesFile docs does not change hunk recounting."),
        ("verbosity","e84c3cf3dc","review","Passing -v through to git-submodule fails because the script does not accept it."),
        ("verbosity","7401ab92f8","keep","Deprecation of a rebase backend does not change how verbosity is forwarded to submodules."),
        ("hunk","The new GUI edits then splits every selected hunk. In 18 of 50 trials we applied the selection to the wrong offset after a split. The 50 control trials that applied edited hunks without splitting all landed correctly.","review","Revisit the accepted loss of offset correction after edited hunks are split; the old unsplit common-case finding remains valid."),
        ("hunk","The new GUI edits hunks and applies them without splitting. All 50 trials applied at the correct offset. The optional edit-then-split path was disabled and accounted for no user traffic or test failures.","keep","The unsplit workload matches the old common case; no evidence the known split limitation has become material.")]
    rows=[]
    for i,(t,n,a,why) in enumerate(samples,1):
        literal=i>4
        new=dict(location=f"fixture://unseen/{i}",author="controlled team report",time="2021-01-01T00:00:00Z",text=n) if literal else commit(n)
        decoy="mmap" if t=="hunk" else "runner"
        cid=f"fresh-{i:02}"
        topics=sorted([t,decoy],key=lambda k:sha256((cid+k).encode()).hexdigest())
        assert all(datetime.fromisoformat(notes[k]["human"]["time"])<datetime.fromisoformat(new["time"]) for k in topics)
        rows.append(dict(id=cid,group="fresh_controlled" if literal else "fresh_git",task="review",topics=topics,incoming=new,target=t,action=a,rubric=why))
    return {"notes":notes,"cases":rows}


def inputs(data,logged):
    packets=judgments(data,logged)
    byid={r["id"]:r for r in data["cases"]}
    out=[]
    for p in packets:
        c=byid[p["id"].split("/")[0]]
        if c["task"]!="review":continue
        payload=json.loads(p["content"])
        old,new,_=assemble(c,data)
        q=packet(p["id"],INSTRUCTION,payload,160)
        q["choices"]=[["review","keep"],list(old),list(new)]
        out.append(q)
    return out


if __name__=="__main__":
    f=fresh();save(HERE/"fresh.json",f)
    # Only genuinely new historical topics need additional writing.
    save(Path("/private/tmp/dr-writer-new.json"),[p for p in writers(f) if p["id"] in ("write/hunk","write/verbosity")])
