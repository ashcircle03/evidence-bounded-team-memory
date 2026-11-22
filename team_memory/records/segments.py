"""Extract source-local Markdown rows and paragraphs and join their original offsets."""
from copy import deepcopy
import re

from . import graph
from team_memory.storage.objects import digest


def blocks(text):
    lines = text.splitlines(keepends=True)
    pos = 0
    paragraph = None
    heading = header = fence = ''
    for i, raw in enumerate(lines):
        line = raw.strip()
        end = pos + len(raw)
        marker = re.match(r'^(?:`{3,}|~{3,})', line)
        table = not fence and line.startswith('|')
        title = not fence and re.match(r'^#{1,6}\s+', line)
        bullet = not fence and re.match(r'^[-*+]\s+|^\d+[.)]\s+', line)
        boundary = not line or table or title or bullet or marker
        if boundary and paragraph is not None:
            yield paragraph, pos, heading, '', False
            paragraph = None
        if marker:
            if not fence:
                fence = marker[0]
            elif marker[0].startswith(fence):
                fence = ''
            yield pos, end, heading, '', True
        elif table:
            delimiter = r'\|(?:\s*:?-+:?\s*\|)+'
            is_header = i + 1 < len(lines) and re.fullmatch(delimiter, lines[i+1].strip())
            if is_header:
                header = line
            yield pos, end, heading, header, bool(is_header or re.fullmatch(delimiter, line))
        elif title:
            heading = line
            yield pos, end, heading, '', False
        elif line and paragraph is None:
            paragraph = pos
        if not table:
            header = ''
        pos = end
    if paragraph is not None:
        yield paragraph, pos, heading, '', False


SEGMENT_LEGACY = 'legacy'    # one block per paragraph, heading and bullet line (default)
SEGMENT_COMPACT = 'compact'  # opt-in, see compact()
SEGMENTATIONS = (SEGMENT_LEGACY, SEGMENT_COMPACT)
MAX_BLOCK_CHARS = 2000
PRECEDING_SENTENCES = 2
_HEADING = re.compile(r'^\s*#{1,6}\s+')
_BULLET = re.compile(r'^\s*(?:[-*+]|\d+[.)])\s+')


def compact(text, spans, max_chars=MAX_BLOCK_CHARS):
    """Regroup blocks() output for extraction. Offsets are unchanged.

    Returns (start, end, heading, header, formatting, kind) with kind:
    'table'   - table header, delimiter or data row: no model call
    'heading' - a heading line alone: no model call, already passed as section
    'bullets' - a run of consecutive bullet items: one model call for the run
    'text'    - a paragraph, split at sentence ends when longer than max_chars
    """
    merged = []
    for start, end, heading, header, formatting in spans:
        piece = text[start:end]
        if header or formatting:
            kind = 'table'
        elif _HEADING.match(piece) and '\n' not in piece.strip():
            kind = 'heading'
        elif _BULLET.match(piece):
            kind = 'bullets'
            last = merged[-1] if merged else None
            if last and last[5] == 'bullets' and last[2] == heading and not text[last[1]:start].strip():
                last[1] = end
                continue
        else:
            kind = 'text'
        merged.append([start, end, heading, header, formatting, kind])
    result = []
    for block in merged:
        if block[5] in ('text', 'bullets') and block[1] - block[0] > max_chars:
            result.extend(_split_long(text, block, max_chars))
        else:
            result.append(tuple(block))
    return result


def _split_long(text, block, max_chars):
    from .alignment import sentence_bounds
    start, end = block[0], block[1]
    cuts = [start + b for _, b in sentence_bounds(text[start:end])]
    pieces, a = [], start
    for i, cut in enumerate(cuts):
        last = i == len(cuts) - 1
        # Close the piece before it would exceed the limit; one long sentence stays whole.
        if last or (cut - a >= max_chars) or (cuts[i + 1] - a > max_chars):
            b = end if last else cut
            if text[a:b].strip():
                pieces.append((a, b, *block[2:]))
            a = b
    return pieces


def preceding(text, start, sentences=PRECEDING_SENTENCES, reach=600):
    """Last sentences before start: reference context for the model, never quoted."""
    from .alignment import sentence_bounds
    window = text[max(0, start - reach):start]
    if not window.strip():
        return ''
    bounds = sentence_bounds(window)[-sentences:]
    return window[bounds[0][0]:].strip()


def assemble(source, pieces, model, builder='langextract-preserving-blocks-v1'):
    units, claims, diagnostics = [], [], []
    for start, end, part in pieces:
        ids = {}
        for unit in part['units']:
            shifted = dict(unit)
            for key in ('start','end','window_start','window_end'):
                shifted[key] += start
            uid = 'u:' + digest([source['id'], [shifted['start'], shifted['end']]])
            ids[unit['id']] = uid
            shifted.update(id=uid, index=len(units))
            units.append(shifted)
        for original in part['claims']:
            claim = deepcopy(original)
            del claim['id']
            for role in graph.ROLES:
                claim[role] = [ids[i] for i in claim[role]]
            for item in claim['basis_annotations']:
                item['unit_id'] = ids[item['unit_id']]
            for item in claim['assertions']:
                item['unit_ids'] = [ids[i] for i in item['unit_ids']]
            claim['id'] = 'c:' + digest([source['id'],claim])
            claims.append(claim)
        for issue in part.get('diagnostics', []):
            diagnostics.append(dict(path=f"source[{start}:{end}].{issue['path']}",reason=issue['reason']))
    status = ('partial' if claims else 'failed') if diagnostics else 'annotated'
    result = dict(version='records.graph/v3', builder=builder,
                  model=model, source_id=source['id'], source_fingerprint=graph.source_fingerprint(source),
                  units=units, claims=claims, edges=graph.edges_for(source['id'],units,claims),
                  diagnostics=diagnostics, status=status, errors=['BLOCK_FAILURE'] if diagnostics else [], excluded=[])
    graph.validate_graph(source,result)
    return result
