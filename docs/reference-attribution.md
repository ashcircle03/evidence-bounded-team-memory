# 상충 답 보존과 문장별 인용

이 경로는 기존 `checked`의 혼합 검색·작성자 전달·인용 QA·문서별 검토 위에 연결한다. 기존 `checked`의 19/20 결과와 원출력을 비교군으로 고정한다. 사례 ID나 정답 키로 분기하지 않는다.

| 문제 | 재사용한 방법 | 설계 의도 |
|---|---|---|
| 반대 근거를 알아도 답 하나를 버림 | [AQA, EMNLP2024](https://aclanthology.org/2024.emnlp-main.956/) §3.4.1, 부록 A.1의 conflict-aware basic prompting | 검색 근거를 함께 읽으며 출처별 답을 남기는 예시를 제공한다. |
| 맞는 부연에 인용이 없음 | [LangChain0.3.27 citation_fuzzy_match](https://github.com/langchain-ai/langchain/blob/langchain%3D%3D0.3.27/libs/langchain/langchain/chains/openai_functions/citation_fuzzy_match.py)의 `FactWithEvidence`·직접 인용 프롬프트 | 답변 전체와 각 문장을 함께 주고 근거 원문 구절을 추출한다. 원래 답 문구와 기존 인용은 유지한다. |

## AQA 연결

AQA의 공개 Drive 학습 예시를 열 수 없어 원형3-shot을 그대로 재현하지 못했다. 대신 논문 Figure1의 상충 대통령 기록을 바꾸어 표현한1-shot을 사용한다. Git·PEP·EverMemBench 평가 내용과 무관한 예시다. 저자 모델 대신 같은 로컬 Qwen3-8B를 사용하며 원 논문 성능 재현이라고 부르지 않는다.

기존 문서 판정에서 반대로 분류됐지만 반환 인용에서 빠진 원문이 있을 때만 호출한다. 고정20문항 중 zip·notes·Confluence의3문항이 이 조건을 만족한다. 후보가 기존 인용 원문과 누락된 반대 원문을 모두 인용해야 교체한다. 이 출처 점검은 프로젝트 연결 코드이며 의미 정확성의 증명은 아니다.119945에서 zip은 두 답을 보존했고 notes·Confluence는 후보를 채택하지 않아 기존 정답을 유지했다.

## 원문 구절에 연결하는 인용

LangChain의 `FactWithEvidence(fact, substring_quote)` 스키마와 정확한 인용 프롬프트를 MIT 라이선스와 함께 보존했다. 전체 체인을 실행한 것은 아니다. 기존 로컬 Qwen/LlamaIndex 전송에 스키마와 프롬프트를 연결했다. 원형과 달라진 부분은 다음과 같다.

- 이미 생성한 답과 인용 없는 문장 목록을 입력한다. 전체 답은 this variable 같은 지시어의 대상을 해석하는 문맥이다.
- 기존 답을 다시 쓰지 않는다. 반환 fact 목록이 요청 문장과 다르면 후보를 버린다.
- 원형의 fuzzy regex 대신 공백 배치만 다른 원문 구절까지 복원한다. 단어·문장부호·코드 기호는 그대로 일치해야 한다. 출처 번호를 모델이 추측하게 하지 않고 실제 구절이 있는 문서에서 계산한다.
- `[N]`만 원래 답 문자열에 삽입한다. 기존 인용과 답의 문구는 삭제하지 않는다. 구절을 못 찾은 문장은 그대로 두고 `unattributed_sentences`에 남긴다.
- `quote_citation_reviews`에 추출 구절과 원문 내 위치를, `quote_attribution_raw`에 모델 원출력을, `pre_citation_raw`에 수정 전 답을 남긴다.

정확한 문자열 일치는 출처 존재 검사다. 의미 지지는 별도 원문 평가가 필요하므로 `citation_entailment_verified`를 true로 바꾸지 않는다. `status=ok`도 의미 정답 인증이 아니다. `attribution_status=partial`은 근거를 붙이지 못한 문장이나 문장 분할 잔여물이 있다는 뜻이다.

## 실제로 시험했지만 채택하지 않은 방식

[ALCE의 공식 TF-IDF 사후 인용](https://github.com/princeton-nlp/ALCE/blob/246c476a4edfc564266b7346b6e29ef4861ae937/post_hoc_cite.py)은 두 누락 근거를 찾았지만 tomllib 이름을 말하지 않는 Motivation 문단을 모듈 이름의 근거로도 붙였다. 유사도 상위 문단이 항상 해당 주장을 지지하지 않았다.

[공개 DeBERTa NLI 분류기](https://huggingface.co/cross-encoder/nli-deberta-v3-base)는 ALCE의 entailment 평가 아이디어를 차용한 별도 작은 모델 실험이었다. 원형 AutoAIS 재현이 아니다.136쌍 중32쌍은512토큰에 맞춰 premise가 잘렸고, 필요한 두 근거를 거절했다. 특히 subjectPrefix를 가리키는 this variable에 패치 경로의 noprefix 문단을 붙였다. 이 모델을 인용 검증기로 채택하지 않는다. 실패 원출력·소스·실행 기록은 보존한다.

## 호출과 검증 범위

기존 JSONL `import_history`/`ask` 계약을 그대로 사용한다. `python -m team_memory.reference_qa --profile attributed ...`로 선택하며 NLI 가중치는 필요 없다. 실제 사용 가능한 기본 QA 구성요소와 Slurm 실행 환경은 [기존 사용법](reference-team-profile.md)을 따른다. CLI 기본값은 비교를 위해 `standard`로 유지한다.

119945는 이전115회 호출을 재사용하고 AQA3회만 추가했다.119957은 모델 준비 후 TIMEOUT으로 끝났고, 같은 코드를20분으로 배정한119960에서 그118회와 AQA 이후 답을 고정하고14개 답에 구절 추출을 추가했다. 매번20문항 전체를 새 추론한 실행이라고 표시하지 않는다.119960은 GPU1·CPU8·48G·20분·conda·노드 지정 없음이며 실제5분17초에 완료했다. 최종 공백 복원은 실제14개 프롬프트의 동일성을 확인한 결정적 로컬 재생이며 추가 추론은 없다. 두 인용 누락과 상충1건을 복구하고 기존19개 답·근거를 보존했다. [실행 전 고정](../results/reference-qa/quote-normalized-v1/freeze.json) · [재사용 범위](../results/reference-qa/quote-v1/reference-provenance.json) · [최신 결과](../results/reference-qa/README.md)
