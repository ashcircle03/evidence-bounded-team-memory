"""68 new same-Qwen calls; no keys or evaluation files in inference packet."""
from pathlib import Path
from hashlib import sha256
import json,os,time,sys,tempfile,importlib.metadata

def main(folder):
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURMD_NODENAME') and os.environ.get('CONDA_PREFIX')==cfg['conda_prefix']
    for n,h in cfg['code_sha256'].items():assert sha256((folder/'code'/n).read_bytes()).hexdigest()==h,n
    for n,h in cfg['data_sha256'].items():assert sha256((folder/n).read_bytes()).hexdigest()==h,n
    import httpx
    from team_memory.records import bound
    from evaluation.record_groups.evaluate import transport
    assert importlib.metadata.version('langextract')=='1.7.2'
    job=os.environ['SLURM_JOB_ID'];out=Path(cfg['project'])/'results'/('record-bound-'+job+'.json');assert not out.exists()
    record=dict(status='running',job_id=job,model_revision=cfg['model_revision'],code_sha256=cfg['code_sha256'],data_sha256=cfg['data_sha256'],calls=0,rows=[],external_model_api_calls=0);start=time.monotonic()
    def save():
        record['seconds']=time.monotonic()-start;tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2));tmp.replace(out)
    try:
        with httpx.Client(trust_env=False,timeout=240) as client,out.with_suffix('.calls.jsonl').open('x') as trace,tempfile.TemporaryDirectory(prefix='record-bound-') as temp:
            for item in json.loads((folder/'inputs.json').read_text())['items']:
                source=item['source'];segs=bound.segments(source)
                body=dict(model='Qwen3-8B',messages=[dict(role='system',content=bound.SYSTEM),dict(role='user',content=bound.prompt(source))],temperature=0,max_tokens=2048,chat_template_kwargs=dict(enable_thinking=False),seed=42,guided_json=bound.schema(len(segs)))
                assert record['calls']<cfg['max_calls'];record['calls']+=1;t=time.monotonic()
                response=client.post(os.environ['PRACTICAL_MODEL_URL']+'/chat/completions',json=body);response.raise_for_status();data=response.json()
                trace.write(json.dumps(dict(id=record['calls'],item_id=item['id'],request=body,response=data),ensure_ascii=False)+'\n');trace.flush()
                raw=data['choices'][0]['message']['content'];g=bound.compile_graph(source,raw,'Qwen3-8B@'+cfg['model_revision']);enriched=dict(source,record_graph=g)
                row=dict(id=item['id'],arm='bound',source=enriched,raw=raw,seconds=time.monotonic()-t)
                try:row['transport']=transport(enriched,Path(temp)/str(record['calls']))
                except Exception as exc:row['transport']=dict(stored_restarted=False,error=type(exc).__name__+': '+str(exc))
                record['rows'].append(row);save();print('ROW',record['calls'],item['id'],g['status'],flush=True)
            assert record['calls']==cfg['max_calls'];record['status']='complete'
    except BaseException as exc:record.update(status='failed',error=type(exc).__name__+': '+str(exc));raise
    finally:save()
if __name__=='__main__':main(Path(sys.argv[1]))
