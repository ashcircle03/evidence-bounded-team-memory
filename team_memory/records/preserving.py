"""Preserve an existing LangExtract response without changing its semantics.

The prompt, rows, groups and exact-alignment policy remain those of grouped.py.
Per-extraction attributes follow LangExtract's Extraction model. Item-level
quarantine adapts SchemaLLMPathExtractor's validation pattern, with diagnostics
instead of silent removal. No inferred links or model retries are introduced.
"""
from collections import defaultdict
from copy import deepcopy
import json

from . import graph, grouped
from team_memory.storage.objects import digest


def _aligned_span(source, row):
    import jsonschema
    from langextract.core.data import AlignmentStatus

    envelope = {'extractions': [row]}
    jsonschema.validate(envelope, grouped.output_schema(basis_types=True))
    _, resolver = grouped.components()
    extraction = resolver.resolve(json.dumps(envelope))[0]
    if extraction.extraction_class != 'claim' and extraction.attributes['stance'] != 'unknown':
        raise ValueError('Context has claim stance')
    if extraction.extraction_class in ('condition', 'basis', 'time', 'subject') and source['text'].count(extraction.extraction_text) > 1:
        raise ValueError('Ambiguous repeated context span')
    extraction = list(resolver.align(
        [extraction], source['text'], token_offset=0, char_offset=0,
        enable_fuzzy_alignment=False, accept_match_lesser=False,
    ))[0]
    if extraction.alignment_status != AlignmentStatus.MATCH_EXACT or extraction.char_interval is None:
        raise ValueError('Ungrounded extraction')
    return dict(role=extraction.extraction_class,
                group=extraction.attributes['claim_group'],
                stance=extraction.attributes['stance'],
                start=extraction.char_interval.start_pos,
                end=extraction.char_interval.end_pos)


def compile_graph(source, raw, *, model='unspecified', isolate_invalid=False):
    """Only change storage: always retain assertion attributes; optionally quarantine.

    isolate_invalid=False is the single-change attribute-preservation control.
    True adds item-level quarantine. Ambiguous positions stay unresolved rather
    than guessing the nearest assertion. Raw model output belongs in the caller's
    extraction trace; source text is always retained in the records source.
    """
    diagnostics = []
    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, dict) or set(parsed) != {'extractions'} or not isinstance(parsed['extractions'], list):
            raise ValueError('Malformed extraction envelope')
        accepted = []
        spans = []
        for index, row in enumerate(parsed['extractions']):
            try:
                span = _aligned_span(source, row)
            except Exception as exc:
                if not isolate_invalid:
                    raise
                diagnostics.append(dict(path=f'extractions[{index}]', reason=f'{type(exc).__name__}: {exc}'))
                continue
            accepted.append(row)
            spans.append(span)
        rooted = {s['group'] for s in spans if s['role'] == 'claim'}
        if any(s['group'] not in rooted for s in spans):
            if not isolate_invalid:
                raise ValueError('Orphaned context group')
            for s in spans:
                if s['group'] not in rooted:
                    diagnostics.append(dict(path='group:' + s['group'], reason='No accepted claim; context is not reparented'))
            pairs = [(r, s) for r, s in zip(accepted, spans) if s['group'] in rooted]
            accepted = [r for r, _ in pairs]
            spans = [s for _, s in pairs]
        # The existing compiler owns roles, offsets, grouping and unit partition.
        result = grouped.compile_graph(source, json.dumps({'extractions': accepted}), canonical=True, basis_types=True)
        groups = defaultdict(list)
        for s in spans:
            groups[s['group']].append(s)
        assert len(result['claims']) == len(groups)
        for claim, members in zip(result['claims'], groups.values()):
            assertions = []
            for s in members:
                if s['role'] != 'claim':
                    continue
                ids = [u['id'] for u in result['units'] if s['start'] <= u['start'] and u['end'] <= s['end']]
                assertions.append(dict(unit_ids=ids, stance=s['stance'], kind='assertion' if not assertions else 'continuation'))
            claim['assertions'] = assertions
            claim['stance'] = assertions[0]['stance']
            claim['id'] = 'c:' + digest([source['id'], {k: v for k, v in claim.items() if k != 'id'}])
        result.update(version='records.graph/v3', builder='langextract-preserving-v1', model=model,
                      status=('partial' if result['claims'] else 'failed') if diagnostics else 'annotated',
                      errors=['ITEM_REJECTED'] if diagnostics else [], diagnostics=diagnostics, excluded=[])
        result['edges'] = graph.edges_for(source['id'], result['units'], result['claims'])
    except Exception as exc:
        result = graph.build(source)
        result.update(version='records.graph/v3', builder='langextract-preserving-v1', model=model,
                      status='failed', errors=[type(exc).__name__],
                      diagnostics=diagnostics + [dict(path='root', reason=f'{type(exc).__name__}: {exc}')], excluded=[])
    graph.validate_graph(source, result)
    return result


def construct(source, generate, *, model, isolate_invalid=False):
    """Drop-in record_builder with unchanged prompt and adopted attribute fix.

    Partial recovery is explicit opt-in: it also exposes wrong rows in documents
    previously rejected wholesale. It has not passed a no-added-false-links gate.
    """
    if 'record_graph' in source:
        raise ValueError('Do not overwrite immutable extraction')
    generator, _ = grouped.components()
    prompt = generator.render(source['text'], additional_context=json.dumps(
        {k: source[k] for k in ('id', 'owner', 'speaker', 'observed_at', 'location')}, ensure_ascii=False))
    raw = generate('Extract grounded records using the supplied format and examples.', prompt)
    return dict(deepcopy(source), record_graph=compile_graph(source, raw, model=model, isolate_invalid=isolate_invalid))
