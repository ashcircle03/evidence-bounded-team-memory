"""End-to-end records port timings, retaining validation and full snapshots.

Run on a local workstation or allocated Slurm node, never a login node.
Numbers describe synthetic workloads on the reported host, not QA performance.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import statistics
import tempfile
from time import perf_counter

from team_memory.adapters.records import RecordsAdapter
from team_memory.adapters.base import request
from team_memory.contracts.ports import CallContext

CONTEXT = CallContext('bench', 'owner', frozenset(['records:read', 'records:write']))


def invoke(port, op, payload):
    result = port.handle(request(op, payload, workspace_id='bench', request_id='benchmark'), context=CONTEXT)
    assert result['status'] == 'ok', result
    return result['data']


def summary(samples):
    ordered = sorted(samples)
    return {'n': len(samples), 'median_ms': statistics.median(samples) * 1000,
            'p95_ms': ordered[min(len(ordered)-1, int(len(ordered)*.95))] * 1000}


def run(sizes, repeats):
    rows = []
    with tempfile.TemporaryDirectory(prefix='records-bench-') as root:
        port = RecordsAdapter(root, 'bench')
        writes = []
        for i in range(1, max(sizes)+1):
            source = dict(id=f's{i}', owner='owner', speaker='작성자', observed_at='2026-11-15T00:00:00Z',
                          location=f'git:synthetic/{i}', text=f'버전 {i}: 조건 A에서 측정값은 {i}ms. 미승인 제안은 확정값이 아니다.\n')
            start = perf_counter()
            invoke(port, 'record.append', dict(source=source, idempotency_key=str(i), expected_revision=i-1))
            writes.append(perf_counter()-start)
            if i not in sizes:
                continue
            samples = []
            for _ in range(repeats):
                start = perf_counter()
                snapshot = invoke(port, 'snapshot.get', {'snapshot_id': None})
                samples.append(perf_counter()-start)
            assert len(snapshot['sources']) == i
            start = perf_counter()
            reopened = RecordsAdapter(root, 'bench')
            assert invoke(reopened, 'snapshot.get', {'snapshot_id': None}) == snapshot
            cold = perf_counter()-start
            rows.append(dict(records=i, append_last_10=summary(writes[-10:]), read=summary(samples),
                             reopen_and_read_ms=cold*1000,
                             stored_bytes=sum(p.stat().st_size for p in (Path(root)/'module_commits').glob('*.json'))))
    files = ['team_memory/adapters/records.py', 'team_memory/contracts/validation.py']
    return dict(measured_at=datetime.now(timezone.utc).isoformat(), host=platform.platform(), python=platform.python_version(),
                workload='synthetic append-only records; complete validated snapshot responses; no proposals or model calls',
                source_sha256={f: hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in files}, rows=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--sizes', type=int, nargs='+', default=[10, 100, 300])
    parser.add_argument('--repeats', type=int, default=10)
    args = parser.parse_args()
    result = run(args.sizes, args.repeats)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result['rows'], ensure_ascii=False))


if __name__ == '__main__':
    main()
