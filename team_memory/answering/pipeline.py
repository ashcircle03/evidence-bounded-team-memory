"""Answering steps on a fixed evidence bundle. Moved verbatim from the port
(adapters/answering.py) so the port only routes, persists and reports.

  evidence_problem    the bundle must carry the paired source and review state
                      of every selected reviewed assertion (mechanical check)
  use_scoped          several condition scopes -> conditional structured answer
  run_strategies      generation, then the optional strategies the reader enables
                      (ConflictScore review, AQA repair, citation repair)
  claims_from_result  sentence-local citation ownership, uncited text kept apart,
                      conflict only when both sides are cited separately; an
                      answer stating one side of an unresolved conflict
                      (evidence inside its assertion span) is flagged
No step retrieves, approves or adds evidence.
"""
import re

from nltk.tokenize import PunktTokenizer

from team_memory.answering.fallback import preserve_answer
from team_memory.answering.strategies.attribution import AttributedQA, ConflictCheckedQA, repair_omitted_answer, attach_citations


def _issue(code, message, item_id=None):
    # Same shape as adapters.base.issue; answering does not import the adapters.
    return dict(code=code, message=message, retryable=False, item_id=item_id)


def evidence_problem(bundle):
    """(reason, error) when a selected reviewed assertion lacks its pair or state, else None.

    A caller can replace the retrieval port, but cannot silently omit the
    state or opposing record for a selected, reviewed assertion.
    """
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
            return ('A selected reviewed assertion is missing its paired source or review state.',
                    _issue('EVIDENCE_INVALID','Incomplete review evidence',proposal['id']))
        if proposal['id'] in state_ids and not all(covered(c[side]) for side in ('previous','incoming')):
            return ('Review context quotes extend outside the supplied evidence.',
                    _issue('EVIDENCE_INVALID','Review context cannot introduce hidden source text',proposal['id']))
    return None


def use_scoped(reader, bundle, views, review):
    """Corrections and unresolved relations retain the dedicated state path."""
    scopes = {frozenset(e['conditions']) for e in views if e['kind']=='source' and e['conditions']}
    review_only = all(r['kind']=='reconsider' for r in (review or {}).get('relations', []))
    return len(scopes)>1 and review_only and not bundle['unresolved_proposal_ids'] and hasattr(reader, 'generate_scoped')


def run_strategies(reader, question, witnesses, review):
    """Generation, then each strategy the reader class enables (unchanged order)."""
    result=reader.generate_evidence(question,witnesses,review)
    if isinstance(reader,ConflictCheckedQA):
        result=preserve_answer(result,'document_review',lambda:reader._review(question,result))
    if isinstance(reader,AttributedQA):
        result=repair_omitted_answer(question,result,reader.llm,context=review)
    return attach_citations(reader,question,result)


def one_side_stated(proposal, evidence, claims):
    """True when a claim cites evidence lying inside one conflicting assertion.

    Only assertion-level proposals are checked: a passage that merely overlaps
    a side may be cited for an unrelated fact in the same passage.
    """
    candidate = proposal['candidate']
    spans = [candidate.get(side + '_assertion') for side in ('previous', 'incoming')]
    if not all(spans):
        return False
    inside = {e['id'] for e in evidence for s in spans if e['kind'] == 'source'
              and e['source_id'] == s['source_id'] and s['start'] <= e['start'] and e['end'] <= s['end']}
    return any(inside.intersection(c['evidence_ids']) for c in claims)


def claims_from_result(answer, bundle, witnesses, views, result, errors):
    """Fill answer claims from the generated text; returns (answer, errors).

    Existing repairs may add a state witness. It must already be in the
    received packet; the answering port cannot add hidden evidence.
    """
    evidence=bundle['evidence'];claims=[];unattributed=[]
    by_id = {e['id']: e for e in evidence}
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
            errors.append(_issue('UNSUPPORTED_CLAIM','Sentence has no citation in the supplied packet',cid));continue
        kind='state' if any(e['kind']=='review_state' and e['id'] in owned for e in evidence) else 'reported_fact'
        # Retain requested scope only when every cited source carries it.
        sources = [by_id[eid] for eid in owned if by_id[eid]['kind'] == 'source']
        conditions = [scope for scope in bundle['query']['conditions']
                      if sources and all(scope in v['conditions'] for src in sources for v in views
                                      if v.get('evidence_id', v['id']) == src['id'])]
        claims.append(dict(id=cid,text=text,kind=kind,evidence_ids=owned,conditions=conditions,alternative_group=None,
                           answer_span=dict(start=0 if index==0 else start,end=stop)))
    if claims:
        answer.update(claims=claims,outcome='answered',reason=None)
        # Only mark a conflict when two separately cited answer units exist.
        for proposal in bundle['snapshot']['proposals']:
            if proposal['id'] not in bundle['unresolved_proposal_ids'] or proposal['candidate']['kind']!='conflict':continue
            sides=[]
            for side in ('previous','incoming'):
                span = proposal['candidate'].get(side + '_assertion') or proposal['candidate'][side]
                eids = {e['id'] for e in evidence if e['kind'] == 'source'
                        and e['source_id'] == span['source_id']
                        and max(e['start'], span['start']) < min(e['end'], span['end'])}
                sides.append([c for c in claims if eids.intersection(c['evidence_ids'])])
            if sides[0] and sides[1] and any(a['id']!=b['id'] and a['evidence_ids']!=b['evidence_ids'] for a in sides[0] for b in sides[1]):
                for c in sides[0]+sides[1]:c['alternative_group']=proposal['id']
                answer['outcome']='conflict'
            elif one_side_stated(proposal, evidence, claims):
                # F04/F06: an unresolved conflict presents both sides in separate
                # claims. Otherwise it is flagged; no side is picked or added.
                errors.append(_issue('UNSUPPORTED_CLAIM','Answer does not cite both sides of an unresolved conflict separately',proposal['id']))
    if result.get('status')=='partial' or result.get('aqa_candidate_accepted'):
        errors.append(_issue('UNSUPPORTED_CLAIM','Legacy reader reports incomplete or unverified attribution'))
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
