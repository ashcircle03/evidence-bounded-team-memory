"""Aggregate explicit source-reviewed ratings; never infer correctness from text."""
import argparse
from collections import Counter
import json
from pathlib import Path


def main(folder):
    result=json.loads((folder/'result.json').read_text())
    ratings=json.loads((folder/'ratings.json').read_text())
    rows={r['case_id']+'/'+r['label']:r for r in result['rows'] if r['request']['operation']=='ask'}
    assert set(rows)==set(ratings) and len(rows)==37
    report=dict(rater='implementation agent; not independent or blinded',splits={})
    for split in ('legacy','streams','transfer'):
        group=[ratings[k] for k,r in rows.items() if r['split']==split]
        for rating in group:
            assert rating['reason'] and all(type(rating[k]) is bool for k in ('answer_correct','source_evidence_complete'))
            assert rating['state_citation_complete'] in (None,True,False)
        report['splits'][split]=dict(total=len(group),
            answer_correct=sum(r['answer_correct'] for r in group),
            answer_and_required_evidence=sum(r['answer_correct'] and r['source_evidence_complete']
                and r['state_citation_complete'] is not False for r in group),
            state_citation_required=sum(r['state_citation_complete'] is not None for r in group),
            state_citation_complete=sum(r['state_citation_complete'] is True for r in group))
    calls=[json.loads(s) for s in (folder/'calls.jsonl').read_text().splitlines()]
    usage=Counter()
    for c in calls:
        for key,value in c['response'].get('usage',{}).items():
            if isinstance(value,int):usage[key]+=value
    report.update(physical_calls=len(calls),tokens=dict(usage),
        response_statuses=dict(Counter(r['result']['status'] for r in rows.values())),
        program_seconds=result['seconds'])
    (folder/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);main(p.parse_args().folder)
