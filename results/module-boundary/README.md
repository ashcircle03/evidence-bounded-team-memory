# 모듈 입출력 수정 결과

**입출력 경계 수정은 채택한다. 기존 QA와 사실 정정은 유지됐지만 재검토 의미 분류는
해결되지 않았다.** 모델 교체나 학습은 하지 않았다. 추가 모델 단계도 없다.

[설계·레퍼런스](../../docs/module-boundary-design.md) · [고정 프로토콜](v1/runtime/PROTOCOL.md) · [판단](v1/decision.json)

## 변경과 검증

- 문장 선택기의 원문 offset을 저장까지 전달한다. 반복되는 동일 문장의 다른 위치를 잘못 연결하지 않는다.
- 잘못된 후보 하나 때문에 정상 사실 정정까지 버리던 배치 처리를 후보별 검증으로 바꿨다.
- 비교 호출 timeout을 실패 receipt로 남긴다. 원문은 유지되고 QA가 계속 동작하며 실패를 빈 정상 결과로 표시하지 않는다.
- 재검토 승인은 재검토 허가로 전달한다. 사실 정정·결정 폐기·실험 성공과 구분한다.
- 과거 상태 인용의 렌더링을 보존하고 새 재검토 스냅숏만 v2로 만든다.

관련 계약·회귀 검사 **77개 통과**. 기존 v1 상태 인용13개도 정확히 같은 구절로
복원됐다. 올바른 재검토 후보를 제공한 서비스 검사는 승인 → 재시작 → QA까지
효과 전달과 기존 사실 보존을 확인했다. **관계 선택을 fixture로 준 연결성 검사이며
Qwen의 분류 성능으로 세지 않는다.**

## 실제 Qwen 실행

같은 Qwen3-8B revision, nonthinking/temp0, 같은 입력37개와 기존 정답 기준.
Slurm **120445, COMPLETED / 0:0**, GPU1·conda·12시간 상한, 지정 없이 g8에 배정.
실제 할당17분38초(17.63 GPU분), 프로그램650.65초, 모델 호출222회, 유료 API0회.
MaxRSS는 batch 행의2,802,396K이며 GPU 메모리 피크 측정값은 아니다.

| 평가 | v3b | 이번 수정 |
|---|---:|---:|
| 기존20, 핵심 답+필요 원문 근거 | 20/20 | 20/20 |
| 상태8, 정정 관계·값·투표 상태 인용 보존 | 8/8 | 8/8 |
| 같은 상태8, 양쪽 원문 직접 인용까지 엄격히 충족 | 7/8 | 7/8 |
| 알려진 합성 흐름11, 답+엄격한 필요 근거 | 8/11 | 8/11 |
| 추가 합성6, 답+필요 근거 | 6/6 | 6/6 |
| 재검토 양성2, 올바른 재검토 종류와 근거 | 0/2 | 0/2 |
| 근접 음성2, 불필요 제안 발생 | 2/2 | 2/2 |

**37개 최종 답 문자열과 답/근거 객체, 11개 제안 목록이 이전 실행과 모두 동일**하다.
새 실제 모델 출력을 대조한 결과이며 과거 출력 재생으로 대신한 것이 아니다.
동일한 답·근거이므로 기존의 원문 기반 의미 판정을 승계했다. 독립 평가자의 새
채점은 아니다. Cedar pending의 새 보고서 직접 인용 누락도 그대로 남아 있다.
기존20의 key 위치 정확 일치는19개이며 나머지 grep.extendedRegexp는 같은 파일의
인접 근거 문단을 검토해 인정한 이전 기준을 유지한다.

초기 QA 요청37개와 비교 요청11개는 모두 이전과 정확히 같다. 전체222개 요청 중
220개가 같다. 두 후속 재작성 요청은 앞 단계 judge의 설명 문구가 달라졌지만 판정
라벨은 같았고 최종 답·근거도 같았다. 모든 내부 출력이 동일한 것은 아니다.
[대조](v1/comparison.json) · [두 요청의 차이](v1/request-differences.json).

입력·코드 해시와 종료 상태를 확인했고 원문 근거53개, 상태 근거13개의 출처·범위·
원문 일치를 검증했다. [검증](v1/verification.json) · [전체 질문·답·근거](v1/cases.md) ·
[원출력](v1/result.json) · [실제 HTTP 호출](v1/calls.jsonl) · [자원 기록](v1/dispatch.json).

## 남은 문제와 판단

Writer의 version4→5 변화와 Cache의 보존 정책 변경을 Qwen은 여전히 correction으로
분류한다. 두 근접 음성에도 불필요한 correction을 제안한다. 이전 결정의 이유가
바뀌는 것과 과거 관측 자체가 틀린 것을 구분하지 못한 **비교 모델 단계의 오류**다.
입출력 수정으로 이 분류 문제가 해결됐다고 주장하지 않는다.

이번 실제37개에서는 모델이 올바른 reconsider를 생성하지 않았으므로, 새
`reconsideration_effects`를 실제 Qwen QA가 정확히 해석하는 성공 사례는 확보하지
못했다. 계약 검사의 통과 범위를 넘겨 해석하면 안 된다. 현재 채택은 출처·실패·상태
연결의 수정에 한정한다. 모델 교체/학습은 별도 선택으로 남겨 둔다.

이 집합은 반복 사용한 개발/회귀 사례다. 기존20에 자연 EverMem3문항이 포함되지만
EverMemBench, WikiContradict, STALE 전체 벤치마크나 일반화 성능을 의미하지 않는다.

## 재검증

```sh
TOKENIZERS_PARALLELISM=false .venv/bin/python -m unittest \
  tests.test_comparison_contract tests.test_timeline tests.test_service \
  tests.test_reference_review_citations tests.test_reference_state_boundary \
  tests.test_reference_contracts tests.test_reference_qa \
  tests.test_source_patch tests.test_decision_patch -q
.venv/bin/python -m evaluation.service_completion.verify results/module-boundary/v1
.venv/bin/python -m evaluation.service_completion.compare_boundary
.venv/bin/python -m evaluation.service_completion.summarize results/module-boundary/v1
```

첫 명령은 로컬 mock/계약 검사다. 나머지는 회수된 실제 실행 자료의 검증·집계이며
모델을 새로 실행하지 않는다. 기존 작업을 재제출하지 않는다.
