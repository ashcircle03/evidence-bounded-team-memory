# Connected QA 고정 개발 비교

실행 전 고정. 기존 contextual-v1의 inputs.json을 바이트 그대로 재사용한다.
EverMem topic01/02 10문항과 기존20문항; Q/A/R 및 정답 기준을 변경하지 않는다.
원문은 pinned EverMem 리비전 a6b210a32248e841967b7b64a64281d2ff3f669d.

## 비교

- legacy20: 새 connected 독해. 기존에 고정한 검색 입력이며 전체 검색 회귀는 아님.
- Ever10 joint: 기존 단순 reader를 원래 top8에서 새 추론. 별도 선택/보정 없음.
- Ever10 reader_only: 새 근거 계획/생성, 원래 top8.
- Ever10 combined: 같은 계획을 공유하되 부족한 근거의 검색 결과를 원래 top8 뒤에 누적.
- 각 Ever 계획은 한 번만 생성하고 두 새 arm이 동일하게 사용한다.
- 50개 최종 출력, 실제 Qwen 요청80회(legacy40, Ever 계획10+생성30).
- 기존 attributed20/20은 역사적 응답 재생 기준. 이번 새 모델 호출로 표시하지 않는다.

동일 Qwen3-8B pinned BF16, nonthinking, temperature0, 출력1024, 문맥32768.
새 combined는 최대16개 검색 구절로 원래 top8보다 더 읽을 수 있다. 동일 토큰 비용
비교라고 주장하지 않고 실제 호출/입출력 토큰을 arm별로 기록한다. 추가 검색은
최대 한 라운드/두 질의/질의당4개다. 실패 후 프롬프트·문항·의미 규칙을 수정하지 않는다.

## 기준

원문과 기존 고정 key를 보고 answer_correct, returned_evidence_supports_all_claims,
required_evidence_complete, narrow_quotes_support_all_claims, unsupported_extra를 기록한다.
일차 성공은 정답 + 반환 근거의 전체 주장 지지 + 필수 근거 완전 + 근거 없는 추가 주장 없음.
원문 문자열 일치, JSON 성공, 검색 R recall을 의미 정답으로 대체하지 않는다.

채택은 (1) legacy20/20 보존, (2) combined가 이전 최선2/10보다 높고 이번 joint보다 높음,
(3) 이전 joint와 contextual 각각의 기존 성공 문항 및 이번 joint 성공을 잃지 않음,
(4) 새 형식/출처 계약 오류가 없음을 모두 요구한다. 미달하면 실험 후보로 남긴다.
구절 단독 인용의 지지도 별도 보고하며 전체 문단 인용으로 개선된 점과 구분한다.

구현 담당 AI의 원문 기반 수동 채점이며 독립 사람 평가가 아니다. 이미 본 개발셋이다.
전체 벤치마크, 미공개 평가 일반화, 승인·병합·자동 재검토 성공을 주장하지 않는다.

## 실행

GPU1/CPU8/RAM48G/45분, 명시적 conda, 노드 지정 없음, --no-requeue.
모델·데이터 준비/해시/추론은 계산 노드. 모델 API는 loopback만 사용한다.
누적 예산 승인 전에는 제출하지 않는다. 반환된 실제 job ID를 먼저 장부에 기록한다.
Slurm COMPLETED/0:0 + 프로그램 complete + 입력/코드 hash를 확인하고,
실제80개 모델 요청의 내용과 출력 재생, 원문 offset을 검증한 뒤 한 번 채점한다.
