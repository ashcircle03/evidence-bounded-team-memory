# 공통 개발 예제

이 디렉터리는 **합성 입력과 사람이 정한 기대 응답**이다. 실측 모델 출력이나 성능 벤치마크가 아니다. [전체 계약](../../docs/modules/README.md).

`cases.json`의 사례 하나는 setup(snapshot), context(신뢰된 테스트 주체), request, response(고정 double), expect(JSON Pointer 단언), state_unchanged, retry_identically로 구성된다. 각 사례는 독립된 저장소를 사용한다. setup은 fixture를 seed하기 위한 개발 전용 기능이며 운영 API로 노출하지 않는다.

| 사례 묶음 | 확인할 연결 |
|---|---|
| records-read / append-idempotent / proposal-pending / owner-approval | 저장 → 제안 → 승인; 원문 보존·재시도 중복 방지 |
| unauthorized-review / stale-review | 작성자 권한·revision 거절, 실패 후 상태 불변 |
| relations-exact-correction / different-conditions / model-timeout | 좁은 정정·조건별 공존·실행 실패 분리 |
| retrieval-keeps-metadata-and-state / no-hits / failed | 원문·작성자·날짜·상태 전달, 검색 누락과 장애 분리 |
| answer-pending / approved / rejected | 현재값·제안값·담당자 유지 |
| answer-conflict / unrelated-conflict / reconsider | 양쪽 근거·무관한 상충·재검토 권한 제한 |
| answer-no-evidence | 근거 없는 답변의 보류 |
| gateway-read-only / unauthorized-review / ingest-failure | 읽기/쓰기 분리, 원문 commit 이후 비교 실패의 partial |

실행:

```sh
python -m pip install -e '.[dev]'
python -m team_memory.contracts.conformance examples/contracts/cases.json
python -m pytest -q tests/test_module_contracts.py
```

fixture-only 실행에서 사용하는 `FixturePort`는 기대 응답을 반환하는 double이다. 실제 adapter 테스트에서는 자기 구현을 넣는다. 최소 factory 구조는 다음과 같다(자기 프로젝트의 import와 생성자로 바꾼다).

```python
from team_memory.contracts.conformance import Subject

def make_subject(case):
    # 테스트 전용 DB; 운영 저장소를 seed하거나 덮어쓰지 않는다.
    store = make_isolated_store()
    store.seed_snapshot(case['setup']['snapshot'])
    # 모델은 deterministic stub, 어댑터와 저장/상태 처리는 실제 구현.
    port = make_my_adapter(store=store, model=make_model_stub(case))
    return Subject(port=port, observe_state=store.export_snapshot)
```

```sh
python -m team_memory.contracts.conformance examples/contracts/cases.json \
  --module answering --factory my_tests.factories:make_subject
```

`observe_state`는 실제 저장 결과를 읽어야 한다. 테스트 기대 response를 그대로 반환하는 port나 고정 state observer로 adapter 완료를 주장하지 않는다. 입력 deep-copy 보호, snapshot 참조, 메타데이터, claim 인용, 상태 쓰기, 동일 요청 재시도를 검사한다. JSON Pointer 단언은 문구까지 고정한 stub 회귀용이며 실제 LLM의 의미 동등 답변을 채점하는 도구가 아니다.

예제 변경 시 `build_examples.py`의 합성 사례와 기대 결과를 먼저 수정하고 `python examples/contracts/build_examples.py`로 JSON을 생성한다. 스키마/예제 drift를 CI가 검사한다. 정답 파일은 운영 모듈이나 모델 프롬프트에서 읽지 않는다.
