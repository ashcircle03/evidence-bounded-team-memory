"""Existing dense/BM25 RRF and review expansion, stopped before generation."""
from collections import OrderedDict
import hashlib
import json
import os
from pathlib import Path
import tempfile
from threading import Lock

from team_memory.contracts.validation import check_snapshot
from team_memory.retrieval.search import ReferenceQA
from team_memory.retrieval.stages import ConditionFilteredCandidates,LlamaIndexCandidates,ThresholdedCandidates,Trace
from .base import Adapter,Failure,issue
from .reader_bridge import reader_for,evidence_from,query_text

TRACE_VERSION='retrieval-trace/v1'
READER_CACHE_SIZE=4


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


def record_conditions(source,start,end):
    """Condition quotes records links to claims inside [start,end), as evidence_from reports them."""
    if source is None:return []
    from team_memory.records.graph import describe
    description=describe(source,start,end)
    return list(dict.fromkeys(u['quote'] for c in description['claims'] for u in c['condition'])) if description else []


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
    capabilities={'evidence.retrieve':'evidence:read','evidence.prepare':'records:write','history.search':'records:write'}

    def __init__(self,workspace_id,reader_factory,cache_root,*,snapshot_loader,min_dense_score=None,min_sparse_score=None,
                 condition_filter=False):
        super().__init__(workspace_id);self.factory=reader_factory;self.cache_root=cache_root;self.snapshot_loader=snapshot_loader
        # "Not in the records" gate, off by default. Values are set later from development data.
        for value in (min_dense_score,min_sparse_score):
            if value is not None and (isinstance(value,bool) or not isinstance(value,(int,float))):
                raise ValueError('Score thresholds must be numbers or None')
        self.min_dense_score,self.min_sparse_score=min_dense_score,min_sparse_score
        # Records condition filter for query.conditions, off by default (not yet measured).
        if not isinstance(condition_filter,bool):raise ValueError('condition_filter must be True or False')
        self.condition_filter=condition_filter
        self._readers=OrderedDict();self._readers_lock=Lock()

    def reader(self,snapshot):
        """The bridged reader for a verified snapshot, built once per snapshot ID.

        A snapshot is immutable and execute() has already compared it with the
        authoritative records, so converting it to the v2 store again (envelope
        and record_graph validation, vote reduction) would give the same reader.
        The reader also keeps its loaded index. Only the latest few are kept.
        """
        key=snapshot['id']
        with self._readers_lock:
            if key in self._readers:
                self._readers.move_to_end(key);return self._readers[key]
        reader=reader_for(self.factory,self.cache_root,snapshot)
        with self._readers_lock:
            reader=self._readers.setdefault(key,reader);self._readers.move_to_end(key)
            while len(self._readers)>READER_CACHE_SIZE:self._readers.popitem(last=False)
        return reader

    def execute(self,operation,payload,context):
        snapshot=payload['snapshot'];check_snapshot(snapshot);self.verify_snapshot(snapshot)
        if operation=='history.search':
            return self.search_history(snapshot,payload['incoming_source_id'],payload['limit']),[]
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

    def search_history(self, snapshot, incoming_id, limit):
        """Rank distinct prior sources; sparse corpus statistics exclude the incoming text."""
        from team_memory.retrieval.stages import StagedRetriever
        sources = {s['id']: s for s in snapshot['sources']}
        if incoming_id not in sources:
            raise Failure('INVALID_INPUT', 'Unknown incoming record')
        incoming = sources.pop(incoming_id)
        spans = []
        if sources:
            # Reuse the prior generation by source/config key; reviews never enter candidate search.
            history = dict(snapshot, sources=list(sources.values()), proposals=[])
            reader = reader_for(self.factory, self.cache_root, history)
            try:
                reader.prepare_index()
                source = LlamaIndexCandidates(reader.index, reader.top_k, sparse=reader.sparse,
                                              use_sparse=reader.profile == 'team')
                ranked = StagedRetriever(source, llm=reader.llm, fused_top_k=2 * reader.top_k)
                seen = set()
                for hit in ranked.retrieve(incoming['text']):
                    meta = hit.node.metadata
                    sid = meta['source_id']
                    if sid in seen:
                        continue
                    seen.add(sid)
                    a, b = meta['parent_start'], meta['parent_end']
                    spans.append(dict(source_id=sid, start=a, end=b, quote=sources[sid]['text'][a:b]))
                    if len(spans) == limit:
                        break
            except Exception as exc:
                raise Failure('RETRIEVAL_FAILED', 'History candidate search failed', retryable=True) from exc
        return dict(snapshot_id=snapshot['id'], candidates=spans)

    def retrieve(self,snapshot,query,limit,trace):
        reader=self.reader(snapshot)
        sources={s['id']:s for s in snapshot['sources']}
        thresholds=dict(dense=self.min_dense_score,sparse=self.min_sparse_score)
        scored=any(value is not None for value in thresholds.values())
        conditions=[c for c in query['conditions'] if c.strip()] if self.condition_filter else []
        gated=scored or bool(conditions)
        from team_memory.retrieval.indexing import IndexNotReady
        # The reader is shared by requests on the same snapshot: install this request's
        # gate under the reader lock and remove it afterwards, so it never leaks.
        with reader.lock:
            inner=getattr(reader,'candidate_source',None)
            def candidates(index):
                # Same default stage 1 as ReferenceQA.ask, then the score gate and the condition filter.
                base=inner(index) if inner else LlamaIndexCandidates(index,reader.top_k,sparse=reader.sparse,
                                                                      use_sparse=reader.profile=='team')
                if scored:base=ThresholdedCandidates(base,thresholds,trace=trace)
                if conditions:
                    base=ConditionFilteredCandidates(base,conditions,
                        lambda sid,start,end:record_conditions(sources.get(sid),start,end),trace=trace)
                return base
            if gated:reader.candidate_source=candidates
            try:
                prepared=ReferenceQA.ask(reader,query_text(query),retrieve_only=True,trace=trace)
            except IndexNotReady as exc:
                raise Failure('INDEX_STALE',str(exc),retryable=True) from exc
            except Exception:raise Failure('RETRIEVAL_FAILED','Retrieval or citation preparation failed')
            finally:
                if gated:
                    if inner is None:del reader.candidate_source
                    else:reader.candidate_source=inner
        from team_memory.records.graph import linked_span
        try:
            with trace.stage('spans'):
                for w in prepared['witnesses']:
                    if w.get('evidence_type')!='review_state':
                        source=sources[w['source_id']]
                        a,b=linked_span(source,w['start'],w['end'])
                        w.update(start=a,end=b,quote=source['text'][a:b])
                found=[evidence_from(w,snapshot,i,sources) for i,w in enumerate(prepared['witnesses'],1)]
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
