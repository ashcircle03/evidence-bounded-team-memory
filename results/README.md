# 결과 자료 안내

최신 비교기 선택은 [comparator-choice](comparator-choice/README.md), 현재 운영 코드의 입출력 검증은 [module-boundary](module-boundary/README.md), 이전 reader 비교는 [service-v3](service-v3/README.md)를 먼저 읽는다. 전체 판단 흐름은 [연구 이력](../docs/research-history.md)에 있다. 아래 폴더는 서로 다른 실험이며 수치를 합산하지 않는다.

| 보고서 | 위치 |
|---|---|
| 올바른 재검토→실제QA와8B/14B 비교기 선택 | [comparator-choice](comparator-choice/README.md) |
| 결정·근거 추출 공개 구현 조사와 CoMRAT 원본 재현 | [rationale-reuse](rationale-reuse/README.md) |
| 오픈소스 서비스 패턴 적용과 상태·인용 경계 검증 | [service-completion](service-completion/README.md) |
| 전체 공개 업데이트 검증 | [publication-2026-11-08](publication-2026-11-08/README.md) |
| 선택 문단 주변에서 실제 실패 동작을 복구할 수 있는가 | [context_review](context_review/README.md) |
| 같은 새 보고로 실제 재검토 대상과 비슷한 결정을 구별할 수 있는가 | [contrast_review](contrast_review/README.md) |
| CUPMem stopped pilot: verified scope and next decision | [cupmem/pilot-v5](cupmem/pilot-v5/README.md) |
| Practical CUPMem 최종 평가와 채택 판단 | [cupmem/practical](cupmem/practical/README.md) |
| CUPMem 서비스 통합 개발 결과 | [cupmem/service-v1](cupmem/service-v1/README.md) |
| 결정 기록을 함께 읽으면 재검토와 QA가 나아지는가? | [decision_records](decision_records/README.md) |
| 고정 사례에서의 설계 유지 판단 | [design_review](design_review/README.md) |
| 올바른 두 문단에서 출발하는 재검토 판정 | [fixed_review](fixed_review/README.md) |
| 과거 결정의 근거 선택과 재검토 검증 | [pair_selection](pair_selection/README.md) |
| 원문 QA: 상충 답 보존과 인용 누락 수정 | [reference-qa](reference-qa/README.md) |
| claims-v1 | [reference-qa/claims-v1](reference-qa/claims-v1/README.md) |
| 주장별 근거를 먼저 선택하는 QA 후보 평가 | [reference-qa/claims-v3](reference-qa/claims-v3/README.md) |
| 근거 계획·누적 검색 연결: 개발 비교 결과 | [reference-qa/connected-v1](reference-qa/connected-v1/README.md) |
| 검색 피드백·원문 맥락 보존 결과 | [reference-qa/contextual-v1](reference-qa/contextual-v1/README.md) |
| 상태와 입출력 계약 수정 | [reference-qa/contract-v1](reference-qa/contract-v1/README.md) |
| 저자 구현 예시·근거 연결 복구: 검증 결과 | [reference-qa/demonstrated-v1](reference-qa/demonstrated-v1/README.md) |
| 문단 ID 독해·실제 검색 비교 결과 | [reference-qa/documents-v1](reference-qa/documents-v1/README.md) |
| 인용 형식 복구와 EverMem 입력 진단 | [reference-qa/format-recovery-v1](reference-qa/format-recovery-v1/README.md) |
| QA 단순화 재감사 — 2026-11-06 | [reference-qa/simplify-audit-v1](reference-qa/simplify-audit-v1/README.md) |
| QA 단순화: 실제 비교와 채택 판단 | [reference-qa/simplify-v2](reference-qa/simplify-v2/README.md) |
| 두 번째 평가 · 언제 과거 결정을 다시 여는가 | [revision](revision/README.md) |
| 설명의 주체·동작·조건을 원문에 연결하는 실험 | [role_review](role_review/README.md) |
| 단일 서비스 연결 결과 | [service-v2](service-v2/README.md) |
| 상태 인용 수정과 고정 비교 결과 | [service-v3](service-v3/README.md) |
| 팀 지식 파일럿 결과 | [team_pilot](team_pilot/README.md) |
| 누적 기록 최소 시스템: 설계 판단 | [timeline](timeline/README.md) |
| 개발 실행과 호환성 확인 | [timeline/development](timeline/development/README.md) |

추가 초기 자료: [개발 기록](development.ko.md) · [CPython 평가](cpython/report.ko.md) · [QA 진단](cpython/qa-diagnosis.ko.md).

각 폴더의 freeze/PROTOCOL은 당시 입력과 기준, calls/outputs/result는 실제 출력, ratings/cases/report는 의미 판정, accounting/progress는 실행 이력이다. 파일명은 단계별로 다를 수 있다. 실패 실행과 부분 완료도 포함하므로 progress와 보고서의 범위를 함께 확인한다.
# 최신 추가: 원문 근거 패치 후보

[실제 구현 조사·수정·기각 결과](source-patch/README.md). 두 후보 모두 기존20은 유지했으나 상태·정정 의미가 회귀해 기본 경로를 v3b로 복구했다. 새 성능 개선을 채택했다는 결과가 아니다.

## 모듈 입출력 경계 수정

[새 Qwen 검증과 적용 판단](module-boundary/README.md): 기존37개 답·근거 유지, 계약 검사77개 통과. 재검토 분류0/2와 불필요 제안2/2는 미해결. 모델·학습 변경 없이 연결부 수정만 채택했다.
