"""Freeze the existing team retriever's channel union on official QMSum validation."""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

from llama_index.core.schema import QueryBundle
from build import meetings, write
from run_team import EPOCH, source
from team_memory.adapters.reader_bridge import reader_for
from team_memory.readers.retrieval import ReferenceQA, local_components
from team_memory.readers.retrieval_stages import LlamaIndexCandidates, StagedRetriever

VAL_SHA = 'fc7444e241bdbe6997c01720d07f1a58b7357284acb73f909766e5a4700db49f'


def main(args):
    assert sha256((args.raw/'meetings.jsonl').read_bytes()).hexdigest() == VAL_SHA
    pools, cases, gold, _ = meetings(args.raw)
    args.output.mkdir(exist_ok=True, parents=True)
    write(args.output, 'gold.jsonl', gold)
    parts = local_components(args.tokenizer, args.model, 'http://127.0.0.1:1/v1')
    def factory(store):
        return ReferenceQA(store, profile='team', **parts)
    by_pool = defaultdict(list)
    for case in cases:
        by_pool[case['pool']].append(case)
    with (args.output/'candidates.jsonl').open('w') as output:
        for mid, queries in by_pool.items():
            snapshot = dict(id='dev-'+mid,revision=0,as_of=EPOCH,
                            sources=[source(d) for d in pools[mid]],proposals=[])
            reader = reader_for(factory, args.cache/mid, snapshot)
            reader.prepare_index()
            total = reader.sparse.bm25.scores['num_docs']
            top = LlamaIndexCandidates(reader.index,4,sparse=reader.sparse,use_sparse=True)
            rrf = StagedRetriever(top,llm=reader.llm,fused_top_k=8)
            full = LlamaIndexCandidates(reader.index,total,sparse=reader.sparse,use_sparse=True)
            for case in queries:
                qb = QueryBundle(case['query'])
                reader.sparse.similarity_top_k = min(4,total)
                fused = rrf.retrieve(qb)
                order = list(dict.fromkeys(n.node.metadata['source_id'] for n in fused))
                chunks = {n.node.node_id for n in fused}
                assert chunks == {n.node_id for hits in rrf.last['candidates'].values() for n in hits}
                # Outside-channel top-4 members still need a real score on this same pool.
                reader.sparse.similarity_top_k = total
                scores = {}
                for name, hits in full.retrieve(qb).items():
                    values = defaultdict(list)
                    for hit in hits:
                        if hit.node.node_id in chunks:
                            values[hit.node.metadata['source_id']].append(float(hit.score))
                    assert set(values) == set(order)
                    scores[name] = {sid:max(values[sid]) for sid in order}
                row = dict(id=case['id'],pool=mid,rrf=order,**scores)
                output.write(json.dumps(row)+'\n')
            output.flush()
            print(mid,len(queries),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('raw','cache','output'):
        p.add_argument('--'+key,type=Path,required=True)
    for key in ('tokenizer','model'):
        p.add_argument('--'+key,required=True)
    main(p.parse_args())
