# records 개선 제안 (수정안)

2026-11-22 · records 담당 · 기준 커밋 `93e8a15` (main)

> **진행 상황 (2026-11-22):** 작업 1·2·3, 3.4의 세 항목, 4-1, 5-1, 5-3, 5-4 코드를 브랜치 `records/alignment-and-blocks`에 7개 커밋으로 올렸다 (`476d8f3`..`e9d5bd2`, GitHub 원격 푸시 완료, PR 미생성). **실행 테스트·68문서 회귀·효과 측정은 아직 하지 않았다.** 3.4 항목: 부분 복구 기본값 `isolate_invalid=True`, layout 규칙 v2(발언은 목록 행으로 저장하지 않음, 검증은 v1·v2 모두 인정), 한글 원문에만 한국어 예시 추가. 5-3: `record_builder`를 RecordsAdapter가 실행(`connect_v2`가 전달). 5-4: `records/view.py`의 `claims_view()` (`records.view/v1`).

> **공개 개발셋 평가 반영 (2026-11-22):** 팀원 124911과 같은 조건으로 비교한 결과 `repair_conditions`(records/repair.py)가 조건 복구 29/49 → 44/49, 조건 정밀도 67.4% → 83.0%로 올려 **construct 기본값으로 채택**했다 (커밋 34ab70e, 로컬). source 정렬·2단계 추출은 선택 기능 유지. 세부 결과: `results/public-eval/SUMMARY.md`.

세 작업은 서로 독립적이다. **별도 브랜치에서 진행하고 따로 커밋한다.** 모두 기본값을 바꾸지 않는 선택 기능으로 먼저 넣고, 아래 채택 기준을 통과할 때만 기본값 전환을 제안한다.

| | 작업 1 | 작업 2 | 작업 3 |
|---|---|---|---|
| 이름 | 주장 먼저, 역할은 나중에 (2단계 추출) | 저장 중복 측정과 파생 데이터 정리 | 정렬과 블록 분할 개선 |
| 해결할 문제 | 조건·이유가 엉뚱한 주장에 붙거나 역할이 틀림 | 저장되는 기록에 다시 계산 가능한 데이터가 많음 | 형식 없는 입력·한국어에서 원문 연결 실패, 문서 전체 손실, 잘못된 위치 연결 |
| 바뀌는 것 | records 내부 추출 경로 (새 builder) | records 저장·읽기 경로 | 원문 정렬(`_aligned_span`), 블록 분할(`segments`, `construct`) |
| 다른 모듈 영향 | 없음 (출력은 같은 `records.graph/v3`) | 없음이 목표 (읽기 결과는 바이트 단위로 동일) | 없음 (출력 형식 동일) |
| GPU 필요 | 예 (Qwen 재생성) | 아니요 | 3-A 아니요 / 3-B 예 (작업 1과 같은 실행에서 측정 가능) |

---

## 작업 1. 2단계 추출: 주장을 먼저 정하고 역할을 채운다

### 1.1 기존 실험에서 확인된 사실

이 제안 전에 확인한 팀의 기존 결과다. 가설은 이 결과와 맞아야 한다.

- **오연결 26개의 원인** ([first-loss](../../evidence-bounded-team-memory/results/record-binding/first-loss/README.md)):
  역할 오류 13, 정답 대상과 연결할 수 없는 그룹 8, 구절 불일치 3, 다른 대상 2.
- **한 요소만 정답으로 바꾼 비교**: 역할만 교정하면 합성 10·자연 4건 복구, 대상 그룹만 교정하면 합성 3·**자연 0건** 복구.
- **"주장을 고정하고 조건·이유만 연결"하는 방식은 이미 기각됐다.**
  `anchored_binding`·`context_contract`(Qwen 8B/14B)는 다른 주장에 붙이거나 조건·이유를 혼동했고 ([v2](../../evidence-bounded-team-memory/results/record-binding/v2/README.md)), `pair_binding` 분류기(v4)는 새 오연결이 많아 기각됐다 ([v4](../../evidence-bounded-team-memory/results/record-binding/v4/README.md)).

따라서 "그룹을 모델이 추측하지 않으면 오연결이 줄어든다"만으로는 근거가 약하다. 이 작업의 목표를 **역할 오류(13개)와 연결할 수 없는 그룹(8개)을 함께 줄이는 것**으로 정한다.

### 1.2 가설과 기존 실험과의 차이

**가설:** 블록 안에서 주장을 먼저 원문 그대로 확정하고, 주장마다 "이 주장의 조건은? 이유는? 시간은? 대상은?"을 빈칸 채우기로 물으면, 한 번에 모든 역할과 그룹을 뽑을 때보다 역할 혼동과 고아 그룹이 줄어든다.

기각된 방식과 다른 점은 다음 세 가지다. 이 차이가 효과를 내는지가 검증 대상이다.

| | 기존 anchored / v4 | 이번 제안 |
|---|---|---|
| 주장 | 기존 추출 결과를 그대로 고정 | 1단계에서 블록 단위로 새로 추출 |
| 질문 방식 | 문맥 구절마다 "어느 주장의 조건/이유인가"를 분류 | 주장마다 역할 칸을 채움 (주장 → 구절 방향) |
| 문맥 범위 | 문서 전체 | 현재 블록만 인용 대상, 앞 1~2문장과 섹션 제목은 인용 불가 참고 문맥 |

### 1.3 설계

**새 파일 `team_memory/records/staged.py`**, 진입점 `construct_staged(source, generate, *, model, ...)`.
기존 `preserving.construct`의 시그니처와 출력 형식을 따르므로 `connect_v2(record_builder=...)`에 그대로 꽂을 수 있다.

```text
segments.blocks(text)                      ← 기존 그대로 (규칙 기반 블록 분할)
  └─ 블록마다
       1단계 호출: 주장·동작 구절 목록 (원문 복사, stance 포함)
       2단계 호출: 위 주장 목록 전체를 주고, 주장별로 condition/basis/time/subject 구절
       → 두 출력을 기존 LangExtract raw 형식으로 변환 (claim_group = 1단계 주장 번호)
       → preserving.compile_graph(...)     ← 기존 정렬·검증 재사용
segments.assemble(...)                     ← 기존 그대로
layout / validate_graph                    ← 기존 그대로
```

- **호출 수:** 블록당 2회로 고정한다. 주장마다 따로 부르지 않는다 (1+N회는 비용이 크다).
- **출력 형식:** `records.graph/v3` 그대로, `builder='langextract-staged-v1'`만 다르다. 계약 변경 없음.
- **1단계는 넉넉하게:** 놓친 주장은 2단계에서 복구할 수 없다. 대신 과잉 추출(인사말 등)은 평가 지표로 따로 센다.
- **참고 문맥:** 앞 블록 1~2문장과 섹션 제목은 프롬프트에 "인용 금지" 영역으로 준다. 정렬은 현재 블록 텍스트에만 하므로 바깥 구절을 인용하면 자동으로 정렬 실패 → `diagnostics`에 남는다.
- **행위자:** 계약에 actor 필드가 없다 (records README: "별도 actor 필드는 없다"). **새 필드를 만들지 않고**, 명시된 행위자를 claim 구절 안에 포함하도록 지시한다. 모든 구절이 원문 복사이므로 원문에 없는 작성자 이름은 구조적으로 들어갈 수 없다. actor 필드 추가는 계약 v1.3 안건으로 분리한다.
- **출력 강제:** 두 단계 모두 vLLM `guided_json`을 쓴다 (`grouped.writer_kwargs` 방식).
- **프롬프트 예시:** 68문서 평가셋 문장을 예시로 쓰지 않는다 (누출 방지).

### 1.3.1 구현 메모 (2026-11-22, 브랜치 `records/alignment-and-blocks`, 미커밋·미검증)

- 작업 3의 `preceding()`·`compact()`를 재사용하므로 **작업 3과 같은 브랜치에 두고 커밋만 분리**한다 (원래 계획: 별도 브랜치).
- 블록 순회는 `preserving.build_blocks(source, extract, ...)`로 공용화했다. `preserving.construct` 기본 동작은 그대로다.
- `staged.construct(source, generate=None, *, model, generate_claims=None, generate_roles=None, isolate_invalid=False, alignment='token', segmentation='legacy', max_block_chars=None)`.
  기본값은 기존과 같은 블록·정렬이라 작업 1의 효과만 따로 비교할 수 있다. `alignment='source'`, `segmentation='compact'`와 조합 가능하다.
- 단계별 출력 형식: 1단계 `{"claims":[{"text","stance"}]}`, 2단계 `{"claims":[{"claim":번호,"condition":[],"basis":[],"time":[],"subject":[]}]}`. guided_json 설정은 `claims_writer_kwargs()`·`roles_writer_kwargs()`.
- `isolate_invalid=True`면 2단계가 실패해도 1단계 주장은 역할 없이 보존하고 diagnostics에 남긴다.
- builder 이름: `langextract-staged-v1`, 블록 경로 `langextract-staged-blocks-v1`/`-v2` (+`+source-align`).
- 아직 없음: 프롬프트 예시(평가셋이 아닌 문장으로 추가 예정), `predict` 역할 보정 연동, 단위 테스트, 관문 0 스크립트.

### 1.4 평가 순서

**관문 0 — 상한 확인 (전체 실행 전에, 저비용).**
68문서의 정답 주장을 1단계 출력 대신 넣고 2단계만 실행한다. 1단계가 완벽해도 역할 오류·고아 그룹이 기존(13·8)보다 줄지 않으면 **여기서 중단**한다. 이 결과만으로도 "그룹 고정의 효과"에 대한 답이 된다.

**관문 1 — 전체 비교.** 관문 0을 통과하면 1·2단계를 모두 실행한다.

- 같은 Qwen3-8B, 같은 68문서, 같은 디코딩 설정(temperature 0)으로 **기존 방식도 새로 생성**해 비교한다. 기존 68문서 회귀는 저장된 출력 재생이라 새 생성과 직접 비교할 수 없다.
- Aurora Slurm 작업으로 실행하고 작업 ID·입력 해시·토큰 수를 남긴다.

| 지표 | 채택 조건 |
|---|---|
| 기존 정답 연결 51개 | **51개 모두 유지** |
| 오연결 수 | 기존 이하 |
| 조건 정밀도 | 기존 이상 |
| 오연결 원인별 개수 (역할/그룹/구절/대상) | 역할·그룹 오류가 실제로 감소 |
| 과잉 주장 수 (인사말·형식 구절) | 기존 대비 증가하지 않음 |
| 호출 수·입출력 토큰 | 보고 (채택 판단 시 비용 고려) |

선택: 공개 개발셋(QA-SRL 1,000문장, Causality 조건 49건)에서 PR #2와 같은 방식으로 추가 비교.

### 1.5 커밋 단위

1. `records: add optional staged extraction builder` — `staged.py` + 가짜 `generate`로 도는 단위 테스트 (블록 분할, 참고 문맥 인용 차단, raw 변환, v3 검증 통과)
2. `evaluation: staged extraction upper-bound and full comparison` — 관문 0·1 스크립트
3. `results: staged extraction on 68 documents` — 원출력·채점·판단

---

## 작업 2. 저장 중복 측정과 파생 데이터 정리

### 2.1 측정 결과 (68문서 저장본)

`results/record-binding/v1/stored-records.json`의 68개 기록(`records.graph/v3`)을 저장소의 실제 직렬화(`store.encoded`)로 측정했다. `v2/anchored-stored.json`도 거의 같은 비율이었다.

| 구성 요소 | 원본 크기 대비 | 압축(zlib) 후 대비 | 다시 계산 가능? |
|---|---:|---:|---|
| 원문 text | 2.7% | — | 아니요 (원본) |
| **quote 복사본** (units, layout, excluded) | **5.1%** | **3.0%** | 예: `text[start:end]` |
| **edges** | **42.1%** | **16.4%** | 예: `graph.edges_for(units, claims)` |
| 들여쓰기·공백 (`indent=2`) | 33.8% | — | 예, 하지만 **변경 불가** (아래) |

추가로, `record.append` 커밋 파일 하나에 같은 source와 그래프가 **두 번** 들어간다. 한 번은 `objects`, 한 번은 재시도 비교용 `payload`다 (`adapters/records.py`). 커밋 파일 크기가 기록의 약 2배라는 뜻이다. 이 부분은 실제 커밋 저장소에서 따로 측정한다 (Windows는 `fcntl` 때문에 불가 → WSL/Aurora).

**결론:** quote만 없애면 압축 기준 약 3%가 줄어 효과가 작다. 같은 원칙(원본에서 다시 계산할 수 있으면 저장하지 않는다)을 **edges에 먼저** 적용하는 것이 효과가 크다.

**범위 밖:** 들여쓰기는 `store.encoded`가 정하는데, `store.py`는 과거 데이터셋 해시에 묶인 고정 파일이라 바꾸지 않는다.

### 2.2 우선순위

| 순서 | 대상 | 예상 효과 | 위험·조율 |
|---|---|---|---|
| A | edges를 저장하지 않고 읽을 때 재계산 | 큼 (압축 후 ~16%) | records 내부만 |
| B | 커밋의 payload 중복 제거 (정규화한 payload의 해시만 저장) | 큼 (커밋 파일 ~절반, 측정 필요) | 재시도(idempotency) 판정 변경 → **Gateway 담당과 조율** |
| C | quote 복사본 제거 | 작음 (~3%) | A와 같은 구현으로 함께 처리 가능 |

### 2.3 공통 설계 규칙 (원안 유지)

- `start`/`end`는 그대로 저장한다 (원문 검증, 같은 구절 구분, 검색 범위 제한, 인용 역추적).
- **읽기 경로에서 복원한다.** records가 snapshot을 만들 때 edges·quote를 다시 채운다. relations·retrieval·answering이 받는 데이터는 지금과 **바이트 단위로 동일**해야 한다.
- **기존 기록은 마이그레이션 없이 읽는다.** edges·quote가 이미 저장된 기록은 저장값과 재계산값이 같은지 검사해 손상을 잡는다.
- 계약 스키마(`records.graph/v3`)는 바꾸지 않는다. 압축 형태는 저장소 내부 표현이고, 검증(`validate_graph`)은 복원한 뒤에 한다. 압축 형태 표시는 그래프가 아니라 저장 envelope에 명시적 필드로 둔다.

### 2.4 해시에 대한 정정

원안의 "claim ID와 기록 해시는 quote 포함 여부와 상관없이 똑같이"를 다음처럼 나눠서 보장한다.

| 식별자 | 계산 방식 | 보장 |
|---|---|---|
| unit ID | `digest([source_id, [start, end]])` | 이미 quote와 무관 → **불변** |
| claim ID | unit ID 목록으로 계산 | 이미 quote와 무관 → **불변** |
| `source_fingerprint` | 원문 기준 | **불변** |
| 커밋 키 | `digest(commit)` = 저장된 바이트 전체 | 기존 커밋은 재작성하지 않으므로 체인 유지. 새 커밋은 저장 형태로 계산 |

- 재시도 판정(`commit['payload'] != payload`)은 비교 전에 양쪽을 같은 형태로 정규화해야 한다.

### 2.5 채택 기준

- 68문서와 모듈 계약 예제에서 `snapshot.get` 결과와 reader 입력 근거 묶음 192개가 변경 전과 **동일**.
- 구버전 기록과 새 형태 기록을 섞은 저장소에서 읽기·검증·재시도가 정상.
- 일부러 손상시킨 quote/edges가 들어간 구버전 기록을 거부.
- 실제 커밋 저장소 기준으로 크기 감소가 팀이 정한 기준(예: 압축 후 15% 이상)을 넘으면 기본값 전환을 제안.

### 2.5.1 구현 메모 (2026-11-22, 브랜치 `records/alignment-and-blocks`, 미커밋·미검증)

- `records/compact.py`: `compact_record` / `hydrate_record` / `hydrate_payload`. 저장하지 않는 값은 unit·layout·excluded·arguments의 quote와 graph edges다. start/end는 유지한다.
- 표시: 압축 기록은 envelope에 `record_storage: records.compact/v1`을 둔다 (그래프 안이 아님). 표시가 없으면 기존 전체 기록으로 읽는다.
- 쓰기: `RecordsAdapter(..., storage='compact')` 또는 `connect_v2(..., records_storage='compact')`. 기본값 `full`은 기존과 같다.
- 읽기: `adapters/legacy.public_source`에서 복원한다. 모든 snapshot·검증 경로가 이 함수를 거치므로 다른 모듈은 기존과 같은 전체 형태를 받는다. 복원 후 `validate_graph`가 기존처럼 검사한다.
- 손상 검출: 압축 기록에 quote나 edges가 들어 있으면 거부한다 (조용히 덮어쓰지 않음). 전체 기록은 기존대로 저장된 quote·edges를 원문·재계산값과 대조한다.
- **2-B 일부 포함:** 커밋 영수증(payload)의 source도 같은 규칙으로 압축한다. 재시도 비교는 `hydrate_payload`로 받은 형태로 되돌려서 한다. 영수증을 해시로 바꾸는 안(원래 2-B)은 하지 않았다. RecordsAdapter 내부 변경이라 Gateway 계약은 그대로다.
- 충돌 검사(`Source ID collision`)는 읽는 쪽에서 보는 형태로 비교하도록 바꿨다. 같은 기록의 전체/압축 사본은 같은 기록으로 본다.
- 측정: `evaluation/records/storage_redundancy.py`는 `records`(JSON 파일)와 `store`(커밋 저장소, fcntl 불필요) 두 모드를 지원한다.

### 2.6 커밋 단위

1. `evaluation: measure records storage redundancy` — 측정 스크립트와 결과 (quote, edges, payload 중복, 실제 커밋 저장소)
2. `records: optional compact storage that rebuilds edges and quotes on read` — 저장·복원 + 호환·손상 검출 테스트

---

## 작업 3. 정렬과 블록 분할 개선

실제 사용자는 형식을 맞추지 않은 메모, 불릿 목록, 한국어 문장을 그대로 넣는다. 그런 입력을 가짜 모델로 `preserving.construct()`에 넣어 현재 동작을 확인했다 (재현: `tools/probe_inputs.py`, `tools/probe_korean_alignment.py`).

### 3.1 실험으로 확인한 문제

| # | 입력 | 관찰 결과 | 원인 위치 |
|---|---|---|---|
| 1 | `dataset v1에서는 Petr가 초안을 승인했다.`에서 subject `초안` | `Ungrounded extraction` → 문서 전체 failed | LangExtract가 띄어쓰기 토큰(`초안을`, `Petr가`) 단위로 정렬. 조사를 뺀 명사는 원문에 있어도 못 찾음 |
| 2 | 한 행만 `tests passed` → `the tests passed`로 바꿔 씀 | 문제없던 다른 주장까지 모두 사라짐 (failed, 주장 0개) | 기본값 `isolate_invalid=False`: 행 하나의 예외가 `_prepare` 전체를 실패시킴 |
| 3 | `Ship it. Later Mina said: ship it.`에서 두 번째를 인용 | 첫 문장 `Ship it`에 **조용히** 연결 (오류 표시 없음) | 정렬이 대소문자를 무시하고 첫 일치 위치 선택. claim에는 반복 검사 없음 |
| 4 | 불릿 3줄 (`- 그건 QA 통과 후에 한다` 포함) | 블록 3개, LLM 호출 3회. 각 호출이 앞 불릿을 못 봄 | `segments.blocks()`가 불릿을 줄마다 블록으로 나눔 |
| 5 | 형식 없는 긴 줄글 | 문서 전체가 블록 하나로 한 번에 모델에 들어감 | 블록 크기 상한 없음. PR #2 평가에서 2,573회 중 447회가 종료 토큰 없이 잘림 |
| 6 | `If QA passes, ship v2. QA owns the checklist.`에서 subject `QA` | `Ambiguous repeated context span` → 문서 전체 failed | 문맥 구절이 원문 전체에서 두 번 이상이면 거부 (의도된 안전 규칙) |
| 0 | `## Release` 제목 줄 | 제목 하나만으로 LLM 호출 1회 | 제목이 별도 블록으로 `_extract`에 전달됨. 다음 블록에는 이미 `section`으로 전달됨 |
| 7 | `- 민수: 문서 정리, 슬라이드 수정` | layout에 `label='민수'`, 쉼표로 나눈 `cells`로 저장 | `layout.layout()`의 `- 라벨: 값` 규칙이 발언자 표기에도 적용 |
| 8 | 한국어 입력 전반 | 프롬프트 예시가 모두 영어. 단일 블록 경로에서 speaker `민수`가 `민수`로 들어감 | `grouped.examples()`, `_extract`의 `ensure_ascii=context is None` |

1·2·6번은 겹쳐서 일어난다. 한국어 명사 하나 또는 흔한 단어 하나 때문에 **문서 전체의 주장이 사라진다.**

### 3.2 작업 3-A: 원문 정렬 (`_aligned_span`) — GPU 불필요

원칙은 그대로 둔다: **원문에 글자 그대로 있고 위치가 하나로 정해질 때만 연결한다.**

| 항목 | 변경 |
|---|---|
| 1. 한국어 조사 | 토큰 정렬이 실패하면 **글자 단위로 정확히 한 번만 나오는** 경우에 그 위치를 쓴다. 여러 번 나오거나 없으면 지금처럼 실패 |
| 3. 반복 문장 | claim에도 반복 검사를 적용한다. 대소문자까지 일치해야 통과한다. 위치를 정할 수 없으면 실패로 기록한다 (조용한 오연결 금지) |
| 6. 흔한 단어 반복 | 같은 그룹 claim이 걸친 문장(window) 안에서 한 번만 나오면 그 위치를 쓴다. 그래도 둘 이상이면 지금처럼 거부 |

- 저장된 모델 출력을 재생하는 기존 68문서 회귀로 검증할 수 있다. 정렬만 바뀌므로 새 생성이 필요 없다.
- 1·6번은 지금 버려지는 연결을 살리므로 **새 오연결이 생기는지**를 반드시 본다. 3번은 지금 조용히 통과하던 연결을 실패로 바꾸므로 **잃는 정답 연결이 있는지**를 본다.

**채택 기준:** 68문서에서 기존 정답 연결 51개 유지, 오연결 수 증가 없음, 조건 정밀도 하락 없음. 위 실험 입력과 한국어 사례를 단위 테스트로 고정한다.

### 3.3 작업 3-B: 블록 분할 (`segments.blocks`, `construct`) — GPU 필요

| 항목 | 변경 |
|---|---|
| 0. 제목 블록 | 제목만 있는 블록은 LLM을 부르지 않고 원문 조각(`graph.build`)으로 처리한다. 제목은 지금처럼 다음 블록의 `section`으로 전달 |
| 4. 불릿 | 연속된 불릿을 하나의 목록 블록으로 묶어 한 번에 추출한다. 표·목록 좌표(layout)는 지금처럼 따로 저장 |
| 5. 긴 블록 | 상한(문자 수 또는 토큰 수)을 넘으면 문장 경계에서 나눈다. 나눈 조각에는 앞 1~2문장을 인용 금지 참고 문맥으로 준다 (작업 1의 참고 문맥 설계 재사용) |

- 프롬프트에 들어가는 텍스트가 바뀌므로 새 생성이 필요하다. **작업 1의 관문 1과 같은 Aurora 실행에서** 기존 방식, 3-B, 작업 1을 함께 비교하면 GPU 사용을 줄일 수 있다.
- 지표: 작업 1의 채택 기준과 같다. 여기에 **블록 수, 호출 수, 잘린 출력 수**를 추가한다.

### 3.4 별도 판단이 필요한 항목

- **2. 부분 복구 기본값 (`isolate_invalid=True`)**: 코드 주석에 "이걸 켜면 예전에 통째로 버려지던 문서의 잘못된 행이 노출되며, 오연결 관문을 통과하지 않았다"고 되어 있다. 3-A를 적용한 뒤 68문서에서 `isolate_invalid=True`의 새 오연결을 측정하고, 통과하면 기본값 전환을 제안한다.
- **7. 발언자 표기**: `- 이름: 내용` 형태를 layout 목록으로 볼지 발언으로 볼지 기준이 필요하다. 쉼표 분할은 값 목록이 확실한 경우로 제한하는 안을 검토한다.
- **8. 한국어 예시와 메타데이터 인코딩**: 평가셋이 아닌 문장으로 한국어 예시를 추가한다. `ensure_ascii` 통일은 예전에 저장한 출력의 재생 비교(프롬프트 바이트 일치)를 깨므로, 새 생성 실험과 함께 바꾼다.

### 3.5 커밋 단위

1. `tests: pin alignment behaviour on Korean, repeated and paraphrased spans` — 현재 동작을 드러내는 테스트 (실패 사례 포함, 기대값은 수정 후 동작)
2. `records: character-level unique fallback and case-sensitive repeat checks in alignment` — 3-A 구현 + 68문서 회귀 결과
3. `records: skip heading-only blocks, merge bullet runs, cap block size` — 3-B 구현 (선택 기능) + 단위 테스트
4. `results: block segmentation comparison` — 작업 1과 함께 실행한 비교 결과

---

## 작업 4. 저장소 운영 문제 (5단계 검토에서 발견)

| # | 문제 | 위치 (workspace) | 상태 |
|---|---|---|---|
| 1 | Git으로 공유하다 체인이 갈라지면 기본 읽기·쓰기가 전부 `STALE_SNAPSHOT` | `4_boundary/records_adapter.py` `chain()` | **코드 작성 (미커밋·미검증)** |
| 2 | `fcntl` 때문에 Windows에서 import 실패 | 같은 파일 `lock()`, `_sync_directories()` | 보류 |
| 3 | 요청마다 전체 체인·모든 source 재검증 (기록 수에 비례해 느려짐) | `chain()`, `_check_objects()`, `snapshot_from()` | 보류 |
| 4 | 손상 기록 하나가 저장소 전체를 막고, 어느 커밋인지 표시 안 함 | `_check_objects()` | 보류 |
| 5 | 검토 권한이 원문 owner로 고정 (위임 불가) | `_apply()` review 검사, proposal reviewer | 팀 안건 |
| 6 | 커밋 시각이 각 PC 시계 | `now()` | 보류 |
| 7 | 내부 KeyError·TypeError도 INVALID_INPUT으로 보고 | `4_boundary/adapter_base.py` | 팀 공통 파일 |

### 4-1 구현 메모 (갈라진 체인)

- **자동 병합은 하지 않는다** (기능명세서 범위 유지). 대신 저장소가 멈추지 않게 한다.
- 기본 읽기·쓰기: head가 여러 개면 **이 checkout이 마지막으로 쓴 head**를 계속 쓴다. 이 포인터는 공유 폴더 밖 `<store 상위>/.module-local-<store 이름>/head`에 둔다 (Git HEAD와 같은 역할, Git으로 공유되지 않음). 포인터가 없으면 지금처럼 `STALE_SNAPSHOT`이지만 메시지에 head 목록을 넣는다.
- `heads()`: 현재 head 목록 (revision, 시각, 내 head 여부).
- `reconcile(base)`: 다른 갈래의 명령(append·제안·검토)을 원래 사용자·idempotency key·시각으로 base 위에 다시 적용한다. 새 명령과 같은 검사를 거친다 (권한·revision 검사만 생략, 원래 갈래에서 이미 통과). **전부 성공할 때만 쓴다.** 충돌하면 멈춘 커밋 ID를 알려준다. base에 이미 같은 명령이 있으면 건너뛴다. 기존 커밋 파일은 바꾸지 않고, `module_reconciliations/`에 흡수된 head 기록을 남긴다.
- 계약 operation이 아니다. 누가 실행할 수 있는지는 호출 쪽(운영 도구)이 정한다.
- 이를 위해 `execute()`의 쓰기 로직을 `_apply()`로 분리했다. 새 명령 경로의 동작은 같다.

---

## 작업 5. 기능명세서 대조에서 찾은 빈틈 (7단계)

F01·F04·5장 경계·6장 시험(T05~T07)·7장 전환을 코드와 대조했다. F04, T05~T07, 동시성 요구는 충족한다.

| # | 빈틈 | 명세 | 상태 |
|---|---|---|---|
| 1 | 블록 하나인 문서에서 모델 호출이 실패하면 예외가 Gateway로 올라가 **원문이 저장되지 않음** | F01 "추출기가 중단돼도 원문은 조회 가능" | **코드 작성 (미커밋·미검증)** |
| 2 | 행 하나 실패 → 문서 전체 failed (기본값 `isolate_invalid=False`) | F01 누락 사유 | 작업 3.4-2와 같음 |
| 3 | 추출 실행이 Gateway(`record_builder`)에 있음 | 7장 Gateway 축소 | Gateway 담당과 함께 |
| 4 | 구버전 그래프·역할 데이터를 공통 주장·구절 표현으로 읽는 변환기 없음 | 7장 Records 표현 통합 | records 몫, 미착수 |
| 5 | 원문 ID를 호출자가 정함 (records는 충돌만 검사) | F01 "Records가 원문 ID 발급" | 계약 해석 확인 |
| 6 | 검토 위임 권한 없음 | F04 "검토 권한" | 팀 안건 (작업 4-5) |
| 7 | 그래프가 없으면 `describe()`가 None. "추출 안 함" 상태를 알려주지 않음 | 5장 "빈 목록과 상태" | 보류 |

### 5-1 구현 메모 (원문 미저장)

- `preserving.build_blocks`의 단일 블록 경로에서 추출 예외를 잡는다 (`_extract_whole`). 원문은 원문 조각(units)으로 남고 `status='failed'`, `errors=['EXTRACTION_FAILURE']`, `diagnostics`에 예외 사유를 기록한다. 블록 여러 개 경로(`_extract_or_raw`)와 같은 방식이다.
- 공용 함수에서 처리하므로 `preserving.construct`와 `staged.construct`에 모두 적용된다. 실패 그래프의 builder는 각각 `langextract-preserving-v1`, `langextract-staged-v1` (+`+source-align`)이다.
- Gateway는 failed 그래프를 받으면 기존대로 `MODEL_OUTPUT_INVALID`를 함께 반환한다 (원문 저장은 성공).
- 기본 동작이 바뀌는 수정이다. 이전에는 모델 서버 오류 시 ingest 전체가 실패했고, 이제는 원문이 저장되고 추출 실패가 기록된다. 저장된 출력을 재생하는 68문서 회귀에는 영향이 없다 (generate가 예외를 내지 않음).

---

## 팀 회의에서 정할 것

1. actor(행위자) 필드를 계약 v1.3에 추가할지. 이번 작업 1은 추가하지 않는 것을 전제로 한다.
2. 작업 1의 Aurora GPU 사용 범위 (관문 0만 먼저 vs 관문 1까지). 작업 3-B를 같은 실행에 포함할지.
3. 작업 2-B(payload 중복)를 Gateway 담당과 함께 진행할지.
4. 작업 2의 기본값 전환 크기 기준.
5. 부분 복구(`isolate_invalid=True`)를 기본값으로 바꾸는 기준.
6. 팀 기록의 주 언어를 한국어로 볼지. 한국어라면 records 평가셋에 한국어 문서를 넣어야 한다 (현재 68문서와 공개 평가셋은 영어 중심).

## 참고

- 측정 스크립트: `records-workspace/tools/measure_storage.py`. 레포 루트에서 `python ../records-workspace/tools/measure_storage.py results/record-binding/v1/stored-records.json`처럼 실행한다. 작업 2의 커밋 1에서 `evaluation/`으로 정식 추가할 예정이다.
- 입력 실험: `records-workspace/tools/probe_inputs.py`(형식 없는 입력 6종), `records-workspace/tools/probe_korean_alignment.py`(한국어 구절별 정렬). 둘 다 레포 루트에서 `.venv`로 실행한다.
- Windows에서는 `fcntl` 때문에 records 어댑터 테스트가 돌지 않는다. 검증은 WSL(Python 3.11 필요) 또는 Aurora에서 한다.
