"""Verify source/stratum identity and exact reused real-model artifacts."""
import json
from pathlib import Path
from collections import Counter
from hashlib import sha256

def main():
    from evaluation.record_strata.arms import prompt,SYSTEM,compile_source
    from team_memory.records import grouped,graph
    base=Path('results/record-strata/v1');out=Path('results/record-full/v3')
    data=json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items'];gold=json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']
    assert len(data)==len(gold)==68
    strata=Counter((i['difficulty'],i['availability']) for i in data if i['panel']=='balanced_synthetic');assert len(strata)==9 and set(strata.values())=={6}
    for i,d in zip(data,gold):
        assert i['id']==d['id'] and i['difficulty']==d['difficulty'] and i['availability']==d['availability']
        assert d['source']=={k:i['source'][k] for k in d['source']}
        for n in d['nodes']:
            for span in n['spans']:assert i['source']['text'][span['start']:span['end']]==span['quote']
    oldfreeze=json.loads((base/'freeze.json').read_text())
    for name,h in oldfreeze['code_sha256'].items():assert sha256(Path(name).read_bytes()).hexdigest()==h,name
    result=json.loads((base/'record-strata-122970.json').read_text());server=json.loads((base/'sm-122970.json').read_text())
    assert result['status']==server['status']=='complete' and server['client_exit_code']==0
    assert result['code_sha256']==oldfreeze['code_sha256'] and result['data_sha256']==oldfreeze['data_sha256']
    calls=[json.loads(line) for line in (base/'record-strata-122970.calls.jsonl').read_text().splitlines()];assert len(calls)==len(result['rows'])==136
    items={i['id']:i for i in data};extra=grouped.writer_kwargs(dict(chat_template_kwargs={'enable_thinking':False},seed=42),basis_types=True)['extra_body']
    for call,row in zip(calls,result['rows']):
        assert call['item_id']==row['id'] and call['arm']==row['arm'];s=items[row['id']]['source'];b=call['request']
        assert b['messages']==[dict(role='system',content=SYSTEM),dict(role='user',content=prompt(s,row['arm']))]
        assert b['model']=='Qwen3-8B' and b['temperature']==0 and b['max_tokens']==2048 and all(b[k]==v for k,v in extra.items())
        assert row['raw']==call['response']['choices'][0]['message']['content']
        reconstructed,error=compile_source(s,row['raw'],row['source']['record_graph']['model'])
        assert reconstructed==row['source'] and error==row['compile_error'];graph.validate_graph(row['source'],row['source']['record_graph'])
        assert row['transport']['stored_restarted']
    verified=dict(status='passed',real_model_job='122970',cached_calls=136,fresh_calls=0,sources=68,primary_strata={str(k):v for k,v in strata.items()},production_code_unchanged=True,exact_prompts_verified=True,compiler_replay_verified=True,source_spans_verified=True,old_store_transport_receipts_verified=True,new_store_transport_run=False,assertion_roots=sum(len(d['records']) for d in gold),information_nodes=sum(len(d['nodes']) for d in gold),required_edges=sum(len(d['edges']) for d in gold),optional_edges=sum(len(d['optional_edges']) for d in gold))
    (out/'verification.json').write_text(json.dumps(verified,indent=2)+'\n');print(json.dumps(verified,indent=2))
if __name__=='__main__':main()
