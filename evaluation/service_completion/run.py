"""Fresh full-source QA and real headless service flows; keys are never loaded."""
import json,os,sys,time
from pathlib import Path
from hashlib import sha256
from threading import Lock

TRACE_KEY='team_memory_completion_trace'


def main(folder):
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ['SLURMD_NODENAME'] and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for n,h in cfg['code_sha256'].items():assert sha256((folder/'code'/n).read_bytes()).hexdigest()==h,n
    for n,h in cfg['data_sha256'].items():assert sha256((folder/n).read_bytes()).hexdigest()==h,n
    import httpx
    from llama_index.core.llms import ChatMessage
    from team_memory.reference_qa import local_components
    from team_memory.reference_attributed import AttributedQA
    from team_memory.service import TeamMemoryService
    job=os.environ['SLURM_JOB_ID'];start=time.monotonic();lock=Lock();context={}
    out=Path(cfg['project'])/'results'/('service-completion-'+job+'.json')
    assert not out.exists();trace=out.with_suffix('.calls.jsonl').open('x')
    # Node-local fsync avoids shared-Ceph per-object latency. All original sources,
    # proposals, votes and snapshots are exported below; no inference on login node.
    root=Path(cfg.get('store_root',str(out.parent)))/('completion-stores-'+job)
    root.mkdir(parents=True,exist_ok=False)
    result=dict(status='running',job_id=job,code_sha256=cfg['code_sha256'],data_sha256=cfg['data_sha256'],
                calls=0,rows=[],stores={},source_version=cfg['source_version'])
    def save():
        result['seconds']=time.monotonic()-start
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2));tmp.replace(out)
    def request(request):
        if not request.url.path.endswith('/chat/completions'):return
        with lock:
            if result['calls']>=cfg['max_calls']:raise RuntimeError('Fixed call maximum reached')
            result['calls']+=1
            request.extensions[TRACE_KEY]=dict(id=result['calls'],context=dict(context),request=json.loads(request.content),started=time.monotonic())
    def response(response):
        response.read();t=response.request.extensions.get(TRACE_KEY)
        if t:
            with lock:
                trace.write(json.dumps(dict(t,response=response.json(),seconds=time.monotonic()-t['started']),ensure_ascii=False)+'\n');trace.flush()
    save()
    try:
        with httpx.Client(trust_env=False,event_hooks={'request':[request],'response':[response]}) as client:
            parts=local_components(cfg['model_path'],cfg['embedding'],os.environ['PRACTICAL_MODEL_URL'],http_client=client)
            def generate(system,content):return parts['llm'].chat([ChatMessage(role='system',content=system),ChatMessage(role='user',content=content)]).message.content
            def service(cid):
                path=root/cid
                return TeamMemoryService(path,reader=AttributedQA(path,**parts),generate=generate)
            def execute(svc,cid,split,step):
                context.clear();context.update(case_id=cid,split=split,label=step['label'])
                before=result['calls'];began=time.monotonic()
                req={k:v for k,v in step.items() if k!='label'}
                answer=svc.handle(req)
                result['rows'].append(dict(**context,request=req,result=answer,calls=result['calls']-before,seconds=time.monotonic()-began))
                save();print('STEP',cid,step['label'],answer['status'],flush=True)
                return answer
            inputs=json.loads((folder/'inputs.json').read_text())
            # Known state failures first; failures are recorded, not silently skipped.
            for split in ('streams','transfer'):
                for c in inputs[split]:
                    cid=c['id'];svc=service(cid)
                    execute(svc,cid,split,dict(label='import',operation='import_history',records=c['initial']))
                    execute(svc,cid,split,dict(label='ingest',operation='ingest',source=c['incoming']))
                    for step in c['steps']:
                        if step['operation']=='restart':
                            svc=service(cid);execute(svc,cid,split,dict(label=step['label'],operation='sync'));continue
                        if step['operation'] in ('review_fixture','conflicting_votes_fixture'):
                            proposals=svc.handle(dict(operation='view'))['relations']
                            if step['operation']=='review_fixture':
                                for p in proposals:execute(svc,cid,split,dict(label=step['label'],operation='review',proposal_id=p['id'],actor=p['reviewer'],choice=step['choice']))
                            else:
                                # Models two valid owner votes arriving from separate clones.
                                for p in proposals:
                                    for choice in ('approve','reject'):svc.store.put('timeline_votes',dict(proposal=p['id'],actor=p['reviewer'],choice=choice))
                            continue
                        execute(svc,cid,split,step)
                    result['stores'][cid]={name:svc.store.load(name) for name in ('sources','timeline_proposals','timeline_votes','review_snapshots')};save()
            for c in inputs['legacy']:
                svc=service(c['id'])
                for step in c['events']:execute(svc,c['id'],'legacy',step)
                result['stores'][c['id']]={'sources':svc.store.load('sources')};save()
            assert sum(r['request']['operation']=='ask' for r in result['rows'])==37
            result['status']='complete'
    except BaseException as exc:
        result.update(status='failed',error=type(exc).__name__+': '+str(exc));raise
    finally:save();trace.close()


if __name__=='__main__':main(Path(sys.argv[1]))
