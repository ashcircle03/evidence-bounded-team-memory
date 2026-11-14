from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
import tempfile
from unittest.mock import patch

import pytest
from team_memory.adapters.records import RecordsAdapter
from team_memory.adapters.base import request
from team_memory.adapters.legacy import public_source
from team_memory.contracts.ports import CallContext
from team_memory.storage.sources import SourceStore
from team_memory.storage.objects import Store

CAPS=frozenset(['records:read','records:write','records:import','review:vote'])


def call(port,op,payload,actor='hana',workspace='demo'):
    return port.handle(request(op,payload,workspace_id=workspace,request_id='test'),
                       context=CallContext(workspace,actor,CAPS))


def source(text,owner='hana',location='test:old'):
    return public_source(dict(owner=owner,observed_at='2026-11-14T00:00:00Z',
                             source=dict(speaker=owner,location=location,text=text)))


def append(port,s,key):
    return call(port,'record.append',dict(source=s,expected_revision=port.snapshot()['revision'],idempotency_key=key))


def proposal(port,kind='reconsider'):
    old=source('Keep one writer because v4 permits one writer. Archive is Orion.')
    new=source('v5 permits four writers.','jun','test:new')
    append(port,old,'old');append(port,new,'new')
    def w(s):return dict(source_id=s['id'],start=0,end=len(s['text']),quote=s['text'])
    c=dict(kind=kind,previous=w(old),incoming=w(new),reason='The blocking writer condition changed.',
           previous_assertion=None,incoming_assertion=None)
    result=call(port,'proposal.submit',dict(candidate=c,expected_revision=2,idempotency_key='proposal'))
    assert result['status']=='ok',result
    return result['data']['object_id']


def test_persistence_reconsider_approval_and_read_only_restart(tmp_path):
    port=RecordsAdapter(tmp_path,'demo');pid=proposal(port)
    before=port.snapshot()
    assert before['proposals'][0]['status']=='pending'
    denied=call(port,'review.apply',dict(proposal_id=pid,choice='approve',expected_revision=3,idempotency_key='vote'),actor='jun')
    assert denied['errors'][0]['code']=='FORBIDDEN';assert port.snapshot()==before
    approved=call(port,'review.apply',dict(proposal_id=pid,choice='approve',expected_revision=3,idempotency_key='vote'))
    assert approved['status']=='ok',approved
    fresh=RecordsAdapter(tmp_path,'demo').snapshot()
    assert fresh['sources']==before['sources']
    assert fresh['proposals'][0]['effect']=='authorize_reconsideration'
    assert fresh['proposals'][0]['decided_at'] is not None
    assert port.snapshot(before['id'])==before


def test_idempotency_conflict_and_concurrent_revision(tmp_path):
    port=RecordsAdapter(tmp_path,'demo');s=source('A')
    payload=dict(source=s,expected_revision=0,idempotency_key='same')
    first=call(port,'record.append',payload)
    retry=call(RecordsAdapter(tmp_path,'demo'),'record.append',payload)
    assert retry['data']==dict(first['data'],replayed=True)
    bad=call(port,'record.append',dict(payload,source=source('B')))
    assert bad['errors'][0]['code']=='IDEMPOTENCY_CONFLICT'
    def submit(i):return call(RecordsAdapter(tmp_path,'demo'),'record.append',
        dict(source=source(str(i)),expected_revision=1,idempotency_key=str(i)))
    with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(submit,[1,2]))
    assert sorted(r['status'] for r in results)==['invalid','ok']
    assert port.snapshot()['revision']==2


def test_failed_commit_does_not_mutate_state_and_retry_succeeds(tmp_path):
    port=RecordsAdapter(tmp_path,'demo');before=port.snapshot()
    payload=dict(source=source('A'),expected_revision=0,idempotency_key='a')
    with patch.object(port.store,'put',side_effect=OSError('injected disk error')):
        assert call(port,'record.append',payload)['errors'][0]['code']=='IO_FAILURE'
    assert port.snapshot()==before
    assert call(port,'record.append',payload)['status']=='ok'


def test_source_collision_and_workspace_capability_isolation(tmp_path):
    port=RecordsAdapter(tmp_path,'demo');s=source('A');append(port,s,'a')
    bad=deepcopy(s);bad['text']='B'
    assert append(port,bad,'b')['status']=='invalid'
    assert call(port,'snapshot.get',{'snapshot_id':None},workspace='other')['errors'][0]['code']=='FORBIDDEN'
    context=CallContext('demo','hana',frozenset(['records:read']))
    result=port.handle(request('record.append',dict(source=source('B'),expected_revision=1,idempotency_key='b'),
        workspace_id='demo',request_id='b'),context=context)
    assert result['errors'][0]['code']=='FORBIDDEN'


def test_bootstrap_keeps_native_ids_and_legacy_files_immutable(tmp_path):
    legacy=SourceStore(tmp_path)
    sid=legacy.capture_source(dict(owner='hana',observed_at='2026-11-01T00:00:00Z',
        source=dict(speaker='Hana',location='test',text='  exact text\n')))
    before={str(p):p.read_bytes() for p in (tmp_path/'sources').glob('*.json')}
    port=RecordsAdapter(tmp_path,'demo')
    assert port.snapshot()['sources'][0]['id']==sid
    assert port.snapshot()['sources'][0]['text']=='  exact text\n'
    append(port,source('New record'),'new')
    assert {str(p):p.read_bytes() for p in (tmp_path/'sources').glob('*.json')}==before


def test_divergent_git_histories_fail_closed(tmp_path):
    port=RecordsAdapter(tmp_path,'demo');base=port.snapshot()
    append(port,source('A'),'a')
    head=port.chain()[-1][1]
    fork=deepcopy(head);fork['at']='2026-11-15T00:00:00Z';fork['payload']['idempotency_key']='fork'
    port.store.put('module_commits',fork)
    with pytest.raises(Exception,match='Divergent histories'):port.snapshot()
    assert port.snapshot(base['id'])==base


def test_mixed_v2_writer_is_detected_instead_of_silently_ignored(tmp_path):
    port=RecordsAdapter(tmp_path,'demo')
    SourceStore(tmp_path).capture_source(dict(owner='a',observed_at='2026-11-14T00:00:00Z',
        source=dict(speaker='a',location='x',text='external legacy append')))
    with pytest.raises(Exception,match='Legacy v2 files changed'):port.snapshot()
