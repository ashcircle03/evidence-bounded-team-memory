# relations — 관계의 의미 판단과 근거 선택

[공통 계약](README.md) · 구현 소유: `review/comparison.py`, `review/policy.py` · [실제 adapter](../../team_memory/adapters/relations.py)

입력 `relations.compare`: snapshot, incoming_source_id, history_source_ids. 출력은 같은 snapshot_id와 candidates다. 후보 하나는 kind, previous/incoming 문맥 span, reason, 정정일 때 두 assertion span이다. 새 문서 전체를 한 종류로 분류하지 않고 새 기록과 과거 기록의 개별 관계를 반환한다. 서로 다른 과거 대상에 복수 후보를 반환할 수 있다.

| kind | 판단 의도 | 허용되는 제안 |
|---|---|---|
| coexist | 조건·대상 차이로 함께 유지 가능 | 정보로 추가 |
| conflict | 비교 가능한 조건에서 두 주장을 함께 채택하기 어려움 | 양쪽 근거를 유지하는 상충 후보 |
| correction | 원문에 명시적인 정정 의도·대상 존재 | 정확한 두 assertion 범위의 정정 후보 |
| reconsider | 바뀐 전제가 기존 결정에 연결됨 | 다시 검토할 후보; 정정으로 바꾸지 않음 |

일치하거나 관계가 없으면 candidates=[]가 정상일 수 있다. 그러나 모델 timeout·형식 실패를 빈 배열 성공으로 반환하면 안 된다. 한 후보만 실패하면 partial + 유효한 후보 + item별 오류; 전체 실패는 error다. 분류 불확실성이면 확정 후보로 밀어 넣지 않고 MODEL_OUTPUT_INVALID 또는 명시된 판단 실패로 남긴다.

권한은 `relations:compare`와 입력 snapshot 읽기뿐이다. 저장·승인·reviewer 선택·QA 답변 권한은 없다. 비교할 후보를 검색하는 일은 호출자/검색 계층이 맡는다. 어떤 과거 기록이 입력에 없었는지도 실행 로그에 남긴다. 후보 누락과 관계 오분류를 분리해 평가하기 위해서다.

공통 검사: 정정의 좁은 span, 조건이 다른 공존, timeout과 빈 결과 구분, 입력 밖 대상·가짜 인용·자동 승인 필드 거절. 별도 모델 평가: 순서 반전, 무관한 유사 주제, 근거 부족, 같은 보고의 복수 관계, 근거 문단 선택·분류 macro-F1과 불필요 제안률. 포트 계약 통과는 이 의미 성능을 보장하지 않는다.
