"""Recover a reported failure and its scope from a bounded contiguous source window."""
import json
import re

from team_memory import referenced_review
from team_memory.pair_selection import paragraphs
from team_memory.role_review import locate, evidence_link

EXTRACT = (
    'Answer using only the supplied text. Copy one or two short quotes that answer the question. '
    'Write each as: excerpt ID | exact quote. Keep negation, objects and limiting conditions. '
    'Do not infer a missing cause or replace an observed failure with a proposed repair. '
    'If the answer is absent, write NONE. No commentary.'
)
FAILURE = 'What specific error or incorrect behavior did the reported operation exhibit?'
CONDITION = 'Under what input or execution conditions did that observed failure occur?'


def coalesce(witnesses, sources):
    """Restore source order and join only contiguous included paragraphs of one record."""
    result = []
    for sid in dict.fromkeys(w['source_id'] for w in witnesses):
        text = sources[sid]['source']['text']
        spans = sorted((w for w in witnesses if w['source_id'] == sid), key=lambda w: w['start'])
        for w in spans:
            if text[w['start']:w['end']] != w['quote']:
                raise ValueError('window does not resolve to the source')
            if result and result[-1]['source_id'] == sid:
                prev = result[-1]
                gap = text[prev['end']:w['start']]
                if w['start'] >= prev['end'] and not gap.strip():
                    result[-1] = dict(prev, end=w['end'], quote=text[prev['start']:w['end']])
                    continue
            result.append(w)
    return result


def resolve(raw, index):
    if raw.strip().upper() == 'NONE':
        return dict(status='insufficient', evidence=[])
    chunks = re.split(r'\n+|(?=\bE\d+\s*\|)', raw.strip())
    evidence = []
    for line in chunks:
        if not line.strip():
            continue
        key, sep, answer = line.strip().partition('|')
        parent = index.get(key.strip())
        if not sep or parent is None:
            return dict(status='invalid_citation', evidence=[])
        answer = answer.strip().removesuffix('|').strip()
        match = locate(parent['quote'], answer)
        if not match or len(evidence) == 2:
            return dict(status='invalid_citation', evidence=[])
        evidence.append(evidence_link(parent, match))
    return dict(status='answered' if evidence else 'insufficient', evidence=evidence)


def read_context(witnesses, sources, generate):
    windows = coalesce(witnesses, sources)
    index = {f'E{i}': w for i, w in enumerate(windows, 1)}
    excerpts = [dict(id=k, source=w['location'], speaker=w['speaker'], text=w['quote'])
                for k, w in index.items()]
    result = {}
    for field, question in [('failure', FAILURE), ('condition', CONDITION)]:
        content = dict(question=question, evidence=excerpts)
        if field == 'condition':
            content['observed_failure'] = [w['quote'] for w in result['failure']['parsed']['evidence']]
        raw = generate(EXTRACT, json.dumps(content, ensure_ascii=False))
        result[field] = dict(raw=raw, parsed=resolve(raw, index))
    return result


def neighborhood(witness, envelope, radius=2):
    blocks = paragraphs(witness['source_id'], (envelope, 'source_only'))
    at = next((i for i, p in enumerate(blocks) if p.start == witness['start'] and p.quote == witness['quote']), None)
    if at is None:
        raise ValueError('selected report paragraph is missing')
    # Keep the heading outside the observation window when a body is available.
    first = 1 if at > 0 else 0
    return [p.cite() for p in blocks[max(first, at-radius):at+radius+1]]


def revise(base, witnesses, sources, generate):
    if base.get('action') not in ('reassess', 'retest'):
        return base
    extraction = read_context(witnesses, sources, generate)
    report_id = base['incoming']['source_id']
    evidence = {}
    for field, value in extraction.items():
        parsed = value['parsed']
        if parsed['status'] != 'answered' or any(w['source_id'] != report_id for w in parsed['evidence']):
            return dict(action='keep', basis='failure or condition lacks an exact quote in this report')
        evidence[field] = parsed['evidence']
    selected = [w for values in evidence.values() for w in values]
    begin = min(w['start'] for w in selected)
    end = max(w['end'] for w in selected)
    text = sources[report_id]['source']['text']
    support = dict(base['incoming'], start=begin, end=end, quote=text[begin:end])
    rationale = render(base['previous'], evidence)
    answer = dict(base, incoming=support, report_anchor=base['incoming'],
                  failure_evidence=evidence, rationale=rationale)
    if 'alternative' in answer:
        answer['distinction'] = ('The alternative addresses “' + answer['alternative']['quote'] +
                                 '”. The reported observation is “' + support['quote'] + '”.')
    return answer


def render(previous, evidence):
    failure = ' / '.join(w['quote'] for w in evidence['failure'])
    condition = ' / '.join(w['quote'] for w in evidence['condition'])
    return ('Reconsider the earlier decision “' + previous['quote'] +
            '”. The report gives this observed behavior “' + failure +
            '” under the reported conditions “' + condition + '”.')


def assess(previous, sid, incoming, goal, generate):
    base = referenced_review.assess(previous, sid, incoming, goal, generate)
    if base.get('action') not in ('reassess', 'retest'):
        return base
    return revise(base, neighborhood(base['incoming'], incoming), {sid: incoming}, generate)


def valid_evidence(item):
    fields = item.get('failure_evidence')
    if not isinstance(fields, dict) or set(fields) != {'failure', 'condition'}:
        return False
    parent = item['incoming']
    for spans in fields.values():
        if not isinstance(spans, list) or not 1 <= len(spans) <= 2:
            return False
        for w in spans:
            if not isinstance(w, dict) or any(type(w.get(k)) is not int for k in ('start', 'end')):
                return False
            if any(w.get(k) != parent.get(k) for k in ('source_id', 'location', 'speaker')):
                return False
            if not parent['start'] <= w['start'] < w['end'] <= parent['end']:
                return False
            quote = parent['quote'][w['start']-parent['start']:w['end']-parent['start']]
            if quote != w.get('quote') or quote not in item.get('rationale', ''):
                return False
    return item.get('rationale') == render(item['previous'], fields)
