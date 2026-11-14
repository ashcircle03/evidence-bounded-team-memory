# review — 관계 제안과 작성자 검토

| 파일 | 입력 → 출력 | 책임 |
|---|---|---|
| `comparison.py` | 원문·문장 ID·주입된 generate → 관계 후보 JSON | 기존 비교 프롬프트, 정확한 문장/구절 결합, 후보별 선택 오류 |
| `state.py` | 원문·후보·작성자 투표 → 제안·유효 상태 | `ingest`, `proposals`, `review`, `valid_witness`, `assertion_status`, receipt |
| `policy.py` | 고정 정책 문자열 | 시간·정정·재검토 의미를 공유하는 기존 문구 |
| `cli.py` | CLI/새 source 목록 → 처리 결과 | 기존 timeline CLI와 `process_sources`; 자동 실행하지 않음 |

`comparison`은 의미 관계를 제안한다. 원문 ID와 offset이 존재한다고 관계가 옳아지는 것은 아니다. `state`는 원문 구절과 투표를 검증하고 상태를 계산한다. 이 둘의 오류를 구분한다.

- 정정 승인은 지정한 주장에만 적용한다.
- 재검토 승인은 다시 살펴볼 권한이다. 과거 사실 대체·새 실험 성공·자동 계획 변경을 뜻하지 않는다.
- 조건이 다른 공존은 자동으로 승인 요청을 만들지 않는다.
- 비교 실패와 관계 없음은 다르다. 실패 receipt를 보존하고 원문은 계속 읽을 수 있다.
- actor 문자열의 일치는 사용자 인증을 대신하지 않는다. 인증은 호출자의 책임이다.

의존성: 불변 저장 계층. 문장 구분은 NLTK, 모델은 호출자 주입. `readers`나 service의 상태를 역으로 수정하지 않는다.

검사: `test_timeline.py`, `test_timeline_git.py`, `test_comparison_contract.py`. 모델 분류 정확도는 `evaluation/`의 고정 실행으로 따로 측정한다.
