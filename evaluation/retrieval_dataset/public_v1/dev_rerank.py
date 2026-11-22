"""Reorder a frozen QMSum development pool. Primary arm: cross-encoder within RRF top 5."""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
import re
from pathlib import Path

import numpy as np

from build import meetings, write
from evaluate import read, unique_index


def restrict_top5(rank, rrf):
    head = set(rrf[:5])
    return [sid for sid in rank if sid in head] + rrf[5:]


def speaker_order(query, turns, labels, rrf):
    """Only a single explicitly named subject of 'what did X ...' can promote its turns."""
    text = query.casefold()
    named = []
    for speaker in labels:
        name = re.sub(r' (am|mp|msp)$', '', speaker.casefold())
        pattern = r'\b' + re.escape(name) + r'\b'
        if re.search(pattern, text):
            named.append((speaker, pattern))
    if len(named) != 1 or not re.match(r'^what did (?:the )?' + named[0][1], text):
        return rrf
    return sorted(rrf[:5], key=lambda sid: turns[sid] != named[0][0]) + rrf[5:]


def predict(args):
    from dev_candidates import VAL_SHA
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    assert sha256((args.raw/'meetings.jsonl').read_bytes()).hexdigest() == VAL_SHA
    pools, cases, _, _ = meetings(args.raw)
    by_id = unique_index(cases)
    docs = {d['id']:d['text'] for turns in pools.values() for d in turns}
    speakers = {d['id']:d['text'].split(' — ',1)[0] for turns in pools.values() for d in turns}
    labels = {mid:set(speakers[d['id']] for d in turns) for mid,turns in pools.items()}
    tokenizer = AutoTokenizer.from_pretrained(args.encoder,local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(args.encoder,local_files_only=True).eval()
    rows = []
    cross_scores = []
    with torch.inference_mode():
        for c in read(args.out/'candidates.jsonl'):
            rrf = c['rrf']
            query = by_id[c['id']]['query']
            tokens = tokenizer([query]*len(rrf),[docs[sid] for sid in rrf],padding=True,
                               truncation='only_second',max_length=512,return_tensors='pt')
            logits = model(**tokens).logits[:,0].tolist()
            assert np.isfinite(logits).all()
            scores = dict(zip(rrf,logits))
            cross_scores.append(dict(id=c['id'],scores=scores))
            def ordered(values):
                return sorted(rrf,key=values.__getitem__,reverse=True)
            dense, sparse, cross = ordered(c['dense']), ordered(c['sparse']), ordered(scores)
            methods = dict(rrf=rrf,sparse=sparse,dense=dense,cross=cross,
                           sparse_top5=restrict_top5(sparse,rrf),cross_top5=restrict_top5(cross,rrf))
            methods['speaker_top5'] = speaker_order(query,speakers,labels[c['pool']],rrf)
            for method,rank in methods.items():
                assert len(rank)==len(rrf)==len(set(rrf)) and set(rank)==set(rrf)
                if method.endswith('_top5'):
                    assert set(rank[:5])==set(rrf[:5])
            rows.append(dict(id=c['id'],pool=c['pool'],rankings=methods))
    assert {r['id'] for r in rows} == by_id.keys() and len(rows)==len(cases)
    write(args.out,'rankings.jsonl',rows)
    write(args.out,'cross_scores.jsonl',cross_scores)


def evaluate(out):
    gold = unique_index(read(out/'gold.jsonl'))
    candidates = unique_index(read(out/'candidates.jsonl'))
    rows = list(read(out/'rankings.jsonl'))
    assert len(rows)==len(gold) and {r['id'] for r in rows}==gold.keys()
    assert candidates.keys() == gold.keys()
    meetings_by_id = sorted({r['pool'] for r in rows})
    methods = list(rows[0]['rankings'])
    metrics = ['hit1','mrr5','recall5','all5']
    totals = np.zeros((len(meetings_by_id),len(methods),len(metrics)))
    sizes = np.zeros(len(meetings_by_id))
    changes = defaultdict(lambda:defaultdict(int))
    pool_hits = 0
    for row in rows:
        groups = [set(g) for g in gold[row['id']]['groups']]
        relevant = set.union(*groups)
        m = meetings_by_id.index(row['pool'])
        sizes[m] += 1
        baseline = row['rankings']['rrf']
        assert baseline == candidates[row['id']]['rrf']
        pool_hits += bool(set(baseline)&relevant)
        for i, method in enumerate(methods):
            rank = row['rankings'][method]
            assert sorted(rank) == sorted(baseline) and len(rank) == len(set(rank))
            if method.endswith('_top5'):
                assert set(rank[:5]) == set(baseline[:5])
            first = next((j for j,sid in enumerate(rank[:5],1) if sid in relevant),None)
            hits = sum(bool(g.intersection(rank[:5])) for g in groups)
            totals[m,i] += (first==1,1/first if first else 0,hits/len(groups),hits==len(groups))
            if (first==1) != (baseline[0] in relevant):
                changes[method]['gained' if first==1 else 'lost'] += 1
    n = len(meetings_by_id)
    weights = np.random.default_rng(20261122).multinomial(n,np.full(n,1/n),size=10000)
    draws = np.einsum('bg,gam->bam',weights,totals)/(weights@sizes)[:,None,None]
    centers = totals.sum(axis=0)/sizes.sum()
    ref = methods.index('rrf')
    report = dict(questions=len(rows),meetings=n,pool_with_gold=pool_hits,arms={})
    for i, method in enumerate(methods):
        summary = {}
        for j, metric in enumerate(metrics):
            delta = draws[:,i,j]-draws[:,ref,j]
            summary[metric] = dict(mean=centers[i,j],delta=centers[i,j]-centers[ref,j],
                                   delta_ci95=np.quantile(delta,[.025,.975]).tolist())
        report['arms'][method] = dict(metrics=summary,hit1_gained=changes[method]['gained'],
                                      hit1_lost=changes[method]['lost'])
    (out/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--raw',type=Path)
    parser.add_argument('--encoder')
    parser.add_argument('--score-only',action='store_true')
    opts=parser.parse_args()
    if not opts.score_only:
        if not opts.raw or not opts.encoder:
            parser.error('--raw and --encoder are required for inference')
        predict(opts)
    evaluate(opts.out)
