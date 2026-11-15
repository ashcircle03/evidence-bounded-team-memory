"""Existing dense/BM25 RRF and review expansion, stopped before generation."""
import hashlib
import json
import os
from pathlib import Path
import tempfile

from team_memory.contracts.validation import check_snapshot
from team_memory.readers.retrieval import ReferenceQA
from team_memory.readers.retrieval_stages import Trace
from .base import Adapter,Failure,issue
from .reader_bridge import reader_for,evidence_from,query_text

TRACE_VERSION='retrieval-trace/v1'


def overlaps(evidence,span):
    return (evidence['kind']=='source' and evidence['source_id']==span['source_id'] and
            max(evidence['start'],span['start'])<min(evidence['end'],span['end']))


def within_budget(evidence,snapshot,limit):
    """Choose what survives the evidence budget; (kept evidence, dropped items).

    Priority: review_state evidence, then the source evidence on both sides of
    each kept state's proposal (the spans answering checks), then the rest in
    retrieval order. If a proposal's sides do not all fit, none of them is
    kept, so no lone side of a conflict or correction remains. The kept
    evidence keeps its original order and IDs. Within budget nothing changes.
    """
    if len(evidence)<=limit:return evidence,[]
    proposals={p['id']:p for p in snapshot['proposals']}
    states=[i for i,e in enumerate(evidence) if e['kind']=='review_state'][:limit]
    chosen=list(states);withheld={}
    for i in states:
        pid=evidence[i]['state_record']['proposal_id'];candidate=proposals[pid]['candidate']
        sides=[j for j,e in enumerate(evidence) if j not in chosen and
               any(overlaps(e,candidate[side]) for side in ('previous','incoming'))]
        if len(chosen)+len(sides)<=limit:chosen+=sides
        else:withheld.update({j:pid for j in sides if j not in withheld})
    for j in range(len(evidence)):
        if len(chosen)>=limit:break
        if j not in chosen and j not in withheld:chosen.append(j)
    dropped=[dict(id=e['id'],kind=e['kind'],reason='proposal_sides_did_not_fit',proposal_id=withheld[j])
             if j in withheld else dict(id=e['id'],kind=e['kind'],reason='below_budget_priority',proposal_id=None)
             for j,e in enumerate(evidence) if j not in chosen]
    return [evidence[j] for j in sorted(chosen)],dropped


def trace_key(snapshot,query,limit):
    blob=json.dumps(dict(snapshot_id=snapshot['id'],query=query,max_evidence=limit),ensure_ascii=False,sort_keys=True)
    return hashlib.sha256(blob.encode('utf-8')).hexdigest()[:24]


def write_trace(directory,key,content):
    """Atomic diagnostic file under the retrieval cache; never team knowledge."""
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix='.pending-',dir=directory)
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as stream:
            stream.write(json.dumps(content,ensure_ascii=False,sort_keys=True,indent=1)+'\n')
        os.replace(tmp,directory/(key+'.json'))
    finally:
        if os.path.exists(tmp):os.unlink(tmp)


class RetrievalAdapter(Adapter):
    module='retrieval'
    capabilities={'evidence.retrieve':'evidence:read','evidence.prepare':'records:write'}

    def __init__(self,workspace_id,reader_factory,cache_root,*,snapshot_loader):
        super().__init__(workspace_id);self.factory=reader_factory;self.cache_root=cache_root;self.snapshot_loader=snapshot_loader

    def execute(self,operation,payload,context):
        snapshot=payload['snapshot'];check_snapshot(snapshot);self.verify_snapshot(snapshot)
        if operation=='evidence.prepare':
            reader=reader_for(self.factory,self.cache_root,snapshot)
            try:prepared=reader.prepare_index()
            except Exception as exc:
                raise Failure('RETRIEVAL_FAILED','Index preparation failed; original records remain saved',retryable=True) from exc
            return dict(snapshot_id=snapshot['id'],**prepared),[]
        query=payload['query']
        if query['time_scope']=='historical':
            raise Failure('TIME_SCOPE_UNAVAILABLE','Legacy vote timestamps cannot prove historical approval state')
        # One diagnostic file per request input under cache_root/traces. Timings are a
        # separate field. A trace that cannot be written fails the request (IO_FAILURE).
        trace=Trace();limit=payload['max_evidence']
        content=dict(version=TRACE_VERSION,snapshot_id=snapshot['id'],query=query,max_evidence=limit,
                     outcome=dict(status='error',codes=[]))
        try:
            data,errors=self.retrieve(snapshot,query,limit,trace)
            content['outcome']=dict(status='partial' if errors else 'ok',codes=[e['code'] for e in errors])
        except Failure as exc:
            content['outcome']=dict(status='error',codes=[exc.issue['code']])
            raise
        finally:
            content.update(trace.data,failure=trace.failure)
            write_trace(Path(self.cache_root)/'traces',trace_key(snapshot,query,limit),dict(content,timings_ms=trace.timings_ms))
        return data,errors

    def retrieve(self,snapshot,query,limit,trace):
        reader=reader_for(self.factory,self.cache_root,snapshot)
        from team_memory.readers.indexing import IndexNotReady
        try:
            prepared=ReferenceQA.ask(reader,query_text(query),retrieve_only=True,trace=trace)
        except IndexNotReady as exc:
            raise Failure('INDEX_STALE',str(exc),retryable=True) from exc
        except Exception:raise Failure('RETRIEVAL_FAILED','Retrieval or citation preparation failed')
        from team_memory.records.graph import linked_span
        sources={s['id']:s for s in snapshot['sources']}
        try:
            with trace.stage('spans'):
                for w in prepared['witnesses']:
                    if w.get('evidence_type')!='review_state':
                        source=sources[w['source_id']]
                        a,b=linked_span(source,w['start'],w['end'])
                        w.update(start=a,end=b,quote=source['text'][a:b])
                found=[evidence_from(w,snapshot,i) for i,w in enumerate(prepared['witnesses'],1)]
            with trace.stage('budget'):
                evidence,dropped=within_budget(found,snapshot,limit)
        except Exception:raise Failure('RETRIEVAL_FAILED','Evidence spans or budget could not be prepared')
        trace.record('review_state_evidence',[dict(id=e['id'],proposal_id=e['state_record']['proposal_id'])
                                              for e in found if e['kind']=='review_state'])
        trace.record('budget',dict(limit=limit,dropped=dropped))
        trace.record('final_evidence_ids',[e['id'] for e in evidence])
        ids={e['state_record']['proposal_id'] for e in evidence if e['kind']=='review_state'}
        unresolved=[p['id'] for p in snapshot['proposals'] if p['id'] in ids and
                    (p['status'] in ('pending','review_conflict') or
                     p['candidate']['kind']=='conflict' and p['status']=='approved')]
        coverage='incomplete' if dropped else ('hits' if evidence else 'no_hits')
        return dict(snapshot=snapshot,query=query,evidence=evidence,coverage=coverage,
                    unresolved_proposal_ids=unresolved),([issue('BUDGET_EXCEEDED','Evidence bundle was truncated')] if dropped else [])
