"""Render the offline audit into the case ledger, stratified counts and decision."""
from collections import Counter
import json
from pathlib import Path

OUT = Path('results/record-binding/first-loss')


def clean_trials(doc, key):
    return {tuple(r['edge']) for r in doc[key] if not (
        r['lost_stances'] or r['lost_edges'] or r['lost_content'] or r['added_fp'] or r['stance_delta']<0)}


def table(rows):
    return '\n'.join('| '+' | '.join(map(str,row))+' |' for row in rows)


def main():
    docs=json.loads((OUT/'audit.json').read_text())
    counts={}
    for d in docs:
        for e in d['edges']:
            key=(d['panel'],e['first_loss'])
            counts.setdefault(key,[]).append(d['id'])
    report=['# 68문서 records 실패표','',
        '문서 ID는 고정 평가셋의 ID다. 각 행 아래에 모든 필수 연결과 기존 오연결을 추적했다. 원문 위치는 문자 단위 반개구간 [시작, 끝)이다. 목록에 여러 위치가 있으면 gold가 보존한 원문 출현 위치를 모두 표시한다. 그룹 소유권은 저장 당시의 범위다. 복수 주장이 있는 그룹은 개별 대상을 확정할 수 없다. 상세 원출력 행, 원문, 그룹과 뒤 모듈에 전달된 구절은 [audit.json](audit.json)에 있다.','',
        '| 문서 | 난도 / 근거 | 저장 | 정답 / 필수 연결 | 오연결 | 첫 손실별 연결 수 |','|---|---|---|---:|---:|---|']
    for d in docs:
        c=Counter(e['first_loss'] for e in d['edges'])
        report.append('| '+' | '.join([d['id'],d['difficulty']+' / '+d['availability'],d['storage_status'],
            f"{c.pop('retained',0)} / {len(d['edges'])}",str(len(d['incorrect'])),str(dict(c))])+' |')
    for d in docs:
        report+=['','## '+d['id'],'',d['source_text'],'',
            '| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |','|---|---|---|---|---|']
        for e in d['edges']:
            loc=lambda k:', '.join(f"{s['start']}–{s['end']}" for s in e[k])
            group_status=', '.join(g+(' (대상 불명확)' if len(d['reader_packets'][g]['received']['assertions'])>1 else '') for g in e['reader_packets'])
            report.append('| '+' | '.join([' / '.join(e['edge']),loc('target_positions')+' → '+loc('context_positions'),
                str(e['raw_target_rows'])+' / '+str(e['raw_context_rows']),e['first_loss'],group_status or '구조화 연결 없음'])+' |')
        for fp in d['incorrect']:
            for origin in fp['origins']:
                rows=[r for r in d['raw'] if r['id'] in origin['raw_row_ids']]
                report+=['',f"- 오연결 {fp['scored_edge']} · {fp['reason']} · {origin['target_status']}. "+
                    ' / '.join(f"원출력 {r['id']} {r['role']} {r['text']!r} [{r['start']}, {r['end']})" for r in rows)+
                    ' → 저장 및 reader '+origin['group']]
    (OUT/'cases.md').write_text('\n'.join(report)+'\n')
    strata=[['난도','근거','문서','필수 조건·이유','선택 가능','구절 추가로 선택 가능','기존 역할 교정 복구 (문서/연결)','기존 대상 교정 복구 (문서/연결)'],['---']*8]
    synthetic=[d for d in docs if d['panel']=='balanced_synthetic']
    for diff in ('easy','medium','hard'):
        for av in ('full','partial','none'):
            ds=[d for d in synthetic if (d['difficulty'],d['availability'])==(diff,av)]
            os=[o for d in ds for o in d['oracles']]
            def repairs(key):
                counts=[len(clean_trials(d,key)) for d in ds]
                return f'{sum(n>0 for n in counts)} / {sum(counts)}'
            strata.append([diff,av,len(ds),len(os),sum(bool(o['eligible_pairs']) for o in os),
                sum(o['gold_context_only'] for o in os),repairs('baseline_role_trials'),repairs('baseline_target_trials')])
    (OUT/'strata.md').write_text('# 합성 자료의 난도·근거 가용성별 비교\n\n'+table(strata)+
        '\n\nnone은 조작한 중심 주장의 근거 가용성이다. 문서 안의 다른 주장에는 필수 근거가 있을 수 있다. 역할·대상 교정은 한 번에 한 행을 바꾼 결과이며 같은 문서의 효과를 더하지 않는다.\n')
    stats=[['최초 손실 또는 보존','합성 문서/연결','자연 문서/연결'],['---']*3]
    for cause in sorted({k[1] for k in counts}):
        row=[cause]
        for panel in ('balanced_synthetic','natural_audit'):
            ids=counts.get((panel,cause),[]);row.append(f'{len(set(ids))} / {len(ids)}')
        stats.append(row)
    (OUT/'loss-counts.md').write_text('# 모든 필수 관계의 최초 관측 손실\n\n'+table(stats)+
        '\n\nretained는 고정 평가에서 맞고 기록 그룹이 reader에 전달된 경우다. whole_record_rejected는 원출력 채점에서 맞았으나 저장 실패로 사라진 경우다. 같은 실패 문서라도 원출력에서 이미 틀린 연결은 먼저 관측된 추출 오류로 센다. raw_to_graph는 정답 원출력이 저장 변환 중 사라지는 경우다. target_missing_or_split과 context_missing_or_split은 일치하는 단일 구절 없음, context_inside_target은 대상과 분리된 근거 구절 없음이다. role_assignment는 같은 그룹에 있는 근거 역할, target_assignment는 역할이 있는 근거의 대상이다. target_and_role_or_unresolved는 두 문제를 분리해 귀속할 수 없는 경우다. 전송은 해당 기록을 지정해 호출한 reader 경로에서 확인했다.\n')
    assert len(docs)==68 and sum(len(d['reader_packets']) for d in docs)==192

if __name__=='__main__':
    main()
