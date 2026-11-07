"""Attribute First fusion in enclosing source context, with explicit provenance.

The selected highlights guide generation but do not replace the enclosing
record. Final citations use LangChain's QuotedAnswer schema and source binding.
"""
from copy import deepcopy
import json

from llama_index.core.llms import ChatMessage

from .reference_claims import Selection, selection_template
from .reference_format import locate_quote, parse_model_json
from .reference_joint import SourceAnswers, format_joint
from .reference_qa import ReferenceQA


FUSION = '''Answer the question using the highlighted source records below.
Following Attribute First's fusion-in-context approach, use the highlights to
locate relevant information, and read their enclosing records to preserve the
subject, action, conditions and references. Highlights are fallible selections,
not new facts. Reject a highlight if its record does not answer the question.
record_author and recorded_at belong to the original record. @mentions identify
recipients, not authors. Preserve those metadata when identifying people or
resolving relative dates. Recording time is not necessarily event time.
For a time interval, identify both events and their dates from the records and
state the counting convention. Do not substitute an unrelated person's event.
For a conditional rule, retain both its applicability and effect. Distinguish
an explicit exception or correction from mere recency. Different conditions can
coexist; unresolved incompatible answers need separately attributed citations.
Return concise JSON using the supplied schema. Each answer must have its own
verbatim citations from the enclosing source text. Include the clause that
identifies the subject and condition, not just the answer value. Displayed
source_id numbers refer to the displayed source table. Empty answers means that
the records do not supply the required information. Do not invent missing dates,
actions, approval or source text. For multiple choice, begin with the option
letter and justify it using the records.
'''


def source_context(witnesses):
    return '\n\n'.join(
        f"Source {i}:\nrecord_author: {w['speaker']}\n"
        f"recorded_at: {w.get('observed_at', 'unknown')}\n{w['quote']}"
        for i, w in enumerate(witnesses, 1)
    )


def answer_from_sources(question, witnesses, llm):
    """Two model calls; the same source objects survive selection and fusion."""
    selection_raw = llm.chat([ChatMessage(role='user', content=selection_template().format(
        context_str=source_context(witnesses), query_str=question))]).message.content
    try:
        selection = parse_model_json(Selection, selection_raw)
    except (ValueError, TypeError) as error:
        return dict(status='error', profile='contextual', answers=[], claims=[],
                    selection_raw=selection_raw, error_type=type(error).__name__,
                    warnings=['Evidence selection could not be parsed'],
                    retrieval_sources=deepcopy(witnesses))

    records, issues = {}, []
    for segment in selection.segments:
        number = segment.source_id
        if not 1 <= number <= len(witnesses):
            issues.append('out_of_range_selection_source')
            continue
        witness = witnesses[number - 1]
        record = records.setdefault(number, dict(
            source_id=number, record_author=witness['speaker'],
            recorded_at=witness.get('observed_at'),
            source_text=witness['quote'], highlights=[]))
        span = locate_quote(segment.quote, witness)
        if span is None:
            # A valid source ID can still be read. Never label the proposed
            # altered quote as verified, or attach it as the final evidence.
            issues.append('selection_quote_not_located')
        else:
            start, end = span
            record['highlights'].append(dict(start=start, end=end,
                                             text=witness['quote'][start:end]))

    if not records:
        return dict(status='partial' if issues else 'insufficient', profile='contextual',
                    answers=[], claims=[], selection_raw=selection_raw,
                    warnings=issues, retrieval_sources=deepcopy(witnesses))
    visible_sources = [witnesses[number-1] for number in records]
    visible_records = [dict(record, source_id=i, retrieval_source_number=number)
                       for i, (number, record) in enumerate(records.items(), 1)]
    prompt = (FUSION + '\nQUESTION: ' + question + '\nSOURCE RECORDS: ' +
              json.dumps(visible_records, ensure_ascii=False) +
              '\nSCHEMA: ' + json.dumps(SourceAnswers.model_json_schema()))
    raw = llm.chat([ChatMessage(role='user', content=prompt)]).message.content
    result = format_joint(question, raw, visible_sources)
    result.update(profile='contextual', selection_raw=selection_raw,
                  selection_records=visible_records,
                  selection_warnings=sorted(set(issues)),
                  retrieval_sources=deepcopy(witnesses))
    for claim, answer in zip(result['claims'], result['answers']):
        claim['evidence'] = deepcopy(answer['evidence'])
    if issues and result['status'] == 'ok':
        result['status'] = 'partial'
    return result


class ContextualQA(ReferenceQA):
    """Optional source-QA profile using feedback retrieval and contextual fusion."""
    def __init__(self, store, **kwargs):
        super().__init__(store, profile='team', **kwargs)
        self.feedback_index_key = None

    def ask(self, question):
        from .reference_retrieval import FeedbackRetriever
        if not isinstance(question, str) or not question.strip():
            raise ValueError('Nonempty question required')
        with self.lock:
            sources = self.store.load('sources')
            if not sources:
                return dict(status='insufficient', answers=[], claims=[])
            key = tuple(sorted(sources))
            if key != self.feedback_index_key:
                witnesses = [dict(source_id=sid, quote=record['source']['text'],
                    start=0, end=len(record['source']['text']),
                    location=record['source']['location'], speaker=record['source']['speaker'],
                    observed_at=record['observed_at']) for sid, record in sorted(sources.items())]
                self.feedback_retriever = FeedbackRetriever(witnesses, self.tokenizer,
                                                           self.llm, top_k=2*self.top_k)
                self.feedback_index_key = key
            retrieved = self.feedback_retriever.retrieve(question)
            result = answer_from_sources(question, retrieved['sources'], self.llm)
            result['retrieval_trace'] = retrieved['trace']
            return result
