"""Partial role-binding probes and actual storage/reader-packet transport.

Neither successful alignment nor partial requirements measure full semantic recall.
"""
from collections import Counter,defaultdict
from hashlib import sha256
import json
from pathlib import Path
import tempfile
from team_memory.records.graph import validate_graph,linked_span,describe,ROLES
from team_memory.adapters.records import RecordsAdapter
from team_memory.adapters.base import request
from team_memory.adapters.reader_bridge import evidence_from,witnesses_from
from team_memory.contracts.ports import CallContext


def covers(text,needle,units):
    starts=[];i=text.find(needle)
    while i>=0:
        starts.append(i);i=text.find(needle,i+1)
    return any(all(any(u['start']<=p<u['end'] for u in units) for p in range(a,a+len(needle)) if not text[p].isspace()) for a in starts)


def linked_text(source,claim,role):
    selected={x for x in claim[role]};spans=[]
    for u in source['record_graph']['units']:
        if u['id'] not in selected:continue
        if spans and not source['text'][spans[-1][1]:u['start']].strip():spans[-1][1]=u['end']
        else:spans.append([u['start'],u['end']])
    return [source['text'][a:b] for a,b in spans]


def probe(source,p):
    g=source['record_graph'];units={u['id']:u for u in g['units']};matches=[]
    for c in g['claims']:
        if not covers(source['text'],p['anchor'],[units[x] for x in c['claim']]):continue
        checks={}
        for role in ('condition','basis'):
            checks[role]=all(covers(source['text'],s,[units[x] for x in c[role]]) for s in p[role])
        checks['absent']=all(not c[r] for r in p['absent'])
        checks['no_forbidden']=not any(covers(source['text'],s,[units[x] for r in ('condition','basis') for x in c[r]]) for s in p['forbidden'])
        matches.append(dict(claim_id=c['id'],checks=checks,passed=all(checks.values())))
    return dict(**p,source_status=g['status'],matched=matches,passed=bool(matches) and any(m['passed'] for m in matches),
                negative_role_violation=any(not m['checks']['absent'] or not m['checks']['no_forbidden'] for m in matches))


def transport(source,root):
    sid=source['id'];g=source['record_graph'];validate_graph(source,g)
    ctx=CallContext('groups','importer',frozenset(['records:read','records:write','records:import']))
    port=RecordsAdapter(root,'groups')
    result=port.handle(request('record.append',dict(source=source,expected_revision=0,idempotency_key=sid),workspace_id='groups',request_id=sid),context=ctx)
    assert result['status']=='ok',result
    snap=RecordsAdapter(root,'groups').snapshot();assert snap['sources']==[source]
    count=0
    for c in g['claims']:
        u=next(u for u in g['units'] if u['id']==c['claim'][0]);a,b=linked_span(source,u['start'],u['end'])
        e=evidence_from(dict(source_id=sid,start=a,end=b,quote=source['text'][a:b]),snap,1)
        bundle=dict(snapshot=snap,query=dict(text='transport only',time_scope='current',as_of=None,conditions=[]),evidence=[e],coverage='hits',unresolved_proposal_ids=[])
        w=witnesses_from(bundle)[0];expected=describe(source,a,b)
        assert w['record_context']==expected
        assert w['speaker']==source['speaker'] and w['observed_at']==source['observed_at']
        # Every linked role span must be inside the delivered original interval.
        units={u['id']:u for u in g['units']}
        assert all(a<=units[x]['start']<units[x]['end']<=b for r in ROLES for x in c[r])
        count+=1
    return dict(stored_restarted=True,claim_packets=count,source_status=g['status'])


def main(folder,job):
    load=lambda p:json.loads(p.read_text())
    freeze=load(folder/'freeze.json');result=load(folder/f'record-groups-{job}.json');server=load(folder/f'sm-{job}.json')
    assert result['status']==server['status']=='complete' and server['client_exit_code']==0
    assert result['code_sha256']==freeze['code_sha256'] and result['data_sha256']==freeze['data_sha256']
    inputs=Path('evaluation/record_groups/inputs.json');key=Path('evaluation/record_groups/key.json')
    assert sha256(inputs.read_bytes()).hexdigest()==freeze['data_sha256']['inputs.json']
    assert sha256(key.read_bytes()).hexdigest()==freeze['key_sha256']
    original={r['source']['id']:r for r in load(inputs)['sources']}
    calls=[json.loads(x) for x in (folder/f'record-groups-{job}.calls.jsonl').read_text().splitlines()]
    assert len(calls)==result['calls']==38 and len(result['rows'])==38
    assert [c['id'] for c in calls]==list(range(1,39))
    from team_memory.records import grouped,graph
    generator,_=grouped.components();cost=defaultdict(Counter)
    for c,row in zip(calls,result['rows']):
        s=original[c['source_id']]['source'];assert c['arm']==row['arm'] and c['source_id']==row['source']['id']
        if c['arm']=='grouped':
            expected=generator.render(s['text'],additional_context=json.dumps({k:s[k] for k in ('id','owner','speaker','observed_at','location')},ensure_ascii=False))
            reconstructed=grouped.construct(s,lambda *_:c['response']['choices'][0]['message']['content'],model=row['source']['record_graph']['model'])
        else:
            expected=json.dumps(dict(source={k:s[k] for k in ('id','owner','speaker','observed_at','location')},sentences=[dict(id=u['index'],text=u['quote']) for u in graph.sentence_units(s)]),ensure_ascii=False)
            reconstructed=graph.construct(s,lambda *_:c['response']['choices'][0]['message']['content'],model=row['source']['record_graph']['model'])
        assert c['request']['messages'][1]['content']==expected
        assert reconstructed==row['source']
        assert {k:v for k,v in row['source'].items() if k!='record_graph'}==s
        cost[c['arm']].update({k:v for k,v in c['response']['usage'].items() if k in ('prompt_tokens','completion_tokens','total_tokens')})
        cost[c['arm']]['calls']+=1
    baseline=load(Path('results/record-graph/v2/record-graph-122843.json'))
    allrows=[dict(arm='baseline',source=s,cached_job_id='122843') for s in baseline['sources']]+result['rows']
    report=dict(scope='Records-only partial probes + mechanical transport; not semantic precision or QA accuracy',job_id=job,program_complete=True,actual_requests_verified=38,arms={},cost=dict(cost),cases=[],all_claims=[])
    keys=load(key)['probes'];transport_rows=[]
    with tempfile.TemporaryDirectory(prefix='record-groups-transport-') as tmp:
        for i,row in enumerate(allrows):
            s=row['source'];arm=row['arm'];validate_graph(s,s['record_graph'])
            assert {k:v for k,v in s.items() if k!='record_graph'}==original[s['id']]['source']
            transport_rows.append(dict(arm=arm,source_id=s['id'],**transport(s,Path(tmp)/str(i))))
            for p in keys:
                if p['source_id']==s['id']:report['cases'].append(dict(arm=arm,case_id=original[s['id']]['case_id'],**probe(s,p)))
            for c in s['record_graph']['claims']:
                report['all_claims'].append(dict(arm=arm,case_id=original[s['id']]['case_id'],source_id=s['id'],claim_id=c['id'],stance=c['stance'],**{r:linked_text(s,c,r) for r in ROLES}))
    for arm in ('baseline','grouped'):
        rows=[r for r in allrows if r['arm']==arm];ps=[r for r in report['cases'] if r['arm']==arm]
        report['arms'][arm]=dict(sources=len(rows),statuses=dict(Counter(r['source']['record_graph']['status'] for r in rows)),
            claims=sum(len(r['source']['record_graph']['claims']) for r in rows),passed_probes=sum(p['passed'] for p in ps),total_probes=len(ps),
            negative_role_violations=sum(p['negative_role_violation'] for p in ps),missing_claim_anchor=sum(not p['matched'] for p in ps),
            fresh_calls=cost[arm]['calls'],cached_sources=22 if arm=='baseline' else 0)
    report['transport']=transport_rows
    (folder/'evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('arms','cost')},indent=2))

if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]),sys.argv[2])
