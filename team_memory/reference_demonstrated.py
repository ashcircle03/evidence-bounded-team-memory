"""Attribute First demonstrations and explicit span-to-sentence alignment.

Adaptation, not a paper reproduction: Qwen, structured transport, metadata and
bounded follow-up retrieval. Author examples are independent of evaluation.
"""
from copy import deepcopy
from functools import lru_cache
import json
from pathlib import Path
import re
from pydantic import BaseModel, Field
from llama_index.core.llms import ChatMessage
from ._vendor.langchain_citation.quoted_answer import Citation
from .reference_connected import source_table, append_sources, ConnectedQA
from .reference_format import locate_quote, parse_model_json
from .reference_joint import SourceAnswers, format_joint


class Selection(BaseModel):
    highlights: list[Citation]
    missing_queries: list[str] = Field(max_length=2)


class Sentence(BaseModel):
    answer: str
    highlight_ids: list[int] = Field(min_length=1)


class AlignedAnswers(BaseModel):
    sentences: list[Sentence]


SELECT = '''Select consecutive VERBATIM source spans needed to answer the question.
Include all relevant alternative answers and every premise of multi-source answers.
Retain each span's subject and condition. Do not interpret, paraphrase or decide
between conflicting sources during selection. record_author is the author;
@mentions are recipients. recorded_at is recording time, not necessarily event time.
If evidence needed by the question is absent, return at most two targeted search
queries for the missing evidence, retaining the question's person/project/event.
Otherwise return missing_queries=[]. Source IDs refer only to this instance.
Examples demonstrate selection and output structure, not facts for the test case.
Return JSON matching the schema. The question's answer format applies at generation.
'''

GENERATE = '''Answer the question using the source records and numbered highlights.
Follow the examples' explicit highlight-to-answer correspondence. Each sentence
must name its supporting highlight IDs; several highlights may jointly support
one sentence. Preserve ALL source-specific incompatible answers and their stated
conditions. Different people/events must not be merged. Recency is not approval.
record_author is the author; @mentions are recipients. Interpret relative dates
using recorded_at without treating recording time as event time. For durations,
use the same person's requested events and state the counting convention.
Use the original records to understand context; cite only the numbered highlights.
Never cite examples or search queries. If no complete answer is supported, return
sentences=[]. For multiple choice, begin the answer with the option letter.
Return only JSON matching the schema. Do not add a separate final-answer copy.
'''

DIRECT = GENERATE.replace('and numbered highlights', '').replace(
    "Follow the examples' explicit highlight-to-answer correspondence. Each sentence\n"
    'must name its supporting highlight IDs; several highlights may jointly support\n'
    'one sentence.', 'Each answer owns its verbatim source citations. Several sources may jointly support one answer.').replace(
    'Use the original records to understand context; cite only the numbered highlights.',
    'Include subject and conditions in each verbatim citation.').replace('sentences=[]', 'answers=[]')


@lru_cache(maxsize=1)
def demonstrations():
    """Deterministic first two original LFQA demos, plus AQA Figure1 adaptation.

    Preserve author's full documents, selected spans and output sentences. Only
    serialization changes. No evaluation question, answer or result is accessed.
    """
    data = json.loads((Path(__file__).parent/'_vendor/attribute_first/LFQA.original.json').read_text())
    examples = []
    for item in data['demos'][:2]:
        sources, highlights = [], []
        for n, doc in enumerate(item['docs'], 1):
            sources.append(dict(source_id=n, record_author=None, recorded_at=None,
                text=doc['text'].replace('{HS}', '').replace('{HE}', '')))
            highlights.extend(dict(source_id=n, quote=s) for s in re.findall(
                r'\{HS\}(.*?)\{HE\}', doc['text'], re.S))
        sentences = [dict(answer=p['output'], highlight_ids=sorted({h for c in p['highlights_cluster']
                     for h in c['highlights']})) for p in item['planning']]
        examples.append(dict(question=item['question'], sources=sources,
            selection=dict(highlights=highlights, missing_queries=[]), sentences=sentences))
    # Existing AQA paper Figure1 paraphrase, NOT unavailable author 3-shot data.
    sources = [dict(source_id=1, record_author=None, recorded_at=None,
                    text='Record A identifies Barack Obama as the serving president.'),
               dict(source_id=2, record_author=None, recorded_at=None,
                    text='Record B identifies Joseph Robinette Biden Jr. as the serving president.')]
    examples.append(dict(question='Who is the serving president according to these records?',
        sources=sources, selection=dict(highlights=[dict(source_id=s['source_id'], quote=s['text'])
            for s in sources], missing_queries=[]), sentences=[
            dict(answer='Record A identifies Barack Obama as the serving president.', highlight_ids=[1]),
            dict(answer='Record B identifies Joseph Robinette Biden Jr. as the serving president.', highlight_ids=[2])]))
    for example in examples:
        for span in example['selection']['highlights']:
            assert span['quote'] in example['sources'][span['source_id']-1]['text']
        for sentence in example['sentences']:
            assert all(1 <= i <= len(example['selection']['highlights']) for i in sentence['highlight_ids'])
    return examples


def numbered(highlights):
    return [dict(highlight_id=i, **h) for i,h in enumerate(highlights, 1)]


def aligned_to_source(sentences, highlights):
    return dict(answers=[dict(answer=s['answer'], citations=[highlights[i-1]
        for i in dict.fromkeys(s['highlight_ids'])]) for s in sentences])


def request(llm, stage, payload):
    instruction, schema = {'select':(SELECT, Selection), 'generate':(GENERATE, AlignedAnswers),
                           'direct':(DIRECT, SourceAnswers)}[stage]
    messages = [ChatMessage(role='system', content=instruction+'\nSCHEMA: '+json.dumps(schema.model_json_schema()))]
    for demo in demonstrations():
        data = dict(question=demo['question'], sources=demo['sources'])
        if stage == 'select':
            output = demo['selection']
        elif stage == 'generate':
            data['highlights'] = numbered(demo['selection']['highlights'])
            output = dict(sentences=demo['sentences'])
        else:
            output = aligned_to_source(demo['sentences'], demo['selection']['highlights'])
        messages.extend([ChatMessage(role='user', content=json.dumps(data, ensure_ascii=False)),
                         ChatMessage(role='assistant', content=json.dumps(output, ensure_ascii=False))])
    messages.append(ChatMessage(role='user', content=json.dumps(payload, ensure_ascii=False)))
    return llm.chat(messages).message.content


def select(question, sources, llm):
    raw = request(llm, 'select', dict(question=question, sources=source_table(sources)))
    warnings, highlights = [], []
    try:
        parsed = parse_model_json(Selection, raw)
    except (ValueError, TypeError):
        return dict(raw=raw, highlights=[], missing_queries=[], warnings=['selection_parse_error'])
    for span in parsed.highlights:
        if not 1 <= span.source_id <= len(sources):
            warnings.append('selection_source_out_of_range')
        elif locate_quote(span.quote, sources[span.source_id-1]) is None:
            warnings.append('selection_quote_not_located')
        else:
            highlights.append(span.model_dump())
    return dict(raw=raw, highlights=highlights,
        missing_queries=list(dict.fromkeys(q.strip() for q in parsed.missing_queries if q.strip())),
        warnings=sorted(set(warnings)))


def generate(question, sources, selection, llm):
    raw = request(llm, 'generate', dict(question=question, sources=source_table(sources),
                                      highlights=numbered(selection['highlights'])))
    warnings = list(selection['warnings'])
    try:
        parsed = parse_model_json(AlignedAnswers, raw)
        sentences = []
        for sentence in parsed.sentences:
            if all(1 <= i <= len(selection['highlights']) for i in sentence.highlight_ids):
                sentences.append(sentence.model_dump())
            else:
                warnings.append('answer_highlight_out_of_range')
        transport = json.dumps(aligned_to_source(sentences, selection['highlights']), ensure_ascii=False)
        result = format_joint(question, transport, sources)
    except (ValueError, TypeError):
        result = format_joint(question, raw, sources)
        result.update(status='error', answers=[], claims=[], raw='', cited_numbers=[])
        warnings.append('aligned_answer_parse_error')
    result.update(profile='demonstrated', aligned_generation_raw=raw, selection=deepcopy(selection))
    result['warnings'] = sorted(set(result['warnings']+warnings))
    if warnings and result['status'] != 'error':
        result['status'] = 'partial'
    for claim, answer in zip(result['claims'], result['answers']):
        claim['evidence'] = deepcopy(answer['evidence'])
    return result


def direct(question, sources, llm):
    raw = request(llm, 'direct', dict(question=question, sources=source_table(sources)))
    return format_joint(question, raw, sources)


def retrieve(question, initial, selection, llm, search, max_rounds=2):
    """Re-read after new evidence; stop on no query, no new source, or two rounds.

    IRCoT-inspired accumulation only, not its last-sentence query algorithm.
    Search query never becomes evidence. Preserve original source order/IDs.
    """
    sources, trace, previous = deepcopy(initial), [], set()
    for _ in range(max_rounds):
        queries = [q for q in selection['missing_queries'] if q not in previous]
        if not queries:
            break
        previous.update(queries)
        batches = [dict(query=q, sources=search(q)[:4]) for q in queries]
        extra = [batch['sources'][i] for i in range(4) for batch in batches if i < len(batch['sources'])]
        expanded = append_sources(sources, extra, limit=8)
        if expanded == sources:
            trace.append(dict(selection=selection, searches=batches, added=0)); break
        trace.append(dict(selection=selection, searches=batches, added=len(expanded)-len(sources)))
        sources = expanded
        selection = select(question, sources, llm)
    return sources, selection, trace


def answer_from_sources(question, sources, llm, search=None):
    selection = select(question, sources, llm)
    expanded, trace = sources, []
    if search:
        expanded, selection, trace = retrieve(question, sources, selection, llm, search)
    result = generate(question, expanded, selection, llm)
    result.update(initial_sources=deepcopy(sources), retrieval_sources=deepcopy(expanded), retrieval_trace=trace)
    return result


class DemonstratedQA(ConnectedQA):
    """Same storage and BM25 adapter; new reader selected explicitly."""
    def ask(self, question):
        from .reference_retrieval import FeedbackRetriever
        if not isinstance(question, str) or not question.strip():
            raise ValueError('Nonempty question required')
        with self.lock:
            records = self.store.load('sources')
            if not records:
                return dict(status='insufficient', answers=[], claims=[])
            key = tuple(sorted(records))
            if key != self.feedback_index_key:
                witnesses = [dict(source_id=sid, quote=r['source']['text'], start=0,
                    end=len(r['source']['text']), location=r['source']['location'],
                    speaker=r['source']['speaker'], observed_at=r['observed_at'])
                    for sid,r in sorted(records.items())]
                self.feedback_retriever = FeedbackRetriever(witnesses, self.tokenizer, self.llm,
                                                            top_k=2*self.top_k)
                self.feedback_index_key = key
            retriever = self.feedback_retriever
            initial = retriever.witnesses(retriever.original.retrieve(question))
            return answer_from_sources(question, initial, self.llm,
                search=lambda query: retriever.witnesses(retriever.metadata.retrieve(query))[:4])
