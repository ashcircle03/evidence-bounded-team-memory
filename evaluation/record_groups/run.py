"""Query-free construction only, same frozen Qwen/decoding as prior writer."""
from hashlib import sha256
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time


def main(folder):
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURMD_NODENAME') and os.environ.get('CONDA_PREFIX')==cfg['conda_prefix']
    for n,h in cfg['code_sha256'].items():assert sha256((folder/'code'/n).read_bytes()).hexdigest()==h,n
    for n,h in cfg['data_sha256'].items():assert sha256((folder/n).read_bytes()).hexdigest()==h,n
    import httpx
    from team_memory.records import graph,grouped
    assert importlib.metadata.version('langextract')=='1.7.2'
    job=os.environ['SLURM_JOB_ID'];out=Path(cfg['project'])/'results'/('record-groups-'+job+'.json')
    assert not out.exists()
    record=dict(status='running',job_id=job,model_revision=cfg['model_revision'],code_sha256=cfg['code_sha256'],
        data_sha256=cfg['data_sha256'],calls=0,rows=[],external_model_api_calls=0,
        packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()})
    start=time.monotonic()
    def save():
        record['seconds']=time.monotonic()-start
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2));tmp.replace(out)
    try:
        with httpx.Client(trust_env=False,timeout=180) as client,out.with_suffix('.calls.jsonl').open('x') as trace:
            for item in json.loads((folder/'inputs.json').read_text())['sources']:
                for arm in item['arms']:
                    def generate(system,content):
                        assert record['calls']<cfg['max_calls']
                        extra=dict(chat_template_kwargs={'enable_thinking':False},seed=42)
                        kw=(graph.vllm_writer_kwargs(extra) if arm=='baseline' else grouped.writer_kwargs(extra))['extra_body']
                        body=dict(model='Qwen3-8B',messages=[dict(role='system',content=system),dict(role='user',content=content)],temperature=0,max_tokens=2048,**kw)
                        record['calls']+=1
                        response=client.post(os.environ['PRACTICAL_MODEL_URL']+'/chat/completions',json=body)
                        response.raise_for_status();data=response.json()
                        trace.write(json.dumps(dict(id=record['calls'],source_id=item['source']['id'],arm=arm,request=body,response=data),ensure_ascii=False)+'\n');trace.flush()
                        return data['choices'][0]['message']['content']
                    module=graph if arm=='baseline' else grouped
                    enriched=module.construct(item['source'],generate,model='Qwen3-8B@'+cfg['model_revision'])
                    record['rows'].append(dict(case_id=item['case_id'],arm=arm,source=enriched));save()
            record['status']='complete'
    except BaseException as exc:
        record.update(status='failed',error=type(exc).__name__+': '+str(exc));raise
    finally:save()

if __name__=='__main__':main(Path(sys.argv[1]))
