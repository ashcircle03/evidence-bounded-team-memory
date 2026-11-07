# 팀원 연결용 단일 호출 경로

`team_memory.service.TeamMemoryService` / `python -m team_memory.service`를 사용한다.
기존 `AttributedQA`와 `timeline`을 연결한다. UI·MCP·Git 전송·신원 인증은 호출자가 맡는다.
이 명세는 의미 성능이 해결됐다는 선언이 아니다.

## 실행

Aurora의 GPU 계산 노드에서 conda를 활성화하고 같은 할당의 로컬 모델 서버에 연결한다.
새 sbatch는 12시간 walltime, 처리 완료 시 종료한다. 로그인 노드에서는 실행하지 않는다.

```sh
export NLTK_DATA=/path/to/prepared/nltk-data
python -m team_memory.service \
  --store /path/to/checkout/shared-records \
  --model-path /path/to/pinned/Qwen3-8B \
  --embedding-path /path/to/pinned/embedding \
  --api-base http://127.0.0.1:PORT/v1 \
  < requests.jsonl > responses.jsonl
```

한 줄에 요청/응답 JSON 하나다. 진단은 stderr로 간다. 의존성은
`requirements-reference.txt`, NLTK 자료는 `punkt_tab`과 BM25용 `stopwords`다.
유료 API로 우회하지 않는다. 이번 실행은 기존 설치 환경을 재사용하며 client/server
각 interpreter·패키지를 결과에 기록한다. 클린 재설치 검증과는 구분한다.

```json
{"operation":"import_history","records":[{"owner":"Alice","observed_at":"2026-01-01T00:00:00Z","source":{"speaker":"Alice","location":"git://notes/1","text":"Original text.\n"}}]}
{"operation":"ingest","source":{"owner":"Bob","observed_at":"2026-01-02T00:00:00Z","source":{"speaker":"Bob","location":"git://notes/2","text":"A new report."}}}
{"operation":"ask","question":"What was reported?","temporal_scope":"current"}
{"operation":"sync"}
{"operation":"review","proposal_id":"RETURNED_ID","actor":"Alice","choice":"approve"}
{"operation":"view"}
```

- `import_history`: 빈 저장소 최초 적재. 모델 호출/소급 승인 없이 저장한다.
- `ingest`: 아직 처리하지 않은 공유 원문을 읽고 새 보고를 기존 timeline으로 비교.
- `sync`: Git 병합 후 새 원문 처리. 처리 영수증 재사용, 실패는 노출하며 무조건 재시도하지 않는다.
- `ask`: 동기화 후 기존 attributed QA. 검색 출처에 연결된 검토 관계가 있으면 양쪽 원문과
  상태를 독해/수정에 전달한다. 무관한 관계의 존재만으로 답을 막지 않는다.
- `review`: 원작성자/정확한 proposal ID 검사. 상충 투표는 유지. actor 문자열은 인증 자체가 아니다.
- 재시작: 원문·제안·투표를 읽으며 native 기억을 다시 작성하지 않는다. `rebuild`는 `sync` 별칭.

## 원문·Git 경계

v2 `SourceStore`는 공백·줄바꿈을 포함한 입력 텍스트를 보존한다. 과거 `store.py`의
정규화 규칙과 기존 해시 파일은 그대로다. 이미 잘린 공백은 복구할 수 없으며,
과거 정규화본과 새 원본은 내용이 다르면 다른 ID다. 자동 치환/소급 덮어쓰기는 하지 않는다.

공유 파일은 `sources/`, `timeline_proposals/`, `timeline_votes/`의 불변 JSON이다.
처리 영수증과 색인은 Git 안에서 `.git/team-memory-clients/` 아래에, Git 밖에서는
`.timeline-client-저장소이름`에 둔다. `--client-state`로 지정할 수도 있다.
타인의 처리 영수증이 자신의 새 맥락 검토를 억제하지 않는다. 한 checkout의 실행
프로세스는 하나로 둔다. 독립 checkout 병합과 같은 checkout의 동시 수정은 다르다.

## 응답 계약

공통 필드는 `schema_version=team-memory/v2`, `operation`, `implementation`, `status`다.
QA는 `raw`, `answers[].evidence`, `citation_sources`, `review_context`, `review_status`를 반환한다.
근거에는 ID·작성자·기록시각·위치·원문 구절·offset을 연결한다. QA 상태와 검토 처리 상태는 분리한다.
정정 관계가 있는 근거의 `assertion_reviews`에는 해당 원문 구절만의 상태를 연결한다.
현재 사실을 검토하는 document judge에는 승인으로 대체된 구절만 제외한 읽기용 표현을 준다.
원본·최종 인용은 바꾸지 않으며 같은 문서의 다른 사실, 과거 QA, 승인 충돌은 제외하지 않는다.
이 구분은 기존 `timeline.assertion_status`를 재사용하며 추가 모델 호출은 없다.

`ok`는 실행/구조 검사 성공이며 의미 정답 인증이 아니다. `partial`은 답·경고를 함께
읽는다. `invalid`/`error`는 기권 정답이 아니다. AQA 교체는 `answer_revision`에 원답·
원근거·후보·교체 기준을 보존하고 `partial`로 표시한다. ID 유지로 의미 보존까지
인증하지 않는다. 잘못된 후보 생성 자체가 해결됐다는 뜻은 아니다.

## 재사용 의도

| 책임 | 재사용 | 이번 변경 |
|---|---|---|
| 저장·출처 | 기존 Store 불변 객체·validator | 새 입력의 원문 보존, 과거 해시 호환 |
| 검색·QA·인용 | LlamaIndex RRF·ConflictScore·AQA·LangChain인 AttributedQA | 일반 QA 경로 유지, 날짜 전달 복구 |
| 비교·검토·투표 | 기존 timeline direct | 같은 저장소/공개 호출 경로에 연결 |
| 정정·공존 문맥 | practical의 양쪽 원문 연결, 기존 TEMPORAL_POLICY | 검증된 관계 구절·실제 상태 전달 |
| 실행 경계 | 기존 JSONL/stdout 분리 | 실험 profile 선택 대신 한 창구 |

새 기억 작성 모델·추가 판정 LLM·검색 알고리즘은 도입하지 않았다. 기존 개별 CLI는
과거 재현/진단용이다. `tests/test_service.py`의 실검색·stub 생성 통합 검사와
[실제 Qwen 실행/기존20 재생](../results/service-v2/README.md)을 구분한다.

## Review evidence and reader comparison

State explanations can cite `evidence_type: review_state` objects with
`snapshot_id`, `proposal_id`, `vote_ids` and `record_snapshot`. Their `source_id`
begins with `review:` and their offsets refer to the deterministic snapshot
rendering, not an original document. Ordinary evidence keeps its existing shape
and IDs. Consumers must distinguish these types before opening source files.
See [state citation contract](review-state-citations.md).

`--reader direct` uses the same original-source retrieval, initial generation,
review context and quote attribution without the optional document judge,
rewrite and AQA stages. `--reader attributed` preserves the checked profile.
The frozen comparison and per-case results live in `results/service-v3/`.
