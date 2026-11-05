"""Slurm smoke through the public pull and QA APIs using actual Qwen weights."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from team_memory.store import Store,capture
from team_memory.sync import pull,relevant_followups,DEFAULT_GOAL
from team_memory.evidence import active_sources,ask,assess
from team_memory.writer import local_generator


def git(cwd,*args):
    env=dict(os.environ,GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM="1",
             GIT_AUTHOR_NAME="Fixture",GIT_COMMITTER_NAME="Fixture",
             GIT_AUTHOR_EMAIL="fixture@example.invalid",GIT_COMMITTER_EMAIL="fixture@example.invalid")
    subprocess.run(["git","-c","commit.gpgSign=false","-C",str(cwd),*args],env=env,check=True,stdout=subprocess.DEVNULL,stderr=None)


def run(args):
    import torch
    assert torch.cuda.is_available()
    raw=args.packets.read_bytes();cases=json.loads(raw)
    assert len(cases)==args.count
    reader=local_generator(args.model,max_new_tokens=96)
    output=[]
    roots=tempfile.TemporaryDirectory()
    probes=[]
    for c in cases:
        if "question" not in c:
            continue
        root=Path(roots.name)/c["id"];root.mkdir()
        origin=root/"origin.git";origin.mkdir()
        git(origin,"init","--bare");git(origin,"symbolic-ref","HEAD","refs/heads/main")
        git(root,"clone",str(origin),"author");author=root/"author"
        git(author,"symbolic-ref","HEAD","refs/heads/main")
        before=Store(author/"records")
        for e in c["old"]:capture(before,e)
        git(author,"add",".");git(author,"commit","-qm","prior");git(author,"push","-u","origin","main")
        git(root,"clone",str(origin),"reader");after=Store(root/"reader/records")
        capture(before,c["incoming"]);git(author,"add",".");git(author,"commit","-qm","arrival");git(author,"push")
        decision=pull(after,DEFAULT_GOAL,reader,"pairwise")["arrivals"]
        probes.append((c,before,after,decision))
    del reader
    import gc
    gc.collect()
    torch.cuda.empty_cache()
    default_reader=local_generator(args.model,max_new_tokens=64)
    for c,before,after,decision in probes:
        qa=[ask(active_sources(store),c["question"],default_reader,"simple") for store in (before,after)]
        output.append(dict(id=c["id"],arrivals=decision,before=qa[0],after=qa[1],
                           review_context=relevant_followups(after,c["question"]),same_sources=before.load("sources")==after.load("sources")))
    roots.cleanup()
    defaults=[]
    for c in cases:
        if not c.get("default_control"):
            continue
        for order in ("forward","reverse"):
            docs=c["old"] if order=="forward" else list(reversed(c["old"]))
            from team_memory.store import digest
            history={digest(doc):(doc,"source_only") for doc in docs}
            r=assess(history,digest(c["incoming"]),c["incoming"],DEFAULT_GOAL,default_reader,"simple")
            defaults.append(dict(id=c["id"]+"/"+order,result=r))
    result=dict(defaults=defaults,status="complete",job_id=args.job,input_sha256=sha256(raw).hexdigest(),model="Qwen2.5-3B-Instruct",revision="aa8e72537993ba99e69dfaafa59ed015b17504d1",calls=output)
    tmp=args.output.with_suffix(".tmp");tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2));tmp.replace(args.output)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("packets","model","output","job"):p.add_argument(name,type=Path if name in ("output","packets") else str)
    p.add_argument("--count",type=int,required=True);p.add_argument("--max-new-tokens",type=int)
    run(p.parse_args())
