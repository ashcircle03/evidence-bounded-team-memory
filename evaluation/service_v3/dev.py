"""Two known attribution failures; existing answer bytes are immutable."""
import json, os, sys, time
from hashlib import sha256
from pathlib import Path
from threading import Lock


TRACE_KEY = 'team_memory_service_state_trace'

def main(folder):
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ['SLURMD_NODENAME'] and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for n,h in cfg['code_sha256'].items():assert sha256((folder/'code'/n).read_bytes()).hexdigest()==h,n
    for n,h in cfg['data_sha256'].items():assert sha256((folder/n).read_bytes()).hexdigest()==h,n
    import httpx
    from team_memory.reference_qa import local_components,format_response
    from team_memory.reference_quotes import add_quote_citations
    from team_memory.review_citations import review_sources
    from team_memory.source_store import SourceStore
    from team_memory import timeline
    job=os.environ['SLURM_JOB_ID'];out=Path(cfg['project'])/'results'/('state-development-'+job+'.json')
    trace=out.with_suffix('.calls.jsonl').open('x');lock=Lock();context={}
    record=dict(status='running',job_id=job,code_sha256=cfg['code_sha256'],data_sha256=cfg['data_sha256'],rows=[],calls=0)
    def save():out.write_text(json.dumps(record,ensure_ascii=False,indent=2))
    def request(request):
        if request.url.path.endswith('/chat/completions'):
            with lock:
                assert record['calls']<cfg['max_calls']
                record['calls']+=1
                request.extensions[TRACE_KEY]=dict(id=record['calls'],context=dict(context),request=json.loads(request.content))
    def response(response):
        response.read()
        with lock:
            trace.write(json.dumps(dict(response.request.extensions[TRACE_KEY],response=response.json()),ensure_ascii=False)+'\n');trace.flush()
    data=json.loads((folder/'dev.json').read_text());save()
    try:
        with httpx.Client(trust_env=False,event_hooks={'request':[request],'response':[response]}) as client:
            parts=local_components(cfg['model_path'],cfg['embedding'],os.environ['PRACTICAL_MODEL_URL'],http_client=client)
            for row in data['cases']:
                context['case_id']=row['label'];store=SourceStore(out.parent/('state-dev-'+job+'-'+row['label']))
                for e in data['sources']:store.capture_source(e)
                for p in row['context']['relations']:
                    obj={k:v for k,v in p.items() if k not in ('id','status')}
                    assert store.put('timeline_proposals',obj)==p['id']
                    if p['status']=='approved':timeline.review(store,p['id'],p['reviewer'],'approve')
                events=review_sources(store,row['context'])
                before=format_response(row['question'],row['raw'],row['witnesses'],allow_source_labels=True)
                after=add_quote_citations(row['question'],before,parts['llm'],review_witnesses=events)
                # Only inserted citation labels may differ, exactly at stored offsets.
                rebuilt=row['raw']
                for op in reversed(after.get('posthoc_citations',[])):
                    rebuilt=rebuilt[:op['start']]+f"[{op['number']}] "+rebuilt[op['start']:]
                assert rebuilt==after['raw']
                for w in before['answers'][0]['evidence']:assert w in after['answers'][0]['evidence']
                record['rows'].append(dict(id=row['label'],result=after,events=events,answer_preserved=True));save()
                print('DEV',row['label'],after['status'],flush=True)
        record['status']='complete'
    finally:save();trace.close()


if __name__=='__main__':main(Path(sys.argv[1]))
