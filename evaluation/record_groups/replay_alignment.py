"""Post-hoc adapter repair on exactly the same outputs; no model rerun.

Does NOT repair role labels or claim_group membership. Primary v1b stays intact.
"""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import tempfile
from .evaluate import probe,transport,linked_text
from .placement import diagnose
from team_memory.records.grouped import construct_aligned
from team_memory.records.graph import ROLES


def main(folder,job):
    inputs=json.loads(Path('evaluation/record_groups/inputs.json').read_text())
    sources={r['source']['id']:r for r in inputs['sources']}
    calls=[json.loads(x) for x in (folder/f'record-groups-{job}.calls.jsonl').read_text().splitlines()]
    old=json.loads((folder/f'record-groups-{job}.json').read_text())
    prior={r['source']['id']:r['source'] for r in old['rows'] if r['arm']=='grouped'}
    key=json.loads(Path('evaluation/record_groups/key.json').read_text())['probes'];rows=[];probes=[]
    report=dict(scope='Post-hoc deterministic adapter repair on the same raw Qwen outputs, not fresh inference or held-out evaluation',model_calls=0,
        original_calls_sha256=sha256((folder/f'record-groups-{job}.calls.jsonl').read_bytes()).hexdigest(),
        code_sha256=sha256(Path('team_memory/records/grouped.py').read_bytes()).hexdigest(),rows=[],probes=[],all_claims=[])
    with tempfile.TemporaryDirectory(prefix='canonical-groups-') as tmp:
        for call in calls:
            if call['arm']!='grouped':continue
            sid=call['source_id'];item=sources[sid];raw=call['response']['choices'][0]['message']['content']
            s=construct_aligned(item['source'],lambda *_:raw,model=prior[sid]['record_graph']['model']);g=s['record_graph']
            rows.append(s)
            report['rows'].append(dict(case_id=item['case_id'],source=s,previous_status=prior[sid]['record_graph']['status'],transport=transport(s,Path(tmp)/sid)))
            for p in key:
                if p['source_id']==sid:
                    entry=dict(case_id=item['case_id'],**probe(s,p),placement=diagnose(s,p));probes.append(entry)
            report['all_claims'].extend(dict(case_id=item['case_id'],source_id=sid,claim_id=c['id'],stance=c['stance'],**{r:linked_text(s,c,r) for r in ROLES}) for c in g['claims'])
    report['probes']=probes
    report['summary']=dict(sources=len(rows),statuses=dict(Counter(s['record_graph']['status'] for s in rows)),claims=len(report['all_claims']),
        passed_probes=sum(p['passed'] for p in probes),total_probes=len(probes),negative_role_violations=sum(p['negative_role_violation'] for p in probes),missing_claim_anchor=sum(not p['matched'] for p in probes))
    (folder/'canonical-replay.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report['summary'],indent=2))

if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]),sys.argv[2])
