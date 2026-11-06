"""Freeze exact-output replay and its sole newly reachable model revision."""
from hashlib import sha256
import json
from pathlib import Path
import tarfile
from evaluation.cupmem.dispatch import validate_submission


def main():
    repo=Path(__file__).resolve().parents[2];campaign=repo.parent/'campaigns/speakermem-dev'
    version='cup-ref-parse-v1';d=json.loads((campaign/'campaign-dispatch.json').read_text())
    assert version not in d['jobs'] and d['jobs']['cup-ref-fix-v3']['state']=='COMPLETED'
    prior=campaign/'source/cup-ref-fix-v3';dest=campaign/'source'/version;dest.mkdir(exist_ok=False)
    cfg=json.loads((prior/'config.json').read_text());names=list(cfg['code_sha256'])+['evaluation/reference_qa/replay.py']
    with tarfile.open(dest/'code.tar.gz','w:gz') as t:
        for name in names:t.add(repo/name,arcname=name)
    for name in ['inputs.json','serve.py','service.py']:(dest/name).write_bytes((prior/name).read_bytes())
    (dest/'service.py').write_text((dest/'service.py').read_text().replace('reference_qa/run.py','reference_qa/replay.py'))
    for src,name in [('result.json','prior-result.json'),('calls.jsonl','prior-calls.jsonl')]:
        (dest/name).write_bytes((repo/'results/reference-qa/fix-v3'/src).read_bytes())
    cfg.update(source_version=version,client_seconds=150,serve_seconds=180,max_new_calls=1,expected_new_calls=1,
        replay_files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in ['prior-result.json','prior-calls.jsonl']},
        code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names})
    cfg['resources']['wall_minutes']=9
    cfg['execution_changes']['parser_recovery']='Upstream explicit-label fallback; all20 frozen outputs replayed; 114 calls reused, one newly reachable Qwen revision. No answer-key input.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script=(prior/'run.sbatch').read_text().replace('cup-ref-fix-v3',version).replace('00:20:00','00:09:00')
    # Replay does not construct an index, tokenizer-based splitter or NLTK reader.
    script='\n'.join(l for l in script.splitlines() if 'NLTK_DATA=' not in l and 'prepare_nltk.py' not in l)+'\n'
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    out=repo/'results/reference-qa/parse-v1';out.mkdir(exist_ok=False)
    files=['run.sbatch','config.json','serve.py','service.py','inputs.json','code.tar.gz','prior-result.json','prior-calls.jsonl']
    freeze=json.loads((repo/'results/reference-qa/fix-v3/freeze.json').read_text())
    freeze.update(source_version=version,profile='checked',
        files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        validation='All20 actual drafts and89 judge outputs; reused revisions only when exact messages match',
        budget=dict(gpus=1,wall_minutes=9,existing_phase_cap_gpu_minutes=50),
        expected_new_calls=1,changed_labels=23,
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 9 '+' '.join(files))
    freeze.pop('actor_unchanged_from',None)
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for name in ['config.json','run.sbatch']:(out/name).write_bytes((dest/name).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
