"""Freeze a small trained-NLI attribution pass; no new QA model calls."""
from hashlib import sha256
import json
from pathlib import Path
import tarfile
from evaluation.cupmem.dispatch import validate_submission


def main():
    repo=Path(__file__).resolve().parents[2];campaign=repo.parent/'campaigns/speakermem-dev'
    version='cup-ref-attr-nli-v1';d=json.loads((campaign/'campaign-dispatch.json').read_text())
    assert version not in d['jobs'] and d['jobs']['cup-ref-attr-v1']['state']=='COMPLETED'
    prior=campaign/'source/cup-ref-attr-v1';dest=campaign/'source'/version;dest.mkdir(exist_ok=False)
    cfg=json.loads((prior/'config.json').read_text())
    names=list(cfg['code_sha256'])+['team_memory/reference_nli.py','evaluation/reference_qa/nli_replay.py']
    with tarfile.open(dest/'code.tar.gz','w:gz') as t:
        for name in names:t.add(repo/name,arcname=name)
    for name in ['inputs.json','prepare_nltk.py']:(dest/name).write_bytes((prior/name).read_bytes())
    for src,name in [('result.json','prior-result.json'),('calls.jsonl','prior-calls.jsonl')]:
        (dest/name).write_bytes((repo/'results/reference-qa/attribution-v1'/src).read_bytes())
    previous=json.loads((dest/'prior-result.json').read_text())
    expected=sum(len(s['result']['posthoc_citations'])*len(s['result']['citation_sources']) for r in previous['rows']
                 for s in r['steps'] if s['label']!='import')
    model=json.loads((repo/'results/reference-qa/attribution-v1/nli-model-plan.json').read_text())
    cfg.update(source_version=version,expected_new_calls=0,max_new_calls=0,expected_nli_pairs=expected,
        nli_model=model,nli_model_path='/local_datasets/pjw031003/capstone-shared-knowledge/models/nli-deberta-v3-base/'+model['revision'],
        replay_files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in ['prior-result.json','prior-calls.jsonl']},
        code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names})
    cfg['resources']['wall_minutes']=12
    cfg['execution_changes']['nli']='Published cross-encoder/nli-deberta-v3-base model and argmax labels. Keep TF-IDF choice if entailed, otherwise highest entailment-probability entailed alternative. Abstain if none. Original citations and all answer words preserved.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    remote=cfg['project']+'/source/sm-'+version
    script=(prior/'run.sbatch').read_text().replace('cup-ref-attr-v1',version).replace('00:20:00','00:12:00')
    script='\n'.join(l for l in script.splitlines() if ' -m pip install ' not in l and '/serve.py' not in l)+'\n'
    script+=f"export PYTHONPATH={cfg['reference_extras']}\n{cfg['python_client']} -u {remote}/code/evaluation/reference_qa/nli_replay.py {remote}\n"
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    out=repo/'results/reference-qa/attribution-nli-v1';out.mkdir(exist_ok=False)
    files=['run.sbatch','config.json','prepare_nltk.py','inputs.json','code.tar.gz','prior-result.json','prior-calls.jsonl']
    freeze=json.loads((repo/'results/reference-qa/attribution-v1/freeze.json').read_text())
    freeze.update(source_version=version,files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        validation='All20 answer strings must remain exact after removing newly inserted citation prefixes. Audit all NLI choices against original sources, retain19 earlier successes and the recovered conflict.',
        budget=dict(gpus=1,wall_minutes=12,approved_phase_cap_gpu_minutes=70,project_cap_unchanged=440),
        expected_new_calls=0,expected_nli_pairs=expected,
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 12 '+' '.join(files))
    freeze.pop('expected_branches',None)
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for name in ['config.json','run.sbatch']:(out/name).write_bytes((dest/name).read_bytes())
    print(freeze['submit_command']);print('NLI pairs',expected)


if __name__=='__main__':main()
