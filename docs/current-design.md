# 현재 설계: 연결부의 책임과 근거

2026-11-08. 이 문서는 현재 `team_memory.service`를 설명한다. 과거 실험 모듈이 남아 있어도 자동으로 현재 경로에서 호출되는 것은 아니다. [실제 성과와 한계](../results/service-v3/README.md)를 설계 명세와 함께 읽는다.

## 의도에서 구현까지

| 필요한 판단/보존 | 사용하는 구현과 의도 | 우리 연결·변형 | 경계와 한계 |
|---|---|---|---|
| 원문을 재해석해 덮어쓰지 않기 | 기존 불변 객체 저장과 validator | `SourceStore`가 공백·줄바꿈까지 보존. 과거 Store 해시 규칙은 유지 | 과거에 이미 정규화된 텍스트는 복구하지 않음 |
| 의미·키워드 검색 누락 줄이기 | LlamaIndex BM25 + vector + reciprocal-rank fusion | 검색 결과에 작성자·시각·위치를 연결, 질문 확장 호출 없음 | 순위 내에 필요한 기록이 없으면 독해로 해결 불가 |
| 원문을 읽으며 인용하기 | LlamaIndex CitationQueryEngine·청킹·문맥 예산 | 원문 ID와 문자 위치를 다시 연결 | 범위 일치가 의미 지지는 아님 |
| 초안이 다른 출처의 답을 버렸는지 확인 | ConflictScore 저자 문서 support 판정 코드와 피드백 흐름 | 로컬 Qwen 전송·출처별 재작성, 파싱 실패는 ERROR | 전체 논문 지표 재현 아님. 날짜 전달 누락·잘림 확인 |
| 상충 기록 중 누락한 답 복구 | AQA의 출처별 답 보존 의도 | 기존 초안/원문과 반대 출처를 읽는 보완, 교체 이력 유지 | 공식 3-shot 전체를 확보한 재현 아님. 새 후보가 의미적으로 틀릴 수 있음 |
| 답 문장과 정확한 구절 연결 | LangChain FactWithEvidence/QuotedAnswer 스키마·프롬프트 | 원답을 바꾸지 않고 인용 번호 삽입, 정확한 구절 위치 검증 | 원형 fuzzy 매칭을 쓰지 않음. 의미 지지 자동 보장은 안 함 |
| AI 제안과 작성자 승인을 구분 | 기존 timeline 제안·원작성자 투표·상태 축약 | 검증된 제안의 양쪽 원문·조건과 실제 상태를 QA에 전달 | actor 문자열은 신원 인증 아님. rejected 전달 결함 남음 |
| 상태 설명도 근거를 가지기 | 기존 정확한 인용 단계 재사용; PROV-DM의 기록/행위/책임 구분 참고 | 제안·유효 투표·보이는 원문을 불변 snapshot으로 인용 | PROV 구현/검증기 아님. pending은 투표 부재인 그 시점의 상태 |

구체적인 upstream 링크·revision·변형은 [기본 검색·QA](reference-reuse.md), [혼합 검색·ConflictScore](reference-team-profile.md), [AQA·LangChain](reference-attribution.md), [상태 인용](review-state-citations.md)에 있다. `team_memory/_vendor/`의 원본·NOTICE·LICENSE도 함께 보존했다.

## 연결 계약

1. 입력은 `owner`, 시간대가 있는 `observed_at`, `source.speaker/location/text`다. 사람이 결론·조건을 별도 정답 레코드로 작성해야만 작동하는 입력은 아니다.
2. 원문은 불변 저장한다. `import_history`는 빈 저장소의 초기 입력을 모델 호출 없이 넣는다. `ingest`/`sync`는 새 기록을 기존 timeline과 비교해 제안을 만든다.
3. 제안에는 과거·신규 원문 구절이 필요하다. 재검토 필요성과 실제 승인·정정 적용은 별개다. 가상 승인 fixture로 통과한 것은 실제 사용자 인증 검증이 아니다.
4. QA는 검색된 원문과 관련 검토 문맥을 받는다. 질문과 무관한 충돌이 존재한다는 이유만으로 답을 전부 차단하지 않는다. 조건이 다른 결과는 각 조건과 함께 남기는 것이 목표다.
5. 답은 원출력, 인용 가능한 원문, 선택된 근거 구절과 offset, 경고를 반환한다. `review_state` 근거의 offset은 원문 보고서가 아닌 결정적 스냅샷 렌더링을 가리킨다.
6. 원문·제안·투표를 Git으로 공유한다. 로컬 영수증/색인은 각 checkout에 둔다. 실제 pull/push, 인증, UI/MCP는 호출자의 책임이다.

## 두 reader와 현재 선택

`direct`와 `attributed`는 검색·초기 독해·검토 문맥·구절 인용을 공유한다. attributed에만 문서별 judge, 필요시 재작성, 누락한 반대 답의 AQA 보완이 있다. 고정 비교의 **43쌍 최초 실제 HTTP 요청이 모두 동일**했으므로 최신 reader 비교에서 초기 입력 차이로 이득을 설명하지 않는다.

attributed는 새 QA 성공을 늘렸지만 호출비 2배 기준을 넘었다. direct는 기존 20문항 중 3문항을 잃었다. 현재 default를 attributed로 유지하는 이유는 기존 동작 보존이며, 모든 추가 단계가 가장 좋은 설계라는 선언이 아니다. 사례 ID로 특정 경로를 고르는 규칙을 넣지 않았다. [사전 판정과 실제 배포 판단의 차이](../results/service-v3/deployment-decision.json).

## 실험용과 과거 구현

`joint`, `claims`, `documents`, `contextual`, `connected`, `demonstrated`는 단순화·검색·근거 연결을 검토한 실험 경로다. 기존 QA 보존 또는 새 사례 성과 기준을 통과하지 못한 후보도 비교 재현을 위해 남겨 두었다. CUPMem native 어댑터와 practical 서비스도 당시 고정 평가를 위한 코드다. 현재 단일 서비스가 이 모든 후보를 연속 실행하지 않는다.

현재 설계에서 이미 확인한 가장 중요한 빈틈은 **저장된 검토 상태 → 모델 문맥 → 최종 사실 선택**이다. 상태 인용의 구조 검사를 강화해도 잘못된 사실 선택을 자동으로 고치지는 못한다. 이 구분을 유지해야 새 검증 단계를 무조건 추가하는 실수를 피할 수 있다.
