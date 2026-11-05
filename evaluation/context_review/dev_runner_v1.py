import argparse
from hashlib import sha256
import json
from pathlib import Path
import torch
from base_experiment import Reader
from diagnostic_reader import read_context
from team_memory.writer import local_generator

p=argparse.ArgumentParser()
for k in ('packets','model','output','job'):p.add_argument(k)
p.add_argument('--count',type=int);p.add_argument('--max-new-tokens',type=int)
a=p.parse_args();blob=Path(a.packets).read_bytes();rows=json.loads(blob)
assert len(rows)==a.count and torch.cuda.is_available()
q=Reader(local_generator(a.model,max_new_tokens=192));results={}
for row in rows:
    start=len(q.used)
    result=read_context(row['base'],row['passages'],q)
    results[row['id']]=dict(result=result,used=q.used[start:])
    print(row['id'],len(q.calls),flush=True)
d=dict(status='complete',job_id=a.job,input_sha256=sha256(blob).hexdigest(),device=torch.cuda.get_device_name(),
       model='Qwen2.5-3B-Instruct',revision='aa8e72537993ba99e69dfaafa59ed015b17504d1',results=results,calls=q.calls)
Path(a.output).write_text(json.dumps(d,ensure_ascii=False))
