"""Team-record adapter over the upstream CUPMem writer and query engine.

The engine owns memory extraction, updates, retrieval and reasoning. This layer
preserves source envelopes and follows its selected evidence back to originals.
No independent QA/compare model or automatic team approval is introduced.
"""
import json
import time
from .store import source_envelope
from evaluation.cupmem.transfer_inputs import attributed_session
from evaluation.cupmem.provenance import resolve_grounding, persistent_state_hash

REVIEW_QUESTION = ('Given the most recently ingested team report, does it provide evidence to '
    'reconsider an earlier decision? State the earlier decision and its original reason, the '
    'changed condition if any, and what should be reconsidered. Preserve earlier observations '
    'that remain true under their original conditions. If no relevant condition changed, say '
    'that no reconsideration is warranted. A recommendation is not an approval.')


class CUPMemTeamMemory:
    def __init__(self, engine, recorded_calls, source_generate=None):
        self.engine=engine;self.recorded_calls=recorded_calls
        self.source_generate=source_generate
        self.sources=[];self.sessions=[];self.queries={};self.started=time.monotonic()

    def snapshot(self):
        return self.engine._build_sample_result(item={'uid':'team-development'},sample_index=0,
            session_mode='full',selected_session_indices=list(range(len(self.sessions))),
            session_logs=self.sessions,query_logs=self.queries,run_status='development',
            current_phase='interactive_core',sample_elapsed_seconds=time.monotonic()-self.started)

    def ingest(self, source, *, review_changes=True):
        env=source_envelope(source);index=len(self.sources)
        log=self.engine.write_session(session=attributed_session(env),session_index=index,
                                      session_time=env['observed_at'])
        self.sources.append(env);self.sessions.append(log)
        result=dict(source=env,native_write=log,review=None)
        if index and review_changes:result['review']=self.ask(REVIEW_QUESTION)
        return result

    def ask(self, question):
        from cup_mem.llm_layer.client import parse_json_object_with_repair
        start=len(self.recorded_calls());label='q_'+str(len(self.queries))
        before=self.snapshot()
        try:
            result=self.engine.answer_query(query_label=label,query_text=question)
        finally:
            snapshot=self.snapshot()
            if persistent_state_hash(before)!=persistent_state_hash(snapshot):
                raise AssertionError('Native QA changed persistent memory')
        self.queries[label]=result
        payload=result.get('debug_trace',{}).get('query',{}).get('answer_composer_raw_payload')
        matches=[]
        for call in self.recorded_calls()[start:]:
            if 'response' not in call:continue
            try:
                raw=call['response']['choices'][0]['message']['content']
                parsed,mode=parse_json_object_with_repair(raw)
                if parsed!=payload:continue
                for message in call['request']['messages']:
                    if message['role']!='user':continue
                    try:body=json.loads(message['content'])
                    except ValueError:continue
                    if body.get('query')==question and isinstance(body.get('canonical_answer_grounding'),dict):
                        matches.append((body['canonical_answer_grounding'],mode))
            except (ValueError,KeyError,TypeError):continue
        citations=[];provenance=None;errors=[]
        if len(matches)==1:
            provenance=resolve_grounding(matches[0][0],snapshot)
            errors.extend(provenance['unresolved'])
            for passage in provenance['reader_payload']['passages']:
                try:
                    env=json.loads(passage['text']);index=passage['session_index']
                    if env!=self.sources[index]:raise ValueError('selected source does not match original arrival')
                    citations.append(dict(source=env['source'],owner=env['owner'],observed_at=env['observed_at'],
                        session_index=index,native_reference=passage['citation_id'],
                        scope='original record supporting native-selected memory; not sentence-level entailment'))
                except (ValueError,KeyError,IndexError,TypeError) as exc:errors.append(str(exc))
        else:errors.append('Final native composer could not be uniquely linked to its actual response')
        output=dict(question=question,answer=result['answer'],citations=citations,
                    provenance_errors=errors,native_query=result,provenance=provenance,
                    approval='not_approved',backend='upstream CUPMem',source_count=len(self.sources))
        if self.source_generate is not None:
            from .cupmem_readout import read_selected_sources
            output['grounded_answer']=read_selected_sources(output,self.source_generate)
        return output
