"""Prepared-index lifecycle counters; mock vectors, not retrieval quality."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from pydantic import PrivateAttr
from llama_index.core.embeddings import MockEmbedding
from llama_index.llms.openai_like import OpenAILike
from transformers import AutoTokenizer
from team_memory.readers.retrieval import ReferenceQA

class CountingEmbedding(MockEmbedding):
    _texts: list = PrivateAttr(default_factory=list)
    _queries: list = PrivateAttr(default_factory=list)
    def _get_text_embedding(self,text):
        self._texts.append(text);return super()._get_text_embedding(text)
    def _get_query_embedding(self,query):
        self._queries.append(query);return super()._get_query_embedding(query)


def main(output):
    tokenizer=AutoTokenizer.from_pretrained('.cache/qwen-tokenizer',local_files_only=True)
    embed=CountingEmbedding(embed_dim=8)
    llm=OpenAILike(model='Qwen3-8B',api_base='http://127.0.0.1:1/v1',api_key='unused-local',
        is_chat_model=True,tokenizer=tokenizer,context_window=4096,max_tokens=256,max_retries=0)
    options=dict(llm=llm,embed_model=embed,tokenizer=tokenizer,context_window=4096,num_output=256)
    rows=[]
    with TemporaryDirectory(prefix='record-storage-audit-') as temp:
        reader=ReferenceQA(temp,**options)
        def source(text):return dict(owner='owner',observed_at='2026-01-01T00:00:00Z',source=dict(text=text,speaker='author',location='test:'+text))
        def step(name,fn):
            before=(len(embed._texts),len(embed._queries));fn()
            rows.append(dict(step=name,document_embeddings=len(embed._texts)-before[0],query_embeddings=len(embed._queries)-before[1],
                stored_sources=len(reader.store.load('sources')),completed_index_generations=len(list(reader.index_dir.glob('*/complete.json')))))
        step('import_two_sources',lambda:reader.import_history([source('The value is amber.'),source('The owner is Hana.')]))
        step('first_question',lambda:reader.ask('What value?',retrieve_only=True))
        step('second_question',lambda:reader.ask('Who owns it?',retrieve_only=True))
        reader=ReferenceQA(temp,**options)
        step('question_after_restart',lambda:reader.ask('What was reported?',retrieve_only=True))
        step('import_one_more_source',lambda:reader.import_history([source('The date is Friday.')]))
        step('question_after_source_change',lambda:reader.ask('Which date?',retrieve_only=True))
    assert [r['document_embeddings'] for r in rows]==[2,0,0,0,1,0]
    assert [r['query_embeddings'] for r in rows]==[0,1,1,1,0,1]
    report=dict(scope='Actual ReferenceQA with counting MockEmbedding; lifecycle only, no vector quality/latency claim',external_model_calls=0,rows=rows,
        confirmed=['Canonical sources exist before any question','Documents embedded during ingestion before any question','Same corpus/restart reuse persisted vectors','Only added document embedded during ingestion; all questions load ready indexes'],
        service_ask_static_audit='TeamMemoryService.ask and GatewayAdapter.ask do not call sync/prepare; tested in test_reference_index_lifecycle.py')
    output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main(Path('results/service-storage/v1/lifecycle.json'))
