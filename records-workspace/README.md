# records 작업용 사본

> **이 폴더에 대해:** records 담당이 레포의 records 관련 파일을 데이터 흐름 순서로 모은 **읽기용 사본**입니다.
> 파일 이름·폴더가 원본과 달라 여기서는 import·실행되지 않습니다. 실제 코드는 레포 원래 위치(`team_memory/`, `evaluation/`)에 있고, 각 파일의 원본 경로는 아래 표의 오른쪽 열입니다.
> 동기화 도구(`sync.py`), 다른 모듈 파일, 팀 공통 문서 사본은 넣지 않았습니다. 공개 개발셋 평가 결과: `results/public-eval/SUMMARY.md`.


레포 `evidence-bounded-team-memory`에서 **records 담당에게 필요한 파일만** 모아 폴더별로 정리한 읽기·학습용 사본이다.

- **여기서 코드를 고친다.** 고친 뒤 `python sync.py --push`로 레포(현재 체크아웃된 브랜치)에 반영한다. 오른쪽 열이 레포 원본 경로다.
- `python sync.py`(pull)는 레포 → 여기로 가져온다. 여기서 고친 파일은 덮어쓰지 않고, 양쪽 다 바뀐 파일은 "충돌"로 알려주고 건드리지 않는다.
- `python sync.py --check`는 복사 없이 파일별 상태만 보여준다.
- 여기 파일끼리는 import가 맞지 않는다(파일명·폴더가 바뀜). 실행·테스트·커밋은 레포에서 한다.
- `3_storage/store.py`는 과거 데이터 해시에 묶인 고정 파일이라 push되지 않는다.
- 실험·재현용 후보(`bound`, `anchored_binding`, `context_contract`, `pair_binding`, `learned_binding`, `positive_binding`)는 일부러 뺐다.

## 읽는 순서

데이터가 흐르는 순서대로 번호를 붙였다.

```text
원문(source)
  │  4_boundary/records_adapter.py   record.append 요청을 받음
  ▼
1_core/construct.py  construct()      ← 공식 진입점
  ├─ 1_core/segments.py   문서를 문단·표·목록 블록으로 나눔
  ├─ 1_core/extract.py    프롬프트·예시·LangExtract 원문 정렬
  ├─ (LLM 호출: generate)
  ├─ 1_core/layout.py     표·목록 좌표
  └─ 1_core/graph.py      record_graph 형식 검증 (validate_graph)
  ▼
source + record_graph
  │  3_storage/           디스크에 불변 객체로 저장, snapshot 발행
  ▼
1_core/graph.py  describe()  →  4_boundary/reader_bridge.py  →  Retrieval·Answering
```

## 파일 지도

### 1_core — 원문을 record_graph로 만드는 핵심 (주로 고칠 곳)

| 작업용 | 원본 | 역할 |
|---|---|---|
| construct.py | `team_memory/records/preserving.py` | `construct()` 공식 진입점. 블록 분할 → LLM 추출 → 정렬 → 그래프 |
| extract.py | `team_memory/records/grouped.py` | 추출 프롬프트·예시·출력 스키마, LangExtract 정렬 |
| graph.py | `team_memory/records/graph.py` | 그래프 형식, `validate_graph`, Retrieval에 보이는 `describe`/`linked_span` |
| segments.py | `team_memory/records/segments.py` | 블록 분할 `blocks()`, 블록 결과 합치기 `assemble()` |
| layout.py | `team_memory/records/layout.py` | Markdown 표·목록의 행/열 좌표 |
| alignment.py | `team_memory/records/alignment.py` | 🆕 작업 3-A. 선택 정렬 `alignment='source'` (한국어 조사, 반복 구절) |
| staged.py | `team_memory/records/staged.py` | 🆕 작업 1. 2단계 추출 builder `staged.construct` (주장 먼저 → 주장별 역할) |
| compact.py | `team_memory/records/compact.py` | 🆕 작업 2. 압축 저장: quote·edges를 저장하지 않고 읽을 때 원문으로 복원 |

### 2_optional — 옵션을 넘겨야 동작

| 작업용 | 원본 | 켜는 방법 |
|---|---|---|
| arguments.py | `team_memory/records/arguments.py` | QA-SRL 출력이 있을 때 `with_arguments()` |
| discourse_roles.py | `team_memory/records/discourse_roles.py` | `construct(..., predict=...)` |
| discourse_scope.py | `team_memory/records/discourse_scope.py` | `construct(..., training_counts=...)` |
| policy_scope.py | `team_memory/records/policy_scope.py` | `construct(..., parse=...)` |

### 3_storage — 저장과 검토 상태 (모델 없음)

| 작업용 | 원본 | 역할 |
|---|---|---|
| store.py | `team_memory/store.py` | 실제 저장 구현. `storage/objects.py`가 이 파일을 가리킴. **과거 해시에 묶여 있어 수정 금지** |
| sources.py | `team_memory/storage/sources.py` | 원문 text를 정규화 없이 보존 |
| verified.py | `team_memory/storage/verified.py` | 검증한 객체의 메모리 캐시 |
| review_state.py | `team_memory/review/state.py` | 제안·승인·거절 상태 계산 |

### 4_boundary — 다른 모듈과 만나는 경계 (바꾸면 남에게 영향)

| 작업용 | 원본 | 역할 |
|---|---|---|
| records_adapter.py | `team_memory/adapters/records.py` | records 포트. `record.append`, `snapshot.get`, `proposal.submit`, `review.apply` |
| contract_schema.py | `team_memory/contracts/schema.py` | 팀 공통 JSON 스키마 원본 (source, record_graph v1~v4, arguments) |
| contract_validation.py | `team_memory/contracts/validation.py` | 스키마와 원문 위치 검증 |
| reader_bridge.py | `team_memory/adapters/reader_bridge.py` | records 그래프를 Retrieval·Answering 입력으로 바꿈 (Retrieval 담당과 공유) |
| adapter_base.py | `team_memory/adapters/base.py` | 모든 모듈 공통 요청 처리 `handle()`: 스키마·권한 검사 후 `execute` 호출, 응답 status 결정 |
| legacy_bridge.py | `team_memory/adapters/legacy.py` | 저장 envelope ↔ 공개 source 변환 (`envelope`, `public_source`). 압축 기록 복원 지점 |
| runtime.py | `team_memory/adapters/runtime.py` | `connect_v2` 조립. `records_storage='compact'` 옵션 |

### 7_eval — 평가·측정

| 작업용 | 원본 | 역할 |
|---|---|---|
| storage_redundancy.py | `evaluation/records/storage_redundancy.py` | 🆕 작업 2. 저장 기록·커밋 저장소에서 quote·edges·영수증 중복 비율 측정 |

### 5_tests — records 관련 테스트

레포 루트에서 실행한다. Windows에서는 `fcntl` 때문에 `test_record_preservation.py` 등 일부가 수집 단계에서 실패한다.

### 6_docs — 문서

| 작업용 | 원본 |
|---|---|
| records_README.md | `team_memory/records/README.md` |
| records_module.md | `docs/modules/records.md` |
| records_experiments.md | `docs/modules/records-experiments.md` |
| functional_spec.md | `docs/modules/team-memory-functional-spec.md` (F01·F04가 records) |
| contract_v1.2.md | `docs/modules/README.md` |
