# Records 구현과 실험 결과

서비스를 연결할 때는 [v0.2.1 사용 예제](../../team_memory/records/README.md)의 `preserving.construct`를 `record_builder`로 전달한다. [v0.2.1 태그](https://github.com/ashcircle03/evidence-bounded-team-memory/tree/v0.2.1)는 당시 구현과 회귀 기준을 고정한다. 아래 후보 파일은 과거 실험의 import 경로를 유지하기 위해 같은 패키지에 둔다. 서비스에 등록하려면 명시적인 연결이 필요하다.

| 상태 | 구현 또는 평가 | 판단 근거 |
|---|---|---|
| 사용 | `preserving.py`, `grouped.py`, `graph.py` | 68문서에서 경로 정리 전후 정답 연결 51개, 오연결 19개, 전달 근거 묶음 192개의 내용이 일치했다. [문서별 회귀 결과](../../results/records/v0.2.1.csv) |
| 선택 기능 | `discourse_roles.py`, `discourse_scope.py`, `policy_scope.py` | 한 주장에 연결된 구절의 역할을 보정한다. 학습된 predictor와 구문 분석기의 적용 전제는 [사용 안내](../../team_memory/records/README.md), 자연 기록의 개선 범위는 [정책 조건 실험](../../results/record-binding/policy-scope/README.md)에 있다. |
| 실험 전용 | `bound.py`, `context_contract.py` | 중첩 추출 및 조건·이유 입력 계약을 비교한 후보. [고정 정답 비교](../../results/record-bound/v1/ANALYSIS.md) |
| 실험 전용 | `learned_binding.py`, `anchored_binding.py`, `positive_binding.py`, `pair_binding.py` | 대상 주장과 근거 구절을 연결하는 후보 및 그래프 호환 코드. [학습 후보의 새 오류](../../results/record-binding/v1/README.md), [자연 기록 실패](../../results/record-binding/v2/README.md), [고정 구절 분류기 기각](../../results/record-binding/v4/README.md)를 따로 볼 수 있다. |
| 진단·평가 | 추출 품질, 저장, Git 교환 | [난이도·근거 가용성](../../results/record-strata/v1/README.md), [문서 전체 채점 v3](../../results/record-full/v3/README.md), [저장 중 정보 손실](../../results/record-causal/v1/README.md), [최초 실패 지점](../../results/record-binding/first-loss/README.md), [두 로컬 환경의 Git 교환](../../results/git-local/README.md) |
| 평가 준비 | [새 팀 기록 주석 프로토콜](../../evaluation/team_record_pilot/README.md) | 사람 records 비교를 위한 준비 자료다. 아래 MeeQA에는 사람이 표시한 답과 근거 구절이 있다. |

## MeeQA에서 관찰한 범위

사람 주석이 있는 서로 다른 회의 8건에서 동일 Qwen3-8B에 원문 또는 원문과 records를 주었다. 답 불가 4문항의 올바른 보류는 0→3건, 답 가능 4문항의 잘못된 보류는 양쪽 모두 2건이었다. 답 가능 문항의 정답·인용 위치 완전 일치는 각각 양쪽 모두 0건이었다. 이 비교는 이미 제공된 발언 창에서 수행했다.

③ 회의록과 ④ 구매 의향의 핵심 발언은 실제로 전달됐다. 평가용 Qwen은 전체 문맥에서는 사람 근거를 표시해도 보류했지만, 질문과 그 발언만 주고 분류시키자 둘 다 간접·조건부 답으로 인정했다. 두 사례에서 추출기를 바꿀 근거는 찾지 못했다. 기록 구조화, 검색, 답변 생성의 책임을 구분해서 해석한다.

[8문항 실제 답·인용](../../results/meeqa-pilot/comparison.md) · [지시 변경 및 후속 진단](../../results/meeqa-pilot/reader-ablation/README.md) · [평가 코드](../../evaluation/meeqa_pilot/)

과거 실행 코드는 당시 입력 파일과 체크포인트 경로를 사용한다. 실행 환경 전체, GPU 가중치, 중복 배포 압축본 및 서버 운영 로그는 이 연구 자료에 포함하지 않는다.

## 팀 배포본과 리모트 통합 점검 (2026-11-22)

팀 배포본 `0.2.1+records.1`은 `1869521`에서 준비했다. 기존 records 추출을 기본으로 사용하고, QA-SRL 역할을 제공받은 경우에만 `records.arguments/v1`으로 저장한다. 술어·역할 질문·답 구절을 원문 문자 위치에 묶고, 답변기에 보낼 때 술어와 답이 모두 선택 범위에 들어오는지 확인한다. 추출 자격은 `model_extracted_unverified`다. 공개 개발 입력 1,049건에서 저장한 연결 4,866개 전부가 재조회됐다. 이 수치는 원문 전체를 제공했을 때의 전달을 측정한다. [공개 개발 평가와 채택 판단](../../results/record-layout/records-v1-evaluation.md) · [저장 및 재조회 예제](../../examples/records_argument_roundtrip.py)

리모트 main `83d03a2`에는 retrieval의 주장 구간 색인과 조건 필터가 들어 있다. 이 시점의 리모트에는 로컬 records의 선택 역할 저장이 없다. 두 작업을 합칠 때의 단위는 다음과 같다.

| 범위 | 함께 확인할 파일과 동작 |
|---|---|
| 원문과 추출 | `records/{arguments,graph,layout,preserving,segments}.py`. 주장, 표 좌표, 선택 역할의 원문 위치를 보존한다. 구간·표 기반 추출의 평가와 기본 채택 여부는 별도로 관리한다. |
| 포트 계약과 전달 | `contracts/{schema.py,schema.json,validation.py}`, `adapters/{legacy,reader_bridge,answering}.py`, `readers/{retrieval,scoped}.py`. 원문에서 검색 구절, 주장별 답변 입력까지 동일한 역할을 전달한다. 리모트 retrieval.py에 추가되는 로컬 차이는 역할을 노드 메타데이터에 싣는 두 줄이다. |
| 회귀 검사 | 역할 저장·재시작 예제, records 보존, 주장 전달, retrieval의 그래프별 색인 키, 모듈 계약을 함께 실행한다. 리모트 색인 키 테스트는 claims만 지워 기존 edges와 불일치하는 입력을 만든다. 로컬 검사는 같은 원문에서 빈 주장을 가진 유효한 그래프를 새로 구성한다. |

리모트 커밋의 임시 복사본에 위 구현과 예제를 적용했다. 리모트 테스트 입력을 그대로 두면 관련 검사 83개 통과, 그래프 연결 검증 1개 실패였다. 로컬의 유효한 그래프 생성 방식까지 반영하면 같은 84개 검사가 모두 통과했다. 모델을 새로 호출하지 않은 로컬 통합 검사다. 팀 wheel의 SHA-256도 배포 매니페스트와 일치했다.
