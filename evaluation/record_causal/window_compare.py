"""Fixed-gold raw-output comparison for the one-factor window diagnostic."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json

from evaluation.record_causal.window import request, alignment_audit
from evaluation.record_bound.rows import raw_rows
from evaluation.record_full.evaluate import score, metric


def main(job):
    out=Path('results/record-causal/v1')
    freeze=json.loads((out/'window-freeze.json').read_text())
    for table in ('frozen_evaluation_files','code_sha256'):
        for n,h in freeze[table].items():
            assert sha256(Path(n).read_bytes()).hexdigest()==h,n
    result=json.loads((out/f'record-window-{job}.json').read_text())
    server=json.loads((out/f'sm-{job}.json').read_text())
    assert result['status']==server['status']=='complete' and server['client_exit_code']==0
    assert result['code_sha256']==freeze['code_sha256'] and result['data_sha256']==freeze['data_sha256']
    assert result['model_revision']==server['revision']==freeze['model_revision']
    calls=[json.loads(l) for l in (out/f'record-window-{job}.calls.jsonl').read_text().splitlines()]
    assert len(calls)==len(result['rows'])==result['calls']==68
    old=json.loads(Path('results/record-bound/v1/record-bound-122986.json').read_text())
    old_calls={c['item_id']:c for c in map(json.loads,Path('results/record-bound/v1/record-bound-122986.calls.jsonl').read_text().splitlines())}
    old_scores=json.loads(Path('results/record-bound/v1/evaluation.json').read_text())
    gold={d['id']:d for d in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    inputs={d['id']:d['source'] for d in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']}
    for i,(call,row) in enumerate(zip(calls,result['rows'])):
        assert call['id']==i+1 and call['item_id']==row['id']
        assert row['source']==inputs[row['id']] and call['request']==request(row['source'])
        assert call['response']['choices'][0]['message']['content']==row['raw']
        assert alignment_audit(row['source'],row['raw'])==row['alignment']
    cases=[];protections=[];cost=Counter();calibration=[]
    for oldrow,row,call in zip(old['rows'],result['rows'],calls):
        iid=row['id'];assert oldrow['id']==iid;d=gold[iid];ss=[]
        for arm,r in [('sentence',oldrow),('document',row)]:
            try:rr=raw_rows(r['raw'])
            except (ValueError,KeyError,TypeError):rr=[]
            sc=score(rr,d,inputs[iid]);ss.append(sc)
            if arm=='sentence':
                previous=next(c['raw'] for c in old_scores['cases'] if c['id']==iid and c['arm']=='bound')
                assert json.loads(json.dumps(sc))==previous
            cases.append(dict(id=iid,arm=arm,panel=d['panel'],difficulty=d['difficulty'],availability=d['availability'],score=sc))
        a,b=ss;required={n['id'] for n in d['nodes'] if n['required']}
        oldnodes=required-set(a['missing_nodes']);oldedges=set(map(tuple,d['edges']))-set(map(tuple,a['missing_edges']))
        protections.append(dict(id=iid,protected_nodes=len(oldnodes),lost_nodes=sorted(oldnodes & set(b['missing_nodes'])),new_nodes=sorted(set(a['missing_nodes'])-set(b['missing_nodes'])),protected_edges=len(oldedges),lost_edges=sorted(oldedges & set(map(tuple,b['missing_edges']))),new_edges=sorted(set(map(tuple,a['missing_edges']))-set(map(tuple,b['missing_edges']))),lost_complete=a['complete'] and not b['complete']))
        cost.update({k:v for k,v in call['response']['usage'].items() if k in ('prompt_tokens','completion_tokens','total_tokens')})
        if old_calls[iid]['request']==call['request']:
            calibration.append(dict(id=iid,identical_raw=oldrow['raw']==row['raw'],identical_scores=a==b))
    summaries=[]
    for panel in ('balanced_synthetic','natural_audit'):
        for arm in ('sentence','document'):
            for diff,av in [('all','all')]+([(d,a) for d in ('easy','medium','hard') for a in ('full','partial','none')] if panel=='balanced_synthetic' else []):
                cs=[c['score'] for c in cases if c['panel']==panel and c['arm']==arm and (diff=='all' or(c['difficulty']==diff and c['availability']==av))]
                summaries.append(dict(panel=panel,arm=arm,difficulty=diff,availability=av,n=len(cs),metrics={k:metric(*(sum(s[k][z] for s in cs) for z in ('tp','fp','fn'))) for k in ('content_recall','claim_recall','typed_edges')},complete=sum(s['complete'] for s in cs),extra_rows=sum(len(s['extra_rows']) for s in cs),wrong_stance=sum(len(s['stance_wrong']) for s in cs)))
    report=dict(job_id=job,frozen_criteria_unchanged=True,old_raw_scores_reproduced=68,new_model_calls=68,
                interpretation='Raw extraction comparison only; not a persisted new production graph or QA result.',
                prior_raw_items_preserved=all(not(p['lost_nodes'] or p['lost_edges'] or p['lost_complete']) for p in protections),
                alignment_rejections=sum(len(r['alignment']['rejected']) for r in result['rows']),
                finish_reasons=dict(Counter(c['response']['choices'][0]['finish_reason'] for c in calls)),
                identical_request_controls=calibration,cost=dict(cost),preservation=protections,summary=summaries,cases=cases)
    (out/'window-evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('preservation','summary','cases')},indent=2))
    for s in summaries:
        if s['difficulty']=='all':print(json.dumps(s))


if __name__=='__main__':
    import sys
    main(sys.argv[1])
