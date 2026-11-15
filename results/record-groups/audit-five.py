"""From repo root: PYTHONPATH=. python results/record-groups/audit-five.py; no model calls."""
import json,hashlib,dataclasses
import langextract
from pathlib import Path
from collections import Counter
from langextract import prompt_validation as pv
from team_memory.records.grouped import examples,components,construct_aligned

root=Path.cwd();folder=root/'results/record-groups/v1b';key=json.loads((root/'evaluation/record_groups/key.json').read_text())['probes'][:5]
inputs=json.loads((root/'evaluation/record_groups/inputs.json').read_text())['sources'];sources={x['source']['id']:x['source'] for x in inputs}
calls=[json.loads(x) for x in (folder/'record-groups-122895.calls.jsonl').read_text().splitlines()]
canonical={r['source']['id']:r['source'] for r in json.loads((folder/'canonical-replay.json').read_text())['rows']}
strict={r['source']['id']:r['source'] for r in json.loads((folder/'record-groups-122895.json').read_text())['rows'] if r['arm']=='grouped'}
records=[];requests=[];seen=set();_,resolver=components()
for i,p in enumerate(key,1):
 s=sources[p['source_id']];c=next(c for c in calls if c['arm']=='grouped' and c['source_id']==s['id']);raw=c['response']['choices'][0]['message']['content'];rows=json.loads(raw)['extractions'];decoded=resolver.resolve(raw)
 # Upstream resolver only parses: all raw roles, group names and stances survive.
 for a,b in zip(rows,decoded):
  role=next(k for k in a if not k.endswith('_attributes'));assert b.extraction_class==role and b.extraction_text==a[role] and b.attributes==a[role+'_attributes']
 assert len(rows)==len(decoded)
 current=construct_aligned(s,lambda *_:raw,model=canonical[s['id']]['record_graph']['model']);assert current==canonical[s['id']]
 anchors=[a['claim_attributes']['claim_group'] for a in rows if 'claim' in a and p['anchor'] in a['claim']]
 assert len(anchors)==1;group=anchors[0];relations=[]
 for expected in ('condition','basis'):
  for needle in p[expected]:
   found=[]
   for a in rows:
    role=next(k for k in a if not k.endswith('_attributes'))
    if needle in a[role]:found.append(dict(role=role,group=a[role+'_attributes']['claim_group'],text=a[role],target_group=a[role+'_attributes']['claim_group']==group))
   assert found,(i,needle)
   assert any(a[role] in s['text'] for a in rows for role in a if not role.endswith('_attributes') and needle in a[role])
   where='same_group_other_role' if any(x['target_group'] for x in found) else 'other_group_only'
   assert not any(x['target_group'] and x['role']==expected for x in found)
   relations.append(dict(expected_role=expected,needle=needle,raw_matches=found,raw_placement=where))
 records.append(dict(requirement_number=i,call_id=c['id'],source_id=s['id'],anchor=p['anchor'],raw_target_group=group,relations=relations,strict_status=strict[s['id']]['record_graph']['status'],canonical_status=current['record_graph']['status'],resolver_preserves_raw_roles_groups=True,canonical_replay_equal=True))
 if s['id'] not in seen:
  seen.add(s['id']);prompt=c['request']['messages'][1]['content'];assert prompt.endswith('Q: '+s['text']+'\nA: ')
  assert c['response']['choices'][0]['finish_reason']=='stop'
  requests.append(dict(call_id=c['id'],source=s,source_chars=len(s['text']),source_present_in_full=True,usage=c['response']['usage'],finish_reason='stop',max_tokens=c['request']['max_tokens'],model=c['request']['model'],decoding={k:c['request'][k] for k in ('temperature','seed','chat_template_kwargs')},raw_model_output=json.loads(raw)))
validation={}
for label,policy in [('upstream_defaults',None),('our_alignment_policy',pv.AlignmentPolicy(enable_fuzzy_alignment=False,accept_match_lesser=False))]:validation[label]=dataclasses.asdict(pv.validate_prompt_alignment(examples(),policy=policy))
versions={}
for n in ['prompting.py','resolver.py','annotation.py','extraction.py']:
 b=(Path(langextract.__file__).parent/n).read_bytes();versions[n]=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
report=dict(scope='Read-only raw-output diagnosis; no model calls, no runtime/prompt/gold/score changes',requirements=len(records),unique_sources=len(seen),fresh_model_calls=0,new_slurm_jobs=0,
 raw_call_file_sha256=hashlib.sha256((folder/'record-groups-122895.calls.jsonl').read_bytes()).hexdigest(),
 grouping_summary=dict(Counter(r['raw_placement'] for p in records for r in p['relations'])),
 requests=requests,requirements_detail=records,upstream_prompt_validation=validation,
 installed_core_git_blob_shas=versions,upstream_commit='0e441bf77ddc3119dd0aa413322959234dd84ee5')
(root/'results/record-groups/five-failure-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,default=str)+'\n')
print(json.dumps({k:report[k] for k in ['requirements','unique_sources','grouping_summary','upstream_prompt_validation']},ensure_ascii=False,default=str,indent=2))
print('calls',[(x['call_id'],x['source_chars'],x['usage']['prompt_tokens'],x['usage']['completion_tokens']) for x in requests])
