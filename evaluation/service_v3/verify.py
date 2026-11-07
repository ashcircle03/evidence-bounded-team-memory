"""Frozen structural audit and arm-blinded semantic review cards (no model judge)."""
import argparse,json
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from team_memory.store import digest


def verify(folder):
    result=json.loads((folder/'result.json').read_text())
    inputs=json.loads((folder/'inputs.json').read_text())
    calls=[json.loads(l) for l in (folder/'calls.jsonl').read_text().splitlines()]
    freeze=json.loads((folder/'freeze-final.json').read_text())
    assert result['status']=='complete' and len(result['rows'])==86
    assert len(calls)==result['calls'] and len({r['id'] for r in calls})==len(calls)
    assert result['code_sha256']==freeze['config']['code_sha256']
    assert result['data_sha256']==freeze['config']['data_sha256']
    assert sha256((folder/'inputs.json').read_bytes()).hexdigest()==result['input_sha256']
    packets={p['id']:p for p in inputs['packets']}
    binding=[];issues=[]
    for row in result['rows']:
        for answer in row['result'].get('answers',[]):
            for w in answer['evidence']:
                if w.get('evidence_type')=='review_state':
                    state=result['stores'][row['case_id'].split('/')[0]]
                    snap=w['record_snapshot'];sid=w['snapshot_id']
                    assert digest(snap)==sid and state['review_snapshots'][sid]==snap
                    p=snap['proposal'];stored=state['timeline_proposals'][p['id']]
                    assert {k:v for k,v in p.items() if k not in ('id','status')}==stored
                    votes=snap['votes'];assert sorted(votes)==w['vote_ids']
                    for vid,v in votes.items():
                        assert digest(v)==vid and state['timeline_votes'][vid]==v
                        assert v['actor']==p['reviewer'] and v['proposal']==p['id']
                    choices={v['choice'] for v in votes.values()}
                    expected={frozenset():'pending',frozenset(['approve']):'approved',frozenset(['reject']):'rejected'}.get(frozenset(choices),'review_conflict')
                    assert p['status']==expected
                    assert w['source_id']=='review:'+sid and w['end']==len(w['quote'])
                    binding.append(dict(id=row['case_id'],arm=row['arm'],type='review_state',source=w['source_id']))
                else:
                    if row['split']=='stream':
                        env=result['stores'][row['case_id'].split('/')[0]]['sources'][w['source_id']]
                        assert digest(env)==w['source_id']
                        assert env['source']['text'][w['start']:w['end']]==w['quote']
                        assert env['source']['speaker']==w['speaker'] and env['source']['location']==w['location']
                    else:
                        p=packets[row['case_id']]
                        originals=p.get('originals')
                        if originals:
                            original=originals[w['source_id']]
                            assert original['quote'][w['start']:w['end']]==w['quote']
                        else:
                            assert w in p['witnesses']
                    binding.append(dict(id=row['case_id'],arm=row['arm'],type='source',source=w['source_id']))
    for c in calls:
        for choice in c['response'].get('choices',[]):
            if choice.get('finish_reason')!='stop':issues.append(dict(call=c['id'],finish_reason=choice.get('finish_reason')))
    # Duplicate initial generation requests show the intended paired prompt control.
    paired=[]
    for cid in packets:
        by_arm={a:[c for c in calls if c['context'].get('case_id')==cid and c['context'].get('arm')==a] for a in ['direct','attributed']}
        assert all(by_arm.values())
        equal=by_arm['direct'][0]['request']==by_arm['attributed'][0]['request']
        assert equal,cid
        paired.append(cid)
    out=dict(program_complete=True,rows=len(result['rows']),physical_calls=len(calls),source_binding_checks=len(binding),
        review_bindings=sum(b['type']=='review_state' for b in binding),finish_issues=issues,
        fixed_packet_initial_requests_identical=len(paired),semantic_entailment_verified=False)
    (folder/'verification.json').write_text(json.dumps(out,indent=2))
    keys=json.loads((folder/'keys.json').read_text())
    streamkeys=json.loads((folder/'stream-keys.json').read_text())
    cards={};mapping={}
    for row in result['rows']:
        rid=sha256(('review-cards-v1:'+row['case_id']+'/'+row['arm']).encode()).hexdigest()[:16]
        key=keys.get(row['case_id'])
        if row['split']=='stream':
            cid,label=row['case_id'].split('/');key=streamkeys[cid]['answers'][label]
        # Do not expose judge/rewrite traces or profile names to the reviewer.
        x=row['result']
        cards[rid]=dict(question=row['question'],split=row['split'],expected=key,answer=x.get('raw'),
            answers=x.get('answers'),quote_reviews=x.get('quote_citation_reviews'),
            source_packet=x.get('citation_sources'),diagnostics=x.get('warnings',[]))
        mapping[rid]=dict(case_id=row['case_id'],arm=row['arm'],split=row['split'])
    (folder/'blind-cards.json').write_text(json.dumps(dict(sorted(cards.items())),ensure_ascii=False,indent=2))
    (folder/'blind-mapping.json').write_text(json.dumps(mapping,indent=2))
    print(json.dumps(out))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);verify(p.parse_args().folder)
