"""Evaluate the product retrieval adapter on the frozen public candidate pools."""
import argparse
import json
from pathlib import Path

from evaluate import ROOT, MAX_ITEMS, MAX_CHARS, inputs
from team_memory.adapters.retrieval import RetrievalAdapter, trace_key
from team_memory.adapters.base import Failure
from team_memory.readers.retrieval import ReferenceQA, local_components

EPOCH = '2000-01-01T00:00:00Z'


def source(d):
    return dict(id=d['id'], text=d['text'], speaker='record', owner='record',
                location=d['id'], observed_at=d.get('created', EPOCH).replace(' ', 'T'))


def run(args):
    parts = local_components(args.tokenizer, args.model, 'http://127.0.0.1:1/v1')
    def factory(store):
        return ReferenceQA(store, profile='team', rerank_turns=not args.rrf_only, **parts)
    previous = None
    args.cache.mkdir(parents=True, exist_ok=True)
    with args.output.open('w') as output:
        for c, docs in inputs(ROOT/'data'):
            if c['task'] != args.task:
                continue
            key = c['id'] if c['task']=='F02' else c['pool']
            if key != previous:
                src = [source(d) for d in docs]
                if c['task']=='F02':
                    src.append(source(dict(id=c['id'], text=c['query'], created=c['before'])))
                snapshot = dict(id=key, revision=0, as_of=EPOCH if c['task']=='F05' else src[-1]['observed_at'],
                                sources=src, proposals=[])
                path = args.cache / c['pool']
                adapter = RetrievalAdapter('benchmark',factory,path,snapshot_loader=lambda sid:snapshot)
                if c['task']=='F05':
                    adapter.execute('evidence.prepare',dict(snapshot=snapshot),None)
                previous = key
            try:
                if c['task']=='F02':
                    data,_ = adapter.execute('history.search',dict(snapshot=snapshot,incoming_source_id=c['id'],limit=5),None)
                    ranked = [s['source_id'] for s in data['candidates']]
                    delivered = ranked
                else:
                    query = dict(text=c['query'],time_scope='current',as_of=None,conditions=[])
                    data,_ = adapter.execute('evidence.retrieve',dict(snapshot=snapshot,query=query,max_evidence=256),None)
                    trace = json.loads((path/'traces'/(trace_key(snapshot,query,256)+'.json')).read_text())
                    ranked = [s['source_id'] for s in trace['fused' if args.rrf_only else 'reranked']][:5]
                    delivered = list(dict.fromkeys(e['source_id'] for e in data['evidence']))[:5]
                lengths={d['id']:len(d['text']) for d in docs}
                final=[];total=0
                for sid in delivered:
                    if total+lengths[sid]<=MAX_CHARS and len(final)<MAX_ITEMS:
                        final.append(sid);total+=lengths[sid]
                row=dict(id=c['id'],status='ok',ranked=ranked,final=final)
            except Failure as exc:
                row=dict(id=c['id'],status='error',ranked=[],final=[],error=exc.issue['code'])
                print(c['id'], repr(exc.__cause__ or exc), flush=True)
            output.write(json.dumps(row)+'\n')
            output.flush()


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('tokenizer','model'):
        p.add_argument('--'+key,required=True)
    p.add_argument('--rrf-only',action='store_true',help='Reproduce the archived pre-reranking baseline')
    p.add_argument('--task', choices=['F02','F05'], required=True)
    for key in ('cache','output'):
        p.add_argument('--'+key,type=Path,required=True)
    run(p.parse_args())
