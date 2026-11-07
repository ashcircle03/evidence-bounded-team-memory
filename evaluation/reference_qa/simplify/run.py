"""Frozen same-model comparison:20 fixed-context regressions and12 paired streams."""
from pathlib import Path
from hashlib import sha256
import json,os,sys,time
from threading import Lock


def main():
    folder=Path(sys.argv[1]);cfg=json.loads((folder/'config.json').read_text())
    assert os.environ['SLURMD_NODENAME'] and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for n,h in cfg['code_sha256'].items():assert sha256((folder/'code'/n).read_bytes()).hexdigest()==h
    for n,h in cfg['data_sha256'].items():assert sha256((folder/n).read_bytes()).hexdigest()==h
    sys.path.insert(0,str(folder/'code'))
    import httpx
    from llama_index.core.llms import ChatMessage
    from team_memory.reference_qa import local_components
    from team_memory.reference_joint import JointSourceQA,joint_template,format_joint
    from team_memory.reference_attributed import AttributedQA
    job=os.environ['SLURM_JOB_ID'];began=time.monotonic();lock=Lock();context={}
    out=Path(cfg['project'])/'results'/f'cup-reference-{job}.json'
    stream=out.with_suffix('.calls.jsonl').open('x',encoding='utf-8')
    record=dict(status='running',job_id=job,source_version=cfg['source_version'],code_sha256=cfg['code_sha256'],data_sha256=cfg['data_sha256'],calls=0,rows=[],external_model_api_calls=0)
    def save():
        record['seconds']=time.monotonic()-began
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(out)
    def request_hook(request):
        if not request.url.path.endswith('/chat/completions'):return
        body=json.loads(request.content)
        with lock:
            if record['calls']>=cfg['max_calls'] or time.monotonic()-began>cfg['client_seconds']-30:raise RuntimeError('Frozen request/time cap reached')
            trace=dict(id=record['calls'],context=dict(context),request=body,started=time.monotonic(),rendered_prompt_tokens=len(parts['tokenizer'].apply_chat_template(body['messages'],tokenize=True,add_generation_prompt=True,enable_thinking=False)))
            request.extensions['reference_trace']=trace;record['calls']+=1
    def response_hook(response):
        response.read();trace=response.request.extensions.get('reference_trace')
        if trace:
            with lock:
                stream.write(json.dumps(dict(trace,response=response.json(),http_status=response.status_code,seconds=time.monotonic()-trace['started']),ensure_ascii=False)+'\n');stream.flush()
    save()
    with httpx.Client(trust_env=False,event_hooks={'request':[request_hook],'response':[response_hook]}) as client:
        parts=local_components(cfg['model_path'],cfg['embedding'],os.environ['PRACTICAL_MODEL_URL'],http_client=client)
        try:
            for case in json.loads((folder/'legacy-contexts.json').read_text())['cases']:
                context.clear();context.update(split='legacy',case_id=case['id'],arm='joint')
                first=record['calls'];start=time.monotonic()
                prompt=joint_template().format(context_str=case['context'],query_str=case['question'])
                raw=parts['llm'].chat([ChatMessage(role='user',content=prompt)]).message.content
                result=format_joint(case['question'],raw,case['witnesses'])
                record['rows'].append(dict(**context,result=result,calls=record['calls']-first,seconds=time.monotonic()-start))
                save();print('STEP',json.dumps(context),result['status'],flush=True)
            local=Path('/local_datasets/pjw031003/capstone-shared-knowledge/simplify')/job
            local.mkdir(parents=True,exist_ok=False)
            for i,case in enumerate(json.loads((folder/'transfer-inputs.json').read_text())['cases']):
                outputs=[]
                for arm in (['joint','attributed'] if i%2==0 else ['attributed','joint']):
                    context.clear();context.update(split='transfer',case_id=case['id'],arm=arm)
                    service=(JointSourceQA if arm=='joint' else AttributedQA)(local/case['id']/arm,index_dir=local/case['id']/'index',**parts)
                    imported=service.import_history(case['records']);assert imported['llm_calls']==0
                    first=record['calls'];start=time.monotonic()
                    result=service.ask(case['question']);outputs.append(result)
                    record['rows'].append(dict(**context,result=result,calls=record['calls']-first,seconds=time.monotonic()-start))
                    save();print('STEP',json.dumps(context),result['status'],flush=True)
                assert outputs[0]['citation_sources']==outputs[1]['citation_sources'],'Retrieval differs between arms'
            assert len(record['rows'])==44
            record.update(status='complete',paired_retrieval_equal=True)
        finally:save();stream.close()


if __name__=='__main__':main()
