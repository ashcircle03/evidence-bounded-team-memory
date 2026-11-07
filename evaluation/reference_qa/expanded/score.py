"""Aggregate explicit per-output semantic ratings; no new thresholds or judges."""
from collections import defaultdict
import json,sys
from pathlib import Path


def main():
    folder=Path(sys.argv[1]);read=lambda n:json.loads((folder/n).read_text())
    cards=read('cards.json');mapping=read('blind-mapping.json');rating_file=read('ratings.json');ratings=rating_file['ratings']
    assert set(ratings)==set(mapping) and rating_file['reviewer']
    fields=['answer_correct','returned_evidence_supports_all_claims','required_evidence_complete','narrow_quotes_support_all_claims','unsupported_extra']
    byid={}
    for bid,r in ratings.items():
        assert r['reason'] and all(isinstance(r[k],bool) for k in fields),bid
        r=dict(r);r['success']=r['answer_correct'] and r['returned_evidence_supports_all_claims'] and r['required_evidence_complete'] and not r['unsupported_extra'];byid[mapping[bid]]=r
    groups=defaultdict(list)
    for cid,c in cards.items():groups[c['split']+'/'+c['arm']].append(cid)
    summary={g:dict(n=len(ids),**{f:sum(byid[k][f] for k in ids) for f in fields+['success']}) for g,ids in groups.items()}
    native_lost=[k for k,c in cards.items() if c['split'] in ['ever','wiki'] and c['arm']=='claims' and byid[k.removesuffix('/claims')+'/joint']['success'] and not byid[k]['success']]
    criteria=dict(legacy20=summary['legacy/claims']['success']==20,
        within_source_both_orders=all(byid['order/'+n+'/claims']['success'] for n in ['forward','reversed']),
        historical_negative_controls=all(byid['transfer/'+n+'/claims']['success'] for n in ['new-conditions','new-unrelated','new-author','new-no-answer']),
        native_no_supported_answer_loss=not native_lost)
    result=dict(summary=summary,criteria=criteria,eligible_for_larger_development=all(criteria.values()),native_regressions=native_lost,
                reviewer=rating_file['reviewer'],independent_human=rating_file['independent_human'],
                limitations='Small development samples, correlated Wiki conditions; QA only. No merge success or full official benchmark claim.')
    (folder/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (folder/'ratings-by-id.json').write_text(json.dumps(byid,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
