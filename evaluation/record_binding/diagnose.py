"""Locate native prediction vs adapter losses; supplemental to unchanged scoring."""
from pathlib import Path
import json
from evaluation.record_full.evaluate import score,metric,raw_rows


def rows(prediction):
    result=[]
    for i,r in enumerate(prediction.get('statement',[])):
        if not isinstance(r.get('claim'),dict):continue
        result.append(dict(id=len(result),role='claim',text=r['claim']['text'],group=str(i),stance='unknown'))
        for role in ('condition','basis'):
            for v in r.get(role,[]):result.append(dict(id=len(result),role=role,text=v['text'],group=str(i),stance='unknown'))
    return result


def main(job):
    out=Path('results/record-binding/v1');gold={d['id']:d for d in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    qwen={r['id']:r for r in json.loads(Path('results/record-strata/v1/record-strata-122970.json').read_text())['rows'] if r['arm']=='ours'}
    predictions={arm:{r['id']:r for r in json.loads((out/file).read_text())['rows']} for arm,file in [('native','record-binding-122996.json'),('adapted',f'record-adapt-{job}.json')]}
    cases=[]
    for iid,d in gold.items():
        source=qwen[iid]['source']
        for arm in ('qwen_raw','native','adapted'):
            rr=raw_rows(qwen[iid]['raw']) if arm=='qwen_raw' else rows(predictions[arm][iid]['prediction'])
            s=score(rr,d,source);expected={tuple(e) for e in d['edges'] if e[1] in ('condition','basis')}
            missing={tuple(e) for e in s['missing_edges'] if e[1] in ('condition','basis')}
            incorrect={tuple(e) for e in s['incorrect_edges'] if e[1] in ('condition','basis')}
            cases.append(dict(id=iid,panel=d['panel'],arm=arm,target_links=metric(len(expected-missing),len(incorrect),len(missing)),correct_target_edges=sorted(expected-missing),missing_target_edges=sorted(missing),incorrect_target_edges=sorted(incorrect),content=s['content_recall']))
    summary=[]
    for panel in ('balanced_synthetic','natural_audit'):
        for arm in ('qwen_raw','native','adapted'):
            ss=[c for c in cases if c['panel']==panel and c['arm']==arm]
            summary.append(dict(panel=panel,arm=arm,target_links=metric(*(sum(c['target_links'][k] for c in ss) for k in ('tp','fp','fn')))))
    report=dict(interpretation='Supplemental condition/basis-only slice of unchanged scorer. Native stances intentionally unknown; no claim of complete-record or QA success.',cases=cases,summary=summary)
    (out/'native-stage-diagnosis.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    import sys
    main(sys.argv[1])
