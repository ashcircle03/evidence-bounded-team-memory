"""Trace every evaluated failure to input, actual Qwen output and storage."""
import json
from pathlib import Path
from hashlib import sha256
from collections import Counter

from team_memory.records import grouped, bound
from evaluation.record_full.evaluate import score, raw_rows
from evaluation.record_bound.rows import raw_rows as bound_rows, compiled_rows


def main():
    out=Path('results/record-causal/v1')
    inputs={x['id']:x['source'] for x in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']}
    gold={x['id']:x for x in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    artifacts=[('grouped','results/record-strata/v1/record-strata-122970'),('bound','results/record-bound/v1/record-bound-122986')]
    traces=[]
    for name,prefix in artifacts:
        result=json.loads(Path(prefix+'.json').read_text())
        calls=[json.loads(l) for l in Path(prefix+'.calls.jsonl').read_text().splitlines()]
        for row in result['rows']:
            if name=='grouped' and row['arm']!='ours':continue
            iid=row['id'];source=inputs[iid]
            call=next(c for c in calls if c['item_id']==iid and (name=='bound' or c['arm']=='ours'))
            assert call['response']['choices'][0]['message']['content']==row['raw']
            if name=='grouped':
                gen,_=grouped.components()
                prompt=gen.render(source['text'],additional_context=json.dumps({k:source[k] for k in ('id','owner','speaker','observed_at','location')},ensure_ascii=False))
                assert call['request']['messages']==[{'role':'system','content':'Extract grounded records using the supplied format and examples.'},{'role':'user','content':prompt}]
                assert call['request']['guided_json']==grouped.output_schema(basis_types=True)
                rr=raw_rows(row['raw'])
            else:
                assert call['request']['messages']==[{'role':'system','content':bound.SYSTEM},{'role':'user','content':bound.prompt(source)}]
                rr=bound_rows(row['raw'])
            raw=score(rr,gold[iid],source);stored=score(compiled_rows(row['source']),gold[iid],source)
            storage_nodes=sorted(set(stored['missing_nodes'])-set(raw['missing_nodes']))
            storage_edges=sorted(set(map(tuple,stored['missing_edges']))-set(map(tuple,raw['missing_edges'])))
            trace=dict(id=iid,arm=name,source=source,request=call['request'],raw=row['raw'],
                       finish_reason=call['response']['choices'][0]['finish_reason'],
                       raw_sha256=sha256(row['raw'].encode()).hexdigest(),
                       raw_score=raw,stored_score=stored,
                       first_observed=dict(already_missing_in_raw=raw['missing_nodes'],already_missing_links_in_raw=raw['missing_edges'],
                         wrong_links_in_raw=raw['incorrect_edges'],extra_rows_in_raw=raw['extra_rows'],
                         storage_lost_nodes=storage_nodes,storage_lost_links=storage_edges,
                         storage_changed_stance=[x for x in stored['stance_wrong'] if x not in raw['stance_wrong']]),
                       storage_status=row['source']['record_graph']['status'],storage_errors=row['source']['record_graph']['errors'])
            if name=='bound':
                segs=bound.segments(source)
                trace['single_quote_boundary_risks']=[n['id'] for n in gold[iid]['nodes'] if n['required'] and n['text'] in source['text'] and not any(n['text'] in s['text'] for s in segs)]
                trace['boundary_interpretation']='One quote cannot express these full spans in the old sentence schema; multi-span reconstruction may still be possible. This is a representation risk, not proof of sole cause.'
            traces.append(trace)
    (out/'failure-traces.json').write_text(json.dumps(traces,ensure_ascii=False,indent=2)+'\n')
    lines=['# Failure location audit','','Every row links to actual original model JSON and storage scores in `failure-traces.json`. Missing content and missing links are separate. “Raw” errors are observed before storage; this does not prove a model-capacity limit.','','| ID | Arm | Raw missing content | Raw missing links | Raw wrong links | Raw extra rows | Storage lost content | Storage lost links | Storage status |','|---|---|---:|---:|---:|---:|---:|---:|---|']
    for t in traces:
        r=t['raw_score'];f=t['first_observed']
        lines.append(f"| {t['id']} | {t['arm']} | {len(r['missing_nodes'])} | {len(r['missing_edges'])} | {len(r['incorrect_edges'])} | {len(r['extra_rows'])} | {len(f['storage_lost_nodes'])} | {len(f['storage_lost_links'])} | {t['storage_status']} |")
    (out/'failure-index.md').write_text('\n'.join(lines)+'\n')
    print('actual requests and raw outputs verified',len(traces))


if __name__=='__main__':main()
