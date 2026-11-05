"""Auxiliary test of the decision rule when source localization is supplied."""
import json
from hashlib import sha256
from pathlib import Path
from team_memory.contrast_review import choose,MATCH,REASON,DIFFERENCE,NONE,encoded
from team_memory.sync import DEFAULT_GOAL


def run(args):
    import torch
    from team_memory.writer import local_generator
    assert torch.cuda.is_available()
    model=local_generator(args.model,max_new_tokens=96)
    blob=args.packets.read_bytes();items=json.loads(blob);assert len(items)==args.count
    results={}
    for row in items:
        query=row["report"]
        ordered=row["earlier"]
        win=choose(model,MATCH,dict(goal=DEFAULT_GOAL,incoming=query),[v["text"] for v in ordered]+[NONE])
        out={}
        if win<len(ordered):
            x=dict(earlier=ordered[win]["text"],incoming=query)
            out=dict(location=ordered[win]["location"],reason=model(REASON,encoded(x)).strip(),
                     distinction=model(DIFFERENCE,encoded(dict(x,other=ordered[1-win]["text"]))).strip())
        results[row["id"]]=out
    d=dict(status="complete",job_id=args.job,input_sha256=sha256(blob).hexdigest(),results=results,device=torch.cuda.get_device_name(),
           model="Qwen2.5-3B-Instruct",revision="aa8e72537993ba99e69dfaafa59ed015b17504d1")
    tmp=args.output.with_suffix(".tmp");tmp.write_text(json.dumps(d,ensure_ascii=False));tmp.replace(args.output)


if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    for n in ("packets","model","output","job"):p.add_argument(n,type=Path if n in ("packets","output") else str)
    p.add_argument("--count",type=int,required=True);p.add_argument("--max-new-tokens",type=int);run(p.parse_args())
