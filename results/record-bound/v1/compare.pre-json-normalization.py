"""Apply fixed full-record gold/scorer and predeclared item-preservation gate."""
from pathlib import Path
from hashlib import sha256
from collections import Counter,defaultdict
import json
from evaluation.record_full.evaluate import score,metric,raw_rows as old_raw,compiled_rows as old_compiled
from evaluation.record_bound.rows import raw_rows,compiled_rows
from team_memory.records import bound,graph


def main(job):
    out=Path('results/record-bound/v1');freeze=json.loads((out/'freeze.json').read_text())
    for table in ('frozen_evaluation_files','adapter_files'):
        for n,h in freeze[table].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
    for n,h in freeze['code_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
    result=json.loads((out/f'record-bound-{job}.json').read_text());server=json.loads((out/f'sm-{job}.json').read_text())
    assert result['status']==server['status']=='complete' and server['client_exit_code']==0
    assert result['code_sha256']==freeze['code_sha256'] and result['data_sha256']==freeze['data_sha256']
    calls=[json.loads(x) for x in (out/f'record-bound-{job}.calls.jsonl').read_text().splitlines()];assert len(calls)==len(result['rows'])==result['calls']==68
    inputs={x['id']:x for x in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']};gold={x['id']:x for x in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    legacy=json.loads(Path('results/record-strata/v1/record-strata-122970.json').read_text())
    cases=[];cost=Counter()
    for i,(call,row) in enumerate(zip(calls,result['rows'])):
        source=inputs[row['id']]['source'];b=call['request'];assert call['id']==i+1 and call['item_id']==row['id']
        expected=dict(model='Qwen3-8B',messages=[dict(role='system',content=bound.SYSTEM),dict(role='user',content=bound.prompt(source))],temperature=0,max_tokens=2048,chat_template_kwargs=dict(enable_thinking=False),seed=42,guided_json=bound.schema(len(bound.segments(source))))
        assert b==expected
        assert call['response']['choices'][0]['message']['content']==row['raw']
        reconstructed=bound.compile_graph(source,row['raw'],row['source']['record_graph']['model']);assert reconstructed==row['source']['record_graph'];graph.validate_graph(source,reconstructed)
        assert {k:v for k,v in row['source'].items() if k!='record_graph'}==source
        cost.update({k:v for k,v in call['response']['usage'].items() if k in ('prompt_tokens','completion_tokens','total_tokens')})
        row['finish_reason']=call['response']['choices'][0]['finish_reason']
    for row in legacy['rows']+result['rows']:
        d=gold[row['id']];source=row['source'];is_new=row['arm']=='bound'
        if is_new:
            try:rr=raw_rows(row['raw'])
            except (ValueError,KeyError,TypeError):rr=[]
        else:rr=old_raw(row['raw']);assert compiled_rows(source)==old_compiled(source)
        cases.append(dict(id=row['id'],arm=row['arm'],panel=d['panel'],difficulty=d['difficulty'],availability=d['availability'],raw=score(rr,d,source),compiled=score(compiled_rows(source),d,source),status=source['record_graph']['status'],transport=row['transport'],diagnostics=source['record_graph'].get('diagnostics',[]),finish_reason=row.get('finish_reason')))
    # Exactly reproduce old scores: representation and criterion not changed.
    old_eval=json.loads(Path('results/record-full/v3/evaluation.json').read_text())
    for c in cases[:136]:
        e=next(e for e in old_eval['cases'] if e['id']==c['id'] and e['arm']==c['arm'])
        assert c['raw']==e['raw'] and c['compiled']==e['compiled'],(c['id'],c['arm'])
    summaries=[]
    for panel in ('balanced_synthetic','natural_audit'):
        for arm in ('simple','ours','bound'):
            for stage in ('raw','compiled'):
                for diff,av in [('all','all')]+([(d,a) for d in ('easy','medium','hard') for a in ('full','partial','none')] if panel=='balanced_synthetic' else []):
                    cs=[c[stage] for c in cases if c['panel']==panel and c['arm']==arm and(diff=='all' or(c['difficulty']==diff and c['availability']==av))]
                    metrics={k:metric(*(sum(c[k][z] for c in cs) for z in ('tp','fp','fn'))) for k in ('content_recall','claim_recall','typed_edges')}
                    summaries.append(dict(panel=panel,arm=arm,stage=stage,difficulty=diff,availability=av,n=len(cs),metrics=metrics,complete=sum(c['complete'] for c in cs),extra_rows=sum(len(c['extra_rows']) for c in cs),boilerplate_rows=sum(len(c['boilerplate_rows']) for c in cs),overmerged_pairs=sum(len(c['overmerged_record_pairs']) for c in cs),stance_wrong=sum(len(c['stance_wrong']) for c in cs),stance_missing=sum(c['stance_missing'] for c in cs)))
    preservation=[]
    for iid in inputs:
        old=next(c for c in cases if c['id']==iid and c['arm']=='ours')['compiled'];new=next(c for c in cases if c['id']==iid and c['arm']=='bound')['compiled'];d=gold[iid]
        required={n['id'] for n in d['nodes'] if n['required']};expected={tuple(e) for e in d['edges']}
        old_nodes=required-set(old['missing_nodes']);new_nodes=required-set(new['missing_nodes'])
        old_edges=expected-{tuple(e) for e in old['missing_edges']};new_edges=expected-{tuple(e) for e in new['missing_edges']}
        preservation.append(dict(id=iid,protected_nodes=len(old_nodes),retained_nodes=len(old_nodes&new_nodes),lost_nodes=sorted(old_nodes-new_nodes),new_nodes=sorted(new_nodes-old_nodes),protected_edges=len(old_edges),retained_edges=len(old_edges&new_edges),lost_edges=sorted(old_edges-new_edges),new_edges=sorted(new_edges-old_edges),old_complete=old['complete'],new_complete=new['complete']))
    def f1(panel,arm):return next(s['metrics']['typed_edges']['f1'] for s in summaries if s['panel']==panel and s['arm']==arm and s['stage']=='compiled' and s['difficulty']=='all')
    checks=dict(protected_nodes_preserved=all(not r['lost_nodes'] for r in preservation),protected_edges_preserved=all(not r['lost_edges'] for r in preservation),complete_documents_preserved=all(not r['old_complete'] or r['new_complete'] for r in preservation),source_integrity=True,transport=all(r['transport']['stored_restarted'] for r in result['rows']),nondecreasing_relation_f1=all(f1(p,'bound')>=f1(p,'ours') for p in ('balanced_synthetic','natural_audit')),improved_relation_f1=any(f1(p,'bound')>f1(p,'ours') for p in ('balanced_synthetic','natural_audit')))
    report=dict(job_id=job,status='verified',old_scores_exactly_reproduced=136,frozen_criteria_unchanged=True,new_calls=68,cached_control_calls=136,cost=dict(cost),adopt_default=all(checks.values()),gate=checks,preservation=preservation,summary=summaries,cases=cases)
    (out/'evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(gate=checks,adopt=report['adopt_default'],cost=dict(cost)),indent=2))
    for s in summaries:
        if s['difficulty']=='all' and s['arm']!='simple':print(json.dumps(s))
if __name__=='__main__':
    import sys
    main(sys.argv[1])
