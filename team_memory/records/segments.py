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


def assemble(source, pieces, model):
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
    result = dict(version='records.graph/v3', builder='langextract-preserving-blocks-v1',
                  model=model, source_id=source['id'], source_fingerprint=graph.source_fingerprint(source),
                  units=units, claims=claims, edges=graph.edges_for(source['id'],units,claims),
                  diagnostics=diagnostics, status=status, errors=['BLOCK_FAILURE'] if diagnostics else [], excluded=[])
    graph.validate_graph(source,result)
    return result
