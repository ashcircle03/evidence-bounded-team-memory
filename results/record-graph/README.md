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
- [v1 제출 장부](v1/dispatch.json), [v2 제출 장부](v2/dispatch.json): 두 작업 모두 COMPLETED/0:0, 프로그램 complete와 입력·코드 hash 확인 완료.
- [기존 QA20 재생](v1/qa-preservation/replay.json):20/20 답·근거 보존,130개 정확한 요청 일치. 새 QA 정확도가 아니다.
- [모델 실행 전 문맥 진단](v1/offline-probes.json): reference window의 전달 범위만 검사.22개 의미 추출은 not_run이며 이를 성능 점수로 세지 않는다.

구조 검사에서 정확한 원문 ID를 연결해도 역할을 틀리게 지정한 반례는 통과할 수 있다.
전용 테스트는 이 반례를 구조 성공으로 남기고 별도 의미 요구사항 검사에서 실패함을 확인한다.
따라서 테스트 개수·문자열 존재·graph edge 무결성을 semantic precision으로 보고하지 않는다.

새 모델 결과의 claim/조건 연결, 상태 혼동, QA 답·근거는 원문에 대조해 따로 판정한다.


## 완료 결과와 결정

**자동 역할 그래프를 QA 기본값으로 채택하지 않는다.** 원문 주소화·명시적 상태 분리·문맥 보존의 구현과 계약은 남기고, 모델의 주장/조건/이유 연결은 opt-in 진단 후보로 둔다. `record_builder=None`이 기본이다.

| 검사 | 첫 실행 v1 | 형식 수정 v2 | 의미 |
|---|---:|---:|---|
| 입력 원문·메타데이터 보존 및 초기 QA 전달 |22/22|22/22|기계적 전달, 의미 정답 아님|
| schema를 통과한 source 구성 |12/22|22/22|vLLM guided_json으로 형식 오류 해소|
| 고정한 10개 진단 요구의 모든 역할 연결 존재 |1/10|2/10|부분 주석에 대한 존재 검사, semantic precision 아님|
| 새 QA 실행 |9쌍|9쌍|동일 원문·동일 Qwen, 실제 저장/재시작/답변 실행|
| 새 실제 모델 호출 |97|101|writer22 + QA 양쪽 포함|

v1의10개 추출 실패는 ID 배열 대신 대상 이름·시간 문자열을 생성한 오류였다.
Pydantic schema를 생성 단계에 연결하지 않은 구현 결함을 발견해, **[vLLM의 기존 guided_json 기능](https://docs.vllm.ai/en/v0.8.5/features/structured_outputs.html)**을 적용했다.
[v2 변경 범위](v2/FORMAT.md)처럼 입력·프롬프트·정답·모델·QA 코드는 유지했다.
v1을 지우거나 성공 결과로 바꿔 쓰지 않는다.

v2의54개 claim을 모두 원문과 비교한 [의미 검토](v2/semantic-review.json)에서는 다음 문제가 남았다.

- 대부분 자기 문장에만 연결되어, polling 유지의 이유나 원거리 version4/CPU 조건이 decision에 붙지 않는다.
- 이유를 조건으로 분류하거나, 완료 보고를 결정으로 분류한다.
- 승인 이벤트가 없다는 중요한 문장은 원문 unit에는 남아도 해당 주장과 연결되지 않는다.
- `It`, `your understanding` 같은 참조가 해소되지 않는다. 단일 source 입력이라 다른 메시지의 선행 질문은 graph에 연결되지 않는다.
- 레퍼런스의 문장 분리도 `etc.`에서 절을 쪼개는 사례가 있다. 업스트림 구현을 실행했다는 사실만으로 우리 데이터에 맞는 지식 단위가 되지는 않는다.

[문항별 답·인용 대조](cases.md), [실제 출력 포함 JSON](cases.json):

- Confluence와 담당자 gold 일치는 유지됐다. 담당자 원문 자체의 개인별 업무 대응은 모호하다.
- 계정 잠금은 **raw D → linked B**로 퇴행했다. 중단해야 할 이메일을 전송한다고 답했다.
- polling은 v1 linked에서만 D였고 v2에서는 다시 C였다. 안정적인 개선 증거가 없다.
- 날짜는 저장된 `last Friday` 연결이 맞아도 v2 QA가 사건을4/7로 잘못 옮겼다. 6일/7일 계산 관례 문제와 별개다.
- 원거리 version4/CPU 조건은 양쪽 답에서 빠졌다.
- 인증된 승인으로 전환하는 저장 이벤트는 생성되지 않았지만, QA의 보고/상충 설명은 여전히 과장됐다.

따라서 '전부 보존됨'을 주장하지 않는다. **원문과 메타데이터는 도달했으나, 역할 연결과 후속 해석은 실패했다.**

## 단계별 증거와 측정 범위

[검증 v1](v1/verification.json), [검증 v2](v2/verification.json)은 writer가 질문 없이 원문만 받은 사실, 저장/재시작 뒤의 source 일치, 초기 QA의 전체 원문·작성자·시각·연결 정보, 각 ConflictScore 입력의 해당 원문·작성자·시각을 확인한다.
ConflictScore는 원문을 독립적으로 검사하며 새 추출 graph를 입력받지 않는다. 모든 하위 검사기에 graph를 전달했다고 주장하지 않는다.
v1 call49는 `halt_downstream_triggers=true`를 입력으로 받고도 이메일 전송 답에 `IRRELEVANT`를 반환했다. 이 오류는 전달 누락으로 설명되지 않는다.

실제 모델 실험은 고정 source QA다. 자동 재검토 관계 분류 개선이나 실제 검색 성능을 측정하지 않았다. 저장→비교→검색→승인→QA의 연결은 stub 기반 통합 테스트로 별도 검사했고, 이를 실제 모델 승인/재검토 정확도로 계산하지 않는다.
기존20문항의130 요청 재생은 답·근거를 보존했다. 이전부터 있던8문항11개 미인용 span도 그대로이며 인용 완벽을 주장하지 않는다.

9개 문항은 기존 실패에서 고른 개발 사례와 합성 대비다. key는 구현 담당자가 만든 부분 주석이며 독립 gold가 아니다. 날짜의 양끝 포함 여부, 두 사람/두 업무의 대응, because 없이 인접한 이유/결정, 수치 보고를 measured로 부르는 문제는 별도로 표시했다.
원본 시간에 timezone이 없어 이번 importer가 UTC를 붙인 것은 명시적 실험 관례다. 실제 timezone을 복원했거나 절대 시간 추론을 검증한 것이 아니다.

## 비용·재현

- v1: writer12,877토큰 + raw QA43,585토큰 + linked QA63,423토큰.
- v2: writer12,650토큰 + raw QA43,561토큰 + linked QA82,289토큰.
- v2 linked QA는 raw의 약1.89배 토큰, 최초 구성 비용까지 포함하면 약2.18배다. 구성 비용은 재사용할 수 있지만 이번9문항에서 상쇄 효과를 보이지 못했다.
- GPU 실제 점유: v1 21분57초 + v2 8분9초 = **30.10 GPU분**, 준비 포함. client 실행은 각각341.3초/365.2초. 준비·캐시 조건이 달라 전체 walltime 차이를 모델 성능으로 해석하지 않는다.
- 총198호출, 유료/외부 모델 API0회. 두 run의 raw 최종 문자열은8/9 동일; 차이는 승인 보고 사례의 표현이며 독립 반복·통계적 유의성을 주장하지 않는다.
- 로컬 전체421개+87subtests 통과, sandbox의 loopback 제한으로 실패한 기존 HTTP1개는 제한 밖 재실행 통과. 이후 추가한 실제 schema 요청 전달 테스트 포함 graph6개 통과. CI도 확인한다.

```bash
python -m evaluation.record_graph.verify results/record-graph/v1 122842
python -m evaluation.record_graph.verify results/record-graph/v2 122843
python -m evaluation.record_graph.analyze --result results/record-graph/v2/record-graph-122843.json --output /tmp/record-graph-analysis.json
```

이번 결과를 보고 추가 의미 규칙이나 프롬프트 수정을 넣지 않았다. 다음 개선의 대상은 graph DB 추가가 아니라 **조건/이유/자격의 올바른 연결과 미해결 참조 표현**, 그리고 원문을 받고도 뒤집는 reader의 별도 오류다. 현재 모델의 연결을 확정 팀 지식으로 승격하지 않는다.
