"""Paired meeting bootstrap and per-case diagnostics on frozen context rankings."""
import argparse
import json
from collections import Counter
from pathlib import Path
import numpy as np
from evaluate import read, unique_index, metrics


def rank_of_hit(rank, relevant):
    return next((i for i,sid in enumerate(rank,1) if sid in relevant),0)


def borders_gold(sid, relevant):
    pool, number = sid.rsplit('-',1)
    return any(f'{pool}-{int(number)+d}' in relevant for d in (-1,1))


def analyze(root):
    dest=root/'context'
    runs=unique_index(read(dest/'runs.jsonl'))
    gold=unique_index(read(root/'gold.jsonl'))
    candidates=unique_index(read(root/'candidates.jsonl'))
    assert runs.keys()==gold.keys()==candidates.keys()
    pools=sorted({r['pool'] for r in runs.values()})
    modes=['rrf','bare','prev','next','both']
    names=['hit1','recall5','mrr5']
    totals=np.zeros((len(pools),len(modes),len(names)))
    sizes=np.zeros(len(pools))
    gains={m:{b:Counter() for b in ('rrf','bare')} for m in modes}
    ranks=Counter()
    details=[]
    for cid,row in runs.items():
        groups=[set(g) for g in gold[cid]['groups']]
        relevant=set.union(*groups)
        rr=candidates[cid]['rrf']
        assert rr==row['rankings']['rrf']
        cluster=pools.index(row['pool'])
        sizes[cluster]+=1
        first={}
        for j,m in enumerate(modes):
            rank=row['rankings'][m]
            assert set(rank[:5])==set(rr[:5]) and rank[5:]==rr[5:] and len(rank)==len(rr)
            first[m]=rank_of_hit(rank,relevant)
            vals=metrics('F05',groups,rank,[],False)
            totals[cluster,j]+=[vals['MRR@1'],vals['Recall@5'],vals['MRR@5']]
        for m in modes:
            for b in ('rrf','bare'):
                if (first[m]==1)!=(first[b]==1):
                    gains[m][b]['gain' if first[m]==1 else 'loss']+=1
        ranks[first['rrf']]+=1
        if first['rrf']>1:
            details.append(dict(id=cid,pool=row['pool'],first_hit=first,
                                rrf_top1=rr[0],both_top1=row['rankings']['both'][0],
                                both_top1_neighbors_gold=borders_gold(row['rankings']['both'][0],relevant)))
    w=np.random.default_rng(20261122).multinomial(len(sizes),np.full(len(sizes),1/len(sizes)),size=10000)
    draws=np.einsum('bg,gam->bam',w,totals)/(w@sizes)[:,None,None]
    mu=totals.sum(axis=0)/sizes.sum()
    arms={}
    for j,m in enumerate(modes):
        arms[m]={'metrics':dict(zip(names,mu[j])), 'changes':gains[m]}
        for b in ('rrf','bare'):
            k=modes.index(b)
            arms[m]['vs_'+b]={name:dict(delta=mu[j,h]-mu[k,h],
                ci95=np.quantile(draws[:,j,h]-draws[:,k,h],[.025,.975]).tolist()) for h,name in enumerate(names)}
    report=dict(questions=len(runs),meetings=len(pools),first_hit_histogram=ranks,arms=arms)
    (dest/'metrics.json').write_text(json.dumps(report,indent=2)+'\n')
    (dest/'misses.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in details))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('dev',type=Path)
    analyze(p.parse_args().dev)
