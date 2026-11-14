# storage — 원문과 불변 객체

| 파일 | 진입점 | 계약 |
|---|---|---|
| `sources.py` | `SourceStore`, `source_envelope` | owner·시간·speaker/location/text를 검증하고 입력 text를 그대로 보존 |
| `objects.py` | `Store`, `digest`, `encoded` | JSON의 결정적 직렬화·해시·원자적 기록·변경된 객체 탐지 |

`objects.py`는 역사적 데이터 해시가 가리키는 `../store.py`와 같은 구현 객체를 노출한다. 두 복사본을 유지하지 않는다. 과거 source 정규화 규칙과 새 정확한 원문 보존 계약을 혼동하지 않는다.

모델·검색기·승인 의미를 이 계층에 넣지 않는다. 저장 예외는 비교 오류로 바꿔 삼키지 않고 호출자에게 전달한다. 저장 형식을 바꾸면 기존 ID와 이력의 호환 정책을 함께 제공한다.

검사: `tests/test_source_reader.py`, `tests/test_team_memory.py`, `tests/test_module_layout.py`, 과거 해시 재현은 `tests/test_cupmem_legacy_inputs.py`.
