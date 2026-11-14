"""Run the existing synthesis/check/AQA/citation pipeline on a fixed bundle.

Sentence-local citation ownership is mechanical, not a new semantic verifier.
Uncited text stays in private diagnostics, never receives fabricated evidence.
"""
from copy import deepcopy
import re
from nltk.tokenize import PunktTokenizer
from team_memory.storage.objects import Store
from team_memory.readers.attribution import AttributedQA,ConflictCheckedQA,repair_omitted_answer,attach_citations
from team_memory.readers.fallback import preserve_answer
from .base import Adapter,Failure,issue
from .reader_bridge import reader_for,witnesses_from,context_from,query_text


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
        # A caller can replace the retrieval port, but cannot silently omit the
        # state or opposing record for a selected, reviewed assertion.
        source_ids={e['source_id'] for e in bundle['evidence'] if e['kind']=='source'}
        state_ids={e['state_record']['proposal_id'] for e in bundle['evidence'] if e['kind']=='review_state'}
        texts={s['id']:s['text'] for s in bundle['snapshot']['sources']}
        def covered(span):
            cursor=span['start']
            for e in sorted((e for e in bundle['evidence'] if e['kind']=='source' and e['source_id']==span['source_id']),key=lambda e:e['start']):
                if e['end']<=cursor or e['start']>=span['end']:continue
                if e['start']>cursor and texts[span['source_id']][cursor:e['start']].strip():return False
                cursor=max(cursor,min(span['end'],e['end']))
            return not texts[span['source_id']][cursor:span['end']].strip()
        for proposal in bundle['snapshot']['proposals']:
            c=proposal['candidate']
            if c['kind']=='coexist':continue
            spans=[c.get(side+'_assertion') or c[side] for side in ('previous','incoming')]
            touched=any(e['kind']=='source' and e['source_id']==s['source_id'] and
                        max(e['start'],s['start'])<min(e['end'],s['end'])
                        for e in bundle['evidence'] for s in spans)
            if touched and (proposal['id'] not in state_ids or any(s['source_id'] not in source_ids for s in spans)):
                answer['reason']='A selected reviewed assertion is missing its paired source or review state.'
                return answer,[issue('EVIDENCE_INVALID','Incomplete review evidence',proposal['id'])]
            if proposal['id'] in state_ids and not all(covered(c[side]) for side in ('previous','incoming')):
                answer['reason']='Review context quotes extend outside the supplied evidence.'
                return answer,[issue('EVIDENCE_INVALID','Review context cannot introduce hidden source text',proposal['id'])]
        reader=reader_for(self.factory,self.cache_root,bundle['snapshot'])
        question=query_text(bundle['query']);review=context_from(bundle,reader)
        try:
            with reader.lock:
                result=reader.generate_evidence(question,witnesses,review)
                if isinstance(reader,ConflictCheckedQA):
                    result=preserve_answer(result,'document_review',lambda:reader._review(question,result))
                if isinstance(reader,AttributedQA):
                    result=repair_omitted_answer(question,result,reader.llm,context=review)
                result=attach_citations(reader,question,result)
        except TimeoutError:raise Failure('MODEL_TIMEOUT','Answer generation timed out')
        except Exception:raise Failure('MODEL_OUTPUT_INVALID','Answer generation failed')
        diagnostic_errors=[]
        try:self.diagnostics.put('answer_diagnostics',dict(bundle=bundle,result=result))
        except OSError:diagnostic_errors.append(issue('IO_FAILURE','Answer preserved but diagnostic persistence failed'))
        # Existing repairs may add a state witness. It must already be in the
        # received packet; the answering port cannot add hidden evidence.
        evidence=bundle['evidence'];errors=diagnostic_errors;claims=[];unattributed=[]
        raw=result['raw']
        spans=list(PunktTokenizer('english').span_tokenize(raw))
        for index,(start,end) in enumerate(spans):
            # Preserve whitespace and original answer bytes across claim units.
            stop=spans[index+1][0] if index+1<len(spans) else len(raw)
            text=raw[0 if index==0 else start:stop]
            numbers=set()
            numbers.update(int(n) for n in re.findall(r'\[(\d+)\]',text))
            numbers.update(int(n) for n in re.findall(r'\bSource\s+(\d+)\b',text,re.I))
            owned=[]
            for number in sorted(numbers):
                if not 1<=number<=len(result['citation_sources']):continue
                w=result['citation_sources'][number-1]
                for ei,original in enumerate(witnesses):
                    if all(w.get(k)==original.get(k) for k in ('source_id','start','end','quote')):
                        owned.append(evidence[ei]['id']);break
            owned=list(dict.fromkeys(owned))
            cid=f'c{index+1}'
            if not owned:
                unattributed.append(dict(start=0 if index==0 else start,end=stop,text=text))
                errors.append(issue('UNSUPPORTED_CLAIM','Sentence has no citation in the supplied packet',cid));continue
            kind='state' if any(e['kind']=='review_state' and e['id'] in owned for e in evidence) else 'reported_fact'
            claims.append(dict(id=cid,text=text,kind=kind,evidence_ids=owned,conditions=[],alternative_group=None,
                               answer_span=dict(start=0 if index==0 else start,end=stop)))
        if claims:
            answer.update(claims=claims,outcome='answered',reason=None)
            # Only mark a conflict when two separately cited answer units exist.
            for proposal in bundle['snapshot']['proposals']:
                if proposal['id'] not in bundle['unresolved_proposal_ids'] or proposal['candidate']['kind']!='conflict':continue
                sides=[]
                for side in ('previous','incoming'):
                    sid=proposal['candidate'][side]['source_id']
                    eids={e['id'] for e in evidence if e['source_id']==sid}
                    sides.append([c for c in claims if eids.intersection(c['evidence_ids'])])
                if sides[0] and sides[1] and any(a['id']!=b['id'] and a['evidence_ids']!=b['evidence_ids'] for a in sides[0] for b in sides[1]):
                    for c in sides[0]+sides[1]:c['alternative_group']=proposal['id']
                    answer['outcome']='conflict'
        if result.get('status')=='partial' or result.get('aqa_candidate_accepted'):
            errors.append(issue('UNSUPPORTED_CLAIM','Legacy reader reports incomplete or unverified attribution'))
        if not claims:answer['reason']='No answer sentence has valid citations in the supplied packet.'
        if raw and not spans:unattributed=[dict(start=0,end=len(raw),text=raw)]
        answer.update(original_text=raw,unattributed=unattributed)
        if result.get('aqa_candidate_accepted'):
            previous=[]
            for a in result.get('aqa_prior_answers',[]):
                for w in a['evidence']:
                    previous.extend(evidence[i]['id'] for i,original in enumerate(witnesses)
                        if all(w.get(k)==original.get(k) for k in ('source_id','start','end','quote')))
            answer['unverified_revision']=dict(original_text=result['pre_aqa_raw'],candidate_text=raw,
                original_evidence_ids=list(dict.fromkeys(previous)),acceptance_basis='source_id_coverage_only')
        return answer,errors
