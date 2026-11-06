"""Package a fresh, bounded team-profile run; never overwrite a submitted actor."""
from hashlib import sha256
import json
from pathlib import Path
import tarfile

from evaluation.cupmem.dispatch import validate_submission


def main():
    repo = Path(__file__).resolve().parents[2]
    campaign = repo.parent/'campaigns/speakermem-dev'
    version = 'cup-ref-fix-v1'
    ledger = json.loads((campaign/'campaign-dispatch.json').read_text())
    if version in ledger['jobs']:
        raise RuntimeError('Dispatched version is immutable')
    dest = campaign/'source'/version
    dest.mkdir(exist_ok=False)
    previous = repo/'results/reference-qa/run-v2'
    cfg = json.loads((previous/'config.json').read_text())
    remote = cfg['project']+'/source/sm-'+version
    names = ['team_memory/__init__.py','team_memory/store.py','team_memory/reference_qa.py',
             'team_memory/reference_prompts.py','evaluation/reference_qa/__init__.py',
             'evaluation/reference_qa/run.py']
    with tarfile.open(dest/'code.tar.gz','w:gz') as tar:
        for name in names:
            tar.add(repo/name, arcname=name)
    blob = (repo/'evaluation/cupmem/practical/legacy.json').read_bytes()
    (dest/'inputs.json').write_bytes(blob)
    cfg.update(source_version=version, profile='team', client_seconds=720, serve_seconds=780,
        scope='Same exposed20 QA; compare against frozen15/20 reference-v2',
        code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names},
        input_sha256=sha256(blob).hexdigest(), reference_extras=remote+'/reference-extra',
        max_calls=60, execution_changes=dict(model='Unchanged Qwen3-8B nonthinking',
            retrieval='Official BM25 top4 + original dense top4; official RRF union top8, num_queries1',
            metadata='record_author and recorded_at visible to reader, unchanged dense embedding text',
            qa='ConflictScore Table14 balanced prompt adapted to record QA + upstream CitationQueryEngine',
            splitter='Original SentenceSplitter512/64; citation1024/0 retains metadata header',
            max_context=32768,max_output_tokens=1024,native_writer=False,approval_semantics='unsupported',
            environment='Read-only v1 client environment plus isolated BM25 extras; private NLTK data'))
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    prior = campaign/'source/cup-ref-qa-v2'
    (dest/'serve.py').write_bytes((prior/'serve.py').read_bytes())
    service = (prior/'service.py').read_text().replace("os.execv(c['python_client']", 
        "os.environ['PYTHONPATH']=c['reference_extras']\nos.execv(c['python_client']")
    (dest/'service.py').write_text(service)
    (dest/'prepare_nltk.py').write_bytes((previous/'prepare_nltk.py').read_bytes())
    (dest/'requirements-extra.txt').write_text(
        'llama-index-retrievers-bm25==0.8.0\nbm25s==0.3.16\nPyStemmer==2.2.0.3\n')
    script = (previous/'run.sbatch').read_text().replace('cup-ref-qa-v2', version)
    install = f"timeout 120 {cfg['python_client']} -m pip install --disable-pip-version-check --no-deps --target {remote}/reference-extra -r {remote}/requirements-extra.txt\n"
    script = script.replace('export NLTK_DATA=', install+'export NLTK_DATA=')
    validate_submission(script,1)
    (dest/'run.sbatch').write_text(script)
    files = ['run.sbatch','config.json','serve.py','service.py','inputs.json','code.tar.gz',
             'requirements-extra.txt','prepare_nltk.py']
    out = repo/'results/reference-qa/fix-v1'
    out.mkdir(exist_ok=False)
    freeze = dict(source_version=version, profile='team', input_sha256=cfg['input_sha256'],
        files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        previous_result_sha256=sha256((previous/'result.json').read_bytes()).hexdigest(),
        previous_ratings_sha256=sha256((previous/'ratings.json').read_bytes()).hexdigest(),
        key_sha256=sha256((repo/'evaluation/cupmem/practical/legacy-key.json').read_bytes()).hexdigest(),
        primary='Answer correct AND citations support answer AND no unsupported extra claims',
        target=dict(total=20,previous_successes_to_preserve=15,failures_to_recover=5),
        interpretation='Exposed development repair. No holdout or independent human evaluation.',
        model_input='Original histories and questions only; answer keys and ratings excluded',
        budget=dict(gpus=1,wall_minutes=20,existing_phase_cap_gpu_minutes=30),
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 20 '+' '.join(files))
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for n in ['config.json','run.sbatch','requirements-extra.txt']:
        (out/n).write_bytes((dest/n).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__': main()
