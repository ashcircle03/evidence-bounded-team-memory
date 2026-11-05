"""Aurora inference payload; no labels or semantic rubrics are packaged here."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import tempfile

from team_memory.evidence import assess,ask,active_sources
from team_memory.store import capture,digest,Store
from team_memory.sync import DEFAULT_GOAL,pull,relevant_followups
from team_memory.writer import local_generator
from fixture_git import git


class Reader:
    def __init__(self,model):
        self.model=model
        self.calls={}
        self.used=[]

    def invoke(self,kind,s,x,n=0):
        key=sha256(json.dumps([kind,s,x,n],ensure_ascii=False).encode()).hexdigest()
        self.used.append(key)
        if key not in self.calls:
            if kind=="options":value=self.model.option_scores(s,x,n)
            elif kind=="margin":value=self.model.evidence_margin(s,x)
            else:value=self.model(s,x)
            self.calls[key]=dict(kind=kind,system=s,content=x,output=value)
        return self.calls[key]["output"]

    def __call__(self,s,x):return self.invoke("generation",s,x)
    def evidence_margin(self,s,x):return self.invoke("margin",s,x)
    def option_scores(self,s,x,n):return self.invoke("options",s,x,n)


def hist(row,reverse=False):
    docs=row["prior"][::-1] if reverse else row["prior"]
    return {digest(d):(d,"source_only") for d in docs}


def evaluate(row, reader, method, reverse=False):
    start=len(reader.used);src=row["incoming"]
    out=assess(hist(row,reverse),digest(src),src,DEFAULT_GOAL,reader,method)
    return dict(result=out,used=reader.used[start:])


def fixture(row,temp,reader):
    root=Path(temp)/row["id"];root.mkdir();origin=root/"remote.git";origin.mkdir()
    git(origin,"init","--bare");git(origin,"symbolic-ref","HEAD","refs/heads/main")
    git(root,"clone",str(origin),"author");author=root/"author";git(author,"symbolic-ref","HEAD","refs/heads/main")
    before=Store(author/"records")
    for d in row["prior"]:capture(before,d)
    git(author,"add",".");git(author,"commit","-qm","prior");git(author,"push","-u","origin","main")
    git(root,"clone",str(origin),"reader");after=Store(root/"reader/records")
    capture(before,row["incoming"]);git(author,"add",".");git(author,"commit","-qm","report");git(author,"push")
    result=pull(after,DEFAULT_GOAL,reader,"contrast-review")
    assert before.load("sources")==after.load("sources")
    return before,after,result["arrivals"]


def run(args):
    import torch,gc
    assert torch.cuda.is_available()
    blob=args.packets.read_bytes();items=json.loads(blob);assert len(items)==args.count
    review=Reader(local_generator(args.model,max_new_tokens=96));results={}
    fresh=Reader(review.model)
    for row in items:
        tag=row["id"]
        r={m:evaluate(row,review,m) for m in ("pairwise","fixed-review","contrast-review")}
        if row.get("check_order"):
            r["contrast-reversed"]=evaluate(row,fresh,"contrast-review",True)
        results[tag]=r
        print(tag,len(review.calls),flush=True)
    with tempfile.TemporaryDirectory() as temp:
        stores={}
        for row in items:
            if row.get("qa"):stores[row["id"]]=fixture(row,temp,review)
        calls={**review.calls,**fresh.calls}
        del review,fresh
        gc.collect();torch.cuda.empty_cache()
        simple=Reader(local_generator(args.model,max_new_tokens=64))
        qa={}
        for row in items:
            tag=row["id"];results[tag]["simple"]=evaluate(row,simple,"simple")
            if tag in stores:
                before,after,arrivals=stores[tag];question=row["qa"];answers=[]
                for store in (before,after):
                    # Independent real generations, including when their input bytes match.
                    single=Reader(simple.model)
                    answer=ask(active_sources(store),question,single,"simple")
                    answers.append(dict(out=answer,used=single.used));calls.update(single.calls)
                qa[tag]=dict(question=question,arrivals=arrivals,context=relevant_followups(after,question),answers=answers)
        calls.update(simple.calls)
    d=dict(status="complete",job_id=args.job,input_sha256=sha256(blob).hexdigest(),device=torch.cuda.get_device_name(),
           model="Qwen2.5-3B-Instruct",revision="aa8e72537993ba99e69dfaafa59ed015b17504d1",results=results,calls=calls,qa=qa)
    tmp=args.output.with_suffix(".tmp");tmp.write_text(json.dumps(d,ensure_ascii=False));tmp.replace(args.output)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for x in ("packets","model","output","job"):parser.add_argument(x,type=Path if x in ("packets","output") else str)
    parser.add_argument("--count",type=int,required=True);parser.add_argument("--max-new-tokens",type=int)
    run(parser.parse_args())
