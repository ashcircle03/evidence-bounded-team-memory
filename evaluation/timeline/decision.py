"""Apply the predeclared adoption rule and expose paired QA losses/root causes.

This only summarizes frozen scores. It never changes grading or inference.
"""
from collections import Counter
import json
from pathlib import Path
from .build import HERE, ROOT, write

OUT=ROOT/'results/timeline'


def choose(direct, indexed, losses, audit):
    checks=dict(more_grounded_reviews=indexed['grounded_reviews']>direct['grounded_reviews'],
                no_more_unsupported_alerts=indexed['unsupported_alerts']<=direct['unsupported_alerts'],
                no_paired_qa_loss=not losses,
                no_raw_loss=audit['raw_source_losses']==0,
                no_unreviewed_promotion=audit['unreviewed_promotions']==0)
    return dict(selected='indexed' if all(checks.values()) else 'direct',checks=checks)


def analyze(rows, generations, keys, audit, summary):
    paired={};gains=[];losses=[];by_mode={}
    for cid in sorted(keys):
        d,i=rows[cid+'/direct'],rows[cid+'/indexed']
        assert set(d['qa'])==set(i['qa'])==set(keys[cid]['qa'])
        qg=[q for q in d['qa'] if not d['qa'][q]['correct'] and i['qa'][q]['correct']]
        ql=[q for q in d['qa'] if d['qa'][q]['correct'] and not i['qa'][q]['correct']]
        gains += [cid+'/'+q for q in qg];losses += [cid+'/'+q for q in ql]
        paired[cid]=dict(type=keys[cid]['kind'],review_gain=not d['grounded_review'] and i['grounded_review'],
                        review_loss=d['grounded_review'] and not i['grounded_review'],qa_gains=qg,qa_losses=ql)
    for mode in ('direct','indexed'):
        selected=[r for r in rows.values() if r['mode']==mode]
        types={};checkpoints={};failures=[];repeat_alerts=[];promotion_context=[]
        for kind in ('reconsider','coexist','conflict','correction','irrelevant'):
            rs=[r for r in selected if r['type']==kind]
            types[kind]=dict(streams=len(rs),required_reviews=sum(r['expected_review'] for r in rs),
                            grounded_reviews=sum(r['grounded_review'] for r in rs),
                            unsupported_alerts=sum(r['unsupported_alerts'] for r in rs),
                            qa_correct=sum(r['qa_correct'] for r in rs),qa_total=sum(r['qa_total'] for r in rs))
        for q in next(iter(keys.values()))['qa']:
            checkpoints[q]=dict(correct=sum(r['qa'][q]['correct'] for r in selected),total=len(selected))
        for r in selected:
            cid=r['id'];s=generations[cid+'/'+mode];key=keys[cid]
            review=next((x['result'] for x in s['steps'] if x['op']=='review'),None)
            for q,item in r['qa'].items():
                if item['correct']:continue
                cause=('missing_qualifying_proposal_prevented_review'
                       if key['kind']=='correction' and q=='reviewed' and review and review['matched']==0
                       else 'invalid_model_output' if item['answer']['kind']=='invalid'
                       else 'answer_evidence_scope_or_status_error')
                failures.append(dict(case=cid,checkpoint=q,category=cause,errors=item['errors']))
            repeat_alerts += [dict(case=cid,proposal=a['proposal']) for a in r['alerts']
                             if a['proposal']['incoming']['source_id']==key.get('repeat_source')]
            if key['kind']=='correction':
                after=r['qa']['reviewed'];old_answers=[a for a in after['answer']['answers'] if a['source_id']==key['old']]
                promotion_context.append(dict(case=cid,review_matched=review['matched'],
                    after_review_correct=after['correct'],old_assertion_returned=bool(old_answers),
                    stale_after_actual_approval=bool(review['matched'] and old_answers),
                    unaffected_archive_correct=r['qa']['other_preserved']['correct']))
        regressions={q:[r['id'] for r in selected if r['qa']['natural_before']['correct'] and not r['qa'][q]['correct']]
                     for q in ('natural_after','natural_after_repeat')}
        by_mode[mode]=dict(types=types,checkpoints=checkpoints,qa_failures=failures,
              qa_failure_categories=dict(Counter(x['category'] for x in failures)),
              repeated_arrival_alerts=repeat_alerts,natural_qa_regressions=regressions,
              correction_workflows=promotion_context,
              ingest_errors_by_stage=dict(Counter(e['stage'] for r in selected for e in r['errors'])))
    return dict(**choose(summary['direct'],summary['indexed'],losses,audit),paired=paired,
                qa_gains=gains,qa_losses=losses,by_mode=by_mode,
                interpretation='Selection among these two prototypes on this controlled set, not proof of general reliability. Primary scores are unchanged; missing review versus downstream QA errors are diagnostic categories.')


def run():
    def read(path):return json.loads(path.read_text())
    rows=read(OUT/'final/rows.json');summary=read(OUT/'final/summary.json')
    generations=read(OUT/'final-generations.json')['streams'];keys=read(HERE/'final-key.json')
    audit=read(OUT/'final-audit.json');git=read(OUT/'final-git.json');legacy=read(OUT/'legacy-qa.json')
    assert audit['status']=='passed' and set(git)==set(generations)==set(rows)
    assert all(r['status']=='passed' and r['clones_converged'] and r['raw_sources_unchanged'] for r in git.values())
    assert legacy['historical_cases']==legacy['preserved']==20
    assert len(keys)==20 and len(rows)==40
    decision=analyze(rows,generations,keys,audit,summary)
    write(OUT/'decision.json',decision)
    labels={'direct':'원문 직접 읽기','indexed':'자동 결정 인용 색인 추가'}
    selected=labels[decision['selected']]
    lines=['# 누적 기록 최소 시스템: 설계 판단','',f'이번 비교에서 선택한 경로는 **{selected}**다.',
        '선택 근거는 사전에 고정한 재검토·불필요 제안·문항별 QA 보존 조건이다. 이 결과만으로 실제 팀 기록 전체에서의 신뢰성을 주장하지 않는다.','',
        '| 같은 Qwen2.5-14B, 같은 원문 접근권 | 원문 직접 읽기 | 색인 추가 |','|---|---:|---:|']
    for title,field,den in [('근거 있는 필요한 검토','grounded_reviews',12),('불필요한 검토 제안','unsupported_alerts',None),
                          ('답·출처·조건·상태가 맞는 QA 시점','qa_correct',140),('자연 QA 반복 확인','natural_qa_correct',60),
                          ('모델 호출 수','calls',None),('입력 토큰','input_tokens',None),('출력 토큰','output_tokens',None)]:
        values=[str(summary[m][field])+(f'/{den}' if den else '') for m in ('direct','indexed')]
        lines.append('| '+' | '.join([title,*values])+' |')
    lines += ['',f"색인 추가로 새로 맞힌 QA 시점은 {len(decision['qa_gains'])}개, 직접 읽기가 맞혔는데 잃은 시점은 {len(decision['qa_losses'])}개다.",
        '140개는 20개 흐름에서 질문을 반복한 평가 시점이다. 자연 질문은 20개이며 60개의 독립 문항으로 해석하지 않는다.',
        '', '채택 조건별 판정:']
    names={'more_grounded_reviews':'근거 있는 필요한 검토 증가','no_more_unsupported_alerts':'불필요 제안 비증가',
           'no_paired_qa_loss':'같은 QA 시점에서 기존 정답 손실 없음','no_raw_loss':'원문 손실 없음','no_unreviewed_promotion':'검토 없이 승인 상태로 승격하지 않음'}
    lines += [f"- {names[k]}: {'충족' if v else '미충족'}" for k,v in decision['checks'].items()]
    lines += ['', '두 경로가 공유하는 원문 보존·구절 단위 정정·검토 기록·출처 검사는 유지한다. 색인은 위 조건을 모두 충족할 때만 선택한다. 과거의 여러 단계 의미 검증 모듈은 이 비교의 기본 경로에 넣지 않았다.',
        '',f"실제 Qwen 입력·출력을 Git 두 복제본으로 재생한 {len(git)}개 흐름에서 입력 일치와 상태 수렴을 확인했다. 별도 3B 기존 QA는 20/20에서 답·상태·인용이 보존됐다. 이는 새로운 14B QA 성과를 대신하지 않는다.",
        '',f"이번 목표의 확인된 전체 Slurm 사용량은 {audit['gpu_seconds']/60:.2f} GPU분, CPU 전용 작업 경과 시간은 {audit['cpu_only_seconds']/60:.2f}분이다. 준비·실패 시도도 포함한다. 호출 구간 경과 시간은 직접 읽기 {summary['direct']['seconds']/60:.2f}분, 색인 추가 {summary['indexed']['seconds']/60:.2f}분이며, 이는 개별 방식에 할당한 GPU 시간과 같지 않다.",
        '', '합성 작업 기록 20개와 원문을 바꾸지 않은 EverMemBench-Dynamic topic 02의 근거 확인된 QA 20개를 결합했다. 검색 대상이 작은 원문 전체 읽기 비교이며, 실제 Git의 장기 기록이나 전체 공식 벤치마크의 성과가 아니다. 제안에 대한 의미 채점은 구현한 AI의 출처 검토이며 독립 평가자 일치도를 측정하지 않았다.',
        '', '작성자 승인은 조건이 맞는 실제 생성 제안에 대해서만 수행한 모의 사용자 행동이다. 승인 누락으로 원하는 최종 지식 상태에 도달하지 못한 실패와, 승인 이후 QA 실패는 [문항별 진단](decision.json)에 구분했다. 작성자 필드 검사는 실제 GitHub 계정 인증과 연결되어 있지 않다.',
        '', '[사용법](../../evaluation/timeline/README.md) · [고정 평가 기준](../../evaluation/timeline/PROTOCOL.md) · [사건별 답과 근거](cases.ko.md) · [원출력](final-generations.json) · [의미 채점](final/ratings.json) · [작업·해시 검증](final-audit.json) · [Git 재생](final-git.json)']
    (OUT/'README.md').write_text('\n'.join(lines)+'\n')
    inputs={r['id']:r for r in read(HERE/'final.json')}
    details=['# 사건별 판단·QA·인용','', '아래 원문 작업 기록은 합성이다. 자연 QA 원문과 질문은 별도 출처를 유지한다. 판정은 동결한 정답·기준을 적용했다.']
    def cell(value):return str(value).replace('|','\\|').replace('\n','<br>')
    for cid in sorted(keys):
        key=keys[cid]
        details += ['',f"## {cid}: {key['kind']}",'',f"기대 판단의 근거: {key['reason_criterion']}",
                    '',f"과거 원문: {key['old_text']}",'',f"새 원문: {key['new_text']}",
                    '', '| 방식 | 근거 있는 필요한 검토 | 불필요 제안 | QA 시점 정답 |','|---|---:|---:|---:|']
        for mode in ('direct','indexed'):
            r=rows[cid+'/'+mode]
            details.append(f"| {labels[mode]} | {int(r['grounded_review']) if r['expected_review'] else '대상 아님'} | {r['unsupported_alerts']} | {r['qa_correct']}/{r['qa_total']} |")
        for mode in ('direct','indexed'):
            details += ['',f"### {labels[mode]}의 관계 제안",'']
            relations=rows[cid+'/'+mode]['relations']
            if not relations:details.append('생성된 관계 제안 없음.')
            for item in relations:
                p=item['proposal']
                details += [f"- `{p['kind']}` / 출처·설명 판정: {'근거 있음' if item['grounded'] else '기준 미충족'}", 
                            f"  - 설명: {p['reason']}",f"  - 과거 인용: {p['previous']['quote']}",f"  - 새 인용: {p['incoming']['quote']}"]
        details += ['', '### 질문별 실제 답과 인용','', '| 시점·질문 | 방식 | 정답 판정 | 실제 출력 |','|---|---|---|---|']
        for step in inputs[cid]['steps']:
            if step['op']!='ask':continue
            for mode in ('direct','indexed'):
                q=rows[cid+'/'+mode]['qa'][step['id']];answer=q['answer']
                texts=[f"종류: {answer['kind']}"]
                for a in answer['answers']:
                    texts.append(f"답: {a['answer']}; 상태: {a['status']}; 조건: {(a.get('condition') or {}).get('quote','')}; 인용: {a['quote']}; 출처: {a['location']} [{a['start']}:{a['end']}]")
                if answer.get('error'):texts.append('검증 오류: '+answer['error'])
                details.append('| '+' | '.join(map(cell,[step['id']+': '+step['question'],labels[mode],
                                        '맞음' if q['correct'] else ', '.join(q['errors']),'<br>'.join(texts)]))+' |')
    (OUT/'cases.ko.md').write_text('\n'.join(details)+'\n')
    print('selected',decision['selected'],'QA gains',len(decision['qa_gains']),'QA losses',len(decision['qa_losses']))


if __name__=='__main__':run()
