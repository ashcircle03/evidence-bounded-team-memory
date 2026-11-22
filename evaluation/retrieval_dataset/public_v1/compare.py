"""Paired percentile intervals; resample meetings or connected duplicate-issue groups."""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from evaluate import ROOT, metrics, read, score, unique_index


def bug_components(gold):
    parent = {}

    def root(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    incoming = {}
    for cid, row in gold.items():
        if 'upstream_id' in row:
            sid = 'b-' + hashlib.sha256(row['upstream_id'].encode()).hexdigest()[:16]
            incoming[cid] = sid
            for group in row['groups']:
                for target in group:
                    parent[root(target)] = root(sid)
    return {cid:root(sid) for cid, sid in incoming.items()}


def compare(data, baseline_path, team_path):
    # Run the frozen protocol checks on every ID, cutoff and output budget first.
    for path in (baseline_path, team_path):
        score(data, path)
    predictions = [unique_index(read(p)) for p in (baseline_path, team_path)]
    gold = unique_index(read(data/'gold.jsonl'))
    bugs = bug_components(gold)
    clusters = defaultdict(lambda: defaultdict(list))
    for case in read(data/'cases.jsonl'):
        cid, task = case['id'], case['task']
        groups = [set(g) for g in gold[cid]['groups']]
        arms = []
        for run in predictions:
            p = run[cid]
            ranks = list(dict.fromkeys(p['ranked'])) if task=='F02' else p['ranked']
            arms.append(metrics(task, groups, ranks, p['final'], p['status']=='error'))
        clusters[task][bugs.get(cid,case['pool'])].append(arms)

    result = {}
    for task, grouped in clusters.items():
        sizes = np.array([len(group) for group in grouped.values()])
        keys = list(next(iter(grouped.values()))[0][0])
        totals = np.array([[[sum(pair[arm][k] for pair in group) for k in keys]
                            for arm in range(2)] for group in grouped.values()])
        rng = np.random.default_rng(20261122)
        weights = rng.multinomial(len(sizes), np.full(len(sizes),1/len(sizes)), size=10000)
        trials = np.einsum('bg,gam->bam', weights, totals)/(weights@sizes)[:,None,None]
        center = totals.sum(axis=0)/sizes.sum()
        def entry(value, reps):
            return dict(mean=float(value), ci95=np.quantile(reps,[.025,.975]).tolist())
        rows = {}
        for j, k in enumerate(keys):
            rows[k] = dict(BM25=entry(center[0,j],trials[:,0,j]),team=entry(center[1,j],trials[:,1,j]),
                           delta=entry(center[1,j]-center[0,j],trials[:,1,j]-trials[:,0,j]))
        result[task] = dict(cases=int(sizes.sum()),clusters=len(sizes),metrics=rows)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('team',type=Path)
    p.add_argument('--bm25',type=Path,default=ROOT/'bm25-predictions.jsonl')
    args=p.parse_args()
    print(json.dumps(compare(ROOT/'data',args.bm25,args.team),indent=2))
