# gateway — 인증된 호출과 흐름 연결

[공통 계약](README.md) · 구현 소유: `service.py`의 조정 부분 / 팀원 MCP transport · 예정 adapter: `adapters/gateway.py`

MCP·JSONL·HTTP는 이 포트 바깥의 transport다. gateway는 모델 판단을 다시 구현하지 않고 신원·요청·snapshot·오류를 전달한다. 현재 service v2는 인증 모듈이 아니다.

| operation | 입력 | 호출 흐름 / 출력 |
|---|---|---|
| `gateway.ask` | query, snapshot_id(nullable) | records snapshot.get → retrieval → answering; bundle + answer |
| `gateway.ingest` | source, idempotency_key, expected_revision | records append → 고정 snapshot에서 relations → records proposal.submit; 원문 receipt + proposal_ids |
| `gateway.review` | proposal_id, choice, idempotency_key, expected_revision | records review.apply; receipt |

ask는 sync·ingest·투표를 호출하지 않는다. 호출 중 새 기록이 들어와도 처음 snapshot으로 답하며 다른 버전을 몰래 섞지 않는다. 검증용 전체 snapshot을 LLM 프롬프트에 보내지 않는다. 사용자가 최신 snapshot으로 다시 묻는 것은 별도 요청이다.

ingest는 여러 records 명령의 조정이며 하나의 대형 원자 transaction으로 가장하지 않는다. 원문 commit 이후 비교가 실패하면 partial + 원문 receipt + 오류를 반환한다. 원문 저장은 되돌리지 않는다. 후속 proposal 명령은 원문 key에서 결정적으로 파생한 별도 key와 최신 expected_revision을 쓰고 중간 결과를 기록한다. 전송 실패 후 같은 요청이 오면 이미 완료된 단계의 receipt를 재사용한다. 이 재개 장부는 gateway 소유이며 팀의 사실 상태와 구분한다.

부분 실패의 남은 단계를 아무 QA 요청에서나 재실행하지 않는다. 명시적인 ingest 재시도나 작업자가 요청한 복구로 진행한다. unknown submission 상태에서 같은 명령을 다른 key로 다시 보내지 않는다.

신원은 transport에서 검증해 CallContext로 주입한다. 외부 JSON의 actor/owner 주장만으로 승인 권한을 부여하지 않는다. records도 다시 소유자 권한을 검사하므로 gateway를 우회해도 승인되지 않아야 한다. 리뷰 로그에 인증 주체와 명령 ID를 남긴다.

공통 검사: read-only ask와 무단 review 거절. 통합 담당자 추가 검사: 실제 인증 실패, workspace 격리, append 성공/비교 실패의 partial, ingest 재시도·중간 저장, 호출 예산 초과, 다른 snapshot 혼합, endpoint별 request_id 보존. 기존 v2 ask의 sync 제거와 claim별 응답 어댑터가 완료되기 전에는 새 계약 API를 서비스 완료로 표시하지 않는다.
