# Records 저장 변환: 원출력의 개별 속성 보존

기존 grouped 추출 프롬프트를 유지하면서 저장 중 상태가 사라지는 결함을 수정한 경로다. 새 LLM 호출 단계나 QA 검사를 추가하지 않는다. 원출력 자체의 의미 오류는 그대로 남으며, 모델이 생성하지 않은 관계를 코드로 추정하지 않는다.

## 사용

```python
from team_memory.records import grouped, preserving

# 기존 모델 클라이언트의 structured output 설정:
writer_options = grouped.writer_kwargs(basis_types=True)

def record_builder(source):
    return preserving.construct(
        source,
        generate,  # 기존 (system, user_prompt) -> raw JSON string 함수
        model="Qwen3-8B@b968826d9c46dd6066d109eabc6255188de91218",
    )
```

`generate`는 호출자가 제공하는 기존 클라이언트다. 위 writer_options는 그 클라이언트에 적용해야 한다. `connect_v2(..., record_builder=record_builder)` 또는 기존 `GatewayAdapter`의 같은 주입 지점에 연결한다. 질문 경로에서 다시 추출하거나 기존 source를 덮어쓰지 않는다. 모델 요청과 원출력 trace는 호출자의 실행 기록에 남긴다.

기존 `grouped.construct_aligned`, `grouped.construct_contract`는 과거 결과 재현을 위해 바꾸지 않았다. 모든 서비스의 설정을 자동으로 변경한 것은 아니다. records 담당자가 선택할 수 있는 수정된 저장 경로를 제공한다.

## 기본 동작과 선택 기능

| 옵션 | 기본값 | 동작 | 검증 판단 |
|---|---|---|---|
| 개별 assertion 속성 보존 | 항상 켜짐 | 같은 그룹의 제안·관찰 등의 stance를 개별 span에 저장 | 기존 정답 보존, 완전 정답 증가 |
| `isolate_invalid` | `False` | True이면 정렬 불가 항목을 격리하고 나머지를 partial로 저장 | 정보는 더 보존하지만 잘못된 관계도 추가 노출되어 기본 채택 보류 |

부분 복구가 필요하면 `preserving.construct(..., isolate_invalid=True)`를 명시한다. 같은 API의 `compile_graph(source, raw, ...)`로 이미 보관한 원출력을 모델 재호출 없이 검증할 수도 있다. source에 record_graph가 이미 있으면 construct는 덮어쓰지 않는다.

## 저장 계약

- 입력은 완전한 원문과 원문 ID·작성자·시간·위치다. 원문은 변경하지 않는다.
- 기존 LangExtract Resolver가 원문 전체에 대해 정확히 정렬한다. fuzzy 보정, 의미 보정, 근처 구절 선택은 하지 않는다.
- 기존 claim_group·역할·원문 offset을 유지한다. 개별 claim row의 `stance`와 span ID를 `records.graph/v3.assertions`에 보관한다.
- 그룹의 대표 stance만으로 모든 assertion의 상태를 판단하면 안 된다. reader packet에는 개별 assertion 속성이 포함된다.
- 추출의 상태 표현은 원문에 대한 미검증 해석이다. 제안·승인·철회 이벤트를 시스템에 적용하지 않는다.
- 반복되는 context의 위치가 모호하면 보류한다. 부분 복구 모드에서도 삭제된 root의 context를 다른 주장으로 옮기지 않는다.
- partial에는 diagnostics가 있다. 정렬이 통과했다는 사실은 연결 의미가 맞다는 뜻이 아니다.
- 부분 복구 후 동일한 claim identity가 충돌하는 경우는 여전히 문서 단위 failed가 될 수 있다. 실제 h05-partial에서 확인됐으며, 임의 병합으로 숨기지 않았다.

## 검증

동일한 실제 Qwen 출력 68개를 old → 개별 속성 보존 → 항목 격리 순서로 처리했다. 정답과 v3 평가기는 그대로다. 세 경로의 204개 실제 append→재시작→reader 전달을 확인했다. 모델 재생성 없이 저장기 변경 효과만 분리한 검사이며, 새로운 QA 성능 검증은 아니다.

```bash
NLTK_DATA="$PWD/.cache/reference-nltk" .venv/bin/python -m pytest -q tests/test_record_preservation.py
NLTK_DATA="$PWD/.cache/reference-nltk" .venv/bin/python -m evaluation.record_causal.storage
```

[실패별 레퍼런스 대조](../records-reference-fit.md), [고정 비교 결과](../../results/record-causal/v1/README.md), [기존 graph/v3 설명](../records-bound-extraction.md).
