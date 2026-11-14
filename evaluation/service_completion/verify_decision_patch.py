"""Verify frozen v2 stage boundaries and unchanged factual model requests."""
import argparse,json
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import jsonpatch
from team_memory.decision_patch import EXTRACT,UPDATE,EXTRACT_SCHEMA,UPDATE_SCHEMA
from team_memory.timeline import decode


def main(folder):
    repo=Path(__file__).resolve().parents[2]
    freeze=json.loads((folder/'freeze.json').read_text())
    assert sha256((repo/'team_memory/decision_patch.py').read_bytes()).hexdigest()==freeze['config']['code_sha256']['team_memory/decision_patch.py']
    result=json.loads((folder/'result.json').read_text())
    grouped=defaultdict(list)
    for c in map(json.loads,(folder/'calls.jsonl').read_text().splitlines()):
        if c['context']['label']=='ingest':grouped[c['context']['case_id']].append(c)
    baseline={}
    for c in map(json.loads,(repo/'results/service-completion/v3b/calls.jsonl').read_text().splitlines()):
        if c['context']['label']=='ingest':baseline[c['context']['case_id']]=c
    audit=[]
    for row in result['rows']:
        if row['request']['operation']!='ingest':continue
        cid=row['case_id'];cs=grouped[cid];receipt=row['result']['receipt'];ex=cs[0]['request']
        assert ex['messages'][0]['content']==EXTRACT and ex['guided_json']==EXTRACT_SCHEMA
        assert set(json.loads(ex['messages'][-1]['content']))=={'earlier'}
        assert ex['chat_template_kwargs']['enable_thinking'] is False
        meta=receipt.get('comparison_metadata',{})
        item=dict(case_id=cid,calls=len(cs),receipt_errors=receipt['errors'],
                  proposals=len(receipt['proposals']),decision_extraction=meta.get('decision_extraction'),
                  suppressed=meta.get('suppressed_decision_candidates',[]),decisions=receipt.get('comparison_audit',[]))
        if not receipt['errors']:
            extracted=decode(cs[0]['response']['choices'][0]['message']['content'])['sources']
            assert extracted==meta['decision_extraction']
            item['factual_request_matches_v3b']=cs[1]['request']==baseline[cid]['request']
            assert item['factual_request_matches_v3b'],cid
            if item['decisions']:
                assert len(cs)==3 and cs[2]['request']['guided_json']==UPDATE_SCHEMA
                assert cs[2]['request']['messages'][0]['content']==UPDATE
                second=json.loads(cs[2]['request']['messages'][-1]['content'])
                updates=decode(cs[2]['response']['choices'][0]['message']['content'])['updates']
                by_id={u['decision_id']:u for u in updates}
                for d,entry in zip(second['existing'],item['decisions'],strict=True):
                    assert entry['decision']==d and entry['update']==by_id[d['decision_id']]
                    assert entry['before']['decision']==entry['after']['decision']
                    if entry['patches']:
                        assert jsonpatch.apply_patch(entry['before'],entry['update']['patches'])==entry['after']
                        assert entry['kind']=='reconsider'
                    else:assert entry['before']==entry['after'] and entry['kind'] is None
        item['grounded_negative_requires_semantic_review']=True
        audit.append(item)
    report=dict(cases=len(audit),guided_output_verified=True,old_only_extraction_verified=True,
                identical_fact_requests=sum(x.get('factual_request_matches_v3b',False) for x in audit),
                failed_cases=[x['case_id'] for x in audit if x['receipt_errors']],
                semantic_correctness_verified=False,cases_detail=audit)
    (folder/'patch-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='cases_detail'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);main(p.parse_args().folder)
