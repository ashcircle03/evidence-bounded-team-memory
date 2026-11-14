"""Atomic append-only commands using the existing immutable Store.put primitive.

Each command writes ONE content-addressed commit containing its native object
delta and idempotency receipt. No mutable HEAD or partially visible source files.
Legacy v2 files are imported once, never overwritten. Forked commit histories
fail closed; this adapter does not invent a Git merge policy.
"""
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime,timezone
import fcntl
from pathlib import Path

from team_memory.storage.objects import Store,digest
from team_memory.storage.sources import SourceStore
from team_memory.review import state
from team_memory.contracts.validation import check_candidate,check_snapshot
from .base import Adapter,Failure
from .legacy import MutableView,public_source,envelope,candidate,witness


class RecordsAdapter(Adapter):
    module='records'
    capabilities={'record.append':'records:write','proposal.submit':'records:write',
                  'review.apply':'review:vote','snapshot.get':'records:read'}

    def __init__(self,root,workspace_id,*,bootstrap=True):
        super().__init__(workspace_id)
        self.store=Store(root)
        self.store.root.mkdir(parents=True,exist_ok=True)
        with self.lock():
            if not self.store.load('module_commits'):
                original=SourceStore(root)
                objects={k:original.load(k) if bootstrap else {} for k in ('sources','timeline_proposals','timeline_votes')}
                genesis=dict(workspace_id=workspace_id,parent=None,revision=0,at=self.now(),
                    objects=objects,identity=None,payload=None,object_id=None)
                # Validate the legacy import before making it authoritative.
                self.snapshot_from([(digest(genesis),genesis)])
                self.store.put('module_commits',genesis)
            self.chain()

    @staticmethod
    def now():return datetime.now(timezone.utc).isoformat()

    @contextmanager
    def lock(self):
        with (self.store.root/'.module-writer.lock').open('a') as stream:
            fcntl.flock(stream,fcntl.LOCK_EX)
            try:yield
            finally:fcntl.flock(stream,fcntl.LOCK_UN)

    def chain(self,snapshot_id=None):
        commits=self.store.load('module_commits')
        if not commits:raise Failure('IO_FAILURE','Missing module history')
        if any(c['workspace_id']!=self.workspace_id for c in commits.values()):
            raise Failure('FORBIDDEN','Store belongs to another workspace')
        if snapshot_id is None:
            parents={c['parent'] for c in commits.values()}
            heads=set(commits)-parents
            if len(heads)!=1:raise Failure('STALE_SNAPSHOT','Divergent histories require explicit reconciliation')
            snapshot_id=heads.pop()
        if snapshot_id not in commits:raise Failure('NOT_FOUND','Snapshot is not in this store')
        output=[];seen=set();key=snapshot_id
        while key is not None:
            if key in seen or key not in commits:raise Failure('IO_FAILURE','Broken commit history')
            seen.add(key);c=commits[key];output.append((key,c));key=c['parent']
        output.reverse()
        if [c['revision'] for _,c in output]!=list(range(len(output))):
            raise Failure('IO_FAILURE','Invalid revision chain')
        baseline=output[0][1]['objects']
        legacy=SourceStore(self.store.root)
        if any(legacy.load(kind)!=baseline.get(kind,{}) for kind in ('sources','timeline_proposals','timeline_votes')):
            raise Failure('STALE_SNAPSHOT','Legacy v2 files changed after migration; do not mix writers')
        return output

    @staticmethod
    def objects_from(chain):
        objects={}
        for _,c in chain:
            for kind,rows in c['objects'].items():
                target=objects.setdefault(kind,{})
                for oid,row in rows.items():
                    if oid in target and target[oid]!=row:raise Failure('IO_FAILURE','Immutable ID collision')
                    target[oid]=deepcopy(row)
        return objects

    def snapshot_from(self,chain):
        sid,head=chain[-1];objects=self.objects_from(chain)
        view=MutableView(self.store.root,objects)
        rows=[]
        for p in state.proposals(view):
            effect=({'correction':'replace_assertion','reconsider':'authorize_reconsideration'}.get(p['kind'],'none')
                    if p['status']=='approved' else 'none')
            dates=[c['at'] for _,c in chain if any(v.get('proposal')==p['id'] for v in c['objects'].get('timeline_votes',{}).values()) and c['revision']>0]
            rows.append(dict(id=p['id'],candidate=candidate(p),reviewer=p['reviewer'],status=p['status'],
                             effect=effect,history_source_ids=p['history'],
                             decided_at=max(dates) if dates and p['status'] in ('approved','rejected') else None))
        for pid,p in objects.get('module_informational',{}).items():
            rows.append(dict(id=pid,candidate=candidate(p),reviewer=objects['sources'][p['previous']['source_id']]['owner'],
                             status='informational',effect='none',decided_at=None))
        snapshot=dict(id=sid,revision=head['revision'],as_of=head['at'],
            sources=[public_source(e,k) for k,e in sorted(objects['sources'].items())],proposals=sorted(rows,key=lambda p:p['id']))
        check_snapshot(snapshot)
        # Do not silently drop malformed imported proposals.
        if len(rows)!=len(objects.get('timeline_proposals',{}))+len(objects.get('module_informational',{})):
            raise Failure('INVALID_INPUT','Legacy proposal could not be migrated losslessly')
        return snapshot

    def snapshot(self,snapshot_id=None):return self.snapshot_from(self.chain(snapshot_id))

    def execute(self,operation,payload,context):
        with self.lock():
            if operation=='snapshot.get':return self.snapshot(payload['snapshot_id']),[]
            chain=self.chain();snapshot=self.snapshot_from(chain);objects=self.objects_from(chain)
            if operation=='record.append' and payload['source']['owner']!=context.principal_id and 'records:import' not in context.capabilities:
                raise Failure('FORBIDDEN','Only the source owner or trusted importer can append')
            if operation=='review.apply':
                p=next((p for p in snapshot['proposals'] if p['id']==payload['proposal_id']),None)
                if p is None:raise Failure('NOT_FOUND','Unknown proposal')
                if p['reviewer']!=context.principal_id:raise Failure('FORBIDDEN','Original owner must review')
            identity=[self.workspace_id,context.principal_id,operation,payload['idempotency_key']]
            for index,(key,commit) in enumerate(chain):
                if commit['identity']==identity:
                    if commit['payload']!=payload:raise Failure('IDEMPOTENCY_CONFLICT','Key is already bound to another payload')
                    return dict(snapshot=self.snapshot_from(chain[:index+1]),object_id=commit['object_id'],replayed=True),[]
            if payload['expected_revision']!=snapshot['revision']:raise Failure('STALE_SNAPSHOT','Reload before writing')
            staged=MutableView(self.store.root,objects)
            if operation=='record.append':
                sid=payload['source']['id'];env=envelope(payload['source'])
                if sid in objects['sources'] and objects['sources'][sid]!=env:
                    raise Failure('INVALID_INPUT','Source ID collision')
                staged.objects['sources'][sid]=env;oid=sid
            elif operation=='proposal.submit':
                c=payload['candidate'];check_candidate(c,snapshot)
                src={s['id']:s for s in snapshot['sources']}
                if 'comparison_snapshot_id' in c:
                    compared=self.snapshot(c['comparison_snapshot_id'])
                    check_candidate(c,compared)
                p=dict(kind=c['kind'],reason=c['reason'],previous=witness(c['previous'],src),
                       incoming=witness(c['incoming'],src))
                if 'comparison_snapshot_id' in c:
                    p.update(comparison_snapshot_id=c['comparison_snapshot_id'],history=c['history_source_ids'])
                if c['kind']=='coexist':oid=staged.put('module_informational',dict(p,requires_review=False))
                else:
                    p.update(reviewer=src[c['previous']['source_id']]['owner'],
                             history=c.get('history_source_ids',[c['previous']['source_id']]))
                    if c['kind']=='correction':p.update(previous_assertion=witness(c['previous_assertion'],src),incoming_assertion=witness(c['incoming_assertion'],src))
                    existing=next((row for row in snapshot['proposals'] if row['id']==digest(p)),None)
                    if existing and existing['status']!='pending':
                        raise Failure('INVALID_INPUT','Already decided proposal cannot be resubmitted as pending')
                    oid=staged.put('timeline_proposals',p)
            else:
                oid=payload['proposal_id']
                state.review(staged,oid,context.principal_id,payload['choice'])
            delta={k:{oid:obj for oid,obj in rows.items() if oid not in objects.get(k,{})}
                   for k,rows in staged.objects.items()}
            commit=dict(workspace_id=self.workspace_id,parent=snapshot['id'],revision=snapshot['revision']+1,
                        at=self.now(),objects=delta,identity=identity,payload=payload,object_id=oid)
            key=digest(commit)
            next_snapshot=self.snapshot_from(chain+[(key,commit)])
            # Single immutable file is the visibility/commit point, including the receipt.
            try:self.store.put('module_commits',commit)
            except OSError:
                if self.store.load('module_commits').get(key)!=commit:raise
            return dict(snapshot=next_snapshot,object_id=oid,replayed=False),[]
