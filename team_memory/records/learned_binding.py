"""Optional learned record binding using the complete GLiNER2.5 record path.

This is a candidate adapter, not the default extractor. The trained encoder,
candidate proposer, record head and decoder belong to the pinned upstream model.
This adapter only joins their source spans to existing Qwen assertion spans.
No gold, semantic nearest-neighbour match or new assertion is used here.
"""
from copy import deepcopy
import json

from . import preserving

REFERENCE_COMMIT = 'c379245ce9fe0fee03a530a320ddb1885847c4d6'
MODEL_ID = 'fastino/gliner2.5-base-v1'
MODEL_REVISION = '07d99c0ba5d15cb3b24e0a236fa99bdd4ef87a5c'
FIELDS = {
    'claim': 'The complete substantive assertion, instruction, decision or proposed action, including its predicate, object, negation and modality.',
    'condition': 'An explicitly stated applicability restriction for THIS assertion: the situation, environment, subset or prerequisite under which it applies. Not its reason or mere nearby text.',
    'basis': 'An explicitly stated reason, justification, supporting observation or purpose explaining WHY THIS assertion or action holds. Do not infer an unstated reason or use a mere procedure.',
}


def schema(model):
    # Natural anchors and non-exclusive list fields preserve instance identity
    # while allowing a source reason to be shared by more than one assertion.
    result = model.create_schema().structure('statement', mode='natural', anchor='claim')
    result.field('claim', dtype='str', cardinality='required_one', description=FIELDS['claim'])
    for role in ('condition', 'basis'):
        result.field(role, dtype='list', cardinality='zero_or_more', exclusive=False, description=FIELDS[role])
    return result


def predict(model, source):
    # Full original source; upstream returns exact character offsets. Fixed
    # checkpoint default threshold, no threshold search on evaluation cases.
    return model.extract(source['text'], schema(model), threshold=0.5,
                         include_spans=True, include_confidence=True)


def checked_span(text, value):
    if not isinstance(value, dict):
        raise ValueError('Missing learned source span')
    a, b = value.get('start'), value.get('end')
    if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(text):
        raise ValueError('Invalid source offsets')
    if text[a:b] != value.get('text'):
        raise ValueError('Learned quote differs from original source')
    return a, b


def bind(source, original_raw, prediction, *, model):
    """Replace condition/basis only for an unambiguously matched assertion.

    Native anchors must equal an existing assertion interval. A shorter entity
    or predicate is not silently treated as a whole assertion. If several
    records predict the same anchor group, or a field is ambiguous in the old
    exact aligner, leave that group untouched. Empty fields are explicit native
    abstention, not a reason to fall back selectively to old correct edges.
    Structural failure leaves the whole original record unchanged with a trace.
    """
    baseline = preserving.compile_graph(source, original_raw, model=model)
    trace = dict(events=[], changed_groups=[], fallback=False)
    if baseline['status'] != 'annotated':
        trace['events'].append(dict(reason='original_storage_failure'))
        return baseline, trace
    parsed = json.loads(original_raw)
    anchors = {}
    for row in parsed['extractions']:
        if 'claim' not in row:
            continue
        span = preserving._aligned_span(source, row)
        anchors.setdefault((span['start'], span['end']), set()).add(span['group'])
    proposals = {}
    for index, record in enumerate(prediction.get('statement', [])):
        try:
            anchor = checked_span(source['text'], record['claim'])
            groups = anchors.get(anchor, set())
            if len(groups) != 1:
                raise ValueError('Native anchor is not exactly one existing assertion')
            group = next(iter(groups))
            fields = []
            for role in ('condition', 'basis'):
                values = record[role]
                if not isinstance(values, list):
                    raise ValueError('Expected optional list field')
                seen = set()
                for value in values:
                    a, b = checked_span(source['text'], value)
                    if (a, b) in seen:
                        raise ValueError('Duplicate field span')
                    seen.add((a, b))
                    attrs = dict(claim_group=group, stance='unknown')
                    if role == 'basis':
                        attrs['basis_kind'] = 'stated'
                    row = {role: source['text'][a:b], role+'_attributes': attrs}
                    aligned = preserving._aligned_span(source, row)
                    if (aligned['start'], aligned['end']) != (a, b):
                        raise ValueError('Existing aligner chooses another occurrence')
                    fields.append(row)
            proposals.setdefault(group, []).append(fields)
            trace['events'].append(dict(record=index, group=group, reason='matched_anchor', anchor=list(anchor)))
        except (ValueError, KeyError, TypeError) as exc:
            trace['events'].append(dict(record=index, reason=str(exc)))
    selected = {g: p[0] for g, p in proposals.items() if len(p) == 1}
    trace['ambiguous_groups'] = sorted(g for g,p in proposals.items() if len(p)>1)
    new_rows = []
    for row in parsed['extractions']:
        role = next(r for r in ('claim','condition','basis','time','subject') if r in row)
        group = row[role+'_attributes']['claim_group']
        if role in ('condition','basis') and group in selected:
            continue
        new_rows.append(deepcopy(row))
    for g, rows in selected.items():
        new_rows.extend(rows)
        trace['changed_groups'].append(g)
    candidate_raw = json.dumps(dict(extractions=new_rows), ensure_ascii=False)
    candidate = preserving.compile_graph(source, candidate_raw, model=model+' + '+MODEL_ID+'@'+MODEL_REVISION)
    trace['candidate_raw'] = candidate_raw
    if candidate['status'] != 'annotated':
        trace.update(fallback=True, candidate_diagnostics=candidate['diagnostics'])
        return baseline, trace
    return candidate, trace
