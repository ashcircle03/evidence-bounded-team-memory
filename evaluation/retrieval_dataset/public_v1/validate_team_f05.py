"""Run evidence.retrieve, audit the trace and actual citations, and score both orders."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

import numpy as np

from build import meetings, write
from dev_candidates import VAL_SHA
from evaluate import ROOT, metrics, read, unique_index
from run_team import EPOCH, ReferenceQA, RetrievalAdapter, local_components, source, trace_key


def run(args):
    if args.split == 'dev':
        assert sha256((args.raw/'meetings.jsonl').read_bytes()).hexdigest() == VAL_SHA
        pools, cases, labels, _ = meetings(args.raw)
        archived = {r['id']:r['rrf'] for r in read(ROOT/'qmsum_dev/candidates.jsonl')}
    else:
        pools = {r['pool']:r['documents'] for r in read(ROOT/'data/pools.jsonl')}
        cases = [r for r in read(ROOT/'data/cases.jsonl') if r['task']=='F05']
        labels = read(ROOT/'data/gold.jsonl')
        archived = {r['id']:r['ranked'] for r in read(ROOT/'team-predictions.jsonl')}
    experiment = ROOT / ('qmsum_dev/context' if args.split == 'dev' else 'qmsum_test_context')
    reference = unique_index(read(experiment/'runs.jsonl'))
    assert reference.keys() == {case['id'] for case in cases}
    gold = unique_index(labels)
    parts = local_components(str(args.tokenizer), str(args.model), 'http://127.0.0.1:1/v1')
    def factory(store):
        return ReferenceQA(store, profile='team', **parts)
    by_pool = defaultdict(list)
    for case in cases:
        by_pool[case['pool']].append(case)
    rows = []
    cluster_scores = []
    for mid, questions in by_pool.items():
        scores = []
        snapshot = dict(id=mid, revision=0, as_of=EPOCH, sources=list(map(source,pools[mid])), proposals=[])
        path = args.cache/mid
        adapter = RetrievalAdapter('benchmark', factory, path, snapshot_loader=lambda sid:snapshot)
        adapter.execute('evidence.prepare',dict(snapshot=snapshot),None)
        for case in questions:
            cid = case['id']
            query = dict(text=case['query'], time_scope='current', as_of=None, conditions=[])
            data, errors = adapter.execute('evidence.retrieve',dict(snapshot=snapshot,query=query,max_evidence=256),None)
            assert not errors
            trace = json.loads((path/'traces'/(trace_key(snapshot,query,256)+'.json')).read_text())
            fused, ranked = (trace[name] for name in ('fused','reranked'))
            def nodes(items):
                return [item['node_id'] for item in items]
            assert Counter(nodes(fused[:5])) == Counter(nodes(ranked[:5]))
            assert nodes(fused[5:]) == nodes(ranked[5:])
            before, after = ([item['source_id'] for item in order] for order in (fused, ranked))
            assert after[:5] == reference[cid]['rankings']['prev'][:5]
            frozen = archived[cid]
            assert (list(dict.fromkeys(before)) if args.split=='dev' else before[:5]) == frozen
            assert data['evidence'][0]['source_id'] == after[0]
            groups = [set(g) for g in gold[cid]['groups']]
            values = [metrics('F05',groups,order,[],False) for order in (before,after)]
            scores.append([[v[k] for k in ('MRR@1','Recall@5','MRR@5')] for v in values])
            assert values[0]['Recall@5'] == values[1]['Recall@5']
            rows.append(dict(id=cid,pool=mid,rrf=before,reranked=after))
        cluster_scores.append(scores)
        print(mid, len(rows), flush=True)
    sizes = np.array(list(map(len,cluster_scores)))
    totals = np.array([np.sum(c,axis=0) for c in cluster_scores])
    means = totals.sum(axis=0)/sum(sizes)
    weights = np.random.default_rng(20261122).multinomial(len(sizes),np.full(len(sizes),1/len(sizes)),size=10000)
    draws = np.einsum('bg,gam->bam',weights,totals)/(weights@sizes)[:,None,None]
    intervals = np.quantile(draws[:,1]-draws[:,0],[.025,.975],axis=0)
    report = dict(questions=len(rows),meetings=len(sizes))
    for i,name in enumerate(('Hit@1','Recall@5','MRR@5')):
        report[name] = dict(rrf=means[0,i],reranked=means[1,i],delta=means[1,i]-means[0,i],ci95=intervals[:,i].tolist())
    dest = ROOT/'qmsum_team'
    dest.mkdir(exist_ok=True)
    write(dest,args.split+'-runs.jsonl',rows)
    (dest/(args.split+'-metrics.json')).write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--split',choices=('dev','test'),required=True)
    for name in ('cache','raw','tokenizer','model'):
        parser.add_argument('--'+name,type=Path,required=name!='raw')
    args = parser.parse_args()
    if args.split == 'dev' and args.raw is None:
        parser.error('--raw is required for the development split')
    run(args)
