# 변경 기록

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
