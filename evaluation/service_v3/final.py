"""One frozen comparison. Gold labels are saved separately, never sent to LLMs."""
import csv,io,json,os,re,sys,time
from copy import deepcopy
from hashlib import sha256,sha1
from pathlib import Path
from threading import Lock,RLock


TRACE_KEY = 'team_memory_service_state_trace'

def main(folder):
    cfg=json.loads((folder/'config.json').read_text())
    assert os.environ['SLURMD_NODENAME'] and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for n,h in cfg['code_sha256'].items():assert sha256((folder/'code'/n).read_bytes()).hexdigest()==h,n
    for n,h in cfg['data_sha256'].items():assert sha256((folder/n).read_bytes()).hexdigest()==h,n
    import httpx
    from llama_index.core import Document
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.retrievers.bm25 import BM25Retriever
    from llama_index.core.llms import ChatMessage
    from team_memory.reference_qa import local_components,format_response
    from team_memory.reference_attributed import AttributedQA,CitedSourceQA,attach_citations,repair_omitted_answer
    from team_memory.service import TeamMemoryService
    from team_memory.source_store import SourceStore
    from team_memory.store import digest
    from team_memory import timeline
    job=os.environ['SLURM_JOB_ID'];start=time.monotonic();context={};lock=Lock()
    out=Path(cfg['project'])/'results'/('service-v3-'+job+'.json')
    traces=out.with_suffix('.calls.jsonl').open('x')
    root=out.parent/('state-final-'+job);root.mkdir(exist_ok=False)
    record=dict(status='preparing',job_id=job,code_sha256=cfg['code_sha256'],data_sha256=cfg['data_sha256'],
        model_revision=cfg['model_revision'],rows=[],updates=[],reviews=[],calls=0,stores={},corpus_hashes={})
    keys={};packets=[];retrieval=[]
    def save():
        record['seconds']=time.monotonic()-start
        tmp=out.with_suffix('.tmp');tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2));tmp.replace(out)
    def request_hook(request):
        if not request.url.path.endswith('/chat/completions'):return
        with lock:
            if record['calls']>=cfg['max_calls']:raise RuntimeError('Frozen maximum physical calls exceeded')
            record['calls']+=1;body=json.loads(request.content)
            request.extensions[TRACE_KEY]=dict(id=record['calls'],context=dict(context),request=body,started=time.monotonic())
    def response_hook(response):
        response.read()
        if TRACE_KEY not in response.request.extensions:return
        with lock:
            t=response.request.extensions[TRACE_KEY]
            traces.write(json.dumps(dict(t,response=response.json(),seconds=time.monotonic()-t['started']),ensure_ascii=False)+'\n');traces.flush()
    def source(text,location,speaker,stamp):
        env=dict(owner=speaker,observed_at=stamp,source=dict(text=text,location=location,speaker=speaker))
        return dict(source_id=digest(env),quote=text,start=0,end=len(text),location=location,speaker=speaker,observed_at=stamp)
    def generate(system,content):
        return parts['llm'].chat([ChatMessage(role='system',content=system),ChatMessage(role='user',content=content)]).message.content
    def evaluate_packet(packet,arms):
        for arm in arms:
            context.clear();context.update(split=packet['split'],case_id=packet['id'],arm=arm)
            first=record['calls'];began=time.monotonic();w=packet['witnesses'];q=packet['question']
            reader=object.__new__(AttributedQA if arm=='attributed' else CitedSourceQA)
            reader.llm=parts['llm'];reader.lock=RLock();reader.active_review_context=None
            # Same actual initial prompt and packets, one fresh generation per arm.
            template=reader._team_templates()[0]
            ctx='\n\n'.join(f"Source {i}:\nrecord_author: {x['speaker']}\nrecorded_at: {x.get('observed_at')}\n\n{x['quote']}" for i,x in enumerate(w,1))
            draft=parts['llm'].chat([ChatMessage(role='user',content=template.format(context_str=ctx,query_str=q))]).message.content
            answer=format_response(q,draft,w,allow_source_labels=True)
            if arm=='attributed':
                answer=reader._review(q,answer)
                answer=repair_omitted_answer(q,answer,reader.llm)
            answer=attach_citations(reader,q,answer)
            if answer.get('aqa_candidate_accepted'):
                # Same public service qualification: source coverage is not proof.
                answer['status']='partial';answer['answer_revision_unverified']=True
            record['rows'].append(dict(**context,question=q,result=answer,calls=record['calls']-first,seconds=time.monotonic()-began))
            save();print('QA',packet['split'],packet['id'],arm,answer['status'],flush=True)
    save()
    try:
        with httpx.Client(trust_env=False,event_hooks={'request':[request_hook],'response':[response_hook]}) as client:
            parts=local_components(cfg['model_path'],cfg['embedding'],os.environ['PRACTICAL_MODEL_URL'],http_client=client)
            data=Path('/local_datasets/pjw031003/capstone-shared-knowledge/datasets-v1')
            manifest=json.loads((folder/'dataset-manifest.json').read_text())
            entries={d['repo'].split('/')[-1]:{f['path']:f for f in d['files']} for d in manifest['datasets']}
            def checked(path,repo,rel):
                raw=path.read_bytes();expected=entries[repo][rel]
                assert len(raw)==expected['bytes'],path
                assert sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==expected['git_blob_sha1'],path
                record['corpus_hashes'][str(path)]=sha256(raw).hexdigest()
                return raw
            exclusions=json.loads((folder/'exclusions.json').read_text());prior=set(exclusions['prior_keys'])
            seed=lambda s:sha256((exclusions['selection_seed']+s).encode()).hexdigest()
            for topic in ('03','04'):
                directory=data/'EverMemBench-Dynamic'/topic
                questions=json.loads(checked(directory/f'qa_{topic}.json','EverMemBench-Dynamic',f'{topic}/qa_{topic}.json'))
                days=json.loads(checked(directory/'dialogue.json','EverMemBench-Dynamic',f'{topic}/dialogue.json'))
                original={};by_location={};docs=[]
                for day in days:
                    for group,messages in day['dialogues'].items():
                        for i,m in enumerate(messages or [],1):
                            loc=f"EverMemBench-Dynamic@{cfg['ever_revision']}/{topic}/{day['date']}/{group}/{i}"
                            w=source(m['dialogue'],loc,m['speaker'],m['time']);original[w['source_id']]=w;by_location[loc]=w
                            docs.append(Document(id_=w['source_id'],text=w['quote'],metadata={'source_id':w['source_id']},excluded_embed_metadata_keys=['source_id'],excluded_llm_metadata_keys=['source_id']))
                splitter=SentenceSplitter(chunk_size=512,chunk_overlap=64,include_metadata=False,
                    tokenizer=lambda text:parts['tokenizer'].encode(text,add_special_tokens=False))
                nodes=splitter.get_nodes_from_documents(docs)
                retriever=BM25Retriever.from_defaults(nodes=nodes,similarity_top_k=8)
                for typ in ('F_SH','F_MH','F_TP'):
                    chosen=min((q for q in questions if q['id'].startswith(typ+'_') and q['id'] not in prior),key=lambda q:seed(q['id']))
                    ws=[];parents={}
                    for item in retriever.retrieve(chosen['Q']):
                        n=item.node;p=original[n.ref_doc_id];a=p['quote'].find(n.text,n.start_char_idx or 0);assert a>=0
                        ws.append(dict(p,quote=n.text,start=a,end=a+len(n.text)));parents[p['source_id']]=p
                    gold=[]
                    for ref in chosen['R']:
                        for segment in re.findall(r'\d+(?:\s*-\s*\d+)?',str(ref['message_index'])):
                            nums=list(map(int,re.findall(r'\d+',segment)))
                            for i in range(nums[0],nums[-1]+1):
                                loc=f"EverMemBench-Dynamic@{cfg['ever_revision']}/{topic}/{ref['date']}/{ref['group']}/{i}"
                                if loc in by_location:gold.append(by_location[loc])
                    q=chosen['Q']
                    if chosen.get('options'):q+='\nOptions:\n'+json.dumps(chosen['options'],ensure_ascii=False)+'\nBegin with the selected option letter and justify from the records.'
                    packets.append(dict(split='ever',id=chosen['id'],question=q,witnesses=ws,originals=parents))
                    keys[chosen['id']]=dict(native=chosen,gold_sources=gold)
                    retrieval.append(dict(id=chosen['id'],records=len(original),chunks=len(nodes),gold_count=len(gold),
                        retrieved_locations=[w['location'] for w in ws]))
            wiki_root=data/'Wikipedia_contradict_benchmark';rel='WikiContradict_dataset_v1_rag_qa.csv'
            raw=checked(wiki_root/rel,'Wikipedia_contradict_benchmark',rel)
            wiki=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
            chosen=sorted((q for q in wiki if 'wiki-'+q['question_ID'] not in prior),key=lambda q:seed('wiki:'+q['question_ID']))[:6]
            assert len(chosen)==6
            for q in chosen:
                cid='wiki-'+q['question_ID'];ws=[source(q[f'context{i}'],q['url']+f'#provided-context-{i}','Wikipedia',None) for i in (1,2)]
                packets.append(dict(split='wiki',id=cid,question=q['question'],witnesses=ws,originals={w['source_id']:w for w in ws}));keys[cid]=q
            for c in json.loads((folder/'legacy.json').read_text())['cases']:
                packets.append(dict(split='legacy',id=c['id'],question=c['question'],witnesses=c['witnesses']))
                keys[c['id']]=dict(expected=c['expected'],expected_evidence=c['expected_evidence'])
            # Selection and input packets are persisted before the first model call.
            assert record['calls']==0
            packet_path=out.with_suffix('.inputs.json');packet_path.write_text(json.dumps(dict(packets=packets,retrieval=retrieval),ensure_ascii=False,indent=2))
            out.with_suffix('.keys.json').write_text(json.dumps(keys,ensure_ascii=False,indent=2))
            record['input_sha256']=sha256(packet_path.read_bytes()).hexdigest();record['status']='running';save()
            for i,packet in enumerate(packets):evaluate_packet(packet,('direct','attributed') if i%2==0 else ('attributed','direct'))
            for i,c in enumerate(json.loads((folder/'streams.json').read_text())['cases']):
                path=root/c['id']
                apps={arm:TeamMemoryService(path,reader=klass(path,**parts),generate=generate) for arm,klass in [('direct',CitedSourceQA),('attributed',AttributedQA)]}
                app=apps['attributed'];app.import_history(c['initial'])
                context.clear();context.update(split='stream',case_id=c['id'],arm='shared_review');first=record['calls'];began=time.monotonic()
                update=app.ingest(c['incoming']);record['updates'].append(dict(id=c['id'],result=update,calls=record['calls']-first,seconds=time.monotonic()-began));save()
                for step in c['steps']:
                    if step['operation']=='review_fixture':
                        targets=[p for p in update['proposals'] if p['kind']=='correction' and p['previous']['source_id']==digest(app.store.source_envelope(c['initial'][0]))]
                        actions=[app.review(p['id'],p['reviewer'],step['choice']) for p in targets]
                        record['reviews'].append(dict(id=c['id'],step=step,applied=actions));save();continue
                    for arm in (('direct','attributed') if i%2==0 else ('attributed','direct')):
                        context.clear();context.update(split='stream',case_id=c['id']+'/'+step['label'],arm=arm)
                        first=record['calls'];began=time.monotonic()
                        answer=apps[arm].ask(step['question'],step.get('temporal_scope','current'))
                        record['rows'].append(dict(**context,question=step['question'],result=answer,calls=record['calls']-first,seconds=time.monotonic()-began));save()
                        print('QA','stream',context['case_id'],arm,answer['status'],flush=True)
                record['stores'][c['id']]={k:app.store.load(k) for k in ('sources','timeline_proposals','timeline_votes','review_snapshots')};save()
            assert len(record['rows'])==86,len(record['rows'])
            record['status']='complete'
    except BaseException as exc:
        record.update(status='failed',error=type(exc).__name__+': '+str(exc));raise
    finally:save();traces.close()


if __name__=='__main__':
    folder=Path(sys.argv[1])
    from evaluation.service_v3.dev import main as development_check
    development_check(folder)
    cfg=json.loads((folder/'config.json').read_text())
    devpath=Path(cfg['project'])/'results'/('state-development-'+os.environ['SLURM_JOB_ID']+'.json')
    dev=json.loads(devpath.read_text())
    assert dev['status']=='complete' and len(dev['rows'])==2
    assert all(r['result']['status']=='ok' and r['answer_preserved'] for r in dev['rows']), 'Known state citation gate failed; no final cases evaluated'
    main(folder)
