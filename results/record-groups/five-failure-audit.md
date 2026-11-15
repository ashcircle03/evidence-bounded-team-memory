# 남은 기존5개 요구의 원출력 원인 감사

2026-11-15. 대상은 기존 어려운 요구5개(EverMem3+기존 합성2), 원문4개다.
polling 원문에서 이유/전환 조건을 각각 검사하므로 독립 원문5개가 아니다.
전체15요구 중 최종 실패8개와도 구분한다. **새 모델 호출·Slurm 제출·모듈 추가0회**다.
런타임 코드, 프롬프트, 기존 정답 키와 점수는 바꾸지 않았다.

[기계 대조·원출력 발췌 JSON](five-failure-audit.json) ·
[원본 trace](v1b/record-groups-122895.calls.jsonl) ·
[원래 키](../../evaluation/record_groups/key.json)

## 결론

5건을 모두 '모델이 조건/이유를 이해하지 못함' 또는 'records가 정보를 잃음'으로
설명하면 부정확하다. **생성 단계에서 이미 역할 표기와 그룹 연결이 기대와 다르고,
한 항목은 우리 프롬프트의 추론 제한과 채점 키도 긴장 관계에 있다.**

- 2요구: 필요한 조건이 같은 주장 그룹에 있는데 role이 다름(잠긴 계정, 미래 전환).
- 2요구: 다른 문장의 정보가 필요한 주장에 연결되지 않음(polling 이유, 원거리 조건).
  원거리 사례는 이유를 condition으로 분류한 오류도 함께 있음.
- 1요구: scope 표기 누락 + 명시되지 않은 인과관계를 정답으로 강제한 평가 문제(version4).

5요구가 요구한 역할 연결은 총7개다. 원출력에서 **4개는 같은 그룹의 다른 role에,
3개는 다른 그룹에만** 있었다. 모두 필요한 구절을 원출력에서 찾을 수 있다.
이는 올바른 구조화를 뜻하지 않지만, '내용을 전부 잊었다'는 설명은 배제한다.

## 실제 입력과 전송 확인

| call | 원문 길이 | 입력/출력 토큰 | 종료 | 확인 |
|---|---:|---:|---|---|
|8|260자|1189/209|stop|전체 원문 있음|
|13|342자|1203/331|stop|전체 원문 있음; 요구2개|
|15|102자|1090/129|stop|전체 원문 있음|
|21|448자|1139/168|stop|원거리 조건과 최종 결정 모두 있음|

동일 Qwen3-8B, seed42, temperature0, nonthinking, 출력 상한2048이다.
본문을 잘라 넣거나 출력 토큰 한도에서 중단한 흔적은 없다. 모든 대상 정보는
각각 하나의 입력 source 안에 있으므로, 이5건을 이전 메시지 누락 탓으로 설명할 수도 없다.
원본 요청의 마지막 Q가 원문 전체와 정확히 일치하는지 확인했다.

실제 upstream Resolver.resolve를 다시 실행해 raw의 class/text/group/stance가 그대로
해석됨을 확인했다. canonical 어댑터 재생도 보존된 결과와 정확히 일치했다.
**parser가 condition을 subject로 바꾸거나 group b를 c로 옮긴 것이 아니다.**

## 1. 잠긴 계정 범위 — call8

원문은 `all accounts marked as ACCOUNT_STATUS_LOCKED`에 정책을 강제 적용한다.

원출력:

```text
group b / claim   : 전체 계정 잠금 정책 문장
group b / subject : all accounts marked as ACCOUNT_STATUS_LOCKED
condition         : 없음
```

조건 문자열이 전체 claim과 subject에 이미 있고 적용 정책과 같은 그룹이다.
따라서 그룹 결합 실패보다는 **역할 계약 불일치**다. 한정된 주어는 문법적으로 subject이고,
논리적으로 적용 범위를 제한한다. 우리 정의는 subject와 condition의 중복 추출 여부를
충분히 명시하지 않은 채, 키는 condition 배열에만 있어야 통과시킨다.
원문 의미가 없어진 것으로 채점하면 안 되지만, 뒤 모듈이 condition 필터에 의존한다면
typed field 누락 자체는 실용적인 실패다. 새로운 평가 통과로 바꾸지 않았다.

## 2. polling 유지 이유 — call13

원출력:

```text
group b / claim     : WebSocket is the best solution
group b / condition : our message push service isn't fully ready yet
group c / claim     : This task can be implemented using polling for now
group c / condition : by requesting the interface every 10 seconds
basis               : 없음
```

미준비 구절을 추출했지만 polling을 선택한 이유로 연결하지 않았다. 10초마다 요청하는
구현 방법도 condition으로 분류했다. **역할 오분류와 주장 간 연결 누락이 동시에 있다.**

다만 미준비 사실이 WebSocket 문장과 관련 있다는 것 자체가 무관한 연결은 아니다.
같은 사실이 WebSocket 적용의 제약인 동시에 polling 임시 선택의 이유가 될 수 있다.
앞 보고의 '다른 주장에 잘못 붙였다'는 표현은 이 점을 충분히 구분하지 않았다.
정확한 진단은 **polling을 지지하는 관계가 빠졌다**는 것이다.

우리는 '서로 다른 명제는 다른 그룹'을 요구하면서, 독립 observation이 다른 결정의
basis로도 재사용되는 예시는 제공하지 않았다. 동일 구절을 여러 group에 반복하는 것은
schema상 가능하지만, 실제 few-shot에는 그런 사례가 없다. 이 입력 설계 차이가
원인일 가능성은 있으나, counterfactual 생성 비교 없이 인과 효과를 확정할 수 없다.

## 3. WebSocket이 안정된 뒤 전환 — 같은 call13

원출력:

```text
group d / claim / unknown  : Once the WebSocket service is stable later
group d / claim / proposal : we can upgrade it uniformly
condition                 : 없음
```

전환과 선행 조건이 이미 같은 그룹에 있다. `condition`을 `claim`으로 분류한 문제다.
우리 예시에도 Once-the-hoist 조건을 condition으로 표시했는데 따르지 않았다.
**현재 모델·현재 입력 설정에서 역할 지시를 안정적으로 수행하지 못한 사례**는 맞다.
그러나 조건 자체를 이해하지 못했거나 다른 주장에 연결했다고 할 증거는 아니다.

초기 어댑터는 unknown/proposal이 한 그룹에 있다는 이유로 이 source 전체를 failed로
처리했다. 이는 우리 구현이 추가한 제약이며 upstream의 의무 조건이 아니다.
이후 canonical 보완은 구절을 보존하고 stance를 unknown으로 바꿨지만, role은 여전히
claim이다. 따라서 source 수락률 개선을 조건 분류 개선으로 보고하면 안 된다.

## 4. version4 실험 보류 — call15

전체 원문:

> Version 4 permits one writer only. We defer the throughput experiment for version 4. Archive is Orion.

원출력은 세 문장을 각각 a/b/c claim으로 보존했다. version4는 보류 결정 group b의
본문에 있지만 condition 필드는 비었다. one-writer 사실은 group a에만 있다.

여기서 **평가 키에도 문제**가 있다. 문장 배치와 상황으로 이유를 추론할 수 있지만
원문은 because/therefore 등으로 원인을 명시하지 않았다. 반면 우리 지시는 stated
reason만 추출하고 mere adjacency로 이유를 만들지 말라고 한다. 명시된 이유와 문맥상
추론한 이유의 경계를 정하지 않은 채, 키는 one-writer를 반드시 basis로 요구했다.

이 항목의 basis 실패를 곧바로 모델의 인과 이해 실패로 확정할 수 없다.
이전 점수0을 사후1로 고치지도 않았다. 다음 정답 명세에서 '명시된 이유'와
'추론 가능한 이유'를 구분해야 할 모호한 항목으로 남긴다.

## 5. 원거리 version4/CPU 조건 — call21

원출력:

```text
group a / claim     : This experiment concerns version 4 on CPU only
group c / claim     : We defer the throughput experiment
group c / condition : because only one writer is available
basis               : 없음
```

첫 문장의 범위를 마지막 결정에 연결하지 않았고, 명시적인 because 구절을 condition으로
분류했다. 이 사례는 **문서 전체의 적용 범위 연결 실패 + 이유 역할 오분류**다.

사이에 반복된 archive 문장이8개 있지만, 원문은448자이며 전체가 같은 입력 안에 있다.
따라서 잘린 context나 이전 chunk 미전달로 설명할 근거는 없다. 'This experiment'가
뒤 결정의 실험과 같은 대상이라는 연결을 수행하지 못한 상태다. 단, 반복 문장이
실패를 일으켰는지, 중립적인 조건에서도 같은지, 다른 모델이면 해결되는지는 미측정이다.

## 레퍼런스 적용에서 확인한 차이

고정 commit `0e441bf...`와 설치된 LangExtract1.7.2의 prompting/resolver/annotation/extraction
네 파일 git-blob SHA가 모두 일치했다. 엉뚱한 버전의 핵심 코드를 비교한 문제는 아니다.

### 기능 범위를 더 크게 해석했다

[공식 관계 예제](https://github.com/google/langextract/blob/0e441bf77ddc3119dd0aa413322959234dd84ee5/docs/examples/medication_examples.md)는
약 이름을 group 값으로 삼아 약–용량–빈도–적응증을 묶는다. 공식 예제 실행 모델은
Gemini2.5Pro다. 우리의 a/b/c 그룹은 새로 생성한 명제이고, 명제의 이유·전역 조건까지
연결해야 한다. **entity 중심 속성 그룹화에서 명제 간 이유/범위 연결로 과제를 확장했다.**

그룹 키를 어떤 값으로 줄지는 모델이 판단한다. Resolver는 출력 파싱과 위치 정렬을
수행하며 '왜 polling을 선택했는가'를 추론해 관계를 보완하지 않는다. upstream 정렬기를
실행했으니 그 인과 추론까지 가져왔다고 해석하면 안 된다. 약 이름 대신 a/b/c를 쓴
변경이 성능에 영향을 주었는지는 아직 가설이다.

### 우리 few-shot은 일부 필요한 패턴을 설명하지 않는다

2개 예시의 basis는 근거리 because 예시1개다. 독립 사실이 다른 결정의 basis가 되는
경우, 같은 사실이 여러 명제에 사용되는 경우, 문서 앞의 범위가 뒤 결정까지 적용되는
경우, 제한된 subject와 condition을 동시에 표시하는 경우가 없다.
한편 Once 조건의 예시는 실제로 있으므로 '예시가 부족해서5건 모두 실패했다'고 단정할
수도 없다. 모델이 지시를 어긴 관찰과 입력 설계가 불충분한 관찰은 함께 남긴다.

### 실제 upstream 예시 검증 절차를 생략했다

[extract의 사전 검사](https://github.com/google/langextract/blob/0e441bf77ddc3119dd0aa413322959234dd84ee5/langextract/extraction.py#L226)는
few-shot 구절이 원문에 정렬되는지 확인한다. 우리는 formatter/resolver만 직접 연결해
이 검사를 생략했다. 이번에 실제 `validate_prompt_alignment`를 실행한 결과:

- 첫 예시의 `the hoist`가 source 등장 순서보다 뒤에 출력되며, 앞 condition과 겹친다.
- upstream 기본 정렬에서는 MATCH_FUZZY 경고1개.
- 우리의 fuzzy-disabled/lesser-disabled 정책으로는 정렬 실패1개.

원문에 없는 구절을 예시에 넣었다는 뜻은 아니다. **예시의 중첩/순서와 가져온 정렬
방식이 맞지 않는다**는 구체적인 적용 문제다. 우리의 독립 구절 정렬에서는 통과하지만,
그 차이를 full-reference 호환성 검사로 검토하지 않았다. 이 경고가 현재5개 role
오류를 유발했다고 증명된 것은 아니다.

### 생략한 기능이라고 모두 이번 실패의 원인은 아니다

- 기본 `extraction_passes=1`, `context_window_chars=None`이다. 현재 source4개는 모두
  기본1000자 buffer보다 짧고 실제로 전체를 받았다. multipass/이전 chunk 문맥을
  생략해서 이5건이 실패했다고 말할 근거는 없다.
- [upstream multipass 병합](https://github.com/google/langextract/blob/0e441bf77ddc3119dd0aa413322959234dd84ee5/langextract/annotation.py#L46)은
  겹친 구절에 대해 첫 pass를 우선하고 새 비중첩 구절을 추가한다. 이미 찾은 구절의
  잘못된 role/group을 교정하는 전용 단계가 아니다. 반복 실행만으로 해결된다고
  기대하는 것도 근거가 부족하다.
- Qwen3-8B 비추론 설정과 공식 예제의 Gemini2.5Pro가 다르지만, 현재 자료에는 같은
  입력을 받은 두 모델의 비교가 없다. 모델 크기/추론 모드/우리 입력 중 어느 요인의
  영향이 큰지 비율로 분해하거나 '8B 한계'로 결론낼 수 없다.

## 현재 판단과 수정 우선순위

**현재 증거로 확정할 수 있는 것:** 필요한 원문은 들어갔고 role/group의 차이는 raw 생성
단계부터 존재한다. parser/저장 단계가 그 의미를 뒤집은 것이 아니다. strict 어댑터의
전체 source 폐기는 별도 구현 결함이었다. 추가 checker로 이 상황을 덮을 이유는 없다.

먼저 정해야 할 것은 더 많은 모듈이 아니라 추출 계약이다:

1. condition은 별도 span으로 반드시 중복 표기해야 하는지, subject 안의 범위를 어떻게
   다룰지 정한다. 내용 보존과 typed-field 성공을 분리한다.
2. stated basis와 inferred basis를 구별한다. 현재 version4 항목은 정답 재검토 대상으로
   표시하고 기존 점수는 유지한다.
3. 그 계약에 맞는 예시를 upstream 사전 검증에 넣고, 원문에 근거한 group anchor와
   다중 연결의 표현을 정한다. 이를 모듈 추가 없이 기존 writer 입력의 한 가지 차이로
   고정해야 모델 차이와 표현 차이를 비교할 수 있다.

이번 턴은 원출력 분석만 수행했다. 위 수정이나 새 성능 실험을 실행했다고 주장하지 않는다.
