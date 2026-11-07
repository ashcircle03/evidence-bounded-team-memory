"""Prepare, but do not submit or enlarge budgets, a same-code20-minute recovery."""
from pathlib import Path
import json,hashlib
from evaluation.cupmem.dispatch import validate_submission


def main():
    repo=Path(__file__).resolve().parents[2];campaign=repo.parent/'campaigns/speakermem-dev'
    version='cup-ref-quote-v2';ledger=json.loads((campaign/'campaign-dispatch.json').read_text())
    assert version not in ledger['jobs'] and ledger['jobs']['cup-ref-quote-v1']['state']=='TIMEOUT'
    prior=campaign/'source/cup-ref-quote-v1';dest=campaign/'source'/version;dest.mkdir(exist_ok=False)
    freeze=json.loads((repo/'results/reference-qa/quote-v1/freeze.json').read_text())
    files=list(freeze['files_sha256'])
    for n in files:
        assert hashlib.sha256((prior/n).read_bytes()).hexdigest()==freeze['files_sha256'][n]
        (dest/n).write_bytes((prior/n).read_bytes())
    cfg=json.loads((dest/'config.json').read_text())
    cfg.update(source_version=version,reference_extras=cfg['reference_extras'].replace('sm-cup-ref-quote-v1','sm-'+version))
    cfg['resources']['wall_minutes']=20
    cfg['execution_changes']['timeout_recovery']='Same model, actor code, prompts, inputs, replay records and criteria; walltime20 rather than6 minutes. Requires explicit budget approval before submission.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script=(dest/'run.sbatch').read_text().replace('cup-ref-quote-v1',version).replace('00:06:00','00:20:00')
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    out=repo/'results/reference-qa/quote-v2';out.mkdir(exist_ok=False)
    freeze.update(source_version=version,files_sha256={n:hashlib.sha256((dest/n).read_bytes()).hexdigest() for n in files},
        budget=dict(gpus=1,wall_minutes=20,approval_pending=True,requested_phase_cap_gpu_minutes=90,requested_cup_cap_gpu_minutes=460,requested_campaign_cap_gpu_minutes=760),
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 20 '+' '.join(files))
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for n in ['config.json','run.sbatch']:(out/n).write_bytes((dest/n).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
