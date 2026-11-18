"""Question-independent preparation using LlamaIndex's persisted nodes/vectors.

Sources remain authoritative. Document caches and immutable index generations are
private, rebuildable projections. Only prepare() performs transformations/embedding.
"""
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import shutil
import tempfile

from llama_index.core import Document, StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.ingestion import IngestionCache, IngestionPipeline
from llama_index.retrievers.bm25 import BM25Retriever
from team_memory.storage.objects import digest

VERSION='prepared-index/v1'


class IndexNotReady(RuntimeError):
    """An explicit ingest/sync/prepare must publish this source/config generation."""


def specification(reader,sources):
    return dict(version=VERSION,config=reader.index_config,
        sources={sid:digest(dict(source=e['source'],observed_at=e['observed_at'])) for sid,e in sorted(sources.items())})


def directory(reader,sources):
    spec=specification(reader,sources)
    return Path(reader.index_dir)/digest(spec),spec


def load(reader,sources):
    path,spec=directory(reader,sources);key=path.name
    marker=path/'complete.json'
    if not marker.is_file():raise IndexNotReady('Index is not prepared for these sources/settings; run import, ingest or sync first')
    if json.loads(marker.read_text())!=spec:raise IndexNotReady('Index manifest mismatch; explicit preparation required')
    if reader.index_key==key and reader.index is not None:return reader.index
    try:
        index=load_index_from_storage(StorageContext.from_defaults(persist_dir=str(path)),embed_model=reader.embed_model)
        sparse=BM25Retriever.from_persist_dir(str(path/'bm25')) if reader.profile=='team' and sources else None
    except (OSError,ValueError,KeyError) as exc:
        raise IndexNotReady('Published index is unreadable; repair it explicitly') from exc
    if sparse is not None:sparse.similarity_top_k=min(reader.top_k,sparse.bm25.scores["num_docs"])
    reader.index,reader.index_key,reader.sparse=index,key,sparse
    return index


@contextmanager
def writer_lock(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    with (root/'prepare.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        try:yield
        finally:fcntl.flock(lock,fcntl.LOCK_UN)


def sync_dir(path):
    fd=os.open(path,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)


def persist_document(path,key,nodes):
    cache=IngestionCache();cache.put(key,nodes)
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.pending-',dir=path.parent);os.close(fd)
    try:
        cache.persist(tmp)
        with open(tmp,'rb') as stream:os.fsync(stream.fileno())
        os.replace(tmp,path);sync_dir(path.parent)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def document_nodes(reader,sid,envelope):
    doc=Document(id_=sid,text=envelope['source']['text'],metadata={'source_id':sid},
        excluded_embed_metadata_keys=['source_id'],excluded_llm_metadata_keys=['source_id'])
    nodes=reader.splitter.get_nodes_from_documents([doc])
    for node in nodes:
        node.metadata.update(source_id=node.ref_doc_id,parent_start=node.start_char_idx,parent_end=node.end_char_idx)
        node.excluded_embed_metadata_keys=list(node.metadata)
        node.excluded_llm_metadata_keys=list(node.metadata)
        if reader.profile=='team':
            node.metadata.update(record_author=envelope['source']['speaker'],recorded_at=envelope['observed_at'])
            node.excluded_embed_metadata_keys=list(node.metadata)
    # Upstream embedding transformation populates node.embedding. The outer
    # IngestionCache also preserves parsing/offsets, with one atomic file per doc.
    return list(IngestionPipeline(transformations=[reader.embed_model],disable_cache=True).run(nodes=nodes))


def prepare(reader,sources):
    path,spec=directory(reader,sources);root=Path(reader.index_dir)
    result=dict(index_key=path.name,source_count=len(sources),prepared_documents=0,reused_documents=0)
    with writer_lock(root):
        if (path/'complete.json').is_file():
            load(reader,sources);return dict(result,reused_documents=len(sources))
        nodes=[]
        for sid,envelope in sorted(sources.items()):
            key=digest(dict(version=VERSION,config=reader.index_config,source_id=sid,source=spec['sources'][sid]))
            cached=root/'documents'/(key+'.json')
            part=IngestionCache.from_persist_path(str(cached)).get(key) if cached.is_file() else None
            if part is None:
                part=document_nodes(reader,sid,envelope)
                if any(n.embedding is None for n in part):raise ValueError('Incomplete document embeddings')
                persist_document(cached,key,part);result['prepared_documents']+=1
            else:result['reused_documents']+=1
            nodes.extend(part)
        # Stable source/chunk IDs preserve tie ordering between incremental and
        # clean builds. Upstream skips already embedded nodes.
        # SimpleVectorStore serialization and BM25 corpus statistics still cost
        # O(corpus) on WRITE; neither reparses nor re-embeds unchanged documents.
        staging=Path(tempfile.mkdtemp(prefix='.pending-',dir=root))
        try:
            index=VectorStoreIndex(nodes,embed_model=reader.embed_model)
            index.storage_context.persist(persist_dir=str(staging))
            if reader.profile=='team' and sources:
                BM25Retriever.from_defaults(docstore=index.docstore,similarity_top_k=reader.top_k).persist(str(staging/'bm25'))
            (staging/'complete.json').write_text(json.dumps(spec,ensure_ascii=False,sort_keys=True))
            for base,dirs,files in os.walk(staging,topdown=False):
                for name in files:
                    with open(Path(base)/name,'rb') as stream:os.fsync(stream.fileno())
                sync_dir(base)
            os.rename(staging,path);sync_dir(root)
        finally:
            if staging.exists():shutil.rmtree(staging)
        load(reader,sources)
    return result
