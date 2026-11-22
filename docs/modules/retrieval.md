# retrieval — 질문에 맞는 근거와 상태 전달

[공통 계약](README.md) · 구현 소유: `readers/retrieval.py`, `readers/context.py`의 검색·문맥 구성 부분 · [실제 adapter](../../team_memory/adapters/retrieval.py)

입력 `evidence.retrieve`: snapshot, query(text,time_scope,as_of,conditions), max_evidence. 출력 bundle: 같은 snapshot·query, evidence, coverage, unresolved_proposal_ids. query는 원 요청을 보존하며 내부 query rewriting은 진단 로그에 별도 기록한다.

evidence는 id, kind, exact span, 조건과 provenance를 가진다. source evidence는 원문 source_id·owner·speaker·observed_at·location을 그대로 전달한다. review_state evidence는 proposal_id·snapshot_id·정해진 상태 렌더링을 참조하며 source 메타데이터를 갖지 않는다. 상태 evidence를 추가하느라 현재값의 원문을 잃지 않는다.

조회 권한은 `evidence:read`다. 질문 경로는 준비된 인덱스를 로드하며 문서 변환·임베딩·BM25 재구축을 하지 않는다. 별도 `evidence.prepare(snapshot)`는 `records:write`로 실행하고 authoritative source·proposal·review state는 변경하지 않는다. [준비·실패·Git 동기화 계약](index-lifecycle.md). 인덱스 revision과 snapshot 불일치를 처리할 수 없으면 INDEX_STALE이다. 내부 query 해석 실패는 QUERY_UNRESOLVED, 시점 미지원은 TIME_SCOPE_UNAVAILABLE이다. 질문을 임의로 현재 시점으로 바꾸지 않는다.

coverage는 hits / no_hits / incomplete다. 필요한 근거가 budget 밖에 남는 것을 알고 있으면 incomplete + partial로 반환한다. 상충 양쪽을 함께 전달하지 못한 경우 한쪽만으로 정상 답변을 유도하지 않는다. 다만 unresolved_proposal_ids에는 질문과 관련 있는 관계만 올린다. 모든 상충을 모든 질문의 차단 조건으로 삼지 않는다.

DB에 정답 근거가 있는지의 gold label은 검색기 입력에 넣지 않는다. 검색 실패(error), 검색 결과 없음(ok/no_hits), 일부 조회(partial/incomplete), 충분한 근거인데 생성 실패를 별도 집계한다.

## 검색 단계

검색은 [`readers/retrieval_stages.py`](../../team_memory/readers/retrieval_stages.py)의 다섯 단계로 나뉜다. 단계를 나눠도 기존 출력은 바뀌지 않는다.

| 단계 | 하는 일 | 구현 |
|---|---|---|
| ① 후보 | 채널별 순위 목록(dense, sparse). 각 후보의 순위·점수·source_id·원문 구간을 융합 전에 기록 | `CandidateSource`, 기본값 `LlamaIndexCandidates`(준비된 색인 + 준비된 BM25) |
| ② 융합 | 상류 `QueryFusionRetriever` reciprocal_rerank를 그대로 사용 | `StagedRetriever` |
| ③ 제안 따라가기 | 검색된 원문에 걸린 제안의 양쪽 구간 추가 | `expand_review_context` 재사용 |
| ④ 상태 근거 | 제안마다 review_state 근거 1개를 목록 뒤에 추가 | `review_sources` 재사용 |
| ⑤ 인용 | 인용 노드를 만들고 원문 위치 복원. 검색 전용 요청은 생성 부품 없이 `CitationQueryEngine`과 같은 분할을 쓴다. 예산 처리는 adapter | `citation_nodes`, `_witness` |

근거가 `max_evidence`를 넘으면 adapter가 고른다. 순서는 review_state 근거, 남긴 상태 근거가 가리키는 제안의 양쪽 원문(answering이 확인하는 `previous`·`incoming` 구간과 겹치는 근거), 나머지 검색 순위 순이다. 한 제안의 양쪽이 다 들어가지 않으면 그 제안의 원문은 넣지 않아 한쪽만 남지 않게 한다. 남긴 근거는 원래 순서와 ID를 유지하고 `incomplete` + `BUDGET_EXCEEDED`로 반환한다. gateway는 incomplete 묶음으로 답을 만들지 않는다. 예산 안이면 출력은 바뀌지 않는다.

요청마다 진단 기록을 `cache_root/traces/<입력 해시>.json`에 남긴다. 계약 응답에는 넣지 않는다. 같은 snapshot·질문·예산이면 같은 파일을 덮어쓴다. 기록 내용은 후보 소스 이름·버전, 채널별 후보(순위·점수·source_id·구간), 융합 결과(RRF 점수), 따라간 제안과 추가 구간, 상태 근거, 예산 때문에 뺀 근거와 이유, 최종 근거 ID, 결과 코드다. 단계별 소요 시간은 `timings_ms`에 따로 두므로 이를 빼면 같은 입력에 같은 기록이 나온다. 실패하면 실패 단계와 예외 종류만 남기고 메시지는 남기지 않는다. 기록을 쓰지 못하면 요청은 `IO_FAILURE`로 실패한다.

오류 코드: snapshot 불일치 `EVIDENCE_INVALID`, 예산 초과 `BUDGET_EXCEEDED`(partial), 준비되지 않았거나 맞지 않는 색인 `INDEX_STALE`, 그 밖의 검색·인용·구간 실패 `RETRIEVAL_FAILED`. 실패를 `no_hits`로 바꾸지 않는다.

"DB에 없음" 판단 장치: retrieval adapter의 `min_dense_score`, `min_sparse_score`(기본 `None` = 꺼짐). 하나라도 주면 ①의 후보를 점수로 거른다. 기준을 준 채널에서 점수가 그 기준 이상인 후보만 남고, 기준이 없는 채널은 후보를 통과시킬 수 없다. 남은 후보는 모든 채널의 순위를 그대로 융합에 쓴다. 아무것도 남지 않으면 `coverage='no_hits'`, 근거는 빈 목록이다. 뺀 후보와 점수는 진단 기록의 `thresholds`에 남는다. 기준값은 records의 벡터 단위와 임베딩 모델이 정해진 뒤 개발용 데이터로 정하며, 꺼져 있으면 출력은 바뀌지 않는다.

records 구조를 쓰는 두 설정(둘 다 기본 꺼짐, 검색 품질은 아직 측정하지 않음):

- **색인 단위** `index_unit='records'`(reader factory 설정): `record_graph`가 있는 원문을 주장 묶음 단위로 색인한다. 주장마다 그 주장·조건·이유·시간·대상 문장을 덮는 원문 구간 하나, 그리고 어느 주장에도 쓰이지 않은 문장 하나씩이다. 묶음이 `chunk_size` 토큰을 넘으면 문장별로 색인한다. `record_graph`가 없는 원문은 512토큰 조각을 그대로 쓴다. 이때 `record_graph`도 색인 명세에 들어가므로 그래프가 바뀌면 다시 준비해야 한다. 기본값 `chunks`는 기존 색인 키와 출력을 바꾸지 않는다.
- **조건 필터** `condition_filter=True`(retrieval adapter 설정): 질문에 `conditions`가 있으면 ① 후보를 records의 조건 구절과 비교한다. records에 조건이 적혀 있는데 요청 조건을 하나도 포함하지 않는 후보만 뺀다. 조건이 안 적힌 후보는 남긴다. 비교는 대소문자·공백만 무시하는 글자 포함이라 "v1"과 "version 1"은 다르게 본다. 뺀 후보는 진단 기록의 `condition_filter`에 남는다. 질문 문장 뒤에 조건을 붙이는 기존 동작은 그대로다.

①만 교체 대상이다. reader에 `candidate_source(index)`를 주면 기본 후보 대신 그 결과를 쓴다. 채널이 하나면 융합하지 않는다.

공통 검사: 원문·날짜·작성자·상태 전달, snapshot 불변, max_evidence, no_hits와 실패 구분. 담당자 추가 검사: Recall@k, 조건/시간/상태 포함률, 인덱스 갱신 경쟁, 질문에 무관한 상충 제거, prompt 렌더링 시 전체 snapshot이 아닌 evidence만 사용. `retrieve_only` 경계로 생성 호출 없이 실제 검색 결과를 반환한다. [연결 검사](../../tests/test_reference_module_adapters.py).
