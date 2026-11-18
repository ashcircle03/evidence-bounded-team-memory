"""Render the focused judgments alongside all document-level regressions."""
from collections import Counter
import json
from pathlib import Path
import sys

ROOT=Path('results/record-binding/discourse-role')


def main(job):
    run=json.loads((ROOT/f'record-discourse-{job}.json').read_text())
    result=json.loads((ROOT/'evaluation.json').read_text())
    docs=result['cases']
    focused={'n03':'basis','n08':'condition'}
    lines=['# 단일 주장에 연결된 구절의 역할 교정','',
           '기존 Qwen3-8B 원출력으로 만든 68문서에서, 대상 주장이 하나인 그룹의 기존 구절만 고려했다. '
           '조건·이유·시간·subject 중 하나로 정렬된 40쌍(28문서)이 대상이다. 9쌍은 근거 구절이 대상 안에 있다. '
           '각 구절의 입력, 원출력 확률, 적용 결정과 점수는 [문서별 JSON](evaluation.json)에 있다.','',
           '| 사례 | 기존 역할 | 요구 역할 | 최고 확률 역할 | 조건 / 이유 / 유지 확률 | 적용 결정 | 복구 |',
           '|---|---|---|---|---|---|---|']
    for d in docs:
        if d['id'] not in focused:continue
        p,=d['pairs'];q=p['prediction'];keep,condition,basis=q['probs']
        lines.append(f"| {d['id']} | {p['old_role']} | {focused[d['id']]} | {q['argmax']} | {condition:.3f} / {basis:.3f} / {keep:.3f} | {q['decision']} | {d['recovered']} |")
    lines+=['','| 평가 집합 | 방식 | 정답 연결 | 오연결 | 완전 정답 문서 |','|---|---|---:|---:|---:|']
    for panel in ('전체','balanced_synthetic','natural_audit'):
        selected=[d for d in docs if panel=='전체' or d['panel']==panel]
        for key in ('before','after'):
            scores=[d[key] for d in selected]
            lines.append(f"| {panel} | {key} | {sum(s['typed_edges']['tp'] for s in scores)} | {sum(s['typed_edges']['fp'] for s in scores)} | {sum(s['complete'] for s in scores)}/{len(selected)} |")
    lines+=['',f"적용 기준 통과 여부는 **{result['accepted']}**. 실제로 바꾼 역할은 {sum(d['changed'] for d in docs)}개다. "
            f"새 오연결 {sum(len(d['new_fp']) for d in docs)}개, 기존 정답 연결 손실 {sum(len(d['lost']) for d in docs)}개. "
            f"기존 내용·주장·stance 손실은 각각 {sum(len(d['lost_content']) for d in docs)}, {sum(len(d['lost_claims']) for d in docs)}, {sum(len(d['lost_stances']) for d in docs)}개다. "
            f"{sum(d['reader_groups'] for d in docs)}개 저장 그룹을 재시작 후 reader까지 확인했다.",'',
            '## 학습과 적용 범위','',
            'DisCoDisCo의 방향 표시와 두 구절·주변 문장을 함께 쓰는 설계를 적용했다. 두 채널을 같은 MiniLM 인코더로 인코딩하고 첫 토큰 표현을 연결해 3종 역할을 지도학습했다. '
            '원 저자의 체크포인트를 재현한 실험은 아니다. [공식 reader](https://github.com/gucorpling/DisCoDisCo/blob/66b8c4e86543f0a14913f4b57f454be80e3bfba5/gucorpling_models/rel/flair_clone_dataset_reader.py) · [논문](https://aclanthology.org/2021.disrpt-1.6/)', '',
            'GUM 2021에서 condition은 조건, cause·purpose·motivation·justify·evidence는 이유, 나머지는 유지로 매핑했다. '
            '기존 역할은 분류기 입력에 넣지 않았다. corpus의 두 담화 단위와 달리 팀 기록에서는 대상 안의 구절도 입력한다. '
            'GUM 방향은 텍스트 순서에 따라 근거에서 대상 주장으로 지정한다. 프로젝트의 주변 문맥은 저장된 원문 window로 GUM의 단일 문장과 길이가 다를 수 있다. '
            '[고정한 공개 데이터](https://github.com/disrpt/sharedtask2021/tree/a9dac1afd9f9800c4fbe704b7ade839bf298c97f/data/eng.rst.gum)','',
            f"학습 {run['train_counts']}, 개발 {run['dev_counts']}. 시드 42, 3 epochs, 128 tokens/channel, AdamW 3e-5. "
            '개발셋에서 해당 클래스 10건 이상, 경험 정밀도 90% 이상인 고정 그리드의 최저 임계값만 허용했다. 기준 미달이면 기존 역할을 보존한다. '
            '팀 68문서의 정답은 채점에만 사용했다. 자연 14문서는 이전부터 조사했던 사례다.','']
    for label,v in run['calibration'].items():
        lines.append(f"- {label} 적용 임계값 {v['threshold']}. 전체 지점별 표본 수와 정답 수는 원출력 calibration에 있다.")
    lines+=['','## 68문서별 변화','','| 문서 | 후보 쌍 | 변경 수 | 복구 | 정답 손실 | 새 오연결 |','|---|---:|---:|---|---|---|']
    for d in docs:
        lines.append(f"| {d['id']} | {len(d['pairs'])} | {d['changed']} | {d['recovered']} | {d['lost']} | {d['new_fp']} |")
    (ROOT/'README.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':
    main(sys.argv[1])
