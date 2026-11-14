# 구현 안내

현재 서비스 개발은 아래 경로에서 시작한다.

| 경로 | 역할 |
|---|---|
| [service.py](service.py) | 공개 JSONL API와 전체 흐름 조정 |
| [storage/](storage/) | 불변 원문과 객체 저장 |
| [review/](review/) | 관계 후보·근거 구절·작성자 검토 상태 |
| [readers/](readers/) | 검색·QA·상태 문맥·인용 |
| [experiments/](experiments/) | 명시적으로 선택하는 실험 후보 |
| [_vendor/](_vendor/) | 실제 재사용한 원본과 라이선스 |
| [packaging.py](packaging.py) | 새 실행에 필요한 전체 source packet 구성 |

루트의 `reference_*`, `timeline`, `source_store` 등은 이전 import/CLI를 위한 호환 진입점이다. 새 로직을 넣는 위치가 아니다. `store.py`는 과거 데이터 manifest의 해시 기준을 보존한 원본이다.

초기 harness·CUPMem·workbench 파일도 재현을 위해 남아 있다. 현재 서비스가 이들을 모두 실행하지는 않는다. [모듈 의존성·경로 대응](../docs/architecture.md)과 [연구 이력](../docs/research-history.md)을 따른다.
