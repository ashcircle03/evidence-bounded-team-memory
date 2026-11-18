"""Predeclared focal-claim probes. Not exhaustive precision/recall of all source claims."""
from collections import defaultdict,Counter
from hashlib import sha256
from pathlib import Path
import json,re
from team_memory.records.graph import ROLES
from evaluation.record_groups.evaluate import linked_text


def norm(s):return ' '.join(re.findall(r'\w+',s.casefold()))
def contains(texts,needle):return norm(needle) in norm(' '.join(texts))


def raw_groups(raw):
    groups={}
    try:
        for row in json.loads(raw)['extractions']:
            role=next(r for r in ROLES if r in row);a=row[role+'_attributes'];gid=a['claim_group']
            g=groups.setdefault(gid,dict(id=gid,stances=[],**{r:[] for r in ROLES}))
            g[role].append(row[role])
            if role=='claim':g['stances'].append(a['stance'])
    except (ValueError,KeyError,TypeError,StopIteration):return []
    for g in groups.values():g['stance']=g['stances'][0] if len(set(g['stances']))==1 else 'unknown'
    return list(groups.values())


def compiled_groups(source):
    return [dict(id=c['id'],stance=c['stance'],**{r:linked_text(source,c,r) for r in ROLES}) for c in source['record_graph']['claims']]


def check(groups,key):
    targets=[g for g in groups if contains(g['claim'],key['core'])]
    details=[]
    for g in targets:
        alltexts=[t for r in ROLES for t in g[r]]
        slots=[dict(**s,recovered=contains(alltexts,s['text']),typed=contains(g[s['role']],s['text'])) for s in key['slots']]
        visible=[s for s in slots if s['available'] and not s.get('optional')]
        missing=[s for s in slots if not s['available']]
        wrong=[s for s in key['forbidden'] if contains(alltexts,s)]
        # Missing evidence is not a recall failure; guessing its value is a failure.
        hallucinated=[s['text'] for s in missing if s['recovered']]
        stance=g['stance'] in key.get('acceptable_stances',[key['stance']])
        details.append(dict(group_id=g['id'],slots=slots,stance_ok=stance,wrong_target=wrong,unsupported_completion=hallucinated,
            visible_recovered=all(s['recovered'] for s in visible),typed_complete=all(s['typed'] for s in visible),
            passed=all(s['typed'] for s in visible) and stance and not wrong and not hallucinated))
    # A correct group cannot cancel a second, wrong group for the same focal claim.
    clean=not any(d['wrong_target'] or d['unsupported_completion'] for d in details)
    return dict(target_found=bool(targets),details=details,visible_recovered=bool(details) and any(d['visible_recovered'] for d in details),
        typed_complete=bool(details) and any(d['typed_complete'] for d in details),
        stance_ok=bool(details) and any(d['stance_ok'] for d in details),
        unsupported_completion=any(d['unsupported_completion'] for d in details),wrong_target=any(d['wrong_target'] for d in details),
        passed=clean and any(d['passed'] for d in details))


def oracle_raw(key):
    rows=[{'claim':key['core'],'claim_attributes':dict(claim_group='target',stance=key['stance'])}]
    for s in key['slots']:
        if not s['available'] or s.get('optional'):continue
        a=dict(claim_group='target',stance=key['stance'] if s['role']=='claim' else 'unknown')
        rows.append({s['role']:s['text'],s['role']+'_attributes':a})
    return json.dumps(dict(extractions=rows))


def main(folder,job):
    from evaluation.record_strata.arms import prompt,SYSTEM,compile_source
    inputs=json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items'];keys=json.loads(Path('evaluation/record_strata/keys.json').read_text())['items']
    freeze=json.loads((folder/'freeze.json').read_text())
    for n,h in freeze['evaluation_sha256'].items():assert sha256(Path(n).read_bytes()).hexdigest()==h,n
    result=json.loads((folder/f'record-strata-{job}.json').read_text());server=json.loads((folder/f'sm-{job}.json').read_text())
    assert result['status']==server['status']=='complete' and server['client_exit_code']==0
    assert result['code_sha256']==freeze['code_sha256'] and result['data_sha256']==freeze['data_sha256']
    calls=[json.loads(x) for x in (folder/f'record-strata-{job}.calls.jsonl').read_text().splitlines()]
    assert result['calls']==len(calls)==len(result['rows'])==136
    items={x['id']:x for x in inputs};gold={x['id']:x for x in keys};cases=[];cost=defaultdict(Counter)
    for i,(call,row) in enumerate(zip(calls,result['rows'])):
        item=items[row['id']];s=item['source'];key=gold[row['id']]
        assert call['id']==i+1 and call['item_id']==row['id'] and call['arm']==row['arm']
        assert call['request']['messages']==[dict(role='system',content=SYSTEM),dict(role='user',content=prompt(s,row['arm']))]
        assert call['response']['choices'][0]['message']['content']==row['raw']
        rebuilt,error=compile_source(s,row['raw'],row['source']['record_graph']['model']);assert rebuilt==row['source'] and error==row['compile_error']
        raw=check(raw_groups(row['raw']),key);stored=check(compiled_groups(row['source']),key)
        spans=[t for g in raw_groups(row['raw']) for r in ROLES for t in g[r]]
        cases.append(dict(id=row['id'],arm=row['arm'],panel=item['panel'],family=item['family'],difficulty=item['difficulty'],availability=item['availability'],raw=raw,compiled=stored,compile_error=error,transport=row['transport'],raw_all_verbatim=bool(spans) and all(t in s['text'] for t in spans),raw_to_compiled_pass_loss=raw['passed'] and not stored['passed'],raw_to_compiled_content_loss=raw['visible_recovered'] and not stored['visible_recovered'],finish_reason=call['response']['choices'][0]['finish_reason']))
        cost[row['arm']].update({k:v for k,v in call['response']['usage'].items() if k in ('prompt_tokens','completion_tokens','total_tokens')});cost[row['arm']]['calls']+=1
    summary=[]
    for panel in ('balanced_synthetic','natural_audit'):
        for arm in ('simple','ours'):
            subsets=[('all','all')]+([(d,a) for d in ('easy','medium','hard') for a in ('full','partial','none')] if panel=='balanced_synthetic' else [])
            for difficulty,availability in subsets:
                cs=[c for c in cases if c['arm']==arm and c['panel']==panel and (difficulty=='all' or (c['difficulty']==difficulty and c['availability']==availability))]
                summary.append(dict(panel=panel,arm=arm,difficulty=difficulty,availability=availability,n=len(cs),**{f'{stage}_{metric}':sum(c[stage][metric] for c in cs) for stage in ('raw','compiled') for metric in ('target_found','visible_recovered','typed_complete','stance_ok','passed','unsupported_completion','wrong_target')},compile_rejections=sum(bool(c['compile_error']) for c in cs),pass_lost_compiling=sum(c['raw_to_compiled_pass_loss'] for c in cs),content_lost_compiling=sum(c['raw_to_compiled_content_loss'] for c in cs),transport_failures=sum(not c['transport']['stored_restarted'] for c in cs)))
    output=dict(job_id=job,scope='Focal linkage diagnosis; synthetic18 related families and failure-selected natural14 messages; not full semantic recall or QA',cases=cases,summary=summary,cost=dict(cost))
    (folder/'evaluation.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(summary=summary,cost=dict(cost)),indent=2))
if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]),sys.argv[2])
