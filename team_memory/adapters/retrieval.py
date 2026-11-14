"""Existing dense/BM25 RRF and review expansion, stopped before generation."""
import fcntl
from pathlib import Path
from team_memory.contracts.validation import check_snapshot
from team_memory.readers.retrieval import ReferenceQA
from .base import Adapter,Failure,issue
from .reader_bridge import reader_for,evidence_from,query_text


class RetrievalAdapter(Adapter):
    module='retrieval'
    capabilities={'evidence.retrieve':'evidence:read'}

    def __init__(self,workspace_id,reader_factory,cache_root,*,snapshot_loader):
        super().__init__(workspace_id);self.factory=reader_factory;self.cache_root=cache_root;self.snapshot_loader=snapshot_loader

    def execute(self,operation,payload,context):
        snapshot=payload['snapshot'];check_snapshot(snapshot);self.verify_snapshot(snapshot)
        query=payload['query']
        if query['time_scope']=='historical':
            raise Failure('TIME_SCOPE_UNAVAILABLE','Legacy vote timestamps cannot prove historical approval state')
        reader=reader_for(self.factory,self.cache_root,snapshot)
        try:
            cache=Path(self.cache_root);cache.mkdir(parents=True,exist_ok=True)
            with (cache/'index.lock').open('a') as lock,reader.lock:
                fcntl.flock(lock,fcntl.LOCK_EX)
                prepared=ReferenceQA.ask(reader,query_text(query),retrieve_only=True)
        except Exception:raise Failure('RETRIEVAL_FAILED','Retrieval or citation preparation failed')
        evidence=[evidence_from(w,snapshot,i) for i,w in enumerate(prepared['witnesses'],1)]
        truncated=len(evidence)>payload['max_evidence']
        evidence=evidence[:payload['max_evidence']]
        ids={e['state_record']['proposal_id'] for e in evidence if e['kind']=='review_state'}
        unresolved=[p['id'] for p in snapshot['proposals'] if p['id'] in ids and
                    (p['status'] in ('pending','review_conflict') or
                     p['candidate']['kind']=='conflict' and p['status']=='approved')]
        coverage='incomplete' if truncated else ('hits' if evidence else 'no_hits')
        return dict(snapshot=snapshot,query=query,evidence=evidence,coverage=coverage,
                    unresolved_proposal_ids=unresolved),([issue('BUDGET_EXCEEDED','Evidence bundle was truncated')] if truncated else [])
