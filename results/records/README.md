# records 단독 검증 — 2026-11-15

**이 결과는 records의 저장 계층 검사이며, 멘토가 요구한 DB 지식 구성 품질은 아직 측정하지 않았다.** 실제 개발 자료의 무손실 저장, 합성 상태 흐름, 운영 오류, 속도, 기존 QA 보존을 분리해서 검사했다. 의미 추출·관계 분류 모델의 정확도를 측정한 결과는 아니다. 공개 v1.1 계약과 기존 v2 review 정책을 유지했다.

[설계·데이터셋·재현 방법](../../docs/modules/records-experiments.md) · [실제 구현](../../team_memory/adapters/records.py)

| 항목 | 결과 | 해석 범위 |
|---|---|---|
| 기존 데이터 기반 source 보존 | EverMem 528 + Git·PEP 245 = **773/773** | ID·text·owner·speaker·observed_at·location 각각 일치. upstream 전처리는 재검증하지 않음 |
| 합성 상태 흐름 | **46/46** | 네 이야기의 변형. relation은 oracle 입력. 독립 held-out 46건 아님 |
| 권한·정정 범위·snapshot 보존 | 합성 흐름의 해당 검사 모두 통과 | 승인된 재검토가 사실 교체로 승격되지 않음 |
| record 운영 검사 | **17개 통과** | IO 실패, commit 뒤 오류, 같은 key 재시도, 손상, cache invalidation, 동시 revision, legacy import 등 |
| 기존 QA 보존 | **20/20**, 정확히 일치하는 모델 요청 **130개** | 고정 근거의 기존 Qwen 응답 재생. 새 추론·새 검색 성능 아님 |

QA의 8문항에 남아 있던 미인용 구절 11개는 여전히 미인용으로 표시한다. 답변 보존을 완전한 주장별 인용 성공으로 바꾸어 보고하지 않는다.

## 무엇을 수정했나

1. 저장된 잘못된 JSON·digest·commit 구조·review actor를 검출한다. 손상을 사용자 입력 오류로 보고하거나 잘못된 vote를 조용히 무시하지 않는다.
2. 파일 생성 후 디렉터리도 동기화한다. 전체 commit이 보인 뒤 sync가 실패할 수 있으므로, 같은 key 재시도로 성공 여부를 확정한다. 이 경우 최초 실패 응답을 “아무것도 저장되지 않음”으로 해석하지 않는다.
3. 검증한 파일과 snapshot을 process-local 캐시로 재사용한다. 파일 목록·메타데이터를 매번 확인하며 off/on 결과와 다른 writer의 변경 반영을 검사한다.
4. review 시각을 찾을 때 proposal마다 전체 commit을 다시 훑던 작업을 한 번의 vote 인덱싱으로 바꿨다. v2 의미 판정·승인 정책·reader 프롬프트는 변경하지 않았다.

## 로컬 지연시간

짧은 합성 원문만 누적한 포트 전체 측정이다. validation과 전체 snapshot 반환을 포함하며, 읽기는 각 크기에서 10회, 쓰기는 마지막 10회를 집계한다.

| 누적 원문 | read median 수정 전 → 후 | append median 수정 전 → 후 |
|---|---:|---:|
| 10 | 2.39 → 1.82ms | 2.40 → 2.16ms |
| 100 | 13.68 → 7.92ms | 15.55 → 11.07ms |
| 300 | 37.73 → 23.18ms | 45.63 → 31.02ms |

300개에서 read median은 약 39%, append median은 약 32% 감소했다. 같은 호스트의 단일 before/after 측정이므로 일반적인 성능 향상률이나 통계적 유의성을 주장하지 않는다. cold reopen+read는 64.77 → 60.09ms였다. 저장 바이트는 같았다. 승인 관계가 많은 부하·큰 원문·대규모 저장소·분산 파일시스템은 별도 측정이 필요하다.

## 평가 과정에서 발견한 정답표 오류

초기 40개 합성 흐름 중 12개는 이미 승인/거절된 제안을 순차적으로 반전시키면 review_conflict가 된다고 잘못 가정했다. v2는 닫힌 review를 반전시키는 명령을 거절한다. 반면 Git의 기존 두 투표가 함께 import된 경우에는 review_conflict가 맞다.

초기 결과는 **28/40**이며 입력·출력을 삭제하지 않았다. 순차 명령의 기대값을 기존 정책에 맞게 수정하고 import 6개를 별도 추가한 결과가 46/46이다. 이것을 코드 변경으로 28→46 개선한 것으로 보고하지 않는다.

- [초기 입력](v1/cases-initial.json), [초기 결과](v1/quality-initial.json)
- [최종 합성 입력](../../evaluation/records/cases.json), [필드·사례별 결과](v1/quality.json)
- [수정 전 속도](v1/before.json), [수정 후 속도](v1/after.json)
- [기존 QA 보존](v1/qa-preservation/replay.json)
- [검증 manifest](v1/verification.json)

## 남은 범위

- 원문 보존과 추출 품질은 다르다. 구조화된 claim·조건·유효시간 추출은 records가 책임져야 하지만 현재 v1.1 API와 구현에 빠져 있다. 별도 span 정답과 모델 평가가 필요하다. 저장 테스트 통과로 이 공백을 대신하지 않는다.
- 인증은 trusted CallContext를 생성하는 transport의 책임이다. 파일 hash는 작성자 서명이 아니다.
- 새 module history가 Git에서 갈라지면 자동 병합하지 않고 멈춘다.
- read 캐시에도 O(N) 파일 확인·전체 snapshot 반환 비용이 남는다.
- 디렉터리 fsync와 장애 주입 검사는 실제 정전·커널 장애 내구성 검증을 대신하지 않는다.
- 추가 GPU 추론·새로운 EverMem QA 정확도 측정·학습은 수행하지 않았다.
