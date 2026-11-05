"""Versioned raw Git views with balanced two-decision positive and negative histories."""
import copy
from datetime import datetime
import random
import re
from evaluation.decision_records.build import commit,read,save
from evaluation.pair_selection.trial import envelope
from .paths import HERE

# Real earlier target, near alternative, second alternative, incoming report, allowable
# witness paragraph numbers and semantic criteria (held outside the model payload).
CASE = [
 ("scheduler","b6c3f8e12c","69ecfcacfd","daa787010c","c95547a394",[3],[3,5],[1,2,3,4],
  "get_schedule_cmd does not populate its out parameter on every path, crashing the caller; initialize it whenever provided.",
  "The other decision orders scheduler initialization and config changes to avoid disabling auto maintenance if setup fails."),
 ("manual","cc75e556a9","951759d3a5","e7a9807a62","32c6fff4b8",[2],[2,8],[1,2],
  "Adding scalar to the command-documentation regex shifted the man-section capture from $1 to $2 (or captured the name instead of the section).",
  "The other decision adds the scalar help subcommand that delegates to git help scalar; it does not parse manpage headings."),
 ("reverse-index","a587b5a786","ec8e7760ac","66f52fa26b","8fe8bae9d2",[2,3,4,5],[1,2,3],[1,2,3,4],
  "The refactored reverse-index writer needlessly allocates/sorts pack order when no .rev will be written; skip this work on that path.",
  "The other decision selects an existing on-disk reverse index instead of constructing it in memory during read/use."),
 ("difftool","03831ef7b5","99474b6340","9f6013a88d","20de316e33",[1,3,5,6],[1,2],[1,2,3],
  "After the Perl-to-builtin difftool conversion, --no-index stopped working outside a Git worktree; restore this mode.",
  "The other decision forwards the external tool's exit status for --trust-exit-code rather than changing where difftool runs."),
 ("quiet","7b0f229222","4f5b532d18","859fdc0c3c","6b89a34c89",[1,2,3,12,14,16],[2],[1],
  "Progress output added for commit-graph writes fails to honor --quiet and must be suppressed then.",
  "The other decision marks commit-graph messages for translation, not whether progress is displayed."),
 ("slab","ac6d45d11f","c8828530b7","fbda77c6c0","d70f554cdf",[1,2,3,4],[1,9,12,13],[1,2],
  "Clearing the shared commit slab on closing a NULL graph/submodule repo discards data still needed by the parent; that close must leave the slab intact.",
  "The other decision closes an unused file descriptor after mmap to avoid fd exhaustion; it does not release the shared graph slab.")
]


def paragraphs(text):
    return [s.strip() for s in re.split(r"\n\s*\n",text) if s.strip()]


def hide_refs(text,subjects):
    text=re.sub(r"(?<![0-9A-Za-z])[0-9a-f]{7,40}(?![0-9A-Za-z])","[ref]",text)
    title, sep, body=text.partition("\n\n")
    for s in subjects:
        pattern=r"\s+".join(re.escape(w) for w in s.split())
        body=re.sub(pattern,"[referenced subject]",body,flags=re.I)
    return title+sep+body


def build():
    rng=random.Random(78164);data=[];keys={}
    archive=read(HERE.parent/"fixed_review/inputs.json")
    previous=" ".join([str(archive),str(read(HERE.parent/"pair_selection/corpus.json"))])
    for name,a,f,g,n,olds,news,foils,rubric,distinction in CASE:
        old,foil,other,new=map(commit,(a,f,g,n))
        assert all(datetime.fromisoformat(p["time"])<datetime.fromisoformat(new["time"]) for p in (old,foil,other))
        assert new["location"].rsplit("/",1)[1][:10] not in previous
        subjects=[v["text"].split("\n")[0] for v in (old,foil,other)]
        for scenario,pool in (("mixed",[old,foil]),("no-match",[foil,other]),("foil-only",[foil])):
            for view in (["raw","hidden"] if len(pool)==2 else ["raw"]):
                past=list(map(envelope,pool)); rng.shuffle(past)
                arrival=copy.deepcopy(new)
                if view=="hidden":arrival["text"]=hide_refs(new["text"],subjects)
                cid=f"t{len(data):02d}"
                row=dict(id=cid,prior=past,incoming=envelope(arrival))
                if view=="raw" and len(pool)==2:
                    row["check_order"]=True
                if name=="manual" and view=="raw" and scenario=="mixed":
                    row["qa"]="Which git command does the scalar help subcommand delegate to?"
                if name=="quiet" and view=="raw" and scenario=="mixed":
                    row["qa"]="Which option must suppress the new commit-graph write progress?"
                data.append(row)
                source=lambda v,i:paragraphs(v["text"])[i-1]
                keys[cid]=dict(topic=name,scenario=scenario,view=view,expected="keep" if scenario!="mixed" else "review",
                     earlier=old["location"],alternative=foil["location"],report=new["location"],
                     old=[source(old,j) for j in olds],new=[source(arrival,j) for j in news],
                     foil=[source(foil,j) for j in foils],rubric=rubric,distinction=distinction,
                     masked=arrival["text"]!=new["text"])
    return data,keys


if __name__=="__main__":
    d,k=build();save(HERE/"inputs.json",d);save(HERE/"key.json",k)
