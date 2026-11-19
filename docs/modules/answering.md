# answering — 근거별 답변과 제한된 추가 검사

[공통 계약](README.md) · 구현 소유: `readers/checking.py`, `attribution.py`, `citations.py`와 생성 부분 · [실제 adapter](../../team_memory/adapters/answering.py)

입력 `answer.generate`: bundle 하나. 출력 answer: snapshot_id, outcome, claims, reason. claim은 id·text·kind·evidence_ids·conditions·alternative_group을 가진다. 모델·ConflictScore·답변 수정·AQA 선택은 내부 구현이다. 다른 담당자가 이 내부 호출 순서를 알아야 포트를 사용할 수 있는 구조는 피한다.

v1.1 실제 어댑터는 original_text, unattributed, claim별 answer_span도 반환한다. 기존 답의 무인용 문장을 삭제하거나 근거를 임의로 복제하지 않고 공개 응답에 남기기 위해서다. [무손실 변환 명세](runtime.md#v11-답을-버리지-않는-주장별-변환).

| claim kind | 의미 | 필수 근거 |
|---|---|---|
| reported_fact | 원문에서 보고한 내용 | source evidence |
| state | 제안/승인/거절/유효 상태에 대한 진술 | review_state evidence; 값 설명에는 해당 source도 연결 |
| inference | 여러 근거를 종합한 추론 | 근거 IDs, 추론임을 유지 |
| uncertainty | 근거 부족·불확실성 설명 | 근거가 있으면 연결; 없으면 생략 가능 |

권한 `answer:generate`. 원문·제안·승인 상태를 쓰거나 최신값을 재판정할 권한은 없다. 추가 검사는 답변 claim의 문구·조건·출처를 수정할 수 있고 records의 상태를 수정할 수 없다. 검사에 실패한 claim을 제거할 때 살아 있는 다른 claim의 인용을 잃지 않는다.

outcome: answered / conditional / conflict / abstained / needs_clarification. 상충이면 같은 alternative_group 안에 양쪽 답과 서로 구분되는 근거가 있어야 한다. 미승인 정정은 현재값을 교체하지 않는다. 재검토 승인은 재실험 성공이나 새 결정 확정이 아니다. 질문에 무관한 상충은 해당 답을 차단하지 않는다. evidence가 없을 때는 이유를 가진 abstained가 정상이다.

### 직접 답과 조건부 답의 판정

질문이 요구하는 결론을 먼저 정한다. 질문이 적용 조건을 이미 지정했거나, 기록된 조건들에서 결론이 하나로 정해지면 `answered`다. 직접 답에도 적용 범위와 상태 근거는 남긴다. 질문 범위 안에서 어떤 조건을 적용하느냐에 따라 지지되는 결론이 달라지면 `conditional`이다. 각 분기의 조건·결론·근거를 함께 반환한다. 조건 단어의 개수, 인용 수, 문장의 완곡한 표현은 판정 기준이 아니다. 같은 조건에서 근거가 양립 불가능하면 기존 `conflict` 계약을 적용한다.

[공통 예제](../../examples/contracts/build_examples.py)는 같은 v1·v2 발언과 같은 재검토 승인 이벤트에서 질문 텍스트만 바꾼다.

| 질문 | outcome | 근거 있는 결론 |
|---|---|---|
| 재검토 승인이 곧 병렬 실행 채택인가? | answered | 아니다. 승인 효과는 재검토 허가로 확정돼 있다. |
| v1에서 병렬 훅을 호출하면 어떻게 되는가? | answered | v1에서는 충돌한다. v1 원문을 인용한다. |
| 병렬 훅의 보고된 동작은 버전에 따라 어떻게 달라지는가? | conditional | v1은 충돌, v2는 해당 문제 수정. 서로 다른 원문을 각 분기에 인용한다. |

원문 구절 일치 검사는 인용 조작을 막지만 의미 지지를 보장하지 않는다. 문서 ID 집합이 겹친다고 두 주장 모두 지지된 것으로 처리하지 않는다. 여러 값을 묶은 claim이 조건을 잃으면 별도 claim으로 분리한다. 내부 지원/반박 판단·문구 수정·대안 보완 결과는 진단으로 기록하고 주장별 지지 정확도와 별도로 평가한다.

공통 검사: pending/current, approved correction/owner 유지, conflict 양쪽, unrelated conflict, reconsideration 효과 제한, no-evidence 보류, 없는 인용·source/state 혼동 거절. 실제 Qwen 입력/출력, 문장 의미와 인용 entailment, 기존 QA20·상태/인용8·EverMem은 별도 실행이다. 이번 계약 작업에서 재추론했다고 보고하지 않는다.
