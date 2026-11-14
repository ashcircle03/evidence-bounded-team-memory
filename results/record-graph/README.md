# records 구성·전달 진단

2026-11-15. [설계·실제 실패·레퍼런스 연결](../../docs/modules/records-graph.md).

이번 작업은 이전의 저장 테스트를 지식 구성 성능으로 보고한 문제를 바로잡는다.
원문에서 자동으로 구성한 주장 후보·조건·이유·시간·대상 연결을 실제 모델로
진단하고, raw source QA와 비교한다. **자동 의미 품질 만점은 주장하지 않는다.**

## 구현 범위

- v1.2 선택적 `source.record_graph`; 원문은 보존, 추출은 미검증 annotation.
- LlamaIndex sentence/window 구현 직접 실행. JSON adjacency list이며 graph DB 없음.
- 원문/메타데이터 → graph → 실제 저장/재시작 → 비교 입력 → retrieval bundle → QA 모델 입력 연결.
- 실패한 추출, 배정하지 못한 문장, 검증되지 않은 완전성을 명시한다.
- graph는 review 이벤트가 아니며 작성자 승인을 만들거나 원문을 자동 무효화하지 않는다.
- raw 경로가 기본값이다. 실제 의미 평가 전 linked를 운영 기본으로 채택하지 않는다.

## 고정한 진단

[입력](../../evaluation/record_graph/inputs.json), [provisional key](../../evaluation/record_graph/key.json),
[프로토콜](../../evaluation/record_graph/PROTOCOL.md), [동결 파일](v1/freeze.json).

5개 EverMem 기존 실패 family의14개 decisive 메시지 +4개 합성 대비의8개 메시지,
총22개 source를 질문 없이 먼저 구성한다. 이후9개 질문의 raw/linked QA를 같은
Qwen3-8B와 같은 원문 근거로 실행한다. 새로운 검색 성능이나 unseen test가 아니다.
정답 키는 서버에 보내지 않는다. provisional key는 구현 담당 AI의 진단 주석이며
독립적인 사람의 검토를 받은 gold가 아니다.

**전달 형식의 교란 요인:** 두 arm의 bundle에는 같은 작성자·시간·location이 있지만,
기존 raw reader가 실제 prompt에 넣던 헤더는 author/time이다. linked의 record_context는
location과 추출 상태도 전달한다. 따라서 차이가 나더라도 graph 역할 연결만의 효과로
분리할 수 없다. 이번은 기록 표현과 전달 경로 전체의 진단이다. 최초 프로토콜의
“동일 메타데이터”는 bundle 기준이며 실제 모델 prompt까지 동일하다는 뜻으로 쓰면
부정확하다. 이 제한을 새 모델 결과를 보기 전에 기록했다. 입력·프롬프트·정답은 변경하지 않았다.

## 실행과 결과

- Slurm122842, GPU1/CPU8/48G,12h walltime, conda, aurora-g8의 기존 NLTK와 공유 checkpoint 재사용.
- 실제 client는60분/300호출 상한. 유료 API와 새 데이터·모델 다운로드 없음.
- [실제 제출 장부](v1/dispatch.json). 완료/종료코드와 입력 hash를 확인한 뒤 결과를 확정한다.
- [기존 QA20 재생](v1/qa-preservation/replay.json):20/20 답·근거 보존,130개 정확한 요청 일치. 새 QA 정확도가 아니다.
- [모델 실행 전 문맥 진단](v1/offline-probes.json): reference window의 전달 범위만 검사.22개 의미 추출은 not_run이며 이를 성능 점수로 세지 않는다.

구조 검사에서 정확한 원문 ID를 연결해도 역할을 틀리게 지정한 반례는 통과할 수 있다.
전용 테스트는 이 반례를 구조 성공으로 남기고 별도 의미 요구사항 검사에서 실패함을 확인한다.
따라서 테스트 개수·문자열 존재·graph edge 무결성을 semantic precision으로 보고하지 않는다.

새 모델 결과의 claim/조건 연결, 상태 혼동, QA 답·근거는 원문에 대조해 따로 판정한다.
