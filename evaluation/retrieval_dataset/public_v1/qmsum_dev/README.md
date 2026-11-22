# QMSum 개발 분할의 고정 후보 재정렬

F05 질문에서 팀 RRF보다 첫 관련 발화를 자주 1위에 놓으면서, 상위 5개의 근거 범위 회수율을 유지할 수 있는지 비교한다. 제품 기본값과 공식 test 분할은 이번 실험의 변경·선택 대상에서 제외했다.

## 개발셋 측정 결과

공식 개발 회의 35개에서 필터를 통과한 질문 235개를 평가했다. 고정 후보 안에 정답 발화가 하나 이상 있는 질문은 185개다. 차이는 현재 RRF 대비 퍼센트포인트(%p)이며 대괄호 안은 대응 95% 구간이다.

| 방법 | Hit@1 | Δ Hit@1 [95% CI] | 범위 Recall@5 | Δ Recall@5 [95% CI] | MRR@5 | 1위 획득 / 상실 |
|---|---:|---:|---:|---:|---:|---:|
| 현재 RRF | 42.55% | +0.00 [+0.00, +0.00] | 72.98% | +0.00 [+0.00, +0.00] | 0.5397 | 0 / 0 |
| Sparse | 36.17% | -6.38 [-12.44, -0.79] | 69.79% | -3.19 [-7.77, +1.10] | 0.4828 | 19 / 34 |
| Dense | 42.55% | +0.00 [-3.56, +3.48] | 71.49% | -1.49 [-4.45, +1.53] | 0.5372 | 10 / 10 |
| Cross-encoder · 전체 후보 | 41.70% | -0.85 [-6.25, +4.37] | 73.19% | +0.21 [-2.26, +2.69] | 0.5417 | 30 / 32 |
| Sparse · RRF 상위 5개 내부 | 36.17% | -6.38 [-12.44, -0.79] | 72.98% | +0.00 [+0.00, +0.00] | 0.4957 | 19 / 34 |
| Cross-encoder · RRF 상위 5개 내부 | 41.70% | -0.85 [-6.05, +4.17] | 72.98% | +0.00 [+0.00, +0.00] | 0.5423 | 28 / 30 |
| 명시 화자 우선 · RRF 상위 5개 내부 (탐색) | 42.13% | -0.43 [-1.38, +0.00] | 72.98% | +0.00 [+0.00, +0.00] | 0.5350 | 0 / 1 |

세부 지표와 회의 단위 신뢰구간은 [metrics.json](metrics.json)에 있다.

## 입력과 순위

- 공식 ALL/val.jsonl과 기존 공개 평가의 specific-query 필터를 사용한다. 회의가 끝난 뒤 해당 회의 전체를 검색한다. 질문과 발화 원문만 점수화하며 정답 요약, 범위 주석, 주제 목록은 모델에 제공하지 않는다. 개발 파일 SHA-256은 fc7444e241bdbe6997c01720d07f1a58b7357284acb73f909766e5a4700db49f다. [원본](https://github.com/Yale-LILY/QMSum/blob/83d7768c1f2b4dfeb091385d3dc7e239b8e5bb7e/data/ALL/jsonl/val.jsonl)
- 팀 기본 프로필로 dense 상위 4개와 sparse 상위 4개 청크를 검색한다. 실제 RRF 순위에서 동일 발화의 첫 등장만 남긴 목록이 그 질문의 고정 후보다. 모든 비교 방법은 이 목록 전체의 순열이다. 후보 추출 뒤 각 채널의 점수를 같은 전체 회의 색인으로 조회해, 다른 채널에서 들어온 후보도 실제 점수로 비교한다. 한 발화의 여러 후보 청크에는 해당 채널의 최대 점수를 준다. 동점은 RRF 순서를 유지한다.
- sparse와 dense는 각각 해당 점수로 전체 후보를 정렬한다. cross는 사전학습된 MS MARCO MiniLM-L6 cross-encoder가 질문과 발화(화자 포함)를 함께 읽고 출력한 logit으로 전체 후보를 정렬한다. 입력 상한은 512토큰이며 긴 발화는 뒤를 자른다. 회의 문맥 추가, 미세조정, 정답 기반 가중치 탐색은 수행하지 않았다. [Cross-encoder 고정 버전](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2/tree/233902d25c440f23af6f7d6e94d2946bac0bee0a)
- 주 비교 방법 cross_top5는 현재 RRF 상위 5개의 구성원을 고정하고 그 안에서만 cross 점수로 정렬한다. sparse_top5도 동일한 제약을 사용한다. 두 방법의 Recall@5는 모든 질문에서 RRF와 같아야 한다. Recall의 동일성은 상위 5개 집합을 고정한 데서 따른다. 이번 단계는 예산 절단 전 검색 순위를 평가한다.
- Hit@1은 첫 발화가 어느 정답 범위에라도 속한 질문 비율이다. Recall@5는 상위 5개에 적어도 한 발화가 포함된 정답 범위의 비율을 질문별로 구한 뒤 평균한다. all5는 모든 주석 범위에 닿은 질문 비율이다. 대응 차이의 95% 구간은 회의 단위로 10,000회 재표집한 percentile 구간이다(seed 20261122). 주 비교를 제외한 방법은 진단용이고 다중 비교 보정은 없다.

탐색 비교에서는 질문이 “What did (the) X …”로 시작하고 회의의 화자 이름 또는 역할 하나만 명시할 때 해당 화자의 발화를 RRF 상위 5개 안에서 먼저 배치했다. 그룹 안의 RRF 순서는 보존했다. 이 규칙은 초기 비교를 본 뒤 추가했다. 1위 발화가 바뀐 문항은 6개이며 독립 검증이 필요하다.

## 재현

기존 팀 실험과 같은 Python 환경, MiniLM 임베딩과 Qwen 토크나이저를 사용한다. RAW에는 위 원본을 meetings.jsonl로 저장한다. 공용 GitBugs·QMSum test 평가와 충돌하지 않도록 CACHE는 별도 개발 전용 경로로 지정한다. 아래 명령은 public_v1 디렉터리에서 실행한다.

```sh
export PYTHONPATH="$(git rev-parse --show-toplevel)"
python dev_candidates.py --raw "$RAW" --cache "$CACHE" --output qmsum_dev --tokenizer "$QWEN_TOKENIZER" --model "$TEAM_EMBEDDING"
python dev_rerank.py --raw "$RAW" --encoder "$CROSS_ENCODER" --out qmsum_dev
python dev_rerank.py --score-only --out qmsum_dev
```

[candidates.jsonl](candidates.jsonl)은 질문별 고정 풀과 sparse·dense 점수, [cross_scores.jsonl](cross_scores.jsonl)은 교차 인코더 점수다. [rankings.jsonl](rankings.jsonl)에 모든 방법의 문항별 순위가 있으며 [gold.jsonl](gold.jsonl)은 채점용이다. 회의·질문 ID는 val 파일 내 행 기준이므로 test 파일에서 같은 이름의 ID와 혼용하지 않는다.
