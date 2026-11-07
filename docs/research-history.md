# 문제정의부터 현재 구현까지

2026-11-08 공개 정리. 모든 수치는 해당 단계의 데이터·모델·평가 조건 안에서만 해석한다. 단계마다 문항, 모델, 재생 범위가 달라 한 성장 곡선이나 전체 평균으로 합칠 수 없다. [이전 README 전체](history-overview-2026-11-08.md)는 설명을 잃지 않도록 별도로 보존했다.

## 1. 문제를 정한 과정

출발점은 Aimers 팀 실험에서 AI가 과거에 철회한 설정의 조건을 놓친 경험이었다. 팀원이 그 설정을 다른 조건으로 실행해 개선을 얻었지만, 개인 AI가 쌓은 GitHub 기록만으로 이를 자율적으로 재검토하기 어려웠다.

문제는 실험 계획만으로 한정하지 않았다. 공유 저장소에 지식이 누적될 때 과거의 결정·이유·조건·출처를 보존하고, 새 근거가 영향을 주는 결정을 찾아 검토 제안을 만드는 문제로 일반화했다. 제안을 원작성자가 확인하는 PR 같은 구조를 선택했다. 승인 전에도 새 보고는 읽을 수 있지만 확정된 지식과 구분해야 한다. 해결되지 않은 상충은 양쪽을 보존한다.

따라서 **재검토 판단의 성공과 최종 실험 성능 향상은 별도 지표**다. 재실험 결과 점수가 오르지 않아도 바뀐 조건을 정확히 짚어 재검토하고 그 근거를 남기면 판단은 성공일 수 있다. [초기 개발 기록](../results/development.ko.md).

## 2. 평가 대상과 베이스라인

- **SpeakerMem-R1:** 초기 다중 사용자 기억 QA의 기준선 후보/개발 실행. 현재 서비스가 논문의 학습·성능을 재현했다거나 공식 비교를 끝냈다는 뜻은 아니다.
- **CUPMem / STALE:** 오래된 기억의 유효성·갱신에 가까운 공개 구현을 실제 가져왔다. 원 설정의 모델과 다른 로컬 Qwen 개발 실행은 대체 모델 실험이다. 조건별 공존·결정의 재검토·원작성자 승인은 원형의 해결 범위라고 가정하지 않았다.
- **단순 방식:** 각 실험에서 동일 모델·원문에 접근하는 직접 독해를 비교했다. “direct”라는 이름만 같고 과거 3B/14B timeline과 현재 8B reader가 같은 구성인 것은 아니다.
- **현재 서비스:** 원문 QA와 timeline 검토를 연결하고, 검증된 공개 라이브러리/저자 코드의 일부를 재사용한다. 현재 기본값은 `attributed`다.

## 3. 진단 실험의 축적

| 단계 | 무엇을 확인했는가 | 결과가 바꾼 판단 / 상세 기록 |
|---|---|---|
| CPython PEP 파일럿 | 과거 원문에서 후속 조치와 QA가 가능한가 | 정답 구절 9/9가 입력에 있어도 답+출처 0/9. 답만/정답 구간 지정 대조로 독해·출력 병목을 분리. [QA 원인 분석](../results/cpython/qa-diagnosis.ko.md) |
| 첫 팀 파일럿 | 일반 QA를 지키면서 상충과 재검토를 처리하는가 | 필요하지 않은 경우에도 제안. 기본 채택 보류. [결과](../results/team_pilot/README.md) |
| 원문 Git 재생 | 원문 Markdown·작성자 검토·QA 전체 흐름 | 오탐은 줄었으나 필요한 재검토/QA 성과 부족. [결과](../results/revision/README.md) |
| 결정 기록 비교 | 원문 / 당시 AI 기록 / 당시 정보의 정리 | 기록 자체와 근거 선택 문제를 분리. [보고서](../results/decision_records/README.md) |
| 후보 선택·순서 | 과거 후보별 비교와 순서 반전 | 올바른 문단 선택과 올바른 재검토 이유가 별개. [pair selection](../results/pair_selection/README.md) |
| 올바른 근거 고정 | 판정·설명의 한계를 검색과 분리 | oracle 문단에서 개선돼도 실제 검색에서는 성립하지 않음. [fixed review](../results/fixed_review/README.md) |
| 대안·역할·주변 문맥 | 주제 유사 결정, 주체/동작/조건, 전후 문단 | 설명의 의미 오류가 지속. [contrast](../results/contrast_review/README.md) · [role](../results/role_review/README.md) · [context](../results/context_review/README.md) |
| 설계 재검토 | 더 강한 모델·단순 방식·같은 근거 | 모델 한계와 입력/구조 문제를 함께 기록. [설계 판단](../results/design_review/README.md) |
| 누적 timeline | direct vs indexed, 동일 14B, 전체 흐름 | 색인 추가가 기존 QA를 잃음. 당시 direct 선택. [해석](../results/timeline/interpretation.ko.md) |
| CUPMem | 실제 native 기억 작성·검색과 원문 QA 연결 | practical에서 근거 있는 재검토 양쪽 0/10, QA+인용 양쪽 7/20. 후보 기본 채택 보류. [고정 평가](../results/cupmem/practical/README.md) |

이 결과는 레퍼런스 자체의 무효성을 입증하지 않는다. 모델·프롬프트·원문 길이·우리 연결부·평가 구성의 효과가 함께 있다. 특히 literal quote 일치와 설명의 타당성을 구분하는 것이 반복해서 중요했다.

## 4. 원문 QA를 공개 구현으로 복구

LlamaIndex의 분할·문맥 예산·검색·인용을 사용해 native 기억 작성 실패가 QA 전체를 막는 의존성을 풀었다. 혼합 검색과 작성자 전달, ConflictScore의 실제 문서별 판정, AQA의 출처별 답 보존, LangChain의 정확한 구절 인용을 순서대로 검토했다.

고정 개발20문항에서 19→20개를 복구하고 부연 인용 누락도 수정했다. 이 과정에는 **저장된 호출 재사용과 일부 추가 추론**이 포함된다. 매번20문항 전체의 새 추론 성과로 쓰지 않는다. [전체 결과와 원자료](../results/reference-qa/README.md) · [레퍼런스 변형 범위](reference-attribution.md).

## 5. 단순화·확대 평가와 채택 보류

| 후보 | 의도 | 관측/결정 |
|---|---|---|
| joint | 답·근거를 한 번에 생성해 단계 축소 | 새 통제12건에서 7→9, 호출51→12. 기존20 중1개와 순서 안정성 상실. 전면 교체 안 함. [보고서](../results/reference-qa/simplify-v2/README.md) |
| claims / format recovery | 주장과 근거를 같은 단위로 연결 | 고정104출력 재생 중99재사용·5새생성. 기존20은17/20. [확대 평가](../results/reference-qa/claims-v3/README.md) · [형식 복구](../results/reference-qa/format-recovery-v1/README.md) |
| documents | LongMemEval 검색·시간순 독해 + ALCE 문서 인용 | 기존20 답19/20·답+인용18/20, Ever10 BM25 2/10·Contriever1/10. [보고서](../results/reference-qa/documents-v1/README.md) |
| contextual | 날짜·작성자·주변 조건 보존 | Ever10 결합2/10, 기존20 17/20. [보고서](../results/reference-qa/contextual-v1/README.md) |
| connected | Attribute First 근거 계획 + 제한된 IRCoT 검색 누적 | Ever10 3/10, 기존20 18/20. [보고서](../results/reference-qa/connected-v1/README.md) |
| demonstrated | 저자 예시의 입력·선택 구절·출력 연결까지 활용 | Ever10 2/10, 기존20 19/20. [보고서](../results/reference-qa/demonstrated-v1/README.md) |

대부분 반복해서 본 개발셋이다. 이 비교만으로 후보 순위를 일반화하지 않는다. [모델·평가 감사](evaluation-model-audit-2026-11-07.md), [개발 프로세스 감사](development-process-audit-2026-11-07.md), [시스템 감사](system-audit-2026-11-07.md)에서 검증 누수, 재생과 새 추론, 패키지·전송·상태의 경계를 점검했다. 감사는 당시 스냅샷이며 이후 수정 여부는 최신 보고서를 따른다.

## 6. 단일 서비스와 최신 고정 비교

`service-v2`는 원문 QA·timeline·검토를 한 진입점으로 연결했다. 실제 Qwen 흐름에서 핵심 답·원문 인용은 맞았으나 상태 설명 세 문장의 근거가 누락됐다. [통합 결과](../results/service-v2/README.md).

`service-v3` 평가에서는 검토 기록의 불변 스냅샷을 기존 인용 단계에 넣어 알려진 누락을 복구했다. 그 뒤 코드·입력·채점 기준을 고정하고 새 원본 QA12개, 새 합성 흐름의 QA11개, 기존20개를 같은 Qwen3-8B로 비교했다. 새23개 답+필요근거는 direct10개/attributed14개, 기존20은17개/20개였다. 비용 기준은 attributed가 실패했다.

**공통 상태 인용 수정은 유지한다. 기존 attributed 기본값도 호환성을 위해 유지한다. direct 전면 교체와 현재 구조의 완성형 채택은 둘 다 하지 않는다.** 실패 원인과 다음 수정 경계를 기록하고 이번 비교를 끝냈다. [최신 보고서](../results/service-v3/README.md) · [문항별 비교](../results/service-v3/cases.md) · [실제 적용 결정](../results/service-v3/deployment-decision.json).

## 남기는 기록의 원칙

실패한 후보·원출력·오류·재시도 비용을 지우지 않는다. 이미 고정한 실험 파일을 새 코드나 점수로 교체하지 않는다. 과거 완료 기록의 `code_pushed:false` 같은 필드는 당시 스냅샷이며, 이후 공개 작업의 상태로 소급 수정하지 않는다. 공개 업데이트 검증은 별도 `results/publication-2026-11-08/`에 둔다.
