"""Verify traces and source offsets, then aggregate explicit semantic ratings."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,sys
from team_memory.store import source_envelope,digest
from team_memory.timeline import valid_witness
from team_memory.reference_joint import format_joint


def main():
    root=Path(__file__).resolve().parents[3];folder=Path(sys.argv[1]) if len(sys.argv)>1 else root/'results/reference-qa/simplify-v2'
    read=lambda p:json.loads(p.read_text())
    write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    freeze=read(folder/'freeze.json');cfg=read(folder/'config.json');result=read(folder/'result.json')
    assert result['status']=='complete' and len(result['rows'])==44
    assert result['code_sha256']==cfg['code_sha256'] and result['data_sha256']==cfg['data_sha256']
    for n,h in cfg['code_sha256'].items():assert sha256((root/n).read_bytes()).hexdigest()==h,n
    for n,h in freeze['evaluation_sha256'].items():assert sha256((root/n).read_bytes()).hexdigest()==h,n
    original=read(root/'evaluation/cupmem/practical/legacy.json')
    old_sources={c['id']:{digest(source_envelope(e)):source_envelope(e) for event in c['events'] for e in event.get('records',[])} for c in original['cases']}
    fresh={c['id']:c for c in read(root/'evaluation/reference_qa/simplify/inputs.json')['cases']}
    old_cards=read(root/'results/reference-qa/quote-normalized-v1/cards.json')
    calls=[json.loads(l) for l in (folder/'calls.jsonl').read_text().splitlines()];calls.sort(key=lambda c:c['id'])
    assert len(calls)==result['calls'] and [c['id'] for c in calls]==list(range(len(calls)))
    assert all(c['http_status']==200 and c['rendered_prompt_tokens']+c['request']['max_tokens']<=32768 for c in calls)
    cards={}
    for row in result['rows']:
        context={n:row[n] for n in ['split','case_id','arm']};cid='/'.join(context.values())
        physical=[c for c in calls if c['context']==context];assert len(physical)==row['calls']
        output=row['result']
        if row['split']=='legacy':
            sources=old_sources[row['case_id'].split('/')[0]];question=old_cards[row['case_id']]['result']['alce']['question']
        else:
            case=fresh[row['case_id']];sources={digest(source_envelope(e)):source_envelope(e) for e in case['records']};question=case['question']
        assert all(valid_witness(w,sources) for w in output['citation_sources'])
        selected=[w for a in output.get('answers',[]) for w in a['evidence']]
        assert all(valid_witness(w,sources) for w in selected)
        assert all(any(w['quote'] in m['content'] for c in physical for m in c['request']['messages']) for w in selected)
        if row['arm']=='joint':
            assert len(physical)==1
            raw=physical[0]['response']['choices'][0]['message']['content']
            assert raw==output['generation_raw']
            rebuilt=format_joint(question,raw,output['citation_sources'])
            assert rebuilt==output
            for claim in output.get('claims',[]):
                for q in claim['quoted_spans']:assert sources[q['source_id']]['source']['text'][q['start']:q['end']]==q['quote']
        else:
            raw=output.get('pre_citation_raw',output['raw'])
            assert any(c['response']['choices'][0]['message']['content']==raw for c in physical)
            rendered=raw
            for op in reversed(output.get('posthoc_citations',[])):
                assert raw[op['start']:op['end']]==op['sentence']
                rendered=rendered[:op['start']]+f"[{op['number']}] "+rendered[op['start']:]
            assert rendered==output['raw']
        cards[cid]=dict(**row,question=question)
    assert len(cards)==44
    for cid in fresh:
        assert cards['transfer/'+cid+'/joint']['result']['citation_sources']==cards['transfer/'+cid+'/attributed']['result']['citation_sources']
    metrics={}
    for split,arm in [('legacy','joint'),('transfer','joint'),('transfer','attributed')]:
        rows=[r for r in result['rows'] if r['split']==split and r['arm']==arm]
        traces=[c for c in calls if c['context']['split']==split and c['context']['arm']==arm]
        metrics[split+'/'+arm]=dict(cases=len(rows),calls=len(traces),seconds=sum(r['seconds'] for r in rows),
            input_tokens=sum(c['response']['usage']['prompt_tokens'] for c in traces),
            output_tokens=sum(c['response']['usage']['completion_tokens'] for c in traces),
            statuses=dict(Counter(r['result']['status'] for r in rows)))
    verification=dict(program_complete=True,rows=44,physical_calls=len(calls),all_original_offsets_valid=True,selected_sources_present_in_model_inputs=True,paired_retrieval_equal=True,joint_generation_and_rendering_verified=True,input_and_actor_hashes_verified=True,truncated_model_outputs=sum(c['response']['choices'][0]['finish_reason']=='length' for c in calls),metrics=metrics)
    write(folder/'cards.json',cards);write(folder/'verification.json',verification)
    if not (folder/'ratings.json').exists():print(json.dumps(verification,indent=2));return
    ratings=read(folder/'ratings.json')['ratings'];assert set(ratings)==set(cards)
    for k,r in ratings.items():assert r['reason'] and isinstance(r['success'],bool)
    scores={}
    for name in metrics:scores[name]=sum(ratings[k]['success'] for k,c in cards.items() if c['split']+'/'+c['arm']==name)
    old=[k for k,c in cards.items() if c['split']=='legacy' and not ratings[k]['success']]
    criteria=dict(legacy20_preserved=scores['legacy/joint']==20,new12_noninferior=scores['transfer/joint']>=scores['transfer/attributed'],
        same_source_both_orders=all(ratings['transfer/'+c+'/joint']['success'] for c in ['new-conflict-one-source','new-conflict-one-source-reversed']),
        critical_controls_no_regression=all(ratings['transfer/'+c+'/joint']['success'] or not ratings['transfer/'+c+'/attributed']['success'] for c in ['new-unrelated','new-author','new-no-answer']),
        at_most_half_calls=metrics['transfer/joint']['calls']<=metrics['transfer/attributed']['calls']/2)
    summary=dict(scores=scores,criteria=criteria,adopt_joint=all(criteria.values()),legacy_regressions=old,verification=verification)
    write(folder/'summary.json',summary)
    lines=['# 고정 비교: 실제 답변과 원문 판정','']
    for k,c in cards.items():
        lines.extend(['## '+k,'',c['question'],'','PASS' if ratings[k]['success'] else 'FAIL',ratings[k]['reason'],'',c['result']['raw'],''])
        for issue in ratings[k].get('citation_issues',[]):
            lines.extend(['인용 주의: '+issue,''])
        if c['arm']=='joint':
            lines.extend(['모델이 선택한 좁은 구절과 위치 진단:','',
                '```json',json.dumps(c['result'].get('claims',[]),ensure_ascii=False,indent=2),'```',''])
        for a in c['result'].get('answers',[]):
            for w in a['evidence']:lines.extend([f"Source {w['source_id']} {w['speaker']} {w['location']} ({w['start']}:{w['end']})",'','> '+w['quote'].replace('\n','\n> '),''])
    (folder/'comparison.md').write_text('\n'.join(lines),encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
