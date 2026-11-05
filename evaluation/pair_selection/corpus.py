"""Pinned Git reports, development replays, and an untouched set with plausible decoys."""
from datetime import datetime
from pathlib import Path
from evaluation.decision_records.build import HERE as PREVIOUS, commit, read, save

HERE=Path(__file__).resolve().parent
NEW=[
    ("mail","3494dfd3ee","3ff15040e2","155067ab4f","The defaults/config/options order fails for --identity because identity selects which config to read."),
    ("checkout","fa655d8411","8424bfd45b","07351d9899","Skipping worktree/index updates on checkout -b is unsafe during the initial checkout."),
    ("missing","7c0fe330d5","f06ab027ef","8560723266","The on-disk existence test treats a cached/virtual empty tree as missing."),
    ("amend","356ee4659b","2d05ef2778","3abd4a67d9","The in-process commit path checks HEAD instead of HEAD^ for emptiness during amend."),
]
def build():
    first=read(PREVIOUS/"frozen.json"); later=read(PREVIOUS/"fresh.json")
    notes={**first["notes"],**later["notes"]}
    cases=[c for c in first["cases"]+later["cases"] if c["task"]=="review"]
    for idx,(topic,old,pos,neg,reason) in enumerate(NEW):
        notes[topic]={"raw":[commit(old)]}
        # Adjacent domains rather than the decision under test alone.
        other=["eol","hunk","order","squash"][idx]
        for j,(report,act) in enumerate([(pos,"review"),(neg,"keep")]):
            new=commit(report);ts=datetime.fromisoformat(new["time"])
            assert all(datetime.fromisoformat(raw["time"])<ts for t in (topic,other) for raw in notes[t]["raw"])
            order=[topic,other] if (idx+j)%2 else [other,topic]
            cases.append(dict(id=f"unseen-{idx+1}{'p' if not j else 'n'}",group="unseen_git",task="review",topics=order,incoming=new,target=topic,action=act,rubric=reason if not j else "The new documentation change provides no evidence against this earlier implementation decision."))
    return dict(notes=notes,cases=cases)
if __name__=="__main__":
    save(HERE/"corpus.json",build())
