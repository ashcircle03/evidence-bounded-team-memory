"""Preserve the checked actor and inputs; use the user's added GPU allowance."""
from hashlib import sha256
import json
from pathlib import Path
from evaluation.cupmem.dispatch import validate_submission


def main():
    repo = Path(__file__).resolve().parents[2]
    campaign = repo.parent/'campaigns/speakermem-dev'
    data = json.loads((campaign/'campaign-dispatch.json').read_text())
    previous = data['jobs']['cup-ref-fix-v2']
    assert previous['state'] in ('TIMEOUT','FAILED','OUT_OF_MEMORY','COMPLETED')
    # This script never cancels/moves a running allocation. Submission remains a
    # separate operation with queue, lock, intent and cumulative-budget checks.
    version = 'cup-ref-fix-v3';assert version not in data['jobs']
    prior = campaign/'source/cup-ref-fix-v2'
    dest = campaign/'source'/version;dest.mkdir(exist_ok=False)
    files = ['run.sbatch','config.json','serve.py','service.py','inputs.json','code.tar.gz','prepare_nltk.py']
    for name in files:(dest/name).write_bytes((prior/name).read_bytes())
    cfg = json.loads((dest/'config.json').read_text())
    cfg.update(source_version=version,client_seconds=600,serve_seconds=660)
    cfg['resources']['wall_minutes']=20
    cfg['execution_changes']['recovery']='User explicitly approved additional20 GPUminutes; identical actor, model, inputs, source grouping, judge and prompts. Cache/startup headroom only.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script = (dest/'run.sbatch').read_text().replace('cup-ref-fix-v2',version).replace('00:09:00','00:20:00')
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    out=repo/'results/reference-qa/fix-v3';out.mkdir(exist_ok=False)
    freeze=json.loads((repo/'results/reference-qa/fix-v2/freeze.json').read_text())
    freeze.update(source_version=version,
        files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        prior_attempt=previous['job_id'],actor_unchanged_from='cup-ref-fix-v2',
        budget=dict(gpus=1,wall_minutes=20,existing_phase_cap_gpu_minutes=50,additional20_user_approved=True),
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 20 '+' '.join(files))
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for name in ['config.json','run.sbatch']:(out/name).write_bytes((dest/name).read_bytes())
    (out/'reference-provenance.json').write_bytes((repo/'results/reference-qa/fix-v2/reference-provenance.json').read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
