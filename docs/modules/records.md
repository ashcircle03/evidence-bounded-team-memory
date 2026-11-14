# records — 근거 있는 팀 지식의 구성과 상태 관리

[공통 계약](README.md) · 구현 소유: `storage/*`, `review/state.py` · [실제 adapter](../../team_memory/adapters/records.py) · [전환 범위](runtime.md)

**records의 연구 책임은 DB에 쌓이는 지식의 품질이다.** 원문 저장뿐 아니라, 이후 비교·검색·답변이 사용할 주장·조건·출처·상태를 충실하게 구성하고 보존하는 것까지 포함한다. LLM이 추출한 내용은 출처가 연결된 추출/추론 기록으로 남기며, 그 자체를 사람의 승인이나 확정 사실로 승격하지 않는다.

**v1.2에 원문에서 주장 후보·조건·이유·시간·대상 구절을 연결하는 opt-in 구성 경로를 추가했다.** [record graph 설계와 코드](records-graph.md)를 참조한다. 기본값은 기존 원문 경로이며, 773개 보존·46개 상태 검사 통과는 지식 구성의 의미 성능이 아니다. 독립된 사람의 정답셋과 대규모 일반화 검증은 아직 없다.

[DB 품질에 대한 범위 교정](records-quality-scope.md). 아래 operation은 유지하고 source에 선택적인 record_graph를 추가했다. 엄격한 schema를 쓰는 팀원은 v1.2로 함께 갱신해야 한다.

| operation | payload | 정상 data |
|---|---|---|
| `record.append` | source + idempotency_key + expected_revision | receipt(snapshot, object_id, replayed) |
| `proposal.submit` | candidate + 동일 쓰기 필드 | receipt; coexist는 informational, 나머지는 pending |
| `review.apply` | proposal_id + choice(approve/reject) + 동일 쓰기 필드 | receipt; 원문은 보존되고 proposal 상태만 갱신 |
| `snapshot.get` | snapshot_id(null이면 현재) | immutable snapshot |

source는 id·owner·speaker·observed_at·location·text다. ID 충돌 시 다른 내용을 덮어쓰지 않는다. 검증된 content addressing을 재사용할 수 있지만 fixture ID는 opaque 값이다. snapshot에는 id·revision·as_of·sources·proposals가 있다. 기존 승인값에 대한 정정은 원문 수정이 아니라 정정 관계의 승인 효과로 표현한다.

권한: `records:read` / `records:write` / `review:vote`. append는 인증 주체가 owner인 원문만 허용한다. 타인 작성 자료를 가져오는 import는 별도 신뢰 경로와 명시적인 `records:import` 권한이 필요하다. reviewer는 candidate가 아니라 이전 원문 owner에서 정한다. 다른 workspace 요청은 거절한다. 재검토 승인에 새 실험 성공이나 결정 교체 효과를 부여하지 않는다.

정정 candidate는 previous/incoming 문맥 span과 그 안의 previous_assertion/incoming_assertion을 모두 요구한다. 변경 범위는 이 assertion 쌍이다. 승인이 담당자나 다른 수치까지 바꾸면 실패다. coexist는 추가 승인 없이 정보로 남기며, conflict 승인도 어느 한 값을 현재값으로 선택하는 권한은 아니다. 상충 투표는 review_conflict로 남기며 임의 latest-wins를 적용하지 않는다. v1에는 철회·강제 해결 명령이 없으므로 이 동작을 review reject로 위장하지 않는다.

잘못된 span/대상은 INVALID_INPUT·NOT_FOUND, 권한은 FORBIDDEN, 새 요청의 오래된 revision은 STALE_SNAPSHOT, key 재사용은 IDEMPOTENCY_CONFLICT다. commit 실패는 IO_FAILURE다. command의 일부만 적용하지 않지만, commit 후 응답·동기화 실패에는 전체 commit이 이미 보일 수 있으므로 아래 재시도 계약을 따른다. 원자성 확보 전에는 runtime adapter 완료로 표시하지 않는다.

필수 adapter 검사: append·proposal·review·retry, 승인된 정정의 다른 필드 보존, 이전 owner 이외 투표 거절, source ID 충돌, 같은 key의 변경 payload, 동시 revision 경쟁에서 한 요청만 성공, IO 실패 후 원상태 유지, 다른 workspace 접근 거절. 공통 예제는 앞의 주요 흐름을 제공하며 동시성·IO/인증 backend 검사는 담당자가 추가한다.

## 담당자 실험 및 저장소 강화

[records 실험·데이터셋·설계 근거](records-experiments.md)와 [실측 결과](../../results/records/README.md)를 기준으로 독립 개발한다. source/제안/review의 공개 v1.1 입출력은 유지한다.

저장된 JSON 손상·잘못된 내부 vote는 사용자 요청의 `INVALID_INPUT`으로 숨기지 않고 `IO_FAILURE`로 처리한다. 새 commit이 보인 후 디렉터리 동기화가 실패하면 `IO_FAILURE(retryable=true)`를 반환할 수 있다. 이때 **state가 안 바뀌었다고 가정하지 말고 같은 payload/key로 재시도**한다. replay는 디렉터리 동기화를 재확인하고 기존 receipt를 돌려준다. 제출 전 실패와 commit 후 응답 실패를 구별한다.

닫힌 review를 반대로 바꾸는 순차 요청은 거절한다. 이미 존재하는 상반된 v2 투표의 import는 `review_conflict`로 보존한다. 새 module commit 분기의 자동 병합은 여전히 지원하지 않는다.
