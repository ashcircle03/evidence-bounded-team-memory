"""Opt-in compact storage: values derivable from the immutable source are not stored.

Stored records repeat the source text as a quote on every span and keep graph
edges that graph.edges_for recomputes exactly (validate_graph already compares
them). Measured on 68 stored records: edges 42% / quotes 5% of the bytes.

Compact storage drops, and rebuilds on read:
  record_graph.units[].quote, record_graph.edges,
  record_graph.layout[] cell / header / label quotes, record_graph.excluded[].quote,
  record_arguments.links[] predicate / argument quotes.
start / end offsets are kept. The exchange format (records.graph/v3 and
records.arguments/v1) is unchanged: readers receive the rebuilt full form.
A compact record is marked with record_storage = records.compact/v1 next to the
graph, never inside it. Unmarked (full) records are read as before.
Unit and claim IDs and source_fingerprint never depend on quotes.
"""
from copy import deepcopy

STORAGE_FULL = 'full'
STORAGE_COMPACT = 'compact'
STORAGES = (STORAGE_FULL, STORAGE_COMPACT)
MARKER = 'record_storage'
VERSION = 'records.compact/v1'


def _without_quote(span):
    return {k: v for k, v in span.items() if k != 'quote'}


def _with_quote(text, span):
    # A stored quote in compact form would be silently replaced, hiding damage.
    if 'quote' in span:
        raise ValueError('Compact record must not store a quote')
    start, end = span.get('start'), span.get('end')
    if type(start) is not int or type(end) is not int or not 0 <= start <= end <= len(text):
        raise ValueError('Compact span outside source')
    return dict(sorted({**span, 'quote': text[start:end]}.items()))


def _map_layout(rows, convert):
    result = []
    for row in rows:
        row = dict(row, cells=[convert(c) for c in row['cells']])
        if 'headers' in row:
            row['headers'] = [convert(c) for c in row['headers']]
        if 'label' in row:
            row['label'] = convert(row['label'])
        result.append(row)
    return result


def compact_graph(graph):
    if 'edges' not in graph:
        raise ValueError('Graph is already compact')
    result = {k: deepcopy(v) for k, v in graph.items() if k != 'edges'}
    result['units'] = [_without_quote(u) for u in graph['units']]
    if 'layout' in graph:
        result['layout'] = _map_layout(graph['layout'], _without_quote)
    if 'excluded' in graph:
        result['excluded'] = [_without_quote(x) for x in graph['excluded']]
    return result


def hydrate_graph(text, source_id, graph):
    from .graph import edges_for
    if 'edges' in graph:
        raise ValueError('Compact graph must not store edges')
    result = deepcopy(graph)
    result['units'] = [_with_quote(text, u) for u in graph['units']]
    if 'layout' in graph:
        result['layout'] = _map_layout(graph['layout'], lambda c: _with_quote(text, c))
    if 'excluded' in graph:
        result['excluded'] = [_with_quote(text, x) for x in graph['excluded']]
    result['edges'] = edges_for(source_id, result['units'], result['claims'])
    # Stored JSON is key-sorted; rebuild in the same order as a full record read from disk.
    return dict(sorted(result.items()))


def _map_arguments(layer, convert):
    links = [dict(link, predicate=convert(link['predicate']), argument=convert(link['argument']))
             for link in layer['links']]
    return dict(deepcopy(layer), links=links)


def is_compact(record):
    marker = record.get(MARKER)
    if marker is None:
        return False
    if marker != VERSION:
        raise ValueError(f'Unknown record storage: {marker}')
    return True


def compact_record(record):
    """Envelope or source dict -> compact copy. Records without annotations are unchanged."""
    if is_compact(record):
        raise ValueError('Record is already compact')
    if 'record_graph' not in record and 'record_arguments' not in record:
        return deepcopy(record)
    result = deepcopy(record)
    if 'record_graph' in record:
        result['record_graph'] = compact_graph(record['record_graph'])
    if 'record_arguments' in record:
        result['record_arguments'] = _map_arguments(record['record_arguments'], _without_quote)
    result[MARKER] = VERSION
    return result


def hydrate_record(record, text, source_id):
    """Compact copy -> full copy without the marker. Full records are returned unchanged."""
    if not is_compact(record):
        return record
    if 'record_graph' not in record and 'record_arguments' not in record:
        raise ValueError('Compact marker without annotations')
    result = {k: v for k, v in record.items() if k != MARKER}
    if 'record_graph' in record:
        result['record_graph'] = hydrate_graph(text, source_id, record['record_graph'])
    if 'record_arguments' in record:
        result['record_arguments'] = _map_arguments(record['record_arguments'], lambda s: _with_quote(text, s))
    return result


def hydrate_payload(payload):
    """record.append receipt as stored -> as received, for idempotency comparison."""
    source = payload.get('source') if isinstance(payload, dict) else None
    if not isinstance(source, dict) or not is_compact(source):
        return payload
    return dict(payload, source=hydrate_record(source, source['text'], source['id']))
