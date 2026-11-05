"""New decisions and natural reports from the Git archive, committed before model inference."""
import re
from datetime import datetime

from evaluation.decision_records.build import commit, read, save
from evaluation.pair_selection.trial import envelope
from .diagnose import HERE, OUT, LAST

# old, positive, topic-adjacent negative, historical alternative; 1-based paragraphs
CASES = [
    ("alias","a9bcf6586d","643df7e234","a9a60b94cc","0989fe9623",2,2,2,
     [1,2],[2,3],"When resolving CamelCased aliases in early config, names must match config keys case-insensitively; -h output is independent."),
    ("cvs","3fb9d58235","e481b1d8db","f3eaa09261","8c372fb01d",2,2,2,
     [1,2],[2],"When neither CLI nor .cvspass supplies a password, initialize the scrambled empty value to A; object IDs do not change password handling."),
    ("svn","b0ad24be8c","8e9d453ce7","ed254710ee","d492b31caf",2,3,2,
     [1,2],[3],"Dropping the Perl/shared library also lost the svn availability check; svnadmin tests need to skip or check when svn is absent. Empty-file test helpers do not restore it."),
    ("trash","38b074de80","6883047071","2f68c99a3b","f69e836fab",2,4,2,
     [2,3],[4,5],"The output directory inherited/defaulted by the subtests puts their scratch outside t0000; set TEST_OUTPUT_DIRECTORY for the sub-tests. Indentation does not affect it."),
    ("symlink","18e051a398","f02033f1d0","150e6b0aed","f66bc5f928",1,2,7,
     [1],[2,6],"Canonicalizing an absolute worktree symlink dereferences the link, making Git act on the target instead of the link. Local clone object-store symlinks are a different operation."),
    ("am","15ced753ac","0e8341f29d","53ce2e3f0a","9b9f5a2258",2,2,7,
     [2],[2],"Patch-format detection must ignore leading whitespace that webmail prepends to saved mail. Resuming a failed patch without a tty is independent."),
]


def paragraph(doc, number):
    return re.split(r"\n\s*\n",doc["text"])[number-1].strip()


def build():
    packets=[]; keys={}
    for i,(cid,a,p,n,b,oi,pi,ni,oks,nks,why) in enumerate(CASES):
        old,positive,negative,other=map(commit,(a,p,n,b))
        for status,update,idx in (("pos",positive,pi),("neg",negative,ni)):
            assert all(datetime.fromisoformat(d["time"])<datetime.fromisoformat(update["time"]) for d in (old,other))
            uid=f"git-{cid}-{status}"
            docs=[old,other] if i%2 else [other,old]
            item=dict(id=uid,prior=[envelope(d) for d in docs],incoming=envelope(update),
                      fixed_old=dict(location=old["location"],quote=paragraph(old,oi)),
                      fixed_new=dict(location=update["location"],quote=paragraph(update,idx)))
            packets.append(item)
            keys[uid]=dict(label=status,rubric=why,allowed_old=[paragraph(old,j) for j in oks],
                           allowed_new=[paragraph(update,j) for j in nks] if status=="pos" else [],
                           previous=old["location"],incoming=update["location"])
            if status=="pos":
                uid="cross-"+cid
                chosen=paragraph(other,2 if len(other["text"].split("\n\n"))>1 else 1)
                packets.append(dict(item,id=uid,fixed_old=dict(location=other["location"],quote=chosen),fixed_only=True))
                keys[uid]=dict(label="neg",rubric="Distinct historical decision. "+why,previous=other["location"],incoming=update["location"])
    # Development checkout fixture exactly as in the earlier experiment.
    base=read(LAST/"cases.json")["unseen-2p/forward/pairwise"]
    from evaluation.pair_selection.trial import streams, HERE as BASE
    case,_,history,new=next(row for row in streams(read(BASE/"corpus.json")) if row[0]["id"]=="unseen-2p")
    packets.append(dict(id="development-checkout",prior=[doc for doc,_ in history.values()],incoming=new,
                        fixed_old=dict(location=base["old"]["location"],quote=base["old"]["text"]),
                        fixed_new=dict(location=base["new"]["location"],quote=base["new"]["text"])))
    keys["development-checkout"]=dict(label="pos",rubric="Initial checkout requires updating the worktree and index; cheap test ordering is incidental.",
            previous=base["old"]["location"],incoming=base["new"]["location"],allowed_old=[base["old"]["text"]],allowed_new=[base["new"]["text"]])
    return packets,keys


if __name__=="__main__":
    packets,keys=build()
    save(HERE/"inputs.json",packets);save(HERE/"key.json",keys)
