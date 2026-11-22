"""Source coordinates for explicit Markdown tables and marked list items."""
import re

from .segments import blocks


def _span(text, start, end):
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end-1].isspace():
        end -= 1
    return dict(start=start, end=end, quote=text[start:end])


def _cells(text, start, end):
    # GFM requires pipes inside cells to be escaped, including in code spans.
    cuts = [start + m.start(1) for m in re.finditer(r'(?<!\\)(?:\\\\)*(\|)', text[start:end])]
    return [_span(text, a+1, b) for a,b in zip(cuts,cuts[1:])]


def layout(text):
    rows = []
    columns = []
    for start,end,heading,header,formatting in blocks(text):
        if header and formatting:
            if text[start:end].strip() == header:
                columns = _cells(text,start,end)
        elif header and columns:
            cells = _cells(text,start,end)
            if len(cells) == len(columns):
                rows.append(dict(kind='table',start=start,end=end, cells=cells,headers=columns))
        else:
            columns = []
            match = re.match(r'\s*[-*+]\s+([^:\n]{1,80}):[ \t]+', text[start:end])
            if match:
                label = _span(text,start+match.start(1),start+match.end(1))
                # Commas inside an interval, code span or parenthesis are literal.
                body = text[start+match.end():end]
                offsets = [0]
                depth = 0
                code = False
                for i,c in enumerate(body):
                    if c == "`":
                        code = not code
                    elif not code:
                        if c in '[({': depth += 1
                        elif c in '])}': depth = max(0,depth-1)
                        elif c == ',' and not depth: offsets.append(i+1)
                base = start+match.end()
                values = [_span(text, base+a, base+b) for a,b in
                          zip(offsets,[i-1 for i in offsets[1:]]+[len(body)])]
                rows.append(dict(kind='list',start=start,end=end,label=label,cells=values))
    return rows


def visible_layout(source,start,end):
    rows = source.get('record_graph', {}).get('layout', [])
    # Header coordinates outside the selected passage are retained in storage
    # only. Never supply uncited text outside the retrieval budget.
    output = []
    for row in rows:
        if row['start'] >= end or row['end'] <= start:
            continue
        def visible(span):
            return span if start <= span['start'] and span['end'] <= end else None
        cells = [visible(c) for c in row['cells']]
        if not any(cells):
            continue
        entry = dict(kind=row['kind'], start=row['start'],end=row['end'],cells=cells)
        if row['kind']=='list':
            entry['label']=visible(row['label'])
        else:
            entry['headers']=[visible(c) for c in row['headers']]
        output.append(entry)
    return output


def with_layout(record):
    """Return a derived v3 record, preserving every existing claim and edge."""
    from copy import deepcopy
    from .graph import validate_graph

    original = record['record_graph']
    validate_graph(record, original)
    if original['version'] != 'records.graph/v3':
        raise ValueError('Layout enrichment requires a v3 record')
    result = deepcopy(record)
    rows = layout(result['text'])
    if rows:
        result['record_graph']['layout'] = rows
    validate_graph(result, result['record_graph'])
    return result


def construct(source, generate, *, model, cell_generate=None, **options):
    """Compatibility entry point. Cell generation is no longer used."""
    from .preserving import construct as build_record
    return build_record(source, generate, model=model, **options)
