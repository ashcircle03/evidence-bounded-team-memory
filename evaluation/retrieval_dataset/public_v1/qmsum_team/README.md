# F05 팀 Retrieval 적용 결과

팀 프로필에서 기존 dense + BM25 RRF 후 상위 5개 청크에 이전 발화 + 중앙 발화 재정렬을 적용했다. 아래는 동결한 개발·테스트 설정을 실제 `RetrievalAdapter.execute('evidence.retrieve', ...)`로 실행한 결과다. 질문에는 주석과 정답 요약을 넣지 않았다.

| 분할 | 1위 적중 (RRF → 적용) | Δ Hit@1 %p [95% CI] | MRR@5 (RRF → 적용) | Δ MRR@5 [95% CI] | 범위 Recall@5 (양쪽) |
|---|---:|---:|---:|---:|---:|
| 개발, 35회의 235문항 | 100 → 111 (42.55 → 47.23%) | +4.68 [−0.91, +9.64] | 0.5397 → 0.5674 | +0.0277 [−0.0059, +0.0584] | 72.98% |
| 테스트, 35회의 242문항 | 99 → 127 (40.91 → 52.48%) | +11.57 [+5.02, +18.01] | 0.5702 → 0.6366 | +0.0665 [+0.0280, +0.1035] | 76.79% |

개발셋에서 선택한 설정으로 테스트에서 45문항을 새로 1위에서 맞히고 17문항을 놓쳐 순증 28건이었다. 두 분할 모두 문항마다 Recall@5 차이가 정확히 0이었고 대응 차이의 95% 구간은 [0, 0]%p다. 각 분할에서 회의를 함께 재표집해 문항별 평균 차이의 percentile 구간을 계산했다(10,000회, seed 20261122, 회의는 입력 순서). 지표는 근거 확장·예산 적용 전 순위 기준이다.

## 제품 경로 검증

- 문항별 `fused`와 `reranked` trace에서 상위 5개 **청크 ID와 중복 횟수**, 6위 이후 **청크 ID 순서**의 일치를 검사했다. 같은 발화의 여러 청크도 유지했다.
- 원래 RRF와 기존 저장 예측을 비교했다. 개발 기록의 고유 발화 규칙, 테스트 기록의 상위 5개 자리 규칙을 각각 사용했다. 재정렬한 상위 5개 발화 순서도 개발 235건과 테스트 242건 모두 동결 실험과 일치했다.
- 모든 요청에서 실제 첫 번째 evidence의 source ID가 새 1위와 일치했다. QMSum은 검토 제안이 없는 snapshot을 사용했고, 검증의 근거 예산은 256개였다. 답변 생성은 평가 범위 밖이다.

## 재실행

프로젝트 루트를 PYTHONPATH에 두고 public_v1에서 실행한다. 개발 원문과 고정 모델 버전은 [개발셋 기록](../qmsum_dev/README.md) 및 [테스트 기록](../qmsum_test_context/README.md)에 있다. 각 분할에 별도의 색인 캐시 경로를 사용한다.

```sh
export TEAM_MEMORY_RERANKER_PATH="$CROSS_ENCODER"
python validate_team_f05.py --split dev --raw "$RAW" --cache "$DEV_CACHE" --tokenizer "$QWEN_TOKENIZER" --model "$TEAM_EMBEDDING"
python validate_team_f05.py --split test --cache "$TEST_CACHE" --tokenizer "$QWEN_TOKENIZER" --model "$TEAM_EMBEDDING"
```

[개발 순위](dev-runs.jsonl) · [개발 지표](dev-metrics.json) · [테스트 순위](test-runs.jsonl) · [테스트 지표](test-metrics.json) · [런타임 설정](../../../../docs/modules/runtime.md)
