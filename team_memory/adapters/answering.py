"""Answering port: routes a fixed evidence bundle through team_memory.answering.

The steps live in answering/pipeline.py; this port checks the snapshot,
builds the reader, maps failures to contract errors and persists diagnostics.
Sentence-local citation ownership is mechanical, not a new semantic verifier.
Uncited text stays in private diagnostics, never receives fabricated evidence.
"""
from team_memory.storage.objects import Store
from team_memory.answering.scoped import public_answer
from team_memory.answering.pipeline import evidence_problem,use_scoped,run_strategies,claims_from_result
from .base import Adapter,Failure,issue
from .reader_bridge import reader_for,witnesses_from,context_from,query_text,claim_views


class AnsweringAdapter(Adapter):
    module='answering'
    capabilities={'answer.generate':'answer:generate'}

    def __init__(self,workspace_id,reader_factory,cache_root,*,snapshot_loader):
        super().__init__(workspace_id);self.factory=reader_factory;self.cache_root=cache_root;self.snapshot_loader=snapshot_loader
        self.diagnostics=Store(cache_root)

    def execute(self,operation,payload,context):
        bundle=payload['bundle'];witnesses=witnesses_from(bundle);self.verify_snapshot(bundle['snapshot'])
        if bundle['query']['time_scope']=='historical':raise Failure('TIME_SCOPE_UNAVAILABLE','Historical state is not supported by this bridge')
        answer=dict(snapshot_id=bundle['snapshot']['id'],outcome='abstained',claims=[],reason='No retrieved evidence supports an answer.')
        if not witnesses:return answer,[]
        if bundle['coverage']=='incomplete':
            answer['reason']='Evidence bundle is incomplete; no answer generated.'
            return answer,[issue('BUDGET_EXCEEDED','Retrieve a complete evidence bundle before generation')]
        problem=evidence_problem(bundle)
        if problem:
            answer['reason']=problem[0]
            return answer,[problem[1]]
        reader=reader_for(self.factory,self.cache_root,bundle['snapshot'])
        question=query_text(bundle['query']);review=context_from(bundle,reader)
        try:
            with reader.lock:
                views = claim_views(bundle['evidence'], bundle['snapshot'])
                scoped_rejected=None
                if use_scoped(reader,bundle,views,review):
                    draft=response=None
                    try:
                        draft = reader.generate_scoped(bundle['query'], views)
                        response = public_answer(draft, bundle, views)
                    except ValueError as exc:
                        # The scoped draft failed a mechanical check (fewer than two grounded
                        # scopes, a quote missing from its evidence, malformed output). The
                        # check stays; the question is answered on the regular path instead.
                        scoped_rejected=dict(reason=str(exc)[:300],draft=draft.model_dump() if draft is not None else None)
                    if response is not None:
                        try:
                            self.diagnostics.put('answer_diagnostics', dict(bundle=bundle, scoped_draft=draft.model_dump()))
                        except OSError:
                            return response,[issue('IO_FAILURE','Answer preserved but diagnostic persistence failed')]
                        return response,[]
                result=run_strategies(reader,question,witnesses,review)
                if scoped_rejected:result=dict(result,scoped_rejected=scoped_rejected)
        except TimeoutError:raise Failure('MODEL_TIMEOUT','Answer generation timed out')
        except Exception:raise Failure('MODEL_OUTPUT_INVALID','Answer generation failed')
        diagnostic_errors=[]
        try:self.diagnostics.put('answer_diagnostics',dict(bundle=bundle,result=result))
        except OSError:diagnostic_errors.append(issue('IO_FAILURE','Answer preserved but diagnostic persistence failed'))
        return claims_from_result(answer,bundle,witnesses,views,result,diagnostic_errors)
