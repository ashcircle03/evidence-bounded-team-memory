"""Profile cache/batching independently, then check the fixed20 retrieval cases."""
import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
import time


def run(packet,output):
    import torch
    from pydantic import PrivateAttr
    from transformers import AutoTokenizer
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.openai_like import OpenAILike
    from team_memory.readers.retrieval import ReferenceQA
    from team_memory.adapters.legacy import MutableView
    from evaluation.storage_cost.instrumentation import Timings,instrument,intervention,current

    cfg=json.loads((packet/'config.json').read_text());root=Path(__file__).resolve().parents[2]
    filehash=lambda p:sha256(p.read_bytes()).hexdigest()
    for name,h in cfg['code_sha256'].items():assert filehash(root/name)==h,name
    for name,h in cfg['data_sha256'].items():assert filehash(packet/name)==h,name
    assert torch.cuda.is_available(),'GPU required; no CPU fallback'
    class MeasuredEmbedding(HuggingFaceEmbedding):
        _batches:list=PrivateAttr(default_factory=list)
        _queries:int=PrivateAttr(default=0)
        _meter:object=PrivateAttr(default=None)
        def _get_text_embeddings(self,texts):
            self._batches.append(len(texts))
            if self._meter:
                with self._meter.measure('embedding_compute'):return super()._get_text_embeddings(texts)
            return super()._get_text_embeddings(texts)
        def _get_query_embedding(self,q):
            self._queries+=1;return super()._get_query_embedding(q)
    embed=MeasuredEmbedding(model_name=cfg['embedding'],device='cuda',embed_batch_size=32)
    tokenizer=AutoTokenizer.from_pretrained(cfg['model_path'],local_files_only=True)
    llm=OpenAILike(model='Qwen3-8B',api_base='http://127.0.0.1:1/v1',api_key='unused-local',
        is_chat_model=True,tokenizer=tokenizer,context_window=32768,max_tokens=1024,max_retries=0)
    opts=dict(llm=llm,embed_model=embed,tokenizer=tokenizer,context_window=32768,num_output=1024,profile='team')
    inputs=json.loads((packet/'inputs.json').read_text());cases=inputs['cases']
    report=dict(job_id=os.environ.get('SLURM_JOB_ID'),node=os.uname().nodename,gpu=torch.cuda.get_device_name(),
        input_sha256=filehash(packet/'inputs.json'),config_sha256=filehash(packet/'config.json'),
        fresh_llm_calls=0,completed=False,ablations=[],phases=[],rows=[],warmup_documents=1)
    # Same immutable checkpoint as the previous actual retrieval run.
    checkpoint=Path(cfg['embedding']);prior=json.loads((packet/'prior-retrieval.json').read_text())
    report['embedding_files_sha256']={name:filehash(checkpoint/name) for name in prior['embedding_files_sha256']}
    assert report['embedding_files_sha256']==prior['embedding_files_sha256']
    assert report['input_sha256']==prior['input_sha256']
    embed.get_text_embedding('Embedding warmup, not a corpus record.')
    def save():
        output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    def make(path,sources):
        # Production module adapters use this in-memory record view as well.
        # Index/cache remain on the same Ceph filesystem as v1. Avoid timing
        # thousands of unrelated fixture-source file writes a second time.
        return ReferenceQA(MutableView(path,dict(sources=sources)),**opts)
    def phase(cid,label,fn,module=current):
        meter=Timings();before=len(embed._batches);queries=embed._queries;embed._meter=meter
        try:
            with instrument(module,meter),meter.measure('total'):value=fn()
        finally:embed._meter=None
        row=dict(case_id=cid,phase=label,document_embeddings=sum(embed._batches[before:]),
            embedding_batches=embed._batches[before:],query_embeddings=embed._queries-queries,
            seconds=meter.rows['total']['seconds'],timings=dict(meter.rows))
        if isinstance(value,dict) and 'prepared_documents' in value:row['preparation']=value
        return value,row
    def ask(reader,qs):return [reader.ask(q['question'],retrieve_only=True)['witnesses'] for q in qs]
    with tempfile.TemporaryDirectory(prefix='storage-cost-',dir=cfg['scratch']) as temp:
        temp=Path(temp);case=cases[0];reference=None
        orders=[['previous','batch_only','cache_only','combined'],['combined','cache_only','batch_only','previous']]
        for repetition,order in enumerate(orders):
            for arm in order:
                reader=make(temp/f'ablation-{repetition}-{arm}',case['sources'])
                with intervention(arm,reader,case['sources']) as module:
                    _,row=phase(case['id'],arm,lambda:module.prepare(reader,reader.store.load('sources')),module)
                witnesses=ask(reader,case['questions'])
                if reference is None:reference=witnesses
                row.update(repetition=repetition,witnesses_equal=witnesses==reference)
                report['ablations'].append(row);save();print(json.dumps(dict(arm=arm,repetition=repetition,seconds=row['seconds'])),flush=True)
        for case in cases:
            cid=case['id'];reader=make(temp/cid/'incremental',case['sources']);qs=case['questions']
            def record(label,fn):
                value,row=phase(cid,label,fn);report['phases'].append(row);return value
            record('initial_prepare',reader.prepare_index)
            initial=record('first_questions',lambda:ask(reader,qs))
            reader=make(reader.store.root,reader.store.load('sources'))
            restarted=record('restart_questions',lambda:ask(reader,qs))
            extra=dict(owner='storage-fixture',observed_at='2026-01-01T00:00:00Z',source=dict(speaker='storage-fixture',
                location='synthetic://storage-unrelated/'+cid,text='The spare telemetry marker in the storage lifecycle fixture is violet.'))
            record('append_prepare',lambda:reader.import_history([extra])['index_preparation'])
            expanded=record('questions_after_append',lambda:ask(reader,qs))
            record('duplicate_prepare',lambda:reader.import_history([extra])['index_preparation'])
            fresh=make(temp/cid/'full',reader.store.load('sources'))
            record('full_expanded_prepare',fresh.prepare_index)
            full=record('full_expanded_questions',lambda:ask(fresh,qs))
            # Expected outputs are accessed only after retrieval has completed.
            expected={(r['case_id'],r['label']):r for r in prior['rows']}
            for i,q in enumerate(qs):
                old=expected[(cid,q['label'])]
                report['rows'].append(dict(case_id=cid,label=q['label'],question=q['question'],
                    previous_equal=initial[i]==old['prepared'],restart_equal=initial[i]==restarted[i],
                    append_prior_equal=initial[i]==expanded[i],incremental_full_equal=expanded[i]==full[i],
                    previous_expanded_equal=expanded[i]==old['incremental'],
                    prepared=initial[i],restarted=restarted[i],incremental=expanded[i],full=full[i]))
            save();print(json.dumps(dict(case=cid,complete=True)),flush=True)
    keys=['previous_equal','restart_equal','append_prior_equal','incremental_full_equal','previous_expanded_equal']
    report['checks']={k:sum(r[k] for r in report['rows']) for k in keys}
    report['checks'].update(total=len(report['rows']),ablation_witnesses_equal=all(r['witnesses_equal'] for r in report['ablations']),
        query_document_embeddings=sum(p['document_embeddings'] for p in report['phases'] if 'questions' in p['phase']),
        append_prepared=[p['preparation']['prepared_documents'] for p in report['phases'] if p['phase']=='append_prepare'],
        duplicate_embeddings=sum(p['document_embeddings'] for p in report['phases'] if p['phase']=='duplicate_prepare'))
    c=report['checks'];report['completed']=True
    report['passed']=c['total']==20 and all(c[k]==20 for k in keys) and c['ablation_witnesses_equal'] and c['query_document_embeddings']==0 and c['duplicate_embeddings']==0 and c['append_prepared']==[1]*7
    save();print(json.dumps(report['checks']),flush=True)
    assert report['passed'],'Preservation failed: do not adopt based on speed alone'


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--packet',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();run(args.packet,args.output)
