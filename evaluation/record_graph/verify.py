"""Verify frozen run inputs and actual transport, not semantic correctness."""
import argparse
from collections import Counter,defaultdict
from hashlib import sha256
import json
import re
from pathlib import Path
from team_memory.records.graph import validate_graph,describe


def verify(folder,job):
    read=lambda name:json.loads((folder/name).read_text())
    freeze=read('freeze.json');result=read(f'record-graph-{job}.json');server=read(f'sm-{job}.json')
    assert result['status']==server['status']=='complete' and server['client_exit_code']==0
    assert result['job_id']==server['job_id']==str(job)
    assert result['code_sha256']==freeze['code_sha256']
    expected_data=freeze.get('data_sha256') or {k:freeze['files_sha256'][k] for k in ('inputs.json','PROTOCOL.md')}
    assert result['data_sha256']==expected_data
    inputs_path=Path('evaluation/record_graph/inputs.json')
    assert sha256(inputs_path.read_bytes()).hexdigest()==result['input_sha256']==expected_data['inputs.json']
    assert sha256(Path('evaluation/record_graph/key.json').read_bytes()).hexdigest()==freeze['key_sha256']
    inputs=json.loads(inputs_path.read_text());original={s['id']:s for c in inputs['cases'] for s in c['sources']}
    sources={s['id']:s for s in result['sources']};assert set(sources)==set(original)
    for sid,s in sources.items():
        assert {k:v for k,v in s.items() if k!='record_graph'}==original[sid]
        validate_graph(s,s['record_graph'])
    calls=[json.loads(x) for x in (folder/f'record-graph-{job}.calls.jsonl').read_text().splitlines()]
    # Responses from parallel document checks can finish out of request order.
    calls.sort(key=lambda c:c['id'])
    assert [c['id'] for c in calls]==list(range(1,result['calls']+1))
    writers=[c for c in calls if c['context']['stage']=='record_construction']
    assert len(writers)==len(sources)
    for c in writers:
        payload=json.loads(c['request']['messages'][1]['content'])
        s=original[c['context']['source_id']]
        assert payload['source']=={k:s[k] for k in ('id','owner','speaker','observed_at','location')}
        assert payload['sentences']==[dict(id=u['index'],text=u['quote']) for u in sources[s['id']]['record_graph']['units']]
    grouped=defaultdict(list)
    for c in calls:
        if c['context']['stage']=='qa':grouped[c['context']['case_id'],c['context']['arm']].append(c)
    assert len(result['rows'])==len(inputs['cases'])*2==len(grouped)
    document_checks=[]
    for row in result['rows']:
        group=grouped[row['case_id'],row['arm']];assert len(group)==row['calls']
        prompt=group[0]['request']['messages'][0]['content']
        for s in row['bundle']['snapshot']['sources']:
            assert s['text'] in prompt and s['speaker'] in prompt and s['observed_at'] in prompt
            assert s== (sources[s['id']] if row['arm']=='linked' else original[s['id']])
        for w in row['reader_witnesses']:
            s=sources[w['source_id']]
            assert w['quote']==s['text'][w['start']:w['end']]
            if row['arm']=='linked':
                context=describe(s,w['start'],w['end']);assert w['record_context']==context
                assert json.dumps(context,ensure_ascii=False) in prompt
            else:assert 'record_context' not in w
        for c in group:
            content='\n'.join(m['content'] for m in c['request']['messages'])
            match=re.search(r'# Document to evaluate against\nSource (\d+):\n(.*?)\n\n# Output format',content,re.S)
            if match:
                evidence=row['bundle']['evidence'][int(match[1])-1]
                assert evidence['quote'] in match[2]
                assert evidence['speaker'] in match[2] and evidence['observed_at'] in match[2]
                document_checks.append(dict(call_id=c['id'],case_id=row['case_id'],arm=row['arm'],
                    source_id=evidence['source_id'],full_quote_author_time_present=True,
                    extracted_graph_present='record_context' in match[2]))
    cost=defaultdict(Counter)
    for c in calls:
        name='construction' if c['context']['stage']=='record_construction' else c['context']['arm']
        cost[name]['calls']+=1
        cost[name].update({k:v for k,v in c['response'].get('usage',{}).items() if k in ('prompt_tokens','completion_tokens','total_tokens')})
    return dict(scope='Frozen inputs/source/actual request verification; not semantic validity',job_id=str(job),
                source_preserved=len(sources),qa_pairs=len(inputs['cases']),actual_calls=len(calls),
                source_statuses=dict(Counter(s['record_graph']['status'] for s in sources.values())),
                program_complete=True,client_exit_code=0,model_revision=result['model_revision'],
                client_seconds=result['seconds'],cost=dict(cost),writer_guided=[bool(c['request'].get('guided_json')) for c in writers],
                initial_qa_packets_verified=True,document_checks=document_checks,
                external_model_api_calls=result['external_model_api_calls'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);p.add_argument('job');a=p.parse_args()
    report=verify(a.folder,a.job);(a.folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
