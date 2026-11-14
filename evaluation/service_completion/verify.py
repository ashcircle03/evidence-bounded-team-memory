"""Verify completion-run provenance and render all outputs without changing ratings."""
import argparse,json,tarfile
from hashlib import sha256
from pathlib import Path
from team_memory.store import digest
from team_memory.timeline import valid_witness,valid_assertion_spans


def snapshot_render(snapshot, state):
    """Reconstruct the exact cited state from that snapshot's sources and votes."""
    from team_memory.review_citations import render_snapshot
    assert all(sid in state['sources'] for sid in snapshot['source_ids'])
    return render_snapshot(snapshot)


def main(folder):
    result=json.loads((folder/'result.json').read_text())
    freeze=json.loads((folder/'freeze.json').read_text())
    calls=[json.loads(line) for line in (folder/'calls.jsonl').read_text().splitlines()]
    for name,expected in freeze['files'].items():
        assert sha256((folder/'runtime'/name).read_bytes()).hexdigest()==expected,name
    with tarfile.open(folder/'runtime/code.tar.gz') as archive:
        for name,expected in freeze['config']['code_sha256'].items():
            assert sha256(archive.extractfile(name).read()).hexdigest()==expected,name
    server=json.loads((folder/'server.json').read_text())
    dispatch=json.loads((folder/'dispatch.json').read_text())
    assert server['status']=='complete' and server['client_exit_code']==0
    assert dispatch['state']=='COMPLETED' and dispatch['exit_code']=='0:0'
    assert server['job_id']==dispatch['job_id']==result['job_id']
    assert result['status']=='complete'
    assert result['code_sha256']==freeze['config']['code_sha256']
    assert result['data_sha256']==freeze['config']['data_sha256']
    assert result['calls']==len(calls)==len({c['id'] for c in calls})
    for state in result['stores'].values():
        for objects in state.values():
            for key,value in objects.items():assert digest(value)==key
    rows=[r for r in result['rows'] if r['request']['operation']=='ask']
    assert len(rows)==37 and sum(r['split']=='legacy' for r in rows)==20
    checks=0;state_checks=0;failures=[]
    text=['# Full model outputs — completion boundary','','Implementation-agent semantic ratings are separate. Structural checks do not prove entailment.','']
    for row in rows:
        x=row['result'];cid=row['case_id'];state=result['stores'][cid];sources=state['sources']
        for sid,env in sources.items():assert digest(env)==sid
        if x['status'] in ('error','invalid','insufficient'):failures.append(dict(id=cid+'/'+row['label'],status=x['status']))
        for answer in x.get('answers',[]):
            for w in answer.get('evidence',[]):
                if w.get('evidence_type')=='review_state':
                    snap=w['record_snapshot'];sid=w['snapshot_id'];assert digest(snap)==sid
                    assert state['review_snapshots'][sid]==snap
                    p=snap['proposal'];assert p['id'] in state['timeline_proposals']
                    assert {k:v for k,v in p.items() if k not in ('id','status')}==state['timeline_proposals'][p['id']]
                    assert valid_assertion_spans(p,sources)
                    assert sorted(snap['votes'])==w['vote_ids']
                    for vid,vote in snap['votes'].items():
                        assert digest(vote)==vid and vote==state['timeline_votes'][vid]
                        assert vote['actor']==p['reviewer'] and vote['proposal']==p['id']
                    choices=frozenset(v['choice'] for v in snap['votes'].values())
                    expected={frozenset():'pending',frozenset(['approve']):'approved',frozenset(['reject']):'rejected'}.get(choices,'review_conflict')
                    assert p['status']==expected
                    rendered=snapshot_render(snap,state)
                    assert w['source_id']=='review:'+sid
                    assert 0 <= w['start'] < w['end'] <= len(rendered)
                    assert rendered[w['start']:w['end']]==w['quote']
                    state_checks+=1
                else:
                    assert valid_witness(w,sources),(cid,w)
                    if w.get('observed_at') is not None:assert w['observed_at']==sources[w['source_id']]['observed_at']
                    checks+=1
        text += [f"## {cid}/{row['label']}",'',row['request']['question'],'',f"Status: {x['status']}; physical calls: {row['calls']}",'',x.get('raw',json.dumps(x,ensure_ascii=False)),'','### Returned evidence','']
        for answer in x.get('answers',[]):
            for w in answer.get('evidence',[]):
                text += [f"- `{w['source_id']}` · {w['speaker']} · {w['location']} · [{w['start']}, {w['end']})",'','> '+w['quote'].replace('\n','\n> '),'']
        if x.get('warnings'):text+=['Warnings: '+json.dumps(x['warnings'],ensure_ascii=False),'']
    report=dict(program_complete=True,slurm_completed=True,frozen_packet_verified=True,qa_outputs=len(rows),physical_calls=len(calls),source_binding_checks=checks,review_binding_checks=state_checks,execution_failures=failures,
                finish_issues=[dict(id=c['id'],context=c['context'],finish_reason=k.get('finish_reason')) for c in calls for k in c['response'].get('choices',[]) if k.get('finish_reason')!='stop'],semantic_entailment_verified=False)
    (folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (folder/'cases.md').write_text('\n'.join(text))
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);main(p.parse_args().folder)
