"""Reuse the v2 sentence selector and exact-span binding; never persist here."""
import json
from team_memory.storage.objects import digest,Store
from team_memory.review.comparison import compare_sources
from team_memory.review.state import decode,prepare_relation
from team_memory.contracts.validation import check_snapshot,check_candidate
from .base import Adapter,Failure,issue
from .legacy import envelope,candidate,FrozenStore,native_objects
from team_memory.review.state import view


class RelationsAdapter(Adapter):
    module='relations'
    capabilities={'relations.compare':'relations:compare'}

    def __init__(self,workspace_id,generate,*,snapshot_loader,cache_root):
        super().__init__(workspace_id);self.generate=generate;self.snapshot_loader=snapshot_loader
        self.diagnostics=Store(cache_root)

    def execute(self,operation,payload,context):
        snapshot=payload['snapshot'];check_snapshot(snapshot);self.verify_snapshot(snapshot)
        src={s['id']:s for s in snapshot['sources']}
        incoming=src[payload['incoming_source_id']]
        history=payload['history_source_ids']
        if incoming['id'] in history:raise Failure('INVALID_INPUT','Incoming record is also in history')
        prior=view(FrozenStore(self.diagnostics.root,native_objects(snapshot)),visible=history)
        content=dict(earlier=prior['sources'],incoming=dict(id=incoming['id'],**envelope(incoming)),
                     earlier_relations=prior['relations'])
        if not history:return dict(snapshot_id=snapshot['id'],candidates=[]),[]
        try:
            raw=compare_sources(self.generate,json.dumps(content,ensure_ascii=False))
            parsed=decode(raw)
        except TimeoutError:raise Failure('MODEL_TIMEOUT','Comparison timed out')
        except Exception:raise Failure('MODEL_OUTPUT_INVALID','Comparison failed; no negative judgment inferred')
        diagnostic_errors=[]
        try:self.diagnostics.put('comparison_diagnostics',dict(snapshot_id=snapshot['id'],content=content,raw=raw))
        except OSError:diagnostic_errors.append(issue('IO_FAILURE','Comparison diagnostic persistence failed'))
        if not isinstance(parsed.get('relations'),list):raise Failure('MODEL_OUTPUT_INVALID','Comparison returned an invalid relation list')
        errors=diagnostic_errors+[issue('MODEL_OUTPUT_INVALID','Sentence selection failed',str(i))
                for i,_ in enumerate(parsed.get('selection_errors',[]))]
        candidates=[]
        for i,row in enumerate(parsed.get('relations',[])+parsed.get('informational_relations',[])):
            try:
                target=row['target']
                if target not in history:raise ValueError('Unavailable target')
                old,new=envelope(src[target]),envelope(incoming)
                bound=prepare_relation(dict(row,target=digest(old)),{digest(old):old},new,
                                       informational=row['kind']=='coexist')
                c=candidate(bound)
                c.update(comparison_snapshot_id=snapshot['id'],history_source_ids=history)
                for side,sid in (('previous',target),('incoming',incoming['id'])):
                    c[side]['source_id']=sid
                    if c[side+'_assertion'] is not None:c[side+'_assertion']['source_id']=sid
                check_candidate(c,snapshot);candidates.append(c)
            except (ValueError,KeyError,TypeError):errors.append(issue('MODEL_OUTPUT_INVALID','Invalid relation or span',str(i)))
        keys=[(c['kind'],c['previous']['source_id']) for c in candidates]
        unique=[]
        for c,key in zip(candidates,keys):
            if keys.count(key)==1:unique.append(c)
            else:errors.append(issue('MODEL_OUTPUT_INVALID','Ambiguous duplicate relation',key[1]))
        if errors and not unique:raise Failure('MODEL_OUTPUT_INVALID','All proposed relations failed validation')
        return dict(snapshot_id=snapshot['id'],candidates=unique),errors
