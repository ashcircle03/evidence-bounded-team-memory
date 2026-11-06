"""Prepare the final bounded recovery using the upstream document judge."""
from hashlib import sha256
import json
from pathlib import Path
import tarfile

from evaluation.cupmem.dispatch import validate_submission


def main():
    repo = Path(__file__).resolve().parents[2]
    campaign = repo.parent/'campaigns/speakermem-dev'
    version = 'cup-ref-fix-v2'
    ledger = json.loads((campaign/'campaign-dispatch.json').read_text())
    assert version not in ledger['jobs']
    prior = campaign/'source/cup-ref-fix-v1'
    dest = campaign/'source'/version; dest.mkdir(exist_ok=False)
    cfg = json.loads((prior/'config.json').read_text())
    names = list(cfg['code_sha256']) + ['team_memory/reference_checked.py',
        'team_memory/_vendor/conflictscore/__init__.py',
        'team_memory/_vendor/conflictscore/eval_all_calibration.py',
        'team_memory/_vendor/conflictscore/LICENSE']
    with tarfile.open(dest/'code.tar.gz','w:gz') as tar:
        for name in names: tar.add(repo/name,arcname=name)
    cfg.update(source_version=version,profile='checked',client_seconds=430,serve_seconds=460,max_calls=160,
        code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names})
    cfg['resources']['wall_minutes'] = 9
    cfg['execution_changes'].update(qa='Ordinary source QA draft; upstream ConflictScore document judge; conditional evidence feedback',
        upstream_revision='microsoft/ConflictScore@a8868e5cd98bff81935a1766b54a02ad3eab9e8f',
        verifier='Whole-answer direct variant; group retrieved chunks by original source; max384 output tokens',
        batching='4 document calls concurrently on the same GPU; vLLM max_num_seqs4',
        citation_mapping='Accept explicit Source N labels as well as [N], preserving physical raw output',
        environment='Reuse unmodified v1 client and fix-v1 isolated extras; fresh private NLTK')
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    for name in ['inputs.json','service.py','prepare_nltk.py']:
        (dest/name).write_bytes((prior/name).read_bytes())
    server = (prior/'serve.py').read_text()
    assert "'--max-num-seqs','1'" in server
    (dest/'serve.py').write_text(server.replace("'--max-num-seqs','1'", "'--max-num-seqs','4'"))
    script = (prior/'run.sbatch').read_text().replace('cup-ref-fix-v1',version).replace('00:20:00','00:09:00')
    script = '\n'.join(line for line in script.splitlines() if 'pip install' not in line)+'\n'
    validate_submission(script,1); (dest/'run.sbatch').write_text(script)
    files = ['run.sbatch','config.json','serve.py','service.py','inputs.json','code.tar.gz','prepare_nltk.py']
    out = repo/'results/reference-qa/fix-v2';out.mkdir(exist_ok=False)
    freeze = json.loads((repo/'results/reference-qa/fix-v1/freeze.json').read_text())
    freeze.update(source_version=version,profile='checked',
        files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        prior_failed_attempt='119861, preserved in fix-v1',
        budget=dict(gpus=1,wall_minutes=9,existing_phase_cap_gpu_minutes=30,includes_all_prior_attempts=True),
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 9 '+' '.join(files))
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for name in ['config.json','run.sbatch']:(out/name).write_bytes((dest/name).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
