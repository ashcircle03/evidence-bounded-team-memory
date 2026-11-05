"""Audit the actual jobs, frozen payloads, paired prompts, and historical QA parser."""
from hashlib import sha256
import json
from pathlib import Path
import zipfile
from .build import ROOT,HERE,write
from evaluation.pair_selection.qa import packets
from evaluation.pair_selection.qa_replay import historical

OUT=ROOT/'results/design_review'
CAMPAIGN=ROOT.parent/'campaigns/speakermem-dev'
JOBS={'design-small-v1':'small.json','design-large-v3':'large.json',
      'design-large-factorial-v1':'large-factorial.json',
      'design-oracle-repair-v1':'oracle-repair.json','design-qa-v1':'qa-generations.json',
      'design-pull-v1':'integration.json'}

def verify():
 ledger=json.loads((CAMPAIGN/'campaign-dispatch.json').read_text());runs=[]
 for path,h in json.loads((HERE/'freeze.json').read_text())['files'].items():assert sha256((ROOT/path).read_bytes()).hexdigest()==h,path
 OUT.mkdir(exist_ok=True)
 for version,name in JOBS.items():
  j=ledger['jobs'][version];assert (j['state'],j['exit_code'],j.get('verified'))==('COMPLETED','0:0',True),version
  p=CAMPAIGN/'results'/('sm-'+j['job_id']+'.json');d=json.loads(p.read_text())
  assert d['status']=='complete' and str(d['job_id'])==j['job_id']
  src=CAMPAIGN/'source'/version
  for fn,h in j['source_sha256'].items():assert sha256((src/fn).read_bytes()).hexdigest()==h,(version,fn)
  assert d['input_sha256']==j['source_sha256']['packets.json']
  if version!='design-qa-v1':
   with zipfile.ZipFile(src/'infer.py') as z:
    for p0 in (ROOT/'team_memory').glob('*.py'):assert z.read('team_memory/'+p0.name)==p0.read_bytes()
    if version!='design-pull-v1':
     assert z.read('direct.py')==(HERE/'direct.py').read_bytes()
     runner='factorial_runner.py' if version=='design-large-factorial-v1' else 'runner.py'
     assert z.read('__main__.py')==(HERE/runner).read_bytes()
  (OUT/name).write_bytes(p.read_bytes())
  runs.append(dict(source=version,job=j['job_id'],state=j['state'],exit_code=j['exit_code'],
                   elapsed_seconds=j['elapsed_seconds'],gpus=j['gpus'],wall_minutes=j['wall_minutes'],
                   usage=j['usage'],source_sha256=j['source_sha256'],result_sha256=sha256(p.read_bytes()).hexdigest()))
 small=json.loads((OUT/'small.json').read_text());large=json.loads((OUT/'large.json').read_text());repair=json.loads((OUT/'oracle-repair.json').read_text())
 assert len(small['results'])==150 and len(large['results'])==60 and len(repair['results'])==6
 factorial=json.loads((OUT/'large-factorial.json').read_text());assert len(factorial['results'])==90
 assert not set(large['results']) & set(factorial['results'])
 large['results'].update(factorial['results']);assert len(large['results'])==150
 assert small['revision']=='aa8e72537993ba99e69dfaafa59ed015b17504d1'
 assert large['revision']=='cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8'
 assert factorial['revision']==large['revision'] and factorial['identity']==large['identity']
 # Same direct prompts, including the repaired two negative oracle cases.
 combined=dict(small['results'])
 for uid,r in repair['results'].items():
  if r['method']=='direct-oracle':combined[uid]=r
 paired={}
 for uid,r in large['results'].items():
  if r['method']=='module':continue
  a=combined[uid]['calls'];b=r['calls'];assert len(a)==len(b)==1
  paired[uid]=all(a[0][f]==b[0][f] for f in ('system','content'))
 assert all(paired.values())
 qa=json.loads((OUT/'qa-generations.json').read_text());assert len(qa['calls'])==136
 historical_rows=historical(packets()[1],{r['id']:r for r in qa['calls']})
 write(OUT/'qa-historical.json',historical_rows)
 integration=json.loads((OUT/'integration.json').read_text());pulls={}
 for uid,q in integration['qa'].items():
  before,after=[x['out'] for x in q['answers']]
  pulls[uid]=dict(same=before==after,pending=[r['status'] for r in q['context']],before=before,after=after)
 checks=dict(frozen_files_unchanged=True,paired_direct_prompts=paired,historical_qa_n=len(historical_rows),
             historical_qa_same=sum(r['identical'] for r in historical_rows.values()),pulls=pulls)
 checks['historical_qa_model']='Qwen2.5-3B-Instruct'
 checks['design_rows_per_model']={'3b':len(combined),'14b':len(large['results'])}
 checks['model_identity']={'3b':small['identity'],'14b':large['identity']}
 write(OUT/'checks.json',checks)
 jobgroup=[j for v,j in ledger['jobs'].items() if v.startswith('design-')]
 write(OUT/'runs.json',dict(jobs=runs,all_attempts=jobgroup,
      gpu_seconds=sum(j.get('elapsed_seconds',0)*j['gpus'] for j in jobgroup),
      cpu_only_seconds=sum(j.get('elapsed_seconds',0) for j in jobgroup if not j['gpus']),
      cumulative_gpu_seconds=sum(j.get('elapsed_seconds',0)*j['gpus'] for j in ledger['jobs'].values()),
      cumulative_cpu_only_seconds=sum(j.get('elapsed_seconds',0) for j in ledger['jobs'].values() if not j['gpus']),
      budget=ledger['budget']))
 print('verified',len(runs),'inference jobs; paired prompts',len(paired),'QA',checks['historical_qa_same'],'/',len(historical_rows))

if __name__=='__main__':verify()
