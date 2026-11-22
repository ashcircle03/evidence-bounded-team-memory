"""Evaluate immediate transcript context for fixed RRF top-five utterances."""
import argparse
import json
from hashlib import sha256
from pathlib import Path

import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from build import meetings, write
from evaluate import read, unique_index
from dev_candidates import VAL_SHA


def pack(tok, query, prev, target, nxt):
    # Keep the same target prefix as in the target-only encoder. Use spare tokens for neighbors.
    budget = 512 - tok.num_special_tokens_to_add(pair=True) - len(query)
    body = target[:budget]
    remaining = budget - len(body)
    if remaining >= 2 and (prev or nxt):
        # Each nonempty neighbor needs a separator and at least one token.
        left = min(len(prev)+1 if prev else 0, remaining//2 if nxt else remaining)
        right = min(len(nxt)+1 if nxt else 0, remaining-left)
        left = min(len(prev)+1 if prev else 0, remaining-right)
        if left >= 2:
            body = prev[-(left-1):] + [tok.sep_token_id] + body
        if right >= 2:
            body = body + [tok.sep_token_id] + nxt[:right-1]
    return tok.prepare_for_model(query, body, add_special_tokens=True, return_attention_mask=True)


def rerank(tok,model,query,tokens,positions,rrf,modes):
    head=rrf[:5]
    q=tok.encode(query,add_special_tokens=False)
    rankings={'rrf':rrf}
    scores={}
    for mode in modes:
        batch=[]
        for sid in head:
            i=positions[sid]
            left=tokens[i-1] if i and mode in ('prev','both') else []
            right=tokens[i+1] if i+1<len(tokens) and mode in ('next','both') else []
            batch.append(pack(tok,q,left,tokens[i],right))
        tensors=tok.pad(batch,return_tensors='pt')
        logits=model(**tensors).logits[:,0].tolist()
        assert np.isfinite(logits).all()
        scores[mode]=dict(zip(head,logits))
        ranked=sorted(head,key=scores[mode].get,reverse=True)
        rankings[mode]=ranked+rrf[5:]
        assert set(ranked)==set(head)
    return rankings,scores


def infer(args):
    root = args.dev
    dest = root/'context'
    dest.mkdir(exist_ok=True)
    assert sha256((args.raw/'meetings.jsonl').read_bytes()).hexdigest() == VAL_SHA
    pools,cases,_,_ = meetings(args.raw)
    cases = unique_index(cases)
    prior = unique_index(read(root/'rankings.jsonl'))
    frozen = unique_index(read(root/'candidates.jsonl'))
    assert cases.keys() == prior.keys() == frozen.keys()
    tok = AutoTokenizer.from_pretrained(args.encoder,local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(args.encoder,local_files_only=True).eval()
    result = []
    with torch.inference_mode():
        for mid, turns in pools.items():
            ids = [d['id'] for d in turns]
            positions = {sid:i for i,sid in enumerate(ids)}
            tokens = tok([d['text'] for d in turns],add_special_tokens=False,verbose=False)['input_ids']
            for c in (c for c in cases.values() if c['pool']==mid):
                cid=c['id']
                rrf=frozen[cid]['rrf']
                assert prior[cid]['rankings']['rrf']==rrf
                rankings,scores = rerank(tok,model,c['query'],tokens,positions,rrf,
                                         ('bare','prev','next','both'))
                assert rankings['bare']==prior[cid]['rankings']['cross_top5'], cid
                result.append(dict(id=cid,pool=mid,rankings=rankings,scores=scores))
            print(mid, len(result), flush=True)
    assert len(result)==len(cases)
    write(dest,'runs.jsonl',result)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dev',type=Path,required=True)
    p.add_argument('--raw',type=Path,required=True)
    p.add_argument('--encoder',required=True)
    infer(p.parse_args())
