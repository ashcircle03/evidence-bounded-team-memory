"""A bounded development check on previously captured native retrieval output."""
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import time
import traceback


def main():
    folder=Path(__file__).resolve().parent;cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ.get('SLURMD_NODENAME')
    assert os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    sys.path.insert(0,str(folder/'code'))
    from team_memory.cupmem_readout import read_selected_sources
    from openai import OpenAI
    for name,expected in cfg['code_sha256'].items():
        assert sha256((folder/'code'/name).read_bytes()).hexdigest()==expected
    blob=(folder/'inputs.json').read_bytes();assert sha256(blob).hexdigest()==cfg['input_sha256']
    job=os.environ['SLURM_JOB_ID']
    local=Path('/local_datasets/pjw031003/capstone-shared-knowledge/source-readout')/job
    local.mkdir(parents=True,exist_ok=False);(local/'inputs.json').write_bytes(blob)
    data=json.loads((local/'inputs.json').read_text())
    out=Path(cfg['project'])/'results'/('cup-readout-'+job+'.json');assert not out.exists()
    client=OpenAI(api_key='local-no-secret',base_url='http://127.0.0.1:28382/v1',timeout=90,max_retries=0)
    record=dict(status='running',job_id=job,native_job=data['native_job'],input_sha256=cfg['input_sha256'],
        model='Qwen3-8B',scope='Four reader calls reusing actual saved CUPMem selections; no new native ingestion/retrieval',
        full_pipeline_rerun=False,rows=[],calls=[])
    start=time.monotonic()
    def save():
        record['seconds']=time.monotonic()-start
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2));tmp.replace(out)
    def generate(system,content):
        if len(record['calls'])>=4:raise RuntimeError('Four calls only')
        body=dict(model='Qwen3-8B',messages=[dict(role='system',content=system),dict(role='user',content=content)],
            max_tokens=900,temperature=0,response_format={'type':'json_object'},
            extra_body={'chat_template_kwargs':{'enable_thinking':False}})
        result=client.chat.completions.create(**body)
        record['calls'].append(dict(request=body,response=result.model_dump(mode='json')));save()
        return result.choices[0].message.content
    save()
    try:
        for native in data['rows']:
            result=read_selected_sources(native,generate)
            record['rows'].append(result);save()
            print('READOUT',native['question'],json.dumps(result['answers'],ensure_ascii=False),flush=True)
        record['status']='complete'
    except BaseException as exc:
        record.update(status='failed',error=str(exc),traceback=traceback.format_exc());raise
    finally:save()


if __name__=='__main__':main()
