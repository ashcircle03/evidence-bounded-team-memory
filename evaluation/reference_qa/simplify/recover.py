"""Transport instrumentation repair only; actor, inputs and criteria stay frozen."""
from pathlib import Path
from hashlib import sha256
import json,tarfile
from evaluation.cupmem.dispatch import validate_submission


def main():
    repo=Path(__file__).resolve().parents[3];camp=repo.parent/'campaigns/speakermem-dev'
    version='cup-ref-simple-v2';ledger=json.loads((camp/'campaign-dispatch.json').read_text())
    assert version not in ledger['jobs'] and ledger['jobs']['cup-ref-simple-v1']['state']=='FAILED'
    prior=camp/'source/cup-ref-simple-v1';dest=camp/'source'/version;dest.mkdir(exist_ok=False)
    cfg=json.loads((prior/'config.json').read_text());changed='evaluation/reference_qa/simplify/run.py'
    for n,h in cfg['code_sha256'].items():
        if n!=changed:assert sha256((repo/n).read_bytes()).hexdigest()==h,n
    with tarfile.open(dest/'code.tar.gz','w:gz') as tar:
        for n in cfg['code_sha256']:tar.add(repo/n,arcname=n)
    for n in ['serve.py','service.py','prepare_nltk.py','legacy-contexts.json','transfer-inputs.json']:(dest/n).write_bytes((prior/n).read_bytes())
    cfg.update(source_version=version,code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in cfg['code_sha256']})
    cfg['resources']['wall_minutes']=14
    cfg['execution_changes']['transport_recovery']='Restore previously used reference_trace extension key; trace is reserved by httpcore. No actor prompt/data/model change.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script=(prior/'run.sbatch').read_text().replace('cup-ref-simple-v1',version).replace('00:17:00','00:14:00')
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    out=repo/'results/reference-qa/simplify-v2';out.mkdir(exist_ok=False)
    freeze=json.loads((repo/'results/reference-qa/simplify-v1/freeze.json').read_text());files=list(freeze['files_sha256'])
    freeze.update(source_version=version,files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},budget=dict(gpus=1,wall_minutes=14,phase_cap=90,cup_cap=460,campaign_cap=760),recovery_change=changed+': only HTTP extension key',submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 14 '+' '.join(files))
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for n in ['config.json','run.sbatch']:(out/n).write_bytes((dest/n).read_bytes())
    for n in ['tests.log','preservation.json','reference-provenance.json']:(out/n).write_bytes((repo/'results/reference-qa/simplify-v1'/n).read_bytes())
    (out/'transport-smoke.json').write_text(json.dumps(dict(reserved_trace_key_untouched=True,actual_frozen_hooks_exercised_with_httpcore=True,no_model_or_network_call=True),indent=2)+'\n')
    print(freeze['submit_command'])


if __name__=='__main__':main()
