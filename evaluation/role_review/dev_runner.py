import argparse
import json
from hashlib import sha256
from pathlib import Path
import torch
from base_experiment import Reader
from team_memory.writer import local_generator
from team_memory.role_review import audit,revise,valid_ledger

p=argparse.ArgumentParser()
for k in ("packets","model","output","job"):p.add_argument(k)
p.add_argument("--count",type=int);p.add_argument("--max-new-tokens",type=int)
a=p.parse_args()
raw=Path(a.packets).read_bytes()
rows=json.loads(raw)
assert len(rows)==a.count and torch.cuda.is_available()
q=Reader(local_generator(a.model,max_new_tokens=96))
results={}
for row in rows:
    r=row["result"]
    checks=[audit(c,[r["previous"],r["incoming"]],q) for c in row["claims"]]
    fixed=revise(r,q)
    results[row["id"]]=dict(checks=checks,revised=fixed,ledger_valid=valid_ledger(fixed))
    print(row["id"],len(q.calls),flush=True)
d=dict(status="complete",job_id=a.job,input_sha256=sha256(raw).hexdigest(),device=torch.cuda.get_device_name(),
       model="Qwen2.5-3B-Instruct",revision="aa8e72537993ba99e69dfaafa59ed015b17504d1",results=results,calls=q.calls)
Path(a.output).write_text(json.dumps(d,ensure_ascii=False))
