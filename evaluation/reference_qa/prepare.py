"""Package the existing Slurm/vLLM launcher with the reference QA client; no submission."""
from hashlib import sha256
import json
from pathlib import Path
import tarfile

from evaluation.cupmem.dispatch import validate_submission


def main():
    repo = Path(__file__).resolve().parents[2]
    campaign = repo.parent/'campaigns/speakermem-dev'
    version = 'cup-ref-qa-v1'
    ledger = json.loads((campaign/'campaign-dispatch.json').read_text())
    if version in ledger['jobs']:
        raise RuntimeError('Do not overwrite a dispatched version')
    dest = campaign/'source'/version; dest.mkdir(exist_ok=True)
    prior = campaign/'source/cup-practical-legacy-git-a-v1'
    cfg = json.loads((prior/'config.json').read_text())
    remote = cfg['project']+'/source/sm-'+version
    names = ['team_memory/__init__.py','team_memory/store.py','team_memory/reference_qa.py',
             'evaluation/reference_qa/__init__.py','evaluation/reference_qa/run.py']
    with tarfile.open(dest/'code.tar.gz','w:gz') as tar:
        for n in names: tar.add(repo/n, arcname=n)
    blob = (repo/'evaluation/cupmem/practical/legacy.json').read_bytes()
    (dest/'inputs.json').write_bytes(blob)
    (dest/'requirements-reference.txt').write_bytes((repo/'requirements-reference.txt').read_bytes())
    cfg.update(source_version=version, scope='Reference source QA on20 exposed development questions',
        resources=dict(gpus=1,cpus=8,ram_gb=48,wall_minutes=30), client_seconds=1380,serve_seconds=1450,
        max_calls=60,input_sha256=sha256(blob).hexdigest(),
        code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names},
        python_client=remote+'/reference-env/bin/python', execution_changes=dict(
            model='Qwen3-8B non-thinking', qa='upstream CitationQueryEngine prompts',
            splitter='SentenceSplitter512/64 with Qwen tokenizer',
            retrieval='VectorStoreIndex top4; same local encoder',max_output_tokens=1024,
            max_context=32768,native_writer=False,approval_semantics='unsupported'))
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    server = (repo/'evaluation/cupmem/practical/server.py').read_text()
    server = server.replace("reason='paired practical service run completed'", "reason='reference source QA completed'")
    server = server.replace("'cup-practical-'+record['job_id']+'.json'", "'cup-reference-'+record['job_id']+'.json'")
    (dest/'serve.py').write_text(server)
    (dest/'service.py').write_text("import json, os\nfrom pathlib import Path\np=Path(__file__).resolve().parent\nc=json.loads((p/'config.json').read_text())\nos.execv(c['python_client'], [c['python_client'], '-u', str(p/'code/evaluation/reference_qa/run.py'), str(p)])\n")
    script = (prior/'run.sbatch').read_text().replace('cup-practical-legacy-git-a-v1',version).replace('00:45:00','00:30:00')
    setup = f'''unset OPENAI_API_KEY BAZE_API_KEY HF_TOKEN HUGGING_FACE_HUB_TOKEN
python -m venv --system-site-packages {remote}/reference-env
timeout 180 {remote}/reference-env/bin/python -m pip install --disable-pip-version-check -r {remote}/requirements-reference.txt
{remote}/reference-env/bin/python -m pip freeze > {remote}/client-environment.txt
'''
    script = script.replace('python -u ',setup+'python -u ')
    validate_submission(script,1); (dest/'run.sbatch').write_text(script)
    files = ['run.sbatch','config.json','serve.py','service.py','inputs.json','code.tar.gz','requirements-reference.txt']
    progress = dict(status='awaiting_ssh_authentication', submitted=False,job_id=None,source_version=version,
        planned_gpus=1,planned_wall_minutes=30,phase_gpu_minutes_cap=30,semantic_results_available=False,
        program=str(dest/'run.sbatch'),files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        checks=dict(integration_tests_passed=5,legacy_tests_passed=223,originals=786,chunks=832,
                    invalid_original_offsets=0,max_chunk_tokens=506),
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 30 '+' '.join(files),
        next='Recheck SSH, whole-user queue, locks and intents; submit once. No automatic resource growth.')
    (repo/'results/reference-qa/progress.json').write_text(json.dumps(progress,indent=2)+'\n')
    print('Prepared; NOT submitted:', dest)


if __name__ == '__main__': main()
