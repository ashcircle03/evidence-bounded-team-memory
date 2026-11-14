"""Lossless envelope/span bridges; native reducers remain the authority."""
from copy import deepcopy
from team_memory.storage.objects import Store, digest
from team_memory.storage.sources import source_envelope
from team_memory.contracts.validation import render_state


def envelope(source):
    result=dict(owner=source['owner'],observed_at=source['observed_at'],
                source={k:source[k] for k in ('speaker','location','text')})
    source_envelope(result)  # Reuse v2 validation without normalizing input metadata.
    return result


def public_source(env, sid=None):
    return dict(id=sid or digest(env),owner=env['owner'],observed_at=env['observed_at'],**env['source'])


def span(witness):
    return {k:witness[k] for k in ('source_id','start','end','quote')}


def candidate(p):
    c=dict(kind=p['kind'],previous=span(p['previous']),incoming=span(p['incoming']),reason=p['reason'],
        previous_assertion=span(p.get('previous_assertion',p['previous'])) if p['kind']=='correction' else None,
        incoming_assertion=span(p.get('incoming_assertion',p['incoming'])) if p['kind']=='correction' else None)
    if 'comparison_snapshot_id' in p:c.update(comparison_snapshot_id=p['comparison_snapshot_id'],history_source_ids=p['history'])
    return c


def witness(w, source_map):
    source=source_map[w['source_id']]
    return dict(w,location=source['location'],speaker=source['speaker'])


def native_objects(snapshot):
    src={s['id']:s for s in snapshot['sources']}
    objects=dict(sources={sid:envelope(s) for sid,s in src.items()},timeline_proposals={},timeline_votes={})
    for row in snapshot['proposals']:
        c=row['candidate']
        if c['kind']=='coexist':continue
        p=dict(kind=c['kind'],reason=c['reason'],reviewer=row['reviewer'],
               history=row.get('history_source_ids',[c['previous']['source_id']]),
               previous=witness(c['previous'],src),incoming=witness(c['incoming'],src))
        if c['kind']=='correction':
            p.update(previous_assertion=witness(c['previous_assertion'],src),
                     incoming_assertion=witness(c['incoming_assertion'],src))
        if 'comparison_snapshot_id' in c:p['comparison_snapshot_id']=c['comparison_snapshot_id']
        objects['timeline_proposals'][row['id']]=p
        choices={'approved':['approve'],'rejected':['reject'],'review_conflict':['approve','reject']}.get(row['status'],[])
        for choice in choices:
            vote=dict(proposal=row['id'],actor=row['reviewer'],choice=choice)
            objects['timeline_votes'][digest(vote)]=vote
    return objects


def state_witness(snapshot,p):
    text=render_state(p,snapshot['id'])
    return dict(source_id='review:'+digest([snapshot['id'],p['id']]),evidence_type='review_state',
        snapshot_id=snapshot['id'],proposal_id=p['id'],location='module_snapshots/'+snapshot['id'],
        speaker='timeline state reducer',observed_at=None,start=0,end=len(text),quote=text)


class FrozenStore(Store):
    """A v2 Store view that cannot write authoritative records."""
    def __init__(self, root, objects, snapshot=None):
        super().__init__(root)
        self.objects=deepcopy(objects)
        self.contract_snapshot=deepcopy(snapshot)

    def load(self, kind):
        if kind in self.objects:return deepcopy(self.objects[kind])
        if kind=='review_snapshots':return super().load(kind)
        return {}

    def put(self, kind, obj):
        if kind!='review_snapshots':raise PermissionError('Frozen source/review state is read-only')
        return super().put(kind,obj)  # Derived cache only, never team knowledge.


class MutableView(FrozenStore):
    """Private transaction overlay, committed once by RecordsAdapter."""
    def put(self,kind,obj):
        key=digest(obj)
        self.objects.setdefault(kind,{})[key]=deepcopy(obj)
        return key
