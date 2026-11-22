"""Rebuild records from stored Qwen outputs with the current records code (no model calls).

A public run (client_variants.py) stores every model output in order. Feeding them
back through the same builder measures post-processing changes (alignment, repair,
validation) without GPU inference. Output rows keep the run format, so the
teammate's score.sh scores them unchanged.

  python replay_outputs.py <run dir> <out.jsonl> [--variant default|source|nopredict|
         repair|repair-source] [--option key=value ...]

<run dir> is a finished run (config.json, results/records-current-*.jsonl).
The role predictor is called exactly as in the original run (cfg role_dir, conda_prefix).
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess

from team_memory.records import preserving

VARIANT_OPTIONS = {'default': {}, 'source': dict(alignment='source'), 'nopredict': {},
                   'repair': dict(repair_conditions=True),
                   'repair-source': dict(alignment='source', repair_conditions=True)}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('run_dir', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--variant', default='repair', choices=list(VARIANT_OPTIONS))
    parser.add_argument('--option', action='append', default=[], help='extra construct option key=json')
    args = parser.parse_args()
    cfg = json.loads((args.run_dir/'config.json').read_text())
    stored = sorted((args.run_dir/'results').glob('records-current-*.jsonl'))
    assert len(stored) == 1, stored
    rows = [json.loads(line) for line in stored[0].read_text().splitlines()]
    docs = {d['id']: d for d in json.loads(Path(os.environ['RECORD_INPUTS']).read_text())['documents']}
    options = dict(VARIANT_OPTIONS[args.variant])
    for item in args.option:
        key, value = item.split('=', 1)
        options[key] = json.loads(value)
    use_predictor = args.variant != 'nopredict'

    def predict(pairs):
        proc = subprocess.run([cfg['conda_prefix']+'/bin/python', cfg['role_dir']+'/role.py'],
                              input=json.dumps([pairs]), text=True, capture_output=True, check=True,
                              env={k: v for k, v in os.environ.items() if k != 'PYTHONPATH'})
        return json.loads(proc.stdout)[0]

    def work(row):
        doc = docs[row['id']]
        src = dict(doc, owner='public-corpus', speaker='unknown', observed_at=cfg['snapshot_at'], location=doc['id'])
        outputs = [c['output'] for c in row['calls']]
        used = []

        def generate(system, prompt):
            if len(used) >= len(outputs):
                raise RuntimeError('Replay asked for more model calls than were stored')
            used.append(outputs[len(used)])
            return used[-1]
        extra = dict(predict=predict, training_counts={'disjoint': 11974}) if use_predictor else {}
        result = preserving.construct(src, generate, model=cfg['model_revision'], **extra, **options)
        return dict(id=row['id'], graph=result['record_graph'], calls=row['calls'],
                    replay=dict(calls_used=len(used), calls_stored=len(outputs)))

    with ThreadPoolExecutor(4) as pool, args.out.open('x') as stream:
        for row in pool.map(work, rows):
            print(json.dumps(row, ensure_ascii=False), file=stream, flush=True)
    print(json.dumps(dict(rows=len(rows), options=options, predictor=use_predictor)))


if __name__ == '__main__':
    main()
