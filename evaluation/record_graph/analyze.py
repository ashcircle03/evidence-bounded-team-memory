"""Mechanical preservation and provisional role-coverage; not semantic precision."""
import argparse
from collections import Counter
import json
from pathlib import Path
from team_memory.records.graph import validate_graph,linked_span,construct


def role_coverage(source,requirements):
    graph=source['record_graph'];units={u['id']:u for u in graph['units']};rows=[]
    for requirement in requirements:
        if requirement['claim'] not in source['text']:continue
        matched=[c for c in graph['claims'] if requirement['claim'] in ' '.join(units[uid]['quote'] for uid in c['claim'])]
        results=[]
        for c in matched:
            checks={}
            for role,anchors in requirement.items():
                if role=='claim':continue
                if role=='stance':checks[role]=c['stance'] in anchors
                else:
                    text=' '.join(units[uid]['quote'] for uid in c[role])
                    checks[role]=all(anchor in text for anchor in anchors)
            results.append(dict(claim_id=c['id'],checks=checks))
        rows.append(dict(anchor=requirement['claim'],claim_found=bool(matched),candidates=results,
                         required_links_present=any(all(r['checks'].values()) for r in results)))
    return rows


def analyze(inputs,key,result=None):
    saved={} if result is None else {s['id']:s for s in result['sources']}
    rows=[]
    for case in inputs['cases']:
        for source in case['sources']:
            linked=saved.get(source['id'])
            window=construct(source)
            row=dict(case_id=case['id'],source_id=source['id'],origin=case['origin'],
                     model_extraction='not_run' if linked is None else linked['record_graph']['status'],
                     source_preserved=None if linked is None else {k:v for k,v in linked.items() if k!='record_graph'}==source,
                     required_role_coverage=None if linked is None else role_coverage(linked,key['requirements'][case['id']]),probes=[])
            if linked is not None:validate_graph(linked,linked['record_graph'])
            for r in key['requirements'][case['id']]:
                if r['claim'] not in source['text']:continue
                a=source['text'].index(r['claim']);b=a+len(r['claim'])
                bounds={'isolated_span':(a,b),'reference_window':linked_span(window,a,b)}
                if linked is not None:bounds['linked_graph']=linked_span(linked,a,b)
                expected=[anchor for role,anchors in r.items() if role not in ('claim','stance') for anchor in anchors]
                row['probes'].append(dict(anchor=r['claim'],expected=expected,arms={arm:dict(start=lo,end=hi,
                    contained=[anchor for anchor in expected if anchor in source['text'][lo:hi]]) for arm,(lo,hi) in bounds.items()}))
            rows.append(row)
    return dict(scope='diagnostic span/role availability; not claim truth, QA accuracy, or independent benchmark',
                semantic_precision=None,semantic_review_required=True,fresh_model_output_present=result is not None,
                source_statuses=dict(Counter(r['model_extraction'] for r in rows)),rows=rows)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inputs',type=Path,default=Path('evaluation/record_graph/inputs.json'))
    p.add_argument('--key',type=Path,default=Path('evaluation/record_graph/key.json'))
    p.add_argument('--result',type=Path)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();report=analyze(json.loads(a.inputs.read_text()),json.loads(a.key.read_text()),None if a.result is None else json.loads(a.result.read_text()))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('scope','source_statuses','fresh_model_output_present')},ensure_ascii=False))
