"""Attribute-first content selection -> evidence-linked claim generation.

Adapt the published two-stage Attribute First pipeline and LangChain Citation
schema. No whole-answer document judge, rewrite loop, or post-hoc citation pass.
"""
from copy import deepcopy
import json
from pathlib import Path
from pydantic import BaseModel, Field
from llama_index.core import PromptTemplate
from llama_index.core.llms import ChatMessage
from team_memory.readers.retrieval import ReferenceQA
from team_memory.experiments.readers.format import locate_quote, parse_model_json
from team_memory.readers.fallback import stage_failure
from team_memory._vendor.langchain_citation.quoted_answer import Citation


class Selection(BaseModel):
    segments: list[Citation] = Field(description='Separate verbatim supporting spans, including different relevant claims within the same source. Empty only when no source is relevant.')


class Claim(BaseModel):
    text: str = Field(min_length=1, description='One factual assertion or one condition-outcome pair, answering the question.')
    evidence: list[int] = Field(min_length=1, description='Displayed Evidence IDs that jointly support this entire claim, including conditions and attribution.')


class ClaimAnswer(BaseModel):
    claims: list[Claim]


_UPSTREAM=json.loads((Path(__file__).parents[2]/'_vendor/attribute_first/prompts.json').read_text())
SELECT=_UPSTREAM['instruction-content-selection'].split('IMPORTANT:')[0].replace(
    'and use <SPAN_DELIM> as a delimiter between each consecutive span.',
    'and keep each span as a separate item.')+'''
Keep every distinct source answer relevant to the question, including conflicting
passages inside one source. Include the subject, action and its conditions, not
just an isolated value. A condition and its effect may require different spans.
Unrelated statements are not alternative answers. record_author is provenance;
@mentions in the text are recipients. Copy source text exactly, including code
punctuation. Return JSON using displayed integer Source numbers. Do not answer
the question yet. Do not infer approval or a winner from dates or source titles.
'''
FUSE='''Answer the question from the selected evidence and its source metadata.
Following Attribute First's fusion-in-context step, cover all and only the
selected evidence. Group evidence that jointly supports ONE claim and produce
that claim with its Evidence IDs. Each output item is one factual assertion or
one condition-outcome pair. Retain the subject and conditions. Keep incompatible
source answers separately attributed; do not resolve them with prior knowledge.
Different conditions can coexist. Do not make unrelated records alternatives.
Respect explicit corrections and scope exceptions when the question asks for
the applicable current rule. Recording time alone is not a correction event.
For authorship use record_author, never an @mention. Several Evidence IDs may
belong to one original source: preserve their distinct claims. Cite every span
needed to support the whole claim. Do not invent evidence IDs or extra facts.
Return only the typed JSON answer; empty claims means insufficient evidence.
'''


def selection_template():
    prefix=(SELECT+json.dumps(Selection.model_json_schema())).replace('{','{{').replace('}','}}')
    return PromptTemplate(prefix+'\nSOURCES:\n{context_str}\nQUESTION: {query_str}\nJSON:')


def bind_selection(raw, witnesses):
    selected=parse_model_json(Selection,raw);units=[];issues=[];seen=set()
    for item in selected.segments:
        n=item.source_id
        if not 1<=n<=len(witnesses):
            issues.append('out_of_range_source');continue
        source=witnesses[n-1];span=locate_quote(item.quote,source)
        if span is None:
            issues.append('quote_not_located');continue
        a,b=span;key=(source['source_id'],source['start']+a,source['start']+b)
        if key in seen:continue
        seen.add(key)
        unit=dict(source_id=source['source_id'],speaker=source['speaker'],location=source['location'],
            start=key[1],end=key[2],quote=source['quote'][a:b],retrieval_number=n)
        if 'observed_at' in source:unit['observed_at']=source['observed_at']
        units.append(unit)
    return units,list(dict.fromkeys(issues))


def finish_claims(question, selection_raw, witnesses, llm):
    out=dict(status='insufficient',profile='claims',raw='',answers=[],claims=[],
        retrieval_sources=deepcopy(witnesses),citation_sources=[],selection_raw=selection_raw,
        generation_raw=None,warnings=[],verification='Literal source binding and selected-evidence coverage only; semantic entailment is not certified')
    try:
        units,issues=bind_selection(selection_raw,witnesses)
    except (ValueError,TypeError) as exc:
        return stage_failure(out,'evidence_selection',type(exc).__name__)
    out['citation_sources']=units;out['warnings']=issues
    if not units:
        return stage_failure(out,'evidence_selection','NoLocatedEvidence') if issues else out
    context=[dict(evidence_id=i,record_author=w['speaker'],original_source_number=w['retrieval_number'],
                  recorded_at=w.get('observed_at'),quote=w['quote']) for i,w in enumerate(units,1)]
    try:
        raw=llm.chat([ChatMessage(role='user',content=FUSE+'\nQUESTION: '+question+
            '\nEVIDENCE: '+json.dumps(context,ensure_ascii=False)+'\nSCHEMA: '+json.dumps(ClaimAnswer.model_json_schema()))]).message.content
        out['generation_raw']=raw;parsed=parse_model_json(ClaimAnswer,raw)
    except Exception as exc:
        return stage_failure(out,'claim_generation',type(exc).__name__)
    used=set()
    for c in parsed.claims:
        ids=list(dict.fromkeys(c.evidence))
        if any(n<1 or n>len(units) for n in ids):
            out=stage_failure(out,'claim_binding','UnknownEvidenceID');continue
        evidence=[deepcopy(units[n-1]) for n in ids]
        # The same evidence objects belong to the claim, API answer and citation.
        out['claims'].append(dict(text=c.text,evidence_ids=ids,evidence=evidence))
        out['answers'].append(dict(text=c.text+' '+''.join(f'[{n}]' for n in ids),evidence=evidence))
        used.update(ids)
    out['raw']='\n\n'.join(a['text'] for a in out['answers'])
    out['cited_numbers']=sorted(used)
    out['unclaimed_evidence_ids']=sorted(set(range(1,len(units)+1))-used)
    if out['answers'] and not out.get('stage_failures'):out['status']='ok'
    if issues:out=stage_failure(out,'evidence_selection','UnboundSpans')
    if out['unclaimed_evidence_ids']:out=stage_failure(out,'claim_coverage','UnusedSelectedEvidence')
    out['alce']=dict(question=question,output=out['raw'],docs=[dict(title=w['location'],text=w['quote']) for w in units])
    return out


def answer_from_sources(question,witnesses,llm):
    context='\n\n'.join(f"Source {i}:\nrecord_author: {w['speaker']}\nrecorded_at: {w.get('observed_at','unknown')}\n{w['quote']}" for i,w in enumerate(witnesses,1))
    selection=llm.chat([ChatMessage(role='user',content=selection_template().format(context_str=context,query_str=question))]).message.content
    return finish_claims(question,selection,witnesses,llm)


class ClaimEvidenceQA(ReferenceQA):
    def __init__(self,store,**kwargs):
        super().__init__(store,profile='team',**kwargs)

    @staticmethod
    def _witness(node,sources,number):
        w=ReferenceQA._witness(node,sources,number)
        w['observed_at']=sources[w['source_id']]['observed_at']
        return w

    def _team_templates(self):
        # Existing LlamaIndex tokenizer-aware compact/refine context packing.
        refine=(SELECT+json.dumps(Selection.model_json_schema())).replace('{','{{').replace('}','}}')
        return selection_template(),PromptTemplate(refine+'\nQUESTION: {query_str}\nPRIOR SELECTION: {existing_answer}\nMORE SOURCES: {context_msg}\nReturn combined selection JSON:')

    def _format_response(self,question,raw,witnesses):
        return finish_claims(question,raw,witnesses,self.llm)
