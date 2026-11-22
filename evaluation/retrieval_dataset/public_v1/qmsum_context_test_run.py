"""Apply the two frozen development configurations to the published F05 test ranks."""
import argparse
from collections import Counter, defaultdict
from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from build import write
from dev_context import rerank
from evaluate import ROOT, read, unique_index


def run(encoder):
    cases = defaultdict(list)
    for case in read(ROOT / 'data/cases.jsonl'):
        if case['task'] == 'F05':
            cases[case['pool']].append(case)
    baseline = unique_index(read(ROOT / 'team-predictions.jsonl'))
    tok = AutoTokenizer.from_pretrained(encoder, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(encoder, local_files_only=True).eval()
    rows = []
    with torch.inference_mode():
        for pool in read(ROOT / 'data/pools.jsonl'):
            mid = pool['pool']
            if mid not in cases:
                continue
            docs = pool['documents']
            pos = {doc['id']: i for i, doc in enumerate(docs)}
            assert all(doc['id'] == f'{mid}-{i}' for i, doc in enumerate(docs))
            tokens = tok([doc['text'] for doc in docs], add_special_tokens=False, verbose=False)['input_ids']
            for case in cases[mid]:
                pred = baseline[case['id']]
                ranks = pred['ranked']
                assert pred['status'] == 'ok' and 0 < len(ranks) <= 5
                rankings, scores = rerank(tok, model, case['query'], tokens, pos, ranks, ('prev', 'both'))
                assert all(Counter(order) == Counter(ranks) for order in rankings.values())
                rows.append(dict(id=case['id'], pool=mid, rankings=rankings, scores=scores))
            print(mid, len(rows), flush=True)
    assert len(unique_index(rows)) == sum(map(len, cases.values()))
    dest = ROOT / 'qmsum_test_context'
    dest.mkdir(exist_ok=True)
    write(dest, 'runs.jsonl', rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--encoder', type=Path, required=True)
    run(parser.parse_args().encoder)
