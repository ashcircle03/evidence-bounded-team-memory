# records 담당자의 개발·실험 기준

## 범위와 멘토 피드백

records의 성공은 **원문과 모델의 제안, 사람의 승인 상태를 섞지 않고 다음 모듈에 전달하는 것**이다. 저장됐다는 이유만으로 주장이 참이 되거나 제안이 승인되면 안 된다. records는 관계 종류를 추론하거나 QA 답변을 생성하지 않는다. `relations`가 제안한 관계와 정확한 원문 span을 받아 구조·참조·권한을 검사하고, 명시적 review 이벤트를 기존 v2 reducer에 적용한다.

| 책임 | 보장할 항목 | 여기서 보장하지 않는 항목 |
|---|---|---|
| 원문 수집 | ID, 원문 문자, owner/speaker, observed_at, location 보존 | 작성자의 진실성·실제 신원 인증 |
| 제안 저장 | 원문 span 일치, 대상 존재, 정정의 assertion 범위, reviewer가 이전 owner | 정정/상충/재검토라는 의미 판단의 정답 여부 |
| 승인 처리 | 권한·revision·idempotency, 원문 보존, 상태별 효과 제한 | 승인된 재검토를 새 실험 성공으로 해석 |
| 조회 | 같은 이력의 결정론적 snapshot, 지정 snapshot ID 재조회 | 자연어 질의 해석, timestamp만으로 과거 유효값 추론 |
| 운영 | 파일 손상 감지, 재시도, 동시 쓰기 직렬화 | 갈라진 module commit의 자동 Git 병합, 서명 검증 |

원문의 조건은 text와 정확한 span으로 남는다. 현재 source 계약에는 독립적인 추출 claim/condition 테이블이 없다. 따라서 아래 보존 점수를 **조건 추출 정확도**라고 부르면 안 된다. 자동 추출을 추가한다면 원문 기준 정답 span, 추출자/모델 버전, `extracted` 자격을 별도로 정의해야 하며, 승인 상태로 자동 승격하지 않아야 한다.

## 설계 근거와 적용 범위

- [Event Sourcing의 원본 이벤트와 재구성 가능한 projection 분리](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)를 적용한다. 기존 immutable JSON commit과 v2 reducer를 유지하고, 캐시는 삭제해도 다시 만들 수 있는 읽기 보조물로 한정했다. 새 DB나 새 의미 판정기를 추가하지 않았다.
- [SQLite의 atomic commit 설명](https://sqlite.org/atomiccommit.html)에 나오는 파일 내용과 디렉터리 항목의 동기화 구분을 참고했다. 기존 `Store.put`의 파일 fsync·atomic link 뒤에 commit 디렉터리와 store root fsync를 추가했다. **SQLite 구현을 사용하거나 SQLite 수준의 내구성을 입증했다는 뜻은 아니다.** 실제 전원 장애·Ceph/NFS 장애 검증은 수행하지 않았다.
- 검증된 객체만 process-local 캐시에 보관한다. 매 조회마다 파일 목록과 device/inode/size/mtime/ctime을 확인하며 변경·삭제·추가를 반영한다. snapshot은 한 개만 캐시하고 반환값은 복사한다. `RecordsAdapter(root, workspace, cache=False)`로 모든 바이트를 다시 읽어 비교할 수 있다. 파일시스템 자체나 저장소 쓰기 권한을 가진 악의적 사용자를 인증하는 기능은 아니다.

## 데이터셋 선택

| 데이터 | 이 모듈에서 사용할 부분 | 사용하지 않을 성능 주장 |
|---|---|---|
| [EverMemBench-Dynamic](https://huggingface.co/datasets/EverMind-AI/EverMemBench-Dynamic/tree/a6b210a32248e841967b7b64a64281d2ff3f669d) | 기존 개발 실행에 포함된 528개 대화 source envelope의 무손실 저장·재조회 | 공식 전체 QA 점수, 승인 권한 평가 |
| 공개 Git·PEP 기록 | 기존 개발 실행의 중복 제거된 245개 source envelope | 새로운 보지 않은 Git 사례의 재검토 분류 성능 |
| [LongMemEval](https://github.com/xiaowu0162/LongMemEval/blob/main/README.md) | 향후 시간·knowledge-update 질의까지 포함할 때 후보 | 이번에는 실행·다운로드하지 않음. QA 변경 정답이 팀의 승인 이벤트를 대신하지 않음 |
| [WikiContradict](https://arxiv.org/abs/2406.13805) | 양쪽 passage 보존 및 relations/answering의 상충 처리 실험에 적합 | 이번 record 평가에 추가하지 않음. owner review와 transaction 정답은 별도 필요 |
| `evaluation/records/cases.json` | 합성 상태 이벤트와 기대 snapshot 효과 | 자연어 관계 분류 정확도, 일반화된 연구 성능 |

공개 데이터의 문장을 사람이 승인한 이벤트로 간주하지 않는다. 이번 자연 자료 평가는 이미 가공·확보한 `results/module-boundary/v1/result.json`의 envelope를 입력으로 한다. **원본 Hugging Face 파일에서 envelope로 바꾸는 전처리의 정확성은 이번 평가 범위 밖**이다. 새 다운로드나 기존 데이터 복제는 없었다.

합성 자료는 네 이야기(공존·상충·정정·재검토)에 원문 형식과 review 순서를 변형한 **46개 진단 흐름**이다. 40개 순차 흐름과 6개 기존 v2의 상충 투표 import 흐름을 구분한다. 46개 독립 이야기/held-out test로 보지 않는다. 관계 label과 span은 oracle 입력이다. 같은 이야기의 변형은 전부 diagnostic split에 둔다. 이후 semantic 모델 평가를 위한 test를 만들면 이야기/출처 단위로 분리하고, 수정에 사용한 이 진단셋을 test로 재명명하지 않는다.

## 상태 전이 계약의 중요한 구분

- pending: 아직 효과 없음.
- correction approve: 정확히 인용된 assertion만 정정 효과. 같은 문서의 담당자 등 다른 필드는 유지.
- reconsider approve: 재검토 허용. 원문이 틀렸거나 대체 결정이 확정됐다는 뜻 아님.
- conflict approve: 갈등 관계를 인정할 뿐 한쪽을 현재값으로 고르지 않음.
- coexist: informational. review 명령으로 승인·거절하지 않음.
- **순차적으로 이미 닫힌 review를 반대로 투표하는 요청은 거절한다.** 철회/재개 API가 없으므로 reject로 철회를 흉내 내지 않는다.
- 기존 v2 Git 저장소에 이미 반대 투표 두 개가 존재하면 import 시 `review_conflict`, effect none으로 보존한다. 새 module commit 분기 자동 병합과는 다른 기능이다.

초기 합성 정답표는 마지막 두 경우를 혼동해 12건을 실패로 기록했다. 기존 `review/state.py:review`의 closed-review 정책과 대조해 정답표의 오류로 판정했다. 초기 입력과 결과는 `results/records/v1/cases-initial.json`, `quality-initial.json`에 남겼다. 해당 12건을 통과시키려고 runtime의 승인 정책을 바꾸지 않았다. 최종 fixture는 이 구분을 명시하고 별도의 import 사례 6개를 추가했다.

## 측정과 실행

```bash
# 정답이 공개된 record 진단셋 + 기존 실제 source envelope 보존
.venv/bin/python -m evaluation.records.evaluate

# record 단독 회귀와 오류 주입
.venv/bin/python -m pytest -q tests/test_module_records.py

# 모델 없이 CI에서도 돌리는 상태 계약
.venv/bin/python -m evaluation.records.evaluate --synthetic-only --output .cache/records-quality.json

# 원문 누적 시 포트 전체 지연시간: validation과 전체 snapshot 응답 포함
.venv/bin/python -m evaluation.records.benchmark --output .cache/records-benchmark.json

# 기존 모델 요청이 정확히 같을 때만 응답을 재생하여 QA 퇴행 검사
TOKENIZERS_PARALLELISM=false .venv/bin/python -m evaluation.module_adapters.replay --output .cache/records-qa-replay
```

실행은 로컬 개발 환경 또는 Slurm 계산 노드에서 한다. Aurora 로그인 노드에서 수행하지 않는다.

측정값은 (1) 필드별 원문/메타데이터 완전 일치, (2) proposal 상태·효과·권한 일치, (3) 정정 범위 밖 보존, (4) 동일 snapshot 재조회와 cache off/on 일치, (5) 손상·실패·동시성 처리, (6) append/read 지연시간과 디스크 바이트, (7) 기존 QA 답·인용 보존으로 나눈다. 여기서 deterministic state 정답률을 LLM 성능처럼 보고하지 않는다.

속도는 10/100/300개 짧은 원문을 누적하며 마지막 10회 append와 10회 read의 median/p95를 기록한다. cold reopen도 따로 기록한다. 첫 수정 전후 수치는 같은 로컬 호스트의 단일 측정이며, proposed/approved 관계가 없는 workload다. 통계적 유의성·클러스터 처리량·대규모 서비스 SLO를 주장하지 않는다. 캐시를 도입해도 전체 snapshot과 파일 stat 확인이 필요하므로 O(N) 비용이 남는다. 승인 이력이 많은 부하와 더 큰 규모는 별도 측정이 필요하다.

결과와 한계는 [records 결과](../../results/records/README.md)에 기록한다.
