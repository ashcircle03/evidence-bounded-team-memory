# 공식 answering 포트의 변환 경계

공식 계약 예제의 bundle 4개와, 상충하는 문장 바깥의 두 구절을 인용한 파생 사례 1개를 사용했다. 각 사례에서 문장과 번호 인용을 고정한 decoder를 실제 AnsweringAdapter.handle에 주입했다. 이 검사는 생성 이후의 변환 및 생성기에 전달되는 필드를 분리해서 본다. 모델 성능 점수가 아니다.

| 사례 | 수정 전 | 수정 후 |
|---|---|---|
| 보류 중 정정 | 120ms 현재값과 90ms 제안·상태 인용은 유지, 두 claim의 조건은 빈 배열 | 동일 답·인용과 v1, CPU 조건 보존 |
| 소유자 질문, 같은 문서에 지연시간 충돌 | answered | answered |
| 두 문서의 충돌 범위 밖 구절을 각각 인용 | conflict | answered |
| 실제 지연시간 충돌의 양쪽 인용 | conflict | conflict |
| 재검토 승인과 기존 결정 | 계약 예제는 conditional, 실제 answered | answered로 남음 |

원문 인용의 문서 ID만 비교하던 부분을 실제 구절 위치의 겹침까지 확인하도록 수정했다. 구절이 너무 넓어 관련·무관한 주장을 모두 담으면 의미상 관련성은 여전히 미확정이다. 조건은 기존 bundle의 source별 목록을 팀 생성 입력으로 전달한다. claim에는 질문에 지정되어 있고 해당 claim의 모든 인용 원문이 공통으로 명시한 조건만 복원한다. 질의에 없는 조건이나 자연어 표현 사이의 함의는 이 규칙으로 결정하지 않는다.

재검토 사례에서 조건 표현은 질문의 “hook invocation”과 원문의 “parallel hook invocation”으로 다르고, 기존 생성 결과는 자유문과 인용 번호만 준다. 문장에 제약이 있다는 이유만으로 conditional을 부여하면 특정 상태를 묻는 직접 응답도 바뀔 수 있다. 후속 후보는 생성 결과에 답의 종류와 근거별 적용 조건을 직접 표현하고, 같은 고정 bundle에 대한 직접답·조건부답을 짝지어 평가하는 것이다.

기존 QA 20문항에서 요청이 일치할 때만 저장된 Qwen 응답을 재사용해 답 원문·인용 구절을 확인했다. 20/20 일치. 별도 상태·인용 8건은 이 재생에 포함되지 않는다.

[수정 전](before.json) · [수정 후](after.json) · [20문항 재생 결과](replay.json) · [진단 코드](../../evaluation/answering_port/conversion.py)

## 질문만 바꾼 계약 재검토

위 표는 당시 라벨을 사용한 최초 진단이다. [현재 answering 계약](../../docs/modules/answering.md)은 승인 효과가 하나로 확정되는 재검토 승인 질문을 answered로 정정했다. 동일 bundle에서 질문 텍스트만 바꾼 고정 생성문 검사에서, 승인 여부와 v1 동작 질문은 기대·실제 모두 answered였다. 버전별 동작을 함께 묻는 경우 두 답과 인용은 남지만 실제 outcome은 answered이고 분기별 conditions도 비어 있다. 계약 기대는 conditional이다. 이 확인은 생성 후 변환에 한정한다.

[QA 20문항 재생](outcome-contract/replay.json)은 실제 과거 Qwen 요청 130개를 정확히 매칭했다. [상태·인용 8건](outcome-contract/state8.json)은 기존 평가에서 정해 둔 사례와 각 시점의 투표 원본을 사용했다. 인용 보완까지 끝난 저장 답을 공식 포트의 출력 변환에 넣고, 답 원문·인용된 원문 구절 집합·상태 근거의 제안 ID와 상태가 유지되는지 검사했다. 이전 상태 인용의 원문도 재렌더링해 대조했다. 공식 포트의 상태 인용은 같은 이벤트를 현행 형식으로 표시한다. 8/8 보존이고 기존 기준의 엄격한 원문 직접 인용은 7/8이다. 이 검사는 새 생성이나 문장별 의미 재채점이 아니다. [실제 포트 출력](outcome-contract/port.json)

## 실제 Qwen 비교 기록

- 버전 비교 합성 사례의 답·조건·인용·outcome 동시 통과는 기존 경로 1/4, 조건별 답 경로 4/4였다. 같은 근거에 질문 표현을 두 가지로 바꾼 결과다. [채점과 입력](scoped-versions/README.md)
- 별도 도메인의 고정 근거 비교는 [채점 결과](domain-transfer/ratings.json)에 기록했다.
- 실제 Aimers 6문항의 [고정 근거 비교](team-question-pairs/ratings.json), [답변 전달 수정 후 재평가](team-question-pairs/delivery-isolated/ratings.json), [원문 저장부터 실행한 결과](team-question-pairs/end-to-end/ratings.json), [구간 추출 후보 실행 결과](team-question-pairs/segments/ratings.json)를 남겼다. 구간 추출 후보에서도 답·조건·인용·outcome 동시 통과는 0/6이었다. 원문 검색까지 포함한 결과이므로 고정 근거의 answering 점수와 따로 본다.
