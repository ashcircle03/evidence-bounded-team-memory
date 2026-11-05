"""Verify complete pilot artifacts and report paired official scores without tuning."""
import argparse
from collections import Counter
import json
from pathlib import Path

from .audit import digest
from .official import state_hash


def verify(result, config, folder):
    assert result['status']=='complete'
    assert result['conda_prefix']==config['conda_prefix']
    assert Path(result['python']).parent==Path(config['conda_prefix'])/'bin'
    assert result['selection']==config['selection']
    assert result['type_counts']=={'T1':200,'T2':200}
    assert len(result['completed'])==2
    audit=[json.loads(line) for line in (folder/'http.jsonl').read_text().splitlines()]
    requests={r['request_id']:r for r in audit if r['event']=='request'}
    responses={r['request_id']:r for r in audit if r['event']=='response'}
    assert len(requests)==sum(r['event']=='request' for r in audit)
    assert set(requests)==set(responses), 'Missing response or transport error'
    assert set(requests)==set(range(1,len(requests)+1))
    observed_in=observed_out=0
    models=Counter()
    for rid, req in requests.items():
        assert req['body_sha256']==digest(req['body'])
        assert req['endpoint']==config['policy']['base_url']+'/chat/completions'
        assert req['body']['model'] in config['policy']['models']
        res=responses[rid]
        assert res['usage_known'] and res['status']==200, 'Report retries/errors separately before accepting complete run'
        usage=res['body']['usage'];observed_in+=usage['prompt_tokens'];observed_out+=usage['completion_tokens']
        assert all(c.get('finish_reason')!='length' for c in res['body']['choices'])
        models[res['body']['model']]+=1
    assert len(requests)<=config['limits']['requests']
    assert observed_in<=config['limits']['input_tokens'] and observed_out<=config['limits']['output_tokens']
    assert observed_in==result['accounting']['observed_input_tokens']
    assert observed_out==result['accounting']['observed_output_tokens']
    scores=[]
    for selected in config['selection']:
        uid=selected['uid']
        trace=json.loads((folder/(uid+'.cupmem.json')).read_text())
        assert trace['input_sha256']==selected['input_sha256']
        assert trace['completed_session_count']==50 and trace['completed_query_count']==3
        assert trace['sample_meta']['session_mode']=='full'
        assert trace['sample_meta']['selected_session_indices']==list(range(50))
        assert all(trace['sample_meta'][k] is None for k in ['M_old','M_new','explanation','relevant_session_index'])
        checks=trace['memory_immutability_checks']
        assert len(checks)==6 and {c['state_sha256'] for c in checks}=={state_hash(trace)}
        item=next(r for r in result['completed'] if r['uid']==uid)
        for arm, judged in item['judgments'].items():
            assert judged['uid']==uid and 'error' not in judged['accounting']
            scores.append(dict(uid=uid,type=selected['type'],arm=arm,
                          passes={dim:judged['ratings'][dim+'_eval']['pass'] for dim in ['dim1','dim2','dim3']}))
    return dict(status='verified',label='two-case alternate-model protocol pilot, not a benchmark score',
                cases=2,physical_requests=len(requests),observed_input_tokens=observed_in,
                observed_output_tokens=observed_out,reported_models=dict(models),scores=scores,
                currency_cost='BAZE monetary/credit debit unavailable from token response; do not substitute OpenAI pricing')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('result',type=Path);parser.add_argument('config',type=Path)
    parser.add_argument('folder',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
    report=verify(json.loads(args.result.read_text()),json.loads(args.config.read_text()),args.folder)
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
