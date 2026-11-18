"""Frozen whole-record scoring for training x integration, no casewise selection."""
from hashlib import sha256
import json
from pathlib import Path
import tempfile

from team_memory.records import preserving, context_contract as anchored_binding
from evaluation.record_bound.rows import compiled_rows
from evaluation.record_causal.storage import correct_stance_nodes
from evaluation.record_full.evaluate import score, metric
from evaluation.record_groups.evaluate import transport


def main(job):
    out=Path('results/record-binding/v3-14b')
    freeze=json.loads((out/'anchored-freeze.json').read_text())
    for table in ('frozen_evaluation_files','code_sha256'):
        for p,h in freeze[table].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    run=json.loads((Path('results/record-binding/v2-14b')/f'record-anchored-{job}.json').read_text())
    assert run['status']=='complete' and len(run['rows'])==68 and run['training_steps']==0
    preds={r['id']:r for r in run['rows']}
    original={r['id']:r for r in json.loads(Path('results/record-strata/v1/record-strata-122970.json').read_text())['rows'] if r['arm']=='ours'}
    gold={d['id']:d for d in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    inputs={d['id']:d['source'] for d in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']}
    previous={c['id']:c['score'] for c in json.loads(Path('results/record-causal/v1/storage-evaluation.json').read_text())['cases'] if c['stage']=='attributes'}
    cases=[];protection=[];traces=[];saved=[];arms=['baseline','anchored']
    with tempfile.TemporaryDirectory(prefix='record-adapt-') as temp:
        for iid,source in inputs.items():
            d=gold[iid];raw=original[iid]['raw'];base=preserving.compile_graph(source,raw,model='Qwen3-8B cached')
            results={};stances={}
            for arm in arms:
                if arm=='baseline':g=base;trace={}
                else:
                    r=preds[iid];assert r['source']==source
                    g,trace=anchored_binding.bind(source,raw,r['raw'],model='Qwen3-8B cached + fixed context contract 14b')
                enriched=dict(source,record_graph=g);rr=compiled_rows(enriched);s=score(rr,d,source)
                results[arm]=s;stances[arm]=correct_stance_nodes(rr,d)
                assert len(stances[arm])==s['stance_correct']
                if arm=='baseline':assert json.loads(json.dumps(s))==previous[iid]
                t=transport(enriched,Path(temp)/iid/arm)
                cases.append(dict(id=iid,panel=d['panel'],difficulty=d['difficulty'],availability=d['availability'],arm=arm,score=s,transport=t))
                saved.append(dict(id=iid,arm=arm,source=enriched));traces.append(dict(id=iid,arm=arm,trace=trace))
            a=results['baseline'];edges=set(map(tuple,d['edges']));nodes={n['id'] for n in d['nodes'] if n['required']}
            for arm in arms[1:]:
                b=results[arm]
                protection.append(dict(id=iid,arm=arm,protected_nodes=len(nodes-set(a['missing_nodes'])),
                    lost_nodes=sorted((nodes-set(a['missing_nodes']))&set(b['missing_nodes'])),
                    protected_edges=len(edges-set(map(tuple,a['missing_edges']))),
                    lost_edges=sorted((edges-set(map(tuple,a['missing_edges'])))&set(map(tuple,b['missing_edges']))),
                    new_edges=sorted(set(map(tuple,a['missing_edges']))-set(map(tuple,b['missing_edges']))),
                    lost_stances=sorted(stances['baseline']-stances[arm]),protected_stances=len(stances['baseline']),
                    lost_complete=a['complete'] and not b['complete']))
    summary=[]
    for panel in ('balanced_synthetic','natural_audit'):
        for arm in arms:
            strata=[('all','all')]+([(d,a) for d in ('easy','medium','hard') for a in ('full','partial','none')] if panel=='balanced_synthetic' else [])
            for diff,av in strata:
                ss=[c['score'] for c in cases if c['panel']==panel and c['arm']==arm and (diff=='all' or(c['difficulty']==diff and c['availability']==av))]
                summary.append(dict(panel=panel,arm=arm,difficulty=diff,availability=av,n=len(ss),
                    metrics={k:metric(*(sum(s[k][z] for s in ss) for z in ('tp','fp','fn'))) for k in ('content_recall','claim_recall','typed_edges')},
                    complete=sum(s['complete'] for s in ss),extra_rows=sum(len(s['extra_rows']) for s in ss),wrong_stance=sum(len(s['stance_wrong']) for s in ss)))
    decisions=[]
    for arm in arms[1:]:
        ps=[p for p in protection if p['arm']==arm]
        retained=all(not(p['lost_nodes'] or p['lost_edges'] or p['lost_stances'] or p['lost_complete']) for p in ps)
        no_extra=True
        for panel in ('balanced_synthetic','natural_audit'):
            a=next(s for s in summary if s['panel']==panel and s['arm']=='baseline' and s['difficulty']=='all')
            b=next(s for s in summary if s['panel']==panel and s['arm']==arm and s['difficulty']=='all')
            no_extra &= b['metrics']['typed_edges']['fp']<=a['metrics']['typed_edges']['fp'] and b['extra_rows']<=a['extra_rows']
        gain=sum(e[1] in ('condition','basis') for p in ps for e in p['new_edges'])
        decisions.append(dict(arm=arm,retained=retained,no_added_errors=no_extra,new_target_links=gain,adopt=bool(retained and no_extra and gain)))
    report=dict(job_id=job,criteria_unchanged=True,baseline_scores_reproduced=68,transport_passed=len(cases),decisions=decisions,summary=summary,protection=protection,cases=cases)
    for n,v in [('anchored-evaluation.json',report),('anchored-traces.json',traces),('anchored-stored.json',saved)]:
        (out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(decisions,indent=2))
    for s in summary:
        if s['difficulty']=='all':print(json.dumps(s))


if __name__=='__main__':
    import sys
    main(sys.argv[1])
