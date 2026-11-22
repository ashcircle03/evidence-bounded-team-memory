"""How much of stored records is derivable or duplicated.

Run from the repository root:
  python -m evaluation.records.storage_redundancy records results/record-binding/v1/stored-records.json
  python -m evaluation.records.storage_redundancy store /path/to/shared-records

records: any JSON file that contains sources with record_graph (found recursively).
store:   a RecordsAdapter root; reads module_commits/*.json without opening the adapter,
         so it also runs where fcntl is unavailable.
Sizes use the store serialization (store.encoded, key-sorted, indent=2). zlib -9 is
reported as a rough stand-in for Git object compression. Output is JSON on stdout.
"""
import argparse
import json
from pathlib import Path
import sys
import zlib

from team_memory.store import encoded
from team_memory.records.compact import compact_record, is_compact


def size(value):
    raw = encoded(value)
    return dict(raw=len(raw), zlib=len(zlib.compress(raw, 9)))


def add(total, value):
    for key, n in size(value).items():
        total[key] = total.get(key, 0) + n


def share(part, whole):
    return {k: round(1 - part[k] / whole[k], 4) if whole.get(k) else None for k in whole}


def annotated_sources(value):
    if isinstance(value, dict):
        if 'record_graph' in value and 'text' in value:
            yield value
        for child in value.values():
            yield from annotated_sources(child)
    elif isinstance(value, list):
        for child in value:
            yield from annotated_sources(child)


def without(record, field):
    graph = dict(record['record_graph'])
    if field == 'edges':
        graph['edges'] = []
    else:
        graph['units'] = [{k: v for k, v in u.items() if k != 'quote'} for u in graph['units']]
    return dict(record, record_graph=graph)


def measure_records(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    records = list({r['id']: r for r in annotated_sources(data)}.values())
    full, text, no_edges, no_quotes, compact = {}, 0, {}, {}, {}
    versions = {}
    for record in records:
        version = record['record_graph']['version']
        versions[version] = versions.get(version, 0) + 1
        add(full, record)
        text += len(record['text'].encode())
        add(no_edges, without(record, 'edges'))
        add(no_quotes, without(record, 'quotes'))
        add(compact, compact_record(record))
    return dict(kind='records', path=str(path), records=len(records), versions=versions,
                bytes_full=full, text_share_raw=round(text / full['raw'], 4) if full else None,
                saved_by_dropping_edges=share(no_edges, full),
                saved_by_dropping_unit_quotes=share(no_quotes, full),
                saved_by_compact_storage=share(compact, full))


def measure_store(root):
    files = sorted((Path(root) / 'module_commits').glob('*.json'))
    if not files:
        sys.exit(f'No module_commits under {root}')
    total, sources, receipts, projected = {}, {}, {}, {}
    compact_commits = 0
    for path in files:
        commit = json.loads(path.read_text(encoding='utf-8'))
        add(total, commit)
        envs = commit['objects'].get('sources', {})
        add(sources, envs)
        payload = commit.get('payload') or {}
        receipt = payload.get('source') if isinstance(payload, dict) else None
        if receipt is not None:
            add(receipts, receipt)
        already = any(is_compact(e) for e in envs.values()) or (isinstance(receipt, dict) and is_compact(receipt))
        compact_commits += already
        if already:
            add(projected, commit)
            continue
        objects = dict(commit['objects'], sources={k: compact_record(e) for k, e in envs.items()})
        projected_payload = dict(payload, source=compact_record(receipt)) if receipt is not None else commit['payload']
        add(projected, dict(commit, objects=objects, payload=projected_payload))
    ratio = lambda part: {k: round(part.get(k, 0) / total[k], 4) for k in total}
    return dict(kind='store', root=str(root), commits=len(files), compact_commits=compact_commits,
                bytes_total=total, share_sources_in_objects=ratio(sources),
                share_sources_in_receipts=ratio(receipts),
                saved_if_all_compact=share(projected, total))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('kind', choices=('records', 'store'))
    parser.add_argument('path')
    args = parser.parse_args(argv)
    result = measure_records(args.path) if args.kind == 'records' else measure_store(args.path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
