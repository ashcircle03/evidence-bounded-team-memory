"""Freeze the upstream per-document fallback before seeing its outputs."""
from hashlib import sha256
import json
from pathlib import Path
import tarfile
from evaluation.cupmem.dispatch import validate_submission
from team_memory.reference_checked import missing_opposing_sources


def main():
    repo=Path(__file__).resolve().parents[2];campaign=repo.parent/'campaigns/speakermem-dev'
    version='cup-ref-acc-v1';d=json.loads((campaign/'campaign-dispatch.json').read_text())
    assert version not in d['jobs'] and d['jobs']['cup-ref-parse-v1']['state']=='COMPLETED'
    prior=campaign/'source/cup-ref-parse-v1';dest=campaign/'source'/version;dest.mkdir(exist_ok=False)
    cfg=json.loads((prior/'config.json').read_text())
    names=list(cfg['code_sha256'])+['evaluation/reference_qa/accumulate_replay.py']
    with tarfile.open(dest/'code.tar.gz','w:gz') as t:
        for name in names:t.add(repo/name,arcname=name)
    for name in ['inputs.json','serve.py','service.py']:(dest/name).write_bytes((prior/name).read_bytes())
    (dest/'service.py').write_text((dest/'service.py').read_text().replace('reference_qa/replay.py','reference_qa/accumulate_replay.py'))
    for src,name in [('result.json','prior-result.json'),('calls.jsonl','prior-calls.jsonl')]:
        (dest/name).write_bytes((repo/'results/reference-qa/parse-v1'/src).read_bytes())
    previous=json.loads((dest/'prior-result.json').read_text());branches=[]
    for row in previous['rows']:
        for step in row['steps']:
            if step['label']=='import':continue
            if missing_opposing_sources(step['result']):
                branches.append(dict(case_id=row['case_id'],label=step['label'],
                    documents=sum(j['label'] in ('SUPPORTS','CONTRADICTS') for j in step['result']['document_judgments'])))
    expected=sum(b['documents'] for b in branches)
    assert len(branches)==3 and expected==8
    cfg.update(source_version=version,client_seconds=180,serve_seconds=210,
        max_new_calls=expected,expected_new_calls=expected,
        replay_files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in ['prior-result.json','prior-calls.jsonl']},
        code_sha256={n:sha256((repo/n).read_bytes()).hexdigest() for n in names})
    cfg['resources']['wall_minutes']=8
    cfg['execution_changes']['accumulate']='Official LlamaIndex Accumulate and Citation QA template for SUPPORTS/CONTRADICTS documents if rewrite omits opposing source citation. No model merger, answer key or case exception.'
    (dest/'config.json').write_text(json.dumps(cfg,indent=2)+'\n')
    script=(prior/'run.sbatch').read_text().replace('cup-ref-parse-v1',version).replace('00:09:00','00:08:00')
    validate_submission(script,1);(dest/'run.sbatch').write_text(script)
    out=repo/'results/reference-qa/accumulate-v1';out.mkdir(exist_ok=False)
    files=['run.sbatch','config.json','serve.py','service.py','inputs.json','code.tar.gz','prior-result.json','prior-calls.jsonl']
    freeze=json.loads((repo/'results/reference-qa/parse-v1/freeze.json').read_text())
    freeze.update(source_version=version,profile='checked',
        files_sha256={n:sha256((dest/n).read_bytes()).hexdigest() for n in files},
        validation='All20 frozen actual outputs; generic omitted-opponent citation gate, upstream per-document QA; no semantic filter after outputs',
        budget=dict(gpus=1,wall_minutes=8,existing_phase_cap_gpu_minutes=50),
        expected_new_calls=expected,expected_branches=branches,
        submit_command='python3 -m evaluation.cupmem.dispatch submit '+version+' 1 8 '+' '.join(files))
    freeze.pop('changed_labels',None)
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    for name in ['config.json','run.sbatch']:(out/name).write_bytes((dest/name).read_bytes())
    print(freeze['submit_command'])


if __name__=='__main__':main()
