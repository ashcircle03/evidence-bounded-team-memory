"""Run the public readers and independent fixed-witness controls on an allocated GPU."""
import argparse
import gc
from hashlib import sha256
import json
from pathlib import Path
import tempfile

from team_memory.evidence import Passage, ask, active_sources
from team_memory.fixed_review import adjudicate, explain
from team_memory.pair_selection import Comparison, DOCUMENT, SUPPORT, REASON, payload, select
from team_memory.pair_selection import assess as original
from team_memory.sync import DEFAULT_GOAL, pull, relevant_followups
from team_memory.store import capture, Store, digest
from team_memory.writer import local_generator


class LoggedReader:
    def __init__(self, generate):
        self.generate=generate
        self.calls={}

    def call(self, instruction, content, score):
        sig=sha256((instruction+"\n"+content).encode()).hexdigest()
        if sig not in self.calls:
            value=(self.generate.evidence_margin if score else self.generate)(instruction,content)
            self.calls[sig]=dict(system=instruction,content=content,value=value,score=score)
        return self.calls[sig]["value"]

    def __call__(self,s,x):return self.call(s,x,False)
    def evidence_margin(self,s,x):return self.call(s,x,True)


def old_order(content, reverse):
    data=json.loads(content)
    if not reverse:return content
    return json.dumps(dict(goal=data["goal"],report=data["report"],earlier=data["earlier"]),ensure_ascii=False)


def locate(env, witness):
    src=env["source"]; quote=witness["quote"]
    assert src["location"]==witness["location"] and src["text"].count(quote)==1
    return Passage(digest(env),src["location"],src["speaker"],src["text"].index(quote),quote,"source_only")


def evaluate(c,reader):
    new=c["incoming"];sid=digest(new);history={digest(d):(d,"source_only") for d in c["prior"]}
    # Whole-store comparison receives none of the fixed-witness annotations.
    out={}
    if not c.get("fixed_only"):
        from team_memory.evidence import assess
        out["end_to_end"]={method:assess(history,sid,new,DEFAULT_GOAL,reader,method) for method in ("pairwise","fixed-review")}
    old_doc=next(d for d in c["prior"] if d["source"]["location"]==c["fixed_old"]["location"])
    old=locate(old_doc,c["fixed_old"]); incoming=locate(new,c["fixed_new"])
    pair=Comparison(old,incoming,0,0)
    # Recover exactly the original full-document input for this known candidate.
    docs=[]
    def record(s,x):
        if s==DOCUMENT:docs.append(x)
        return 0
    select({old.sid:history[old.sid]},sid,new,DEFAULT_GOAL,record)
    assert len(docs)==1
    fixed={}
    for flip in (False,True):
        tag="report-first" if flip else "earlier-first"
        phrases=old_order(payload(DEFAULT_GOAL,old.quote,incoming.quote),flip)
        doc=reader.evidence_margin(DOCUMENT,old_order(docs[0],flip))
        support=reader.evidence_margin(SUPPORT,phrases)
        original_reason=reader(REASON,phrases).strip()
        v=adjudicate(pair,history,DEFAULT_GOAL,reader,report_first=flip)
        # Ask both readers for the explanation even when their gate keeps. Never expose
        # a forced explanation as a proposal or ground-truth hit.
        forced,focus=explain(pair,DEFAULT_GOAL,reader)
        fixed[tag]=dict(original=dict(action="reassess" if min(doc,support)>0 else "keep",
                                      document=doc,support=support,forced_reason=original_reason),
                        revised=dict(result=v,forced_reason=forced,focus=focus))
    out["fixed"]=fixed
    return out


def git(cwd,*args):
    import os,subprocess
    env=dict(os.environ,GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM="1",GIT_AUTHOR_NAME="Test",GIT_COMMITTER_NAME="Test",
             GIT_AUTHOR_EMAIL="fixture@example.invalid",GIT_COMMITTER_EMAIL="fixture@example.invalid")
    subprocess.run(["git","-c","commit.gpgSign=false","-C",str(cwd),*args],env=env,check=True,stdout=subprocess.DEVNULL)


def integration(rows,reader,temp):
    probes=[]
    for cid,question in (("development-checkout","Which configuration key opts sparse-checkout users into the earlier optimized branch-creation behavior?"),
                         ("git-cvs-pos","What literal value is needed to initialize an empty CVS password when neither source supplies one?")):
        c=next(row for row in rows if row["id"]==cid)
        root=Path(temp)/cid;root.mkdir();origin=root/"origin.git";origin.mkdir();git(origin,"init","--bare");git(origin,"symbolic-ref","HEAD","refs/heads/main")
        git(root,"clone",str(origin),"author");author=root/"author";git(author,"symbolic-ref","HEAD","refs/heads/main");before=Store(author/"records")
        for e in c["prior"]:capture(before,e)
        git(author,"add",".");git(author,"commit","-qm","prior");git(author,"push","-u","origin","main")
        git(root,"clone",str(origin),"reader");after=Store(root/"reader/records")
        capture(before,c["incoming"]);git(author,"add",".");git(author,"commit","-qm","arrival");git(author,"push")
        res=pull(after,DEFAULT_GOAL,reader,"fixed-review")
        assert before.load("sources")==after.load("sources")
        probes.append((cid,question,before,after,res["arrivals"]))
    return probes


def run(args):
    import torch
    assert torch.cuda.is_available()
    blob=args.packets.read_bytes(); rows=json.loads(blob);assert len(rows)==args.count
    reader=LoggedReader(local_generator(args.model,max_new_tokens=96))
    res={}
    for row in rows:
        res[row["id"]]=evaluate(row,reader);print(row["id"],len(reader.calls),flush=True)
    with tempfile.TemporaryDirectory() as temp:
        probes=integration(rows,reader,temp)
        calls=reader.calls;del reader;gc.collect();torch.cuda.empty_cache()
        qa_reader=LoggedReader(local_generator(args.model,max_new_tokens=64))
        qa={}
        for cid,q,a,b,decisions in probes:
            qa[cid]=dict(question=q,decision=decisions,baseline=ask(active_sources(a),q,qa_reader,"simple"),
                         candidate=ask(active_sources(b),q,qa_reader,"simple"),context=relevant_followups(b,q))
    report=dict(status="complete",job_id=args.job,input_sha256=sha256(blob).hexdigest(),model="Qwen2.5-3B-Instruct",
                revision="aa8e72537993ba99e69dfaafa59ed015b17504d1",device=torch.cuda.get_device_name(),rows=res,
                calls=calls,qa=qa,qa_calls=qa_reader.calls)
    tmp=args.output.with_suffix(".tmp");tmp.write_text(json.dumps(report,ensure_ascii=False));tmp.replace(args.output)


if __name__=="__main__":
    p=argparse.ArgumentParser()
    for n in ("packets","model","output","job"):p.add_argument(n,type=Path if n in ("packets","output") else str)
    p.add_argument("--count",type=int,required=True);p.add_argument("--max-new-tokens",type=int)
    run(p.parse_args())
