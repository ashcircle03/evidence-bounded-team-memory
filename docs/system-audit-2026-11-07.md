# 구현·개발·평가 전체 흐름 감사

이 문서는 수정 전 감사 기록이다. 후속 구현·검증은
[service-v2 결과](../results/service-v2/README.md)를 확인한다.

2026-11-07. 현재 작업 트리를 대상으로 한 로컬 감사다. 서버의 실시간 상태,
새 모델 추론, 실제 원격 CI 실행은 포함하지 않았다. 기존 코드·동결 입력·채점·
실험 결과는 수정하지 않았다. 아래는 제품 완성 여부를 판단하기 위한 범위 감사이며,
모든 코드 줄이나 가능한 입력을 완전 검증했다는 뜻은 아니다.

## 결론

부품별 성과는 있지만, 지원하는 하나의 팀 메모리 시스템으로 연결됐다는 증거는
아직 부족하다. 특히 **QA 독해 개선, Git 상태 처리, 실제 서비스가 서로 다른 경로에
존재한다.** 특정 경로의 회귀 성공을 다른 경로 또는 전체 시스템의 성공으로 옮겨
해석하면 안 된다. 새 독해 단계를 추가하기보다 지원 경로와 경계 계약을 먼저
확정하고, 이미 있는 구현을 연결하는 것이 우선이다.

## 이번에 직접 실행한 검증

- `.venv/bin/python -m unittest discover -s tests -v`: 278개 중 277개 통과,
  1개는 샌드박스의 localhost bind 금지로 오류. skip 없음.
- 해당 `tests.test_contextual_transport` 1개만 허용된 실행 환경에서 재실행하여 통과.
  전체를 한 번에 통과했다고 기록하지 않는다. 새 GPU·유료 API 호출은 없다.
- [재현 스크립트](../results/audit-2026-11-07/probes.py)와
  [실제 출력](../results/audit-2026-11-07/probes.json): 아래 5개 경계 확인.
  모델은 stub이며 의미 성능을 측정한 실험이 아니다. 임시 디렉터리만 사용한다.

| 항목 | 직접 관찰 | 분류와 영향 범위 |
|---|---|---|
| 날짜 전달 | source에는 날짜가 있지만 `ReferenceQA._witness` 반환과 documents의 recorded_at은 누락/null | 재현된 메타데이터 전달 결함. 기존 고정 평가 입력에는 날짜가 있었으므로 그 입력까지 잘못됐다는 주장은 아님 |
| 시간순 정렬 | 09:00+09:00(00:00 UTC)이 01:00+00:00보다 뒤에 배치됨 | 재현된 정렬 결함. `reference_documents.documents`는 aware datetime을 문자열로 정렬. native 데이터의 미상 시간대에 UTC를 임의 부여하는 것으로 고쳐서는 안 됨 |
| 원문 보존 | 입력 `"  Fact\n"`이 `"Fact"`로 저장되고 Fact 시작 위치가 2→0 | 재현된 정규화 동작/계약 한계. 저장된 원문 내부 offset 검증은 유효하지만 외부 원문 바이트/위치 보존은 아님. 모든 기존 인용이 틀렸다는 뜻은 아님 |
| 답 보존 | 10[1]을 999[1][2]로 바꾸는 stub도 accepted=True, status=ok | 재현된 보호 범위 한계. ID 포함 검사로 값·주체·조건 보존은 보장하지 못함. 코드도 semantic verifier가 아니라고 명시 |
| practical의 병렬 기록 합치기 | 독립 디렉터리 두 곳의 ingest는 각각 ok. JSON 파일을 합친 뒤 rebuild는 ValueError | 문서상 미지원 흐름을 재현. 양쪽 ordinal=0의 intake/batch 정렬 불일치. 실제 Git 명령이 아니라 충돌 없는 파일 합집합을 모의한 것. 단일 소유자 서비스의 회귀 결함으로 분류하지 않음 |

## 전체 검토 범위와 판단

아래 표는 새 결함과 이전 두 감사의 확인 사항을 합친 것이다. 우선순위 P0은
현재 개발 판단/제품 연결을 막는 항목, P1은 이후 성능 비교를 신뢰하기 위한 항목이다.

| 영역 | 확인한 상태 | 필요한 조치 / 완료 증거 |
|---|---|---|
| P0. 문제·제품 범위 | 원 요구는 각자 기록을 쌓고 공유한 뒤 재검토·QA. practical 문서는 단일 프로세스 소유/원격 Git 병합 미구현을 명시 | QA reader 완성과 팀 시스템 완성을 분리. 기존 timeline Git 경로와 서비스 중 어떤 경로를 지원할지 하나로 명시하고 실제 공개 API로 연결 검사 |
| P0. 진입점·배포 대상 | decision은 attributed, reference CLI 기본은 standard, practical 예제는 simple, 최신 documents는 별도 reader | 지원 명령·profile·모델·schema·revision을 고정한 실행 명세 하나. 과거 실험은 재현 경로로 보존 |
| P0. 원문·출처 계약 | 원문 앞뒤 strip, 반환 witness 날짜 누락. 작성자/위치/ID/offset 검사는 존재 | 원본과 검색용 표현 구분, 원본 기준 offset 유지, 날짜/작성자/조건/검토 상태의 필수 전달 경계 명시. 상태는 별도 관계로 관리하되 QA 입력까지 도달해야 함 |
| P0. 갱신·시간 | Store timestamp는 UTC 정규화. 별도 documents reader의 aware 시간은 문자열 순서. 시간대 미상 자료도 수용 | aware끼리는 실제 시각 비교, 미상 시간대는 확정 순서로 가장하지 않는 정책. 같은 사실의 정정과 조건별 공존을 분리 |
| P0. 생성·보강·검증 | 예외 fallback과 source-ID 보존은 있지만 내용의 보존을 보장하지 않음. `status=ok`도 의미 정답 인증이 아님 | 원답/추가 주장/대체 주장을 구분. 원답을 바꾸지 않는 보강부터 사용하고 대체는 명시적 결과로 노출. 또 다른 미검증 LLM gate를 자동 추가하지 않음 |
| P0. 상태·Git·복구 | immutable 파일, owner 일치 확인, 상충 투표 보존, assertion 단위 정정과 timeline 두 clone 재생 테스트 통과. practical Git 합치기는 미지원 | 검증된 timeline 동작을 실제 지원 경로에서 재사용. ingest→제안→승인/거절→재시작→QA를 같은 서비스로 검증. actor 문자열 확인과 호출자 신원 확인은 다른 책임이며 후자는 팀원의 연결 계층과 계약 필요 |
| P1. 검색·문맥 | 최신 reader 실험은 준비된 witness 입력. 검색/적재/최종 독해를 모두 측정한 것은 아님. 전체 문서 확장 시 문맥 초과가 알려진 제한 | 실제 검색 결과 기준으로 근거 없음/부분/충분을 구분하고 필요한 근거의 경계 손실을 측정. 전체 파이프라인 결과와 reader-only 결과를 구분 |
| P1. 레퍼런스 연결 | upstream commit·NOTICE·라이선스 및 수정 설명 보존. 모델/예시/출력 단위/문단 단위가 달라 원 효과의 자동 이전은 성립하지 않음 | 원문제→필수 가정→재사용 부분→변경 부분→이 모듈이 다음 모듈에 보장하는 것의 짧은 연결표. 원구현과 비교 가능한 계산/포맷에는 작은 동일입력 대조 |
| P1. 데이터·독립성 | legacy20/Ever10은 반복 노출된 개발 회귀. 최신80출력은 독립80문항이 아님. Wiki253·Ever전체·재검토 파생셋 완수로 해석 불가 | 노출 자료는 회귀, 새 사건/대화 흐름은 holdout. 같은 사건의 순서/모델/문맥 변형은 같은 묶음으로 계산. 이미 본 최종셋은 새 판단에서 미공개 holdout으로 부르지 않음 |
| P1. 정답·채점 | 답+인용+필수근거+불필요정보+상태의 결합점수, 인용 개수 제한, 질문 전제의 인정 여부가 결과에 영향. 구현자가 채점 | 원 벤치마크 답 점수와 제품의 근거·상태 점수를 분리. 경계 사례 기준을 먼저 확정하고 일부를 독립 검토. 근거 위치 일치와 의미 지지를 구분 |
| P1. 비교·모델 | 과거 selected20/20과 새 엄격 평가의 fresh 후보는 동등 비교 아님. 현재 Qwen3-8B nonthinking 한 설정은 모델 능력의 상한 증거 아님 | 동일 입력·현재 채점·같은 backend의 fresh 기준선. 정확한 근거를 준 작은 calibration으로 모델/검색/설계 병목을 분리한 뒤 모델 선택 |
| P1. 환경·CI | 과거 reference-env와 extra 경로를 합친 client, 별도 conda model server. 현재 workflow에는 새 reference 의존성 설치 없음 | client/server 각각 실제 interpreter·import 경로·의존성·모델 revision 보존. 깨끗한 설치에서 core/reference 테스트 실행. 이번 로컬 통과는 원격 CI 성공이 아님 |
| P1. 실행·비용 | dispatcher의 lock, intent, 중복 version 차단, 실제 job ID 선저장, 사용자 queue/GPU 확인이 존재. 12시간 walltime 정책 반영. 비용은 주로 전체 작업+arm token | 기존 안전장치 유지. 색인/준비/질의 비용 구분, cold/warm 및 고정 실행 순서 영향 명시. 이번 감사는 live scheduler/분산 동시 제출의 완전성 검증은 하지 않음 |
| P0. 개발 판단·완료 표시 | progress의 최신 job120296과 과거 job119960·20점·remaining0·full_task_completed가 혼재. 많은 최신 파일이 아직 untracked | 결과마다 모델/코드/입력/평가기준/범위 식별. 실행완료·채점완료·채택·실제 서비스 연결을 분리. 실패한 가설의 적용 조건과 재검토 조건 보존 |
| P1. 테스트 해석 | 278개 테스트의 최종 개별 결과는 통과. 다수는 stub·저장 응답 재생·구조 검사 | 모델 정답률과 합치지 않음. 실제 진입점의 작은 통합 검사, 클린 설치, 미노출 의미 평가가 각각 다른 증거임을 유지 |

## 유지할 부분

전면 폐기할 상황은 아니다. source hash/정확한 quote·offset 검증, immutable 객체,
실패 시 원문 보존, 검토 승인과 관측 진실성의 분리, 상충 투표 보존, 실제 모델
입출력과 Slurm ID 보존, frozen 결과 재생은 이미 구현·테스트된 기반이다.
특히 `tests/test_timeline.py`와 `test_timeline_git.py`가 확인하는 범위를 새 서비스에
연결하면 된다. 새 상태 엔진이나 새 평가 프레임워크를 만들 필요는 없다.

## 수정 및 검증 순서

1. **지원 경로와 원문 계약**: 한 진입점에서 원본·작성자·시각·인용·관계 상태가
   끝까지 유지되게 하고, 날짜 전달/정렬/원본 위치를 먼저 수정한다. 기존 파일은
   해시 주소이므로 소급 덮어쓰기 대신 버전/이행 방침이 필요하다.
2. **실제 흐름 연결**: 같은 경로에서 적재→QA→새 보고→재검토 제안→원 작성자
   승인/거절→재시작→QA 및 독립 기록 합치기를 확인한다. 의미 판단은 저장 출력
   재생으로 기계적 연결부터 확인하고, 실제 모델 성공과 구분한다. 모듈을 없애는
   기준은 파일 수가 아니라 중복 호출/상태/판단을 줄이면서 책임을 유지하는지다.
3. **동일 조건 비교**: 깨끗한 실행 환경과 채점 기준을 확정한 뒤, 기존20/Ever10은
   회귀로 사용하고 새 흐름은 별도 holdout에서 단순 기준선과 비교한다. QA와
   재검토의 이득·손실을 따로 보고, 비용 증가에 상응하는 이점이 없는 단계는 제외한다.

이번에는 감사 자료만 추가했다. 새 모델·GPU 작업, frozen 코드 수정, 기존 점수 수정,
원격 게시를 하지 않았다. 독립 사람 채점, 미노출 일반화, 실제 클린 서버 설치 및
종단간 모델 실행은 후속 검증으로 남아 있다.

## 근거 자료

- [평가·모델 감사](evaluation-model-audit-2026-11-07.md)
- [개발 프로세스 감사](development-process-audit-2026-11-07.md)
- [평가 약속과 현재 범위](evaluation-coverage.md)
- [practical 사용법과 명시적 제한](practical-usage.md)
- [검증 요약](../results/audit-2026-11-07/verification.json)
- 구현: `team_memory/store.py`, `reference_qa.py`, `reference_documents.py`,
  `reference_attributed.py`, `timeline.py`, `cupmem_service.py`, `cupmem_practical.py`.
- 실행: `.github/workflows/tests.yml`, `requirements-reference.txt`,
  `evaluation/timeline/dispatch.py`, `evaluation/cupmem/dispatch.py`.
