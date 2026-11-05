"""Greedy constrained form. No access to evaluation keys or previously scored outputs."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import time


def transitions(tokenizer, fields):
    # Share the end of each field across its possible values. The delimiter after
    # the ID distinguishes e.g. paragraph 1 from paragraph 10.
    transitions=[{}]
    start=0
    for options in fields:
        ends=[]
        for text in options:
            ids=tokenizer.encode(text,add_special_tokens=False)
            assert tokenizer.decode(ids)==text
            state=start
            for token in ids:
                if token not in transitions[state]:
                    transitions[state][token]=len(transitions)
                    transitions.append({})
                state=transitions[state][token]
            ends.append(state)
        after=len(transitions)
        shared={}
        transitions.append(shared)
        for end in ends:
            assert not transitions[end]
            transitions[end]=shared
        start=after
    return transitions


class Form:
    def __init__(self, tokenizer, width, choices):
        self.width=width
        self.tables=[]
        self.states=[0]*len(choices)
        for actions,old,new in choices:
            self.tables.append(transitions(tokenizer,[
                ["Action: "+a+"\nOld: " for a in actions],
                [a+"\nNew: " for a in old],[a+"\nReason:" for a in new]]))

    def __call__(self, ids, scores):
        latest=ids[:,-1].tolist() if ids.shape[1]>self.width else None
        for i,table in enumerate(self.tables):
            state=self.states[i]
            if latest is not None and table[state]:
                state=table[state][latest[i]]
                self.states[i]=state
            if table[state]:
                allowed=list(table[state])
                kept=scores[i,allowed].clone()
                scores[i].fill_(float("-inf"))
                scores[i,allowed]=kept
        return scores


def run(a):
    import torch
    from transformers import AutoModelForCausalLM,AutoTokenizer,LogitsProcessorList
    if not torch.cuda.is_available():raise RuntimeError("GPU required")
    tok=AutoTokenizer.from_pretrained(a.model,padding_side="left",local_files_only=True)
    model=AutoModelForCausalLM.from_pretrained(a.model,torch_dtype=torch.bfloat16,local_files_only=True).to("cuda").eval()
    blob=a.packets.read_bytes();pack=json.loads(blob)
    assert len({p["id"] for p in pack})==len(pack)==a.count
    entries=[]
    for p in pack:
        assert sha256((p["system"]+"\n"+p["content"]).encode()).hexdigest()==p["sha256"]
        j=json.loads(p["content"]);assert p["choices"]==[["review","keep"],[x["id"] for x in j["old"]],[x["id"] for x in j["incoming"]]]
        msgs=[dict(role="system",content=p["system"]),dict(role="user",content=p["content"])]
        ids=tok.apply_chat_template(msgs,tokenize=True,add_generation_prompt=True)
        assert len(ids)<=8192 and p["max_output_tokens"]==160
        entries.append((len(ids),p["id"],ids,p))
    entries.sort();calls=[];start=time.monotonic()
    with a.output.with_suffix(".partial.jsonl").open("x") as part:
        for n in range(0,len(entries),4):
            group=entries[n:n+4]
            batch=tok.pad({"input_ids":[g[2] for g in group]},padding=True,return_tensors="pt").to("cuda")
            width=batch.input_ids.shape[1]
            form=Form(tok,width,[g[3]["choices"] for g in group])
            with torch.inference_mode():
                generated=model.generate(**batch,do_sample=False,max_new_tokens=160,pad_token_id=tok.eos_token_id,logits_processor=LogitsProcessorList([form]))
            for (length,uid,_,p),tail in zip(group,generated[:,width:].tolist()):
                if tok.eos_token_id in tail:tail=tail[:tail.index(tok.eos_token_id)+1]
                transcript=tok.decode(tail,skip_special_tokens=True)
                m=re.fullmatch(r"Action: (review|keep)\nOld: ([\w.]+)\nNew: ([\w.]+)\nReason:(.*)",transcript,re.S)
                if not m:raise RuntimeError(f"invalid constrained envelope {uid}")
                action,old,new,reason=m.groups()
                assert [action,old,new]==[v for v,choices in zip((action,old,new),p["choices"]) if v in choices]
                ans=dict(action=action,old=old,new=new,reason=reason.strip())
                row=dict(id=uid,sha256=p["sha256"],raw=json.dumps(ans,ensure_ascii=False),transcript=transcript,input_tokens=length,output_tokens=len(tail))
                calls.append(row);part.write(json.dumps(row,ensure_ascii=False)+"\n")
            part.flush();print(len(calls),"/",len(entries),flush=True)
    result=dict(status="complete",job_id=a.job,model="Qwen2.5-3B-Instruct",revision="aa8e72537993ba99e69dfaafa59ed015b17504d1",device=torch.cuda.get_device_name(),dtype=str(model.dtype),generation_seconds=round(time.monotonic()-start,2),input_sha256=sha256(blob).hexdigest(),calls=calls)
    tmp=a.output.with_suffix(".tmp");tmp.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n");tmp.replace(a.output)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    for n in ("packets","model","output","job"):parser.add_argument(n,type=Path if n in ("packets","output") else str)
    parser.add_argument("--count",type=int,required=True);parser.add_argument("--max-new-tokens",type=int)
    run(parser.parse_args())
