# 문항별 판단 · 작업 119269

같은 행의 두 출력은 같은 질문 또는 새 기록에 대한 것이다. 각 칸은 검증을 거쳐 사용자에게 전달한 결과다. ✓는 답과 근거 또는 재검토 대상·근거·조치의 결합 정답이다. 원출력을 볼 때는 표의 ID와 조건, 방식 이름을 함께 사용한다. [모델 원출력](outputs.json) · [실제 인용 구절, 출처와 판정 사유](review-cards.json)

## QA

| 문항 | 조건 | 단순 검색 | 후보 모듈 |
|---|---|---|---|
| [pep-680](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0680.rst#L19) | 원본 | ✗ 인용 오류 | ✓ tomllib |
| [pep-680](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0680.rst#L19) | 무관한 충돌 | ✗ 인용 오류 | ✓ tomllib |
| [pep-680](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0680.rst#L19) | 답이 갈리는 충돌 | ✗ 인용 오류 | ✗ tomlreader |
| [pep-615](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0615.rst#L21) | 원본 | ✓ tzdata | ✓ tzdata |
| [pep-615](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0615.rst#L21) | 무관한 충돌 | ✓ tzdata | ✓ tzdata |
| [pep-615](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0615.rst#L21) | 답이 갈리는 충돌 | ✗ zonefiles | ✗ tzdata |
| [pep-515](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0515.rst#L40) | 원본 | ✗ 인용 오류 | ✗ 인용 오류 |
| [pep-515](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0515.rst#L40) | 무관한 충돌 | ✗ 인용 오류 | ✗ 인용 오류 |
| [pep-515](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0515.rst#L40) | 답이 갈리는 충돌 | ✗ 인용 오류 | ✗ 인용 오류 |
| [pep-572](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst#L18) | 원본 | ✓ NAME := expr | ✓ NAME := expr |
| [pep-572](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst#L18) | 무관한 충돌 | ✓ NAME := expr | ✓ NAME := expr |
| [pep-572](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst#L18) | 답이 갈리는 충돌 | ✗ NAME := expr | ✗ NAME := expr |
| [pep-597](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0597.rst#L13) | 원본 | ✓ EncodingWarning | ✗ 인용 오류 |
| [pep-597](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0597.rst#L13) | 무관한 충돌 | ✓ EncodingWarning | ✗ 인용 오류 |
| [pep-597](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0597.rst#L13) | 답이 갈리는 충돌 | ✗ LocaleDefaultWarning | ✗ 인용 오류 |
| [pep-618](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst#L18) | 원본 | ✗ 인용 오류 | ✓ ValueError |
| [pep-618](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst#L18) | 무관한 충돌 | ✗ 인용 오류 | ✓ ValueError |
| [pep-618](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst#L18) | 답이 갈리는 충돌 | ✗ LengthMismatchError | ✗ 인용 오류 |
| [pep-669](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0669.rst#L28) | 원본 | ✓ sys.monitoring | ✓ sys.monitoring |
| [pep-669](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0669.rst#L28) | 무관한 충돌 | ✓ sys.monitoring | ✓ sys.monitoring |
| [pep-669](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0669.rst#L28) | 답이 갈리는 충돌 | ✗ sys.events | ✗ sys.monitoring |
| [pep-654](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0654.rst#L29) | 원본 | ✓ the except* syntax | ✗ ExceptionGroup |
| [pep-654](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0654.rst#L29) | 무관한 충돌 | ✓ the except* syntax | ✗ ExceptionGroup |
| [pep-654](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0654.rst#L29) | 답이 갈리는 충돌 | ✗ catch* | ✗ ExceptionGroup / catch* |
| [pep-553](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0553.rst#L108) | 원본 | ✓ 0 | ✓ 0 |
| [pep-553](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0553.rst#L108) | 무관한 충돌 | ✓ 0 | ✓ 0 |
| [pep-553](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0553.rst#L108) | 답이 갈리는 충돌 | ✗ 0 | ✗ 인용 오류 |
| [pep-552](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0552.rst#L75) | 원본 | ✗ 인용 오류 | ✗ source_hash(source) |
| [pep-552](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0552.rst#L75) | 무관한 충돌 | ✗ 인용 오류 | ✗ source_hash(source) |
| [pep-552](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0552.rst#L75) | 답이 갈리는 충돌 | ✗ BLAKE2s | ✗ BLAKE2s |
| F_SH_Top01_013 | 기존 개발 문항 | ✗ 10 working days | ✗ 10 working days |
| F_SH_Top01_033 | 기존 개발 문항 | ✓ Lizhen Zhou | ✓ Lizhen Zhou |

## 재검토

비교는 재시험 제안, 재평가는 과거 제약이나 가정의 재검토를 뜻한다. 음성 사례에 대한 능동 제안은 오탐이다. 출력 형식이 잘못돼 조치가 전달되지 않으면 오탐 수에서는 제외하되 올바른 유지 판단으로도 세지 않는다. [20개 원기록과 사전 허용 조치](../../evaluation/team_pilot/cases.json)

| ID / 사안 | 허용 조치 | 단순 검색 | 후보 모듈 |
|---|---|---|---|
| review-01 / adaptive packing | 비교 | ✓ 비교 | ✓ 비교 |
| review-02 / invoice | 재평가 | ✗ 비교 | ✗ 비교 |
| review-03 / rebuild | 비교 또는 재평가 | ✓ 비교 | ✓ 비교 |
| review-04 / shoreline | 비교 또는 재평가 | ✓ 비교 | ✓ 비교 |
| review-05 / consent | 재평가 | ✗ 비교 | ✗ 비교 |
| review-06 / transliteration | 비교 | ✓ 비교 | ✓ 비교 |
| review-07 / crates | 비교 | ✓ 비교 | ✓ 비교 |
| review-08 / settlement | 재평가 | ✗ 비교 | ✗ 비교 |
| review-09 / checkpointing | 비교 | ✓ 비교 | ✓ 비교 |
| review-10 / controller | 비교 또는 재평가 | ✓ 비교 | ✓ 비교 |
| review-11 / telemetry | 유지 | ✗ 비교 | ✗ 비교 |
| review-12 / plate | 유지 | ✗ 비교 · 다른 결정 | ✗ 비교 · 다른 결정 |
| review-13 / survey | 유지 | ✗ 비교 | ✗ 비교 |
| review-14 / pool | 유지 | ✗ 비교 | ✗ 비교 |
| review-15 / sterilization | 유지 | ✗ 비교 | ✗ 비교 |
| review-16 / compiler | 유지 | ✗ 출력 형식 오류 | ✗ 비교 · 다른 결정 |
| review-17 / terraces | 유지 | ✗ 비교 | ✗ 비교 |
| review-18 / signing | 유지 | ✗ 비교 | ✗ 비교 |
| review-19 / incubation | 유지 | ✗ 비교 | ✗ 비교 |
| review-20 / bridge | 유지 | ✗ 비교 | ✗ 비교 |
