"""Paired original-output regression, with separate protection for the five prior gains."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory

from evaluation.record_binding.discourse.evaluate import edge_identity
from evaluation.record_binding.first_loss import reader_packets,read
from evaluation.record_bound.rows import compiled_rows
from evaluation.record_causal.storage import correct_stance_nodes
from evaluation.record_full.evaluate import score
from team_memory.records import discourse_roles,discourse_scope,preserving

OUT=Path('results/record-binding/discourse-scope')
SOURCE=Path('../campaigns/speakermem-dev/source')
ARMS=('old','sentence','support','combined')

def main(job):
    manifest=read(OUT/'freeze.json')
    for path,expected in manifest['files'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected,path
    packet=SOURCE/'record-discourse-scope-v1'
    run=read(OUT/f'record-scope-{job}.json')
    assert run['job']==job and run['status']=='complete'
    for name,h in run['hashes'].items():assert h==manifest['files'][str(packet/name)]
    old_run=read('results/record-binding/discourse-role/record-discourse-124235.json')
    assert run['calibration']==old_run['calibration']
    gold={d['id']:d for d in read('evaluation/record_full/gold.json')['documents']}
    orig={d['id']:d for d in read(SOURCE/'record-pair-v1/inputs.json')}
    prior={d['id']:d for d in read('results/record-binding/discourse-role/evaluation.json')['cases']}
    old_outputs={d['id']:d['decisions'] for d in old_run['rows']}
    docs=read(packet/'pairs.json')
    assert len(docs)==68 and {d['id'] for d in docs}==set(prior)==set(gold)
    n=sum(len(d['pairs']) for d in docs)
    assert all(len(x)==n for x in run['outputs'].values()) and n==40
    cases=[];at=0
    with TemporaryDirectory() as root:
        for d in docs:
            iid=d['id'];source=orig[iid]['source'];raw=orig[iid]['original_raw'];key=gold[iid]
            pairs=d['pairs'];loc=d['localized'];m=len(pairs)
            assert pairs==discourse_roles.candidates(source,raw)
            assert loc==[dict(p,geometry=discourse_scope.geometry(p)) for p in discourse_scope.sentence_pairs(source,pairs)]
            outputs={k:v[at:at+m] for k,v in run['outputs'].items()};at+=m
            assert [v['decision'] for v in outputs['old']]==[v['decision'] for v in old_outputs[iid]]
            for preds in outputs.values():
                for v in preds:
                    names=['keep','condition','basis'];k=max(range(3),key=v['probs'].__getitem__);label=names[k]
                    thr=run['calibration'].get(label,{}).get('threshold')
                    assert v['argmax']==label and v['decision']==(label if thr is not None and v['probs'][k]>=thr else 'keep')
            g=preserving.compile_graph(source,raw,model='baseline')
            def evaluate(graph):
                s=dict(source,record_graph=graph);rows=compiled_rows(s);metrics=score(rows,key,source)
                fp={edge_identity(e,s,rows) for e in metrics['incorrect_edges']}
                return metrics,fp,correct_stance_nodes(rows,key)
            base,bad,stance=evaluate(g)
            assert json.loads(json.dumps(base))==prior[iid]['before']
            res={};cache={};counts=run['train_stats']['geometries']
            for arm in ARMS:
                predicted=outputs['old' if arm in ('old','support') else 'sentence']
                roles=[v['decision'] for v in predicted]
                if arm in ('combined','support'):
                    roles=discourse_scope.supported_decisions(loc,roles,counts)
                if tuple(roles) not in cache:
                    graph=discourse_roles.apply(source,raw,lambda _:roles,model='scope-probe')
                    assert g['units']==graph['units'] and g['status']==graph['status']
                    assert [c['assertions'] for c in g['claims']]==[c['assertions'] for c in graph['claims']]
                    cache[tuple(roles)]=graph,evaluate(graph)
                graph,(s,wrong,stances)=cache[tuple(roles)]
                missing=set(s['missing_edges']);before=set(base['missing_edges'])
                res[arm]=dict(decisions=roles,typed=s['typed_edges'],complete=s['complete'],
                    lost_complete=bool(base['complete'] and not s['complete']),lost=sorted(missing-before),
                    gained=sorted(before-missing),prior_gains_lost=sorted(missing&set(map(tuple,prior[iid]['recovered']))),
                    new_fp=sorted(wrong-bad),removed_fp=sorted(bad-wrong),lost_stances=sorted(stance-stances),
                    lost_nodes=sorted(set(s['missing_nodes'])-set(base['missing_nodes'])),
                    lost_claims=sorted(set(s['missing_claims'])-set(base['missing_claims'])),
                    extra_increase=len(s['extra_rows'])-len(base['extra_rows']))
                if arm=='old':assert json.loads(json.dumps(s))==prior[iid]['after']
                if arm in ('combined','support'):
                    reader_packets(dict(source,record_graph=graph),Path(root)/iid/arm)
            cases.append(dict(id=iid,panel=key['panel'],pairs=pairs,localized=loc,outputs=outputs,results=res))
    assert at==40
    summary={}
    for arm in ARMS:
        rr=[c['results'][arm] for c in cases]
        summary[arm]=dict(tp=sum(r['typed']['tp'] for r in rr),fp=sum(r['typed']['fp'] for r in rr),
            complete=sum(r['complete'] for r in rr),old_correct_lost=sum(len(r['lost']) for r in rr),
            protected_five_lost=sum(len(r['prior_gains_lost']) for r in rr),new_fp=sum(len(r['new_fp']) for r in rr),
            eligible=all(not any(r[k] for k in ('lost','prior_gains_lost','new_fp','lost_stances','lost_nodes','lost_claims','lost_complete')) and r['extra_increase']<=0 for r in rr))
    selected=next((arm for arm in ('combined','support') if summary[arm]['eligible']),None)
    (OUT/'evaluation.json').write_text(json.dumps(dict(summary=summary,selected=selected,cases=cases),ensure_ascii=False,indent=2))
    print(json.dumps(summary),selected)

if __name__=='__main__':
    import sys
    main(sys.argv[1])
