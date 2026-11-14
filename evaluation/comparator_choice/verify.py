"""Check provenance and literal bindings separately from semantic scoring."""
import json,sys,tarfile
from pathlib import Path
from hashlib import sha256
from team_memory.store import digest
from team_memory.timeline import valid_witness,valid_assertion_spans
from team_memory.review_citations import render_snapshot


def main(folder):
    freeze=json.loads((folder/'freeze.json').read_text());cfg=freeze['config']
    for name,h in freeze['files'].items():assert sha256((folder/'runtime'/name).read_bytes()).hexdigest()==h,name
    with tarfile.open(folder/'runtime/code.tar.gz') as archive:
        for name,h in cfg['code_sha256'].items():assert sha256(archive.extractfile(name).read()).hexdigest()==h,name
    result=json.loads((folder/'result.json').read_text());server=json.loads((folder/'server.json').read_text())
    dispatch=json.loads((folder/'dispatch.json').read_text())
    assert dispatch['state']=='COMPLETED' and dispatch['exit_code']=='0:0'
    assert result['status']==server['status']=='complete' and server['client_exit_code']==0
    assert result['job_id']==server['job_id']==dispatch['job_id']
    assert result['code_sha256']==cfg['code_sha256'] and result['data_sha256']==cfg['data_sha256']
    assert result['model']==cfg['model_repo'] and result['revision']==cfg['model_revision']
    calls=list(map(json.loads,(folder/'calls.jsonl').read_text().splitlines()))
    assert len(calls)==result['calls']==len({c['id'] for c in calls})
    qa=[r for r in result['rows'] if r['request']['operation']=='ask']
    assert len(qa)==cfg['expected_qa'] and len(result['selectors'])==cfg['expected_comparisons']
    sources_checked=0;states_checked=0;proposals_checked=0
    for state in result['stores'].values():
        for objects in state.values():
            for key,obj in objects.items():assert digest(obj)==key
        for p in state['timeline_proposals'].values():
            assert all(valid_witness(p[k],state['sources']) for k in ('previous','incoming'))
            assert valid_assertion_spans(p,state['sources']);proposals_checked+=1
    text=['# Actual QA outputs','', 'These are model outputs; semantic ratings are separate.','']
    for row in qa:
        x=row['result'];state=result['stores'][row['case_id']]
        text += ['## '+row['case_id']+'/'+row['label'],'',row['request']['question'],'',x.get('raw',json.dumps(x)), '']
        for a in x.get('answers',[]):
            for w in a.get('evidence',[]):
                if w.get('evidence_type')=='review_state':
                    snap=w['record_snapshot'];assert digest(snap)==w['snapshot_id']
                    assert state['review_snapshots'][w['snapshot_id']]==snap
                    p=snap['proposal'];assert {k:v for k,v in p.items() if k not in ('id','status')}==state['timeline_proposals'][p['id']]
                    votes=snap['votes'];assert all(v==state['timeline_votes'][k] and v['actor']==p['reviewer'] and v['proposal']==p['id'] for k,v in votes.items())
                    choices=frozenset(v['choice'] for v in votes.values())
                    assert p['status']=={frozenset():'pending',frozenset(['approve']):'approved',frozenset(['reject']):'rejected'}.get(choices,'review_conflict')
                    assert render_snapshot(snap)[w['start']:w['end']]==w['quote'];states_checked+=1
                else:
                    assert valid_witness(w,state['sources']);sources_checked+=1
                    if w.get('observed_at') is not None:assert w['observed_at']==state['sources'][w['source_id']]['observed_at']
                text += [f"- {w['source_id']} · {w['speaker']} [{w['start']}, {w['end']}): {w['quote']}",'']
    checks=dict(slurm_complete=True,program_complete=True,packet_hashes_valid=True,qa_outputs=len(qa),calls=len(calls),
        proposal_bindings=proposals_checked,source_bindings=sources_checked,review_bindings=states_checked,
        failures=[dict(case_id=r['case_id'],label=r['label'],status=r['result']['status']) for r in result['rows'] if r['result']['status'] in ('invalid','error','insufficient')],
        comparison_errors=[dict(case_id=r['case_id'],errors=r['result']['receipt']['errors']) for r in result['rows'] if r['request']['operation']=='ingest' and r['result']['receipt']['errors']],
        finish_issues=[dict(id=c['id'],context=c['context'],finish_reason=k.get('finish_reason')) for c in calls for k in c['response'].get('choices',[]) if k.get('finish_reason')!='stop'],
        semantic_correctness_checked=False)
    (folder/'verification.json').write_text(json.dumps(checks,indent=2)+'\n')
    (folder/'cases.md').write_text('\n'.join(text))
    print(json.dumps(checks,indent=2))


if __name__=='__main__':main(Path(sys.argv[1]))
