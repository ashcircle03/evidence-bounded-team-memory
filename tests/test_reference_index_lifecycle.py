"""Actual upstream index persistence and port lifecycle; decoder is a stub."""
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
import json
import pytest
from tests import test_reference_qa as reference
from evaluation.service_storage.audit import CountingEmbedding
from team_memory.readers.retrieval import ReferenceQA
from team_memory.readers.indexing import IndexNotReady


@pytest.fixture
def env():
    t=reference.ReferenceQAIntegration();t.setUp()
    t.embed=CountingEmbedding(embed_dim=8);t.options['embed_model']=t.embed
    t.output='The value is amber. [1]'
    yield t
    t.doCleanups()


def documents(t):
    return [t.source('The value is amber.','test:value'),t.source('The owner is Hana.','test:owner')]


@pytest.mark.parametrize('profile',['standard','team'])
def test_import_first_question_restart_append_and_duplicate(env,profile):
    t=env;root=Path(t.temp.name)/profile
    def reader():return ReferenceQA(root,profile=profile,**t.options)
    r=reader();prepared=r.import_history(documents(t))
    assert prepared['index_preparation']['prepared_documents']==2
    assert len(t.embed._texts)==2 and not t.calls
    before=r.ask('What is the value?');count=len(t.embed._texts)
    assert count==2 and len(t.embed._queries)==1
    again=reader().ask('What is the value?')
    assert again['raw']==before['raw'] and again['answers']==before['answers']
    assert len(t.embed._texts)==count
    r=reader();p=r.import_history([t.source('The date is Friday.','test:date')])
    assert p['index_preparation']['prepared_documents']==1 and p['index_preparation']['reused_documents']==2
    assert len(t.embed._texts)==3 and t.embed._texts[-1]=='The date is Friday.'
    r.ask('What is the value?');assert len(t.embed._texts)==3
    p=r.import_history(documents(t));assert p['index_preparation']['prepared_documents']==0
    assert len(t.embed._texts)==3
    # Compare the complete expanded-corpus retrieval to a clean full build;
    # source ordering is preserved even for tied mock embeddings.
    full=ReferenceQA(Path(t.temp.name)/('full-'+profile),profile=profile,**t.options)
    full.import_history(documents(t)+[t.source('The date is Friday.','test:date')])
    assert r.ask('What is the value?')['citation_sources']==full.ask('What is the value?')['citation_sources']


def test_unprepared_queries_do_not_embed_parse_or_repair(env):
    t=env;r=ReferenceQA(Path(t.temp.name)/'cold',**t.options)
    r.import_history(documents(t),prepare=False)
    with patch('team_memory.readers.indexing.document_nodes',side_effect=AssertionError('query transformed docs')):
        with pytest.raises(IndexNotReady):r.ask('What value?')
    assert not t.embed._texts and not t.embed._queries and not t.calls
    r.prepare_index();assert len(t.embed._texts)==2


def test_failed_publish_keeps_originals_old_generation_and_cached_embeddings(env):
    t=env;root=Path(t.temp.name)/'failure';r=ReferenceQA(root,profile='team',**t.options)
    r.import_history(documents(t));old_key=r.index_key;original=deepcopy(r.store.load('sources'))
    with patch('team_memory.readers.indexing.BM25Retriever.persist',side_effect=OSError('disk full')):
        with pytest.raises(OSError):r.import_history([t.source('The date is Friday.','test:date')])
    assert len(t.embed._texts)==3 and len(r.store.load('sources'))==3
    assert (r.index_dir/old_key/'complete.json').exists()
    assert not list(r.index_dir.glob('.pending-*'))
    with pytest.raises(IndexNotReady):r.ask('What value?')
    again=ReferenceQA(root,profile='team',**t.options)
    ready=again.prepare_index()
    assert ready['prepared_documents']==0 and ready['reused_documents']==3
    assert len(t.embed._texts)==3
    assert all(again.store.load('sources')[k]==v for k,v in original.items())
    assert again.ask('What value?')['status']=='ok'


def test_changed_config_requires_explicit_preparation(env):
    t=env;root=Path(t.temp.name)/'version';r=ReferenceQA(root,**t.options)
    r.import_history(documents(t));r2=ReferenceQA(root,chunk_size=256,**t.options)
    with pytest.raises(IndexNotReady):r2.ask('What value?')
    assert len(t.embed._texts)==2
    r2.prepare_index();assert len(t.embed._texts)==4


def test_service_ask_never_syncs_and_review_never_reembeds(env):
    from team_memory.service import TeamMemoryService
    from team_memory.readers.attribution import CitedSourceQA
    t=env;root=Path(t.temp.name)/'service';compares=[]
    def compare(_,content):
        compares.append(content);d=json.loads(content)
        return json.dumps(dict(relations=[dict(kind='reconsider',target=d['earlier'][0]['id'],old_sentence_ids=[0],new_sentence_ids=[0],reason='Changed writer limit')]))
    def service():return TeamMemoryService(root,reader=CitedSourceQA(root,**t.options),generate=compare)
    s=service();s.import_history([t.source('Version4 permits one writer. The value is amber.')])
    before=s.ask('What value?');assert len(t.embed._texts)==1 and not compares
    p=s.ingest(t.source('Version5 permits four writers.','test:new'))['proposals'][0]
    assert len(t.embed._texts)==2 and len(compares)==1
    s.review(p['id'],'author','approve');count=len(t.embed._texts)
    s=service()
    with patch.object(s,'sync',side_effect=AssertionError('query called sync')):
        assert s.ask('What value?')['raw']==before['raw']
    assert len(t.embed._texts)==count and len(compares)==1


def test_gateway_prepares_at_ingest_and_readonly_caller_cannot_prepare(env):
    from team_memory.adapters.runtime import connect_v2
    from team_memory.adapters.base import request
    from team_memory.adapters.legacy import public_source
    from team_memory.contracts.ports import CallContext
    t=env;root=Path(t.temp.name)/'gateway'
    from team_memory.readers.attribution import CitedSourceQA
    factory=lambda store:CitedSourceQA(store,**t.options)
    g=connect_v2(root,workspace_id='demo',reader_factory=factory,generate=lambda *_:'{"relations":[]}')
    ctx=CallContext('demo','author',frozenset(['records:read','records:write','relations:compare','evidence:read','answer:generate']))
    def call(port,op,payload,context=ctx):return port.handle(request(op,payload,workspace_id='demo',request_id=op),context=context)
    source=public_source(t.source('The value is amber.'))
    appended=call(g.records,'record.append',dict(source=source,expected_revision=0,idempotency_key='initial'))
    snapshot=appended['data']['snapshot'];query=dict(text='What value?',time_scope='current',as_of=None,conditions=[])
    missing=call(g,'gateway.ask',dict(query=query,snapshot_id=None))
    assert missing['errors'][0]['code']=='INDEX_STALE' and not t.embed._texts
    ro=CallContext('demo','author',frozenset(['evidence:read']))
    denied=call(g.retrieval,'evidence.prepare',dict(snapshot=snapshot),ro)
    assert denied['errors'][0]['code']=='FORBIDDEN' and not t.embed._texts
    ready=call(g.retrieval,'evidence.prepare',dict(snapshot=snapshot));assert ready['status']=='ok'
    assert len(t.embed._texts)==1
    new=public_source(t.source('The date is Friday.','test:new'))
    ingested=call(g,'gateway.ingest',dict(source=new,expected_revision=1,idempotency_key='new'))
    assert ingested['status']=='ok' and len(t.embed._texts)==2
    got=call(g,'gateway.ask',dict(query=query,snapshot_id=None));assert got['status'] in ('ok','partial'),got
    assert got['data']['bundle']['coverage']=='hits'
    assert len(t.embed._texts)==2


def test_pulled_record_requires_explicit_sync_before_query(env):
    from team_memory.service import TeamMemoryService
    from team_memory.readers.attribution import CitedSourceQA
    t=env;root=Path(t.temp.name)/'pulled';compares=[]
    def compare(_,content):
        compares.append(content);return '{"relations":[]}'
    s=TeamMemoryService(root,reader=CitedSourceQA(root,**t.options),generate=compare)
    s.import_history(documents(t));before=s.ask('What value?')
    # Simulate an external source arriving in the same checkout after Git pull.
    s.store.put('sources',s.store.source_envelope(t.source('The date is Friday.','test:pulled')))
    missing=s.handle(dict(operation='ask',question='What value?'))
    assert missing['error_code']=='INDEX_STALE' and len(t.embed._texts)==2 and not compares
    synced=s.sync()
    assert synced['index_preparation']['prepared_documents']==1 and len(compares)==1
    after=s.ask('What value?')
    assert after['raw']==before['raw'] and len(t.embed._texts)==3 and len(compares)==1


def test_failed_initial_import_sync_does_not_compare_history(env):
    from team_memory.service import TeamMemoryService
    from team_memory.readers.attribution import CitedSourceQA
    t=env;root=Path(t.temp.name)/'initial-failure';compares=[]
    def compare(_,content):
        compares.append(content);return '{"relations":[]}'
    def service():return TeamMemoryService(root,reader=CitedSourceQA(root,**t.options),generate=compare)
    s=service()
    with patch('team_memory.readers.indexing.VectorStoreIndex',side_effect=OSError('disk full')):
        failed=s.handle(dict(operation='import_history',records=documents(t)))
    assert failed['status']=='error' and len(s.store.load('sources'))==2
    s=service();fixed=s.sync()
    assert fixed['processed']==0 and not compares
    assert fixed['index_preparation']['prepared_documents']==0 and len(t.embed._texts)==2
    assert s.ask('What value?')['raw']=='The value is amber. [1]'
