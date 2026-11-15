"""Frozen-input comparison; link coverage is distinct from reason qualification."""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import tempfile
from evaluation.record_groups.evaluate import probe, covers, linked_text, transport
from team_memory.records import grouped
from team_memory.records.graph import ROLES


def reason_check(source, p, index, policy):
    graph=source['record_graph'];units={u['id']:u for u in graph['units']};matches=[]
    expected='stated' if index in policy['stated_probes'] else 'inferred' if index in policy['inferred_only_if_present'] else None
    for c in graph['claims']:
        if not covers(source['text'],p['anchor'],[units[x] for x in c['claim']]):continue
        bykind=defaultdict(list)
        for a in c['basis_annotations']:bykind[a['kind']].append(units[a['unit_id']])
        checks=[]
        for premise in p['basis']:
            present=covers(source['text'],premise,[units[x] for x in c['basis']])
            kinds=[k for k,us in bykind.items() if covers(source['text'],premise,us)]
            checks.append(dict(premise=premise,present=present,kinds=kinds,correct_kind=present and expected in kinds if expected else None,
                falsely_stated=expected=='inferred' and covers(source['text'],premise,bykind['stated'])))
        matches.append(dict(claim_id=c['id'],premises=checks))
    return dict(probe_index=index,expected=expected,matched=matches,
        recovered_with_expected_kind=bool(expected) and any(m['premises'] and all(x['correct_kind'] for x in m['premises']) for m in matches),
        false_stated=any(x['falsely_stated'] for m in matches for x in m['premises']))


def main(folder,job):
    load=lambda p:json.loads(p.read_text())
    freeze=load(folder/'freeze.json');result=load(folder/f'record-contract-{job}.json');server=load(folder/f'sm-{job}.json')
    assert result['status']==server['status']=='complete' and server['client_exit_code']==0
    assert result['code_sha256']==freeze['code_sha256'] and result['data_sha256']==freeze['data_sha256']
    cfg=load(folder/'config.json');assert result['model_revision']==server['revision']==cfg['model_revision']
    for name,expected in freeze['code_sha256'].items():assert sha256(Path(name).read_bytes()).hexdigest()==expected,name
    inputs=Path('evaluation/record_contract/inputs.json');key=Path('evaluation/record_contract/key.json')
    assert sha256(inputs.read_bytes()).hexdigest()==freeze['data_sha256']['inputs.json']
    assert sha256(key.read_bytes()).hexdigest()==freeze['key_sha256']
    data=load(inputs);keys=load(key);original={x['source']['id']:x for x in data['sources']}
    old=load(Path('evaluation/record_groups/inputs.json'))
    assert [x['source'] for x in old['sources']]==[x['source'] for x in data['sources']]
    assert keys['probes']==load(Path('evaluation/record_groups/key.json'))['probes']
    calls=[json.loads(x) for x in (folder/f'record-contract-{job}.calls.jsonl').read_text().splitlines()]
    assert len(calls)==result['calls']==60 and len(result['rows'])==60
    assert [c['id'] for c in calls]==list(range(1,61))
    expected_order=[(x['source']['id'],a) for x in data['sources'] for a in x['arms']]
    assert [(c['source_id'],c['arm']) for c in calls]==expected_order
    cost=defaultdict(Counter);request_parameters=None;finish=defaultdict(Counter)
    for c,row in zip(calls,result['rows']):
        s=original[c['source_id']]['source'];assert c['arm']==row['arm'] and c['source_id']==row['source']['id']
        captured=[]
        def replay(system,prompt):
            captured.extend([dict(role='system',content=system),dict(role='user',content=prompt)])
            return c['response']['choices'][0]['message']['content']
        reconstructed=grouped.construct_contract(s,replay,model=row['source']['record_graph']['model'],revised_input=c['arm']=='revised')
        assert c['request']['messages']==captured
        assert reconstructed==row['source']
        params={k:v for k,v in c['request'].items() if k!='messages'}
        if request_parameters is None:request_parameters=params
        assert params==request_parameters
        assert params['guided_json']==grouped.output_schema(basis_types=True)
        assert {k:v for k,v in row['source'].items() if k!='record_graph'}==s
        cost[c['arm']].update({k:v for k,v in c['response']['usage'].items() if k in ('prompt_tokens','completion_tokens','total_tokens')})
        cost[c['arm']]['calls']+=1;finish[c['arm']][c['response']['choices'][0]['finish_reason']]+=1
    report=dict(scope='Development partial link probes and typed reasons; not full semantic recall or QA accuracy',job_id=job,
        actual_requests_verified=60,same_sources_verified=30,identical_nonmessage_request_parameters=True,arms={},cost=dict(cost),finish_reason=dict(finish),cases=[],all_claims=[],transport=[])
    protected={(p['source_id'],p['anchor']) for p in keys['protected']}
    with tempfile.TemporaryDirectory(prefix='record-contract-transport-') as tmp:
        for i,row in enumerate(result['rows']):
            s=row['source'];arm=row['arm'];report['transport'].append(dict(arm=arm,source_id=s['id'],**transport(s,Path(tmp)/str(i))))
            for j,p in enumerate(keys['probes']):
                if p['source_id']==s['id']:
                    report['cases'].append(dict(arm=arm,probe_index=j,case_id=original[s['id']]['case_id'],protected=(s['id'],p['anchor']) in protected,
                        reason=reason_check(s,p,j,keys['reason_policy']),**probe(s,p)))
            units={u['id']:u for u in s['record_graph']['units']}
            for c in s['record_graph']['claims']:
                report['all_claims'].append(dict(arm=arm,case_id=original[s['id']]['case_id'],source_id=s['id'],claim_id=c['id'],stance=c['stance'],
                    basis_annotations=[dict(quote=units[a['unit_id']]['quote'],**a) for a in c['basis_annotations']],**{r:linked_text(s,c,r) for r in ROLES}))
    for arm in ('control','revised'):
        rows=[r for r in result['rows'] if r['arm']==arm];ps=[r for r in report['cases'] if r['arm']==arm]
        report['arms'][arm]=dict(sources=len(rows),statuses=dict(Counter(r['source']['record_graph']['status'] for r in rows)),
            claims=sum(len(r['source']['record_graph']['claims']) for r in rows),passed_probes=sum(p['passed'] for p in ps),total_probes=len(ps),
            protected_passed=sum(p['passed'] for p in ps if p['protected']),protected_total=7,
            hard_five_passed=sum(p['passed'] for p in ps if p['probe_index']<5),
            negative_role_violations=sum(p['negative_role_violation'] for p in ps),missing_claim_anchor=sum(not p['matched'] for p in ps),
            qualified_reason_recovery=sum(p['reason']['recovered_with_expected_kind'] for p in ps),
            false_stated_probes=sum(p['reason']['false_stated'] for p in ps),
            protected_regressions=[p['probe_index'] for p in ps if p['protected'] and not p['passed']])
    report['default_adoption']='pending_full_semantic_review' if report['arms']['revised']['protected_passed']==7 else 'blocked_protected_link_regression'
    (folder/'evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('arms','cost','finish_reason','default_adoption')},indent=2))

if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]),sys.argv[2])
