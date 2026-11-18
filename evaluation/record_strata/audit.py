"""Post-output diagnostic audit; never changes frozen primary scores or prompts."""
from pathlib import Path
from collections import Counter
import json
from evaluation.record_strata.score import raw_groups,contains,check,norm
from team_memory.records.graph import ROLES

def main(folder,job):
    ev=json.loads((folder/'evaluation.json').read_text());result=json.loads((folder/f'record-strata-{job}.json').read_text())
    keys={x['id']:x for x in json.loads(Path('evaluation/record_strata/keys.json').read_text())['items']}
    items={x['id']:x for x in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']}
    out=dict(scope='Diagnostic only. Primary frozen scores unchanged. n06 exclusion declared before model outputs.',mixed_stance=[],surface_boundary_flags=[],natural_valid_subset=[],cases=[])
    for row,c in zip(result['rows'],ev['cases']):
        key=keys[row['id']];groups=raw_groups(row['raw'])
        try:extractions=json.loads(row['raw'])['extractions']
        except (ValueError,KeyError):extractions=[]
        for g in groups:
            if not contains(g['claim'],key['core']):continue
            matching=[r for r in extractions if 'claim' in r and r['claim_attributes']['claim_group']==g['id'] and contains([r['claim']],key['core'])]
            focal_stances=[r['claim_attributes']['stance'] for r in matching]
            if len(set(g['stances']))>1 and any(s in key.get('acceptable_stances',[key['stance']]) for s in focal_stances):
                out['mixed_stance'].append(dict(id=row['id'],arm=row['arm'],group_id=g['id'],focal_stances=focal_stances,all_stances=g['stances'],compiled_status=row['source']['record_graph']['status'],effect='Mixed group stances collapse to unknown; focal row had expected stance. Not proof all caveat stances are correct.'))
            for slot in key['slots']:
                if slot['role']!='time' or not slot['available']:continue
                words=norm(slot['text']).split()
                if words and words[0] in ('on','at','in') and not contains(g['time'],slot['text']) and contains(g['time'],' '.join(words[1:])):
                    out['surface_boundary_flags'].append(dict(id=row['id'],arm=row['arm'],gold=slot['text'],predicted=g['time'],note='Check manually: a missing preposition need not be missing temporal meaning. Primary metric remains unchanged.'))
        alltexts=[t for g in groups for r in ROLES for t in g[r]]
        required=[v for v in key['slots'] if v['available'] and not v.get('optional')]
        global_recovered=contains(alltexts,key['core']) and all(contains(alltexts,v['text']) for v in required)
        d=c['raw'];cause=[]
        if global_recovered and not d['visible_recovered']:cause.append('visible_content_present_elsewhere_but_not_bound_to_focal_claim')
        if not d['target_found']:cause.append('focal_anchor_not_in_raw_claim_group')
        elif not d['visible_recovered']:cause.append('visible_qualifier_not_recovered_in_focal_group')
        elif not d['typed_complete']:cause.append('content_retained_but_typed_role_missing')
        if d['target_found'] and not d['stance_ok']:cause.append('group_stance_incorrect_or_mixed')
        if d['unsupported_completion']:cause.append('withheld_value_completed_without_support')
        if d['wrong_target']:cause.append('foil_linked_to_focal_claim')
        if c['compile_error']:cause.append('compiler_rejected_source')
        if not c['transport']['stored_restarted']:cause.append('persistent_transport_failure')
        if c['finish_reason']=='length':cause.append('generation_token_limit')
        out['cases'].append(dict(id=row['id'],arm=row['arm'],global_visible_recovered=global_recovered,causes=cause))
    for arm in ('simple','ours'):
        cs=[c for c in ev['cases'] if c['panel']=='natural_audit' and c['id']!='n06' and c['arm']==arm]
        out['natural_valid_subset'].append(dict(arm=arm,n=len(cs),raw_passed=sum(c['raw']['passed'] for c in cs),compiled_passed=sum(c['compiled']['passed'] for c in cs),raw_visible_recovered=sum(c['raw']['visible_recovered'] for c in cs),raw_typed_complete=sum(c['raw']['typed_complete'] for c in cs)))
    out['availability_pairs']=[]
    for arm in ('simple','ours'):
        for fid in sorted({c['family'] for c in ev['cases'] if c['panel']=='balanced_synthetic'}):
            rows={c['availability']:c for c in ev['cases'] if c['arm']==arm and c['family']==fid}
            out['availability_pairs'].append(dict(arm=arm,family=fid,**{a:dict(raw_passed=rows[a]['raw']['passed'],raw_visible_recovered=rows[a]['raw']['visible_recovered'],compiled_passed=rows[a]['compiled']['passed'],unsupported=rows[a]['raw']['unsupported_completion']) for a in ('full','partial','none')}))
    (folder/'diagnostic-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('mixed_stance','surface_boundary_flags','natural_valid_subset')},ensure_ascii=False,indent=2))
if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]),sys.argv[2])
