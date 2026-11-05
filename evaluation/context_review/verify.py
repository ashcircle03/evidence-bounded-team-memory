"""Verify submitted archives and immutable source citations before aggregating scores."""
from hashlib import sha256
from pathlib import Path
import zipfile
from evaluation.decision_records.build import ROOT,WORK,read,save
from evaluation.contrast_review.score import run
from evaluation.pair_selection.qa import packets
from evaluation.pair_selection.qa_replay import historical
from team_memory.context_review import valid_evidence,revise

HERE=Path(__file__).parent
OUT=ROOT/'results/context_review'
JOBS={'records-read-v30':'development.json','records-read-v31':'qa-generations.json',
      'records-read-v32':'development-v2.json','records-read-v34':'development-v3.json',
      'records-read-v33':'comparison.json','records-read-v35':'integration.json'}

def verify():
    base=WORK/'campaigns/speakermem-dev'; ledger=read(base/'campaign-dispatch.json');runs=[]
    for version,name in JOBS.items():
        j=ledger['jobs'][version];output=read(OUT/name)
        assert (j['state'],j['exit_code'],j['verified'])==('COMPLETED','0:0',True)
        assert output['status']=='complete' and str(output['job_id'])==j['job_id']
        assert output['input_sha256']==j['source_sha256']['packets.json']
        folder=base/'source'/version
        for fn,h in j['source_sha256'].items():assert sha256((folder/fn).read_bytes()).hexdigest()==h
        if version in ('records-read-v34','records-read-v33','records-read-v35'):
            with zipfile.ZipFile(folder/'infer.py') as z:
                for p in (ROOT/'team_memory').glob('*.py'):assert z.read('team_memory/'+p.name)==p.read_bytes()
        runs.append(dict(source=version,job=j['job_id'],state=j['state'],exit_code=j['exit_code'],
                         elapsed_seconds=j['elapsed_seconds'],wall_minutes=j['wall_minutes'],gpu=j['gpus'],
                         max_rss=[x['MaxRSS'] for x in j['usage'] if x['JobID'].endswith('.batch')],
                         source_sha256=j['source_sha256'],result=name,result_sha256=sha256((OUT/name).read_bytes()).hexdigest()))
    for p,h in read(HERE/'freeze.json')['files'].items():assert sha256((ROOT/p).read_bytes()).hexdigest()==h
    save(OUT/'runs.json',dict(jobs=runs,gpu_seconds=sum(j['elapsed_seconds'] for j in runs),
         completed_gpu_seconds=sum(j['elapsed_seconds'] for j in ledger['jobs'].values() if j['gpus'] and 'elapsed_seconds' in j),
         unaccounted_gpu_jobs=[j['job_id'] for j in ledger['jobs'].values() if j['gpus'] and 'elapsed_seconds' not in j],
         cap_gpu_minutes=ledger['budget']['single_gpu_minutes']))
    d=read(OUT/'comparison.json');key=read(HERE/'key.json');order={}
    for cid,methods in d['results'].items():
        r=methods['context-review']['result']
        if r['action'] in ('reassess','retest'):assert valid_evidence(r)
        if 'context-reversed' in methods:
            order[cid]=methods['context-reversed']['result']==r
    qa=historical(packets()[1],{r['id']:r for r in read(OUT/'qa-generations.json')['calls']})
    save(OUT/'qa-historical.json',qa)
    pulls={}
    for cid,v in d['qa'].items():
        before,after=[x['out'] for x in v['answers']]
        pulls[key[cid]['topic']]=dict(same=before==after,context=[x['status'] for x in v['context']],
                before=[a['answer'] for a in before.get('answers',[])],after=[a['answer'] for a in after.get('answers',[])])
    save(OUT/'checks.json',dict(order=order,historical_qa_same=sum(v['identical'] for v in qa.values()),
                              historical_qa_n=len(qa),matched_batch_prompts=len(read(OUT/'qa-generations.json')['calls']),pulls=pulls))
    integration=read(OUT/'integration.json')
    integration_checks={}
    for cid, q in integration['qa'].items():
        output=integration['results'][cid]['context-review']['result']
        if output['action'] in ('reassess','retest'):assert valid_evidence(output)
        integration_checks[cid]=dict(action=output['action'],
            identical=q['answers'][0]['out']==q['answers'][1]['out'],
            pending=[r['status'] for r in q['context']],
            answer=[a['answer'] for a in q['answers'][1]['out'].get('answers',[])])
    save(OUT/'integration-checks.json',integration_checks)
    run(HERE,OUT)

if __name__=='__main__':verify()
