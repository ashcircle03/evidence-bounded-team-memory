# Records 개발 안내

기록이 들어올 때 원문과 출처를 보존하고 주장마다 원문 구절·조건·이유·상태를 연결한다. 기록에서 추출한 상태는 원 작성자의 승인 이벤트와 별도로 관리한다.

재현용 후보 구현도 이 디렉터리에 있다. 서비스 연결에는 아래 진입점을 사용한다. [후보 파일별 상태와 실험 결과](../../docs/modules/records-experiments.md)에서 채택 범위를 확인할 수 있다.

## 팀원이 연결할 경로

기본 서비스 구성에서 원문 저장은 항상 가능하다. 구조화하려면 `connect_v2`에 아래 생성기를 전달한다. `generate(system, prompt)`는 호출자가 제공하는 모델 클라이언트이며, 클라이언트에 `grouped.writer_kwargs(basis_types=True)`의 출력 설정을 적용한다.

```python
from functools import partial
from team_memory.adapters.runtime import connect_v2
from team_memory.records import preserving

record_builder = partial(preserving.construct, generate=generate, model=model_id)
gateway = connect_v2(
    root, workspace_id=workspace_id, reader_factory=reader_factory,
    generate=generate, record_builder=record_builder,
)
```

| 작업 | 수정하거나 확인할 코드 |
|---|---|
| 추출 예시·원문 정렬 | [grouped.py](grouped.py) |
| 개별 주장의 상태 보존·정렬 실패 처리 | [preserving.py](preserving.py) |
| 그래프 형식·출처 검증·reader에 보이는 구절 | [graph.py](graph.py) |
| 이미 한 주장에 연결된 구절의 역할 보정 | [discourse_roles.py](discourse_roles.py), [discourse_scope.py](discourse_scope.py) |
| 정책 대상 명사구의 제한절을 적용 조건으로 연결 | [policy_scope.py](policy_scope.py) |
| 명시적 대상 구절을 가진 실험 v4 그래프 호환 | [pair_binding.py](pair_binding.py) |

기본 추출과 역할 보정은 모두 `preserving.construct`를 사용한다. 역할 보정을 켜려면 같은 함수에 `predict=predict, training_counts=training_counts, parse=parse`를 전달한다. 이전 `discourse_roles.construct`, `discourse_scope.construct`, `policy_scope.construct`도 이 경로를 호출한다. 각 추출 행의 원문 위치를 한 번 정렬한 뒤 같은 위치로 후보와 저장 그래프를 구성한다. 역할이 바뀌면 해당 주장 그룹의 필드와 그래프 연결을 갱신한다. `predict`는 후보 순서대로 keep/condition/basis를 반환하고, `training_counts`는 학습에 관측된 구절 위치 관계별 빈도다. `parse`는 영어 의존 구문 분석 callback이다. 측정에는 spaCy 3.7.5와 en_core_web_sm 3.7.1을 사용했다. 학습 체크포인트와 비공개 실행 경로는 릴리스에 포함하지 않았다. 추출 구절의 원문 일치, 모델 판단, 검토 승인은 각각 별개다.

## v0.2.0의 평가 범위

고정 Qwen 원출력에 직전 역할 보정과 새 정책 적용 범위 처리를 각각 적용했다. 합성 54문서는 정답 연결 40개·오연결 13개, 자연 14문서는 정답 10→11개·오연결 7→6개였다. 기존 정답 50개가 모두 유지됐고 새 오연결은 0개였다. n08에서 올바른 정책 조건이 추가됐지만 인사말 추출이 남아 자연 기록 전체 정답 문서는 0개다. 새 문서·최종 QA 성능은 이 비교에서 측정하지 않았다. [문서별 결과](../../results/records/v0.2.0.csv)

`.[reference,dev]` 및 NLTK punkt_tab·stopwords를 준비한 뒤 저장소 루트에서 실행한다.

```bash
python -m pytest -q tests/test_record_preservation.py tests/test_discourse_roles.py tests/test_discourse_scope.py
```

구문 분석 모델이 있는 Python 환경에서는 `python -m evaluation.record_binding.discourse.check_policy_scope`로 RFC 5049 예시와 여섯 대조 사례를 확인한다.

### v0.2.1 검증 결과

동일한 68개 입력으로 태그의 policy_scope.construct와 통합된 preserving.construct를 각각 실행했다. 저장 후 다시 읽은 records 전체, reader에 전달한 근거 묶음 192개, 문서별 정답 연결 51개와 오연결 19개의 식별자가 일치했다. LangExtract 정렬에 전달된 추출 행은 1,431→294개, 원문에서 그래프 단위를 만들기 위한 문장 분할은 136→68회였다. 고정 모델 출력을 재사용한 구조 회귀 검사다. 최종 QA 응답 생성은 이번 검증 범위 밖이다. [문서별 비교표](../../results/records/v0.2.1.csv)에서 before는 v0.2.0, after는 v0.2.1이다. 각 SHA-256 열은 문서별로 정렬한 정답·오연결 식별자, 저장 기록 전체 또는 reader에 전달된 근거 묶음을 비교한다.

### 표와 동작별 자연어 추출

`preserving.construct`는 헤더와 구분 행이 있는 파이프 표의 데이터 행을 읽어
`record_graph.layout`에 저장한다. 한 행의 `cells[i]`는 `headers[i]`와 짝이고,
행과 각 구절은 원문 기준 반개구간 [start, end)를 갖는다. 열 순서만으로
subject나 condition을 만들지 않는다. 기존 v3 결과에는 `layout.with_layout(record)`으로
원본을 수정하지 않고 좌표를 갖춘 사본을 얻는다. 기존 의미 연결 ID와 오류 이력도 보존한다.

자연어에서 그룹 하나는 하나의 동작 또는 보고된 결과다. 같은 그룹 안에서 다음 질문을 적용한다.

| 질문 | 저장 규칙 |
|---|---|
| 누가 무엇을 했나? | 명시된 행위자가 드러나는 claim 원문을 선택한다. 별도 actor 필드는 없다. 문서 작성자를 행위자로 채우지 않는다. |
| 무엇에 한 동작인가? | 변경·승인·측정된 대상의 원문을 같은 그룹의 subject로 연결한다. 대상과 행위자가 다르면 구별한다. |
| 어떤 상황에서 적용되나? | 그 동작에 명시된 전제나 제한 구절을 condition으로 붙인다. 이유가 명시되면 basis로 구분한다. |
| 원문으로 특정할 수 있나? | 대상이 생략됐거나 앞 문장의 지시 대상이 모호하면 연결을 비운다. 인용은 원문 좌표를 따른다. |

예를 들어 “운영위가 문서를 승인했다”에서 행위자는 운영위이고 대상은 문서다.
“승인을 받으면 배포한다”에서는 배포가 동작이고 승인을 받는 것이 조건이다.
두 번째 문장에는 배포 주체가 없다. QA-SRL의 술어별 질문 방식을 차용한 계약이다.
기존 모델 출력의 재생으로 새 지시문의 생성 품질을 측정할 수는 없다.
