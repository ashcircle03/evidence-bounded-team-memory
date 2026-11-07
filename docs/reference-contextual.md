# 검색 피드백과 원문 맥락을 유지하는 QA 후보

이 후보는 첫 검색에서 확인한 사람·사건을 다음 검색에 사용하고, 선택한 구절의 원문 맥락을 최종 답 생성까지 유지한다. `contextual` 프로필은 개발 비교용이며 기존 선택 경로 `attributed`를 자동으로 대체하지 않는다.

| 책임 | 가져온 구현·의도 | 적용 범위 |
|---|---|---|
| 여러 검색 질의의 결과를 결합 | [LlamaIndex QueryFusionRetriever](https://developers.llamaindex.ai/python/framework/integrations/retrievers/reciprocal_rerank_fusion/) | 설치된0.14.25의 질의 생성과 RRF를 직접 호출한다. BM25와 결과 top8을 사용한다. |
| 찾은 사실을 후속 검색에 반영 | [IRCoT](https://aclanthology.org/2023.acl-long.557/)의 검색·추론 교차 목적 | 첫 top8 원문을 질의 생성 프롬프트에 추가하고 후속 질의3개만 만든다. 원 논문의 문장별 CoT·반복 종료·데모 전체 재현은 아니다. |
| 작성자·날짜를 검색과 답변에서 유지 | 실제 원문 메타데이터와 [LongMemEval의 시간 정보 문제 분석](https://arxiv.org/abs/2410.10813) | 실제 작성자·기록 시각을 검색 키에 포함한다. LongMemEval의 사실 추출·시간 범위 필터 구현은 가져오지 않았다. 기록 시각을 사건 시각으로 자동 치환하지 않는다. |
| 선택한 구절의 지시 대상·조건을 보존 | [Attribute First](https://aclanthology.org/2024.acl-long.182/)의 fusion-in-context | 기존 공식 프롬프트 발췌를 사용한 선택 뒤, 해당 구절이 들어 있는 검색 문단 전체와 메타데이터를 함께 전달한다. |
| 각 답에 근거 연결 | 기존 LangChain QuotedAnswer와 원문 위치 복원 | 최종 답이 인용 구절을 다시 고른다. 반환 원문·작성자·시각·위치와 좁은 구절을 함께 보존하며 문자열 일치를 의미 인증으로 취급하지 않는다. |

이전 후보는 선택한 짧은 구절만 생성기에 전달했다. 이번에는 인물·조건을 이해할 원문 문단도 전달하므로 입력 토큰이 늘어난다. 모델 단계는 검색 질의 생성1회, 구절 선택1회, 답 생성1회다. 실패 시 모델 재시도를 추가하지 않는다. 검색에 사용한 질의·초기 원문, 선택 구절, 생성 원출력, 최종 근거를 남긴다.

Python의 `ContextualQA`는 기존 `import_history`와 `ask`를 지원한다. JSONL CLI에서는 기존 인자와 함께 `--profile contextual`을 지정한다. 답과 각 주장에 동일한 근거 객체를 연결하며, 작성자 승인을 추론하지 않는다. Git 전송·승인·병합은 이번 수정 범위에 포함하지 않는다.

[고정 비교와 채택 기준](../results/reference-qa/contextual-v1/PROTOCOL.md) · [검색 어댑터](../team_memory/reference_retrieval.py) · [독해 어댑터](../team_memory/reference_contextual.py)

실제 비교에서 Ever 답·근거는 독해만2/10, 검색만1/10, 결합2/10이었다. 기존20은17/20으로 보존 기준을 통과하지 못했다. 첫 검색에서 잘못 연결한 사람을 후속 질의가 이어받고, 긴 원문을 전달해도 작성자·시간·조건을 놓치는 사례가 남았다. 구현은 실험용으로 유지한다. [전체 결과와 출력 계약 실패의 구분](../results/reference-qa/contextual-v1/README.md)
