"""Original-record QA: LongMemEval reading and ALCE document citations.

One generation call, no quote-copy or selection gate. See docs/reference-documents.md
for adaptations and the limits of document identity verification.
"""
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path

from llama_index.core.llms import ChatMessage
from pydantic import BaseModel, ConfigDict, Field, StrictInt

from team_memory.experiments.readers.format import parse_model_json


class DocumentAnswer(BaseModel):
    model_config = ConfigDict(extra='forbid')
    answer: str = Field(min_length=1, description='One factual answer sentence, retaining its applicable subject and conditions.')
    document_ids: list[StrictInt] = Field(description='Minimum sufficient subset of displayed Document IDs supporting this sentence.')


class DocumentAnswers(BaseModel):
    model_config = ConfigDict(extra='forbid')
    reasoning: str = Field(description='Brief evidence-based working notes when requested, otherwise empty.')
    answers: list[DocumentAnswer] = Field(description='Source-specific answer sentences; empty if the required information is absent.')


TEAM_CONTRACT = '''These are records from multiple people, not one user's biography.
record_author is the writer; @mentions are recipients, not writers. location is
the original record identifier, not an inferred project name. Keep groups and
people distinct. recorded_at is the recording time, not necessarily event time.
Use stated event dates and explicit conditions. Do not infer approval, a correction
or a replacement merely because a record is newer. When records give incompatible
answers, preserve both answers with their respective sources. Different applicable
conditions may coexist. If a required fact is absent, do not invent it.
Return JSON matching the schema. Use document_ids instead of inline brackets;
the client renders brackets from these IDs. Do not copy supporting quotes into
the output. Each answer sentence must cite its own supporting documents.
For multiple choice, include the selected option letter and its supported reason.
'''


def documents(witnesses):
    """Assign IDs BEFORE sorting; retain original offset and metadata bindings."""
    rows = []
    for number, w in enumerate(witnesses, 1):
        if not isinstance(w['start'], int) or w['start'] < 0 or w['end']-w['start'] != len(w['quote']):
            raise ValueError('Invalid original source span')
        stamp = w.get('observed_at')
        try:
            parsed = datetime.fromisoformat(stamp.replace('Z', '+00:00')) if stamp else None
        except (ValueError, TypeError, AttributeError):
            raise ValueError('Unparseable recorded_at; do not guess chronological order')
        # Dates with unknown zones retain their native wall-clock representation.
        # Do not invent a UTC zone to compare unrelated records.
        key = (parsed.astimezone(timezone.utc).isoformat() if parsed.tzinfo else parsed.isoformat()) if parsed else ''
        rows.append(dict(document_id=number, source_id=w['source_id'],
            record_author=w['speaker'], recorded_at=stamp, location=w['location'],
            start=w['start'], end=w['end'], text=w['quote'], _date_key=key,
            _zone='aware' if parsed and parsed.tzinfo else 'local' if parsed else 'missing'))
    # Mixed known/unknown time zones cannot establish a common chronology.
    # Preserve input order rather than silently treating unknown zones as UTC.
    if len({r['_zone'] for r in rows}) == 1:
        rows.sort(key=lambda r: (r['_date_key'], r['document_id']))
    for row in rows:
        del row['_date_key']
        del row['_zone']
    return rows


def prompt(question, witnesses, *, reading='direct'):
    if reading not in ('direct', 'con') or not isinstance(question, str) or not question.strip():
        raise ValueError('Valid reading method and nonempty question required')
    alce = json.loads((Path(__file__).parents[2]/'_vendor/alce/asqa_default.original.json').read_text())
    reading_instruction = ('Answer the question step by step: first extract all the relevant information, '
        'and then reason over the information to get the answer. Put brief working notes in reasoning.'
        if reading == 'con' else 'Answer the question based on the relevant records. Set reasoning to an empty string.')
    return '\n\n'.join([alce['instruction'], TEAM_CONTRACT, reading_instruction,
        'SCHEMA: '+json.dumps(DocumentAnswers.model_json_schema()),
        'DOCUMENTS (chronological only when time zones are comparable; otherwise input order, not a chronology; IDs stay attached to their original records):\n'+json.dumps(documents(witnesses), ensure_ascii=False),
        'QUESTION: '+question])


def format_answer(question, raw, witnesses):
    out = dict(status='partial', profile='documents', raw='', generation_raw=raw,
        answers=[], claims=[], warnings=[], citation_sources=deepcopy(witnesses),
        cited_numbers=[], verification='Document identity and original offsets only; semantic support requires evaluation.')
    try:
        parsed = parse_model_json(DocumentAnswers, raw)
    except (ValueError, TypeError) as error:
        out.update(status='error', error_type=type(error).__name__, warnings=['invalid_answer_schema'])
        return out
    out['reasoning'] = parsed.reasoning
    for item in parsed.answers:
        numbers, issues = [], []
        for n in item.document_ids:
            if not 1 <= n <= len(witnesses):
                issues.append('out_of_range_document')
            elif n not in numbers:
                numbers.append(n)
        if not numbers:
            issues.append('answer_without_source')
        if len(numbers) > 3:
            issues.append('more_than_three_documents')
        evidence = [deepcopy(witnesses[n-1]) for n in numbers]
        # Retain uncited answers as partial, never silently erase or certify them.
        out['answers'].append(dict(text=item.answer+''.join(f' [{n}]' for n in numbers), evidence=evidence))
        out['claims'].append(dict(text=item.answer, source_numbers=numbers,
            proposed_document_ids=item.document_ids, evidence=deepcopy(evidence), diagnostics=issues))
        out['warnings'].extend(issues)
    out['raw'] = '\n\n'.join(a['text'] for a in out['answers'])
    out['warnings'] = list(dict.fromkeys(out['warnings']))
    out['cited_numbers'] = sorted({n for c in out['claims'] for n in c['source_numbers']})
    out['status'] = ('insufficient' if not parsed.answers else 'partial' if out['warnings'] else 'ok')
    out['alce'] = dict(question=question, output=out['raw'],
        docs=[dict(title=w['location'], text=w['quote']) for w in witnesses])
    return out


def answer_from_sources(question, witnesses, llm, *, reading='direct'):
    content = prompt(question, witnesses, reading=reading)
    if not witnesses:
        return dict(status='insufficient', profile='documents', reading=reading,
                    raw='', answers=[], claims=[], warnings=[], citation_sources=[])
    raw = llm.chat([ChatMessage(role='user', content=content)]).message.content
    return dict(format_answer(question, raw, witnesses), reading=reading)


class DocumentQA:
    """Small explicit composition: search once, read once. No state mutation."""
    def __init__(self, retriever, llm, *, reading='direct'):
        if reading not in ('direct', 'con'):
            raise ValueError('Unknown reading method')
        self.retriever, self.llm, self.reading = retriever, llm, reading

    def ask(self, question):
        if not isinstance(question, str) or not question.strip():
            raise ValueError('Nonempty question required')
        sources = self.retriever.retrieve(question)
        return dict(answer_from_sources(question, sources, self.llm, reading=self.reading),
                    retrieval_sources=deepcopy(sources))


def main():
    import argparse
    from team_memory.readers.retrieval import local_components
    parser = argparse.ArgumentParser(description='One-call original-record QA; JSON input/output, no UI')
    parser.add_argument('--input', required=True, help='JSON with question and original sources')
    parser.add_argument('--model-path', required=True)
    parser.add_argument('--embedding-path', required=True)
    parser.add_argument('--api-base', required=True, help='Explicit loopback Qwen endpoint')
    parser.add_argument('--reading', choices=['direct','con'], default='direct')
    args=parser.parse_args()
    packet=json.loads(Path(args.input).read_text())
    from contextlib import redirect_stdout
    import sys
    with redirect_stdout(sys.stderr):
        parts=local_components(args.model_path,args.embedding_path,args.api_base)
        answer=answer_from_sources(packet['question'],packet['sources'],parts['llm'],reading=args.reading)
    print(json.dumps(answer,ensure_ascii=False))


if __name__=='__main__':
    main()
