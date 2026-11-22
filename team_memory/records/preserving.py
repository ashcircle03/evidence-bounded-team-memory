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
from .alignment import MODE_SOURCE, MODE_TOKEN, MODES, Ambiguous, locate, narrow, sentence_bounds
from team_memory.storage.objects import digest

BUILDER = 'langextract-preserving-v1'
SOURCE_ALIGN_SUFFIX = '+source-align'
REPAIR_SUFFIX = '+repair'


def _check_alignment(alignment):
    if alignment not in MODES:
        raise ValueError(f'Unknown alignment mode: {alignment}')


def _aligned_span(source, row, resolver=None, alignment=MODE_TOKEN):
    import jsonschema
    from langextract.core.data import AlignmentStatus

    envelope = {'extractions': [row]}
    jsonschema.validate(envelope, grouped.output_schema(basis_types=True))
    if resolver is None:
        _, resolver = grouped.components()
    extraction = resolver.resolve(json.dumps(envelope))[0]
    if extraction.extraction_class != 'claim' and extraction.attributes['stance'] != 'unknown':
        raise ValueError('Context has claim stance')
    if alignment == MODE_SOURCE:
        # Character search with a uniqueness rule; see alignment.py.
        span = dict(role=extraction.extraction_class,
                    group=extraction.attributes['claim_group'],
                    stance=extraction.attributes['stance'])
        try:
            span['start'], span['end'] = locate(source['text'], extraction.extraction_text)
        except Ambiguous as exc:
            if extraction.extraction_class == 'claim':
                raise ValueError('Ambiguous repeated claim span') from exc
            # Narrowed to the claim's sentence once the group's claims are known.
            span.update(start=None, end=None, candidates=exc.candidates)
        return span
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


def _narrow_repeated(source, spans, diagnostics, isolate_invalid):
    """Source alignment only: place a repeated context quote within its claim's sentence."""
    pending = [s for s in spans if 'candidates' in s]
    if not pending:
        return spans
    bounds = sentence_bounds(source['text'])
    anchors = defaultdict(list)
    for s in spans:
        if s['role'] == 'claim':
            anchors[s['group']].append((s['start'], s['end']))
    kept = []
    for s in spans:
        if 'candidates' in s:
            try:
                s['start'], s['end'] = narrow(source['text'], s.pop('candidates'), anchors[s['group']], bounds)
            except Ambiguous as exc:
                if not isolate_invalid:
                    raise ValueError(str(exc)) from exc
                diagnostics.append(dict(path=f"extractions[{s['index']}]", reason=f'ValueError: {exc}'))
                continue
        kept.append(s)
    return kept


def _prepare(source, raw, model, isolate_invalid, alignment=MODE_TOKEN, repair_conditions=False):
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
                span = _aligned_span(source, row, resolver, alignment)
            except Exception as exc:
                if not isolate_invalid:
                    raise
                diagnostics.append(dict(path=f'extractions[{index}]', reason=f'{type(exc).__name__}: {exc}'))
                continue
            span['index'] = index
            span['basis_kind'] = row.get('basis_attributes', {}).get('basis_kind', 'unspecified')
            spans.append(span)
        if alignment == MODE_SOURCE:
            spans = _narrow_repeated(source, spans, diagnostics, isolate_invalid)
        if repair_conditions:
            from .repair import repair_spans
            spans = repair_spans(source['text'], spans)
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
    builder = BUILDER + (SOURCE_ALIGN_SUFFIX if alignment == MODE_SOURCE else '') + (REPAIR_SUFFIX if repair_conditions else '')
    result.update(version='records.graph/v3', builder=builder, model=model,
                  diagnostics=diagnostics, excluded=[])
    graph.validate_graph(source, result)
    return result, groups, identities


def compile_graph(source, raw, *, model='unspecified', isolate_invalid=False, predict=None, alignment=MODE_TOKEN,
                  repair_conditions=False):
    """Align once, then update only the claim groups whose context role changed.

    alignment='source' is opt-in: unique character positions, Korean particles,
    case-sensitive repeats reported instead of silently taking the first match.
    """
    from .discourse_roles import pairs_from_groups

    _check_alignment(alignment)
    result, groups, identities = _prepare(source, raw, model, isolate_invalid, alignment, repair_conditions)
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


def construct(source, generate, *, model, isolate_invalid=True, predict=None, training_counts=None, parse=None,
              alignment=MODE_TOKEN, segmentation='legacy', max_block_chars=None, repair_conditions=False):
    """Drop-in record_builder with unchanged prompt and adopted attribute fix.

    Partial recovery is the default (2026-11-22): one ungrounded or ambiguous row
    is dropped with its reason in diagnostics instead of failing the whole source.
    It also exposes rows of documents previously rejected wholesale; the 68-document
    no-added-false-links check is pending. isolate_invalid=False restores the old
    all-or-nothing behaviour (compile_graph keeps False as its default).

    Opt-in, defaults unchanged:
    alignment='source'      unique character positions (see alignment.py)
    segmentation='compact'  no call for headings or table rows, one call per bullet
                            run, long paragraphs split at sentence ends with the
                            preceding sentences as unquotable reference context
    """
    if 'record_graph' in source:
        raise ValueError('Do not overwrite immutable extraction')
    if parse is not None and training_counts is None:
        raise ValueError('Policy scope requires discourse training counts')
    if training_counts is not None and predict is None:
        raise ValueError('Discourse scope requires a role predictor')
    _check_alignment(alignment)
    options = dict(model=model, isolate_invalid=isolate_invalid, predict=predict,
                   training_counts=training_counts, parse=parse, alignment=alignment,
                   repair_conditions=repair_conditions)
    suffix = (SOURCE_ALIGN_SUFFIX if alignment == MODE_SOURCE else '') + (REPAIR_SUFFIX if repair_conditions else '')

    def extract(local, context):
        return _extract(local, generate, context=context, **options)

    result = build_blocks(source, extract if generate is not None else None, model=model,
                          segmentation=segmentation, max_block_chars=max_block_chars,
                          builders=('langextract-preserving-blocks-v1' + suffix,
                                    'langextract-preserving-blocks-v2' + suffix),
                          single_builder=BUILDER + suffix)
    return dict(deepcopy(source), record_graph=result)


def build_blocks(source, extract, *, model, segmentation='legacy', max_block_chars=None, builders,
                 single_builder=BUILDER):
    """Shared block loop for every extractor; returns the record_graph.

    extract(local_source, context) returns one graph part. context is None when
    the whole source is a single plain block, else {section, columns[, preceding_text]}.
    extract=None keeps raw units only. builders = (legacy name, compact name);
    single_builder names a failed whole-source extraction.
    An extractor failure (model timeout, connection error) never loses the source:
    the source is kept as raw units with status failed and the reason (F01).
    """
    from .segments import (blocks, assemble, compact, preceding, SEGMENTATIONS,
                           SEGMENT_COMPACT, MAX_BLOCK_CHARS)
    if segmentation not in SEGMENTATIONS:
        raise ValueError(f'Unknown segmentation: {segmentation}')
    if max_block_chars is not None and segmentation != SEGMENT_COMPACT:
        raise ValueError('max_block_chars requires compact segmentation')
    text = source['text']
    spans = list(blocks(text))
    if segmentation == SEGMENT_COMPACT:
        plan = compact(text, spans, max_block_chars or MAX_BLOCK_CHARS)
        if extract is not None and len(plan) == 1 and plan[0][5] in ('text', 'bullets'):
            result = _extract_whole(source, extract, model, single_builder)
        else:
            pieces = []
            for a, b, heading, header, _, kind in plan:
                local = dict(source, text=text[a:b])
                if kind in ('table', 'heading') or extract is None:
                    part = graph.build(local)
                else:
                    context = dict(section=heading, columns=header)
                    earlier = preceding(text, a)
                    if earlier:
                        context['preceding_text'] = earlier
                    part = _extract_or_raw(local, extract, context)
                pieces.append((a, b, part))
            result = assemble(source, pieces, model, builder=builders[1])
    elif extract is not None and len(spans) <= 1 and not any(header or formatting for _,_,_,header,formatting in spans):
        result = _extract_whole(source, extract, model, single_builder)
    else:
        pieces = []
        for a, b, heading, header, formatting in spans:
            local = dict(source, text=text[a:b])
            if formatting or header or extract is None:
                part = graph.build(local)
            else:
                part = _extract_or_raw(local, extract, dict(section=heading, columns=header))
            pieces.append((a,b,part))
        result = assemble(source, pieces, model, builder=builders[0])
    from .layout import layout
    rows = layout(source['text'])
    if rows:
        result['layout'] = rows
        graph.validate_graph(source, result)
    return result


def failed_graph(source, model, builder, exc):
    """The source as raw units with status failed and the reason (F01)."""
    part = graph.build(source)
    part.update(version='records.graph/v3', builder=builder, model=model, status='failed',
                errors=['EXTRACTION_FAILURE'], excluded=[],
                diagnostics=[dict(path='root', reason=type(exc).__name__+': '+str(exc))])
    graph.validate_graph(source, part)
    return part


def _extract_whole(source, extract, model, builder):
    """Whole-source extraction; on failure keep the source as a failed raw graph."""
    try:
        return extract(source, None)
    except Exception as exc:
        return failed_graph(source, model, builder, exc)


def _extract_or_raw(local, extract, context):
    """One block's extraction; on failure keep its raw units and the reason."""
    try:
        return extract(local, context)
    except Exception as exc:
        part = graph.build(local)
        part['diagnostics'] = [dict(path='root', reason=type(exc).__name__+': '+str(exc))]
        return part


def _extract(source, generate, model, isolate_invalid, predict, training_counts, parse, context=None,
             alignment=MODE_TOKEN, repair_conditions=False):
    if training_counts is not None:
        if predict is None:
            raise ValueError('Discourse scope requires a role predictor')
        from .discourse_scope import scoped_predictor
        predict = scoped_predictor(source, predict, training_counts, parse)
    # Korean sources add a Korean example; other sources keep the unchanged prompt.
    generator, _ = grouped.components(*grouped.prompt_parts(source['text']))
    metadata = {k: source[k] for k in ('id', 'owner', 'speaker', 'observed_at', 'location')}
    if context:
        metadata.update(context)
    # ensure_ascii=False shows non-ASCII names (speaker 민수) as written; ASCII metadata is byte-identical.
    prompt = generator.render(source['text'], additional_context=json.dumps(metadata, ensure_ascii=False))
    system = 'Extract grounded records using the supplied format and examples.'
    if context:
        system += (' Extract only from the current row or paragraph. Use section and column labels for interpretation. '

                   'Keep distinct results and their scopes together; quote only text present in this block.')
        if context.get('preceding_text'):
            system += (' preceding_text is earlier source text given only to resolve references; '
                       'never quote it or extract records from it.')
    system += (' Use one group per action or reported result. Ask: who performed it, what was acted '
               'on, and under what explicit circumstances? Keep an explicit actor with its action '
               'in the claim. Use subject for the affected object or measured entity, condition for '
               'an explicit applicability restriction, basis for a stated reason. Do not infer the '
               'actor from the author. Leave unexpressed arguments empty and copy original spans.')
    raw = generate(system, prompt)
    return compile_graph(source, raw, model=model, isolate_invalid=isolate_invalid, predict=predict,
                         alignment=alignment, repair_conditions=repair_conditions)
