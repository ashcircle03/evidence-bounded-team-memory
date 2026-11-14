# readers — 검색, 답변, 상태 문맥, 인용

기본 서비스는 `attribution.AttributedQA`, 비교 경로는 `attribution.CitedSourceQA`다. 둘은 검색·초기 독해·상태 문맥·구절 인용을 공유한다.

| 파일 | 주요 API | 입출력과 의도 |
|---|---|---|
| `retrieval.py` | `ReferenceQA`, `local_components`, `format_response` | 원문을 LlamaIndex로 검색하고 번호 붙은 witness와 초안 반환. 실제 tokenizer로 입력 예산 계산 |
| `context.py` | `expand_review_context`, `resolution_view`, `reconsideration_view` | 관련 원문과 검토 상태를 연결. 의미 분류를 새로 하지 않음 |
| `state_citations.py` | `review_sources` | 실제 제안·투표의 불변 snapshot을 별도 상태 근거로 렌더링 |
| `checking.py` | `ConflictCheckedQA` | 초안의 문서별 판단과 필요한 재작성. 현재 whole-answer 검사 한계는 유지·공개 |
| `attribution.py` | `AttributedQA`, `CitedSourceQA`, `repair_omitted_answer` | 기존 조건부 AQA와 두 reader 조합, 공통 인용 연결 |
| `citations.py` | `add_quote_citations`, `quote_span` | 미인용 문장을 정확한 원문 구절과 연결. 답 문구를 재작성하지 않음 |
| `fallback.py` | `preserve_answer`, `stage_failure` | 추가 단계 실패 시 기존 답·근거와 오류를 함께 보존 |
| `prompts.py` | 기존 template 상수 | 프롬프트 변경의 위치와 검토 범위를 명확히 유지 |

입력: 질문, `SourceStore`, 명시적인 로컬 모델 endpoint, 관련 review context.
출력: `raw`, `answers`, `citation_sources`, 단계별 진단과 경고. witness에는 원문 ID·작성자·시각·quote/start/end가 있다. 상태 witness는 `evidence_type=review_state`로 구분한다.

이 계층은 사용자 투표를 만들거나 QA 해석을 확정 사실로 저장하지 않는다. 인용 위치 일치, `status=ok`, source ID 커버리지는 의미 정답 보장이 아니다. 원문 값과 검토 상태의 근거 역할을 바꾸지 않는다.

현재 추가 검사의 한계·원형 변형·보류한 대안은 [연결 감사](../../docs/reference-composition-audit.md)를 참고한다.

검사: `scripts/check.py reference --fail-on-skip`. 실제 모델 성능은 `evaluation/reference_audit/` 등 동결 실험과 구분한다. 새로운 후보를 이 기본 경로에 바로 붙이지 말고 `experiments/readers`에서 비교한다.
