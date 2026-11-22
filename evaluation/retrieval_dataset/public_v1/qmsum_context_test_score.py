"""Evaluate frozen test rankings with paired whole-meeting bootstrap intervals."""
from collections import Counter, defaultdict
import json

import numpy as np
from evaluate import ROOT, metrics, read, unique_index

DEST = ROOT / 'qmsum_test_context'
ARMS = ('rrf', 'prev', 'both')
METRICS = ('MRR@1', 'Recall@5', 'MRR@5')


def summarize():
    runs = unique_index(read(DEST / 'runs.jsonl'))
    baseline = unique_index(read(ROOT / 'team-predictions.jsonl'))
    gold = unique_index(read(ROOT / 'data/gold.jsonl'))
    cases = unique_index(c for c in read(ROOT / 'data/cases.jsonl') if c['task'] == 'F05')
    assert cases.keys() == runs.keys()
    clusters = defaultdict(list)
    for cid, case in cases.items():
        row = runs[cid]
        ranks = row['rankings']
        assert row['pool'] == case['pool'] and ranks['rrf'] == baseline[cid]['ranked']
        groups = [set(g) for g in gold[cid]['groups']]
        scores = []
        for arm in ARMS:
            assert Counter(ranks[arm]) == Counter(ranks['rrf'])
            result = metrics('F05', groups, ranks[arm], [], False)
            scores.append([result[key] for key in METRICS])
        assert all(s[1] == scores[0][1] for s in scores)
        clusters[row['pool']].append(scores)
    sizes = np.array([len(group) for group in clusters.values()])
    totals = np.array([np.sum(group, axis=0) for group in clusters.values()])
    rows = np.concatenate(list(clusters.values()))
    means = rows.mean(axis=0)
    weights = np.random.default_rng(20261122).multinomial(
        len(sizes), np.full(len(sizes), 1 / len(sizes)), size=10000)
    draws = np.einsum('bg,gam->bam', weights, totals) / (weights @ sizes)[:, None, None]
    archived = json.loads((ROOT / 'team-comparison.json').read_text())['F05']['metrics']
    report = dict(questions=len(rows), meetings=len(sizes), arms={})
    for j, arm in enumerate(ARMS):
        flips = rows[:, j, 0] - rows[:, 0, 0]
        stats = dict(hits=int(rows[:, j, 0].sum()), gained=int(sum(flips > 0)), lost=int(sum(flips < 0)))
        for i, name in enumerate(METRICS):
            assert np.isclose(means[0, i], archived[name]['team']['mean'])
            delta = draws[:, j, i] - draws[:, 0, i]
            stats['Hit@1' if i == 0 else name] = dict(
                mean=means[j, i], ci95=np.quantile(draws[:, j, i], [.025, .975]).tolist(),
                delta=means[j, i] - means[0, i], delta_ci95=np.quantile(delta, [.025, .975]).tolist())
        report['arms'][arm] = stats
    (DEST / 'metrics.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    summarize()
