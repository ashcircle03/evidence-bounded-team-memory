"""Report fixed-score results without modifying labels or predictions."""
from pathlib import Path
import json


def pct(x):return '—' if x is None else f'{x*100:.1f}%'


def main():
    out=Path('results/record-causal/v1');r=json.loads((out/'storage-evaluation.json').read_text())
    lines=['# Records: 원인별 수정과 고정 평가', '',
           '**채택: 기존 grouped 원출력의 개별 상태를 보존하는 저장 수정. 부분 복구는 옵션이며 기본 채택하지 않는다.**', '',
           '새로 생성한 문장을 기존 정답에 맞춰 합치지 않았다. 첫 비교는 같은 Qwen3-8B 실제 원출력 68개를 그대로 두고 저장 단계만 순차적으로 변경했다. 정답·평가기준·난이도/근거 분포는 유지했다. 합성 54개와 자연 14개를 나눠 보고한다.', '',
           '## 저장기만 바꾼 비교', '',
           '| 패널 | 경로 | 필수 내용 재현 | 연결 P / R / F1 | 오연결 | 잘못된 상태 | 전체 문서 정답 | 저장 중 내용 손실 |',
           '|---|---|---:|---|---:|---:|---:|---:|']
    names={'original':'기존','attributes':'개별 속성 보존','quarantine':'+ 항목 격리(옵션)'}
    for s in r['summary']:
        m=s['metrics'];e=m['typed_edges'];n=m['content_recall']
        lines.append(f"| {s['panel']} | {names[s['stage']]} | {n['tp']}/{n['tp']+n['fn']} ({pct(n['recall'])}) | {pct(e['precision'])} / {pct(e['recall'])} / {pct(e['f1'])} | {e['fp']} | {s['stance_wrong']} | {s['complete']}/{s['n']} | {s['storage_lost_nodes']} |")
    lines += ['', '### 기존 정답 보존', '',
              '| 비교 | 보호 내용 | 보호 연결 | 보호 상태 | 잃은 내용/연결/상태/전체 문서 |',
              '|---|---:|---:|---:|---|']
    for label in ('original→attributes','attributes→quarantine','original→quarantine'):
        ps=[p for p in r['protection'] if p['comparison']==label]
        lines.append(f"| {label} | {sum(p['protected_nodes'] for p in ps)} | {sum(p['protected_edges'] for p in ps)} | {sum(p['protected_stances'] for p in ps)} | {sum(len(p['lost_nodes']) for p in ps)} / {sum(len(p['lost_edges']) for p in ps)} / {sum(len(p['lost_stances']) for p in ps)} / {sum(p['lost_complete'] for p in ps)} |")
    lines += ['', '기존 완전 정답 23개는 모두 유지했다. 개별 속성 보존으로 새로 완전 정답이 된 문서는 e04-full, e04-partial, m04-partial, h04-partial이다. 자연 기록 전체 정답은 여전히 0/14다.', '',
              '원인이 저장기라는 주장은 같은 원출력에서 상태만 달라지는 것으로 확인했다. 부분 격리는 7개 실패 문서 중 6개를 partial로 복구했지만, 모델 원출력에 있던 잘못된 관계도 5개 추가 노출했다. 그러므로 추가 정보 회복을 의미 정확도 개선으로 포장하지 않고 기본 옵션을 끈다. h05-partial의 중복 claim identity 문제는 아직 failed로 남긴다.', '',
              '## 실제 입력 범위 단일 변수 비교', '']
    window=out/'window-evaluation.json'
    if window.exists():
        w=json.loads(window.read_text())
        lines += [f"별도 실제 Qwen job {w['job_id']}, 새 68회 호출. 기존 bound122986의 지시문·예시·모델·출력 한도는 그대로 두고 SOURCE의 sentence segments만 문서 전체 한 범위로 바꿨다. 이 비교는 **원출력 평가**이며 새 운영 그래프/QA 결과로 해석하지 않는다.", '',
                  '| 패널 | 입력 범위 | 내용 재현 | 연결 F1 | 오연결 | 문서 전체 정답 |',
                  '|---|---|---:|---:|---:|---:|']
        for s in w['summary']:
            if s['difficulty']!='all':continue
            m=s['metrics'];n=m['content_recall'];e=m['typed_edges']
            lines.append(f"| {s['panel']} | {s['arm']} | {n['tp']}/{n['tp']+n['fn']} | {pct(e['f1'])} | {e['fp']} | {s['complete']}/{s['n']} |")
        p=w['preservation'];cal=w['identical_request_controls']
        lines += ['', f"기존 bound 원출력에서 맞힌 내용 손실 {sum(len(x['lost_nodes']) for x in p)}개, 연결 손실 {sum(len(x['lost_edges']) for x in p)}개, 완전 정답 문서 손실 {sum(x['lost_complete'] for x in p)}개. 같은 요청이었던 대조 {len(cal)}건 중 원출력 동일 {sum(x['identical_raw'] for x in cal)}건.",
                  f"정확한 원문 위치 정렬 실패 {w['alignment_rejections']}항목. 종료 사유 {w['finish_reasons']}. 토큰 {w['cost']}. 상세 채점은 `window-evaluation.json`과 실제 `.calls.jsonl`에 보존했다.", '']
    else:
        lines += ['아직 실행/검증 중이다. 완료 전 성능을 추정하지 않는다.', '']
    lines += ['## 재현과 범위', '',
              '- 관련 계약 검사 98개 통과; 저장 경로 3개 × 문서 68개 = 204개 실제 append→재시작→reader 전달 확인.',
              '- 기존 grouped 68개 저장 후 점수를 고정 v3 평가기로 정확히 재현했다. 개별 stance 보호 집계는 frozen scorer의 매칭/기여 규칙으로 검증했고, 보완 전후 모든 사례 점수가 같음을 확인했다.',
              '- 이 문서의 “올바른 상태”는 추출 assertion의 stance다. 시스템 승인 상태를 새로 적용하거나 평가한 것이 아니다.',
              '- 합성 54개는 18개 이야기 × 근거 변형이다. 자연 14개는 5개 실패 사례에서 선택했다. 독립·대표 표본이나 held-out 성능으로 주장하지 않는다.',
              '- 부분 복구도 모델 원출력의 의미 오류를 고치지 않는다. QA 20문항을 새로 실행한 작업이 아니며, 이번 결과를 QA 성능으로 바꾸어 말하지 않는다.', '',
              '## 코드와 증거', '',
              '- [실패별 실제 레퍼런스 구현·작동 전제](../../../docs/records-reference-fit.md)',
              '- [수정된 records 경로 사용법](../../../docs/modules/records-preserving.md)',
              '- [모든 실패의 단계별 목록](failure-index.md), 전체 실제 입력/원출력 `failure-traces.json`',
              '- [저장 비교](storage-evaluation.json), [보존 검증](storage-verification.json)',
              '- [고정 프로토콜](../../../evaluation/record_causal/PROTOCOL.md)',
              '- `initial-freeze.json`, `storage-freeze.json`, `window-freeze.json`, `references.json`', '']
    (out/'README.md').write_text('\n'.join(lines))


if __name__=='__main__':main()
