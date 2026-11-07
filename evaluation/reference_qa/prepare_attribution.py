"""Freeze AQA/ALCE candidate and fixed19-success gate before inference."""
from hashlib import sha256
import json
from pathlib import Path
import tarfile
from evaluation.cupmem.dispatch import validate_submission
from team_memory.reference_checked import missing_opposing_sources


def main():
    repo=Path(__file__).resolve().parents[2];campaign=repo.parent/'campaigns/speakermem-dev'
    version='cup-ref-attr-v1';d=json.loads((campaign/'campaign-dispatch.json').read_text())
    assert version not in d['jobs'] and d['jobs']['cup-ref-parse-v1']['state']=='COMPLETED'
    prior=campaign/'source/cup-ref-parse-v1';dest=campaign/'source'/version;dest.mkdir(exist_ok=False)
    cfg=json.loads((prior/'config.json').read_text())
    names=list(cfg['code_sha256'])+['team_memory/reference_attributed.py','evaluation/reference_qa/attribution_replay.py']
    names += [str(p.relative_to(repo)) for p in (repo/'team_memory/_vendor/alce').iterdir() if p.is_file()]
    with tarfile.open(dest/'code.tar.gz','w:gz') as t:
        for name in names:t.add(repo/name,arcname=name)
    for name in ['inputs.json','serve.py','service.py']:(dest/name).write_bytes((prior/name).read_bytes())
    (dest/'service.py').write_text((dest/'service.py').read_text().replace('reference_qa/replay.py','reference_qa/attribution_replay.py'))
    (dest/'prepare_nltk.py').write_bytes((campaign/'source/cup-ref-fix-v3/prepare_nltk.py').read_bytes())
    for src,name in [('result.json','prior-result.json'),('calls.jsonl','prior-calls.jsonl')]:
        (dest/name).write_bytes((repo/'results/reference-qa/parse-v1'/src).read_bytes())
    previous=json.loads((dest/'prior-result.json').read_text())
    branches=[dict(case_id=r['case_id'],label=s['label']) for r in previous['rows'] for s in r['steps']
              if s['label']!='import' and missing_opposing_sources(s['result'])]
    assert len(branches)==3
    remote=cfg['project']+'/source/sm-'+version
    cfg.update(source_version=version,client_seconds=240,serve_seconds=270,
        max_new_calls=3,expected_new_calls=3,profile='attributed',
        reference_extras=remote+'/reference-extra:'+cfg['reference_extras'],
        replay_files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in ['prior-result.json','prior-calls.jsonl']},
        code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names})
    cfg['resources']['wall_minutes']=20
    cfg['execution_changes']['attribution']='AQA section3.4.1/appendixA.1 with paraphrased figure1 example and Qwen; ALCE top1 TF-IDF citation addition, no overwrite. Not original3shot/model reproduction.'
    cfg['execution_changes']['acceptance']='Candidate must cite every previous source and previously missing opponent; this is structural only. Fixed20 semantic regression decides adoption.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script=(prior/'run.sbatch').read_text().replace('cup-ref-parse-v1',version).replace('00:09:00','00:20:00')
    setup=f'''export NLTK_DATA=/local_datasets/pjw031003/capstone-shared-knowledge/reference-nltk/$SLURM_JOB_ID
{cfg['python_client']} -u {remote}/prepare_nltk.py
{cfg['python_client']} -m pip install --disable-pip-version-check --no-input --no-deps --target {remote}/reference-extra scikit-learn==1.7.2
'''
    script=script.replace('unset OPENAI_API_KEY',setup+'unset OPENAI_API_KEY')
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    out=repo/'results/reference-qa/attribution-v1';out.mkdir(exist_ok=False)
    files=['run.sbatch','config.json','serve.py','service.py','prepare_nltk.py','inputs.json','code.tar.gz','prior-result.json','prior-calls.jsonl']
    freeze=json.loads((repo/'results/reference-qa/parse-v1/freeze.json').read_text())
    freeze.update(source_version=version,profile='attributed',
        files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        validation='All20 outputs; fixed19 correct answers and evidence must remain. All new citations judged against originals. Conflict must retain both source answers without unrelated answers.',
        budget=dict(gpus=1,wall_minutes=20,existing_phase_cap_gpu_minutes=50,requested_phase_cap_gpu_minutes=70,project_cap_unchanged=440),
        expected_new_calls=3,expected_branches=branches,
        checked_reference_sha256={n:sha256((repo/'results/reference-qa/parse-v1'/n).read_bytes()).hexdigest() for n in ['result.json','ratings.json']},
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 20 '+' '.join(files))
    freeze.pop('changed_labels',None)
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for name in ['config.json','run.sbatch']:(out/name).write_bytes((dest/name).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
