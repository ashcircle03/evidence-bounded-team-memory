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
RECORD_INDEX_UNIT='records-claims-v1'  # opt-in index unit; see record_index_spans


class IndexNotReady(RuntimeError):
    """An explicit ingest/sync/prepare must publish this source/config generation."""


def specification(reader,sources):
    records=reader.index_config.get('index_unit')==RECORD_INDEX_UNIT
    def entry(e):
        item=dict(source=e['source'],observed_at=e['observed_at'])
        # Record spans depend on the record_graph, so a changed graph needs a new index.
        if records and 'record_graph' in e:item['record_graph']=e['record_graph']
        return digest(item)
    return dict(version=VERSION,config=reader.index_config,sources={sid:entry(e) for sid,e in sorted(sources.items())})


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


def persist_cache(path,cache):
    """Atomically publish the upstream multi-key cache once per preparation."""
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.pending-',dir=path.parent);os.close(fd)
    try:
        cache.persist(tmp)
        with open(tmp,'rb') as stream:os.fsync(stream.fileno())
        os.replace(tmp,path);sync_dir(path.parent)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


def record_index_spans(graph,text,count_tokens,max_tokens):
    """Index spans from one source's record_graph, as (start, end) in the original text.

    One span per claim group, from its first to its last claim, condition,
    basis, time or subject sentence; then every sentence no claim uses. A claim
    group longer than max_tokens is indexed as its separate sentences instead.
    Spans are original text, never joined. Duplicates are dropped; the result is
    in text order.
    """
    from team_memory.records.graph import ROLES
    units={u['id']:u for u in graph['units']};used=set();spans=[]
    for claim in graph['claims']:
        ids=[uid for role in ROLES for uid in claim.get(role,[]) if uid in units]
        if not ids:continue
        used.update(ids)
        start=min(units[i]['start'] for i in ids);end=max(units[i]['end'] for i in ids)
        if count_tokens(text[start:end])<=max_tokens:spans.append((start,end))
        else:spans.extend((units[i]['start'],units[i]['end']) for i in ids)
    spans.extend((u['start'],u['end']) for u in graph['units'] if u['id'] not in used)
    return sorted(set(spans))


def record_nodes(reader,sid,envelope,graph):
    """Nodes for record_index_spans with the same metadata as the chunk nodes below."""
    from llama_index.core.schema import NodeRelationship,RelatedNodeInfo,TextNode
    text=envelope['source']['text']
    def count(value):return len(reader.tokenizer.encode(value,add_special_tokens=False))
    nodes=[]
    for i,(start,end) in enumerate(record_index_spans(graph,text,count,reader.index_config['chunk_size'])):
        node=TextNode(id_='node:'+digest([sid,RECORD_INDEX_UNIT,i]),text=text[start:end],
            start_char_idx=start,end_char_idx=end,metadata=dict(source_id=sid,parent_start=start,parent_end=end),
            relationships={NodeRelationship.SOURCE:RelatedNodeInfo(node_id=sid)})
        node.excluded_embed_metadata_keys=list(node.metadata)
        node.excluded_llm_metadata_keys=list(node.metadata)
        if reader.profile=='team':
            node.metadata.update(record_author=envelope['source']['speaker'],recorded_at=envelope['observed_at'])
            node.excluded_embed_metadata_keys=list(node.metadata)
        nodes.append(node)
    return nodes


def document_nodes(reader,sid,envelope):
    graph=envelope.get('record_graph')
    if reader.index_config.get('index_unit')==RECORD_INDEX_UNIT and graph and graph.get('units'):
        return record_nodes(reader,sid,envelope,graph)
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
    return nodes


def embed_documents(reader,parts):
    """Batch only changed documents using the existing embedding transformation."""
    nodes=[node for part in parts for node in part]
    if not nodes:return parts
    embedded=list(IngestionPipeline(transformations=[reader.embed_model],disable_cache=True).run(nodes=nodes))
    if [n.node_id for n in embedded]!=[n.node_id for n in nodes] or any(n.embedding is None for n in embedded):
        raise ValueError('Incomplete or reordered document embeddings')
    result=[];offset=0
    for part in parts:
        result.append(embedded[offset:offset+len(part)]);offset+=len(part)
    return result


def prepare(reader,sources):
    path,spec=directory(reader,sources);root=Path(reader.index_dir)
    result=dict(index_key=path.name,source_count=len(sources),prepared_documents=0,reused_documents=0)
    with writer_lock(root):
        if (path/'complete.json').is_file():
            load(reader,sources);return dict(result,reused_documents=len(sources))
        # IngestionCache already supports many document keys. Keep its format;
        # one atomic snapshot replaces one durable file transaction per document.
        cache_path=root/'document-cache.json'
        cache=IngestionCache.from_persist_path(str(cache_path)) if cache_path.is_file() else IngestionCache()
        legacy_dir=root/'documents';has_legacy=legacy_dir.is_dir()
        parts=[];missing=[];dirty=False
        for sid,envelope in sorted(sources.items()):
            key=digest(dict(version=VERSION,config=reader.index_config,source_id=sid,source=spec['sources'][sid]))
            part=cache.get(key)
            if part is None:
                # Read-only migration: reuse existing v1 vectors, never delete
                # old files or force a re-embedding just to change cache layout.
                cached=legacy_dir/(key+'.json')
                if has_legacy and cached.is_file():
                    part=IngestionCache.from_persist_path(str(cached)).get(key)
                    if part is not None:cache.put(key,part);dirty=True
            if part is None:
                part=document_nodes(reader,sid,envelope)
                missing.append(len(parts));result['prepared_documents']+=1
            else:result['reused_documents']+=1
            parts.append((key,part))
        for position,part in zip(missing,embed_documents(reader,[parts[i][1] for i in missing])):
            key=parts[position][0];parts[position]=(key,part)
            cache.put(key,part);dirty=True
        # Commit only a complete changed-document set. A later index publish
        # failure reuses it; an interrupted embedding/cache transaction retries
        # that uncommitted set, while all previously committed keys remain intact.
        if dirty:persist_cache(cache_path,cache)
        nodes=[node for _,part in parts for node in part]
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
