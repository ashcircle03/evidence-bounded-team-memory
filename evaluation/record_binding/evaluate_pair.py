"""Frozen whole-record scoring for training x integration, no casewise selection."""
from hashlib import sha256
import json
from pathlib import Path
import tempfile

from team_memory.records import preserving, pair_binding
from evaluation.record_binding.pair_rows import compiled_rows
from evaluation.record_causal.storage import correct_stance_nodes
from evaluation.record_full.evaluate import score, metric
from evaluation.record_groups.evaluate import transport


def collapsed_group(source,raw,g):
    """Change only endpoint scope; never regenerate/realign a context quote."""
    from copy import deepcopy
    from team_memory.records.graph import edges_for,validate_graph
    from team_memory.storage.objects import digest
    if g['version']!='records.graph/v4':return g
    result=deepcopy(g);bindings=result.pop('context_bindings');result['version']='records.graph/v3'
    units={u['id']:u for u in result['units']}
    for b in bindings:
        spans=[u for u in result['units'] if b['context_start']<=u['start'] and u['end']<=b['context_end']]
        assert spans and spans[0]['start']==b['context_start'] and spans[-1]['end']==b['context_end']
        for c in result['claims']:
            anchors={(units[a['unit_ids'][0]]['start'],units[a['unit_ids'][-1]]['end']) for a in c['assertions']}
            if (b['target_start'],b['target_end']) not in anchors:continue
            c[b['role']]=sorted(set(c[b['role']])|{u['id'] for u in spans},key=lambda uid:units[uid]['index'])
            if b['role']=='basis':
                kinds={a['unit_id']:a['kind'] for a in c['basis_annotations']}
                c['basis_annotations']=[dict(unit_id=uid,kind=kinds.get(uid,'stated')) for uid in c['basis']]
    for c in result['claims']:c['id']='c:'+digest([source['id'],{k:v for k,v in c.items() if k!='id'}])
    result['edges']=edges_for(source['id'],result['units'],result['claims'])
    result['builder']='same-predictions-group-scope';validate_graph(source,result)
    return result


def main(job):
    out=Path('results/record-binding/v4')
    freeze=json.loads((out/'pair-freeze.json').read_text())
    for table in ('frozen_evaluation_files','code_sha256'):
        for p,h in freeze[table].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
    run=json.loads((out/f'record-pair-{job}.json').read_text())
    assert run['status']=='complete' and len(run['rows'])==68 and run['training_steps']==0
    assert run['code_sha256']==freeze['runtime_code_sha256'] and run['data_sha256']==freeze['data_sha256']
    packet=json.loads(Path(freeze['packet_inputs']).read_text())
    expected={(i['id'],q['context']['id']):pair_binding.request(i['source'],q) for i in packet for q in i['catalog']['queries']}
    calls=[json.loads(x) for x in (out/f'record-pair-{job}.calls.jsonl').read_text().splitlines()]
    assert len(calls)==run['calls']==len(expected)==freeze['max_calls']
    seen=set()
    for c in calls:
        key=(c['item_id'],c['context_id']);assert key not in seen;seen.add(key)
        assert c['request']==expected[key]
        row=next(r for r in run['rows'] if r['id']==c['item_id'])
        assert row['outputs'][c['context_id']]==c['response']['choices'][0]['message']['content']
        assert c['response']['choices'][0]['finish_reason']=='stop'
    assert seen==set(expected)
    preds={r['id']:r for r in run['rows']}
    original={r['id']:r for r in json.loads(Path('results/record-strata/v1/record-strata-122970.json').read_text())['rows'] if r['arm']=='ours'}
    gold={d['id']:d for d in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    inputs={d['id']:d['source'] for d in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']}
    previous={c['id']:c['score'] for c in json.loads(Path('results/record-causal/v1/storage-evaluation.json').read_text())['cases'] if c['stage']=='attributes'}
    cases=[];protection=[];traces=[];saved=[];arms=['baseline','pair_atomic','pair_group']
    with tempfile.TemporaryDirectory(prefix='record-adapt-') as temp:
        for iid,source in inputs.items():
            d=gold[iid];raw=original[iid]['raw'];base=preserving.compile_graph(source,raw,model='Qwen3-8B cached')
            results={};stances={}
            for arm in arms:
                if arm=='baseline':g=base;trace={}
                else:
                    r=preds[iid];assert r['source']==source
                    g,trace=pair_binding.bind(source,raw,r['outputs'],model='Qwen3-8B cached + fixed-pair Qwen3-8B')
                    assert all(g[k]==base[k] for k in ('units','claims','edges'))
                    if arm=='pair_group':g=collapsed_group(source,raw,g)
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
    for n,v in [('pair-evaluation.json',report),('pair-traces.json',traces),('pair-stored.json',saved)]:
        (out/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(decisions,indent=2))
    for s in summary:
        if s['difficulty']=='all':print(json.dumps(s))


if __name__=='__main__':
    import sys
    main(sys.argv[1])
