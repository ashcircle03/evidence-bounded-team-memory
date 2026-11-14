"""Fixed service, replace only comparator; fixture/replayed judgments are explicit."""
import json,os,sys,time
from pathlib import Path
from hashlib import sha256
from threading import Lock


def main(folder):
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ['SLURMD_NODENAME'] and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for name,h in cfg['code_sha256'].items():assert sha256((folder/'code'/name).read_bytes()).hexdigest()==h,name
    for name,h in cfg['data_sha256'].items():assert sha256((folder/name).read_bytes()).hexdigest()==h,name
    import httpx
    from team_memory.source_store import SourceStore
    from team_memory.service import TeamMemoryService
    from team_memory import timeline
    job=os.environ['SLURM_JOB_ID'];start=time.monotonic();context={};lock=Lock()
    out=Path(cfg['project'])/'results'/('comparator-choice-'+job+'.json');assert not out.exists()
    trace=out.with_suffix('.calls.jsonl').open('x')
    root=Path('/local_datasets/pjw031003/capstone-shared-knowledge/choice-stores')/job
    root.mkdir(parents=True,exist_ok=False)
    result=dict(status='running',job_id=job,mode=cfg['mode'],model=cfg['model_repo'],revision=cfg['model_revision'],
                calls=0,rows=[],stores={},selectors=[],source_version=cfg['source_version'],
                code_sha256=cfg['code_sha256'],data_sha256=cfg['data_sha256'])
    def save():
        result['seconds']=time.monotonic()-start
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2));tmp.replace(out)
    def request(req):
        if not req.url.path.endswith('/chat/completions'):return
        with lock:
            if result['calls']>=cfg['max_calls']:raise RuntimeError('Fixed request limit reached')
            result['calls']+=1
            req.extensions['choice_trace']=dict(id=result['calls'],context=dict(context),request=json.loads(req.content),started=time.monotonic())
    def response(resp):
        resp.read();t=resp.request.extensions.get('choice_trace')
        if t:
            with lock:trace.write(json.dumps(dict(t,response=resp.json(),seconds=time.monotonic()-t['started']),ensure_ascii=False)+'\n');trace.flush()
    save()
    try:
        with httpx.Client(trust_env=False,timeout=90,event_hooks={'request':[request],'response':[response]}) as client:
            parts=None
            comparator_tokenizer=None
            if cfg['mode']=='compare':
                from transformers import AutoTokenizer
                from team_memory.reference_qa import guard_request
                comparator_tokenizer=AutoTokenizer.from_pretrained(cfg['model_path'],local_files_only=True)
            if cfg['mode']!='compare':
                from team_memory.reference_qa import local_components
                from team_memory.reference_attributed import AttributedQA
                parts=local_components(cfg['model_path'],cfg['embedding'],os.environ['PRACTICAL_MODEL_URL'],http_client=client)
            class ImportReader:
                def __init__(self,path):self.store=SourceStore(path)
                def import_history(self,records):return dict(status='ok',source_ids=[self.store.capture_source(e) for e in records])
            inputs=json.loads((folder/'inputs.json').read_text())
            replays=json.loads((folder/'replays.json').read_text()) if cfg['mode']=='flow' else {}
            for case in inputs['cases']:
                cid=case['id'];path=root/cid
                def generate(system,content):
                    if cfg['mode']=='oracle':
                        row=dict(case['selector'],target=json.loads(content)['earlier'][0]['id'])
                        raw=json.dumps(dict(relations=[row]));origin='supplied_correct_relation_fixture'
                    elif cfg['mode']=='flow':
                        saved=replays[cid]
                        assert saved['system']==system and saved['content']==content,cid
                        raw=saved['raw'];origin='exact_recorded_comparator_output'
                    else:
                        # Validate context using this comparator's own tokenizer; no truncation.
                        body=dict(model=cfg['served_model'],messages=[dict(role='system',content=system),dict(role='user',content=content)],
                            temperature=0.0,max_tokens=1024,stream=False,chat_template_kwargs=dict(enable_thinking=False))
                        req=client.build_request('POST',os.environ['PRACTICAL_MODEL_URL']+'/chat/completions',json=body)
                        guard_request(comparator_tokenizer)(req)
                        resp=client.send(req);resp.raise_for_status()
                        raw=resp.json()['choices'][0]['message']['content'];origin='fresh_local_model'
                    result['selectors'].append(dict(case_id=cid,system=system,content=content,raw=raw,origin=origin))
                    return raw
                def service():
                    return TeamMemoryService(path,reader=AttributedQA(path,**parts) if parts else ImportReader(path),generate=generate)
                svc=service()
                def execute(step):
                    context.clear();context.update(case_id=cid,label=step['label'],split=case['split'])
                    req={k:v for k,v in step.items() if k!='label'};before=result['calls'];began=time.monotonic()
                    answer=svc.handle(req)
                    result['rows'].append(dict(**context,request=req,result=answer,calls=result['calls']-before,seconds=time.monotonic()-began))
                    save();print('STEP',cid,step['label'],answer['status'],flush=True)
                    return answer
                execute(dict(label='import',operation='import_history',records=case['initial']))
                if 'incoming' in case:execute(dict(label='ingest',operation='ingest',source=case['incoming']))
                for step in case.get('steps',[]):
                    if step['operation']=='restart':svc=service();execute(dict(label=step['label'],operation='sync'))
                    elif step['operation']=='review_fixture':
                        for p in timeline.proposals(svc.store):execute(dict(label=step['label'],operation='review',proposal_id=p['id'],actor=p['reviewer'],choice=step['choice']))
                    elif step['operation']=='conflicting_votes_fixture':
                        for p in timeline.proposals(svc.store):
                            for choice in ('approve','reject'):svc.store.put('timeline_votes',dict(proposal=p['id'],actor=p['reviewer'],choice=choice))
                    else:execute(step)
                result['stores'][cid]={name:svc.store.load(name) for name in ('sources','timeline_proposals','timeline_votes','review_snapshots')};save()
            assert sum(r['request']['operation']=='ask' for r in result['rows'])==cfg['expected_qa']
            assert len(result['selectors'])==cfg['expected_comparisons']
            result['status']='complete'
    except BaseException as exc:
        result.update(status='failed',error=type(exc).__name__+': '+str(exc));raise
    finally:save();trace.close()


if __name__=='__main__':main(Path(sys.argv[1]))
