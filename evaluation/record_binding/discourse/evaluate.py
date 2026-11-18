"""Compare persisted candidate and accepted records with the frozen whole-record scorer."""
from collections import Counter
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from evaluation.record_binding.first_loss import read, reader_packets
from evaluation.record_bound.rows import compiled_rows
from evaluation.record_causal.storage import correct_stance_nodes
from evaluation.record_full.evaluate import score
from team_memory.records import discourse_roles, preserving

OUT=Path('results/record-binding/discourse-role')
PACKET=Path('../campaigns/speakermem-dev/source/record-discourse-v1')


def edge_identity(edge,source,rows):
    owner,role,node=edge
    groups=source['record_graph']['claims']
    if owner.startswith('unbound:'):
        claim=next(c for c in groups if c['id']==owner[len('unbound:'):])
        owner='unbound:'+json.dumps(claim['claim'])
    if node.startswith('unmatched:'):
        row=next(r for r in rows if r['id']==int(node.split(':')[-1]))
        claim=next(c for c in groups if c['id']==row['group'])
        node='unmatched:'+json.dumps([claim['claim'],row['text']])
    return owner,role,node


def main(job):
    freeze=read(OUT/'freeze.json')
    for path,expected in freeze.items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==expected,path
    result=read(OUT/f'record-discourse-{job}.json')
    assert result['input_sha256']==freeze[str(PACKET/'pairs.json')]
    assert result['source_sha256']==freeze[str(PACKET/'run.py')]
    assert result['status']=='complete' and result['job']==job
    gold=read('evaluation/record_full/gold.json')['documents']
    items={i['id']:i for i in read(PACKET.parent/'record-pair-v1/inputs.json')}
    input_pairs={i['id']:i['pairs'] for i in read(PACKET/'pairs.json')}
    preds={r['id']:r['decisions'] for r in result['rows']}
    old={r['id']:r['score'] for r in read('results/record-binding/v4/pair-evaluation.json')['cases'] if r['arm']=='baseline'}
    assert set(preds)==set(items)==set(input_pairs)==set(old) and len(preds)==len(result['rows'])==68
    cases=[]
    with TemporaryDirectory() as tmp:
        for doc in gold:
            iid=doc['id'];item=items[iid];source=item['source'];raw=item['original_raw']
            pairs=discourse_roles.candidates(source,raw);assert pairs==input_pairs[iid]
            assert [p['index'] for p in pairs]==[p['index'] for p in preds[iid]]
            decisions=[p['decision'] for p in preds[iid]]
            for p in preds[iid]:
                choices=['keep','condition','basis'];label=choices[max(range(3),key=p['probs'].__getitem__)]
                threshold=result['calibration'].get(label,{}).get('threshold')
                assert p['argmax']==label and p['decision']==(label if threshold is not None and max(p['probs'])>=threshold else 'keep')
            base=preserving.compile_graph(source,raw,model='same-original')
            graph=discourse_roles.apply(source,raw,lambda _:decisions,model='discourse-role-v1')
            assert graph['units']==base['units'] and graph['status']==base['status']
            assert [[c['assertions'],c['stance']] for c in graph['claims']]==[[c['assertions'],c['stance']] for c in base['claims']]
            scores=[];bad=[];stances=[];extras=[]
            for g in (base,graph):
                enriched=dict(source,record_graph=g);rows=compiled_rows(enriched);s=score(rows,doc,source)
                scores.append(s);stances.append(correct_stance_nodes(rows,doc))
                bad.append({edge_identity(e,enriched,rows) for e in s['incorrect_edges']})
                extras.append(Counter((row['role'],row['text']) for row in s['extra_rows']))
            before,after=scores
            assert json.loads(json.dumps(before))==old[iid]
            packets=reader_packets(dict(source,record_graph=graph),Path(tmp)/iid)
            before_missing=set(before['missing_edges']);after_missing=set(after['missing_edges'])
            cases.append(dict(id=iid,panel=doc['panel'],pairs=[dict(**p,prediction=q) for p,q in zip(pairs,preds[iid])],
                changed=sum(q!='keep' and q!=p['old_role'] for p,q in zip(pairs,decisions)),
                recovered=sorted(before_missing-after_missing),lost=sorted(after_missing-before_missing),
                new_fp=sorted(bad[1]-bad[0]),removed_fp=sorted(bad[0]-bad[1]),lost_content=sorted(set(after['missing_nodes'])-set(before['missing_nodes'])),
                lost_claims=sorted(set(after['missing_claims'])-set(before['missing_claims'])),lost_stances=sorted(stances[0]-stances[1]),
                new_extras=list((extras[1]-extras[0]).elements()),reader_groups=len(packets),
                lost_complete=before['complete'] and not after['complete'],before=before,after=after))
    accepted=any(c['recovered'] for c in cases) and not any(
        any(c[k] for k in ('lost','new_fp','lost_content','lost_claims','lost_stances','lost_complete','new_extras')) for c in cases)
    out=dict(accepted=accepted,cases=cases)
    (OUT/'evaluation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print('Accepted',accepted)
    for arm in ('before','after'):
        print(arm,[sum(c[arm]['typed_edges'][k] for c in cases) for k in ('tp','fp')],sum(c[arm]['complete'] for c in cases))
    for c in cases:
        if c['changed'] or c['id'] in ('n03','n08'):
            print(c['id'],c['changed'],c['recovered'],c['lost'],c['new_fp'],[(p['old_role'],p['prediction']) for p in c['pairs']])

if __name__=='__main__':
    import sys
    main(sys.argv[1])
