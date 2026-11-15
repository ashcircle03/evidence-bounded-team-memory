# records 조건·이유 연결 재대조 결과

2026-11-15. **실제 대화의 어려운 연결 문제는 아직 해결되지 않았다.**
LangExtract의 그룹·원문 정렬을 실제로 연결했고, 조건별 주장 분리와 구절 보존 경로는
구현했다. 그러나 기존 조건/이유5개 요구(EverMem 실제 대화3개+기존 합성2개)는 여전히0/5다. 새 합성 대비의
개선만으로 기본 경로를 바꾸지 않는다.

[원 설계와 구현 대조](../../docs/modules/records-grouped.md) ·
[고정 입력·프로토콜](../../evaluation/record_groups/PROTOCOL.md) ·
[원출력](v1b/record-groups-122895.calls.jsonl) ·
[전체 원문 대조](v1b/semantic-review.json) · [QA 오류 분리](qa-errors-separate.md)

## 무엇을 고쳤나

- SentenceWindow를 관계 추출로 간주하던 적용을 교정했다. 주변 문맥 복구는 그대로
  쓰고, LangExtract1.7.2의 실제 example formatter→resolver→alignment를 재사용한다.
- medication_group 예제를 claim_group으로 변형해 주장·조건·이유·시간·대상 구절을
  같은 그룹에 묶는다. 모델이 질문/정답을 보기 전에 source 전체를 처리한다.
- 원문 위치를 기존 JSON graph로 컴파일하여 저장·재시작·reader packet까지 전달한다.
  새 DB·검사 LLM·QA 수정 단계는 추가하지 않았다.
- **추가로 발견한 우리 어댑터의 문제:** 한 그룹의 개별 구절에 다른 발화 유형이
  붙었다고 source 전체를 버리는 것은 과도했다. 같은 원출력을 다시 처리하는
  `construct_aligned`는 구절을 보존하고 그룹 stance를 명시적으로 unknown으로 둔다.
- upstream MATCH_EXACT는 token alignment다. 정렬된 원문 위치의 **원래 문자열**을
  저장하므로 `in`/`In` 표기 차이를 원문 왜곡 없이 처리한다. fuzzy 정렬은 허용하지 않는다.
- 반복된14:00을 양쪽 사건 모두 첫 위치에 붙이는 문제도 발견했다. 최종 어댑터는
  반복된 조건/이유/시간/대상 구절의 모호한 위치를 거절한다. 복수 발생 위치를
  해소한 것은 아니며, 이 때문에 최종 실패 source가 하나 늘어난 기록도 보존한다.

## 같은 모델·원문 비교

Qwen3-8B b968826d, temperature0, seed42, nonthinking, 출력2048토큰.
기존22source(14 EverMem 개발 메시지+8합성)와 새 합성8source, 총30개다.
기존22개 baseline은122843 캐시, 새8개 baseline과 grouped30개는122895의 **38회 새 호출**이다.
추출 prompt/examples가 달라져 토큰 비용도 다르며 개별 변경 하나의 인과 효과 실험이 아니다.

| 항목 | 기존 문장ID 방식 | 첫 grouped 동결 실행 | 최종 canonical 어댑터 |
|---|---:|---:|---:|
| 추출 graph 수락 source |29/30|18/30|26/30|
| 수락 claim 그룹 |69|44|69|
| 기존 어려운 연결 요구 |0/5|0/5|0/5|
| 새 합성 연결 요구 |5/10|7/10|7/10|
| 전체 부분 요구 |5/15|7/15|7/15|
| 추가 모델 호출 |8 (+기존22 캐시)|30|0, 동일 원출력 재생|

**이 표는 벤치마크 정확도나 전체 semantic precision이 아니다.** 요구15개는 구현 담당자가
작성한 부분 주석이고, 새8개 원문도 구현 담당자의 합성 자료다. 조건/이유 역할을
다른 주장에 붙이는 것과 명제/조건/이유를 같은 긴 문장으로 뭉치는 문제는 원문 검토를
추가로 확인해야 한다. `annotated`는 추출 수락 상태이지 내용이 맞았다는 뜻이 아니다.

첫 동결 결과와 후속 보완을 섞지 않는다:

- [첫 동결 점수·실제38요청 검증](v1b/evaluation.json)
- [같은 원출력의 최종 어댑터 재생](v1b/canonical-replay.json)
- [모호한 시간 위치를 막기 전 중간 결과](v1b/canonical-before-ambiguity-fix.json):27/30,8/15였지만
  잘못된 시간 위치를 발견해 그대로 채택하지 않았다. 최종은26/30,7/15다.
- [각 역할 정보의 실제 위치](v1b/placement.json): 기대 role / 같은 claim의 다른 role /
  다른 claim·원문에만 존재 / claim 자체 추출 실패를 구분한다.
- 옛10개 키를 수정하지 않고 다시 실행하면 [strict](v1b/old-key-strict.json)·
  [canonical](v1b/old-key-canonical.json) 모두0/10이다. 옛 검사는 문장 전체·마침표의
  문자열 포함을 요구해 새 구절 분해에도 실패한다. 이전2/10과 새15개 점수를 바꿔
  이어 붙이지 않는다. 옛 키의 'no measurement/no approval event=basis' 요구 역시
  자격 설명과 실제 결정 이유를 혼동할 수 있어 진단 한계로 명시한다.

## 어디가 좋아졌고 무엇이 남았나

| 사례 | 실제 구성 결과 |
|---|---|
| saline/dry → trayR/S | 기존 한 claim에서 두 claim+각 조건으로 분리 |
| 오염 batch 출시 금지 | `do not` 부정, 적용 조건, assay 실패 이유를 같은 주장에 연결 |
| pressure8/2 → pumpX/Y | 서로 다른 조건과 각 이유를 정확히 분리; 무관한 badge는 별도 |
| coastal 제안 | 조건·시점·might·미측정·미승인 자격을 함께 보존; stance는 unknown |
| 실제 polling | push service 미준비를 polling 이유가 아니라 WebSocket-is-best에 붙임. 여전히 잘못된 연결 |
| version4/CPU 원거리 조건 | 결정과 조건이 따로 남음. one-writer를 basis 대신 condition으로 분류 |
| 잠긴 계정 | ACCOUNT_STATUS_LOCKED는 claim/subject에는 있음. condition 표시는 빠짐: 정보 완전 소실과 구분 |
| 승인 인용 보고 | `Jun says` 귀속이 claim에서 빠지고, 인증 이벤트 없음이 별도 claim에 남음 |
| 반복14:00 | 위치를 확정할 수 없어 최종 실패 처리. 원문 보존을 위치 해소 성공으로 세지 않음 |

정해 둔 부정 조건 위반은 최종 probe에서0건이지만 **전체 오탐0을 뜻하지 않는다.**
polling의 잘못된 연결은 실제로 남아 있다. 원문69개 최종 claim과 원문30개 전부를
구현 담당 AI가 검토했고, 독립 사람의 검증이나 전수 semantic F1은 아니다.

## 전달·QA를 따로 확인

모든30source의 원문·작성자·시간·location이 그대로 저장된다. 최종 수락69claim에 대해
**실제 RecordsAdapter 저장→재시작→linked_span→evidence_from→witnesses_from**을 실행하여
연결된 구절과 자격이 packet에 남는지 검사했다. 실패4source는 raw source와 failed
상태를 보존한다. 구조적 전달이 맞아도 잘못 연결한 의미는 그대로 전달될 수 있다.

이번에는 QA를 새로 생성하지 않았다. [기존20QA 재생](v1/qa-preservation/replay.json)은
130개 정확한 요청이 일치하고20/20 답·근거가 보존됐다. **새 grouped graph를 넣은 QA
정확도가 아니다.** 기존8문항11개 미인용 구절도 그대로 남는다. 원문이 있는데도
계정 잠금/이메일 중단, Friday 날짜, ConflictScore가 틀린 사례는 [별도 트랙](qa-errors-separate.md)이다.

## 실행·비용·재현

- 122892: 의존성 `six` 누락으로 **FAILED/1:0**,104초, 모델 호출0. [실패 로그](v1/sm-122892.log).
- 122895: six만 보완한 별도 source, **COMPLETED/0:0**,1012초. 프로그램 complete,
  입력/코드 SHA와 실제38요청·응답 재생 확인. [장부](v1b/dispatch.json).
- 합계 **18.60 GPU분**(준비·실패 포함), GPU1/CPU8/48G,12h walltime, g8에서 기존
  NLTK·공유 checkpoint 재사용. master에서 Python/추론을 실행하지 않았고 데이터 복제도 없음.
- grouped30개40,157토큰, 새baseline8개4,101토큰. 이전22개baseline12,650토큰과 합치면
  동일30source의 baseline16,751토큰으로, grouped는 약2.40배다. 이것은 구성 비용 비교다.
- 최종 로컬 전체 검사432개+87subtests 통과. 계약/회귀 검사이며 모델 의미 정확도가 아니다.
- 외부/유료 모델 API0회. 후속 canonical 보완은 로컬 원출력 재생만 했다.
- 평가용 importer fixture에 records:import 권한을 빠뜨린 오류를 고쳤다.
  [수정 기록](v1b/measurement-fix.json); 제품 권한 규칙이나 채점 조건은 바꾸지 않았다.

```sh
NLTK_DATA=.cache/reference-nltk python -m evaluation.record_groups.evaluate results/record-groups/v1b 122895
NLTK_DATA=.cache/reference-nltk python -m evaluation.record_groups.placement results/record-groups/v1b 122895
NLTK_DATA=.cache/reference-nltk python -m evaluation.record_groups.replay_alignment results/record-groups/v1b 122895
```

**결정:** 원문 정렬·주장 그룹·구절 보존의 연결 코드는 opt-in으로 남긴다. 원문 기본값은
유지한다. 실제 대화의 핵심 실패가 그대로이므로 “records 지식 품질을 해결했다”거나
“QA도 좋아졌다”고 보고하지 않는다. 남은 문제는 graph DB의 부재가 아니라, 모델이
어떤 구절을 어느 명제의 조건·이유로 묶는지와 원문 내 반복/대화 간 참조의 해소다.
