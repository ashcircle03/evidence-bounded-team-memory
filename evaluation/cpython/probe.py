"""Read blind packets using a single Qwen checkpoint. The scoring key stays off the server."""
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path

from team_memory.choice import LocalChoice
from team_memory.qa import read_answer
from team_memory.reconsider import ACTIONS, JUDGE, judge_case, prompt

def run(packets, choose, generate, emit):
    for p in packets:
        for name, goal in p["goals"]:
            direct = dict(p["direct"], goal=goal)
            body = prompt(direct,True,linked=False)
            letter = choose(JUDGE, body)
            emit({"event":p["id"],"goal":name,"arm":"direct","action":ACTIONS[letter],"votes":[letter]})
            again = choose(JUDGE+" Check the initial choice against the actual decision and all constraints.",
                           body+"\nInitial choice: "+letter)
            emit({"event":p["id"],"goal":name,"arm":"checked","action":ACTIONS[again],"votes":[letter,again]})
            verdict = judge_case(dict(p["module"],goal=goal),choose) if p["module"] else {"action":"no_target"}
            emit({"event":p["id"],"goal":name,"arm":"module",**verdict})
    for p in packets:
        for q in p["qa"]:
            res=read_answer(copy.deepcopy(q["evidence"]),q["question"],generate)
            emit({"event":p["id"],"kind":q["kind"],"phase":q["phase"],"arm":"qa",
                  "reader":res.get("reader",{}),"answer":res["answer"]})

if __name__=="__main__":
    j=os.environ["SLURM_JOB_ID"]
    out=Path.cwd()/"results"/("system-"+j);out.mkdir(exist_ok=False)
    src=Path(os.environ["PEP_PACKETS"])
    packets=json.loads(gzip.decompress(src.read_bytes()))
    model=LocalChoice(os.environ["PAIR_MODEL"])
    if model.model.device.type!="cuda":raise RuntimeError("GPU allocation required")
    calls=[];rows=[]
    def log(name,r):
        with (out/name).open("a",encoding="utf8") as f: f.write(json.dumps(r,ensure_ascii=False)+"\n")
    def tokens(system,content):
        t=model.tokenizer.apply_chat_template([{"role":"system","content":system},{"role":"user","content":content}],
                                                add_generation_prompt=True,return_tensors="pt")
        if t.size(1)>8192: raise ValueError("registered input budget exceeded")
        return t
    def trace(kind,system,content,n,value,output_tokens):
        row={"kind":kind,"sha256":hashlib.sha256((system+"\n"+content).encode()).hexdigest(),
             "tokens":n,"output":value,"output_tokens":output_tokens}
        calls.append(row);log("calls.jsonl",row);return value
    def choose(system,content):
        n=tokens(system,content).size(1)
        return trace("choice",system,content,n,model(system,content),1)
    def generate(system,content):
        t=tokens(system,content).to(model.model.device)
        with model.torch.inference_mode():
            y=model.model.generate(input_ids=t,attention_mask=model.torch.ones_like(t),max_new_tokens=96,do_sample=False,
                                   pad_token_id=model.tokenizer.eos_token_id)
        answer=model.tokenizer.decode(y[0,t.size(1):],skip_special_tokens=True)
        return trace("qa",system,content,t.size(1),answer,y.size(1)-t.size(1))
    def emit(row):
        rows.append(row);log("rows.jsonl",row)
        print(row["event"],row["arm"],row.get("goal",row.get("phase")),flush=True)
    run(packets,choose,generate,emit)
    assert len(rows)==24
    report={"status":"complete","job_id":j,"device":str(model.model.device),"dtype":str(model.model.dtype),
            "model":"Qwen2.5-3B-Instruct","revision":"aa8e72537993ba99e69dfaafa59ed015b17504d1",
            "packets_sha256":hashlib.sha256(src.read_bytes()).hexdigest(),"rows":rows,"calls":calls}
    dst=Path.cwd()/"results"/("sm-"+j+".json")
    dst.with_suffix(".tmp").write_text(json.dumps(report,ensure_ascii=False))
    dst.with_suffix(".tmp").replace(dst)
