"""Freeze full-context quote attribution before Qwen inference; no answer key in actor."""
from hashlib import sha256
import json,tarfile
from pathlib import Path
from evaluation.cupmem.dispatch import validate_submission


def main():
    repo=Path(__file__).resolve().parents[2];campaign=repo.parent/'campaigns/speakermem-dev'
    version='cup-ref-quote-v1';ledger=json.loads((campaign/'campaign-dispatch.json').read_text())
    assert version not in ledger['jobs'] and ledger['jobs']['cup-ref-attr-nli-v2']['state']=='COMPLETED'
    prior=campaign/'source/cup-ref-attr-v1';dest=campaign/'source'/version;dest.mkdir(exist_ok=False)
    cfg=json.loads((prior/'config.json').read_text());names=list(cfg['code_sha256'])
    names+=['team_memory/reference_quotes.py','evaluation/reference_qa/quote_replay.py']
    names+=[str(p.relative_to(repo)) for p in (repo/'team_memory/_vendor/langchain_citation').iterdir() if p.is_file()]
    with tarfile.open(dest/'code.tar.gz','w:gz') as t:
        for name in names:t.add(repo/name,arcname=name)
    for name in ['inputs.json','serve.py','service.py','prepare_nltk.py']:(dest/name).write_bytes((prior/name).read_bytes())
    (dest/'service.py').write_text((dest/'service.py').read_text().replace('attribution_replay.py','quote_replay.py'))
    for src,name in [('result.json','prior-result.json'),('calls.jsonl','prior-calls.jsonl')]:
        (dest/name).write_bytes((repo/'results/reference-qa/attribution-v1'/src).read_bytes())
    remote=cfg['project']+'/source/sm-'+version
    cfg.update(source_version=version,client_seconds=180,serve_seconds=200,max_new_calls=14,expected_new_calls=14,
        reference_extras=cfg['reference_extras'].replace('sm-cup-ref-attr-v1','sm-'+version),
        replay_files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in ['prior-result.json','prior-calls.jsonl']},
        code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names})
    cfg['resources']['wall_minutes']=6
    cfg['execution_changes']['attribution']='LangChain0.3.27 FactWithEvidence schema and exact quote prompt adapted to unchanged sentences, full answer context, literal matching and insertion only. ALCE TF-IDF and NLI variants rejected.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script=(prior/'run.sbatch').read_text().replace('cup-ref-attr-v1',version).replace('00:20:00','00:06:00')
    script=script.replace('export PYTHONDONTWRITEBYTECODE=1','export PYTHONUTF8=1 PYTHONIOENCODING=utf-8\nexport PYTHONDONTWRITEBYTECODE=1')
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    out=repo/'results/reference-qa/quote-v1';out.mkdir(exist_ok=False)
    files=['run.sbatch','config.json','serve.py','service.py','prepare_nltk.py','inputs.json','code.tar.gz','prior-result.json','prior-calls.jsonl']
    freeze=json.loads((repo/'results/reference-qa/attribution-v1/freeze.json').read_text())
    freeze.update(source_version=version,files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        budget=dict(gpus=1,wall_minutes=6,approved_phase_cap_gpu_minutes=70,project_cap_unchanged=440),
        expected_new_calls=14,validation='Fixed20 required answers and original evidence; all19 previous successes must remain. Review every new quote/citation, both known gaps, no new citation errors.',
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 6 '+' '.join(files))
    freeze.pop('expected_branches',None)
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for name in ['config.json','run.sbatch']:(out/name).write_bytes((dest/name).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
