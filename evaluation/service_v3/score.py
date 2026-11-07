"""Apply precommitted engineering gate to source-reviewed per-case ratings."""
import json,sys
from pathlib import Path


def main(folder):
    result=json.loads((folder/'result.json').read_text())
    mapping=json.loads((folder/'blind-mapping.json').read_text())
    ratings=json.loads((folder/'ratings.json').read_text())
    assert set(ratings)==set(mapping)
    by={}
    for rid,r in ratings.items():
        assert all(isinstance(r[k],bool) for k in ['answer_correct','source_supported','unsupported_state'])
        assert r['reason'].strip()
        m=mapping[rid];by.setdefault(m['case_id'],{})[m['arm']]=dict(r,split=m['split'])
    good=lambda r:r['answer_correct'] and r['source_supported']
    totals={};wins=[];losses=[];extra_state=[]
    for arm in ['direct','attributed']:
        totals[arm]={}
        for split in ['ever','wiki','stream','legacy']:
            rows=[pair[arm] for pair in by.values() if pair[arm]['split']==split]
            totals[arm][split]=dict(n=len(rows),answer=sum(r['answer_correct'] for r in rows),supported=sum(good(r) for r in rows),
                unsupported_state=sum(r['unsupported_state'] for r in rows))
        physical=[r for r in result['rows'] if r['arm']==arm and r['split']!='legacy']
        totals[arm]['new_calls']=sum(r['calls'] for r in physical)
        totals[arm]['new_seconds']=sum(r['seconds'] for r in physical)
    for cid,pair in by.items():
        if pair['direct']['split']=='legacy':continue
        if good(pair['attributed']) and not good(pair['direct']):wins.append(cid)
        if good(pair['direct']) and not good(pair['attributed']):losses.append(cid)
        if pair['attributed']['unsupported_state'] and not pair['direct']['unsupported_state']:extra_state.append(cid)
    gates=dict(net_supported_gain_at_least_two=len(wins)-len(losses)>=2,no_supported_losses=not losses,
        no_added_unsupported_state=not extra_state,call_ratio_at_most_two=totals['attributed']['new_calls']<=2*totals['direct']['new_calls'])
    legacy_losses=[cid for cid,pair in by.items() if pair['direct']['split']=='legacy' and not good(pair['direct'])]
    out=dict(totals=totals,wins=wins,losses=losses,extra_unsupported_state=extra_state,gates=gates,
        selected='attributed' if all(gates.values()) else 'direct',
        direct_legacy_not_supported=legacy_losses,
        global_replacement_supported=all(gates.values()) or not legacy_losses,
        limitations='Small selected natural QA and authored streams; implementation-agent ratings; no significance/full benchmark claim. Shared reconsideration scored separately.')
    (folder/'decision.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':main(Path(sys.argv[1]))
