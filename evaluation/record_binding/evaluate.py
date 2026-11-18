"""Score the fixed learned-binding candidate; never used during inference."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import tempfile

from team_memory.records import learned_binding, preserving
from evaluation.record_bound.rows import compiled_rows
from evaluation.record_causal.storage import correct_stance_nodes
from evaluation.record_full.evaluate import score, metric
from evaluation.record_groups.evaluate import transport


def main(job):
    out=Path('results/record-binding/v1')
    frozen=json.loads((out/'freeze.json').read_text())
    for table in ('frozen_evaluation_files','code_sha256','controls'):
        for p,h in frozen[table].items(): assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    run=json.loads((out/f'record-binding-{job}.json').read_text())
    assert run['status']=='complete' and len(run['rows'])==68 and run['strict_checkpoint_load']
    assert run['revision']==learned_binding.MODEL_REVISION and run['reference_commit']==learned_binding.REFERENCE_COMMIT
    original={r['id']:r for r in json.loads(Path('results/record-strata/v1/record-strata-122970.json').read_text())['rows'] if r['arm']=='ours'}
    gold={d['id']:d for d in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    inputs={d['id']:d['source'] for d in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']}
    previous={c['id']:c['score'] for c in json.loads(Path('results/record-causal/v1/storage-evaluation.json').read_text())['cases'] if c['stage']=='attributes'}
    cases=[];protection=[];traces=[];saved=[]
    with tempfile.TemporaryDirectory(prefix='record-binding-') as temp:
        for row in run['rows']:
            iid=row['id'];source=inputs[iid];d=gold[iid];assert row['source']==source
            raw=original[iid]['raw'];model='Qwen3-8B@b968826d9c46dd6066d109eabc6255188de91218'
            base=preserving.compile_graph(source,raw,model=model)
            candidate,trace=learned_binding.bind(source,raw,row['prediction'],model=model)
            pair=[]
            for arm,g in [('baseline',base),('learned',candidate)]:
                enriched=dict(source,record_graph=g);rr=compiled_rows(enriched);s=score(rr,d,source)
                stances=correct_stance_nodes(rr,d);assert len(stances)==s['stance_correct']
                if arm=='baseline':assert json.loads(json.dumps(s))==previous[iid]
                t=transport(enriched,Path(temp)/iid/arm)
                cases.append(dict(id=iid,panel=d['panel'],difficulty=d['difficulty'],availability=d['availability'],arm=arm,score=s,transport=t))
                saved.append(dict(id=iid,arm=arm,source=enriched));pair.append((s,stances))
            (a,sa),(b,sb)=pair
            edges=set(map(tuple,d['edges']));nodes={n['id'] for n in d['nodes'] if n['required']}
            protection.append(dict(id=iid,protected_nodes=len(nodes-set(a['missing_nodes'])),
                lost_nodes=sorted((nodes-set(a['missing_nodes'])) & set(b['missing_nodes'])),
                protected_edges=len(edges-set(map(tuple,a['missing_edges']))),
                lost_edges=sorted((edges-set(map(tuple,a['missing_edges']))) & set(map(tuple,b['missing_edges']))),
                new_edges=sorted(set(map(tuple,a['missing_edges']))-set(map(tuple,b['missing_edges']))),
                lost_stances=sorted(sa-sb),protected_stances=len(sa),lost_complete=a['complete'] and not b['complete']))
            traces.append(dict(id=iid,prediction=row['prediction'],trace=trace,source_sha256=sha256(source['text'].encode()).hexdigest()))
    summaries=[]
    for panel in ('balanced_synthetic','natural_audit'):
        for arm in ('baseline','learned'):
            for difficulty,availability in [('all','all')]+([(d,a) for d in ('easy','medium','hard') for a in ('full','partial','none')] if panel=='balanced_synthetic' else []):
                ss=[c['score'] for c in cases if c['panel']==panel and c['arm']==arm and (difficulty=='all' or(c['difficulty']==difficulty and c['availability']==availability))]
                summaries.append(dict(panel=panel,arm=arm,difficulty=difficulty,availability=availability,n=len(ss),
                    metrics={k:metric(*(sum(s[k][z] for s in ss) for z in ('tp','fp','fn'))) for k in ('content_recall','claim_recall','typed_edges')},
                    complete=sum(s['complete'] for s in ss),extra_rows=sum(len(s['extra_rows']) for s in ss),wrong_stance=sum(len(s['stance_wrong']) for s in ss)))
    keep=all(not(p['lost_nodes'] or p['lost_edges'] or p['lost_stances'] or p['lost_complete']) for p in protection)
    no_extra=True
    for panel in ('balanced_synthetic','natural_audit'):
        a,b=[s for s in summaries if s['panel']==panel and s['difficulty']=='all']
        no_extra &= b['metrics']['typed_edges']['fp']<=a['metrics']['typed_edges']['fp'] and b['extra_rows']<=a['extra_rows']
    gain=sum(e[1] in ('condition','basis') for p in protection for e in p['new_edges'])
    report=dict(job_id=job,fixed_criteria=True,baseline_scores_reproduced=68,transport_passed=len(cases),
                prior_correct_items_preserved=keep,no_added_errors_by_panel=no_extra,new_target_links=gain,
                adopt=bool(keep and no_extra and gain),
                native_records=sum(len(r['prediction'].get('statement',[])) for r in run['rows']),
                changed_groups=sum(len(t['trace']['changed_groups']) for t in traces),
                event_reasons=dict(Counter(e['reason'] for t in traces for e in t['trace']['events'])),
                summary=summaries,protection=protection,cases=cases)
    for name,data in [('evaluation.json',report),('binding-traces.json',traces),('stored-records.json',saved)]:
        (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('summary','protection','cases')},indent=2))
    for s in summaries:
        if s['difficulty']=='all':print(json.dumps(s))


if __name__=='__main__':
    import sys
    main(sys.argv[1])
