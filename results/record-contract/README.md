# 추출 계약·예시 비교: 일부 연결 개선, 기본 채택 보류

2026-11-15. **계약과 저장·전달은 구현했지만, 새 입력 묶음을 기본값으로 채택하지 않는다.**
같은 Qwen3-8B와 같은30원문에서 부분 연결 검사는7/15→10/15로 올랐으나,
기존에 맞힌7개 중1개가 퇴행했고 날짜·발화 상태·자격 정보 손실도 확인했다.
이는 벤치마크 정확도가 아니라 구현 담당자가 만든 개발용 부분 요구 검사다.

[추출 계약](../../docs/modules/records-extraction-contract.md) ·
[고정 프로토콜](../../evaluation/record_contract/PROTOCOL.md) ·
[실제60요청·원출력](v1/record-contract-122915.calls.jsonl) ·
[30원문·전체 출력 카드](v1/review-cards.md) · [전체 의미 검토](v1/semantic-review.json)

## 변경과 레퍼런스 근거

LangExtract1.7.2의 medication_group 사례가 관련 구절을 의미 있는 대상 키로 연결하는
방식을 그대로 prompt formatter→resolver→exact alignment에 사용한다. 새 검사 모듈은 없다.
이번 변경은 조건·이유의 **대상별 연결 계약과 예시**다.

- 제한된 대상 구절이 subject/claim 안에 있어도 condition으로 별도 연결.
- basis에 `stated` / `inferred` / legacy `unspecified`를 보존. 모두 모델의 미검증 주석이다.
- 동일한 원문 구절이 여러 주장·역할에 연결될 수 있도록 공유 unit과 대상별 edge를 유지.
- graph/v2에 basis_annotations를 추가하고 원문·작성자·시간·상태 권한과 분리.
  v1은 그대로 지원하고 기존 저장 기록은 수정하지 않는다.
- 예시17행은 upstream preflight의 독립 구절 정렬을 모두 통과했다. 중복/겹침이 필요한
  전체 순차 정렬에서는4문제가 발생한다는 점을 공개했다. upstream의 전체 순차 경로와
  동일하다고 주장하지 않는다.

이유 분류는 LangExtract가 제공하는 검증된 인과 추출기가 아니다. upstream은 그룹화와
원문 정렬을 제공하며, 역할의 의미 정확도는 이 비교에서 확인해야 하는 부분이다.

## 통제한 비교

같은30source(14 EverMem 개발 메시지+16합성), Qwen3-8B b968826d,
temperature0/seed42/nonthinking/출력2048. 두 arm 모두 새로30회씩 호출했다.
원문·메타데이터·system·출력schema·compiler는 동일하고 description/examples/그룹 키
안내만 다르다. 복수 입력 변경을 한 묶음으로 평가했으므로 어느 문장 하나의 효과인지는 모른다.
기존 입력 arm의30개 원출력은 과거122895의 grouped 출력과 모두 동일했다.

| 항목 | 기존 입력, 새 실행 | 수정 입력, 새 실행 |
|---|---:|---:|
| 전체 부분 연결 요구 |7/15|10/15|
| 기존 어려운5요구 |0/5|2/5|
| 이전에 맞힌7연결 보존 |7/7|6/7|
| 추출 수락 원문 |26/30|24/30|
| 수락 주장 |69|52|
| EverMem14메시지 추출 수락 |12/14|9/14|
| 총 토큰 |40,157|54,356|

수락은 schema/구절 정렬 성공을 뜻하며 의미 정확도를 뜻하지 않는다. 모든60출력은
finish_reason=stop이며 길이 잘림으로 실패한 것은 아니다. 수정 입력 비용은 약1.35배다.

## 기존5개 요구의 실제 결과

| 요구 | 수정 입력 결과 |
|---|---|
| ACCOUNT_STATUS_LOCKED 적용 범위 | subject와 condition에 같은 제한 구절 연결. 복구 |
| polling 선택의 미준비 이유 | raw에서는 polling에 연결했지만 `stated`로 잘못 분류. 반복된 bare `WebSocket` subject의 위치 모호성으로 원문 전체 추출 거절 |
| WebSocket 안정화 뒤 전환 조건 | raw에서는 Once 조건을 올바른 전환 주장에 연결. 같은 원문 거절로 저장된 graph에는 없음 |
| version4 실험 연기 이유 | version 조건은 연결. 명시되지 않은 이유는 생략. 모호한 이유를 단정하지 않는 것은 허용되지만 이유 복구로 세지 않음 |
| 멀리 떨어진 version4/CPU 조건과 one-writer 이유 | 조건과 명시된 이유를 연기 결정에 함께 연결. 복구 |

원출력의 부분 개선과 실제 저장 성공을 섞지 않았다. version4의 조건 구절은 원문의
대문자 `Version 4`를 택해 옛 소문자 부분키에도 맞지 않지만, 이유 자체가 없어 원래
전체 요구는 어차피 실패다. 키를 고쳐 점수를 올리지 않았다.

## 채택하지 않는 이유

- **보호 연결 퇴행:** coastal 제안의 `no durability measurement exists`를 inferred
  basis로 만들어, 기존의 “이유 없음” 검사를 잃었다. `This is not approval...`도
  해당 주장과 분리됐다. 미측정·미승인은 근거의 한계이지 자동으로 지지 이유가 아니다.
- **날짜·발화 상태 손실:** Thursday/afternoon 누락, 완료된 태스크 제목을 decision으로
  추출하는 오류, 일부 명령을 proposal로 바꾸는 오류가 있다.
- **예시 복사2건:** AWS 비교와 notification 원문에서 마지막 station-Z/calibration
  예시를 그대로 출력했다. 원문 정렬이 거절했으나 추출 성공으로 볼 수 없다.
- **잘못된 이유:** untested/no-measurement를 stated basis로, version4 미검증을 version5
  성능의 inferred basis로 처리했다. acknowledgement와 목적의 인과 방향도 뒤집었다.
- **반복 위치 문제:** 실제 polling은 주된 연결이 좋아져도 보조 subject의 반복 위치 때문에
  전체 실패한다. 정렬 정책을 사후 완화해 결과를 구제하지 않았다.

수정 입력은 기존 예시의 시간·불확실성 사례와 명시적인 stance 정의를 보존하지 않은
채 조건/이유 예시로 교체했다. 이 입력 차이는 확인된 사실이고, 그것이 모든 퇴행의
단독 원인이라는 인과 결론은 아니다. 같은 모델에서 일부 어려운 연결은 개선됐으므로
“모델이 원천적으로 못한다”는 결론도 내릴 수 없다.

[evaluation.json](v1/evaluation.json)의 `false_stated_probes=0`은 **수락 graph의 정해진
대상·전제 쌍만** 센 값이다. 실패한 polling raw나 그 밖의 잘못된 이유는 이 숫자에
들어가지 않는다. 전체 오탐0으로 해석하면 안 된다. 모든121수락 주장과10실패 raw,
30원문을 구현 담당 AI가 대조했으며 독립 사람의 전체 semantic gold는 아니다.

## 저장·전달과 기존 QA

모든60source에서 원문·메타데이터 불변을 확인하고 실제 record.append→store restart→
evidence→reader packet 경로를 재생했다. 수락121claim의 연결과 basis 종류가 보존됐다.
공유 근거를 두 주장에 전달하는 것은 공통 예시 fixture로 검사했다. 이30source에서
실제 모델이 그 기능을 일반적으로 잘 수행한다는 결과는 없다.

기존 QA20문항은130개 정확한 요청의 기록 재생에서 답·근거20/20을 유지했다.
새 graph를 넣은 실제 Qwen QA 성능은 아니다. 기존8문항11개 미인용 구절도 남아 있다.
로컬 전체 검사436개+87subtests 통과. [검사 기록](v1/local-checks.json).

## 실행과 결정

Aurora122915는 **COMPLETED/0:0**, 프로그램 complete, 코드·입력 SHA와60실제요청·출력
재생 일치. GPU1/CPU8/48G/g8,12h 제한으로 제출해 실제922초(**15.37 GPU분**) 사용했다.
초기 SSH handshake 실패는 queue/accounting상 미제출임을 확인한 뒤 제출했다.
기존 데이터·checkpoint·의존성을 재사용했고 master에서 계산하지 않았다. 외부 모델 API0회.

**유지:** 역할 중복·공유 구절·이유 자격을 표현하고 끝까지 전달하는 계약/코드.
**기본 채택 보류:** 이번 revised description/examples 묶음. 기본 원문 QA 경로는 그대로다.
추가 rescue 실험이나 사후 prompt 수정은 하지 않았다. 서비스 저장/색인 수명주기의 문제는
[별도 감사](../service-storage/README.md)로 분리한다.

```sh
NLTK_DATA=.cache/reference-nltk python -m evaluation.record_contract.evaluate results/record-contract/v1 122915
NLTK_DATA=.cache/reference-nltk python -m evaluation.record_contract.review_cards results/record-contract/v1 122915
```
