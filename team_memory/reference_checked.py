"""Reference R-RAG pattern: draft, upstream document judgment, bounded revision.

The document judge is Microsoft's unmodified MIT implementation, pinned in
_vendor/conflictscore. Whole-answer checking follows the upstream direct variant;
this is not a reproduction of the full claim-decomposition metric or paper score.
"""
from concurrent.futures import ThreadPoolExecutor
import json
import re
from types import SimpleNamespace

from llama_index.core.llms import ChatMessage
from llama_index.core import PromptTemplate
from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.core.response_synthesizers.accumulate import Accumulate
from llama_index.core.query_engine.citation_query_engine import CITATION_QA_TEMPLATE, CITATION_REFINE_TEMPLATE
from ._vendor.conflictscore.eval_all_calibration import evaluate_document_support
from .reference_qa import ReferenceQA, format_response
from .reference_prompts import RECORD_QA_CONTRACT


def parse_judgment(raw):
    """Use the upstream JSON -> explicit label -> XML fallback, not strict JSON alone.

    Adapted from eval_all_calibration.py's main-loop parsing under its MIT license.
    The only error-policy change is ERROR, rather than IRRELEVANT, when no valid
    label can be recovered. No label is inferred from the explanation prose.
    """
    label = None
    try:
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw, re.DOTALL)
        if match:
            obj = json.loads(match.group(0))
            label = obj.get('answer', obj.get('support'))
    except (ValueError, KeyError, TypeError):
        pass
    if label is None:
        for field in ('answer','support'):
            match = re.search(r'"'+field+r'":\s*"([^"]+)"',raw,re.DOTALL|re.IGNORECASE)
            if match:
                label = match.group(1);break
    if label is None:
        match = re.search(r'<answer>(.*?)</answer>',raw,re.DOTALL)
        if match:label = match.group(1)
    label = label.strip().upper() if isinstance(label,str) else 'ERROR'
    return label if label in ('SUPPORTS','CONTRADICTS','IRRELEVANT') else 'ERROR'


def review_messages(question, draft_raw, witnesses, judgments):
    """The same source-record revision contract for live and exact-output replay."""
    grouped = {}
    for number,w in enumerate(witnesses,1):
        grouped.setdefault(w['source_id'],[]).append(
            f"Source {number}:\nrecord_author: {w['speaker']}\n{w['quote']}")
    sources = '\n\n'.join(part for parts in grouped.values() for part in parts)
    feedback = json.dumps(judgments,ensure_ascii=False)
    return [ChatMessage(role='system',content=RECORD_QA_CONTRACT+
        '\nUse [N] for every claim to cite the provided Source N. Return only the concise answer.'),
        ChatMessage(role='user',content=f'''Re-examine the original sources and revise the draft in light of the document judgments. The judgments can be wrong; the source text is the evidence.
QUESTION: {question}
ORIGINAL SOURCES:
{sources}
DRAFT ANSWER:
{draft_raw}
DOCUMENT JUDGMENTS:
{feedback}
Preserve all different answers actually stated for the question with their own citations. Do not invent an unrecorded difference in conditions or choose an authoritative winner. If a judgment concerns a different condition or an unrelated attribute, retain the supported answer and state only the relevant conditions.''')]


class _TracedAccumulate(Accumulate):
    """Capture exact constituent outputs; generation/concatenation remain upstream."""
    def _format_response(self, outputs, separator):
        self.segments = list(outputs)
        return super()._format_response(outputs,separator)


def missing_opposing_sources(result):
    cited = {w['source_id'] for a in result.get('answers',[]) for w in a['evidence']}
    return [j['source_id'] for j in result.get('document_judgments',[])
            if j['label']=='CONTRADICTS' and j['source_id'] not in cited]


def accumulate_omitted_records(question, result, llm, tokenizer):
    """Rejected experimental fallback; retained for exact result reproduction.

    Per-document QA recovers an omitted opposing record but also invents answers
    from irrelevant records. It is deliberately not called by ConflictCheckedQA.
    """
    missing = missing_opposing_sources(result)
    if not missing:return result
    witnesses=result['citation_sources'];documents=[]
    for j in result['document_judgments']:
        if j['label'] not in ('SUPPORTS','CONTRADICTS'):continue
        documents.append('\n\n'.join(
            f"Source {i}:\nrecord_author: {witnesses[i-1]['speaker']}\n{witnesses[i-1]['quote']}"
            for i in j['citation_numbers']))
    helper=PromptHelper(context_window=llm.metadata.context_window-256,
        num_output=llm.metadata.num_output,tokenizer=lambda t:tokenizer.encode(t,add_special_tokens=False))
    synth=_TracedAccumulate(llm=llm,prompt_helper=helper,text_qa_template=CITATION_QA_TEMPLATE,use_async=False)
    raw=synth.get_response(query_str=question,text_chunks=documents)
    accumulated=format_response(question,raw,witnesses,allow_source_labels=True)
    for key in ('draft_raw','document_judgments','revised'):
        accumulated[key]=result[key]
    accumulated.update(revised_raw=result['raw'],generation_kind='llama-index-accumulate',
        generation_segments=synth.segments,missing_opposing_sources_before=missing)
    if any(j['label']=='ERROR' for j in result['document_judgments']):
        accumulated['status']='partial'
        accumulated['warnings'].append('Conflict review incomplete: document judge parse or transport failure')
    return accumulated


class _LocalJudgeClient:
    """Adapt the upstream OpenAI call to the existing traced, loopback-only LLM."""
    def __init__(self, llm):
        self.llm = llm
        self.chat = self.completions = self

    def create(self, *, messages, **unused):
        # Bounded local-model substitution; no provider discovery or paid fallback.
        response = self.llm.chat([ChatMessage(**m) for m in messages], max_tokens=384)
        return SimpleNamespace(choices=[SimpleNamespace(message=response.message)])


class ConflictCheckedQA(ReferenceQA):
    def __init__(self, store, **kwargs):
        super().__init__(store, profile='team', **kwargs)

    def _team_templates(self):
        # R-RAG begins with an ordinary draft, then checks it. Hedging the draft
        # before the upstream partial-support judge can conceal its disagreement.
        author = 'The record_author metadata identifies who wrote a record; @mentions are recipients or references.\n'
        return tuple(PromptTemplate(author+t.template) for t in (CITATION_QA_TEMPLATE,CITATION_REFINE_TEMPLATE))

    def ask(self, question):
        with self.lock:
            draft = super().ask(question)
            witnesses = draft['citation_sources']
            if not witnesses:
                return draft
            grouped = {}
            for number,w in enumerate(witnesses,1):
                group = grouped.setdefault(w['source_id'], dict(numbers=[],parts=[],speaker=w['speaker']))
                group['numbers'].append(number)
                group['parts'].append(f"Source {number}:\nrecord_author: {w['speaker']}\n{w['quote']}")
            client = _LocalJudgeClient(self.llm)

            def judge(item):
                sid,g = item
                raw = evaluate_document_support(client, '\n\n'.join(g['parts']), draft['raw'],
                                                question, 'Qwen3-8B')
                label = parse_judgment(raw)
                return dict(source_id=sid,citation_numbers=g['numbers'],label=label,raw=raw)

            # Parallel I/O to the same local GPU service. The paper's per-document
            # judgment is unchanged; grouping respects the original document IDs.
            with ThreadPoolExecutor(max_workers=4) as pool:
                judgments = list(pool.map(judge, grouped.items()))
            contradicted = [j for j in judgments if j['label']=='CONTRADICTS']
            result = draft
            if contradicted:
                # R-RAG's evidence feedback pattern; its binary answer contract is
                # replaced by the user's record-preservation QA contract.
                messages = review_messages(question,draft['raw'],witnesses,judgments)
                response = self.llm.chat(messages)
                result = format_response(question, response.message.content, witnesses, allow_source_labels=True)
            result['draft_raw'] = draft['raw']
            result['document_judgments'] = judgments
            result['revised'] = bool(contradicted)
            if any(j['label']=='ERROR' for j in judgments):
                result['warnings'].append('Conflict review incomplete: document judge parse or transport failure')
                result['status'] = 'partial'
            # The evaluated Accumulate alternative regressed ordinary QA. Keep
            # the measured19/20 path; preserve the alternative only for replay.
            return result
