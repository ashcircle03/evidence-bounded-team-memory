"""LangChain fact/quote attribution, adapted to an immutable existing answer.

Quoted passages are returned with exact offsets; that validates provenance, not
semantic entailment. Use full answer context for pronouns and source conditions.
"""
from copy import deepcopy
import json
import re
from llama_index.core.llms import ChatMessage
from nltk.tokenize import PunktTokenizer
from ._vendor.langchain_citation import QuestionAnswer
from .reference_qa import format_response
from .reference_fallback import preserve_answer, carry_diagnostics, stage_failure


def quote_span(quote,context):
    """Recover literal words with layout whitespace; no edit-distance tolerance.

    The upstream LangChain matcher allows fuzzy regex edit distance. This
    adapter only tolerates whitespace: escape every non-whitespace token so
    code punctuation, entities and conditions must still match literally.
    """
    parts=quote.split()
    if not parts:return None
    match=re.search(r'\s+'.join(re.escape(part) for part in parts),context)
    return match.span() if match else None


def uncited_sentences(raw):
    return [dict(start=a,end=b,sentence=raw[a:b])
            for a,b in PunktTokenizer('english').span_tokenize(raw)
            if re.search(r'[A-Za-z0-9]',raw[a:b])
            and not re.search(r'\[\d+\]|\bSource\s+\d+\b',raw[a:b],re.I)]


def quote_messages(question,raw,witnesses,sentences):
    context='\n\n'.join(f"Source {i}:\n{w['quote']}" for i,w in enumerate(witnesses,1))
    return [ChatMessage(role='system',content='You are a world class algorithm to answer questions with correct and exact citations.'),
        ChatMessage(role='user',content=f'''Attach evidence to the existing answer using the context. Preserve every fact exactly as supplied. Read the full answer to resolve references such as "this variable". Each quote must support the corresponding fact about the same subject and conditions. Return no quote when the context does not support it. Do not rewrite the answer.

Context:
{context}

Question: {question}
Existing answer:
{raw}

Facts requiring attribution:
{json.dumps([s['sentence'] for s in sentences],ensure_ascii=False)}

Tips: Make sure to cite your sources, and use the exact words from the context.
Return only JSON matching this schema. Include every requested fact once; substring_quote may be empty. Quotes are literal substrings from Source text, without Source labels.
{json.dumps(QuestionAnswer.model_json_schema())}''')]


def add_quote_citations(question,result,llm, *, review_witnesses=None):
    return preserve_answer(result,'quote_attribution',lambda:_add_quote_citations(question,result,llm,review_witnesses=review_witnesses))


def _add_quote_citations(question,result,llm, *, review_witnesses=None):
    out=deepcopy(result);raw=result['raw'];witnesses=result['citation_sources']
    sentences=uncited_sentences(raw)
    if not sentences or not witnesses:return out
    witnesses = deepcopy(witnesses) + deepcopy(review_witnesses or [])
    messages = quote_messages(question,raw,witnesses,sentences)
    if review_witnesses:
        numbers = list(range(len(result['citation_sources'])+1,len(witnesses)+1))
        messages[0].content += (' Sources '+str(numbers)+' are rendered review-state snapshots, not original reports. '
            'Use them only for approval, pending, rejection, or preservation claims about their exact proposal. '
            'Document facts still require original document sources. A pending snapshot is not an approval event. '
            'Quote enough to identify the same proposal and assertion; do not attach an unrelated review.')
    response=llm.chat(messages).message.content
    operations=[];reviews=[];error=None
    try:
        payload=re.sub(r'^```(?:json)?\s*|\s*```$','',response.strip())
        parsed=QuestionAnswer.model_validate_json(payload)
        facts={item.fact:item for item in parsed.answer}
        if len(facts)!=len(parsed.answer) or set(facts)!={s['sentence'] for s in sentences}:
            raise ValueError('Fact list differs from requested unchanged sentences')
        for s in sentences:
            evidence=[]
            for quote in facts[s['sentence']].substring_quote:
                if not quote.strip():continue
                event_matches = [w for w in (review_witnesses or []) if quote_span(quote,w['quote']) is not None]
                for number,w in enumerate(witnesses,1):
                    # A generic status phrase shared by several proposals cannot
                    # identify which review supports the claim.
                    if w.get('evidence_type') == 'review_state' and len(event_matches) != 1:
                        continue
                    span=quote_span(quote,w['quote'])
                    if span is not None:
                        start,end=span
                        evidence.append(dict(number=number,proposed_quote=quote,
                            quote=w['quote'][start:end],start=start,end=end))
            reviews.append(dict(**s,proposed_quotes=facts[s['sentence']].substring_quote,evidence=evidence))
            # Multiple sources may jointly support one fact. No model-supplied IDs
            # are trusted: source numbers are resolved by literal quote matching.
            for number in sorted({e['number'] for e in evidence}):
                operations.append(dict(**s,number=number))
    except (ValueError,TypeError) as exc:
        error=type(exc).__name__+': '+str(exc)
    new_raw=raw
    for op in reversed(operations):
        new_raw=new_raw[:op['start']]+f"[{op['number']}] "+new_raw[op['start']:]
    out.update(format_response(question,new_raw,witnesses,allow_source_labels=True))
    covered={op['start'] for op in operations}
    out.update(pre_citation_raw=raw,posthoc_citations=operations,
        citation_method='LangChain FactWithEvidence exact-quote attribution; full answer context; additive, no overwrite',
        quote_attribution_raw=response,quote_citation_reviews=reviews,
        quote_attribution_error=error,citation_entailment_verified=False,
        unattributed_sentences=[s for s in sentences if s['start'] not in covered],
        attribution_status='partial' if any(s['start'] not in covered for s in sentences) else 'complete')
    if result['status']=='partial':
        out['status']='partial';out['warnings']=list(dict.fromkeys(result['warnings']+out['warnings']))
    out=carry_diagnostics(result,out)
    if error:
        out=stage_failure(out,'quote_attribution','InvalidStructuredOutput')
    elif out['unattributed_sentences']:
        out=stage_failure(out,'quote_attribution','IncompleteAttribution')
    return out
