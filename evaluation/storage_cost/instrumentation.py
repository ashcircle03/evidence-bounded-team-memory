"""Evaluation-only timers and the two independent indexing interventions."""
from collections import defaultdict
from contextlib import contextmanager,ExitStack
import os
import time
from unittest.mock import patch

from llama_index.core import StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionCache,IngestionPipeline
from llama_index.retrievers.bm25 import BM25Retriever
from team_memory.readers import indexing as current
from evaluation.storage_cost import indexing_v1 as previous


class Timings:
    def __init__(self):
        self.rows=defaultdict(lambda:dict(calls=0,seconds=0,exclusive_seconds=0));self.stack=[]

    @contextmanager
    def measure(self,label):
        frame=[time.perf_counter(),0.0];self.stack.append(frame)
        try:yield
        finally:
            elapsed=time.perf_counter()-frame[0];self.stack.pop()
            row=self.rows[label];row['calls']+=1;row['seconds']+=elapsed;row['exclusive_seconds']+=elapsed-frame[1]
            if self.stack:self.stack[-1][1]+=elapsed


@contextmanager
def instrument(module,meter):
    """Inclusive and exclusive times; nested categories must not be added twice."""
    targets=[(module,'document_nodes','document_transform'),
        (module,'VectorStoreIndex','vector_index_construct'),(module,'load','ready_index_load'),
        (IngestionCache,'get','cache_get'),(IngestionCache,'put','cache_put'),
        (IngestionCache,'persist','cache_serialize_write'),(IngestionCache,'from_persist_path','cache_load'),
        (IngestionPipeline,'run','embedding_pipeline'),(SentenceSplitter,'get_nodes_from_documents','split'),
        (StorageContext,'persist','vector_store_persist'),(BM25Retriever,'from_defaults','bm25_build'),
        (BM25Retriever,'persist','bm25_persist'),(os,'fsync','fsync'),
        (os,'replace','atomic_replace'),(os,'rename','atomic_rename')]
    targets.append((module,'persist_document' if module is previous else 'persist_cache','cache_transaction'))
    def wrapper(fn,label):
        def call(*args,**kwargs):
            with meter.measure(label):return fn(*args,**kwargs)
        return call
    with ExitStack() as stack:
        for obj,name,label in targets:stack.enter_context(patch.object(obj,name,wrapper(getattr(obj,name),label)))
        yield


@contextmanager
def intervention(arm,reader,sources):
    """Four cold-cache arms. No production flags or answer-dependent choices."""
    if arm=='previous':yield previous;return
    if arm=='combined':yield current;return
    if arm=='cache_only':
        batched=current.embed_documents
        def individually(r,parts):return [batched(r,[part])[0] for part in parts]
        with patch.object(current,'embed_documents',individually):yield current
        return
    if arm!='batch_only':raise ValueError(arm)
    prepared={}
    def batch_once(r,sid,envelope):
        if not prepared:
            ids=sorted(sources)
            parts=[current.document_nodes(r,key,sources[key]) for key in ids]
            prepared.update(zip(ids,current.embed_documents(r,parts)))
        return prepared[sid]
    with patch.object(previous,'document_nodes',batch_once):yield previous
