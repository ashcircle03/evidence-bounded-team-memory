# 변경 기록

## v0.2.0 · 2026-11-18

- records 저장 시 개별 주장의 상태와 원문 구절을 보존한다. v3 그래프와 실험 v4 연결 형식을 읽고 검증한다.
- 선택적 역할 보정기로 단일 주장에 귀속된 조건·이유와 정책 적용 대상을 다룬다. 사용자는 ingest 시 생성기를 선택한다.
- 고정 68문서 재채점에서 직전 정답 연결 50개가 모두 보존됐고 자연 기록 한 건을 추가 복구했다. [실행 경로와 제한](team_memory/records/README.md) · [문서별 비교](results/records/v0.2.0.csv)

## 2026-11-15 — records 연결 구조 후보 / 계약 v1.2

- 원문 구절과 주장 후보·조건·이유·시간·대상을 연결하는 선택적 record_graph를 추가했다. LlamaIndex sentence window를 실제 재사용하며 별도 graph DB는 없다.
- 기록 구성부터 저장·재시작·비교 입력·검색 문맥·QA 입력까지 연결했다. 미검증 추출을 승인 이벤트로 승격하지 않는다.
- 실제 실패에서 정한22개 source·9개 질문을 고정했다. [설계](docs/modules/records-graph.md)와 [실행/결과](results/record-graph/README.md)에서 의미 평가와 전달 검사를 구분한다.
- Qwen 두 실행과 실패 원출력을 공개했다. vLLM guided_json으로 형식 실패를 고쳤지만 의미 연결 누락·QA 퇴행이 남아 기본 채택은 보류했다. 기존 raw 경로와20문항 재생은 유지한다.

## 2026-11-15 — records 품질·실험 기반

- v1.1 입출력을 유지하면서 파일 손상 검사, 재생성 가능한 읽기 캐시, 디렉터리 동기화와 같은 key 재시도를 보완했다.
- 실제 개발 envelope 773개 보존, 46개 합성 상태 흐름, 지연시간과 기존 QA 보존을 분리해 측정했다.
- 닫힌 review의 순차 반전 거절과 기존 v2 상충 투표 import를 구분했다. 초기 정답표 오류도 공개한다.
- [record 실험 기준](docs/modules/records-experiments.md) · [결과와 한계](results/records/README.md).

## 2026-11-15 — 실제 v2 어댑터 연결 / 계약 v1.1

- records·relations·retrieval·answering·gateway를 `connect_v2`로 연결했다. 기존 v2 API도 유지한다.
- 기존 Store와 검토 reducer를 재사용해 원자적 명령 commit, owner 권한, revision, idempotency를 구현했다.
- 기존 검색과 생성 사이를 나누고 QA 중 sync/비교/상태 쓰기를 제거했다.
- 비교 당시 snapshot/history를 보존하고, 조작된 snapshot이나 빠진 상태 근거를 거절한다.
- 기존20의130개 정확한 모델 요청을 재생해 답·근거를 보존했다.8문항의11개 무인용 구절도 원문 그대로 유지하도록 v1.1의 original_text/unattributed/answer_span을 추가했다.
- 실제 저장·재시작·재검토·정정·상충·QA 연결을 검사했다. decoder는 stub이며 새 GPU 추론으로 보고하지 않는다.

[검증 결과와 운영 제한](results/module-adapters/README.md) · [실제 연결 방법](docs/modules/runtime.md). 분기 Git 자동 병합·인증 transport·과거 시점 조회는 아직 범위 밖이다.

## 2026-11-14 — 팀 개발 계약 v1

- 협업 책임을 records / relations / retrieval / answering / gateway로 정의했다.
- JSON Schema, Python ports, 참조 무결성 검사, 교체 가능한 conformance runner를 추가했다.
- 합성 시나리오22개와 계약·오류 주입 검사56개를 제공한다. fixture double과 실제 adapter 검증을 구분한다.
- 각 모듈의 입출력·권한·원자성·부분 실패·재시도·담당 파일·전환 작업을 문서화했다.
- claim별 근거, 승인 효과 제한, read-only QA와 trusted caller 경계를 명세했다.
- 기존 v2 모델·프롬프트·런타임 경로는 유지했다. 새 adapter는 아직 구현 완료가 아니다.

검증: [387개 테스트·87개 하위 사례 및 패키지 확인](docs/modules/verification.json). 새 모델 추론·벤치마크 성능 측정은 포함하지 않는다.

## 2026-11-14 — 모듈 구조와 개발 환경

- 현재 구현을 storage/review/readers와 service 진입점으로 구분했다.
- 대안 reader와 patch 후보를 experiments로 이동하고 기존 import/CLI는 유지했다.
- 과거 데이터 해시에 묶인 store 원본과 동결 source archive는 보존했다.
- 설치 가능한 패키지, source packager, 동일한 로컬/CI pytest 진입점을 추가했다.
- 모듈별 책임·입출력·의존성·검사 문서와 간결한 README를 제공한다.
- GitHub에 없던 후속 상태·입출력 수정과 실험 기록도 공개 상태에 맞췄다. 소규모 개발 결과와 미해결 문제는 구분한다.

구조 이동 자체는 모델·프롬프트·상태 전이를 바꾸지 않는다. 이전 공개 커밋과의 차이에는 앞서 로컬에서 완료한 기능 수정도 포함되므로, 전체 변경을 모델 효과가 없는 파일 이동으로만 해석하면 안 된다.

모델/벤치마크 결과는 [연구 이력](docs/research-history.md)과 [실행별 결과](results/README.md)를 기준으로 읽는다. 후속 레퍼런스 조합 비교는 아직 완료된 성과로 포함하지 않는다.
