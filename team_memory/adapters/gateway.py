"""Explicit write orchestration and read-only QA over the five ports."""
from copy import deepcopy
from contextlib import contextmanager
import fcntl
from pathlib import Path
from team_memory.storage.objects import Store,digest
from .base import Adapter,Failure,request,issue


class GatewayAdapter(Adapter):
    module='gateway'
    capabilities={'gateway.ask':'records:read','gateway.ingest':'records:write','gateway.review':'review:vote'}

    def __init__(self,workspace_id,records,relations,retrieval,answering,*,journal_root,max_evidence=256):
        super().__init__(workspace_id)
        self.records,self.relations,self.retrieval,self.answering=records,relations,retrieval,answering
        self.journal=Store(journal_root);self.journal.root.mkdir(parents=True,exist_ok=True)
        self.max_evidence=max_evidence

    def call(self,port,operation,payload,context):
        result=port.handle(request(operation,payload,workspace_id=self.workspace_id,
                                   request_id=digest([operation,payload])),context=context)
        if result['status'] in ('invalid','error'):
            e=result['errors'][0];raise Failure(e['code'],e['message'],retryable=e['retryable'],item_id=e['item_id'])
        return result['data'],result['errors']

    @contextmanager
    def ingest_lock(self):
        with (self.journal.root/'ingest.lock').open('a') as stream:
            fcntl.flock(stream,fcntl.LOCK_EX)
            try:yield
            finally:fcntl.flock(stream,fcntl.LOCK_UN)

    def execute(self,operation,payload,context):
        if operation=='gateway.review':return self.call(self.records,'review.apply',payload,context)
        if operation=='gateway.ask':
            snapshot,_=self.call(self.records,'snapshot.get',dict(snapshot_id=payload['snapshot_id']),context)
            bundle,errors=self.call(self.retrieval,'evidence.retrieve',
                dict(snapshot=snapshot,query=payload['query'],max_evidence=self.max_evidence),context)
            if bundle['coverage']=='incomplete':
                answer=dict(snapshot_id=snapshot['id'],outcome='abstained',claims=[],reason='Evidence budget omitted required context; no answer generated.')
                return dict(bundle=bundle,answer=answer),errors
            answer,answer_errors=self.call(self.answering,'answer.generate',dict(bundle=bundle),context)
            return dict(bundle=bundle,answer=answer),errors+answer_errors
        with self.ingest_lock():return self.ingest(payload,context)

    def ingest(self,payload,context):
        identity=[self.workspace_id,context.principal_id,payload['idempotency_key']]
        saved=[p for p in self.journal.load('ingest_progress').values() if p['identity']==identity]
        if saved and any(p['payload']!=payload for p in saved):raise Failure('IDEMPOTENCY_CONFLICT','Ingest key already used')
        progress=deepcopy(max(saved,key=lambda p:p['sequence'])) if saved else dict(
            identity=identity,payload=payload,sequence=0,plan=None,steps=[],done=[])
        def save():
            progress['sequence']+=1
            self.journal.put('ingest_progress',progress)
        append=dict(source=payload['source'],idempotency_key=payload['idempotency_key']+':source',
                    expected_revision=payload['expected_revision'])
        receipt,_=self.call(self.records,'record.append',append,context)
        out=dict(receipt=receipt,proposal_ids=deepcopy(progress['done']))
        if progress['plan'] is None:
            snapshot=receipt['snapshot'];sid=payload['source']['id']
            try:
                plan,errors=self.call(self.relations,'relations.compare',dict(snapshot=snapshot,
                    incoming_source_id=sid,history_source_ids=[s['id'] for s in snapshot['sources'] if s['id']!=sid]),context)
            except Failure as exc:return out,[exc.issue]
            progress['plan']=plan;progress['errors']=errors;save()
        errors=deepcopy(progress.get('errors',[]))
        for index,c in enumerate(progress['plan']['candidates']):
            if index<len(progress['done']):continue
            if index==len(progress['steps']):
                snapshot,_=self.call(self.records,'snapshot.get',dict(snapshot_id=None),context)
                progress['steps'].append(dict(candidate=c,idempotency_key=payload['idempotency_key']+':proposal:'+str(index),
                                              expected_revision=snapshot['revision']))
                save()  # Persist intent BEFORE sending a mutation.
            try:
                applied,_=self.call(self.records,'proposal.submit',progress['steps'][index],context)
            except Failure as exc:
                if exc.issue['code']=='STALE_SNAPSHOT':
                    # Definitely not committed; next explicit retry can refresh
                    # its revision. Unknown/IO outcomes retain the exact intent.
                    progress['steps'].pop();save()
                return out,errors+[exc.issue]
            progress['done'].append(applied['object_id']);save()
            out['proposal_ids']=deepcopy(progress['done'])
        return out,errors
