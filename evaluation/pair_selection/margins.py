"""Batched equivalent of LocalChoice.evidence_margin; no gold labels or source indices."""
import argparse
import json
import time
from hashlib import sha256
from pathlib import Path


def run(args):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    if not torch.cuda.is_available():
        raise RuntimeError("Expected a Slurm GPU")
    tokenizer=AutoTokenizer.from_pretrained(args.model,local_files_only=True,padding_side="left")
    model=AutoModelForCausalLM.from_pretrained(args.model,local_files_only=True,torch_dtype=torch.bfloat16).to("cuda").eval()
    labels=[tokenizer.encode(s,add_special_tokens=False) for s in ("Yes","No")]
    assert all(len(x)==1 for x in labels)
    label_ids=[x[0] for x in labels]
    blob=args.packets.read_bytes()
    ps=json.loads(blob)
    assert len(ps)==args.count==len({p["id"] for p in ps})
    items=[]
    for p in ps:
        sig=sha256((p["system"]+"\n"+p["content"]).encode()).hexdigest()
        assert sig==p["sha256"]
        messages=[dict(role="system",content=p["system"]),dict(role="user",content=p["content"])]
        ids=tokenizer.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
        assert len(ids)<=8192
        items.append((len(ids),sig,p["id"],ids))
    if "layout" in ps[0]:
        # Align every eight-row block and its padding peers across both field orders.
        # Use padding to the joint block maximum so the physical width also matches.
        from itertools import groupby
        lookup={p["id"]:p for p in ps}
        slots={}
        for arm, entries in groupby(sorted(items,key=lambda x:(lookup[x[2]]["layout"],lookup[x[2]]["peer"])), key=lambda x:lookup[x[2]]["layout"]):
            entries=list(entries)
            for idx in range(0,len(entries),8):
                slots[(arm,idx)]=entries[idx:idx+8]
        blocks=[(group,max(z[0] for (other,j),peers in slots.items() if j==i for z in peers)) for (arm,i),group in slots.items()]
    else:
        items.sort()
        blocks=[(items[i:i+8],None) for i in range(0,len(items),8)]
    calls=[]; started=time.monotonic()
    with torch.inference_mode():
        for i,(group,width) in enumerate(blocks):
            batch=tokenizer.pad({"input_ids":[g[3] for g in group]},return_tensors="pt",padding="max_length" if width else True,max_length=width).to("cuda")
            pos=(batch["attention_mask"].cumsum(-1)-1).clamp(min=0)
            h=model.model(**batch,position_ids=pos,use_cache=False).last_hidden_state[:,-1,:]
            logits=model.lm_head(h)[:,label_ids].float()
            for (length,sig,uid,_),pair in zip(group,logits.tolist()):
                calls.append(dict(id=uid,sha256=sig,input_tokens=length,margin=pair[0]-pair[1]))
            if i%160==0: print(i,"/",len(items),flush=True)
    result=dict(status="complete",job_id=args.job,model="Qwen2.5-3B-Instruct",revision="aa8e72537993ba99e69dfaafa59ed015b17504d1",input_sha256=sha256(blob).hexdigest(),device=torch.cuda.get_device_name(),generation_seconds=round(time.monotonic()-started,2),calls=calls)
    tmp=args.output.with_suffix(".tmp");tmp.write_text(json.dumps(result)+"\n");tmp.replace(args.output)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for n in ("packets","model","output","job"):
        p.add_argument(n,type=Path if n in ("packets","output") else str)
    p.add_argument("--count",type=int,required=True);p.add_argument("--max-new-tokens",type=int)
    run(p.parse_args())
