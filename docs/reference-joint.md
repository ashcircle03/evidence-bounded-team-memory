# 답과 근거를 함께 만드는 단순 구성

목적은 기존 답의 정확도·출처·조건을 보존하면서 문서별 판정과 반복 재작성의 필요성을 줄이는 것이다. **실제 비교 후 `joint`의 전면 채택은 보류했다.** 새12개에서 호출51→12, 필수 답·원문 근거7/12→9/12였지만 기존20개는19/20이 되었고 같은 문서 내 상충의 순서 반전에 실패했다. [고정 기준](../evaluation/reference_qa/simplify/PROTOCOL.md)에 따라 선택 경로는 `attributed`를 유지한다. 기본 CLI도 변경하지 않는다. [전체 결과](../results/reference-qa/simplify-v2/README.md)

| 역할 | 가져온 구현·접근 | 우리 문제에 맞춘 범위 |
|---|---|---|
| 원문 검색·작성자 전달 | 기존 LlamaIndex BM25+dense RRF·메타데이터 | 검색 후보와 순서를 그대로 유지해 독해 단계 차이만 비교한다. |
| 서로 다른 답을 남김 | [AQA, EMNLP2024](https://aclanthology.org/2024.emnlp-main.956/)의 source-specific answer prompting | 조건이 다른 답은 조건과 함께, 같은 조건의 상충은 출처별로 함께 답한다. 하나의 원문 안에 있는 다른 주장도 읽는다. 기존 figure1의 별도 예시를 유지한다. |
| 답과 인용을 함께 출력 | [LangChain0.3.27 qa_citations](https://github.com/langchain-ai/langchain/blob/langchain%3D%3D0.3.27/docs/docs/how_to/qa_citations.ipynb)의 `Citation`·`QuotedAnswer` | 각 답이 자신의 source 번호와 근거 구절을 갖는 목록으로 출력한다. 먼저 답을 고르고 나중에 근거를 붙이는 단계는 없다. |
| 근거를 실제 원문에 연결 | 기존 immutable source 객체와 공백 배치만 허용하는 위치 복원 | Source 번호는 해당 검색 결과에만 대응한다. 구절이 실제로 있는지 검사하고 원문의 문자 위치를 반환한다. 의미 지지를 자동으로 인증하지 않는다. |
| 기존 정답 보호 | [LangChain with_fallbacks](https://github.com/langchain-ai/langchain/blob/langchain%3D%3D0.3.27/libs/core/langchain_core/runnables/fallbacks.py)의 단계별 fallback | 기존 attributed 경로의 부가 단계가 실패하면 이전 답을 반환하고 실패 단계·오류 종류를 표시한다. 다른 API나 재시도를 추가하지 않는다. |

정상 입력에서 `joint`는 `검색 → 답·출처별 근거 생성 → 원문 연결`을 수행한다. 문서별 SUPPORTS/CONTRADICTS 판정, 초안 재작성, AQA 재시도, 사후 문장 인용은 호출하지 않는다. 비교 문맥은 한 호출에 들어가도록 고정했다. 미래의 긴 입력에서 LlamaIndex compact가 여러 번 refine하면 호출이 늘 수 있으므로 모든 입력에서 무조건1회라고 보장하지 않는다.

`QuotedAnswer` 스키마는 MIT 라이선스와 함께 가져왔다. 원형의 OpenAI tool binding 대신 기존 로컬 Qwen에 JSON 스키마를 프롬프트로 전달한다. 단일 답 구조를 출처별 답 목록으로 확장한 것은 우리 기록 보존 요구에 맞춘 연결이다. AQA 원 모델·학습·데이터의 성능 재현이나 LangChain 전체 실행 체인의 재현으로 부르지 않는다.

## 입출력

기존 `import_history`/`ask` JSONL 계약을 유지한다. `python -m team_memory.reference_qa --profile joint`에 기존 store·model-path·embedding-path·api-base 인자를 사용한다. Python에서는 `JointSourceQA`를 사용한다. 웹 UI·MCP 서버는 만들지 않는다.

- `answers[]`: 각 답의 문구와 그 답에 대응하는 원문 evidence 객체다.
- `claims[]`: 답별 source 번호·실제로 복원한 `quoted_spans`·미복원 구절 진단을 갖는다. 같은 원문을 가리키더라도 서로 다른 답 항목을 합치지 않는다.
- `generation_raw`: 모델의 실제 JSON 출력이다. `raw`는 각 모델 답 문구와 Source 번호를 연결해 렌더링한 문자열이다.
- 유효한 source 번호와 구절 매칭은 구분한다. 구절을 못 찾더라도 번호가 유효하면 원래 입력 문단을 반환하고 `quote_not_located`·`status=partial`을 표시한다. 조작된 구절이나 만들어낸 위치를 반환하지 않는다.
- `insufficient`: 원문에서 답을 못 찾아 빈 답 목록을 반환했다. `error`: 구조화 출력을 해석하지 못했다. 이것을 정답으로 처리하지 않는다.

기존 경로에서 부가 단계가 실패하면 원래 답·근거를 유지한 `partial`과 `stage_failures`를 반환한다. 호출자는 답의 존재와 단계 실패를 함께 표시해야 한다. 취소/KeyboardInterrupt는 fallback으로 삼키지 않는다.

인용 번호가 있다는 사실은 의미 정확성의 증명이 아니다. 같은 문서에서 반대 주장을 누락하거나 관련 없는 원문을 인용하는 오류는 여전히 모델에서 발생할 수 있으며, 원문 기반 평가의 실패로 처리한다. 승인된 현재 지식·과거 결정 재검토·병합 상태를 이 QA 구성으로 해결했다고 주장하지 않는다.

## 비교 범위

기존20개는 이미 본 개발셋이며 선택된 원문을 고정해 joint를 새로 생성한다. 기존 attributed20개는 실제17개 부가 단계 입력의 동일성을 검사한 재생으로 보존했다. 새12개는4개의 공개 Git 질문과8개의 합성 변형이며 두 구성 모두 새로 전체 기록을 검색·독해한다. 같은 모델·검색의 비교지만 사례 설계자와 채점자가 동일하므로 독립 자연 벤치마크 성능과 구분한다.

## 구현에서 유지할 것과 미해결 사항

부가 단계 예외가 이미 생성된 답을 없애던 오류는 고쳤다. 기존20개와17개 부가 단계의 정확한 입력을 재생해 답과 반환 근거가 동일함을 확인했다. 예외 주입 검사는 document review·AQA repair·quote attribution 실패 시 이전 답과 실패 진단이 함께 반환되는지 확인한다. 이 수정은 예외 처리이며 모델의 의미적 오답을 자동 판별하지 않는다.

단순 구성은 재작성 단계를 제거했지만 문서 내부의 여러 주장을 빠짐없이 고르도록 보장하지 않는다. 작성자 질문에서 `record_author`와 본문의 `@수신자`를 혼동했고, 조건과 동작을 서로 다른 기록에서 결합할 때 한쪽 원문만 인용했다. 기존 구성도 작성자를 맞힌 초안을 문서 검토가 오히려 망쳤다. 따라서 반복 검토를 많이 붙이면 안전해진다는 가정도 이번 결과로 지지되지 않는다.

다음 변경은 이 세 책임—주장 누락 방지, 작성자 식별, 결합한 주장 전체의 근거 선택—중 무엇을 해결하는지 명확해야 한다. 문항별 예외를 더하거나 이번 결과를 보고 프롬프트를 다시 고치지는 않았다. `joint`는 실험용 API로 남기며 완전한 대체 경로로 권장하지 않는다.

[실행·진행 기록](../results/reference-qa/simplify-v2/progress.json) · [원형·변형 내역](../results/reference-qa/simplify-v2/reference-provenance.json) · [기존20개 보존](../results/reference-qa/simplify-v2/preservation.json)
