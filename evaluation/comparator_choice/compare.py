"""Pair exact comparator inputs and aggregate source-reviewed relation ratings."""
import json
from pathlib import Path
from .prepare import ROOT,HERE,write


def main():
    root=ROOT/'results/comparator-choice'
    data={arm:json.loads((root/('compare-'+arm+'-v1')/'result.json').read_text()) for arm in ('8b','14b')}
    records={arm:{r['case_id']:r for r in x['selectors']} for arm,x in data.items()}
    assert set(records['8b'])==set(records['14b']) and len(records['8b'])==31
    for cid in records['8b']:
        for field in ('system','content'):assert records['8b'][cid][field]==records['14b'][cid][field],(cid,field)
    old=json.loads((ROOT/'results/module-boundary/v1/result.json').read_text())
    baseline={r['case_id']:r['result'] for r in old['rows'] if r['request']['operation']=='ingest'}
    replay={r['case_id']:r['result'] for r in data['8b']['rows'] if r['request']['operation']=='ingest'}
    preserved={cid:all(baseline[cid][f]==replay[cid][f] for f in ('proposals','receipt')) for cid in baseline}
    baseline_cfg=json.loads((ROOT/'results/module-boundary/v1/freeze.json').read_text())['config']
    for arm in ('8b','14b'):
        cfg=json.loads((root/('compare-'+arm+'-v1')/'freeze.json').read_text())['config']
        assert all(cfg['code_sha256'][n]==h for n,h in baseline_cfg['code_sha256'].items() if n.startswith('team_memory/'))
    summary=dict(exact_paired_comparison_inputs=31,known8b_proposals_and_receipts_equal_prior=preserved,
        prior_qa_reference='results/module-boundary/v1/result.json; actual8B job120445',
        checkpoints='Qwen3-8B vs Qwen2.5-14B-Instruct; not parameter-count-only effect',models={})
    expected=json.loads((HERE/'new-key.json').read_text())['cases']
    for arm in ('8b','14b'):
        p=root/('compare-'+arm+'-v1');ratings=json.loads((p/'relation-ratings.json').read_text())
        assert set(ratings)==set(expected) and all(r['reason'] for r in ratings.values())
        counts={kind:dict(correct=sum(r['correct'] for r in ratings.values() if r['expected']==kind),total=4)
                for kind in ('reconsider','none','correction','conflict','coexist')}
        counts.update(negative_unnecessary_review=sum(r['review_proposals']>0 for r in ratings.values() if r['expected']=='none'),
            failed_cases=sum(r['failed'] for r in ratings.values()),rater='implementation agent, not independent')
        write(p/'relation-summary.json',counts);summary['models'][arm]=counts
    a,b=[summary['models'][arm] for arm in ('8b','14b')]
    summary['comparator_gate']=(b['reconsider']['correct']>=3 and b['reconsider']['correct']>a['reconsider']['correct']
        and b['negative_unnecessary_review']<=1 and b['negative_unnecessary_review']<=a['negative_unnecessary_review']
        and all(b[k]['correct']>=a[k]['correct'] for k in ('none','correction','conflict','coexist')))
    summary['end_to_end_adoption_not_established_by_this_gate']=True
    write(root/'comparison.json',summary);print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
