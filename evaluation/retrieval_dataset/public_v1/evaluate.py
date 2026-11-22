"""Export point-in-time inputs, run a BM25 baseline, or score ranked retrieval."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from math import log1p
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
KS=(1,3,5)
MAX_ITEMS=5
MAX_CHARS=4000


def read(path):
    with path.open() as stream:
        for line in stream:
            yield json.loads(line)


def unique_index(rows):
    items={}
    for r in rows:
        if r['id'] in items:
            raise ValueError('Repeated id '+r['id'])
        items[r['id']]=r
    return items


def inputs(folder):
    pools={r['pool']:r['documents'] for r in read(folder/'pools.jsonl')}
    for c in read(folder/'cases.jsonl'):
        docs=pools[c['pool']]
        if c['task']=='F02':
            at=datetime.fromisoformat(c['before'])
            docs=[d for d in docs if datetime.fromisoformat(d['created'])<at]
        yield c,docs


class BM25:
    def __init__(self,docs):
        self.postings=defaultdict(list);self.lengths={};self.n=len(docs)
        for d in docs:
            terms=Counter(re.findall(r'\w+',d['text'].casefold()))
            self.lengths[d['id']]=sum(terms.values())
            for t,f in terms.items():
                self.postings[t].append((d['id'],f))
        self.avg=sum(self.lengths.values())/max(1,self.n)

    def search(self,query):
        scores=Counter()
        for term in sorted(set(re.findall(r'\w+',query.casefold()))):
            rows=self.postings.get(term,[])
            idf=log1p((self.n-len(rows)+0.5)/(len(rows)+0.5))
            for i,f in rows:
                scores[i]+=idf*f*2.2/(f+1.2*(0.25+0.75*self.lengths[i]/self.avg))
        return sorted(scores,key=lambda i:(-scores[i],i))


def baseline(folder):
    cache_key,index=None,None
    for c,docs in inputs(folder):
        k=(c['pool'],c.get('before'))
        if k!=cache_key:
            index=BM25(docs);cache_key=k
        ranked=index.search(c['query'])[:5]
        sizes={d['id']:len(d['text']) for d in docs}
        final=[];total=0
        for i in ranked:
            if total+sizes[i]<=MAX_CHARS:
                final.append(i);total+=sizes[i]
        yield dict(id=c['id'],status='ok',ranked=ranked,final=final)


def metrics(task,groups,ranked,final,failed):
    relevant=set.union(*groups)
    result=dict(error_rate=int(failed),positive_empty_rate=int(not failed and not ranked))
    for k in KS:
        hits=ranked[:k]
        first=next((r for r,i in enumerate(hits,1) if i in relevant),None)
        result[f'MRR@{k}']=1/first if first else 0
        result[f'Recall@{k}']=sum(bool(g.intersection(hits)) for g in groups)/len(groups)
        if task=='F05':
            result[f'all_ranges@{k}']=int(all(g.intersection(hits) for g in groups))
            result[f'turn_recall@{k}']=len(relevant.intersection(hits))/len(relevant)
    if task=='F05':
        result['final_all_ranges']=int(all(g.intersection(final) for g in groups))
    return result


def score(folder,predictions):
    preds=unique_index(read(predictions));gold=unique_index(read(folder/'gold.jsonl'))
    if set(preds)!=set(gold):
        raise ValueError('Prediction IDs must exactly cover all cases; submit explicit error rows for failures')
    sums=defaultdict(Counter);counts=Counter()
    for c,docs in inputs(folder):
        cid=c['id'];p=preds[cid];sizes={d['id']:len(d['text']) for d in docs}
        groups=[set(g) for g in gold[cid]['groups']]
        if not groups or any(not g or not g<=sizes.keys() for g in groups):
            raise ValueError('Unreachable gold: '+cid)
        ranked,final=p['ranked'],p['final']
        for seq in (ranked,final):
            if not isinstance(seq,list) or not set(seq)<=sizes.keys():
                raise ValueError('Invalid or out-of-time prediction: '+cid)
        if len(final)!=len(set(final)) or len(final)>MAX_ITEMS or sum(sizes[i] for i in final)>MAX_CHARS:
            raise ValueError('Invalid final bundle: '+cid)
        if p['status'] not in ('ok','error') or (p['status']=='error' and (ranked or final)):
            raise ValueError('Invalid status: '+cid)
        if c['task']=='F02':
            ranked=list(dict.fromkeys(ranked))
        values=metrics(c['task'],groups,ranked,final,p['status']=='error')
        sums[c['task']].update(values);counts[c['task']]+=1
    return {task:dict(n=counts[task],**{m:round(v/counts[task],6) for m,v in s.items()}) for task,s in sums.items()}


def main():
    p=argparse.ArgumentParser();p.add_argument('command',choices=['inputs','baseline','score'])
    p.add_argument('file',type=Path);p.add_argument('--data',type=Path,default=ROOT/'data');a=p.parse_args()
    if a.command=='score':
        print(json.dumps(score(a.data,a.file),indent=2))
    else:
        rows=baseline(a.data) if a.command=='baseline' else (
            dict(id=c['id'],task=c['task'],query=c['query'],candidates=d) for c,d in inputs(a.data))
        with a.file.open('w') as f:
            for row in rows:
                f.write(json.dumps(row,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
