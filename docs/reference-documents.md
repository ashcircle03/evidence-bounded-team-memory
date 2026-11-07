# Original-record QA 수정 계획과 구현

2026-11-07. 기준 결과는 demonstrated-v1이며 이전 점수·코드는 수정하지 않는다.
이번 범위는 입력 기록에서 QA를 반환하는 경로다. 승인 상태 변경이나 재검토/병합
판정을 해결했다고 주장하지 않는다. 기본 selected attributed는 채택 기준 전까지 유지한다.

## 연결 의도

| 변경 | 가져온 구현/의도 | 이 프로젝트의 변형 |
|---|---|---|
| 선택기 optional 검색 제거 | LongMemEval flat retrieval: 질문이 실제 검색을 실행 | 동일512/64 원문 chunk와 top8에서 BM25/Contriever 비교 |
| 검색 key와 답의 원문 분리 | LongMemEval key/value identity | 생성한 fact나 summary 대신 원문 witness/offset 그대로 반환 |
| 메타데이터·시간 보존 | LongMemEval chronological history reader | 복수 작성자·대화방 location·원 기록 시간 유지; user-only 필터 미사용 |
| 문장별 문단 ID | ALCE 기본 doc prompt와 최소 충분 인용 | JSON 문장+document_ids, 원문을 클라이언트가 연결; quote 생성 필수조건 제거 |
| 한 번의 독해 | LongMemEval direct / 기본 con | direct와 단일 호출 con 비교; con-separate나 온라인 judge 미추가 |
| 상태/실패 분리 | 기존 source identity 계약 | malformed JSON=error, 인용 오류=partial, 실제 빈 답=insufficient; 원출력 보존 |

사용한 공개 버전과 원본은 team_memory/_vendor/longmemeval/NOTICE.md,
team_memory/_vendor/alce/asqa_default.original.json에 고정했다. 공개 코드를 쓴
대체 모델/데이터 어댑터이며 논문 성능 재현이라고 부르지 않는다.
Contriever의 pooling/dot product/ranking을 유지하되 batch16·embedding cache를 사용한다.
문단 ID는 검색 순위로 먼저 부여하고 시간순 표시 후에도 같은 witness를 참조한다.
원 location은 그대로 보존한다. 이를 임의 프로젝트 이름으로 해석하지 않는다.

## 실행 순서

1. source binding, 정렬, 잘못된 ID, 빈 검색, 상충 답 분리 계약 테스트.
2. 고정된 legacy20/Ever10 입력·정답·실행 코드를 해시로 동결.
3. GPU1·12시간·conda 계산 노드에서 Contriever 다운로드/색인 후 같은 Qwen3-8B 실행.
4. 기존 BM25 top8의 정확한 일치를 확인. 같은 corpus chunk를 dense에도 사용.
5. legacy20에서 direct/con 각각; Ever10에서 BM25/dense × direct/con: 총80호출.
6. COMPLETED/0:0와 프로그램/해시를 확인하고 모든 실제 요청과 결과를 재생.
7. 고정 정답 및 원문으로 답·인용·필요 근거·불필요 인용을 각각 채점하고 채택 결정.

같은 노출 개발 문항에 대한 수정 비교다. 새 일반화 성능이나 전체 벤치마크 완주로
표현하지 않는다. 기존 related-record R은 최소 충분 근거의 정답 라벨이 아니다.
oracle용 수작업 근거를 actor 입력에 새로 넣지 않으며, 필요한 근거가 있었는지는
결과 평가에서 원문으로 구분한다. 원인 분리를 위해 새 query expansion, fact
생성, reranker, temporal filter는 이 버전에 추가하지 않는다.

## 사용

`answer_from_sources(question, witnesses, llm, reading='direct')`는 원문을 한 번 읽는다.
`DocumentQA(retriever, llm).ask(question)`는 실제 검색을 한 번 호출한 뒤 읽는다.
retriever.retrieve는 source_id, quote, start, end, location, speaker, observed_at을
가진 원문 witness 목록을 반환해야 한다. Contriever.index(witnesses) / retrieve가
이 인터페이스를 제공한다. 서버 모델은 loopback에만 연결한다.

```sh
python -m team_memory.reference_documents --input input.json \
  --model-path /path/to/Qwen3-8B --embedding-path /path/to/existing/embed \
  --api-base http://127.0.0.1:8000/v1 --reading direct
```

실행은 GPU가 할당된 계산 노드의 conda 환경에서 한다. 기존 local_components를
재사용하므로 embedding-path가 필요하지만, source-only 호출에서는 추가 검색을 하지 않는다.
반환 evidence는 원문 문단이다. 유효 ID는 문장의 의미를 보증하지 않으며 semantic
support는 별도 평가 대상이다. 답과 근거가 틀렸는데 status=ok일 수 있다는 점은
구조 검증과 의미 평가의 구분이다.
