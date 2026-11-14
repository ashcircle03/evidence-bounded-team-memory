"""Frozen raw-vs-linked diagnosis on one local Qwen. No scoring key is loaded."""
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
from threading import Lock
import time


def main(folder):
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURMD_NODENAME') and os.environ.get('CONDA_PREFIX')==cfg['conda_prefix']
    for name,h in cfg['code_sha256'].items():assert sha256((folder/'code'/name).read_bytes()).hexdigest()==h,name
    for name,h in cfg['data_sha256'].items():assert sha256((folder/name).read_bytes()).hexdigest()==h,name
    import httpx
    from transformers import AutoTokenizer
    from llama_index.llms.openai_like import OpenAILike
    from llama_index.core.llms import ChatMessage
    from llama_index.core.embeddings import MockEmbedding
    from team_memory.readers.retrieval import guard_request
    from team_memory.readers.attribution import AttributedQA
    from team_memory.records.graph import construct
    from team_memory.adapters.records import RecordsAdapter
    from team_memory.adapters.answering import AnsweringAdapter
    from team_memory.adapters.reader_bridge import evidence_from,witnesses_from
    from team_memory.adapters.base import request
    from team_memory.contracts.ports import CallContext
    job=os.environ['SLURM_JOB_ID'];out=Path(cfg['project'])/'results'/('record-graph-'+job+'.json')
    assert not out.exists()
    record=dict(status='preparing',job_id=job,model_revision=cfg['model_revision'],input_sha256=cfg['data_sha256']['inputs.json'],
                code_sha256=cfg['code_sha256'],data_sha256=cfg['data_sha256'],calls=0,sources=[],rows=[],external_model_api_calls=0)
    start=time.monotonic();lock=Lock();current={}
    def save():
        record['seconds']=time.monotonic()-start
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2));tmp.replace(out)
    with out.with_suffix('.calls.jsonl').open('x') as trace:
        def on_request(req):
            if req.url.path.endswith('/chat/completions'):
                with lock:
                    if record['calls']>=cfg['max_calls']:raise RuntimeError('Physical request budget reached')
                    record['calls']+=1
                    req.extensions['record_trace']=dict(id=record['calls'],context=deepcopy(current),request=json.loads(req.content))
        def on_response(res):
            res.read()
            if 'record_trace' in res.request.extensions:
                with lock:
                    trace.write(json.dumps(dict(res.request.extensions['record_trace'],response=res.json()),ensure_ascii=False)+'\n');trace.flush()
        try:
            tokenizer=AutoTokenizer.from_pretrained(cfg['model_path'],local_files_only=True)
            with httpx.Client(trust_env=False,event_hooks={'request':[guard_request(tokenizer),on_request],'response':[on_response]}) as client:
                def model(max_tokens):
                    return OpenAILike(model='Qwen3-8B',api_base=os.environ['PRACTICAL_MODEL_URL'],api_key='local-no-secret',
                        is_chat_model=True,is_function_calling_model=False,context_window=32768,max_tokens=max_tokens,
                        tokenizer=tokenizer,temperature=0,timeout=180,max_retries=0,http_client=client,
                        additional_kwargs={'extra_body':{'chat_template_kwargs':{'enable_thinking':False},'seed':42}})
                writer=model(2048);reader_llm=model(1024)
                def generate(system,content):return writer.chat([ChatMessage(role='system',content=system),ChatMessage(role='user',content=content)]).message.content
                inputs=json.loads((folder/'inputs.json').read_text())
                # Construct ALL records without passing questions to the writer.
                enriched={}
                for case in inputs['cases']:
                    for source in case['sources']:
                        if source['id'] in enriched:continue
                        current.clear();current.update(stage='record_construction',source_id=source['id'])
                        enriched[source['id']]=construct(source,generate,model='Qwen3-8B@'+cfg['model_revision'])
                        record['sources'].append(enriched[source['id']]);save()
                record['status']='running'
                context=CallContext('graph-eval','owner',frozenset(['records:read','records:write','records:import','answer:generate']))
                for case_index,case in enumerate(inputs['cases']):
                    arms=['raw','linked'] if case_index%2==0 else ['linked','raw']
                    for arm in arms:
                        current.clear();current.update(stage='qa',case_id=case['id'],arm=arm)
                        base=Path(cfg['store_root'])/('record-graph-'+job)/case['id']/arm
                        port=RecordsAdapter(base,'graph-eval')
                        for i,source in enumerate(case['sources']):
                            value=enriched[source['id']] if arm=='linked' else source
                            response=port.handle(request('record.append',dict(source=value,expected_revision=i,idempotency_key=str(i)),workspace_id='graph-eval',request_id=str(i)),context=context)
                            assert response['status']=='ok',response
                        snapshot=RecordsAdapter(base,'graph-eval').snapshot()
                        evidence=[]
                        for i,source in enumerate(case['sources'],1):
                            w=dict(source_id=source['id'],start=0,end=len(source['text']),quote=source['text'])
                            evidence.append(evidence_from(w,snapshot,i))
                        bundle=dict(snapshot=snapshot,query=dict(text=case['question'],time_scope='current',as_of=None,conditions=[]),
                                    evidence=evidence,coverage='hits',unresolved_proposal_ids=[])
                        factory=lambda s:AttributedQA(s,llm=reader_llm,embed_model=MockEmbedding(embed_dim=8),tokenizer=tokenizer,
                                                       context_window=32768,num_output=1024)
                        adapter=AnsweringAdapter('graph-eval',factory,base/'private',snapshot_loader=port.snapshot)
                        first=record['calls']
                        answer=adapter.handle(request('answer.generate',dict(bundle=bundle),workspace_id='graph-eval',request_id=case['id']),context=context)
                        record['rows'].append(dict(case_id=case['id'],arm=arm,bundle=bundle,reader_witnesses=witnesses_from(bundle),
                                                   answer=answer,calls=record['calls']-first))
                        save()
                record['status']='complete'
        except BaseException as exc:
            record.update(status='failed',error=type(exc).__name__+': '+str(exc));raise
        finally:save()


if __name__=='__main__':main(Path(sys.argv[1]))
