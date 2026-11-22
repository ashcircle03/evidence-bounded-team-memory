"""Atomic append-only commands using the existing immutable Store.put primitive.

Each command writes ONE content-addressed commit containing its native object
delta and idempotency receipt. No mutable HEAD or partially visible source files.
Legacy v2 files are imported once, never overwritten. Forked commit histories
(two checkouts that appended and then exchanged commits through Git) are never
merged automatically: default reads and writes stay on this checkout's own line
(a pointer outside the shared store), heads() lists every line, any snapshot ID
stays readable, and reconcile(base) explicitly replays the other lines onto base.
"""
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime,timezone
import fcntl
import os
from pathlib import Path

from team_memory.storage.objects import Store,digest
from team_memory.storage.sources import SourceStore
from team_memory.storage.verified import VerifiedObjects
from team_memory.review import state
from team_memory.contracts.validation import check_candidate,check_snapshot
from team_memory.records.compact import STORAGES,STORAGE_COMPACT,compact_record,hydrate_payload
from .base import Adapter,Failure
from .legacy import MutableView,public_source,envelope,candidate,witness


class RecordsAdapter(Adapter):
    module='records'
    capabilities={'record.append':'records:write','proposal.submit':'records:write',
                  'review.apply':'review:vote','snapshot.get':'records:read'}

    def __init__(self,root,workspace_id,*,bootstrap=True,cache=True,storage='full',record_builder=None):
        """storage='compact' (opt-in) writes new records without derivable quotes and
        edges; see records/compact.py. Reading accepts both forms in any mix.

        record_builder(source) -> source with record_graph, e.g.
        partial(preserving.construct, generate=..., model=...). When given, records runs
        extraction itself on record.append (spec 7: extraction belongs to Records).
        """
        if storage not in STORAGES:raise ValueError(f'Unknown records storage: {storage}')
        self.storage=storage
        self.record_builder=record_builder
        super().__init__(workspace_id)
        self.store=Store(root)
        self.store.root.mkdir(parents=True,exist_ok=True)
        self.reader=VerifiedObjects(self.store.root,cache=cache)
        self.cache_enabled=cache
        self._snapshot_cache=None
        # Per-checkout pointer, outside the shared (Git-tracked) store, like a Git HEAD.
        self.local_head_path=self.store.root.parent/('.module-local-'+self.store.root.name)/'head'
        with self.lock():
            if not self._load('module_commits'):
                original=SourceStore(root)
                objects={k:original.load(k) if bootstrap else {} for k in ('sources','timeline_proposals','timeline_votes')}
                genesis=dict(workspace_id=workspace_id,parent=None,revision=0,at=self.now(),
                    objects=objects,identity=None,payload=None,object_id=None)
                # Validate the legacy import before making it authoritative.
                self.snapshot_from([(digest(genesis),genesis)])
                self._persist(genesis)
                self._remember_head(digest(genesis))
            # Divergent heads must not make the port unusable; explicit snapshots stay readable.
            self._head_keys(self._commits())

    def _load(self,kind):
        try:return self.reader.load(kind)
        except (ValueError,TypeError,KeyError) as exc:
            raise Failure('IO_FAILURE','Stored immutable data is corrupt; restore or audit before retrying') from exc

    @staticmethod
    def _check_commits(commits):
        fields={'workspace_id','parent','revision','at','objects','identity','payload','object_id'}
        kinds={'sources','timeline_proposals','timeline_votes','module_informational'}
        try:
            for c in commits.values():
                if set(c)!=fields or type(c['revision']) is not int or c['revision']<0:
                    raise ValueError('Invalid commit envelope')
                if c['parent'] is not None and not isinstance(c['parent'],str):raise ValueError('Invalid parent')
                if not isinstance(c['workspace_id'],str):raise ValueError('Invalid workspace')
                dt=datetime.fromisoformat(c['at'].replace('Z','+00:00'))
                if dt.tzinfo is None:raise ValueError('Missing commit timezone')
                if not isinstance(c['objects'],dict) or set(c['objects'])-kinds:raise ValueError('Unknown object collection')
                if any(not isinstance(rows,dict) for rows in c['objects'].values()):raise ValueError('Invalid delta')
                if c['revision']==0:
                    if any(c[k] is not None for k in ('parent','identity','payload','object_id')):raise ValueError('Invalid genesis')
                elif (not isinstance(c['identity'],list) or len(c['identity'])!=4
                      or not isinstance(c['payload'],dict) or not isinstance(c['object_id'],str)):
                    raise ValueError('Missing command receipt')
        except (ValueError,TypeError,KeyError,AttributeError) as exc:
            raise Failure('IO_FAILURE','Invalid stored commit structure') from exc

    @staticmethod
    def _check_objects(objects):
        # The legacy reducer ignores malformed votes. At the storage boundary
        # that would hide corruption as a legitimate pending/approved state.
        try:
            src=objects.get('sources',{})
            for sid,env in src.items():envelope(public_source(env,sid))
            proposals=objects.get('timeline_proposals',{})
            for kind in ('timeline_proposals','timeline_votes','module_informational'):
                for oid,row in objects.get(kind,{}).items():
                    if not isinstance(row,dict) or digest(row)!=oid:raise ValueError('Invalid object identity')
            for vote in objects.get('timeline_votes',{}).values():
                if set(vote)!={'proposal','actor','choice'}:raise ValueError('Invalid vote fields')
                p=proposals[vote['proposal']]
                owner=src[p['previous']['source_id']]['owner']
                if vote['actor']!=owner or vote['choice'] not in ('approve','reject'):
                    raise ValueError('Invalid stored review')
        except (ValueError,TypeError,KeyError) as exc:
            raise Failure('IO_FAILURE','Invalid stored source, proposal or review') from exc

    def _persist(self,commit):
        try:self.store.put('module_commits',commit)
        except OSError:
            if self._load('module_commits').get(digest(commit))!=commit:raise
        # File fsync alone does not persist creation of its directory entry.
        # On sync failure keep the visible commit and require the same-key retry.
        self._sync_directories()

    def _sync_directories(self):
        try:
            for path in (self.store.root/'module_commits',self.store.root):
                fd=os.open(path,os.O_RDONLY)
                try:os.fsync(fd)
                finally:os.close(fd)
        except OSError as exc:
            raise Failure('IO_FAILURE','Commit may be visible; retry the identical idempotency key to confirm durability',retryable=True) from exc

    @staticmethod
    def now():return datetime.now(timezone.utc).isoformat()

    @contextmanager
    def lock(self):
        with (self.store.root/'.module-writer.lock').open('a') as stream:
            fcntl.flock(stream,fcntl.LOCK_EX)
            try:yield
            finally:fcntl.flock(stream,fcntl.LOCK_UN)

    def _commits(self):
        commits=self._load('module_commits')
        self._check_commits(commits)
        if not commits:raise Failure('IO_FAILURE','Missing module history')
        if any(c['workspace_id']!=self.workspace_id for c in commits.values()):
            raise Failure('FORBIDDEN','Store belongs to another workspace')
        return commits

    def _head_keys(self,commits):
        """Commits without a child, minus heads absorbed by an explicit reconcile()."""
        parents={c['parent'] for c in commits.values()}
        absorbed=set()
        for record in self._load('module_reconciliations').values():
            if (set(record)!={'workspace_id','base','absorbed','result','at'} or record['workspace_id']!=self.workspace_id
                    or not isinstance(record['absorbed'],list) or record['result'] not in commits
                    or record['base'] not in commits or any(a not in commits for a in record['absorbed'])):
                raise Failure('IO_FAILURE','Invalid reconciliation record')
            absorbed.update(record['absorbed'])
        heads=set(commits)-parents-absorbed
        if not heads:raise Failure('IO_FAILURE','No current history head')
        return heads

    def heads(self):
        """Current heads, newest revision first. More than one means divergent histories."""
        commits=self._commits()
        rows=[dict(snapshot_id=k,revision=commits[k]['revision'],at=commits[k]['at'],
                   local=k==self._local_head()) for k in self._head_keys(commits)]
        return sorted(rows,key=lambda r:(-r['revision'],r['snapshot_id']))

    def _local_head(self):
        try:return self.local_head_path.read_text(encoding='utf8').strip() or None
        except OSError:return None

    def _remember_head(self,key):
        # Best effort: the commit is already durable; a lost pointer only affects default reads.
        try:
            self.local_head_path.parent.mkdir(parents=True,exist_ok=True)
            temporary=self.local_head_path.with_suffix('.tmp')
            temporary.write_text(key+'\n',encoding='utf8')
            os.replace(temporary,self.local_head_path)
        except OSError:
            pass

    def chain(self,snapshot_id=None):
        commits=self._commits()
        if snapshot_id is None:
            heads=self._head_keys(commits)
            if len(heads)==1:
                snapshot_id=heads.pop()
            elif self._local_head() in heads:
                # Divergent after a Git pull: keep this checkout on its own line until reconcile().
                snapshot_id=self._local_head()
            else:
                raise Failure('STALE_SNAPSHOT','Divergent histories: read an explicit snapshot_id or reconcile. Heads: '
                              +', '.join(sorted(heads)))
        if snapshot_id not in commits:raise Failure('NOT_FOUND','Snapshot is not in this store')
        output=[];seen=set();key=snapshot_id
        while key is not None:
            if key in seen or key not in commits:raise Failure('IO_FAILURE','Broken commit history')
            seen.add(key);c=commits[key];output.append((key,c));key=c['parent']
        output.reverse()
        if [c['revision'] for _,c in output]!=list(range(len(output))):
            raise Failure('IO_FAILURE','Invalid revision chain')
        baseline=output[0][1]['objects']
        if any(self._load(kind)!=baseline.get(kind,{}) for kind in ('sources','timeline_proposals','timeline_votes')):
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
        cache_key=tuple(key for key,_ in chain)
        if self.cache_enabled and self._snapshot_cache and self._snapshot_cache[0]==cache_key:
            return deepcopy(self._snapshot_cache[1])
        sid,head=chain[-1];objects=self.objects_from(chain)
        self._check_objects(objects)
        vote_dates={}
        for _,commit in chain:
            if commit['revision']>0:
                for vote in commit['objects'].get('timeline_votes',{}).values():
                    vote_dates[vote['proposal']]=commit['at']
        view=MutableView(self.store.root,objects)
        rows=[]
        for p in state.proposals(view):
            effect=({'correction':'replace_assertion','reconsider':'authorize_reconsideration'}.get(p['kind'],'none')
                    if p['status']=='approved' else 'none')
            rows.append(dict(id=p['id'],candidate=candidate(p),reviewer=p['reviewer'],status=p['status'],
                             effect=effect,history_source_ids=p['history'],
                             decided_at=vote_dates.get(p['id']) if p['status'] in ('approved','rejected') else None))
        for pid,p in objects.get('module_informational',{}).items():
            rows.append(dict(id=pid,candidate=candidate(p),reviewer=objects['sources'][p['previous']['source_id']]['owner'],
                             status='informational',effect='none',decided_at=None))
        snapshot=dict(id=sid,revision=head['revision'],as_of=head['at'],
            sources=[public_source(e,k) for k,e in sorted(objects['sources'].items())],proposals=sorted(rows,key=lambda p:p['id']))
        check_snapshot(snapshot)
        # Do not silently drop malformed imported proposals.
        if len(rows)!=len(objects.get('timeline_proposals',{}))+len(objects.get('module_informational',{})):
            raise Failure('INVALID_INPUT','Legacy proposal could not be migrated losslessly')
        if self.cache_enabled:self._snapshot_cache=(cache_key,deepcopy(snapshot))
        return snapshot

    def snapshot(self,snapshot_id=None):return self.snapshot_from(self.chain(snapshot_id))

    def execute(self,operation,payload,context):
        prepared=None
        if operation=='record.append':
            # Model calls run outside the writer lock; the result is checked again under it.
            prepared=self._prepare_source(payload,context)
        with self.lock():
            if operation=='snapshot.get':return self.snapshot(payload['snapshot_id']),[]
            data,commit=self._apply(self.chain(),operation,payload,context.principal_id,context.capabilities,
                                    prepared_source=prepared)
            if commit is None:
                self._sync_directories()
            else:
                # Single immutable file is the visibility/commit point, including the receipt.
                self._persist(commit)
                self._remember_head(digest(commit))
            return data,[]

    def _prepare_source(self,payload,context):
        """Run record_builder for a source without record_graph. None when not needed.

        A retry of an already committed command is answered from its receipt, so the
        model is not called again. A builder failure keeps the source (F01): it is
        stored as raw units with status failed and the reason.
        """
        source=payload['source']
        if self.record_builder is None or 'record_graph' in source:return None
        if source['owner']!=context.principal_id and 'records:import' not in context.capabilities:
            return None  # refused under the lock; do not spend a model call
        identity=[self.workspace_id,context.principal_id,'record.append',payload['idempotency_key']]
        try:
            if any(c['identity']==identity for _,c in self.chain()):return None
        except Failure:
            pass  # history problems are reported by the locked write itself
        from team_memory.records.preserving import failed_graph
        try:
            built=self.record_builder(deepcopy(source))
        except Exception as exc:
            return dict(deepcopy(source),record_graph=failed_graph(source,'unknown','record-builder',exc))
        if not isinstance(built,dict) or {k:v for k,v in built.items() if k!='record_graph'}!=source:
            raise Failure('INVALID_INPUT','Record builder changed original source')
        return built

    def _apply(self,chain,operation,payload,principal,capabilities,*,replay_at=None,prepared_source=None):
        """One write command on top of chain. Returns (response data, new commit or None).

        Nothing is persisted here. replay_at is set only by reconcile(): the command
        was already authorized and revision-checked on its own line, and keeps its time.
        prepared_source is the payload source with its record_graph; the receipt keeps
        the payload as received.
        """
        replay=replay_at is not None
        snapshot=self.snapshot_from(chain);objects=self.objects_from(chain)
        if not replay and operation=='record.append' and payload['source']['owner']!=principal and 'records:import' not in capabilities:
            raise Failure('FORBIDDEN','Only the source owner or trusted importer can append')
        if operation=='review.apply':
            p=next((p for p in snapshot['proposals'] if p['id']==payload['proposal_id']),None)
            if p is None:raise Failure('NOT_FOUND','Unknown proposal')
            if p['reviewer']!=principal:raise Failure('FORBIDDEN','Original owner must review')
        identity=[self.workspace_id,principal,operation,payload['idempotency_key']]
        for index,(key,commit) in enumerate(chain):
            if commit['identity']==identity:
                # A compact receipt is compared in the form it was received.
                if hydrate_payload(commit['payload'])!=payload:raise Failure('IDEMPOTENCY_CONFLICT','Key is already bound to another payload')
                return dict(snapshot=self.snapshot_from(chain[:index+1]),object_id=commit['object_id'],replayed=True),None
        if not replay and payload['expected_revision']!=snapshot['revision']:raise Failure('STALE_SNAPSHOT','Reload before writing')
        staged=MutableView(self.store.root,objects)
        receipt=payload
        if operation=='record.append':
            sid=payload['source']['id'];env=envelope(prepared_source or payload['source'])
            if self.storage==STORAGE_COMPACT:
                env=compact_record(env)
                receipt=dict(payload,source=compact_record(payload['source']))
            # Compare as readers see them, so full and compact copies of one record agree.
            if sid in objects['sources'] and public_source(objects['sources'][sid],sid)!=public_source(env,sid):
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
            state.review(staged,oid,principal,payload['choice'])
        delta={k:{oid:obj for oid,obj in rows.items() if oid not in objects.get(k,{})}
               for k,rows in staged.objects.items()}
        commit=dict(workspace_id=self.workspace_id,parent=snapshot['id'],revision=snapshot['revision']+1,
                    at=replay_at or self.now(),objects=delta,identity=identity,payload=receipt,object_id=oid)
        next_snapshot=self.snapshot_from(chain+[(digest(commit),commit)])
        return dict(snapshot=next_snapshot,object_id=oid,replayed=False),commit

    def reconcile(self,base):
        """Explicitly linearize divergent histories onto the chosen head `base`.

        Every command recorded after the fork on the other heads (append, proposal,
        review) is applied again on top of base, with its original principal,
        idempotency key and time, through the same checks as a new command.
        All-or-nothing: on the first conflict (for example a source ID with other
        content, or a review of a proposal already closed on base) nothing is written
        and the error names the commit. Existing commit files are never changed;
        a reconciliation record marks the other heads as absorbed.
        Not a contract operation: the caller decides who may run it.
        """
        with self.lock():
            commits=self._commits()
            heads=self._head_keys(commits)
            if base not in heads:raise Failure('NOT_FOUND','Base is not a current head')
            others=sorted(heads-{base})
            chain=self.chain(base)
            if not others:return dict(head=base,replayed=[],skipped=[])
            seen={key for key,_ in chain}
            replayed,skipped,built=[],[],[]
            for head in others:
                for key,commit in self.chain(head):
                    if key in seen:continue
                    seen.add(key)
                    if commit['identity'] is None:
                        raise Failure('INVALID_INPUT','Histories have different origins; reconcile is not possible',item_id=key)
                    _,principal,operation,_=commit['identity']
                    prepared=None
                    stored=commit['objects'].get('sources',{}).get(commit['object_id']) if operation=='record.append' else None
                    if stored is not None:
                        # Keep the extraction made on the original line; never call the model again.
                        prepared=public_source(stored,commit['object_id'])
                    try:
                        data,new=self._apply(chain,operation,hydrate_payload(commit['payload']),principal,frozenset(),
                                             replay_at=commit['at'],prepared_source=prepared)
                    except Failure as exc:
                        raise Failure(exc.issue['code'],f"Reconcile stopped at {key}: {exc.issue['message']}",item_id=key) from exc
                    except (ValueError,KeyError,TypeError) as exc:
                        raise Failure('INVALID_INPUT',f'Reconcile stopped at {key}: {exc}',item_id=key) from exc
                    if new is None:
                        skipped.append(key)  # the same command already exists on base
                        continue
                    chain=chain+[(digest(new),new)]
                    built.append(new)
                    replayed.append(dict(original=key,replayed=digest(new)))
            for new in built:
                self._persist(new)
            result=chain[-1][0]
            self.store.put('module_reconciliations',dict(workspace_id=self.workspace_id,base=base,
                                                          absorbed=others,result=result,at=self.now()))
            self._sync_directories()
            self._remember_head(result)
            self._snapshot_cache=None
            return dict(head=result,replayed=replayed,skipped=skipped)
