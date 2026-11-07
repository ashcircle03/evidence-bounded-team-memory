# QA 단순화: 실제 비교와 채택 판단

**부가 단계 실패 시 이전 답을 보존하는 수정은 채택했다. 한 번에 답과 근거를 생성하는 `joint`는 전면 교체하지 않는다.** 호출을 줄이고 새 사례 일부를 개선했지만 기존 정답과 상충 처리의 순서 안정성을 잃었다. 선택 경로는 `--profile attributed`, 실험 경로는 `--profile joint`이며 CLI 기본값 `standard`는 그대로다.

| 평가 | 기존 attributed | 단순 joint |
|---|---:|---:|
| 이미 본 개발20개: 필수 답과 원문 근거 | 20/20, 이전 실제 호출의 정확한 재생 | 19/20, 같은 검색 문맥에서 새 생성 |
| 새12개: 필수 답과 원문 근거 | 7/12, 새 검색·생성 | 9/12, 새 검색·생성 |
| 새12개 모델 호출 | 51 | 12 |
| 새12개 실제 입력/출력 토큰 | 62,327 / 7,643 | 18,984 / 1,441 |
| 새12개 처리 시간 합계 | 133.91초 | 42.04초 |

새12개는 공개 Gitv2.48.0 문서 기반4개와 합성 팀 기록 변형8개다. 같은 원문 내 상충의 순서 반전 쌍도 있어 독립 자연 질문12개가 아니다. 검색 결과의 내용·순서와 모델 Qwen3-8B는 같지만 전체 토큰 예산을 같게 소진시킨 비교는 아니다. 캐시와 교대 실행의 영향이 있는 처리 시간보다 실제 호출·토큰 수를 우선 해석한다. 의미 채점은 개발 담당 AI가 원문과 대조했으며 독립 인간 검증은 없다.

[44개 실제 답·근거·판정](comparison.md) · [원문 판정 JSON](ratings.json) · [고정 기준](../../../evaluation/reference_qa/simplify/PROTOCOL.md) · [집계와 채택 조건](summary.json)

## 가져온 방식과 연결 의도

기존 LlamaIndex 혼합 검색과 작성자 메타데이터는 유지했다. [AQA](https://aclanthology.org/2024.emnlp-main.956/)의 출처별 답변과 [LangChain QuotedAnswer](https://github.com/langchain-ai/langchain/blob/langchain%3D%3D0.3.27/docs/docs/how_to/qa_citations.ipynb)의 답·인용 구절 구조를 결합해 **검색 → 출처별 답·근거 생성 → 원문 위치 연결**로 줄였다. 문서마다 검토하고 답을 다시 쓰고 인용을 뒤늦게 붙이던 단계가 후보에는 없다. 실제 스키마를 라이선스와 함께 재사용했으며, AQA의 원 모델·학습이나 전체 LangChain 체인을 재현한 것은 아니다.

[LangChain 단계별 fallback](https://github.com/langchain-ai/langchain/blob/langchain%3D%3D0.3.27/libs/core/langchain_core/runnables/fallbacks.py)의 접근은 기존 경로에 적용했다. 부가 단계에서 예외가 나면 이전 답과 근거를 반환하면서 `partial`, `stage_failures`로 실패를 표시한다. 다른 API나 자동 재시도를 추가하지 않는다. [설계 의도·입출력 계약](../../../docs/reference-joint.md)

## 문항별 비교

| 새 사례 | attributed | joint | 원문에 비추어 본 차이 |
|---|---|---|---|
| rebase error 동작 | 실패 | 성공 | 기존 출력은 올바른 주답 뒤에 “error에서도 계속 진행”이라는 모순된 설명을 덧붙였다. |
| pull.ff=only | 성공 | 성공 | fast-forward 제한과 merge.ff 우선관계를 보존했다. |
| push.autoSetupRemote | 성공 | 성공 | upstream 없음, default push, 세 모드 조건을 보존했다. |
| rerere.autoUpdate | 성공 | 성공 | 기본 false와 clean resolution 이후 index 갱신을 답했다. |
| 서로 다른 문서의 true/false | 성공 | 성공 | 양쪽 기록을 인용한 답을 남겼다. |
| 한 문서의 true/false, 정순 | 실패 | 실패 | 기존은 false만, joint는 true만 답했다. |
| 한 문서의 true/false, 역순 | 실패 | 성공 | joint만 양쪽을 보존했다. 두 순서 모두 성공해야 하는 기준은 미달이다. |
| rebase.stat 상충 | 성공 | 성공 | 실험 true와 매뉴얼 false를 함께 남겼다. |
| local warn / CI error | 실패 | 실패 | 동작 내용은 맞지만 절차 기록만 인용했다. 동작을 설명하는 검색 원문3의 인용이 빠졌다. |
| 무관한 enabled=true | 성공 | 성공 | autoUpdate와 다른 설정을 섞지 않았다. |
| 보고서 작성자 | 실패 | 실패 | 기존은 정답 Mira에 무관한 작성자를 추가했다. joint는 수신자 Noah를 골랐다. |
| 원문에 없는 gc.auto | 성공 | 성공 | 모델 지식으로 기본값을 만들지 않고 답 없음으로 반환했다. |

기존20개에서 joint가 잃은 것은 strict zip 상충 사례다. PEP618의 `ValueError`만 답하고 입력에 있던 Fay의 `LengthMismatchError` 기록을 누락했다. 깨끗한 PEP618 문항은 여전히 맞혔다. 따라서 단순화의 실패를 일반 zip 지식 부족이나 검색 누락으로 설명할 수 없다.

작성자 사례의 기존 경로는 초안에서 Mira를 맞혔다. 이후 문서 판정이 Git 설명서와 Eli의 다른 설정 기록을 CONTRADICTS로 잘못 분류했고, 재작성에서 이를 추가 작성자로 만들었다. 이는 실제 `draft_raw`·`document_judgments`·최종 출력으로 확인한 경로다. 여러 단계를 거친다는 사실이 더 나은 검증을 보장하지 않는다.

## 인용 점수의 범위

일차 점수는 필수 답과 그것을 지지하는 반환 원문 문단의 존재를 함께 본다. **19/20은 모든 인용·모든 좁은 구절이 정확하다는 뜻이 아니다.** joint는 PEP680에서 올바른 Abstract[1] 외에 tomli만 설명하는 부적절한 Source3도 붙였다. Confluence 문항은 올바른 전체 원문을 반환했지만, 좁혀 고른 구절은 업로드가 아닌 Freemium 전략 설명이었다. 두 오류를 판정 파일에 별도로 기록했다.

joint의 기존20개 중7개와 새12개 중1개는 좁은 구절을 원문에서 그대로 찾지 못했다. 이때 원래 입력 문단을 반환하고 `quote_not_located`·`partial`을 표시한다. 새 작성자 사례처럼 문자열 위치가 맞아도 주장 의미가 틀릴 수 있다. 문자 위치 검증을 의미 정확성으로 채점하지 않았다.

## 실행·검증·비용

- 119975: FAILED/1:0, 2분41초. 새 실행 도구가 HTTPX의 예약된 `trace` 확장 키를 잘못 사용했다. 모델 응답 전 실패했다. 실패 원본·로그를 보존했다.
- 119979: COMPLETED/0:0, 4분54초. HTTP 전송의 기록 키만 `reference_trace`로 고친 별도 버전이다. 모델·입력·프롬프트·평가 기준은 그대로다. GPU1·CPU8·RAM48G·conda 계산 노드에서 수행했다.
- 총 **7.58 GPU분**, 실패와 준비 시간 포함. 유료 외부 모델 API0회, 실제 로컬 모델 호출83회, 결과44개. 최대 RSS는 batch 단계에 기록되며 모델 GPU 메모리를 나타내는 값은 아니다.
- 전체 코드 검사246개 통과. 기존20개는17개 실제 부가 단계의 입력이 정확히 같은 재생에서 답과 근거가 보존됐다. 새로운 전체20개 재추론 성공으로 표현하지 않는다.
- 원문 위치·실제 모델 입력·출력·44개 결과·코드/입력/평가기준 SHA와 새12개 양쪽 검색 결과 일치를 검증했다. 결과를 보고 프롬프트나 의미 규칙을 추가하지 않았다.

[실행 검증](verification.json) · [기존20개 보존](preservation.json) · [전송 수정 검사](transport-smoke.json) · [Slurm·누적 비용](accounting.json) · [실제 요청·응답](calls.jsonl)

QA 누적77.62/90, CUPMem450.18/460, 캠페인745.23/760 GPU분이다. 두 작업은 모두 종료했고 추가 제출은 계획하지 않았다.

이번 결과로 동일 성능의 단순 대체물을 완성했다고 주장하지 않는다. 과거 결정 재검토·작성자 승인·병합도 이 실험의 평가 범위가 아니다. 안전하게 채택한 것은 기존 답을 잃지 않는 실패 처리이며, 단순화 후보는 효율의 가능성과 남은 실패 원인을 보여주는 실행 가능한 비교 구현으로 남긴다.
