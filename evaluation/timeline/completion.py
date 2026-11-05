"""Final evidence audit; no inference, resubmission or primary-score changes."""
from hashlib import sha256
import json
from pathlib import Path
from .build import HERE, ROOT, write
from team_memory import timeline as t
from team_memory.store import digest

OUT=ROOT/'results/timeline'
CAMPAIGN=ROOT.parent/'campaigns/speakermem-dev'


def audit():
    def read(p):return json.loads(p.read_text())
    frozen=[]
    for manifest,base in [('freeze.json',ROOT),('data-freeze.json',HERE),('reporting-freeze.json',HERE)]:
        for name,h in read(HERE/manifest)['files'].items():
            assert sha256((base/name).read_bytes()).hexdigest()==h,(manifest,name)
            frozen.append(str((base/name).relative_to(ROOT)))
    inputs={r['id']:r for r in read(HERE/'final.json')};keys=read(HERE/'final-key.json')
    generations=read(OUT/'final-generations.json')['streams'];replays=read(OUT/'final-git.json')
    assert set(inputs)==set(keys) and len(inputs)==20
    assert set(generations)==set(replays)=={cid+'/'+mode for cid in inputs for mode in ('direct','indexed')}
    assert {k['kind'] for k in keys.values()}=={'reconsider','coexist','conflict','correction','irrelevant'}
    calls=answer_citations=reviews=0
    for uid,s in generations.items():
        inp=inputs[s['id']];sources={digest(x['source']):x['source'] for x in inp['steps'] if x['op']=='ingest'}
        assert sources==s['objects']['sources'] and len(sources)==5
        assert replays[uid]['status']=='passed' and replays[uid]['clones_converged'] and replays[uid]['raw_sources_unchanged']
        assert replays[uid]['calls_replayed']==len(s['calls'])
        it=iter(s['calls']);seen=set();approved={};proposed={}
        def consume(expected):
            nonlocal calls
            call=next(it);assert call['system']==expected;calls+=1
            content=json.loads(call['content'])
            assert call['usage']['output_tokens']<=call['cap']
            for p in content.get('relations',content.get('earlier_relations',[])):
                assert p['previous']['source_id'] in seen and p['incoming']['source_id'] in seen
                if p['status']=='approved':assert p['id'] in approved
            for card in content.get('decision_index',[]):assert card['source_id'] in seen
            return content
        def covers(w,a):
            pos=a['quote'].find(a['answer'])
            return pos>=0 and w['source_id']==a['source_id'] and w['start']<=a['start']+pos and a['start']+pos+len(a['answer'])<=w['end']
        for step,out in zip(inp['steps'],s['steps']):
            assert step['op']==out['op'] and step.get('id')==out['id']
            result=out['result']
            if step['op']=='ingest':
                env=step['source'];sid=digest(env)
                assert sid not in seen and set(result['history'])==seen
                if seen:
                    c=consume(t.COMPARE)
                    assert set(c)<= {'earlier','incoming','earlier_relations','decision_index'}
                    assert c['incoming']==dict(id=sid,**env)
                    assert {e['id'] for e in c['earlier']}==seen
                    for e in c['earlier']:assert {k:e[k] for k in ('owner','observed_at','source')}==sources[e['id']]
                if s['mode']=='indexed':assert consume(t.INDEX)==env
                for p in result['relations']:
                    assert p['status']=='pending' and p['reviewer']==sources[p['previous']['source_id']]['owner']
                    assert p['previous']['source_id'] in seen and p['incoming']['source_id']==sid
                    proposed[p['id']]=p
                seen.add(sid)
            elif step['op']=='review':
                for p in result['reviews']:
                    assert p['id'] in proposed and p['status']=='approved'
                    assert p['reviewer']==step['actor']==sources[p['previous']['source_id']]['owner']
                    approved[p['id']]=p;reviews+=1
            else:
                c=consume(t.QA)
                assert set(c)<= {'question','sources','relations','decision_index'}
                assert c['question']==step['question'] and {e['id'] for e in c['sources']}==seen
                for e in c['sources']:assert {k:e[k] for k in ('owner','observed_at','source')}==sources[e['id']]
                for a in result['answers']:
                    assert a['source_id'] in seen
                    text=sources[a['source_id']]['source']['text']
                    assert text[a['start']:a['end']]==a['quote']
                    assert a['answer'] in a['quote'] or a['answer']==sources[a['source_id']]['source']['speaker']
                    if a['condition']:
                        w=a['condition'];assert w['source_id']==a['source_id'] and text[w['start']:w['end']]==w['quote']
                    state=a['status']
                    if state in ('approved_correction','superseded_assertion'):
                        side='incoming' if state=='approved_correction' else 'previous'
                        assert any(p['kind']=='correction' and covers(p[side],a) for p in approved.values())
                    elif state=='pending_correction':
                        assert any(p['kind']=='correction' and pid not in approved and covers(p['incoming'],a) for pid,p in proposed.items())
                    else:assert state=='reported',state
                    answer_citations+=1
        try:next(it);raise AssertionError('unused model call')
        except StopIteration:pass
        assert seen==set(sources)
    assert calls==540
    ledger=read(CAMPAIGN/'campaign-dispatch.json');jobs={v:j for v,j in ledger['jobs'].items() if v.startswith('timeline-')}
    assert len(jobs)==5
    for v,j in jobs.items():
        assert (j['state'],j['exit_code'],j.get('verified'))==('COMPLETED','0:0',True),v
        result=read(CAMPAIGN/'results'/f"sm-{j['job_id']}.json")
        assert result['status']=='complete' and str(result['job_id'])==j['job_id']
        assert j['submission_intent']=='submitted'
        for name,h in j['source_sha256'].items():assert sha256((CAMPAIGN/'source'/v/name).read_bytes()).hexdigest()==h
        if 'packets.json' in j['source_sha256']:assert result['input_sha256']==j['source_sha256']['packets.json']
    gpu_seconds=sum(j['elapsed_seconds']*j['gpus'] for j in jobs.values())
    assert gpu_seconds<=240*60
    assert sum(j.get('elapsed_seconds',0)*j['gpus'] for j in ledger['jobs'].values())<=500*60
    legacy=read(OUT/'legacy-qa.json');assert legacy['preserved']==legacy['historical_cases']==20
    natural=read(OUT/'natural-provenance-audit.json')
    assert len(natural['items'])==20 and all(x['source_in_official_reference_spans'] and x['original_question_answer_and_message_unchanged'] for x in natural['items'])
    rows=read(OUT/'final/rows.json');ratings=read(OUT/'final/ratings.json');cards=read(OUT/'final/blind-cards.json')
    assert set(ratings)==set(cards) and all(isinstance(v['ok'],bool) and v['reason'] for v in ratings.values())
    assert sum(r['qa_total'] for r in rows.values())==280
    decision=read(OUT/'decision.json');assert decision['selected']=='direct'
    assert read(OUT/'sensitivity.json')['alternative_selection']['selected']=='direct'
    assert all((ROOT/p).is_file() for p in ['team_memory/timeline.py','team_memory/timeline_cli.py','evaluation/timeline/README.md',
               'results/timeline/README.md','results/timeline/interpretation.ko.md','results/timeline/cases.ko.md','results/timeline/diagnostics.json'])
    requirements=[
      ('minimum_source_review_qa_system','team_memory/timeline.py; team_memory/timeline_cli.py; 540 measured calls replayed through actual Git'),
      ('sequential_accumulation_without_future_or_gold_input','independent call-by-call source/approval visibility audit above; frozen inputs contain only worklogs and event-time review fixtures'),
      ('all_five_requested_knowledge_events','20 frozen streams, four per reconsider/coexist/conflict/correction/irrelevant type'),
      ('fair_fixed_comparison','same pinned 14B model, common raw access and stream budgets, code/data freeze verified'),
      ('review_hits_and_false_requests_measured','final/rows.json; final/ratings.json; diagnostics.json distinguish wrong kinds, negative cases and repeats'),
      ('old_and_new_qa_measured','legacy-qa.json: 20/20 unchanged 3B results; final/rows.json: all 280 new 14B QA checkpoints retained'),
      ('raw_preservation_and_no_unreviewed_promotion','each final source equals its input; every published approval state has a preceding exact source-bound review witness'),
      ('real_cost_all_attempts','all five timeline Slurm jobs completed and source/results verified; 103.45 GPU minutes'),
      ('design_selection_and_runnable_documentation','direct already is the CLI default; decision.json and interpretation.ko.md state retained/excluded components and failures'),
      ('no_final_case_tuning_or_extra_experiments','frozen method/input/primary grading files unchanged; exactly the five planned data/development/legacy/final jobs')]
    result=dict(status='complete_for_implementation_comparison_and_design_selection',requirements=[dict(id=k,status='evidenced',evidence=v) for k,v in requirements],
       source_files_checked=len(frozen),final_stream_arms=40,exact_model_calls_replayed=calls,published_answer_citations_verified=answer_citations,
       explicit_review_events_verified=reviews,raw_source_overwrites=0,unreviewed_promotions=0,goal_gpu_seconds=gpu_seconds,
       goal_cpu_only_seconds=sum(j['elapsed_seconds'] for j in jobs.values() if not j['gpus']),
       jobs={v:{k:j[k] for k in ('job_id','state','exit_code','elapsed_seconds','gpus')} for v,j in jobs.items()},
       limitations=['Performance is not error-free: strict new QA 111/140 per arm, false requests and output-contract failures remain.',
                    'Selected natural QA is support-selected; review scenarios are controlled synthetic records, not a real-team field trial.',
                    'One implementing AI graded semantics; one disputed rating and one alias strictness issue are disclosed.',
                    'Owner reviews are simulated field-matched actions, not authenticated GitHub users or independent human judgments.',
                    'Legacy 3B QA compatibility is distinct from new 14B timeline performance; no long-corpus retrieval or concurrent-writer guarantee.'])
    write(OUT/'completion-audit.json',result)
    print('Completion evidence audited:',calls,'actual calls,',answer_citations,'published citations,',reviews,'reviews;',gpu_seconds/60,'GPU minutes')


if __name__=='__main__':audit()
