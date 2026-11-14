"""Compare frozen boundary run to v3b; carry ratings only for identical outputs."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path


def main():
    repo=Path(__file__).resolve().parents[2]
    base=repo/'results/service-completion/v3b';folder=repo/'results/module-boundary/v1'
    old=json.loads((base/'result.json').read_text());new=json.loads((folder/'result.json').read_text())
    assert new['status']=='complete'
    def asks(result):return {r['case_id']+'/'+r['label']:r for r in result['rows'] if r['request']['operation']=='ask'}
    left,right=asks(old),asks(new)
    assert set(left)==set(right) and len(right)==37
    comparison={k:dict(request_identical=left[k]['request']==r['request'],
        answer_text_identical=left[k]['result'].get('raw')==r['result'].get('raw'),
        answers_and_evidence_identical=left[k]['result'].get('answers')==r['result'].get('answers'))
        for k,r in right.items()}
    def calls(path):
        return Counter(json.dumps(dict(context=x['context'],request=x['request']),sort_keys=True)
                       for x in map(json.loads,path.read_text().splitlines()))
    same_calls=calls(base/'calls.jsonl')==calls(folder/'calls.jsonl')
    relation_cases={}
    for r in new['rows']:
        if r['request']['operation']!='ingest':continue
        prior=next(p for p in old['rows'] if (p['case_id'],p['label'])==(r['case_id'],r['label']))
        relation_cases[r['case_id']]=dict(status=r['result']['status'],
            kinds=[p['kind'] for p in r['result']['proposals']],
            proposals_identical=prior['result']['proposals']==r['result']['proposals'])
    report=dict(scope='Exact regression comparison; not independent semantic adjudication',
        qa=comparison,model_requests_identical_as_multiset=same_calls,relations=relation_cases)
    (folder/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
    # A changed answer/evidence must be inspected; never copy a rating by case ID alone.
    changed=[k for k,v in comparison.items() if not all(v.values())]
    assert not changed, 'Manual original-source rating required: '+str(changed)
    ratings=deepcopy(json.loads((base/'ratings.json').read_text()))
    for rating in ratings.values():
        rating['reason']='Fresh Qwen answer text and complete answer/evidence objects equal v3b. Prior source-based judgment: '+rating['reason']
    (folder/'ratings.json').write_text(json.dumps(ratings,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(identical_qa=len(comparison),identical_request_multiset=same_calls,
        identical_proposal_sets=sum(v['proposals_identical'] for v in relation_cases.values())),indent=2))


if __name__=='__main__':main()
