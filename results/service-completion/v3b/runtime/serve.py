"""Bounded Slurm local server; inherited from the verified service-v1 launcher."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
from urllib.request import ProxyHandler, build_opener


def main():
    folder=Path(__file__).resolve().parent
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ.get('SLURMD_NODENAME')
    assert os.environ.get('CONDA_PREFIX')==cfg['conda_prefix']
    import torch
    assert torch.cuda.device_count()==1
    port=31000+int(os.environ['SLURM_JOB_ID'])%20000
    result=Path(cfg['project'])/'results'/('sm-'+os.environ['SLURM_JOB_ID']+'.json')
    assert not result.exists()
    import importlib.metadata
    server_environment=dict(python=sys.executable, packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()})
    record=dict(server_environment=server_environment,status='preparing',job_id=os.environ['SLURM_JOB_ID'],source_version=cfg['source_version'],
                model=cfg['model_repo'],revision=cfg['model_revision'],external_model_api_calls=0,
                port=port,node=os.environ['SLURMD_NODENAME'],serve_seconds=cfg['serve_seconds'])
    def save():
        tmp=result.with_suffix('.tmp');tmp.write_text(json.dumps(record,indent=2));tmp.replace(result)
    save();process=None
    try:
        local,shared=Path(cfg['model_path']),Path(cfg['model_shared'])
        ready=json.loads((shared/'READY.json').read_text())
        assert ready['revision']==cfg['model_revision'] and ready['files_sha256']==cfg['model_files_sha256']
        local.mkdir(parents=True,exist_ok=True)
        for name,expected in cfg['model_files_sha256'].items():
            assert Path(name).name==name
            dst=local/name;src=shared/name
            if dst.exists():
                assert dst.stat().st_size==src.stat().st_size, 'Cached model size mismatch'
            else:
                tmp=local/(name+'.workbench-'+record['job_id']);assert not tmp.exists()
                h=hashlib.sha256()
                with src.open('rb') as inp,tmp.open('xb') as out:
                    while block:=inp.read(8*1024*1024):h.update(block);out.write(block)
                assert h.hexdigest()==expected
                tmp.replace(dst)
        record['cache_check']='Previously verified cache: file sizes. Newly copied files: SHA256.'
        cmd=[sys.executable,'-m','vllm.entrypoints.openai.api_server','--model',str(local),
             '--served-model-name','Qwen3-8B','--host','127.0.0.1','--port',str(port),
             '--dtype','bfloat16','--tensor-parallel-size','1','--max-model-len','32768',
             '--max-num-seqs','4','--gpu-memory-utilization','0.90','--max-num-batched-tokens','4096',
             '--enable-chunked-prefill','--enforce-eager','--generation-config','vllm','--seed','42',
             '--disable-log-requests']
        env=dict(os.environ)
        for key in ('OPENAI_API_KEY','BAZE_API_KEY','HF_TOKEN','HUGGING_FACE_HUB_TOKEN'):env.pop(key,None)
        env['PRACTICAL_MODEL_URL']='http://127.0.0.1:'+str(port)+'/v1'
        process=subprocess.Popen(cmd,env=env,start_new_session=True)
        http=build_opener(ProxyHandler({}));start=time.monotonic()
        while time.monotonic()-start<cfg['startup_seconds']:
            if process.poll() is not None:raise RuntimeError('Model server exited during startup')
            try:
                with http.open('http://127.0.0.1:'+str(port)+'/health',timeout=3) as response:
                    if response.status==200:break
            except OSError:time.sleep(2)
        else:raise RuntimeError('Server startup exceeded configured preparation limit')
        record.update(status='ready',ready_at=time.time(),expires_at=time.time()+cfg['serve_seconds'])
        save();print('SERVICE_READY',json.dumps(record),flush=True)
        completed=subprocess.run([sys.executable,'-u',str(folder/'service.py')],env=env,timeout=cfg['client_seconds'])
        record['client_exit_code']=completed.returncode
        if completed.returncode:raise RuntimeError('Documents service run failed; preserve detailed result')
        record.update(status='complete',reason='reference source QA completed',native_result=str(result.with_name('service-completion-'+record['job_id']+'.json')))
    except BaseException as exc:
        record.update(status='failed',error=type(exc).__name__+': '+str(exc));raise
    finally:
        if process and process.poll() is None:
            os.killpg(process.pid,signal.SIGTERM)
            try:process.wait(timeout=15)
            except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait()
        save()


if __name__=='__main__':main()
