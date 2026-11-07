# 2026-11-08 공개 업데이트 검증

전체 진행 내용의 공개 요청에 따라 현재 코드, 기존에 미게시된 후보·평가·실패 기록, 최신 비교와 상세 설명을 한 저장소에 연결했다. 새로운 GPU/모델 실험은 수행하지 않았다.

## 공개한 내용

- 현재 상태 중심으로 루트 README를 다시 구성했다. [문제/전체 연구 이력](../../docs/research-history.md), [설계/레퍼런스 연결](../../docs/current-design.md), [평가/재현](../../docs/evaluation-guide.md), [문서 지도](../../docs/INDEX.md), [결과 지도](../README.md)를 추가했다.
- 이전 README의 상세 설명을 [보존본](../../docs/history-overview-2026-11-08.md)으로 남겼다. 과거 완료 기록·동결 결과의 의미를 소급 변경하지 않았다.
- 최신 job120370 제출 묶음14개와 동결 actor/evaluator archive를 공개했다. [검증 JSON](verification.json)의 해시 검사와80개 코드 일치를 확인했다.
- 팀 코드의 라이선스는 보류 상태를 유지했다. vendor LICENSE/NOTICE를 공개하며 배포 패키지에도 LICENSE를 포함하도록 CI 묶음 구성을 맞췄다.

## 검사 결과

- 전체 discover272개에서270개 통과, 공식 CUPMem 소스가 없던2개 모듈 skip. 공식 pinned source를 준비한 뒤 그2개 모듈의21개 검사를 모두 통과했다. **서로 다른 실제 검사291개 성공**이며 한 번에291개 실행한 로그로 표시하지 않는다.
- 격리 배포 묶음의13개 계약 검사 통과.
- 저장 결과 복사본에서 최신 구조 검증·블라인드 카드·mapping·판정 집계를 재생해 공개 결과와 일치했다. 새 의미 평가나 새 모델 호출이 아니다.
- 문서의 로컬 링크와 공개 파일/압축 내부의 자격증명 패턴을 검사했다. 상세 수는 [verification.json](verification.json)을 따른다. 패턴 검사가 모든 비밀정보 부재의 증명은 아니다.
- 과거 실패 자료 `results/cupmem/practical/legacy-pep-v1/native.jsonl.gz`는 끝이 잘린 gzip이다. 읽을 수 있는 부분을 검사했으며 원본을 수정하거나 완전한 로그라고 표시하지 않았다. 이 파일은 최신 비교의 입력이 아니다.
- 과거 원출력·원문 발췌·vendor 원본에는 trailing whitespace가 있다. 바이트/해시 보존을 위해 정리하지 않았다. 신규 설명 문서·현재 프로젝트 코드의 공백 검사는 별도로 수행했다.

[전체 로그](unit-tests.log) · [CUPMem 추가 검사](cupmem-tests.log) · [격리 패키지](package-tests.log) · [검사/환경 요약](tests.json).

이 문서는 커밋 전 로컬 검증 기록이다. 게시 커밋과 GitHub CI 상태는 저장소 커밋 이력과 [Actions](https://github.com/ashcircle03/evidence-bounded-team-memory/actions/workflows/tests.yml)에서 확인한다. 기존 service-v3 completion.json의 code_pushed/remote_ci_run은 당시 완료 시점의 기록을 유지한다.
