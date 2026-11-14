# records — 불변 원문과 상태의 유일한 쓰기 주체

[공통 계약](README.md) · 구현 소유: `storage/*`, `review/state.py` · 예정 adapter: `adapters/records.py`

LLM이 문서 관계를 해석해도 저장된 승인 상태는 모델 문장으로 바뀌지 않아야 한다. 원문과 이벤트를 보존하고 유효 상태를 계산하는 책임이다. 구조 검증은 의미의 진실 판정이 아니다.

| operation | payload | 정상 data |
|---|---|---|
| `record.append` | source + idempotency_key + expected_revision | receipt(snapshot, object_id, replayed) |
| `proposal.submit` | candidate + 동일 쓰기 필드 | receipt; coexist는 informational, 나머지는 pending |
| `review.apply` | proposal_id + choice(approve/reject) + 동일 쓰기 필드 | receipt; 원문은 보존되고 proposal 상태만 갱신 |
| `snapshot.get` | snapshot_id(null이면 현재) | immutable snapshot |

source는 id·owner·speaker·observed_at·location·text다. ID 충돌 시 다른 내용을 덮어쓰지 않는다. 검증된 content addressing을 재사용할 수 있지만 fixture ID는 opaque 값이다. snapshot에는 id·revision·as_of·sources·proposals가 있다. 기존 승인값에 대한 정정은 원문 수정이 아니라 정정 관계의 승인 효과로 표현한다.

권한: `records:read` / `records:write` / `review:vote`. append는 인증 주체가 owner인 원문만 허용한다. 타인 작성 자료를 가져오는 import는 별도 신뢰 경로와 명시적인 `records:import` 권한이 필요하다. reviewer는 candidate가 아니라 이전 원문 owner에서 정한다. 다른 workspace 요청은 거절한다. 재검토 승인에 새 실험 성공이나 결정 교체 효과를 부여하지 않는다.

정정 candidate는 previous/incoming 문맥 span과 그 안의 previous_assertion/incoming_assertion을 모두 요구한다. 변경 범위는 이 assertion 쌍이다. 승인이 담당자나 다른 수치까지 바꾸면 실패다. coexist는 추가 승인 없이 정보로 남기며, conflict 승인도 어느 한 값을 현재값으로 선택하는 권한은 아니다. 상충 투표는 review_conflict로 남기며 임의 latest-wins를 적용하지 않는다. v1에는 철회·강제 해결 명령이 없으므로 이 동작을 review reject로 위장하지 않는다.

잘못된 span/대상은 INVALID_INPUT·NOT_FOUND, 권한은 FORBIDDEN, 새 요청의 오래된 revision은 STALE_SNAPSHOT, key 재사용은 IDEMPOTENCY_CONFLICT다. commit 실패는 IO_FAILURE이며 부분 commit을 노출하지 않는다. 원자성 확보 전에는 runtime adapter 완료로 표시하지 않는다.

필수 adapter 검사: append·proposal·review·retry, 승인된 정정의 다른 필드 보존, 이전 owner 이외 투표 거절, source ID 충돌, 같은 key의 변경 payload, 동시 revision 경쟁에서 한 요청만 성공, IO 실패 후 원상태 유지, 다른 workspace 접근 거절. 공통 예제는 앞의 주요 흐름을 제공하며 동시성·IO/인증 backend 검사는 담당자가 추가한다.
