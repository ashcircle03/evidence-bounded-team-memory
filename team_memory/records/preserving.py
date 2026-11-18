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


def _aligned_span(source, row, resolver=None):
    import jsonschema
    from langextract.core.data import AlignmentStatus

    envelope = {'extractions': [row]}
    jsonschema.validate(envelope, grouped.output_schema(basis_types=True))
    if resolver is None:
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


def _claim(source, members, units):
    fields = grouped.claim_fields(source, members, units, canonical=True, basis_types=True)
    # The v2 compiler rejected identical groups before v3 added assertion attributes.
    group_id = fields.pop('id')
    assertions = []
    for span in members:
        if span['role'] == 'claim':
            ids = [u['id'] for u in units if span['start'] <= u['start'] and u['end'] <= span['end']]
            assertions.append(dict(unit_ids=ids, stance=span['stance'],
                                   kind='continuation' if assertions else 'assertion'))
    fields.update(assertions=assertions, stance=assertions[0]['stance'])
    fields['id'] = 'c:' + digest([source['id'], fields])
    return group_id, fields


def _prepare(source, raw, model, isolate_invalid):
    diagnostics = []
    groups = defaultdict(list)
    identities = []
    try:
        parsed = json.loads(raw)
        if not isinstance(parsed, dict) or set(parsed) != {'extractions'} or not isinstance(parsed['extractions'], list):
            raise ValueError('Malformed extraction envelope')
        spans = []
        _, resolver = grouped.components()
        for index, row in enumerate(parsed['extractions']):
            try:
                span = _aligned_span(source, row, resolver)
            except Exception as exc:
                if not isolate_invalid:
                    raise
                diagnostics.append(dict(path=f'extractions[{index}]', reason=f'{type(exc).__name__}: {exc}'))
                continue
            span['index'] = index
            span['basis_kind'] = row.get('basis_attributes', {}).get('basis_kind', 'unspecified')
            spans.append(span)
        rooted = {s['group'] for s in spans if s['role'] == 'claim'}
        accepted = []
        for span in spans:
            if span['group'] in rooted:
                accepted.append(span)
                groups[span['group']].append(span)
            elif isolate_invalid:
                diagnostics.append(dict(path='group:' + span['group'], reason='No accepted claim; context is not reparented'))
            else:
                raise ValueError('Orphaned context group')
        units = grouped.partition_units(source, accepted)
        claims = []
        for members in groups.values():
            identity, claim = _claim(source, members, units)
            identities.append(identity)
            claims.append(claim)
        if len(set(identities)) != len(identities):
            raise ValueError('Changed claim identity')
        result = dict(source_id=source['id'], source_fingerprint=graph.source_fingerprint(source),
                      units=units, claims=claims, edges=graph.edges_for(source['id'], units, claims),
                      status=('partial' if claims else 'failed') if diagnostics else 'annotated',
                      errors=['ITEM_REJECTED'] if diagnostics else [])
    except Exception as exc:
        result = graph.build(source)
        result.update(status='failed', errors=[type(exc).__name__])
        diagnostics.append(dict(path='root', reason=f'{type(exc).__name__}: {exc}'))
    result.update(version='records.graph/v3', builder='langextract-preserving-v1', model=model,
                  diagnostics=diagnostics, excluded=[])
    graph.validate_graph(source, result)
    return result, groups, identities


def compile_graph(source, raw, *, model='unspecified', isolate_invalid=False, predict=None):
    """Align once, then update only the claim groups whose context role changed."""
    from .discourse_roles import pairs_from_groups

    result, groups, identities = _prepare(source, raw, model, isolate_invalid)
    if predict is None or result['status'] != 'annotated':
        return result
    pairs = pairs_from_groups(source, groups, result['units'])
    if not pairs:
        return result
    decisions = predict(pairs)
    if len(decisions) != len(pairs) or any(r not in ('condition', 'basis', 'keep') for r in decisions):
        raise ValueError('Invalid discourse role decision batch')
    updates = {p['index']: role for p, role in zip(pairs, decisions) if role not in ('keep', p['old_role'])}
    if not updates:
        return result
    try:
        for i, members in enumerate(groups.values()):
            if not any(s['index'] in updates for s in members):
                continue
            for span in members:
                if span['index'] in updates:
                    span['role'] = updates[span['index']]
                    span['basis_kind'] = 'stated' if span['role'] == 'basis' else 'unspecified'
            identities[i], result['claims'][i] = _claim(source, members, result['units'])
        if len(set(identities)) != len(identities):
            raise ValueError('Changed claim identity')
        result['edges'] = graph.edges_for(source['id'], result['units'], result['claims'])
        graph.validate_graph(source, result)
    except ValueError as exc:
        raise ValueError('Role rewrite failed original graph contract') from exc
    return result


def construct(source, generate, *, model, isolate_invalid=False, predict=None, training_counts=None, parse=None):
    """Drop-in record_builder with unchanged prompt and adopted attribute fix.

    Partial recovery is explicit opt-in: it also exposes wrong rows in documents
    previously rejected wholesale. It has not passed a no-added-false-links gate.
    """
    if 'record_graph' in source:
        raise ValueError('Do not overwrite immutable extraction')
    if parse is not None and training_counts is None:
        raise ValueError('Policy scope requires discourse training counts')
    if training_counts is not None:
        if predict is None:
            raise ValueError('Discourse scope requires a role predictor')
        from .discourse_scope import scoped_predictor
        predict = scoped_predictor(source, predict, training_counts, parse)
    generator, _ = grouped.components()
    prompt = generator.render(source['text'], additional_context=json.dumps(
        {k: source[k] for k in ('id', 'owner', 'speaker', 'observed_at', 'location')}, ensure_ascii=False))
    raw = generate('Extract grounded records using the supplied format and examples.', prompt)
    return dict(deepcopy(source), record_graph=compile_graph(source, raw, model=model, isolate_invalid=isolate_invalid, predict=predict))
