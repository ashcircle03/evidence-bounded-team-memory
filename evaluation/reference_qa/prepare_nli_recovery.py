"""UTF-8 persistence repair only; preserve classifier, inputs and fixed criteria."""
from hashlib import sha256
import json,tarfile
from pathlib import Path
from evaluation.cupmem.dispatch import validate_submission


def main():
    repo=Path(__file__).resolve().parents[2];campaign=repo.parent/'campaigns/speakermem-dev'
    version='cup-ref-attr-nli-v2';ledger=json.loads((campaign/'campaign-dispatch.json').read_text())
    assert version not in ledger['jobs'] and ledger['jobs']['cup-ref-attr-nli-v1']['state']=='FAILED'
    prior=campaign/'source/cup-ref-attr-nli-v1';dest=campaign/'source'/version;dest.mkdir(exist_ok=False)
    cfg=json.loads((prior/'config.json').read_text());names=list(cfg['code_sha256'])
    for name,h in cfg['code_sha256'].items():
        if name!='evaluation/reference_qa/nli_replay.py':assert sha256((repo/name).read_bytes()).hexdigest()==h
    with tarfile.open(dest/'code.tar.gz','w:gz') as t:
        for name in names:t.add(repo/name,arcname=name)
    for name in ['inputs.json','prepare_nltk.py','prior-result.json','prior-calls.jsonl']:(dest/name).write_bytes((prior/name).read_bytes())
    cfg.update(source_version=version,code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names})
    cfg['resources']['wall_minutes']=8
    cfg['execution_changes']['encoding_recovery']='Explicit UTF-8 JSON and JSONL I/O; no classifier/prompt/input/ranking change. Failed119952 preserved.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script=(prior/'run.sbatch').read_text().replace('cup-ref-attr-nli-v1',version).replace('00:12:00','00:08:00')
    script=script.replace('export PYTHONDONTWRITEBYTECODE=1','export PYTHONUTF8=1 PYTHONIOENCODING=utf-8\nexport PYTHONDONTWRITEBYTECODE=1')
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    out=repo/'results/reference-qa/attribution-nli-v2';out.mkdir(exist_ok=False)
    files=['run.sbatch','config.json','prepare_nltk.py','inputs.json','code.tar.gz','prior-result.json','prior-calls.jsonl']
    freeze=json.loads((repo/'results/reference-qa/attribution-nli-v1/freeze.json').read_text())
    freeze.update(source_version=version,files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        budget=dict(gpus=1,wall_minutes=8,approved_phase_cap_gpu_minutes=70,project_cap_unchanged=440),
        only_changed_source='evaluation/reference_qa/nli_replay.py: UTF-8 result persistence',
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 8 '+' '.join(files))
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for name in ['config.json','run.sbatch']:(out/name).write_bytes((dest/name).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
