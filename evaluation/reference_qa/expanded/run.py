"""Frozen development expansion. Keys never enter model messages or retrieval.

QA20+old12 regression; pure order pair;10 native EverMem development questions;
8 WikiContradict questions under individual and paired passage conditions.
"""
from collections import Counter
from hashlib import sha256
import csv,json,os,re,sys,time
from pathlib import Path
from threading import Lock


def iter_dialogue_messages(days):
    """Native null groups have no messages; retain all nonempty groups verbatim."""
    for day in days:
        for group,messages in day['dialogues'].items():
            if messages is None:continue
            if not isinstance(messages,list):raise TypeError('Expected native message list or null')
            for index,message in enumerate(messages,1):yield day['date'],group,index,message


def main():
    folder=Path(sys.argv[1]);cfg=json.loads((folder/'config.json').read_text())
    assert os.environ['SLURMD_NODENAME'] and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for n,h in cfg['code_sha256'].items():assert sha256((folder/'code'/n).read_bytes()).hexdigest()==h,n
    for n,h in cfg['data_sha256'].items():assert sha256((folder/n).read_bytes()).hexdigest()==h,n
    for n,h in cfg.get('resume_sha256',{}).items():assert sha256((folder/n).read_bytes()).hexdigest()==h,n
    sys.path.insert(0,str(folder/'code'))
    import httpx
    from llama_index.core import Document
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.retrievers.bm25 import BM25Retriever
    from llama_index.core.llms import ChatMessage
    from team_memory.reference_qa import local_components
    from team_memory.reference_joint import joint_template,format_joint
    from team_memory.reference_claims import answer_from_sources
    from team_memory.store import digest
    job=os.environ['SLURM_JOB_ID'];began=time.monotonic();context={};lock=Lock()
    out=Path(cfg['project'])/'results'/f'cup-expanded-{job}.json'
    traces=out.with_suffix('.calls.jsonl').open('x',encoding='utf-8')
    keys={};selection=[];retrieval_audit=[]
    result=dict(status='running',job_id=job,source_version=cfg['source_version'],code_sha256=cfg['code_sha256'],
                data_sha256=cfg['data_sha256'],rows=[],calls=0,external_model_api_calls=0)
    if cfg.get('resume_sha256'):
        prior=json.loads((folder/'prior-result.json').read_text());prior_calls=(folder/'prior-calls.jsonl').read_text()
        assert len(prior['rows'])==36 and prior['calls']==len(prior_calls.splitlines())
        result.update(rows=prior['rows'],calls=prior['calls'],reused_calls=prior['calls'],reused_job_id=prior['job_id'])
        traces.write(prior_calls);traces.flush()
    completed={(r['split'],r['case_id'],r['arm']):r for r in result['rows']}
    def save():
        result['seconds']=time.monotonic()-began
        result['new_calls']=result['calls']-result.get('reused_calls',0)
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(out)
        keypath=out.with_suffix('.keys.json');keytmp=out.with_suffix('.keys.tmp')
        keytmp.write_text(json.dumps(dict(keys=keys,selection=selection,retrieval=retrieval_audit),ensure_ascii=False,indent=2),encoding='utf-8');keytmp.replace(keypath)
    def request_hook(request):
        if not request.url.path.endswith('/chat/completions'):return
        body=json.loads(request.content)
        with lock:
            if result['calls']>=cfg['max_calls'] or time.monotonic()-began>cfg['client_seconds']-45:
                raise RuntimeError('Frozen request/time cap reached')
            request.extensions['reference_trace']=dict(id=result['calls'],context=dict(context),request=body,
                rendered_prompt_tokens=len(parts['tokenizer'].apply_chat_template(body['messages'],tokenize=True,add_generation_prompt=True,enable_thinking=False)))
            assert request.extensions['reference_trace']['rendered_prompt_tokens']+body['max_tokens']<=32768
            result['calls']+=1
    def response_hook(response):
        response.read();trace=response.request.extensions.get('reference_trace')
        if trace:
            traces.write(json.dumps(dict(trace,response=response.json(),http_status=response.status_code),ensure_ascii=False)+'\n');traces.flush()
    def evaluate(split,cid,question,witnesses,arms=('joint','claims')):
        for arm in arms:
            if (split,cid,arm) in completed:
                prior=completed[split,cid,arm]
                assert prior['question']==question and prior['retrieval_sources']==witnesses
                continue
            context.clear();context.update(split=split,case_id=cid,arm=arm)
            first=result['calls'];start=time.monotonic()
            if arm=='claims':answer=answer_from_sources(question,witnesses,parts['llm'])
            else:
                ctx='\n\n'.join(f"Source {i}:\nrecord_author: {w['speaker']}\nrecorded_at: {w.get('observed_at','unknown')}\n{w['quote']}" for i,w in enumerate(witnesses,1))
                raw=parts['llm'].chat([ChatMessage(role='user',content=joint_template().format(context_str=ctx,query_str=question))]).message.content
                answer=format_joint(question,raw,witnesses)
            result['rows'].append(dict(**context,question=question,retrieval_sources=witnesses,result=answer,calls=result['calls']-first,seconds=time.monotonic()-start))
            save();print('STEP',split,cid,arm,answer['status'],flush=True)
    def source(text,location,speaker='Wikipedia',stamp=None):
        # Dataset witnesses are immutable read-only evidence, not Store imports.
        # Keep native timezone-unspecified text; never invent an offset or Wiki date.
        env=dict(owner=speaker,observed_at=stamp,source=dict(text=text,location=location,speaker=speaker))
        return dict(source_id=digest(env),quote=text,start=0,end=len(text),location=location,speaker=speaker,observed_at=stamp)
    save()
    with httpx.Client(trust_env=False,event_hooks={'request':[request_hook],'response':[response_hook]}) as client:
        parts=local_components(cfg['model_path'],cfg['embedding'],os.environ['PRACTICAL_MODEL_URL'],http_client=client)
        try:
            regressions=json.loads((folder/'regressions.json').read_text())
            for c in regressions['cases']:evaluate(c['split'],c['id'],c['question'],c['witnesses'],('claims',))
            for c in regressions['order']:
                evaluate('order',c['id'],c['question'],[source(c['text'],'controlled:order','Recorder')])
            data=Path('/local_datasets/pjw031003/capstone-shared-knowledge/datasets-v1')
            seed=lambda item:sha256(('claim-evidence-v1:'+item).encode()).hexdigest()
            for topic in ['01','02']:
                root=data/'EverMemBench-Dynamic'/topic
                rows=json.loads((root/f'qa_{topic}.json').read_text())
                chosen=[]
                for typ in ['F_SH','F_MH','F_TP','MA_U','MA_P']:
                    chosen.append(min([q for q in rows if q['id'].startswith(typ+'_') and q['id'] not in cfg['excluded_ever_ids']],key=lambda q:seed(q['id'])))
                original={};docs=[]
                for date,group,i,m in iter_dialogue_messages(json.loads((root/'dialogue.json').read_text())):
                    location=f"EverMemBench-Dynamic@{cfg['ever_revision']}/{topic}/{date}/{group}/{i}"
                    w=source(m['dialogue'],location,m['speaker'],m['time']);original[w['source_id']]=w
                    docs.append(Document(id_=w['source_id'],text=w['quote'],metadata={'source_id':w['source_id']},
                        excluded_embed_metadata_keys=['source_id'],excluded_llm_metadata_keys=['source_id']))
                splitter=SentenceSplitter(chunk_size=512,chunk_overlap=64,include_metadata=False,
                    tokenizer=lambda text:parts['tokenizer'].encode(text,add_special_tokens=False))
                nodes=splitter.get_nodes_from_documents(docs)
                retriever=BM25Retriever.from_defaults(nodes=nodes,similarity_top_k=8)
                for q in chosen:
                    witnesses=[]
                    for n in retriever.retrieve(q['Q']):
                        node=n.node;parent=original[node.ref_doc_id];text=node.text
                        start=parent['quote'].find(text,node.start_char_idx or 0)
                        assert start>=0
                        witnesses.append(dict(parent,quote=text,start=start,end=start+len(text)))
                    question=q['Q']
                    if q.get('options'):
                        question+='\nOptions:\n'+json.dumps(q['options'],ensure_ascii=False)+'\nBegin your answer with the selected option letter and justify it from the records.'
                    keys[q['id']]=q;selection.append(q['id'])
                    gold=[]
                    for ref in q['R']:
                        for segment in re.findall(r'\d+(?:\s*-\s*\d+)?',str(ref['message_index'])):
                            nums=list(map(int,re.findall(r'\d+',segment)))
                            for idx in range(nums[0],nums[-1]+1):gold.append(f"EverMemBench-Dynamic@{cfg['ever_revision']}/{topic}/{ref['date']}/{ref['group']}/{idx}")
                    retrieval_audit.append(dict(id=q['id'],corpus_records=len(original),chunks=len(nodes),
                        gold_reference_locations=sorted(set(gold)),retrieved_locations=[w['location'] for w in witnesses]))
                    evaluate('ever',q['id'],question,witnesses,('joint','claims') if len(selection)%2 else ('claims','joint'))
            with (data/'Wikipedia_contradict_benchmark/WikiContradict_dataset_v1_rag_qa.csv').open(encoding='utf-8-sig') as f:wiki=list(csv.DictReader(f))
            assert len(wiki)==253 and len({q['question_ID'] for q in wiki})==253
            chosen=sorted(wiki,key=lambda q:seed('wiki:'+q['question_ID']))[:8]
            for q in chosen:
                cid='wiki-'+q['question_ID'];keys[cid]=q;selection.append(cid)
                evidence=[source(q[f'context{i}'],q['url']+f'#provided-context-{i}') for i in [1,2]]
                for condition,ws in [('single1',evidence[:1]),('single2',evidence[1:]),('both',evidence)]:
                    evaluate('wiki',cid+'/'+condition,q['question'],ws,
                             ('joint','claims') if int(q['question_ID'])%2 else ('claims','joint'))
            # Evaluator-only native labels are saved separately, never put in prompts.
            out.with_suffix('.keys.json').write_text(json.dumps(dict(keys=keys,selection=selection,retrieval=retrieval_audit),ensure_ascii=False,indent=2),encoding='utf-8')
            assert len(result['rows'])==104,len(result['rows'])
            result.update(status='complete',selected_ever=10,selected_wiki=8,wiki_conditions=3,
                selection=selection,scope='Development pilot: projects01/02 only; native QA, fixed-passage Wiki and prior regression reader inputs. Not full benchmark or merge evaluation.')
        finally:save();traces.close()


if __name__=='__main__':main()
