"""Record preservation and deterministic state evaluation, no LLM or QA scoring."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import tempfile

from team_memory.adapters.records import RecordsAdapter
from team_memory.adapters.base import request
from team_memory.adapters.legacy import public_source, native_objects
from team_memory.contracts.ports import CallContext
from team_memory.review.state import assertion_status

CAPS=frozenset(['records:read','records:write','records:import','review:vote'])


def call(port,op,payload,actor='hana'):
    return port.handle(request(op,payload,workspace_id='records-eval',request_id='eval'),
                       context=CallContext('records-eval',actor,CAPS))


def write(port,op,payload,key,actor='hana'):
    return call(port,op,dict(payload,expected_revision=port.snapshot()['revision'],idempotency_key=key),actor)


def synthetic(root,cases):
    rows=[]
    for case in cases:
        folder=root/case['id'];port=RecordsAdapter(folder,'records-eval')
        checks={};steps=[]
        for i,s in enumerate(case['sources']):
            steps.append(write(port,'record.append',{'source':s},f'source-{i}')['status'])
        submitted=write(port,'proposal.submit',{'candidate':case['candidate']},'proposal')
        steps.append(submitted['status']);pid=submitted['data']['object_id']
        pending=port.snapshot()
        unauthorized=write(port,'review.apply',dict(proposal_id=pid,choice='approve'),'intruder',actor='outsider')
        checks['unauthorized_review_rejected']=unauthorized['errors'][0]['code']=='FORBIDDEN' and port.snapshot()==pending
        accepted=0
        if case['mode']=='legacy_vote_conflict':
            from team_memory.storage.objects import Store
            objects=native_objects(pending)
            # Native source IDs must be content addresses, so use the converter
            # below to remap the opaque fixture source IDs and proposal spans.
            from team_memory.storage.objects import digest
            source_ids={sid:digest(env) for sid,env in objects['sources'].items()}
            native=next(iter(objects['timeline_proposals'].values()))
            native['history']=[source_ids[sid] for sid in native['history']]
            for field in ('previous','incoming','previous_assertion','incoming_assertion'):
                if field in native:native[field]['source_id']=source_ids[native[field]['source_id']]
            # Use a fresh legacy directory, retaining only the remapped proposal.
            legacy=Store(folder/'imported')
            for env in objects['sources'].values():legacy.put('sources',env)
            native_id=legacy.put('timeline_proposals',native)
            for choice in case['votes']:
                legacy.put('timeline_votes',dict(proposal=native_id,actor='hana',choice=choice))
            imported=RecordsAdapter(legacy.root,'records-eval').snapshot()
            p=imported['proposals'][0]
            checks.update(state_exact=all(p[k]==case['expected'][k] for k in ('status','effect','reviewer')),
                          originals_preserved=sorted(s['text'] for s in imported['sources'])==sorted(s['text'] for s in case['sources']),
                          cached_uncached_equal=RecordsAdapter(legacy.root,'records-eval',cache=False).snapshot()==imported)
            rows.append(dict(id=case['id'],scenario_group=case['scenario_group'],expected=case['expected'],
                             observed={k:p[k] for k in ('status','effect','reviewer')},checks=checks,passed=all(checks.values())))
            continue
        for i,choice in enumerate(case['votes']):
            result=write(port,'review.apply',dict(proposal_id=pid,choice=choice),f'vote-{i}')
            accepted+=result['status']=='ok'
        snap=RecordsAdapter(folder,'records-eval').snapshot()
        p=snap['proposals'][0];gold=case['expected']
        checks.update(source_metadata_exact=sorted(snap['sources'],key=lambda s:s['id'])==sorted(case['sources'],key=lambda s:s['id']),
                      candidate_spans_exact=p['candidate']==case['candidate'],
                      state_exact=all(p[k]==gold[k] for k in ('status','effect','reviewer')),
                      vote_authority=accepted==gold['accepted_votes'],
                      pending_snapshot_unchanged=port.snapshot(pending['id'])==pending,
                      cached_uncached_equal=RecordsAdapter(folder,'records-eval',cache=False).snapshot()==snap,
                      writes_succeeded=all(status=='ok' for status in steps))
        if case['candidate']['kind']=='correction':
            c=case['candidate'];objects=native_objects(snap)
            from team_memory.adapters.legacy import FrozenStore
            from team_memory.review.state import proposals
            links=proposals(FrozenStore(folder,objects))
            # Non-target assertion must remain reported even after a correction.
            old=case['sources'][0];a=old['text'].index('Owner is Hana.')
            cite=dict(source_id='old',start=a,end=a+len('Owner is Hana.'),quote='Owner is Hana.')
            checks['unrelated_field_unchanged']=assertion_status(cite,'Hana',links)=='reported'
            expected='superseded_assertion' if gold['status']=='approved' else 'reported'
            checks['target_effect_exact']=assertion_status(c['previous_assertion'],'120ms',links)==expected
        rows.append(dict(id=case['id'],scenario_group=case['scenario_group'],expected=gold,
                         observed={k:p[k] for k in ('status','effect','reviewer')},checks=checks,passed=all(checks.values())))
    return rows


def natural(root,archive):
    data=json.loads(archive.read_text());sources={}
    for store in data['stores'].values():
        for sid,env in store['sources'].items():
            if env['source']['location'].startswith(('EverMemBench-Dynamic@','https://github.com/')):
                if sid in sources:assert sources[sid]==env
                sources[sid]=env
    port=RecordsAdapter(root,'records-eval');expected=[];receipts=[]
    for sid,env in sorted(sources.items(),key=lambda row:(datetime.fromisoformat(row[1]['observed_at'].replace('Z','+00:00')),row[0])):
        s=public_source(env,sid);expected.append(s)
        result=write(port,'record.append',{'source':s},sid)
        if result['status']!='ok':raise RuntimeError(result)
        receipts.append(result['data']['snapshot']['id'])
    snapshot=RecordsAdapter(root,'records-eval',cache=False).snapshot()
    actual={s['id']:s for s in snapshot['sources']}
    fields=['id','text','owner','speaker','observed_at','location']
    field_scores={f:dict(correct=sum(actual.get(s['id'],{}).get(f)==s[f] for s in expected),total=len(expected)) for f in fields}
    # A small fixed prefix is also checked against its actual historical receipt.
    historical=port.snapshot(receipts[9])
    prefix_exact=historical['sources']==sorted(expected[:10],key=lambda s:s['id'])
    counts=Counter('EverMemBench-Dynamic' if s['location'].startswith('EverMemBench') else 'Git-PEP' for s in expected)
    return dict(selection='All unique EverMem/Git/PEP sources in the existing development archive; not an unseen split',
                dataset_counts=dict(counts),field_scores=field_scores,source_count=len(snapshot['sources']),
                fabricated_proposals=len(snapshot['proposals']),historical_prefix_exact=prefix_exact,
                passed=prefix_exact and not snapshot['proposals'] and len(actual)==len(expected) and
                all(v['correct']==v['total'] for v in field_scores.values()))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases',type=Path,default=Path('evaluation/records/cases.json'))
    parser.add_argument('--archive',type=Path,default=Path('results/module-boundary/v1/result.json'))
    parser.add_argument('--output',type=Path,default=Path('results/records/v1/quality.json'))
    parser.add_argument('--synthetic-only',action='store_true')
    args=parser.parse_args();fixtures=json.loads(args.cases.read_text())
    with tempfile.TemporaryDirectory(prefix='records-quality-') as temp:
        rows=synthetic(Path(temp)/'synthetic',fixtures['cases'])
        actual=None if args.synthetic_only else natural(Path(temp)/'natural',args.archive)
    result=dict(measured_at=datetime.now(timezone.utc).isoformat(),fresh_inference=False,
                scope='record module; oracle relationship labels; preservation and state, not extraction or QA accuracy',
                input_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [args.cases,args.archive]},
                synthetic=dict(passed=sum(r['passed'] for r in rows),total=len(rows),
                               independent_story_templates=fixtures['independent_story_templates'],rows=rows),natural=actual)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(synthetic_passed=result['synthetic']['passed'],synthetic_total=len(rows),natural=actual),ensure_ascii=False))
    return 0 if all(r['passed'] for r in rows) and (actual is None or actual['passed']) else 1


if __name__=='__main__':raise SystemExit(main())
