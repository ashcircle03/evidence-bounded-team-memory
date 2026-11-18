"""Offline evidence checks; changed prose is queued for source-based review."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from team_memory.timeline import valid_witness


def main(folder, baseline):
    result=json.loads((folder/'result.json').read_text())
    assert result['status']=='complete'
    freeze=json.loads((folder/'runtime/freeze.json').read_text())
    assert result['code_sha256']==freeze['config']['code_sha256']
    assert result['data_sha256']==freeze['config']['data_sha256']
    for name,h in freeze['files'].items():
        assert sha256((folder/'runtime'/name).read_bytes()).hexdigest()==h,name
    server=json.loads((folder/'server.json').read_text())
    accounting=json.loads((folder/'dispatch.json').read_text())
    assert server['status']=='complete' and server['client_exit_code']==0
    assert accounting['state']=='COMPLETED' and accounting['exit_code']=='0:0'
    assert server['job_id']==accounting['job_id']==result['job_id']
    old=json.loads((baseline/'result.json').read_text())
    gold=json.loads((baseline/'ratings.json').read_text())
    previous={r['case_id']+'/'+r['label']:r for r in old['rows'] if r['split']=='legacy' and r['request']['operation']=='ask'}
    assert len(previous)==20
    inputs=json.loads((folder/'runtime/inputs.json').read_text())
    assert result['sources']['a']==result['sources']['b']
    for c in inputs['cases']:
        for sid,env in c['sources'].items(): assert result['sources']['a'][c['id']][sid]==env
    expected_new={m['revision']:{cid:set(ids) for cid,ids in m['new_ids'].items()} for m in result['mutations']}
    expected_flat={r:{sid for ids in v.values() for sid in ids} for r,v in expected_new.items()}
    ratings={};pending=[];phases={};total_calls=0;finish_issues=[];quotes=0
    response_ids=[];usage=Counter()
    text=['# Two local Git environments — fresh Qwen outputs','',
          'Changed answers require source-based semantic review; quote offsets alone do not prove support.','']
    pids=[];first={};index_paths={}
    for p in result['phases']:
        name=p['label'];x=json.loads((folder/p['output']).read_text());assert x['status']=='complete'
        pids.append(x['pid']);side='a' if name.startswith('a_') else 'b'
        index_paths.setdefault(side,set()).update(x['index_paths'])
        assert all('/'+side.upper()+'/.git/team-memory-clients/' in n for n in x['index_paths'])
        calls=[json.loads(l) for l in (folder/(name+'.calls.jsonl')).read_text().splitlines()]
        assert x['calls']==len(calls)==sum(r['calls'] for r in x['rows'])
        assert len({c['id'] for c in calls})==len(calls)
        total_calls+=len(calls)
        for c in calls:
            assert c['request']['model']=='Qwen3-8B' and c['response']['model']=='Qwen3-8B'
            assert c['request']['temperature']==0 and c['request']['chat_template_kwargs']['enable_thinking'] is False
            assert c['response']['usage']['completion_tokens']>0
            response_ids.append(c['response']['id'])
            usage.update({k:c['response']['usage'][k] for k in ('prompt_tokens','completion_tokens')})
            for choice in c['response']['choices']:
                if choice['finish_reason']!='stop':finish_issues.append(dict(phase=name,id=c['id'],finish_reason=choice['finish_reason']))
        regular=[r for r in x['rows'] if r['label']!='canary'];assert len(regular)==20
        assert all(r['calls']>0 and r['document_batches']==0 and r['parsed_documents']==0 for r in x['rows'])
        if name.endswith('restart'):
            assert not x['document_batches'] and not x['parsed_source_ids'] and not x['preparation']
        if name in ('a_pull','b_pull'):
            revision=1 if name=='a_pull' else 2
            assert set(x['parsed_source_ids'])==expected_flat[revision]
            assert len(x['parsed_source_ids'])==len(expected_flat[revision])
            assert sum(len(b['texts']) for b in x['document_batches'])==len(expected_flat[revision])
            assert all(r['result']['prepared_documents']==revision for r in x['preparation'])
        phase=dict(legacy_questions=20,exact_previous=0,exact_initial=0,calls=len(calls),
                   legacy_status_counts=dict(Counter(r['result']['status'] for r in regular)),
                   parsed_documents=len(x['parsed_source_ids']),document_embeddings=sum(len(b['texts']) for b in x['document_batches']))
        for r in x['rows']:
            key=r['case_id']+'/'+r['label'];rk=name+'/'+key;answer=r['result']
            for a in answer.get('answers',[]):
                for w in a.get('evidence',[]):
                    assert valid_witness(w,result['sources'][side][r['case_id']]),rk
                    env=result['sources'][side][r['case_id']][w['source_id']]
                    assert w['speaker']==env['source']['speaker'] and w['location']==env['source']['location']
                    if 'observed_at' in w:assert w['observed_at']==env['observed_at']
                    quotes+=1
            if r['label']=='canary':
                pending.append(rk)
            else:
                prior=previous[key]['result']
                identical=all(answer.get(k)==prior.get(k) for k in ('raw','answers'))
                if identical:
                    ratings[rk]=dict(gold[key],basis='Fresh Qwen raw and complete answer/evidence objects exactly equal previously source-reviewed output')
                    phase['exact_previous']+=1
                else:pending.append(rk)
                if name=='a_initial':first[key]=answer
                if all(answer.get(k)==first[key].get(k) for k in ('raw','answers')):phase['exact_initial']+=1
            text += [f'## {rk}','',r['question'],'',answer.get('raw',str(answer)),'','### Cited original passages','']
            for a in answer.get('answers',[]):
                for w in a.get('evidence',[]):
                    text += [f"- {w['speaker']} · {w.get('observed_at')} · {w['location']} · `{w['source_id']}` [{w['start']},{w['end']})",'', '> '+w['quote'].replace('\n','\n> '),'']
        phases[name]=phase
    assert len(set(pids))==6 and not (index_paths['a'] & index_paths['b'])
    assert len(set(response_ids))==total_calls
    for name,revision in [('b_add_prepare',1),('a_change_prepare',2),('a_noop_prepare',0),('b_noop_prepare',0)]:
        data=json.loads((folder/(name+'.json')).read_text())
        assert data['document_embeddings']==7*revision
        assert set(data['parsed_ids'])==(expected_flat[revision] if revision else set())
        assert len(data['parsed_ids'])==7*revision
        assert [r['result']['prepared_documents'] for r in data['rows']]==[revision]*7
    report=dict(status='structural_checks_passed',job_id=result['job_id'],fresh_calls=total_calls,token_usage=dict(usage),phases=phases,
        quote_binding_checks=quotes,finish_issues=finish_issues,manual_review_candidates=pending,
        process_restart=True,independent_index_paths=True,delta_only_parse_and_embed=True,original_sources_preserved=True,
        no_document_embedding_during_qa=True,no_query_response_replay=True,
        scope='Logical two-checkout isolation on one compute node; storage/index/QA, not relationship or approval accuracy',
        offline_verifier_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    (folder/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (folder/'inherited-ratings.json').write_text(json.dumps(ratings,ensure_ascii=False,indent=2)+'\n')
    (folder/'cases.md').write_text('\n'.join(text)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);parser.add_argument('--baseline',type=Path,default=Path('results/module-boundary/v1'))
    args=parser.parse_args();main(args.folder,args.baseline)
