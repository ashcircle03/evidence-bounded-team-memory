# 레퍼런스 원형과 현재 연결 감사

2026-11-14. 현재 파일, 저자 공개 구현의 고정 revision, 저장된 실제 모델 입력·출력을
대조했다. **원형의 효과가 현재 조합에도 성립한다고 볼 근거는 부족하며, 실제로
검사 목적이 약해진 연결을 확인했다.** 다만 모든 추가 단계가 해로운 것은 아니다.
새 모듈이나 운영 프롬프트를 추가하지 않았다.

현재 결론은 코드·기존 출력에 근거한 진단이다. 새 동일 조건 비교는 Slurm122740으로
제출했지만 계정 GPU 한도 때문에 대기 중이다. 새 실험의 개선/회귀 점수는 아직 없다.

## 1. 무엇을 실제로 가져왔나

| 레퍼런스 | 원형의 작동 단위·목표 | 현재 실제 사용 | 의도 보존 여부와 판단 |
|---|---|---|---|
| LlamaIndex CitationQueryEngine / QueryFusionRetriever | 검색된 노드를 순위 통합하고, 토큰 예산 안에 묶어 번호가 붙은 근거로 답변 생성 | core0.14.25의 BM25+dense RRF, CitationQueryEngine, CompactAndRefine, 실제 tokenizer 사용 | 알고리즘 자체를 실행한다. `num_queries=1`로 다중 질의 생성은 끈 의도적 선택. 작성자/시간·원문 offset 연결은 유지할 가치가 있다. 검색 성공·현재 상태의 권위·인용의 의미 정확성까지 보장하는 기능은 아니다. 이번 비교는 검색 이후를 고정하므로 검색 개선 주장을 하지 않는다. |
| ConflictScore | 답변을 주장들로 분해하고 각 주장×문서를 판정한 뒤 충돌 지표 계산. 논문의 R-RAG 사례는 TruthfulQA 선택형 응답 | 저자 `evaluate_document_support` 함수는 실제 사용. **답변 전체를 한 claim으로** 넘기고, 반박 문서 하나라도 있으면 우리 재작성 프롬프트 실행. CS-C/CS-R는 운영 경로에서 미사용 | 원형 전체가 아니다. 특히 partial support 판단과 전체 답변 입력을 결합하면 일부 맞는 내용이 별도 오류를 가릴 수 있다. 주장 단위 복원 후보를 비교하되, 분해 과정의 조건/귀속 손실도 함께 본다. |
| Adaptive QA(AQA) | 상충·모호한 근거에서 복수 답과 각각의 출처를 함께 생성·평가. prompting/document-split/fine-tuning은 별도 baseline 선택지 | Figure1을 바꾼 한 예시와 출처별 답 생성 프롬프트. **미인용 반박 source ID가 있을 때만 호출**, 인용 ID 집합이 늘면 교체 | 가장 큰 변형은 예시 개수보다 **호출 조건과 성공 단위**다. 문서를 인용했어도 그 안의 답 하나를 빠뜨릴 수 있다. 출처 ID 커버리지는 답–출처 쌍 보존을 뜻하지 않는다. 같은 AQA 프롬프트를 첫 생성에 두는 조건으로 위치 효과만 비교한다. |
| LangChain citation fuzzy match | `QuestionAnswer → FactWithEvidence[]`로 답의 사실과 해당 구절을 함께 생성. 각 사실의 source 집합을 분리하도록 스키마에 명시 | 스키마와 프롬프트를 재사용하되 **이미 쓴 답의 미인용 문장만** 처리. 공백 차이만 허용하는 정확한 구절 매칭, 답 문구 불변 | 엄격한 원문 일치와 답 보존은 의도적 장점. 그러나 이미 잘못 인용한 문장은 재검사하지 않으며, 복합 문장이 여러 주장이어도 그대로 유지한다. `format_response`의 최종 answers는 답 전체+인용 집합이라 원형의 사실별 결합을 제공하지 않는다. 의미 검증기로 설명하면 안 된다. |
| ALCE | 답 정확성과 인용 품질을 분리해 평가; 사후 인용 검색은 후보를 찾는 방법이고 entailment 평가는 별도 | 과거 TF-IDF/NLI 시도와 vendored 코드가 남아 있지만 **현재 기본 인용 경로는 LangChain 구절 어댑터** | ALCE의 의미 검증을 현재 시스템이 수행한다고 해석하면 안 된다. 출처 번호/offset 존재를 citation correctness로 채점하지 않는다. 이번 평가에서도 구절 존재와 문장 지지를 분리한다. |
| LangChain HITL | 허용된 결정을 실제 tool-call 실행 직전에 적용. 거절이면 실행 대신 메시지를 반환 | 투표 reducer, 정정 적용과 재검토 허가의 분리라는 설계 의도 참고. middleware 자체 미실행 | 저장 상태 계산에는 의도가 반영돼 있다. **QA는 그 상태를 프롬프트로 읽고 자유롭게 문장을 생성**하므로, tool 실행 차단과 같은 보장이 아니다. 재검토 승인을 사실 변경으로 말하지 않는다는 보장은 아직 없다. |
| Graphiti | fact별 episode 출처와 `valid_at/invalid_at/reference_time` 등 시간 의미를 구분한 구조 | 원문 ID·작성자·기록 시간·구절 및 별도 상태 snapshot을 보존하는 의도 참고. Graphiti DB/검색기 미실행 | `observed_at` 하나가 사실 유효 기간을 대신하지 않는다. 출처 메타데이터 보존만으로 Graphiti의 시간 처리 효과를 얻었다고 볼 수 없다. 이번 판정은 기록의 조건·승인 상태 보존에 한정한다. |
| Mem0 | 이번 고정 소스에서는 문맥·과거 기억 검색→추출→embedding/중복 제거→실제 저장 확인→이력·연결의 단계. 명시적 update API도 존재 | 원문 저장과 비교 실패를 분리하고, 실패를 정상 빈 결과처럼 취급하지 않는 의도 참고. Mem0 런타임 미실행 | 현재 revision의 `_add_to_vector_store`는 additive 단계다. 모든 Mem0 버전을 단순 ADD/UPDATE/DELETE 판정기로 설명하면 부정확하다. 우리 비교 오류가 답변 생성 이후에 반환되는 경로는 “오류 보고”는 해도 “생성 시 불확실성 전달”은 못 한다. |

CUPMem과 SpeakerMem-R1은 과거 별도 baseline/실험 구현이다. 현재
`TeamMemoryService`는 `timeline-direct`와 `AttributedQA`를 연결한다. 두 연구의
전체 memory writer/학습 효과가 현재 서비스에 포함돼 있다고 계산하지 않는다.

## 2. 실제로 끊긴 지점

### 주장 단위가 단계마다 바뀐다

현재 경로는 대체로 다음처럼 연결된다.

`답변 전체 → 문서별 판정 → 인용 source ID 집합 → 미인용 문장 → 최종 답 전체+근거 집합`

ConflictScore의 주장별 판정, AQA의 답–출처 쌍, LangChain의 사실–인용 구절은
같은 단위가 아니다. 원형의 이름을 연결했지만 그 사이에서 필요한 구분을 잃는다.
이것은 새 검사기를 하나 더 넣기 전에 검증해야 하는 연결 문제다.

예컨대 같은 문서가 “A는23ms, B는31ms”를 담고 있을 때 답이 A만 설명해도 그 문서는
이미 인용됐다. 현 `missing_opposing_sources()`는 그 문서를 누락으로 보지 않는다.
이 반례를 로컬 계약 테스트로 재현했다. 실제 모델이 해당 문장을 틀렸다는 점수와는
구분하는 구조적 반례다.

### 검사기와 생성기가 같은 오해를 반복한다

기존 oracle-v1의 실제8B 요청을 다시 대조했다. 8개 최초 생성 입력 모두에
올바른 reconsideration 효과가 들어 있었고, 기록된 draft와 judge 응답이
실제 HTTP 원출력에 존재함을 확인했다.

| 기존 기록 분석 | 관측 상태37 QA | 올바른 재검토 입력8 QA |
|---|---:|---:|
| 문서 judge 호출 | 139 | 24 |
| 반박 판정이 나온 질문 | 7 | 0 |
| 재작성 실행 | 7 | 0 |
| 인용 삽입 전 답 문구가 바뀐 질문 | 6 | 0 |
| AQA 호출 / 채택 | 4 / 2 | 0 / 0 |
| 기존 의미 채점에서 실패한 질문 | 2 | 6 |

이는 새 점수가 아니라 [기존 원출력 재분석](../results/reference-audit/v1/historical-stage-analysis.json)이다.
8개는 writer/cache 두 이야기에서 파생된 질문들이므로 독립8사례라고 확대하지 않는다.

구체적으로 `writer-reopen/pending-reason`은 버전4의 단일 writer 제한과 버전5의
병렬 writer 보고를 올바르게 설명하다가, 마지막에 새 보고를 **정정 제안**이라고
잘못 부른다. 세 문서 judge는 모두 SUPPORTS를 냈다. 상태 snapshot은 재검토를
명시하고 사실 대체를 부정하는데, judge의 이유에는 그 snapshot이 정정 제안을
확인한다는 잘못된 해석이 들어 있다.

따라서 두 문제가 함께 있다. 전체 답변 판정이 부분 오류를 가리는 문제, 그리고
모델 자체의 관계 해석 오류다. 주장 분해만 복원하면 해결된다는 결론은 아직 못 낸다.

### 유용한 단계도 확인된다

기존 zip 질문의 초안과 ConflictScore 이후 재작성은 ValueError만 남겼다.
AQA가 실행된 뒤에는 기록에 있는 LengthMismatchError와 ValueError를 출처별로
함께 남겼다. walrus 질문에서는 재작성 단계가 `:=`와 `<-` 두 기록을 함께 남겼다.
여기서 정답은 현실의 Python 문법 하나를 고르는 것이 아니라 주어진 상충 기록의
답을 출처와 함께 보존하는 평가 계약이다.

기존20문항의 저장된 채점은 답20/20, 요구 근거20/20이다. 이를 모든 문장 인용의
완전성이나 새 데이터 일반화 성능으로 해석하지 않는다. 추가 단계를 모두 제거하는
결정도 이 기록과 충돌하므로, 같은 입력의 단순 방식과 다시 비교한다.

## 3. 원형대로 되돌리면 자동으로 좋아지는가

그렇지 않다. ConflictScore 논문은 조건과 귀속을 어떻게 분해하느냐에 민감하다고
명시한다. 부분 지지는 균형 잡힌 답을 불필요하게 벌주지 않으려는 의도다. 이를
무조건 완전 함의로 바꾸면 다른 방법이 된다. 이번에는 judge의 부분 지지 정의를
유지하고 분해 단위만 바꾼다. source attribution을 잃은 claim은 별도 오류로 센다.

AQA의 prompting, document-split, fine-tuning을 전부 붙여야 한다는 뜻도 아니다.
서로 다른 baseline이다. 저자 few-shot 스크립트에는 고정 학습 예시 선택, 입력
절단, 모델별 문맥 한도, beam search가 있으며, 우리 실행과 다르다. 이번 AQA-first는
기존 한 예시와 Qwen을 그대로 두어 **위치만 비교**한다. 원 논문 수치 재현이라고
부르지 않는다. 공식 평가 코드도 정답/출처 답 문자열 포함을 계산하므로, 상태 위반과
잘못된 귀속을 다루는 우리 평가를 그 문자열 기준으로 대체하면 안 된다.

## 4. 지금 유지할 것과 아직 선택하지 않은 것

**유지:** 불변 원문·정확한 위치, 작성자/시간 전달, 승인 이벤트의 결정적 축약,
정정과 재검토의 다른 효과, 원문 근거와 상태 근거의 구분. 정확한 구절 매칭도
유지하되 의미 검증이라는 이름을 붙이지 않는다. 기존 검색은 이번 진단에서 고정한다.

**수정 우선순위:** 전체답 판정과 source-ID 기반 AQA 호출이 원형 목적을 약화시키는지
먼저 비교한다. 최종 답의 주장별 근거 관계와 상태 사용 권한은 현재 인터페이스가
보장하지 않는다고 명시한다. 인용된 문장의 오인용과 비교 실패 문맥의 누락을 별도
실패 종류로 남긴다. 이를 이유로 새 DB/검사 모델을 지금 추가하지 않는다.

**보류:** claim 단위 복원 또는 AQA-first를 운영 기본값으로 교체하는 결정.
새 비교가 끝나기 전에는 개선 수치를 만들거나 기본 reader를 바꾸지 않는다.

## 5. 동일 조건 비교와 실행 상태

기존37 QA와 올바른 재검토 입력8 QA를 모두 포함한45문항, 네 조건180출력을
사전에 고정했다. Qwen3-8B revision·온도·출력 예산·원문·작성자·날짜·상태·근거 순서가
같고, direct/current/claim 조건은 같은 초안을 공유한다.

1. direct: 공유 초안+기존 인용.
2. current: 현 문서 judge→재작성→조건부 AQA+기존 인용.
3. AQA-first: 같은 AQA 프롬프트로 처음부터 출처별 답 생성+기존 인용.
4. claim-review: 저자 분해 프롬프트→주장×문서 판정, 나머지 연결은 current와 같음.

코드·입력·채점 키를 출력 전에 보존했다. gold와 과거 답은 모델 입력에서 제외했다.
기존 모델 준비를 재사용하고 새 모델/데이터를 내려받지 않는다. 로컬 계약 테스트16개와
소스 packet의79개 파일 해시 검사를 통과했다. 이는 GPU 추론 성공을 뜻하지 않는다.

Slurm **122740**, GPU1·CPU8·48G·12h. client는3h/2000호출 상한으로 별도 제한한다.
기존 g8의 NLTK 런타임을 재사용하기 위해 g8을 선택하며, checkpoint는 공유 프로젝트
경로에서 직접 읽는다. 자원이 없으면 다른 노드로 복제하지 않는다.
현재 `PENDING(QOSMaxGRESPerUser)`: 다른 프로젝트121613이 계정 한도4GPU를 사용한다.
그 작업을 취소·변경하지 않았으며122740을 중복 제출하지 않는다.

완료 후 입력 해시·모든 호출·Slurm 결과를 확인하고 blind card별 원문 채점을 해야
최종 유지/수정을 결정할 수 있다. 기존 답·근거 성공을 잃거나 새로운 승인 권한
위반이 생긴 후보는 채택하지 않는다. 성능 개선 없이 호출만 늘어도 채택하지 않는다.
세부 중단·채택 기준은 [고정 프로토콜](../evaluation/reference_audit/PROTOCOL.md),
재개 절차는 [실행 기록](../results/reference-audit/v1/README.md)에 있다.

## 6. 확인한 원본

- [ConflictScore 논문 §3/§6/limitations/Table10](https://arxiv.org/html/2606.26437v1),
  [공식 judge a8868e5](https://github.com/microsoft/ConflictScore/blob/a8868e5cd98bff81935a1766b54a02ad3eab9e8f/src/eval_with_conflict_score/eval_all_calibration.py).
  vendored 파일과 비교했으며 차이는 예외 로깅과 끝 줄바꿈이다. 공개 README의 실행
  단계와 논문의 전체 response-decomposition/R-RAG 절차는 구분했다.
- [AQA 논문](https://aclanthology.org/2024.emnlp-main.956/),
  [few_shot.py f72bdb3](https://github.com/Shaier/Adaptive_QA/blob/f72bdb3e5d1f4bf83a3dd84596039b67ddd145e8/experiments/few_shot.py),
  [평가 코드](https://github.com/Shaier/Adaptive_QA/blob/f72bdb3e5d1f4bf83a3dd84596039b67ddd145e8/evaluation_method.py).
- LlamaIndex 설치본 core0.14.25의 `citation_query_engine.py`, `fusion_retriever.py`,
  `compact_and_refine.py`. 공식 구현을 재사용하며 현재 연결은
  [reference_qa.py](../team_memory/reference_qa.py)에 있다.
- [LangChain0.3.27 원형 보존본](../team_memory/_vendor/langchain_citation/citation_fuzzy_match_original.py),
  [현재 어댑터](../team_memory/reference_quotes.py),
  [ALCE 사후 인용 원형](https://github.com/princeton-nlp/ALCE/blob/246c476a4edfc564266b7346b6e29ef4861ae937/post_hoc_cite.py).
- [HITL d9caf08](https://github.com/langchain-ai/langchain/blob/d9caf083577c43a91c5bf6bd1f7dfc289581184d/libs/langchain_v1/langchain/agents/middleware/human_in_the_loop.py),
  [Graphiti edges747b480](https://github.com/getzep/graphiti/blob/747b480ec6b12ecb718f1e2bc588b20ee36ea9c2/graphiti_core/edges.py),
  [Mem0 f1791da](https://github.com/mem0ai/mem0/blob/f1791daa86d469249c9b002f62644d58a1eb96a0/mem0/memory/main.py).

고정 원본의 URL/파일 SHA256은 결과 폴더의 `reference-source-manifest.json`에 남긴다.
