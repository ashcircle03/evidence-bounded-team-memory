# 팀 기록의 출처를 보존하는 QA 구성

이 문서는 `checked`까지의 기존 기반과 사용법을 설명한다. 그 위에 AQA·LangChain 인용을 연결한 최신 `attributed`는 같은 개발20문항에서 **20/20, 기존19개 답·근거 유지, 부연 인용 누락2건 복구**를 확인했다. [최신 설계와 변경 범위](reference-attribution.md) · [결과와 한계](../results/reference-qa/README.md). 아래19/20·미해결 설명은 당시 checked 경로의 기록이며 현재 attributed의 결과와 구분한다. 승인된 현재 지식, 자동 재검토, 병합 상태 머신 전체를 대체하지 않는다. `team`은 실패한 중간안이다.

| 실패 | 실제 가져온 방식 | 적용 이유와 범위 |
|---|---|---|
| 정답 문단이 의미 검색 상위4개에 없음 | LlamaIndex `BM25Retriever` + `QueryFusionRetriever(mode='reciprocal_rerank')` | 원래 의미 검색 상위4개와 단어 검색 상위4개를 합쳐 최대8개를 유지한다. 기존 후보를 버리지 않고 문서 키워드를 보완한다. `num_queries=1`로 질문 생성 호출은 하지 않는다. |
| 본문에서 언급한 수신자를 작성자로 오인 | LlamaIndex 메타데이터 필드와 `MetadataMode.LLM` | envelope의 실제 작성자와 기록 시각을 입력까지 전달한다. 본문에서 작성자를 추측하지 않는다. 임베딩 입력은 바꾸지 않는다. |
| 양쪽 원문을 받았는데 한쪽 답만 선택 | ConflictScore 공식 문서 판정 함수와 R-RAG 피드백 흐름 | 실제 원문별 지지·반대·무관 판정을 초안과 함께 다시 읽는다. Table14 지침만 붙인 중간안의 실패와 구분한다. |
| 반대 기록을 알아도 재작성에서 한쪽을 누락 | LlamaIndex `Accumulate` + 공식 citation QA 템플릿을 시험했으나 **기각** | 마지막 상충은 복구했지만 무관한 문서에서 잘못된 답을 추가해18/20으로 하락했다. 현재 `checked`는 이 단계를 호출하지 않는다. |

[공식 혼합 검색 예제](https://developers.llamaindex.ai/python/framework/integrations/retrievers/reciprocal_rerank_fusion/) · [공식 메타데이터 전달](https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/usage_documents/) · [ConflictScore 논문·Table14](https://arxiv.org/html/2606.26437v1) · [저자 공식 저장소](https://github.com/microsoft/ConflictScore/tree/a8868e5cd98bff81935a1766b54a02ad3eab9e8f)

검색 점수·결합·청킹·문맥 압축을 새로 구현하지 않았다. `reference_prompts.py`는 CC BY4.0으로 공개된 논문의 Table14 지침을 가져오고 출처를 표시한다. 논문의 보고서 형식을 QA로 바꿨다. 작성자와 수신자 구분, 같은 조건의 상충은 양쪽 답·출처 보존, 다른 조건은 조건별 답변, 무관한 충돌은 답변을 막지 않는다는 부분은 사용자 요구를 연결한 명시적 계약이다.

첫 수정안(`team`, fix-v1)은 **ConflictScore 전체 재현이 아니다**. Table14의 지침만 붙인 실제 실행은17/20의 답 내용을 맞혔지만, 인용 표기를 연결하지 못하고 상충 기록을 누락하여 답·반환 인용 기준으로8/20이었다. 이 실패 결과를 보존한다. 논문의 이진 답 선택용 Table17은 양쪽 기록을 남기려는 목적과 달라 그대로 적용하지 않았다.

## 실제 판정 코드를 사용하는 후속안 (`checked`)

1. 같은 혼합 검색과 메타데이터를 사용해 원래 CitationQueryEngine으로 초안을 만든다. 처음부터 균형 서술로 감싸지 않는다.
2. 검색된 청크를 원문 ID별로 묶어 [저자 구현의 `evaluate_document_support`](https://github.com/microsoft/ConflictScore/blob/a8868e5cd98bff81935a1766b54a02ad3eab9e8f/src/eval_with_conflict_score/eval_all_calibration.py)를 그대로 호출한다. 각 원문이 질문에 대해 초안을 지지하는지, 다른 답을 주는지, 무관한지 판정한다.
3. 반대 판정이 있으면 원문·초안·문서별 판정을 Qwen에 다시 주고 출처별 답을 작성하게 한다. 판정도 오류가 날 수 있음을 명시하고 원문을 최종 근거로 사용한다. 조건 차이는 조건별 답으로 남긴다.
4. `[N]`와 명시적인 `Source N`을 같은 출처 번호로 연결한다. 모델 원출력을 바꾸거나 근거 없는 인용을 삽입하지 않는다. 번호가 없거나 범위를 벗어나면 `partial`이다.

공식 파일과 MIT 라이선스는 `team_memory/_vendor/conflictscore/`에 보존한다. 외부 API 대신 기존 로컬 Qwen에 연결하는 전송 어댑터만 바꿨다. 문서 판정 출력은384토큰으로 제한하고 같은 GPU에서 최대4요청을 묶어 처리한다. 정답 키는 사용하지 않는다. [출처·변경 범위](../results/reference-qa/fix-v2/reference-provenance.json)를 기록한다.

공식 예제의 전체 답 직접 검토 변형을 따르며, 전체 claim 분해나 논문의 ConflictScore 수치를 재현한 것은 아니다. 다중 주장 일부가 지지될 때 나머지 오류를 놓칠 수 있는 한계가 있다. 문서별 판정이 파싱되지 않으면 무관하다고 간주하지 않고 검토 미완료를 표시한다. R-RAG의 피드백 흐름을 가져왔으나 이진 선택 대신 양쪽 기록 보존이라는 사용자 요구에 맞춰 재작성 계약을 적용했다.

파서는 저자 코드의 JSON → 명시적인 `answer`/`support` 필드 → XML 순서의 복구를 가져왔다. Qwen이 문자열 안에 줄바꿈을 그대로 출력해 JSON 전체 파싱이 실패해도 명시된 판정 표기를 복구한다. 이유 문장의 단어를 보고 판정을 새로 추측하지 않는다. 알 수 없는 값은 원형의 무관 처리 대신 `ERROR`로 남긴다.

검토 후 기각한 `Accumulate`는 [공식 response synthesizer](https://developers.llamaindex.ai/python/framework/module_guides/querying/response_synthesizers/)의 문서별 독립 QA 방식이다. 반대 원문의 인용이 누락됐을 때 지지·반대 문서 각각을 읽고 원출력을 upstream 방식으로 병렬 나열했다. 원출력은 `generation_segments`, 이전 답은 `revised_raw`에 보존했다. 그러나 실제 Qwen은 `format.notes`와 `notes.rewriteMode`의 다른 기본값을 `notes.mergeStrategy`의 답으로 만들었고, 다른 프로젝트 charter 경로를 Huilan Chen의 보고서 경로로 답했다. 기존 정답을 잃었으므로 기본 경로에서 제거했다. 재현용 함수만 남기며 `evaluation.reference_qa.accumulate_replay`에서 호출한다.

문서 판정의 오탐은 현재 선택안에도 남는다. 또한 **인용이 있다는 것만으로 해당 문서의 답을 완전히 보존했다고 보장하지 않는다.** 선택한19/20 구성의 마지막 실패는 올바른 반대 판정을 받아도 Qwen 재작성에서 `LengthMismatchError`를 버린 것이다. 질문·대상·동작이 일치하는 근거인지 판단하는 단계와, 그 근거를 답에서 누락하지 않는 단계가 모두 필요하며 후속 기능이 검증됐다고 표시하지 않는다.

원래 검색 청크는512토큰·64토큰 겹침을 유지한다. 인용 재분할 상한은1024토큰·겹침0으로 두어 짧은 출처 헤더와 검색 청크를 함께 전달한다. 반환 근거에서는 헤더를 분리하고 원문 ID·정확한 문자 위치를 검증한다. 헤더가 잘려 안전하게 대응시킬 수 없으면 오류를 반환한다. 작성자·시각 이외의 원문 ID·문자 위치는 모델에게 노출하지 않는다.

## 사용

`requirements-reference.txt`를 격리 환경에 설치하고 기존 로컬 Qwen·임베딩 경로를 사용한다. Aurora에서는 GPU 계산 노드·conda·개인 `NLTK_DATA`가 필요하다. [기존 환경 설정](reference-reuse.md#사용)을 참고한다.

```bash
python -m team_memory.reference_qa \
  --profile checked \
  --store /path/to/reference-records \
  --model-path /local_datasets/.../Qwen3-8B/... \
  --embedding-path /path/to/existing/local/embedding \
  --api-base http://127.0.0.1:PORT/v1
```

JSONL의 `import_history`/`ask` 입출력은 기존과 같다. CLI와 Python `ReferenceQA` 기본값은 기존 `standard`다. 검토 포함 Python 호출은 `ConflictCheckedQA`를 사용한다. `team`은 지침만 추가한 중간 구성의 비교용이다. 상충 답변은 `raw`/`answers[].text`에서 출처별 번호 인용을 붙이고, 원문은 `citation_sources`와 `answers[].evidence`로 반환한다. 검토 결과는 `document_judgments`, 이전 초안은 `draft_raw`, 재작성 여부는 `revised`로 반환한다. `status=ok`는 실행·인용 번호 연결 성공이며 내용 정답이나 entailment 인증이 아니다.

## 비교 조건

같은 Qwen3-8B, 같은 MiniLM 인코더, 같은20문항과 전체 기록을 사용한다. 이전15개 성공을 회귀 기준으로 삼는다. 정답 키·기존 답은 모델 입력에 포함하지 않는다. [실행 전 고정 정보](../results/reference-qa/fix-v1/freeze.json)는 코드·입력·기존 결과·채점 기준 해시를 포함한다. [측정한 v2 원본 코드](../results/reference-qa/run-v2/source)를 보존했다.

로컬 연결 검사는 실제 LlamaIndex와 가짜 디코더를 사용한다. 작성자 전달, 두 원문 인용의 위치 복원, 재시작, 기존 의미 검색 후보를 유지한 단어 검색 보완, 명시적인 판정 파싱, 실제 upstream Accumulate 호출을 확인한다. 이는 실제 모델 정답률이 아니다. 실제 결과는 [QA 실행 기록](../results/reference-qa/README.md)에서 버전별로 구분한다.

전체 실행119872의 초안·문서 판정과 실제 입력을 고정한 뒤, 파서 수정119928은20문항 모두를 재생하며 새로 도달한 재작성1회만 Qwen으로 실행했다. 후속 Accumulate 검증119944도20문항의 실제 출력을 재사용하고, 일반 조건으로 선택된3문항의 문서별 QA 8회만 추가했다. 매번20문항 전체를 새로 추론한 결과로 표시하지 않는다. 각 실행의 입력·코드·이전 출력 해시, 실제 호출과 답변 연결을 검사했다. 현재 `ConflictCheckedQA`의 클래스 AST와 QA·프롬프트 파일은 선택한119928 구성과 일치한다.

이번 비교는 이미 본 개발 문항의 수정·회귀 검사다. 새 holdout 성능이나 전체 팀 메모리 문제의 해결을 의미하지 않는다. 검색·출처 전달·서술 지침이 함께 바뀌므로 각 요소의 인과 효과를 분리 측정했다고 주장하지 않는다.


상태·입출력 계약 수정과 주장별 근거 후보는 [reference-claims](reference-claims.md), 원래 데이터셋 구성과 평가 범위는 [evaluation-coverage](evaluation-coverage.md)를 참조한다. 새 후보는 실제 확대 평가가 끝나기 전 채택한 설계로 취급하지 않는다.
