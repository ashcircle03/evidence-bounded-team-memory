# 질문 독립 저장·벡터화 경로 감사

> 아래 감사는 변경 전 `cabaf1f` 기준이다. 이후 구현·결과는 [준비된 색인 v1](v1/README.md)과 [초기 준비 비용 수정 v2b](v2b/README.md), 사용법은 [색인 수명주기 계약](../../docs/modules/index-lifecycle.md)을 따른다. 과거 실측 파일은 보존했다.

2026-11-15. 원문/records가 질문 때 처음 저장되는 것은 아니다. 현재 문제는
**질문 경로가 문서 색인 생성·전체 재임베딩을 수행하며, 기존 v2 ask가 관계 sync도 한다**는 점이다.
서비스 저장 구조 변경은 아직 적용하지 않았다. 아래는 현재 구현의 재현과 구현할 경계다.

[evaluation/service_storage/audit.py](../../evaluation/service_storage/audit.py)는 실제
ReferenceQA에 Counting MockEmbedding을 넣고 문서/질문 임베딩 호출을 구분했다.
모델 품질·실제 시간 측정이 아닌 수명주기 검사이며 외부 API/LLM 호출0회다.

| 동작 | 새 문서 임베딩 | 질문 임베딩 | 원문 수 |
|---|---:|---:|---:|
| 원문2개 import |0|0|2|
| 첫 질문 |2|1|2|
| 같은 DB의 두 번째 질문 |0|1|2|
| 프로세스 재시작 뒤 질문 |0|1|2|
| 원문1개 추가 |0|0|3|
| 추가 후 첫 질문 |3|1|3|

[실측 JSON](audit.json). 새 원문1개 때문에 기존2개도 재임베딩한다. 따라서 “매 질문마다
모든 문서를 재임베딩한다”는 표현은 정확하지 않지만, 질문에 무거운 갱신이 얹히는 것은 맞다.

- `readers/retrieval.py: import_history`는 원문을 먼저 영속 저장한다.
- `_index`는 전체 source-ID 집합과 설정의 해시로 색인을 선택한다. 저장된 세대가 있으면
  로드하고, 없으면 모든 원문을 chunk/embedding한 뒤 LlamaIndex StorageContext를 persist한다.
- `ask`에서 `_index`를 호출한다. team profile의 BM25도 질의마다 구성한다.
- 기존 `TeamMemoryService.ask`는 `sync()`를 먼저 호출해 미처리 원문의 관계 제안을 만들 수 있다.
  다섯 포트의 `GatewayAdapter.ask`는 이 sync를 호출하지 않지만 retrieval의 lazy indexing은 남아 있다.

## 서비스용 저장 선택

| 정보 | 권위 있는 저장 | 검색/조회에서의 역할 |
|---|---|---|
| 원문·작성자·시각·위치·내용 해시 | 기존 불변 JSON, 원문 평문 유지 | 정확한 인용·재처리·Git 공유의 기준 |
| 주장·조건·근거·이유 종류·추출 버전 | 원문 span ID가 연결된 구조화 JSON | 미검증 해석 보존. 원문/승인 사실과 구분 |
| 제안·승인·거절 이벤트 | 인증된 불변 이벤트와 기존 reducer | 상태/대상 필드/허용 범위를 결정론적으로 조회 |
| 문서 chunk 벡터 | 체크아웃별 영속 파생 색인 | 의미가 비슷한 후보 ID 검색만 담당 |
| 키워드 색인·상태 조회표 | 재생성 가능한 로컬 projection | 정확한 용어와 구조 필터; 필요시 SQLite로 조회 구현 |

지금의 각자 pull/push 구조에서는 JSON 원장을 유지한다. SQLite 파일이나 벡터 DB 파일을
Git에서 병합할 이유가 없다. 평문과 벡터 중 하나만 고르는 문제가 아니다. 원문/이벤트는
보존하고 벡터는 그 위에 재구축 가능한 검색 표현으로 둔다. 승인 상태·현재값·필드 변경 범위는
벡터 유사도로 결정하지 않는다. JSON의 그래프 edge를 저장한다고 별도 graph DB가 필요한 것도 아니다.

현재 단계의 검색 backend는 **기존 LlamaIndex 영속 색인을 재사용**한다. 전용 벡터 DB 서버
도입은 현재 확인된 문제의 필수 해법이 아니다. 다중 서버/worker, 서버측 필터, ANN 검색량이
요구될 때 그 포트의 backend를 교체한다. 현재 SimpleVectorStore의 메모리·검색 규모 한계를
서비스 전체가 해결한 것으로 주장하지 않는다. SQLite 조회 projection 역시 아직 구현 전이다.

## 고쳐야 할 수명주기

1. import/ingest/Git pull에서 원문을 먼저 저장한다. 질문은 받지 않는다.
2. 기록 추출과 관계 후보 처리는 독립 작업으로 실행한다. 실패해도 원문과 실패 상태는 남긴다.
3. 변경 source/chunk만 임베딩하고 키워드 색인을 갱신한다. 모델·revision·전처리·분할 설정과
   source hash를 포함한 manifest를 저장한다. 승인 이벤트만 바뀐 경우 원문 재임베딩은0회다.
4. 완성된 색인 세대를 원자적으로 ready로 게시한다. 미완성 색인을 완료로 재사용하지 않는다.
5. ask는 snapshot/색인 준비 상태를 읽고 **질문만 임베딩**한다. 검색 후보의 원문·조건·상태를
   원장에서 다시 조회한다. ask가 문서 추출·관계 sync·전체 색인 생성을 몰래 수행하지 않는다.
6. 색인이 뒤처졌다면 명시적인 not-ready/부분 범위와 indexed source 집합을 반환한다.
   기본적으로 준비된 것처럼 전체 DB 답변을 하지 않는다. 실패/재시작 후 ingest 작업을 재개한다.

기존 [LlamaIndex IngestionPipeline](https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline/)
은 변환 cache와 docstore 기반 문서 관리를 제공한다. 새 색인 관리기를 만들기 전에 이 구현을
고정 버전에서 대조해 재사용한다. [StorageContext persist/load](https://developers.llamaindex.ai/python/framework/module_guides/storing/save_load/)
도 이미 사용하는 경로다. cache가 있다고 원자적 게시·snapshot 일치·권한이 자동 보장되는 것은
아니므로 서비스 경계에서 별도 검증해야 한다.

## 다음 구현의 통과 조건

- 질문0회 상태에서 원문·records·검색 색인이 준비됨.
- 준비된 DB의 첫/반복/재시작 후 ask: 문서 임베딩0회, 기록 추출0회, 관계 sync0회.
- 원문1개 추가: 기존 원문의 재임베딩0회. 동일 ingest 재실행도0회.
- 승인/거절만 변경: 벡터 재생성0회, 조회 상태는 새 snapshot과 일치.
- 인덱싱 실패·중단: 원문/승인 이벤트 불변, 부분 색인을 ready로 표시하지 않음.
- 질의 순서를 바꿔도 저장된 주장·관계·상태 해시 불변; 질의 로그는 별도.
- 기존 검색 근거와 QA를 고정해 변경 전후 비교. 예열된 벤치뿐 아니라 cold start,
  추가/중복 입력/재시작/실패복구를 평가한다.

이번 추출 입력 비교의 결과와 이 저장 수명주기는 별개다. 잘못 추출된 이유를 벡터 DB에
영속 저장한다고 의미 품질이 해결되지 않으며, 추출 점수가 좋아도 lazy 전체 인덱싱 문제가
해결되는 것은 아니다. [추출 계약 비교](../record-contract/README.md).
