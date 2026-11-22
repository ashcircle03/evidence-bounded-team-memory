"""Offline release checks, including a deliberately invalid future-issue prediction."""
import json
import tempfile
from pathlib import Path
from datetime import datetime
from build import ISSUE_HINT, ANNOTATION, norm
from evaluate import inputs, unique_index, read, ROOT, score, metrics


def verify(folder):
    visible = list(inputs(folder))
    cases = unique_index(c for c,_ in visible)
    gold = unique_index(read(folder/'gold.jsonl'))
    assert cases.keys() == gold.keys()
    seen=set()
    counts={}
    for c,docs in visible:
        task=c['task'];cid=c['id'];ids={d['id'] for d in docs}
        assert len(ids)==len(docs) and set(c)<= {'query','pool','task','before','id'}
        assert (task,norm(c['query'])) not in seen
        seen.add((task,norm(c['query'])))
        groups=gold[cid]['groups']
        assert groups and all(g and set(g)<=ids for g in groups)
        if task=='F02':
            assert len(docs)>=100 and not ISSUE_HINT.search(c['query'])
            for d in docs:
                assert datetime.fromisoformat(d['created'])<datetime.fromisoformat(c['before'])
                assert norm(d['text'])!=norm(c['query']) and not ISSUE_HINT.search(d['text'])
        else:
            assert not ANNOTATION.search(c['query'])
            assert all(set(d)=={'id','text'} and d['id'].startswith(c['pool']+'-') for d in docs)
        counts[task]=counts.get(task,0)+1
    assert min(counts.values())>=100
    with tempfile.TemporaryDirectory() as tmp:
        preds=Path(tmp)/'invalid.jsonl'
        rows=[dict(id=cid,status='error',ranked=[],final=[]) for cid in cases]
        c,docs=next((c,ds) for c,ds in visible if c['task']=='F02')
        pool=next(r['documents'] for r in read(folder/'pools.jsonl') if r['pool']==c['pool'])
        future=next(d for d in pool if datetime.fromisoformat(d['created'])>=datetime.fromisoformat(c['before']))
        p=next(p for p in rows if p['id']==c['id'])
        p.update(status='ok',ranked=[future['id']])
        preds.write_text(''.join(json.dumps(row)+'\n' for row in rows))
        try:
            score(folder,preds)
        except ValueError as e:
            assert 'out-of-time' in str(e)
        else:
            raise AssertionError('Scorer accepted future data')
    print('Validated cases, labels, visibility and future-candidate rejection:',counts)


if __name__=='__main__':
    verify(ROOT/'data')
