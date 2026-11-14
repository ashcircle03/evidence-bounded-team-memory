# 서비스 구현 경계 수정과 오픈소스 비교

2026-11-08. 변경 전 기준은39dd648의 service-v3이다. 이번 작업은 논문 알고리즘 추가보다 실제 서비스의 상태 전달·적용 경계를 바로잡는다. 아래 프로젝트의 실행 코드를 읽고 revision을 [고정 목록](../evaluation/service_completion/opensource-references.json)에 남겼다.

## 프로젝트 코드에서 확인한 것

| 프로젝트 | 실제 확인한 연결 | 우리에게 적용 / 적용하지 않는 부분 |
|---|---|---|
| [Mem0](https://github.com/mem0ai/mem0/blob/f1791daa86d469249c9b002f62644d58a1eb96a0/mem0/memory/main.py#L2052) | `_update_memory`는 기존 payload에서 metadata를 이어받고 현재 vector를 갱신한 뒤 old/new·actor·시간을 history에 남긴다. SQLite history는 별도 자료다. | 현재 표현과 변경 이력을 구분한다. 원문·제안·투표는 기존 Git 불변 저장소를 유지한다. 자동 UPDATE/DELETE를 사용자 승인으로 간주하거나 중앙 SQLite로 Git 저장을 바꾸지 않는다. |
| [Graphiti](https://github.com/getzep/graphiti/blob/747b480ec6b12ecb718f1e2bc588b20ee36ea9c2/graphiti_core/edges.py#L263) | 개별 fact edge가 episode 출처, valid_at/invalid_at/expired_at을 가진다. [충돌 처리](https://github.com/getzep/graphiti/blob/747b480ec6b12ecb718f1e2bc588b20ee36ea9c2/graphiti_core/utils/maintenance/edge_operations.py#L748)는 시간 구간을 비교한다. | 변경 적용 단위를 문서 전체가 아닌 주장 구절로 분리한다. 관측시각을 모든 독해 단계에 보존한다. 새 보고 시각만으로 옛 사실을 무효화하거나 LLM 추정 시각을 승인시각으로 사용하지 않는다. |
| [LangChain HITL](https://github.com/langchain-ai/langchain/blob/d9caf083577c43a91c5bf6bd1f7dfc289581184d/libs/langchain_v1/langchain/agents/middleware/human_in_the_loop.py#L637) | 요청·판정·실행을 구분하고, reject는 성공한 tool 결과가 아닌 실행되지 않은 결과로 모델에 돌아간다. 허용된 decision과 call ID를 검사한다. | 기존 owner vote reducer에서 승인된 효과를 계산한다. pending/rejected를 현재값과 섞지 않는 `correction_effects`를 생성·수정·judge에 동일하게 전달한다. 거절을 읽기 문맥에서 삭제하지 않는다. |

이는 **서비스 패턴의 비교와 기존 코드에 대한 변형**이다. Mem0·Graphiti·LangGraph 패키지를 설치해 실행했다고 주장하지 않는다. 현재 실제 호출 라이브러리는 기존 LlamaIndex, 실제 ConflictScore 문서 판정 함수, 기존 LangChain 구절 스키마 어댑터다. Git별 독립 클라이언트에 없는 중앙 workflow/graph DB를 새로 추가할 이유는 이번 결함에서 확인되지 않았다.

## 구현 변경

1. `expand_review_context`가 rejected 관계도 양쪽 원문과 함께 전달한다. 제안이 거절됐다는 정보가 누락돼 새 값을 확정값으로 읽던 결함을 고친다.
2. `correction_effects`는 기존 owner vote를 축약한 상태에서 계산한다. pending/rejected/disputed는 변경 미적용, approved만 변경 적용이다. 원문과 제안은 읽을 수 있게 남는다. 이 필드는 제안별 적용 이력이며 세상 사실의 참/거짓 인증이 아니다.
3. 정정 제안의 context quotation과 changed assertion을 분리한다. `previous_assertion/incoming_assertion`은 각각 기존 `previous/incoming` 안에 있는 정확한 원문 구절이어야 한다. 승인 범위는 좁은 assertion에만 적용한다. 과거 객체에는 새 필드를 소급 삽입하지 않는다.
4. 현재 사실을 검사하는 judge에는 승인된 옛 주장과 pending/rejected 새 주장을 현재 근거로 쓰지 않는 표현을 준다. 원문 저장·최종 인용·historical 독해는 유지한다. 일반 QA에는 해당 정정 관계가 없으므로 이 처리도 없다.
5. `source_text`를 통해 문서 검토·재작성·AQA에 작성자와 recorded_at을 함께 전달한다. 처음 독해에서 보였던 날짜를 다음 단계에서 버리지 않는다.
6. ConflictScore 저자 함수가 요청한4096 completion budget을 전송 어댑터가 존중한다. 기존 local384 강제값 때문에 최종 answer 필드가 잘린 문제를 해결하려는 변경이다. 실제 남은 context보다 예약할 수 없고 실패 후 자동 확대·재시도하지 않는다. 추가 judge 호출 단계는 없다.

## 완성 판단의 범위

[고정 검사 계획](../evaluation/service_completion/PROTOCOL.md)은 기존20 QA를 전체 원문 검색부터 새로 실행하고, 기존8흐름11질문과 새 합성3흐름6질문을 확인한다. 값과 상태를 구분한 정답, 실제 원문/투표 인용, 변경되지 않은 사실 유지, 무관한 보고 무제안, 재시작을 본다.

문서 구조나 offset 검사만으로 완성이라고 하지 않는다. 실제 Qwen 결과에서 위 요구가 실패하면 그 실패를 남긴다. EverMem 전체 검색 일반화, 자연 Git의 모든 의미적 재검토, 호출자의 신원 인증은 이 작은 검사로 해결됐다고 주장할 수 없다. UI/MCP는 팀원의 별도 작업이다.

## 실제 실행에서 확인한 입력 계약 수정 — v2

첫 v1 실행120381에서 모델이 source의 `the`를 `The`로 바꾼 assertion을 내어,
정확한 구절 검증이 제안 전체를 거절했다. 이 결과와 원출력은 그대로 보존한다.
`source_comparison`은 이미 사용하는 NLTK Punkt로 원문 문장에 번호를 붙이고,
LangChain Citation의 source ID 선택 방식처럼 모델이 번호만 고르게 한다.
문자 offset과 실제 quotation은 코드가 원본에서 복원한다. 단어·대소문자 교정이나
fuzzy matching은 없다. 원문은 한 번만 전달하며 추가 LLM 호출도 없다.
문장보다 더 작은 복합 주장 범위는 별도 한계로 남는다.

또한 승인할 변경이 없는 coexist는 검토 요청으로 만들지 않는다. 원문 둘은 계속
검색·QA에 사용하며 `receipt.informational_relations`에 출처를 가진 설명을 남긴다.
이것은 모델의 관계 분류 정확도가 올랐다는 주장이 아니라 **informational observation과
state-changing action의 서비스 계약 분리**다. Mem0의 current/history 구분과 HITL의
실행 승인 경계를 참조하며, Git 저장/기존 owner reducer를 대체하지 않는다.
실제 변경·재검토·충돌 제안은 계속 원작성자 검토 대상으로 남긴다.

잘못된 sentence ID는 실패 영수증으로 기록한다. 이후 ask/sync가 동일 실패를
자동 반복 호출하지 않는다. 구절을 못 골랐다는 사실을 성공한 변경처럼 숨기지 않는다.

## 상태 근거를 생성 시점부터 연결 — v3b

v2는 상태 값을 복구했지만 승인·거절 문장에 이미 원문 번호가 붙으면
기존 `uncited_sentences` 경로를 통과하지 않아 실제 투표를 인용하지 않았다.
새 판정기를 더하는 대신 이미 있는 불변 review snapshot을 LlamaIndex
CitationQueryEngine의 입력 노드로 넣는다. 초안·문서 검토·재작성·AQA가
같은 번호의 원문과 상태 근거를 사용한다. 원문과 review_state의 자료형 및
offset 공간은 구분한다. 인용 보완은 이미 번호가 붙은 상태 자료도 인식한다.
모델이 실제로 올바른 번호를 선택했는지는 별도 실행 결과로 판단한다.

v3는 제출 전 코드 점검 중 기존 번호의 상태 인용 처리 누락을 발견해
실행하지 않았다. 최종 제출 패키지는 v3b이며 v1/v2 결과는 보존한다.

## 비교 판단의 기존 의도 복원 — v4

문장 ID로의 전환에서 출력 형식뿐 아니라 비교 지침을 축약한 문제가 드러났다.
v1은 writer/cache 두 사례를 reconsider로 분류했지만 v2/v3b는 correction으로
분류했고, writer 음성 사례에도 correction을 제안했다. 실제 v2/v3b 비교 HTTP
입력과 출력은 동일했다. QA가 그럴듯해도 비교 모듈의 의미 오류를 별도로 센다.
v4는 기존 timeline.COMPARE의 비교 정책과 종류별 근거 선택 의도를 재사용하고,
출력 표현만 원문 문장 ID로 바꾼다. 새로운 판정 단계를 추가하지 않는다.
여러 변경이 섞인 개발 회귀 검사이므로 독립적인 인과 효과나 일반화를 주장하지 않는다.

실행 후 결정: v4도 정정의 assertion ID를4건에서 누락했고 writer의 조건 변경을
정정으로 해석했다. 채택하지 않았다. 작업 소스는 검증한 v3b로 돌아갔으며,
그 버전 역시 재검토 양성2건과 음성2건을 실패했다. 개선된 상태·인용 경계와
미해결 의미 판단을 분리한다. [전체 결과](../results/service-completion/README.md).
