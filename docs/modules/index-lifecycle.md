# 기록 입력에서 준비하고 질문에서는 읽는 색인

구현: [`readers/indexing.py`](../../team_memory/readers/indexing.py). 검증: [비용 분해·검색·QA 보존](../../results/service-storage/v2b/README.md), [이전 수명주기 검사](../../results/service-storage/v1/README.md).

원문과 구조화 기록은 기존 불변 JSON 원장에 먼저 저장한다. 벡터는 검색 후보를 찾는 파생 데이터다. 승인 상태·현재값을 벡터에 맡기지 않으며, 원문이 없는 벡터만으로 답을 구성하지 않는다. 이 변경은 추출·답변 모델의 의미 판단을 개선했다고 주장하지 않는다.

## 저장·검색의 책임

| 경로 | 수행하는 일 | 수행하지 않는 일 |
|---|---|---|
| `record.append` | 원문과 선택적 record graph를 저장 | 검색 색인 자동 생성, 관계 승인 |
| `evidence.prepare(snapshot)` | 변경 문서 분할·임베딩, 검색 색인 게시 | 질문 입력, LLM 답변, 원문·상태 변경 |
| `gateway.ingest` | records commit → prepare → 관계 비교·후보 저장 | 미승인 후보를 현재 사실로 승격 |
| v2 `import_history` / `ingest` / `sync` | 기존 기록 처리 후 해당 원문 색인 준비 | 질문이 올 때까지 준비를 미루는 동작 |
| `evidence.retrieve` / `ask` | 일치하는 색인 로드, 질문 임베딩, 검색·현재 검토 상태 연결 | 문서 임베딩·분할, BM25 재구축, 관계 sync |

`evidence.prepare`는 `records:write`, `evidence.retrieve`는 `evidence:read`가 필요하다. 준비 응답은 `snapshot_id`, `index_key`, `source_count`, `prepared_documents`, `reused_documents`다. 앞의 두 문서 수를 더하면 snapshot 원문 수다. 이는 문서 수이며 긴 문서의 chunk 임베딩 호출 수와는 다르다.

초기 적재에서 `record.append`를 직접 호출하는 팀원은 적재를 마친 snapshot으로 `evidence.prepare`를 한 번 호출한다. `gateway.ingest`를 사용하는 경우 이미 연결돼 있다. 기존 v2 저장소는 업그레이드 후 첫 질문 전에 `sync`를 호출한다. 과거 lazy 색인의 node ID·manifest와 새 문서 캐시 형식이 다르므로 최초 전환은 전체 문서를 한 번 준비한다. 과거 색인을 삭제하지 않으며, 이후 변경 없는 원문은 재임베딩하지 않는다. 준비되지 않은 원문/설정 조합에는 `INDEX_STALE`을 반환하며 질문으로 준비를 대신하지 않는다.

```python
ready = gateway.retrieval.handle(
    request('evidence.prepare', {'snapshot': snapshot},
            workspace_id='my-team', request_id='prepare-1'),
    context=writer_context,
)
assert ready['status'] == 'ok'
```

## 재사용한 구현과 추가한 경계

고정 버전 `llama-index-core==0.14.25`, `llama-index-retrievers-bm25==0.8.0`의 구현을 대조했다.

- [IngestionPipeline / IngestionCache](https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline/): 기존 SentenceSplitter 결과와 임베딩 변환을 사용하고, 문서별 키의 완성 node를 하나의 IngestionCache에 담아 원자적으로 영속 저장한다. 변경 문서들의 구절은 함께 임베딩 변환에 전달해 upstream 배치 처리를 활용한다. node에는 원문 ID·위치·작성자·시각과 벡터가 함께 남는다. 외부 문서 캐시가 분할과 임베딩을 함께 재사용하므로 중복된 내부 변환 캐시는 끈다.
- [StorageContext persist/load](https://developers.llamaindex.ai/python/framework/module_guides/storing/save_load/): 벡터가 채워진 node로 VectorStoreIndex를 만들면 upstream은 재임베딩하지 않는다. 전체 벡터 저장소까지 persist하고 질문에서는 load만 한다. IngestionPipeline.persist만으로 벡터 저장까지 완료된다고 가정하지 않는다.
- BM25Retriever의 `persist` / `from_persist_dir`: corpus 통계 구성은 쓰기 경로로 옮긴다. 로드할 때 top-k는 실제 문서 수 이하로 제한한다.

Pipeline의 기본 upsert는 기존 문서 삭제와 새 변환 사이의 서비스 원자성을 보장하지 않는다. 따라서 기존 원장 위에 **문서별 캐시 키의 일괄 저장 + 불변 색인 세대의 원자적 게시**를 연결했다. 별도 벡터 DB 서버·새 의미 판단 모듈은 추가하지 않았다.

문서 캐시 키는 원문 ID, 텍스트·출처 메타데이터 해시, 분할·tokenizer·embedding 설정으로 계산한다. 주장 graph나 승인 이벤트만 바뀌면 문서 임베딩을 재사용한다. 모델 경로 안에서 가중치를 덮어쓰지 말고 revision별 경로를 사용해야 한다. 현재 경로의 내용 해시를 매 질문 계산하는 구현은 아니다.

분할 node ID는 `source ID + chunk ordinal`로 고정했다. 과거 임의 UUID는 유사도 동점 정렬에 영향을 줄 수 있었다. 새 구현의 incremental/full/restart 비교는 같은 ID로 이루어지며 과거 임의 동점 순서까지 무조건 동일하다고 주장하지 않는다.

## 실패·재시작·동시성

1. 원문 저장 후 색인 준비가 실패해도 원문을 취소하거나 덮어쓰지 않는다.
2. 캐시에 commit된 문서는 유지한다. 새 문서 집합의 임베딩·캐시 저장이 끝나기 전에 실패하면 그 미완료 집합은 다시 처리할 수 있다. 이미 commit된 변경 없는 문서는 재임베딩하지 않는다. 캐시 commit 이후 색인 게시만 실패했다면 재시도에서 새 문서 벡터도 재사용한다.
3. 색인 파일과 BM25를 임시 디렉터리에 완성하고 fsync한 뒤 원자적으로 게시한다. 이전 세대는 보존한다.
4. 같은 cache root의 준비 작업은 파일 lock으로 직렬화한다. 질문은 완성 세대만 읽는다.
5. 원문이 추가됐는데 새 세대가 없으면 옛 세대로 최신 원문까지 검색했다고 답하지 않는다.
6. v2 최초 import의 처리 영수증은 색인 준비 전에 저장한다. 색인 실패 후 sync가 초기 기록을 새 보고로 소급 비교하지 않는다.

강제 종료로 생긴 `.pending-*`는 ready 세대가 아니므로 로드하지 않는다. 캐시 손상은 오류로 노출한다. 세대/캐시의 보존 기간·자동 GC·백그라운드 작업 큐는 이번 범위가 아니다.

## Git과 벡터 DB

Git에는 원문·주장/조건/근거 연결·승인 이벤트를 공유하고, 벡터/BM25 파일은 각 checkout의 private cache에 둔다. Git pull 후 v2 `sync`, 또는 authoritative module snapshot을 가져온 뒤 `evidence.prepare`를 명시적으로 실행한다. Git 기록이 원본이고 색인은 그로부터 생성하므로 서로를 양방향 병합하지 않는다. 다섯 모듈의 기존 분기 Git 병합 제한은 그대로다.

현재 운영 방향은 각자 로컬 실행과 Git을 통한 원장 공유다. 검색 캐시는 각자의 환경에 보관한다. 로컬 저장 backend를 바꿔도 이 공유·권한 경계는 유지한다.

## 남은 비용

변경 없는 문서는 다시 분할하거나 임베딩하지 않는다. 그러나 현재 SimpleVectorStore는 새 세대의 전체 벡터를 직렬화하고 BM25 corpus 통계도 다시 구성한다. 질문에서도 원장을 읽고 manifest를 비교하며, 첫 로드에는 색인을 읽는 비용이 있다. 따라서 **질문의 전체 임베딩/분할 재처리를 제거한 것**과 모든 I/O·CPU를 변경량에 비례하게 만든 것은 구분한다. 큰 기록 집합에 필요한 로컬 ANN backend·증분 키워드 색인은 별도 규모 측정으로 결정한다.

이전 v1에서 초기 준비 합계685.52초의 퇴행을 확인했다. 후속 같은229문서 비교에서 문서별 fsync가 지배적이었고, 다중 키 캐시의 일괄 저장·배치 임베딩을 채택했다. 두 반복 중앙값148.33→6.51초이며 전체20문항 근거 보존을 통과했다. 대규모·종단간 운영 성능 주장과 구분한다. [원인·수치·한계](../../results/service-storage/v2b/README.md).

### 일괄 캐시의 호환·마이그레이션

현재 구현은 `document-cache.json`에 upstream multi-key cache를 저장한다. 문서 키와 색인 manifest는 동일하므로 이미 준비된 세대는 그대로 읽는다. 기존 `documents/<key>.json`이 있으면 다음 갱신 때 필요한 키를 읽어 일괄 캐시에 합치고, 기존 파일과 벡터는 보존한다. 캐시 형식 전환 때문에 임베딩을 다시 호출하지 않는다. 이후 갱신은 일괄 캐시를 한 번 읽는다. 파일 수·작은 영속 쓰기는 줄지만 일괄 캐시 전체 읽기/쓰기와 메모리 사용은 남는다. [비용 분해·고정20문항 비교](../../results/service-storage/v2b/README.md).
