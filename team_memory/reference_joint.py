"""One-pass source-specific QA: AQA intent + LangChain QuotedAnswer schema.

Reuse the existing LlamaIndex retrieval and citation source construction. Each
answer owns its citations; source-ID coverage is never called claim coverage.
"""
import json
from copy import deepcopy
from pydantic import BaseModel, Field
from llama_index.core import PromptTemplate
from .reference_qa import ReferenceQA
from .reference_format import locate_quote, parse_model_json
from ._vendor.langchain_citation.quoted_answer import QuotedAnswer


class SourceAnswers(BaseModel):
    answers: list[QuotedAnswer] = Field(description='Distinct source-specific answers; include conditions and author in each answer when relevant. Empty if no source answers the question.')


INSTRUCTIONS='''Answer using only the supplied records and their source metadata.
The record_author is the author; @mentions are not authors.
Preserve distinct answers that the records actually give to this question. Keep their stated conditions and attribution. Unrelated attributes are not alternative answers. Do not invent conditions to reconcile disagreements or infer approval/correction from recency alone. Conflicting passages may appear within one Source.
Example: Record A says Barack Obama is the serving president; Record B says Joseph Robinette Biden Jr. is the serving president. The answer must preserve both record-specific names with their own evidence.
Return concise JSON matching the schema. Each answer has its own citations. source_id is the displayed integer Source number. quote is a verbatim supporting passage from that source. Include enough context to retain subject and conditions. Never cite the example.
'''


def joint_template():
    instructions=(INSTRUCTIONS+json.dumps(SourceAnswers.model_json_schema())).replace('{','{{').replace('}','}}')
    return PromptTemplate(instructions+'\n\nSOURCES:\n{context_str}\nQUESTION: {query_str}\nJSON:')


def format_joint(question,raw,witnesses):
    """Bind generated claims to original source objects; quote diagnostics separate.

    As in LangChain's source-ID citation variant, a valid selected ID returns the
    original passage. Quote mismatch is explicit, never silently fabricated or
    treated as proof that the answer is false. Semantic support needs evaluation.
    """
    out=dict(status='partial',raw='',generation_raw=raw,answers=[],claims=[],citation_sources=witnesses,
        cited_numbers=[],warnings=[],verification='Original source identities and offsets only; semantic support is not certified',
        profile='joint',generation_kind='structured-source-answers')
    try:
        parsed=parse_model_json(SourceAnswers,raw)
    except (ValueError,TypeError) as exc:
        out.update(status='error',error_type=type(exc).__name__,warnings=['Structured answer could not be parsed'])
        return out
    for item in parsed.answers:
        evidence=[];spans=[];numbers=[];issues=[]
        for citation in item.citations:
            n=citation.source_id
            if not 1<=n<=len(witnesses):
                issues.append('out_of_range_source');continue
            w=witnesses[n-1]
            if n not in numbers:numbers.append(n);evidence.append(deepcopy(w))
            match=locate_quote(citation.quote,w)
            if match:
                a,b=match
                spans.append(dict(source_number=n,source_id=w['source_id'],quote=w['quote'][a:b],
                    start=w['start']+a,end=w['start']+b))
            else:issues.append('quote_not_located')
        rendered=item.answer+(' '+''.join(f'[{n}]' for n in numbers) if numbers else '')
        out['claims'].append(dict(text=item.answer,source_numbers=numbers,quoted_spans=spans,
            proposed_citations=[c.model_dump() for c in item.citations],diagnostics=issues))
        out['answers'].append(dict(text=rendered,evidence=evidence))
        out['warnings'].extend(issues or ([] if numbers else ['answer_without_source']))
    out['raw']='\n\n'.join(a['text'] for a in out['answers'])
    out['cited_numbers']=sorted({n for c in out['claims'] for n in c['source_numbers']})
    out['status']='insufficient' if not parsed.answers else ('partial' if out['warnings'] else 'ok')
    out['warnings']=list(dict.fromkeys(out['warnings']))
    out['alce']=dict(question=question,output=out['raw'],docs=[dict(title=w['location'],text=w['quote']) for w in witnesses])
    return out


class JointSourceQA(ReferenceQA):
    def __init__(self,store,**kwargs):
        super().__init__(store,profile='team',**kwargs)

    def _team_templates(self):
        # Same upstream compact synthesizer. Contexts used here fit one request;
        # do not promise one request when future inputs require refinement.
        return joint_template(),PromptTemplate(INSTRUCTIONS+'\nQUESTION: {query_str}\nPRIOR JSON: {existing_answer}\nADDITIONAL SOURCES: {context_msg}\nUpdate JSON without losing supported answers:')

    def _format_response(self,question,raw,witnesses):
        return format_joint(question,raw,witnesses)
