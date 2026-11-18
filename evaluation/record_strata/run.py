"""Key-free inference, exact input traces, actual persistence and reader transport."""
from hashlib import sha256
import importlib.metadata
import json,os,sys,time,tempfile
from pathlib import Path

def main(folder):
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURMD_NODENAME') and os.environ.get('CONDA_PREFIX')==cfg['conda_prefix']
    for n,h in cfg['code_sha256'].items():assert sha256((folder/'code'/n).read_bytes()).hexdigest()==h,n
    for n,h in cfg['data_sha256'].items():assert sha256((folder/n).read_bytes()).hexdigest()==h,n
    import httpx
    from team_memory.records import grouped
    from evaluation.record_strata.arms import prompt,compile_source,SYSTEM
    from evaluation.record_groups.evaluate import transport
    assert importlib.metadata.version('langextract')=='1.7.2'
    job=os.environ['SLURM_JOB_ID'];out=Path(cfg['project'])/'results'/('record-strata-'+job+'.json')
    assert not out.exists()
    record=dict(status='running',job_id=job,model_revision=cfg['model_revision'],code_sha256=cfg['code_sha256'],data_sha256=cfg['data_sha256'],calls=0,rows=[],external_model_api_calls=0)
    start=time.monotonic()
    def save():
        record['seconds']=time.monotonic()-start
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2));tmp.replace(out)
    try:
        with httpx.Client(trust_env=False,timeout=240) as client,out.with_suffix('.calls.jsonl').open('x') as trace,tempfile.TemporaryDirectory(prefix='records-strata-') as temp:
            for item in json.loads((folder/'inputs.json').read_text())['items']:
                for arm in item['arms']:
                    assert record['calls']<cfg['max_calls']
                    body=dict(model='Qwen3-8B',messages=[dict(role='system',content=SYSTEM),dict(role='user',content=prompt(item['source'],arm))],temperature=0,max_tokens=2048,**grouped.writer_kwargs(dict(chat_template_kwargs={'enable_thinking':False},seed=42),basis_types=True)['extra_body'])
                    record['calls']+=1;t=time.monotonic()
                    response=client.post(os.environ['PRACTICAL_MODEL_URL']+'/chat/completions',json=body)
                    response.raise_for_status();data=response.json()
                    trace.write(json.dumps(dict(id=record['calls'],item_id=item['id'],source_id=item['source']['id'],arm=arm,request=body,response=data),ensure_ascii=False)+'\n');trace.flush()
                    raw=data['choices'][0]['message']['content']
                    enriched,error=compile_source(item['source'],raw,'Qwen3-8B@'+cfg['model_revision'])
                    row=dict(id=item['id'],arm=arm,source=enriched,raw=raw,compile_error=error,seconds=time.monotonic()-t)
                    try:row['transport']=transport(enriched,Path(temp)/str(record['calls']))
                    except Exception as exc:row['transport']=dict(stored_restarted=False,error=type(exc).__name__+': '+str(exc))
                    record['rows'].append(row);save()
                    print('ROW',record['calls'],item['id'],arm,enriched['record_graph']['status'],flush=True)
            assert record['calls']==cfg['max_calls']
            record['status']='complete'
    except BaseException as exc:
        record.update(status='failed',error=type(exc).__name__+': '+str(exc));raise
    finally:save()
if __name__=='__main__':main(Path(sys.argv[1]))
