"""Verify a source-QA run and apply explicit source-based ratings, not answer aliases."""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys

from evaluation.cupmem.practical.score import success
from team_memory.store import digest, source_envelope
from team_memory.timeline import valid_witness

ROOT = Path(__file__).resolve().parents[2]


def read(p): return json.loads(p.read_text())
def write(p, value): p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def main():
    folder = Path(sys.argv[1])
    result = read(folder/'result.json')
    assert result['status'] == 'complete'
    inputs_path = ROOT/'evaluation/cupmem/practical/legacy.json'
    assert sha256(inputs_path.read_bytes()).hexdigest() == result['input_sha256']
    inputs = read(inputs_path)
    key = read(ROOT/'evaluation/cupmem/practical/legacy-key.json')['cases']
    baseline = read(ROOT/'results/cupmem/practical/scored-cases.json')['legacy']
    by_baseline = {(r['case_id'],r['label'],r['arm']):r for r in baseline}
    histories = {c['id']:{digest(source_envelope(e)):source_envelope(e)
                         for event in c['events'] for e in event.get('records',[])} for c in inputs['cases']}
    calls = sorted([json.loads(s) for s in (folder/'calls.jsonl').read_text().splitlines()], key=lambda c:c['id'])
    assert len(calls) == result['calls']
    assert [c['id'] for c in calls] == list(range(len(calls)))
    assert all(c['request']['model']=='Qwen3-8B' for c in calls)
    assert all(c['rendered_prompt_tokens']+c['request']['max_tokens'] <= 32768 for c in calls)
    cards = {}
    for row in result['rows']:
        assert row['sources_preserved']
        case = row['case_id']; assert case in histories
        for step in row['steps']:
            label = step['label']
            if label == 'import':
                assert step['calls']==0 and step['result']['status']=='ok'
                continue
            card_id = case+'/'+label
            assert card_id not in cards
            output = step['result']
            selected = [w for a in output.get('answers',[]) for w in a['evidence']]
            assert all(valid_witness(w,histories[case]) for w in selected+output.get('citation_sources',[]))
            actual = [c for c in calls if c['context']==dict(case_id=case,label=label)]
            assert len(actual)==step['calls']
            assert all(any(w['quote'] in m['content'] for call in actual
                           for m in call['request']['messages']) for w in selected)
            if output.get('raw'):
                generated=output.get('pre_citation_raw',output['raw'])
                if 'pre_citation_raw' in output:
                    reconstructed=generated
                    for op in reversed(output['posthoc_citations']):
                        assert generated[op['start']:op['end']]==op['sentence']
                        assert 1<=op['number']<=len(output['citation_sources'])
                        reconstructed=reconstructed[:op['start']]+f"[{op['number']}] "+reconstructed[op['start']:]
                    assert reconstructed==output['raw']
                segments=output.get('generation_segments',[generated])
                if output.get('generation_kind')=='llama-index-accumulate':
                    assert output['raw']=='\n---------------------\n'.join(f'Response {i+1}: {s or "Empty Response"}' for i,s in enumerate(segments))
                answer_calls = [c for c in actual if c.get('response',{}).get('choices',[{}])[0].get('message',{}).get('content') in segments]
                assert answer_calls
                assert all(any(c['response']['choices'][0]['message']['content']==s for c in answer_calls) for s in segments)
                assert all(any(w['quote'] in m['content'] for call in answer_calls
                               for m in call['request']['messages']) for w in selected)
            if output.get('aqa_candidate_raw'):
                candidate_calls=[c for c in actual if c.get('response',{}).get('choices',[{}])[0].get('message',{}).get('content')==output['aqa_candidate_raw']]
                assert candidate_calls
                assert all(any(w['quote'] in m['content'] for c in candidate_calls for m in c['request']['messages'])
                           for w in output['citation_sources'])
            if output.get('quote_attribution_raw'):
                quote_calls=[c for c in actual if c.get('response',{}).get('choices',[{}])[0].get('message',{}).get('content')==output['quote_attribution_raw']]
                assert quote_calls
                assert all(any(w['quote'] in m['content'] for c in quote_calls for m in c['request']['messages'])
                           for w in output['citation_sources'])
                assert any(output['pre_citation_raw'] in m['content'] for c in quote_calls for m in c['request']['messages'])
                expected=[]
                for review in output['quote_citation_reviews']:
                    assert output['pre_citation_raw'][review['start']:review['end']]==review['sentence']
                    for e in review['evidence']:
                        proposed=e.get('proposed_quote',e['quote'])
                        assert proposed in review['proposed_quotes']
                        assert proposed.split()==e['quote'].split()
                        assert output['citation_sources'][e['number']-1]['quote'][e['start']:e['end']]==e['quote']
                    for n in sorted({e['number'] for e in review['evidence']}):
                        expected.append(dict(start=review['start'],end=review['end'],sentence=review['sentence'],number=n))
                assert expected==output['posthoc_citations']
            for judgment in output.get('document_judgments',[]):
                checked = [output['citation_sources'][i-1] for i in judgment['citation_numbers']]
                assert all(w['source_id']==judgment['source_id'] for w in checked)
                if judgment['label'] != 'ERROR':
                    physical = [c for c in actual if c.get('response',{}).get('choices',[{}])[0].get('message',{}).get('content','').strip()==judgment['raw']]
                    assert physical
                    assert all(any(w['quote'] in m['content'] for call in physical
                                   for m in call['request']['messages']) for w in checked)
            cards[card_id] = dict(case_id=case,label=label,question=key[case]['questions'][label],
                result=output,seconds=step['seconds'],calls=step['calls'],
                simple=by_baseline[(case,label,'simple')]['rating'],
                cupmem=by_baseline[(case,label,'cupmem')]['rating'])
    assert set(cards)=={c+'/'+q for c,m in key.items() for q in m['questions']}
    nli_traces=[]
    if result.get('nli_pairs') is not None:
        nli_traces=[json.loads(l) for l in (folder/'nli.jsonl').read_text().splitlines()]
        assert len(nli_traces)==result['nli_pairs']
        assert [t['id'] for t in nli_traces]==list(range(len(nli_traces)))
        expected=[]
        for cid,c in cards.items():
            out=c['result'];ops={op['start']:op for op in out['posthoc_citations']}
            for review in out['nli_citation_reviews']:
                assert out['pre_citation_raw'][review['start']:review['end']]==review['sentence']
                supported=[i for i,j in enumerate(review['judgments']) if j['label']=='entailment']
                if supported:
                    number=review['tfidf_number']
                    if number-1 not in supported:
                        number=max(supported,key=lambda i:review['judgments'][i]['probabilities'][1])+1
                    assert ops[review['start']]['number']==number
                else:assert review['start'] not in ops
                for w,j in zip(out['citation_sources'],review['judgments'],strict=True):
                    expected.append((c,w,j,review['sentence']))
        assert len(expected)==len(nli_traces)
        for trace,(c,w,j,claim) in zip(nli_traces,expected,strict=True):
            assert trace['context']==dict(case_id=c['case_id'],label=c['label'])
            assert trace['passage']==w['quote'] and trace['claim']==claim
            assert trace['probabilities']==j['probabilities'] and trace['label']==j['label']
            assert len(trace['input_ids'])==len(trace['attention_mask'])<=512
            assert trace['truncated']==(trace['full_tokens']>512)
            assert sum(trace['attention_mask'])==min(512,trace['full_tokens'])
            assert abs(sum(trace['probabilities'])-1)<1e-5
            assert trace['label']==['contradiction','entailment','neutral'][max(range(3),key=lambda i:trace['probabilities'][i])]
    write(folder/'cards.json',cards)
    write(folder/'alce.json',dict(data=[c['result']['alce'] for c in cards.values() if 'alce' in c['result']]))
    composites=sum(c['result'].get('generation_kind')=='llama-index-accumulate' for c in cards.values())
    posthoc=sum(bool(c['result'].get('posthoc_citations')) for c in cards.values())
    verification = dict(program_complete=True,planned_qa=20,observed_qa=len(cards),
        input_sha256=result['input_sha256'],originals_preserved=True,all_returned_offsets_valid=True,
        raw_answers_match_physical_model_responses=composites==0 and posthoc==0,
        answer_segments_match_physical_model_responses=True,
        composite_raw_matches_upstream_concatenation=True,
        selected_quotes_present_in_actual_inputs=True,calls=len(calls),
        upstream_accumulate_composites=composites,
        posthoc_changed_answers=posthoc,
        posthoc_additions=sum(len(c['result'].get('posthoc_citations',[])) for c in cards.values()),
        posthoc_edits_are_exact_citation_insertions=True,
        quote_attribution_calls=sum(bool(c['result'].get('quote_attribution_raw')) for c in cards.values()),
        quote_attribution_errors=sum(bool(c['result'].get('quote_attribution_error')) for c in cards.values()),
        nli_pairs=len(nli_traces),nli_truncated_pairs=sum(t['truncated'] for t in nli_traces),
        nli_input_output_and_selection_verified=bool(nli_traces),
        unattributed_sentences=sum(len(c['result'].get('unattributed_sentences',[])) for c in cards.values()),
        selected_quotes_present_in_answer_generating_inputs=True,document_judgments_match_actual_model_calls=True,
        max_rendered_prompt_tokens=max((c['rendered_prompt_tokens'] for c in calls),default=0),
        max_output_reservation=max((c['request']['max_tokens'] for c in calls),default=0),
        statuses=dict(Counter(c['result']['status'] for c in cards.values())),
        unfinished_generations=sum(c.get('response',{}).get('choices',[{}])[0].get('finish_reason')=='length' for c in calls),
        result_sha256=sha256((folder/'result.json').read_bytes()).hexdigest(),
        calls_sha256=sha256((folder/'calls.jsonl').read_bytes()).hexdigest())
    write(folder/'verification.json',verification)
    ratings_path = folder/'ratings.json'
    if not ratings_path.exists():
        print(json.dumps(verification)); return
    ratings = read(ratings_path)['ratings']; assert set(ratings)==set(cards)
    assert all(r.get('reason','').strip() for r in ratings.values())
    corpus = defaultdict(lambda: dict(total=0,simple=0,cupmem=0,reference=0))
    lost, gained = [], []
    for cid,c in cards.items():
        bucket = corpus[c['question']['corpus']]; bucket['total'] += 1
        for arm,rating in [('simple',c['simple']),('cupmem',c['cupmem']),('reference',ratings[cid])]:
            bucket[arm] += success(rating)
        if success(c['simple']) and not success(ratings[cid]): lost.append(c['question']['original_id'])
        if not success(c['simple']) and success(ratings[cid]): gained.append(c['question']['original_id'])
    summary = dict(scope='Exposed development diagnostic; historical controls, not a new paired holdout',
        answer_correct=sum(r['answer_correct'] is True for r in ratings.values()),
        answer_and_citation=sum(success(r) for r in ratings.values()),total=20,
        simple_answer_and_citation=sum(success(c['simple']) for c in cards.values()),
        cupmem_answer_and_citation=sum(success(c['cupmem']) for c in cards.values()),
        lost_simple_successes=lost,gained_over_simple=gained,by_corpus=dict(corpus),verification=verification,
        limitations=['One developer AI rated meaning against original sources; no independent human adjudication.',
            'Chunking, context size, prompting, metadata visibility and output cap changed together.',
            'ALCE-shaped export exists; AutoAIS was not run. Raw Source N labels need canonical citation normalization for ALCE.',
            'Required-answer citation support is scored; full sentence-level citation completeness is separate.',
            'This run does not test new Git reconsideration or owner approval semantics.'])
    if result.get('profile') in ('team','checked','attributed'):
        previous_folder = ROOT/'results/reference-qa/run-v2'
        freeze = read(folder/'freeze.json')
        for filename, field in [('result.json','previous_result_sha256'),
                                ('ratings.json','previous_ratings_sha256')]:
            assert sha256((previous_folder/filename).read_bytes()).hexdigest() == freeze[field]
        assert sha256((ROOT/'evaluation/cupmem/practical/legacy-key.json').read_bytes()).hexdigest() == freeze['key_sha256']
        previous = read(previous_folder/'ratings.json')['ratings']
        assert set(previous) == set(ratings)
        comparisons = {cid:dict(previous=success(previous[cid]),current=success(ratings[cid]))
                       for cid in ratings}
        summary['versus_reference_v2'] = dict(
            previous_correct=sum(c['previous'] for c in comparisons.values()),
            preserved=sum(c['previous'] and c['current'] for c in comparisons.values()),
            recovered=[cid for cid,c in comparisons.items() if not c['previous'] and c['current']],
            regressed=[cid for cid,c in comparisons.items() if c['previous'] and not c['current']],
            still_failed=[cid for cid,c in comparisons.items() if not c['current']],
            cases=comparisons)
        summary['limitations'][1] = 'Hybrid retrieval, visible provenance and generation/review changed together; no causal ablation.'
        old_cards = read(previous_folder/'cards.json')
        if result.get('profile')=='attributed':
            checked_folder=ROOT/'results/reference-qa/parse-v1'
            for name,h in freeze['checked_reference_sha256'].items():
                assert sha256((checked_folder/name).read_bytes()).hexdigest()==h
            previous_checked=read(checked_folder/'ratings.json')['ratings']
            old_cards=read(checked_folder/'cards.json')
            comparisons={cid:dict(previous=success(previous_checked[cid]),current=success(ratings[cid]))
                         for cid in ratings}
        lines = ['# 같은20문항의 수정 전후 답·인용', '',
            '이미 본 개발 문항이다. 같은 고정 기준으로 개발 담당 AI가 원문을 대조해 판정했다. 독립 평가가 아니다.', '',
            '| 문항 | 이전 | 수정 후 |', '|---|---|---|']
        for cid,c in comparisons.items():
            lines.append(f"| {cards[cid]['question']['original_id']} | {int(c['previous'])} | {int(c['current'])} |")
        for cid,c in cards.items():
            lines.extend(['', '## '+c['question']['original_id'], '', c['question']['question'], '',
                          '판정: '+ratings[cid]['reason'], '', '수정 전:', '', old_cards[cid]['result']['raw'],
                          '', '수정 후:', '', c['result'].get('raw', str(c['result'])), '', '수정 후 인용 원문:'])
            for number in c['result'].get('cited_numbers',[]):
                witnesses = c['result'].get('citation_sources',[])
                if not 1 <= number <= len(witnesses):
                    continue
                w = witnesses[number-1]
                lines.extend(['', f"[{number}] {w['speaker']} · {w['location']}", '',
                    f"원문 ID `{w['source_id']}`, 문자 위치 {w['start']}–{w['end']}", '',
                    '\n'.join('> '+line for line in w['quote'].splitlines())])
        (folder/'comparison.md').write_text('\n'.join(lines)+'\n')
        if result.get('profile')=='attributed':
            checked=ROOT/'results/reference-qa/parse-v1'
            for name,h in freeze['checked_reference_sha256'].items():
                assert sha256((checked/name).read_bytes()).hexdigest()==h
            prior=read(checked/'ratings.json')['ratings']
            summary['versus_checked']=dict(previous_correct=sum(success(r) for r in prior.values()),
                preserved=sum(success(prior[k]) and success(ratings[k]) for k in prior),
                regressed=[k for k in prior if success(prior[k]) and not success(ratings[k])],
                recovered=[k for k in prior if not success(prior[k]) and success(ratings[k])])
    summary['claim_level_citation_gap_cases']=[cid for cid,r in ratings.items() if r.get('claim_level_citation_gap')]
    summary['new_citation_error_cases']=[cid for cid,r in ratings.items() if r.get('new_citation_error')]
    if result.get('replay_from_job_id'):
        summary['replay']=dict(from_job_id=result['replay_from_job_id'],
            reused_physical_calls=result['reused_physical_calls'],new_physical_calls=result['new_physical_calls'],
            changed_answer_cases=[row['case_id']+'/'+s['label'] for row in result['rows'] for s in row['steps']
                                  if s['label']!='import' and not s.get('answer_text_unchanged')])
    write(folder/'summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
