"""Frozen old/full versus prepared retrieval with real local embeddings.

No answer key or LLM completion is used. Answer preservation is a separate
exact-request response replay, and must not be called fresh model inference.
"""
import argparse
from hashlib import sha256
import importlib.util
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
    from team_memory.storage.sources import SourceStore

    cfg=json.loads((packet/'config.json').read_text())
    root=Path(__file__).resolve().parents[2]
    filehash=lambda p:sha256(p.read_bytes()).hexdigest()
    for name,expected in cfg['code_sha256'].items():assert filehash(root/name)==expected,name
    for name,expected in cfg['data_sha256'].items():assert filehash(packet/name)==expected,name
    assert torch.cuda.is_available(),'Real embedding GPU required; no CPU fallback'
    class CountedEmbedding(HuggingFaceEmbedding):
        _texts: int = PrivateAttr(default=0)
        _queries: int = PrivateAttr(default=0)
        def _get_text_embeddings(self,texts):
            self._texts+=len(texts);return super()._get_text_embeddings(texts)
        def _get_query_embedding(self,query):
            self._queries+=1;return super()._get_query_embedding(query)
    embed=CountedEmbedding(model_name=cfg['embedding'],device='cuda',embed_batch_size=32)
    tokenizer=AutoTokenizer.from_pretrained(cfg['model_path'],local_files_only=True)
    llm=OpenAILike(model='Qwen3-8B',api_base='http://127.0.0.1:1/v1',api_key='unused-local',
        is_chat_model=True,tokenizer=tokenizer,context_window=32768,max_tokens=1024,max_retries=0)
    opts=dict(llm=llm,embed_model=embed,tokenizer=tokenizer,context_window=32768,num_output=1024,profile='team')
    spec=importlib.util.spec_from_file_location('team_memory.readers._frozen_retrieval',root/'evaluation/service_storage/legacy_retrieval.py')
    legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
    inputs=json.loads((packet/'inputs.json').read_text())
    report=dict(job_id=os.environ.get('SLURM_JOB_ID'),node=os.uname().nodename,mode='real CUDA embeddings; retrieval only',
        input_sha256=filehash(packet/'inputs.json'),config_sha256=filehash(packet/'config.json'),
        gpu=torch.cuda.get_device_name(),fresh_llm_calls=0,rows=[],phases=[])
    checkpoint=Path(cfg['embedding'])
    report['embedding_files_sha256']={name:filehash(checkpoint/name) for name in
        ['config.json','config_sentence_transformers.json','modules.json','sentence_bert_config.json',
         'model.safetensors','tokenizer.json','tokenizer_config.json','1_Pooling/config.json']}
    def phase(cid,name,fn):
        before=(embed._texts,embed._queries);start=time.monotonic();result=fn()
        report['phases'].append(dict(case_id=cid,phase=name,document_embeddings=embed._texts-before[0],
            query_embeddings=embed._queries-before[1],seconds=time.monotonic()-start,
            preparation=result if isinstance(result,dict) and 'prepared_documents' in result else None))
        return result
    def ask(reader,questions):
        return [reader.ask(q['question'],retrieve_only=True)['witnesses'] for q in questions]
    def populated(path,sources):
        store=SourceStore(path)
        for sid,env in sources.items():assert store.put('sources',env)==sid
        return store
    with tempfile.TemporaryDirectory(prefix='index-verification-',dir=cfg['scratch']) as temporary:
        for case in inputs['cases']:
            cid=case['id'];base=Path(temporary)/cid;questions=case['questions']
            old=legacy.ReferenceQA(populated(base/'old',case['sources']),**opts)
            old_answers=phase(cid,'old_first_questions',lambda:ask(old,questions))
            reader=ReferenceQA(populated(base/'prepared',case['sources']),**opts)
            phase(cid,'initial_prepare',reader.prepare_index)
            initial=phase(cid,'first_questions',lambda:ask(reader,questions))
            reader=ReferenceQA(reader.store,**opts)
            restarted=phase(cid,'restart_questions',lambda:ask(reader,questions))
            extra=dict(owner='storage-fixture',observed_at='2026-01-01T00:00:00Z',source=dict(
                speaker='storage-fixture',location='synthetic://storage-unrelated/'+cid,
                text='The spare telemetry marker in the storage lifecycle fixture is violet.'))
            phase(cid,'append_prepare',lambda:reader.import_history([extra])['index_preparation'])
            expanded=phase(cid,'questions_after_append',lambda:ask(reader,questions))
            phase(cid,'duplicate_prepare',lambda:reader.import_history([extra])['index_preparation'])
            fresh=ReferenceQA(populated(base/'fresh',reader.store.load('sources')),**opts)
            phase(cid,'full_expanded_prepare',fresh.prepare_index)
            clean=phase(cid,'full_expanded_questions',lambda:ask(fresh,questions))
            for i,q in enumerate(questions):
                report['rows'].append(dict(case_id=cid,label=q['label'],question=q['question'],
                    old_equal=old_answers[i]==initial[i],restart_equal=initial[i]==restarted[i],
                    incremental_full_equal=expanded[i]==clean[i],append_prior_equal=initial[i]==expanded[i],
                    old=old_answers[i],prepared=initial[i],restarted=restarted[i],incremental=expanded[i],full=clean[i]))
            print(json.dumps(dict(case=cid,complete=True)),flush=True)
    report['checks']=dict(total=len(report['rows']),
        old_equal=sum(r['old_equal'] for r in report['rows']),
        restart_equal=sum(r['restart_equal'] for r in report['rows']),
        incremental_full_equal=sum(r['incremental_full_equal'] for r in report['rows']),
        append_prior_equal=sum(r['append_prior_equal'] for r in report['rows']),
        query_document_embeddings=sum(p['document_embeddings'] for p in report['phases'] if p['phase'] in
            ['first_questions','restart_questions','questions_after_append','full_expanded_questions']),
        append_prepared=[p['preparation']['prepared_documents'] for p in report['phases'] if p['phase']=='append_prepare'],
        duplicate_embeddings=sum(p['document_embeddings'] for p in report['phases'] if p['phase']=='duplicate_prepare'))
    c=report['checks'];report['completed']=True
    report['passed']=c['total']==20 and c['restart_equal']==20 and c['incremental_full_equal']==20 and c['query_document_embeddings']==0 and c['duplicate_embeddings']==0 and all(n==1 for n in c['append_prepared'])
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report['checks']),flush=True)
    assert report['passed'],'Lifecycle validation failed; inspect saved output'


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--packet',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();run(args.packet,args.output)
