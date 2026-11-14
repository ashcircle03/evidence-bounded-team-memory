# 다섯 실제 어댑터 연결 결과

**기존 v2의 저장·검토 규칙과 reader를 재사용해 다섯 포트를 연결했다.** 실제 파일 저장 → 재검토/정정 제안 → owner 승인 → 재시작 → QA가 동작한다. 기존 v2 진입점은 그대로 유지한다. [사용법·범위](../../docs/modules/runtime.md).

## 확인한 것

| 검사 | 결과 | 의미 |
|---|---:|---|
| 기존20, 완전한 Qwen HTTP 요청 일치 | 130/130 | 동일 요청일 때만 기록된 응답을 사용 |
| 기존20, native 최종 답 문자열 | 20/20 동일 | reader 생성·후처리 보존 |
| 기존20, native 답/인용 객체 | 20/20 동일 | 기존 구절·출처·위치 보존 |
| 기존20, 공개 original_text | 20/20 동일 | 새 claim 변환이 원문 답을 삭제하지 않음 |
| 기존20, claim에 연결된 인용의 전체 집합 | 20/20 동일 | 다른 근거를 만들거나 기존 근거를 잃지 않음 |
| 명시적 인용이 없는 구절 | 8문항·11구절 | partial/unattributed로 보존; 임의 인용 금지 |

[문항별 대조·입력 해시](v1/replay.json). 원 측정은 module-boundary 작업120445의 Qwen3-8B 결과다. **이번은 과거 검색 결과를 고정한 정확한 요청/응답 재생이다. 새 모델 추론·검색 벤치마크·새 정답 채점이 아니다.** 전체 호출의 일치를 확인하므로 잘못된 요청에 과거 정답을 덧씌우지 않는다.

20문항의8개는 원래 문장별 인용이 완전하지 않았다. 최초 단순 변환은 그 문장을 버렸고, 이를 고치기 위해 v1.1에 original_text·unattributed·answer_span을 추가했다. 원문 답·기존 근거는 보존하지만 문장별 인용 완전성을20/20이라고 보고하지 않는다. 구절 일치 자체도 의미 지지를 증명하지 않는다.

## 실제 구현 연결 검사

다음 검사는 고정 응답 포트가 아니라 **실제 records·relations·retrieval·answering·gateway**를 사용한다. LlamaIndex 검색·HTTP client·상태 축약·파일 commit은 실제 코드이며, decoder 출력만 stub이다.

- 저장·승인 후 재시작과 동일 snapshot 복원.
- 재검토 승인이 사실 변경으로 바뀌지 않고 QA의 상태 근거에 전달됨.
- 사실 정정이 지정 assertion만 대상으로 삼고 다른 사실의 답·근거는 유지됨.
- 상충 답 두 개가 별도 근거와 함께 반환됨.
- QA가 비교 모델이나 상태 쓰기를 호출하지 않음.
- 검색은 생성하지 않고, 고정 근거를 받은 생성은 재검색하지 않음.
- 비교 실패 후 원문은 남고, 명시적 재시도가 중복 저장/중복 비교를 피함.
- 무단 투표·workspace/capability 위반·조작된 snapshot을 거절.
- revision 경쟁에서 한 쓰기만 성공, IO 실패/재시도 후 상태 일관성 유지.
- 미연결 답 구절을 보존하고, 상태 근거 누락·예산 초과 시 생성 전에 명시적으로 중단.
- 기존 v2 파일 변경과 갈라진 Git module 이력을 숨기지 않고 STALE_SNAPSHOT으로 표시.

[저장 검사](../../tests/test_module_records.py) · [실제 어댑터 연결 검사](../../tests/test_reference_module_adapters.py) · [전체 검증 기록](v1/verification.json).

## 남은 범위

현재는 단일 이력의 opt-in runtime이다. 분기된 Git 이력 자동 병합·실제 인증 transport·historical 상태 조회는 완료하지 않았다. 모델의 재검토 오분류를 해결한 변경도 아니다. 원문 조건은 그대로 전달하고 질문의 조건을 모델 입력에 붙이지만, 새로운 조건 추출기를 추가하지 않았다.

새 canonical 상태 근거를 실제 Qwen이 얼마나 잘 해석하는지, 상태8의 새 추론 성능은 별도 확인이 필요하다. Aurora 조회 당시122740은 QOSMaxGRESPerUser로 대기했고121613이 실행 중이었다. 이번 작업에서 기존 작업을 변경하거나 새 GPU 작업을 중복 제출하지 않았다.

```sh
python -m pytest -q tests/test_module_records.py tests/test_reference_module_adapters.py
TOKENIZERS_PARALLELISM=false python -m evaluation.module_adapters.replay
python scripts/check.py all --fail-on-skip
```
