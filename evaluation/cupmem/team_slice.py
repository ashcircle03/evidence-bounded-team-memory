"""Execute a tiny native CUPMem team stream on the allocation's local model."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace
import traceback


def main():
    folder=Path(__file__).resolve().parent;cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ.get('SLURMD_NODENAME')
    assert os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    sys.path[:0]=[str(folder/'code'),cfg['upstream']]
    from cup_mem import CupMemEngine,LLMClient,TraceConfig
    from team_memory.cupmem_adapter import CUPMemTeamMemory
    from openai import OpenAI
    job=os.environ['SLURM_JOB_ID'];out=Path(cfg['project'])/'results'/('cup-team-'+job+'.json')
    calls=[];lock=threading.Lock();started=time.monotonic()
    calls_file=out.with_suffix('.calls.jsonl').open('x')
    class LimitStop(BaseException):pass
    class LocalClient:
        def __init__(self,**kwargs):
            assert kwargs['base_url']=='http://127.0.0.1:28382/v1'
            self.real=OpenAI(**kwargs,max_retries=0,timeout=90)
            self.chat=SimpleNamespace(completions=SimpleNamespace(create=self.create))
        def create(self,**kwargs):
            with lock:
                if len(calls)>=180 or time.monotonic()-started>840:raise LimitStop('Bounded development run ended')
                kwargs['max_tokens']=4096
                kwargs.setdefault('temperature',0.0)
                kwargs.setdefault('response_format',{'type':'json_object'})
                kwargs['extra_body']={'chat_template_kwargs':{'enable_thinking':False}}
                row=dict(id=len(calls),request=kwargs);calls.append(row)
            begin=time.monotonic()
            try:
                result=self.real.chat.completions.create(**kwargs)
                row['response']=result.model_dump(mode='json');return result
            except Exception as exc:
                row.update(error_type=type(exc).__name__,error=str(exc));raise
            finally:
                row['seconds']=time.monotonic()-begin
                with lock:calls_file.write(json.dumps(row,ensure_ascii=False)+'\n');calls_file.flush()
    blob=(folder/'inputs.json').read_bytes();assert sha256(blob).hexdigest()==cfg['input_sha256']
    # Stage data on node-local storage before native processing.
    data_dir=Path('/local_datasets/pjw031003/capstone-shared-knowledge/team-slice')/job
    data_dir.mkdir(parents=True,exist_ok=False);(data_dir/'inputs.json').write_bytes(blob)
    data=json.loads((data_dir/'inputs.json').read_text())
    for name,expected in cfg['code_sha256'].items():
        assert sha256((folder/'code'/name).read_bytes()).hexdigest()==expected,name
    record=dict(status='running',job_id=job,input_sha256=cfg['input_sha256'],
        upstream_revision='ea7d391103a151927cd29d2f01d87597a782bdcb',model='Qwen3-8B',
        original_model_reproduction=False,scope='Existing synthetic development sources through unmodified CUPMem',
        steps=[],sources=data['sources'])
    def save():
        record['calls']=len(calls);record['seconds']=time.monotonic()-started
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2));tmp.replace(out)
    save()
    memory=None
    try:
        llm=LLMClient(model='Qwen3-8B',api_key='local-no-secret',base_url='http://127.0.0.1:28382/v1',openai_cls=LocalClient)
        engine=CupMemEngine(llm=llm,embedding_model_path=cfg['embedding'],embedding_device='cpu',
                            trace_config=TraceConfig(enable_debug_trace=True))
        memory=CUPMemTeamMemory(engine,lambda:list(calls))
        for source in data['sources']:
            value=memory.ingest(source,review_changes=True)
            record['steps'].append(dict(operation='ingest',result=value));save()
            print('INGEST_DONE',len(memory.sources),'calls',len(calls),flush=True)
        for question in data['questions']:
            value=memory.ask(question);record['steps'].append(dict(operation='qa',result=value));save()
            print('QA_DONE',question,json.dumps(value['answer'],ensure_ascii=False),'citations',len(value['citations']),flush=True)
        record['status']='complete'
    except BaseException as exc:
        record.update(status='failed',error_type=type(exc).__name__,error=str(exc),traceback=traceback.format_exc(),
                      raw_response_excerpt=getattr(exc,'raw_response_excerpt',None));raise
    finally:
        if memory:
            try:record['native_snapshot']=memory.snapshot()
            except Exception as snapshot_error:record['snapshot_error']=str(snapshot_error)
        save();calls_file.close()


if __name__=='__main__':main()
