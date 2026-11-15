# records 조건·이유 결합: 레퍼런스 구현 재대조

2026-11-15. 이 변경은 **records 구성**을 다룬다. 원문이 전달된 뒤 QA가 오답을
만드는 문제는 별도 트랙으로 남긴다. [이전 실제 실패](../../results/record-graph/cases.md).

## 앞선 적용에서 빠진 것

문장 ID의 존재를 검사하면 없는 원문을 인용하는 오류는 줄지만, 그 문장이 어느
주장의 이유인지 알 수 없다. SentenceWindow는 주변 텍스트를 복구할 뿐 관계 추출기가
아니다. 그래서 `schema 성공22/22`와 `역할 요구2/10`이 동시에 나타났다.

| 실제 참고 구현 | 작동에 필요한 연결 | 기존 적용의 차이 / 이번 결정 |
|---|---|---|
| [LangExtract medication 관계 예제](https://github.com/google/langextract/blob/0e441bf77ddc3119dd0aa413322959234dd84ee5/docs/examples/medication_examples.md) | 추출 구절마다 `medication_group`을 부여해 용량·빈도·대상을 같은 그룹에 연결. 실제 formatter→resolver→원문 위치 alignment 사용 | `claim_group`으로 변형. **설치된1.7.2의 PromptTemplateStructured, QAPromptGenerator, Resolver.resolve/align을 실행**한다. 새로운 추론 검사기를 더하지 않는다 |
| [LlamaIndex SentenceWindow](https://github.com/run-llama/llama_index/blob/v0.14.25/llama-index-core/llama_index/core/node_parser/text/sentence_window.py) | 검색된 문장에 주변 문맥을 회복 | 기존 구현 유지. window 안에 있다는 이유로 condition/basis edge를 생성하지 않는다 |
| [StructMem/LightMem 실제 add_memory](https://github.com/zjunlp/LightMem/blob/09b57f75d82cc90148b8c14ab258f2a49a3fae21/src/lightmem/memory/lightmem.py) 및 [prompts](https://github.com/zjunlp/LightMem/blob/09b57f75d82cc90148b8c14ab258f2a49a3fae21/src/lightmem/memory/prompts.py) | segment·source/time 맥락을 factual/relational memory로 넘기는 전체 파이프라인. factual prompt는 구체 정보와 상대시간의 기준 보존을 요구 | LoCoMo relational prompt는 대인·정서 관계 중심이다. 이름만 보고 우리 조건/이유 추출기로 가져올 수 없다. 실행하지 않았으며 해당 성능을 계승한다고 주장하지 않는다 |
| [Graphiti edge extraction](https://github.com/getzep/graphiti/blob/main/graphiti_core/prompts/extract_edges.py) | 이미 추출한 서로 다른 두 entity 사이의 관계, episode 출처 및 이전 메시지의 참조 문맥 | entity resolution/episode 흐름 없이 edge schema만 가져오는 것은 원 설계의 재현이 아니다. DB·entity pipeline은 추가하지 않는다 |

LangExtract의 전체 provider/chunking/multipass 파이프라인을 재현한 것은 아니다.
고정한 짧은 source를 기존 로컬 Qwen으로 한 번씩 처리한다. upstream 기본의 fuzzy
alignment를 끄고, 우리 계약에 맞게 **원문 위치의 문자열**을 저장한다. `construct_aligned`는 upstream MATCH_EXACT의
대소문자 차이를 원래 표기로 되돌리고, 서로 다른 구절 stance는 unknown으로 보존한다.
동결 실험의 엄격한 `construct`는 재현용으로 남긴다. 중첩된
claim/context를 순차 정렬하면 일부가 누락되므로 각 extraction을 독립 정렬한다.
반복되는 조건·이유·시간·대상 구절은 발생 위치가 모호하면 실패로 남긴다. 이 제한은 정확도를
확정하는 장치가 아니라 잘못된 위치를 확정 저장하지 않기 위한 선택이다.

## 입력에서 뒤 모듈까지

1. source 원문·작성자·시각·location 전체를 질문 없이 writer에 전달한다.
2. writer는 `claim_group`으로 주장·조건·이유·대상·시간의 원문 구절들을 묶는다.
3. upstream resolver/aligner로 원문 위치를 얻고 substring 일치와 그룹 완결성을 검사한다.
4. 기존 `record_graph` 계약으로 컴파일한다. 겹치는 구절은 경계에서 잘라 공유 가능한
   원문 unit으로 만들고, **주장별 typed edge**로 연결한다. 전체 원문은 별도로 보존한다.
5. 기존 records 저장·재시작·relations 전달·retrieval 확장·reader bridge를 재사용한다.
   bundle 밖의 구절에 의존하는 annotation은 reader에게 전달하지 않는다.

`condition`은 적용 상황, `basis`는 원문이 진술한 이유/근거다. 시간상 인접했다는
것만으로 원인으로 묶지 않는다. 없는 조건/이유는 빈 목록이며, 추출 자체가 실패한
경우에는 `failed`로 구분한다. 상태 보고와 실제 인증된 승인 이벤트는 합치지 않는다.
미검증 추출에는 항상 `model_extracted_unverified` 자격이 남는다.

이 구조는 **JSON으로 저장한 원문 구절–주장 그래프**다. 새 그래프 DB가 필요한 것은
아니다. 원문의 사실성, 인과관계, 자동 승인 여부를 graph가 보증하지 않는다.
다른 source에 있는 `your understanding` 선행 발화 해소도 이번 단일-source 범위 밖이다.

## 사용 계약

```python
from functools import partial
from team_memory.records.grouped import construct_aligned, writer_kwargs

# writer_options는 records 전용 Qwen 클라이언트에만 적용한다.
writer_options = writer_kwargs({
    'chat_template_kwargs': {'enable_thinking': False}, 'seed': 42,
})
record_builder = partial(construct_aligned, generate=generate, model='Qwen3-8B@b968826d...')
gateway = connect_v2(root, workspace_id=workspace, reader_factory=reader_factory,
                     generate=generate, record_builder=record_builder)
```

추출 모델 ID는 실제 revision을 기록한다. 기존 immutable source는 덮어쓰지 않는다.
실패해도 원문을 저장할 수 있지만 원문 fallback을 역할 추출 성공으로 계산하지 않는다.
`record_builder=None` 기본값을 유지한다. 임시 graph를 확정된 팀 지식으로 승격하는
API나 인증 권한을 추가하지 않았다.

## 평가 경계

[고정 프로토콜](../../evaluation/record_groups/PROTOCOL.md),
[입력](../../evaluation/record_groups/inputs.json), [부분 주석](../../evaluation/record_groups/key.json),
[결과](../../results/record-groups/README.md).

- 문자 위치 무결성/저장/전달은 기계 검사로 측정한다.
- 같은 주장에 조건·이유가 붙었는지, 없는 관계를 만들었는지는 별도 부분 주석과
  전체 출력 원문 검토로 평가한다. 구절 존재나 테스트 통과가 의미 정답은 아니다.
- 원문과 조건이 있어도 QA가 틀리는 것은 별도 기록으로 남긴다. 계정 잠금의
  이메일 중단, Friday 사건 날짜, ConflictScore의 IRRELEVANT 오류를 이번 개선 성과로 세지 않는다.
- 기존20QA exact-request replay는 호환성 검사다. 새 추론 정확도 또는 인용 완벽성이 아니다.

## 남겨 둔 경계

- source 간 참조 해소나 전체 대화의 관계 구성은 이번 단일-source writer가 하지 않는다.
- 문맥 확장은 현재 claim에 걸린 검색 hit에서 연결된 조건/이유로 향한다. 조건만 검색된
  경우의 역방향 회복이나 검색 recall 개선은 이번 저장/전달 검사로 주장하지 않는다.
- 기존 원문 ID에 추출 revision을 여러 개 공존시키는 운영 API는 아직 없다. 이번 비교는
  별도 저장소를 사용하며, 기존 기록을 덮어쓰지 않는다.
- 글자 위치 검증은 인과·적용 범위의 의미 검증을 대신하지 않는다. 같은 그룹에 붙었다는
  것도 모델의 해석이다. 조건/이유가 잘못 붙으면 코드 계약을 통과해도 의미 실패다.
