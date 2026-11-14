"""Audit actual before/after model stages and upstream patch application.

Structural verification only. Human-readable relation ratings remain separate.
"""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path

from team_memory.source_patch import apply_delta
from team_memory.timeline import decode


def main(folder):
    result=json.loads((folder/'result.json').read_text())
    config=json.loads((folder/'freeze.json').read_text())['config']
    repo=Path(__file__).resolve().parents[2]
    assert sha256((repo/'team_memory/source_patch.py').read_bytes()).hexdigest()==config['code_sha256']['team_memory/source_patch.py']
    calls=[json.loads(line) for line in (folder/'calls.jsonl').read_text().splitlines()]
    by_case=defaultdict(list)
    for call in calls:
        if call['context'].get('label')=='ingest':by_case[call['context']['case_id']].append(call)
    rows=[r for r in result['rows'] if r['request']['operation']=='ingest']
    audit=[]
    for row in rows:
        cid=row['case_id'];receipt=row['result']['receipt'];cs=by_case[cid]
        states=receipt.get('comparison_audit',[])
        first=json.loads(cs[0]['request']['messages'][-1]['content'])
        assert set(first)=={'earlier'},cid
        try:extracted=decode(cs[0]['response']['choices'][0]['message']['content'])['records']
        except (ValueError,KeyError,TypeError):
            assert receipt['errors'],cid
            extracted=[]
        item=dict(case_id=cid,model_calls=len(cs),extracted_records=len(extracted),
                  receipt_errors=receipt['errors'],audit_records=len(states),
                  proposal_count=len(receipt['proposals']),updates=[])
        if not receipt['errors'] and extracted:
            assert len(cs)==2,cid
            second=json.loads(cs[1]['request']['messages'][-1]['content'])
            patched=decode(cs[1]['response']['choices'][0]['message']['content'])['updates']
            expected=[dict(r,record_id='R'+str(i)) for i,r in enumerate(extracted)]
            assert second['existing']==expected and second['earlier']==first['earlier'],cid
            assert len(states)==len(expected)==len(patched),cid
            by_id={u['record_id']:u for u in patched}
            for s,r in zip(states,expected):
                assert s['record']==r and s['update']==by_id[r['record_id']],cid
                assert s['delta']==apply_delta(r,s['update']),cid
                item['updates'].append(dict(record_id=r['record_id'],record_type=r['record_type'],
                    subject=r['subject'],attribute=r['attribute'],**s['delta'],reason=s['update']['reason']))
        # Failed or empty extraction is not a successful negative classification.
        item['eligible_negative']=bool(extracted and states and not receipt['errors'])
        audit.append(item)
    summary=dict(old_extraction_received_no_incoming=True,cases=len(audit),
        failed_cases=[x['case_id'] for x in audit if x['receipt_errors']],
        empty_extractions=[x['case_id'] for x in audit if not x['extracted_records']],
        semantic_correctness_verified=False,cases_detail=audit)
    (folder/'patch-verification.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='cases_detail'},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path)
    main(parser.parse_args().folder)
