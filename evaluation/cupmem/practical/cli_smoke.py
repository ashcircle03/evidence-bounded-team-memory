"""Run the shipped JSONL example against the allocated local model, once."""
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    folder=Path(__file__).resolve().parent
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ.get('CONDA_PREFIX')==cfg['conda_prefix']
    job=os.environ['SLURM_JOB_ID'];code=folder/'code'
    for path,expected in cfg['code_sha256'].items():
        assert sha256((code/path).read_bytes()).hexdigest()==expected,path
    raw=(folder/'inputs.json').read_bytes()
    assert sha256(raw).hexdigest()==cfg['input_sha256']
    requests=[json.loads(s) for s in raw.splitlines()]
    store=Path('/local_datasets/pjw031003/capstone-shared-knowledge/cli-smoke')/job
    assert not store.exists()
    command=[sys.executable,str(code/'examples/practical_service.py'),'--upstream',cfg['upstream'],
             '--embedding',cfg['embedding'],'--store',str(store),'--base-url',os.environ['PRACTICAL_MODEL_URL'],
             '--strategy','cupmem']
    started=time.monotonic()
    completed=subprocess.run(command,input=raw,capture_output=True,timeout=cfg['client_seconds']-20)
    result=dict(status='failed',scope='Shipped JSONL CLI wiring on known development input; not an additional benchmark',
        job_id=job,source_version=cfg['source_version'],input_sha256=cfg['input_sha256'],code_sha256=cfg['code_sha256'],
        returncode=completed.returncode,seconds=time.monotonic()-started,external_model_api_calls=0,
        requests=requests,stdout=completed.stdout.decode(),stderr=completed.stderr.decode())
    out=Path(cfg['project'])/'results'/('cup-practical-'+job+'.json')
    try:
        assert completed.returncode==0
        responses=[json.loads(s) for s in result['stdout'].splitlines()]
        assert len(responses)==len(requests)==3
        assert all(r['status'] in ('ok','partial') for r in responses)
        assert any(p['kind']=='reconsider' and p['status']=='pending' for p in responses[1]['proposals'])
        answers=responses[2]['answers'];assert answers
        assert all(a['evidence'] for a in answers)
        sys.path.insert(0,str(code))
        from team_memory.store import Store
        from team_memory.timeline import valid_witness
        sources=Store(store).load('sources')
        assert len(sources)==2
        assert all(valid_witness(w,sources) for a in answers for w in a['evidence'])
        assert not any(p['status']=='approved' for r in responses for p in r['proposals'])
        result.update(status='complete',responses=responses,checks=dict(jsonl_roundtrip=True,original_sources=2,
            pending_reconsideration=True,exact_qa_citations=True,no_implicit_approval=True))
    finally:
        out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('CLI_SMOKE_COMPLETE',job,flush=True)


if __name__=='__main__':main()
