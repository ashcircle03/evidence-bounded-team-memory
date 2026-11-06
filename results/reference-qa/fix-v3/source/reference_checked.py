"""Reference R-RAG pattern: draft, upstream document judgment, bounded revision.

The document judge is Microsoft's unmodified MIT implementation, pinned in
_vendor/conflictscore. Whole-answer checking follows the upstream direct variant;
this is not a reproduction of the full claim-decomposition metric or paper score.
"""
from concurrent.futures import ThreadPoolExecutor
import json
from types import SimpleNamespace

from llama_index.core.llms import ChatMessage
from llama_index.core import PromptTemplate
from llama_index.core.query_engine.citation_query_engine import CITATION_QA_TEMPLATE, CITATION_REFINE_TEMPLATE
from ._vendor.conflictscore.eval_all_calibration import evaluate_document_support
from .reference_qa import ReferenceQA, format_response
from .reference_prompts import RECORD_QA_CONTRACT


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
                try:
                    obj = json.loads(raw.strip().removeprefix('```json').removesuffix('```').strip())
                    label = obj['answer'].upper()
                    if label not in ('SUPPORTS','CONTRADICTS','IRRELEVANT'):
                        raise ValueError('Invalid judge label')
                except (ValueError, KeyError, TypeError):
                    label = 'ERROR'  # Do not turn parser failures into irrelevance.
                return dict(source_id=sid,citation_numbers=g['numbers'],label=label,raw=raw)

            # Parallel I/O to the same local GPU service. The paper's per-document
            # judgment is unchanged; grouping respects the original document IDs.
            with ThreadPoolExecutor(max_workers=4) as pool:
                judgments = list(pool.map(judge, grouped.items()))
            contradicted = [j for j in judgments if j['label']=='CONTRADICTS']
            result = draft
            if contradicted:
                sources = '\n\n'.join(part for g in grouped.values() for part in g['parts'])
                feedback = json.dumps(judgments, ensure_ascii=False)
                # R-RAG's evidence feedback pattern; its binary answer contract is
                # replaced by the user's record-preservation QA contract.
                messages = [ChatMessage(role='system',content=RECORD_QA_CONTRACT+
                    '\nUse [N] for every claim to cite the provided Source N. Return only the concise answer.'),
                    ChatMessage(role='user',content=f'''Re-examine the original sources and revise the draft in light of the document judgments. The judgments can be wrong; the source text is the evidence.
QUESTION: {question}
ORIGINAL SOURCES:
{sources}
DRAFT ANSWER:
{draft['raw']}
DOCUMENT JUDGMENTS:
{feedback}
Preserve all different answers actually stated for the question with their own citations. Do not invent an unrecorded difference in conditions or choose an authoritative winner. If a judgment concerns a different condition or an unrelated attribute, retain the supported answer and state only the relevant conditions.''')]
                response = self.llm.chat(messages)
                result = format_response(question, response.message.content, witnesses, allow_source_labels=True)
            result['draft_raw'] = draft['raw']
            result['document_judgments'] = judgments
            result['revised'] = bool(contradicted)
            if any(j['label']=='ERROR' for j in judgments):
                result['warnings'].append('Conflict review incomplete: document judge parse or transport failure')
                result['status'] = 'partial'
            return result
