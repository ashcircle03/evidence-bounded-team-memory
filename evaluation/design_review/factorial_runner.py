"""Frozen model comparisons. Inference payload contains source text, never semantic keys."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import time
import zipfile

from team_memory.writer import local_generator
from team_memory.evidence import assess
from team_memory.store import digest
from team_memory.sync import DEFAULT_GOAL
import direct

class Reader:
 def __init__(self,model):self.model=model;self.calls=[];self.cache={};self.input_tokens=0;self.output_tokens=0
 def invoke(self,kind,s,x,n=0):
  key=sha256(json.dumps([kind,s,x,n],ensure_ascii=False).encode()).hexdigest()
  if key in self.cache:return self.cache[key]
  start=time.monotonic()
  if kind=='options':
   value=self.model.option_scores(s,x,n);usage=self.model.choice_reader().last_usage
  elif kind=='margin':
   value=self.model.evidence_margin(s,x);usage=self.model.choice_reader().last_usage
  else:
   value=self.model(s,x);usage=self.model.last_usage
  self.input_tokens+=usage['input_tokens'];self.output_tokens+=usage.get('output_tokens',usage.get('scored_tokens',0))
  self.calls.append(dict(kind=kind,system=s,content=x,output=value,usage=dict(usage),seconds=time.monotonic()-start))
  if self.input_tokens>120000 or self.output_tokens>4096:raise RuntimeError('frozen case budget exceeded')
  self.cache[key]=value;return value
 def __call__(self,s,x):return self.invoke('generation',s,x)
 def option_scores(self,s,x,n):return self.invoke('options',s,x,n)
 def evidence_margin(self,s,x):return self.invoke('margin',s,x)

def load(path,large=False):
 import torch
 from transformers import AutoModelForCausalLM,AutoTokenizer
 from functools import lru_cache
 from team_memory.choice import LocalChoice
 tokenizer=AutoTokenizer.from_pretrained(path,local_files_only=True)
 config=dict(local_files_only=True,torch_dtype=torch.bfloat16)
 if large:
  assert torch.cuda.device_count()==2
  config.update(device_map='balanced',max_memory={0:'21GiB',1:'21GiB'})
  model=AutoModelForCausalLM.from_pretrained(path,**config).eval()
  assert all(str(v) not in ('cpu','disk') for v in model.hf_device_map.values())
 else:model=AutoModelForCausalLM.from_pretrained(path,**config).to('cuda').eval()
 @torch.inference_mode()
 def generate(s,x):
  inputs=tokenizer.apply_chat_template([{'role':'system','content':s},{'role':'user','content':x}],add_generation_prompt=True,return_tensors='pt').to(model.device)
  output=model.generate(input_ids=inputs,max_new_tokens=generate.cap,do_sample=False,pad_token_id=tokenizer.eos_token_id)
  generate.last_usage=dict(input_tokens=int(inputs.shape[1]),output_tokens=int(output.shape[1]-inputs.shape[1]))
  return tokenizer.decode(output[0,inputs.shape[1]:],skip_special_tokens=True)
 generate.cap=512
 generate.choice_reader=lru_cache(maxsize=1)(lambda:LocalChoice.from_loaded(path,tokenizer,model))
 generate.option_scores=lambda s,x,n:generate.choice_reader().option_scores(s,x,n)
 generate.evidence_margin=lambda s,x:generate.choice_reader().evidence_margin(s,x)
 generate.identity=dict(device_map=getattr(model,'hf_device_map',None),parameters=sum(p.numel() for p in model.parameters()),dtype=str(model.dtype))
 return generate

def run(args):
 import torch
 blob=args.packets.read_bytes();payload=json.loads(blob);rows=payload['rows'];oracle=payload['oracle']
 assert torch.cuda.is_available()
 generator=load(args.model,args.large);results={}
 partial=args.output.with_suffix('.partial.jsonl')
 with partial.open('x') as log:
  for row in rows:
   cid=row['id'];methods=['module'] if cid in oracle else ['direct-full','module']
   for name in methods:
    reader=Reader(generator);generator.cap=192 if name=='module' else 512
    start=time.monotonic()
    try:
     if name=='module':
      previous={digest(d):(d,'source_only') for d in row['prior']}
      result=assess(previous,digest(row['incoming']),row['incoming'],DEFAULT_GOAL,reader,'context-review')
     else:result=direct.assess(row,reader,oracle[cid] if name=='direct-oracle' else None)
    except (RuntimeError,ValueError,KeyError) as exc:
     if 'out of memory' in str(exc).lower():raise
     result=dict(action='execution_error',error=str(exc))
    rec=dict(case=cid,method=name,result=result,calls=reader.calls,input_tokens=reader.input_tokens,output_tokens=reader.output_tokens,seconds=time.monotonic()-start)
    results[cid+'/'+name]=rec;log.write(json.dumps(rec,ensure_ascii=False)+'\n');log.flush()
    print(cid,name,result['action'],len(reader.calls),flush=True)
 report=dict(status='complete',job_id=args.job,input_sha256=sha256(blob).hexdigest(),
             model='Qwen2.5-14B-Instruct' if args.large else 'Qwen2.5-3B-Instruct',
             revision='cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8' if args.large else 'aa8e72537993ba99e69dfaafa59ed015b17504d1',
             devices=[torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],identity=generator.identity,
             peak_gpu_bytes=[torch.cuda.max_memory_allocated(i) for i in range(torch.cuda.device_count())],results=results)
 tmp=args.output.with_suffix('.tmp');tmp.write_text(json.dumps(report,ensure_ascii=False));tmp.replace(args.output)

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ['packets','model','output','job']:p.add_argument(n,type=Path if n in ('packets','output') else str)
 p.add_argument('--large',action='store_true');run(p.parse_args())
