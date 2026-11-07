"""Resume unexecuted native inputs after the null-group adapter failure."""
from hashlib import sha256
import json,tarfile
from pathlib import Path
from evaluation.cupmem.dispatch import validate_submission


def main():
    root=Path(__file__).resolve().parents[3];camp=root.parent/'campaigns/speakermem-dev'
    prior=camp/'source/cup-ref-claims-v2';old=root/'results/reference-qa/claims-v2'
    version='cup-ref-claims-v3';dest=camp/'source'/version;dest.mkdir(exist_ok=False)
    cfg=json.loads((prior/'config.json').read_text());ledger=json.loads((camp/'campaign-dispatch.json').read_text())
    assert ledger['jobs']['cup-ref-claims-v2']['state']=='FAILED' and version not in ledger['jobs']
    for n,h in cfg['code_sha256'].items():
        if n!='evaluation/reference_qa/expanded/run.py':assert sha256((root/n).read_bytes()).hexdigest()==h,n
    for n,h in cfg['data_sha256'].items():assert sha256((prior/n).read_bytes()).hexdigest()==h,n
    for n in ['config.json','serve.py','service.py','prepare_nltk.py','download.py','manifest.json','PROTOCOL.md','regressions.json','run.sbatch']:
        (dest/n).write_bytes((prior/n).read_bytes())
    (dest/'run.sbatch').write_text((dest/'run.sbatch').read_text().replace('cup-ref-claims-v2',version));validate_submission((dest/'run.sbatch').read_text(),1)
    for src,n in [('result.json','prior-result.json'),('calls.jsonl','prior-calls.jsonl')]:
        (dest/n).write_bytes((old/src).read_bytes())
    prev=json.loads((dest/'prior-result.json').read_text());calls=(dest/'prior-calls.jsonl').read_text().splitlines()
    assert len(prev['rows'])==36 and prev['calls']==len(calls)
    assert [json.loads(c)['id'] for c in calls]==list(range(len(calls)))
    cfg.update(source_version=version,resume_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in ['prior-result.json','prior-calls.jsonl']})
    cfg['code_sha256']['evaluation/reference_qa/expanded/run.py']=sha256((root/'evaluation/reference_qa/expanded/run.py').read_bytes()).hexdigest()
    cfg['execution_changes']['recovery']='Skip native null message groups; resume36 completed outputs with byte-identical physical calls. No actor, prompt, question, seed, model, retrieval or score changes.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    with tarfile.open(dest/'code.tar.gz','w:gz') as tar:
        for n in cfg['code_sha256']:tar.add(root/n,arcname=n)
    files=['run.sbatch','config.json','serve.py','service.py','prepare_nltk.py','download.py','manifest.json','PROTOCOL.md','regressions.json','code.tar.gz','prior-result.json','prior-calls.jsonl']
    out=root/'results/reference-qa/claims-v3';out.mkdir(exist_ok=False)
    freeze=json.loads((old/'freeze.json').read_text())
    freeze.update(source_version=version,submission_status='authorized_recovery_within_existing60GPUminutes',
        parent='claims-v2',reused_job_id='120041',reused_outputs=36,reused_calls=len(calls),
        files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        submit_command='python -m evaluation.cupmem.dispatch submit '+version+' 1 45 '+' '.join(files))
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for n in ['config.json','run.sbatch','PROTOCOL.md']:(out/n).write_bytes((dest/n).read_bytes())
    for n in ['budget-approval.json','review-work.json','reporting-freeze.json']:(out/n).write_bytes((old/n).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
