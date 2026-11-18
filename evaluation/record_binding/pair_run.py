"""Frozen-context relation selection; no gold, new spans, validation model or training."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
import os
from pathlib import Path
import time
from team_memory.records.pair_binding import request


def main(folder):
    import httpx
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURMD_NODENAME') and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for table,root in [('code_sha256',folder/'code'),('data_sha256',folder)]:
        for n,h in cfg[table].items():assert sha256((root/n).read_bytes()).hexdigest()==h,n
    job=os.environ['SLURM_JOB_ID'];out=Path(cfg['project'])/'results'/f'record-pair-{job}.json'
    assert not out.exists();start=time.monotonic()
    result=dict(status='running',job_id=job,model_revision=cfg['model_revision'],rows=[],calls=0,
        code_sha256=cfg['code_sha256'],data_sha256=cfg['data_sha256'],training_steps=0,external_model_api_calls=0)
    def save():
        result['seconds']=time.monotonic()-start
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2));tmp.replace(out)
    try:
        with httpx.Client(trust_env=False,timeout=240) as client,ThreadPoolExecutor(max_workers=4) as pool,out.with_suffix('.calls.jsonl').open('x') as log:
            def infer(source,q):
                body=request(source,q);response=client.post(os.environ['PRACTICAL_MODEL_URL']+'/chat/completions',json=body)
                response.raise_for_status();return body,response.json()
            for item in json.loads((folder/'inputs.json').read_text()):
                assert result['calls']+len(item['catalog']['queries'])<=cfg['max_calls']
                result['calls']+=len(item['catalog']['queries'])
                futures={pool.submit(infer,item['source'],q):q for q in item['catalog']['queries']};outputs={};usage=[]
                for f in as_completed(futures):
                    q=futures[f];body,data=f.result();key=q['context']['id']
                    log.write(json.dumps(dict(item_id=item['id'],context_id=key,request=body,response=data),ensure_ascii=False)+'\n');log.flush()
                    assert data['choices'][0]['finish_reason']=='stop','Truncated relation classification'
                    outputs[key]=data['choices'][0]['message']['content'];usage.append(data.get('usage',{}))
                result['rows'].append(dict(id=item['id'],source=item['source'],outputs=dict(sorted(outputs.items())),usage=usage))
                save();print('ROW',item['id'],'TOTAL_CALLS',result['calls'],flush=True)
        assert result['calls']==cfg['max_calls'] and len(result['rows'])==68
        result['status']='complete'
    except BaseException as exc:
        result.update(status='failed',error=f'{type(exc).__name__}: {exc}');raise
    finally:save()


if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]))
