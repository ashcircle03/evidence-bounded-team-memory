"""No loss of original text, source and location through the official store.

Each document of a public run is appended to its own RecordsAdapter store, the
store is reopened (cold restart), and the snapshot source is compared with what
was appended: text, owner, speaker, observed_at, location and the whole
record_graph (every span start/end/quote). Done for full and compact storage.

  python check_provenance.py <records.jsonl> <panel.json> <out.json> [--limit N]
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import tempfile

from team_memory.adapters.base import request
from team_memory.adapters.records import RecordsAdapter
from team_memory.contracts.ports import CallContext
from team_memory.records.graph import validate_graph

FIELDS = ('id', 'text', 'owner', 'speaker', 'observed_at', 'location')


def roundtrip(source, root, storage):
    ctx = CallContext('provenance', source['owner'], frozenset({'records:write', 'records:read'}))
    port = RecordsAdapter(root, 'provenance', storage=storage, bootstrap=False)
    reply = port.handle(request('record.append', dict(source=source, expected_revision=0,
                                                      idempotency_key=source['id']),
                                workspace_id='provenance', request_id='append'), context=ctx)
    if reply['status'] != 'ok':
        return 'append_' + reply['errors'][0]['code']
    reopened = RecordsAdapter(root, 'provenance', storage=storage, bootstrap=False, cache=False)
    snap = reopened.handle(request('snapshot.get', dict(snapshot_id=None), workspace_id='provenance',
                                   request_id='read'), context=ctx)
    if snap['status'] != 'ok':
        return 'read_' + snap['errors'][0]['code']
    stored = snap['data']['sources'][0]
    if any(stored[k] != source[k] for k in FIELDS):
        return 'source_changed'
    if stored['record_graph'] != source['record_graph']:
        return 'graph_changed'
    return 'ok'


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('records', type=Path)
    parser.add_argument('panel', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--snapshot-at', required=True, help="the run config's snapshot_at")
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    docs = {d['id']: d for d in json.loads(args.panel.read_text())['documents']}
    rows = [json.loads(line) for line in args.records.read_text().splitlines()][:args.limit]
    result = {s: Counter() for s in ('full', 'compact')}
    spans = Counter()
    failures = []
    for row in rows:
        doc = docs[row['id']]
        graph = row['graph']
        # Same source fields as the run (client_variants.py); the graph fingerprint binds them.
        source = dict(id=doc['id'], text=doc['text'], owner='public-corpus', speaker='unknown',
                      observed_at=args.snapshot_at, location=doc['id'], record_graph=graph)
        try:
            validate_graph(source, graph)
        except ValueError as exc:
            result['full']['invalid_graph'] += 1
            failures.append(dict(id=row['id'], storage='validate', reason=str(exc)[:120]))
            continue
        spans['units'] += len(graph['units'])
        spans['claims'] += len(graph['claims'])
        spans['role_links'] += sum(len(c[r]) for c in graph['claims'] for r in ('claim', 'condition', 'basis', 'time', 'subject'))
        for storage in ('full', 'compact'):
            with tempfile.TemporaryDirectory() as tmp:
                outcome = roundtrip(source, Path(tmp)/'store', storage)
            result[storage][outcome] += 1
            if outcome != 'ok':
                failures.append(dict(id=row['id'], storage=storage, reason=outcome))
    report = dict(documents=len(rows), stored=spans, outcomes={k: dict(v) for k, v in result.items()},
                  failures=failures[:50])
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(documents=len(rows), outcomes=report['outcomes'], stored=dict(spans))))


if __name__ == '__main__':
    main()
