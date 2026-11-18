# Records: 실패 원인과 레퍼런스 구현의 적용 범위

2026-11-15. 정답·평가기는 `evaluation/record_full` v3 그대로 유지했다. 원문과 실제 모델 입력/출력 136개(grouped 68, bound 68)의 대조는 [실패 목록](../results/record-causal/v1/failure-index.md), 전체 증거는 같은 디렉터리 `failure-traces.json`에 있다. 아래에서 **관찰된 실패 지점, 원인 가설, 실제로 검증한 수정**을 구분한다.

## 1. 개별 상태가 저장 과정에서 사라짐 — 원인 확인, 수정 채택

기존 grouped 원출력에는 한 그룹의 제안과 미승인 관찰이 각각 다른 stance로 있었다. `grouped.compile_graph`는 이들을 그룹 하나의 `unknown`으로 바꿨다. 정보가 처음 변한 지점은 모델 다음의 저장 변환이다.

[LangExtract Extraction](https://github.com/google/langextract/blob/main/langextract/core/data.py)은 추출 항목마다 attributes와 원문 위치를 보유한다. 역할과 상태를 같은 추출 단위에 보관하는 전제를 가져왔다. 우리 `preserving.py`는 기존 LangExtract 정렬과 그룹·구절을 그대로 재사용하고 각 assertion에 원래 stance를 저장한다. 모델 재호출, 의미 재분류, 새 관계 생성은 없다.

**전제:** 원출력의 상태 속성이 맞아야 한다. 잘못된 모델 상태도 충실히 저장하므로 이것은 상태 의미 판정기가 아니다. 승인 표현의 저장은 시스템 승인 이벤트를 만드는 권한을 갖지 않는다.

**검증:** 같은 실제 Qwen 원출력 68개로 저장기만 교체했다. 기존 필수 내용 283개, 연결 44개, 올바른 상태 168개, 완전 정답 문서 23개를 모두 보존했다. 잘못된 상태 판정 23→4, 합성 완전 정답 23→27. 타입 연결 FP·추가 행은 변하지 않았다. 새 `preserving.construct`의 기본 동작은 이 변경만 적용한다.

## 2. 구절 하나의 오류가 문서 전체를 소거 — 원인 확인, 부분 복구는 옵션

기존 컴파일러는 반복되는 시간 구절이나 정렬 실패를 발견하면 예외를 던지고, 호출자가 전체 claims를 비웠다. 실제 원출력의 맞는 항목도 같이 소실됐다.

[LlamaIndex SchemaLLMPathExtractor](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/indices/property_graph/transformations/schema_llm.py)는 중첩 triplet을 항목별로 검증하고 잘못된 항목을 제외한다. `_prune_invalid_triplets`는 허용된 타입 조합과 속성도 검사한다. 여기에서 **독립 항목의 실패를 분리하는 처리 방식**을 가져왔다. 우리 구현은 삭제 이유를 diagnostics로 보존하고 partial 상태를 전달한다. 유효한 claim이 없는 context를 다른 claim으로 옮기지 않는다.

**전제:** 검증기는 정렬/스키마 오류를 발견한다. 원문에 실제 존재하는 구절을 잘못된 대상에 붙이는 의미 오류까지 발견하지 않는다. LlamaIndex의 타입 제한도 올바른 의미 연결을 보장하거나 누락을 채우지 않는다.

**검증:** 이전 정답은 보존하면서 저장 손실 50→16개를 줄였으나, 이전에 문서 전체가 버려져 보이지 않던 잘못된 연결도 26→31개로 노출됐다. 따라서 부분 복구는 명시적인 `isolate_invalid=True` 옵션이고 기본값은 False다. 복구된 결과도 미검증 추출이며, partial을 성공/완전성으로 바꾸지 않는다.

## 3. 문장 경계가 의미 구절의 경계가 됨 — 표현 제약 확인, 단일 변수 검증

bound 입력은 원문 전체를 제공하지만 sentence segment 한 개 안에서만 quote를 선택하게 했다. n03의 `etc.` 뒤에서 분할되어 이유 범위의 일부가 다음 segment로 넘어갔다. 원출력은 이를 독립된 주장들로 복사했고 연결을 만들지 않았다. **한 구절로 표현할 수 없는 제약은 확인했다. 여러 구절로 연결할 가능성이 있었으므로 분할 하나가 실패의 유일한 원인이라고 단정하지 않는다.**

[LangExtract Annotator](https://github.com/google/langextract/blob/main/langextract/annotation.py)는 입력 chunk를 모델에 제공하고 해당 chunk에서 정렬한 뒤 문서 offset을 복원한다. [ChunkIterator](https://github.com/google/langextract/blob/main/langextract/chunking.py)의 버퍼 단위는 우리 문장 ID 강제 계약과 같지 않다. [UIE parser](https://github.com/universal-ie/UIE/blob/main/uie/extraction/predict_parser/spotasoc_predict_parser.py)는 span을 전달받은 전체 text에 대해 확인하고, spot에 association을 붙인다. 우리처럼 sentence ID 경계를 의미 범위로 강제할 필요는 없다.

**전제:** 원문이 모델의 입력 창에 들어가야 한다. 문서 범위를 넓히면 반복 구절 위치가 모호해질 수 있다. 원문 전체를 주는 것만으로 의미 관계가 자동 완성되지는 않는다.

검증은 bound의 지시문·예시·모델·출력 예산을 유지하고 SOURCE의 segment 범위만 문서 전체로 바꾼다. 이 비교는 새 실제 Qwen 호출이며 저장기 재생과 구분한다. 결과가 나와도 기존 정답 보존 없이 기본 추출기로 채택하지 않는다.

**실측 결과:** job122992의 68회 호출이 완료됐다. n03의 이유 전체 문구는 복구됐지만 basis 연결은 여전히 없었다. n10도 검토 이력을 다시 포함했으나 여러 독립 주장을 한 root로 합쳤다. 자연 기록 원출력의 내용은 91/93→93/93이지만 오연결은 1→15, 연결 F1은 44.4→42.5%였다. 기존 올바른 연결 3개와 완전 정답 문서 2개를 잃었다. 정확히 동일한 요청이었던 대조 12건은 원출력도 모두 같았다. 문서 전체 범위에서 반복 구절 82항목의 위치가 모호해져 정렬도 거절됐다. 따라서 **경계 확대는 내용 단절을 일부 고치지만 의미 연결의 해결책으로 충분하지 않으며, 위치 구분과의 조합까지 검증해야 한다.** 이 입력 변경은 채택하지 않았다.

## 4. 조건·이유·시간을 문장에만 복사하고 연결을 비움 — 의미 추출 실패, 해결 주장 보류

e01/e03/n12 등은 내용이 입력과 원출력 root에 있으나 typed context 목록이 비어 있다. e04는 미승인을 별도 root로 만들어 대상 제안과 분리했다. m03은 saline 조건을 freshwater 주장에도 붙였다. 공통으로 저장기가 생성한 오류가 아니라 출력된 관계가 이미 틀렸다. 모델이 만들 수 없는지, 현재 계약에서 어떤 단위를 골라야 하는지가 모호한지는 아직 구분되지 않았다.

[UIE SEL2Record](https://github.com/universal-ie/UIE/blob/main/uie/sel2record/sel2record.py)는 spot과 association을 event trigger/roles로 함께 변환한다. 하지만 [공식 실행 구성](https://github.com/universal-ie/UIE/blob/main/README.md)은 SEL 표현과 schema를 사용한 모델 학습/예측을 전제로 한다. 파서나 괄호 구조만 가져와서 일반 Qwen이 같은 연결 능력을 갖는다고 볼 수 없다. [offset mapper](https://github.com/universal-ie/UIE/blob/main/uie/sel2record/record.py)에는 first/closest 등 위치 선택 전략도 있어, 그대로 사용하면 우리 반복 구절의 보수적인 위치 정책과 충돌할 수 있다.

[GLiNER2 record specification](https://github.com/fastino-ai/GLiNER2/blob/main/gliner2/processing/records.py)은 anchor별 record instance와 field-to-instance 할당을 분리한다. 선택/연결에는 학습된 점수와 디코딩이 필요하다. **실제로 핏한 문제 정의는 발견했지만, schema builder만 Qwen 앞에 붙이는 것은 이 구현을 재현하는 방법이 아니다.** 이번에 새 모델을 설치하거나 해당 방법의 성능을 측정하지 않았다.

실제 [RecordHead/FieldAssignmentScorer 코드](https://github.com/fastino-ai/GLiNER2/blob/main/gliner2/models/boundary/records.py)에서는 instance와 field candidate의 상태로 연결 점수를 계산하고 `ABSENT` 선택지를 함께 둔다. [BoundaryExtractorModel의 `_record_loss`](https://github.com/fastino-ai/GLiNER2/blob/main/gliner2/models/boundary/model.py)는 record 존재와 field 할당 손실을 결합한다. 즉, 누가 어느 조건을 가져야 하는지에 대한 **할당 판단 자체가 학습 대상**이다. 우리처럼 JSON 목록이 유효한지만 검사하는 것과 다르다. 이 경로의 성능을 가져오려면 해당 checkpoint/head·후보 생성·디코더를 함께 검증해야 하며, 일부 구조만 흉내 내는 것으로 대체할 수 없다.

## 5. 불필요 추출과 실질 이력의 잘못된 제외 — 분류 기준·모델 준수 문제, 필터 미도입

n10에서는 `I've reviewed the document`를 ignored로 제외했고, n13에서는 같은 인사가 root와 ignored에 모두 등장했다. 후자는 구조상 모순이며, 전자는 업무 이력과 단순 응답을 구분해야 하는 의미 판단이다. 특정 문구 목록으로 지우면 기존 정답을 더 잃을 수 있어 그런 필터를 추가하지 않았다.

[Graphiti edge 추출](https://github.com/getzep/graphiti/blob/main/graphiti_core/prompts/extract_edges.py)은 이미 제공된 entity 목록과 현재/이전 episode를 활용한다. [실행 연결부](https://github.com/getzep/graphiti/blob/main/graphiti_core/utils/maintenance/edge_operations.py)는 타입별 entity signature와 추출 context를 구성한다. 이는 특정 entity 간 fact 관계 추출을 위한 전제다. 우리 문서 전체의 질문·제안·검토 이력을 빠짐없이 보존하는 계약에 그대로 쓰면 해당 기록이 관계 필터에서 빠질 수 있다. 따라서 인사 필터나 기본 facts prompt만 가져오지 않는다.

## 도입하지 않은 우회책

LangExtract의 [multi-pass 병합](https://github.com/google/langextract/blob/main/langextract/annotation.py)은 겹치는 구절에 대해 앞선 pass를 유지한다. 우리 관계는 같은 구절이 여러 역할/주장에 연결될 수 있으므로, 구절 overlap만으로 병합하면 필요한 관계가 제거될 수 있다. 단순히 pass를 늘리거나 후보를 합치지 않았다. 이번 범위에서 검증한 것은 **개별 상태 저장 수정**, **부분 복구의 효과와 부작용**, **입력 범위의 단일 변수 효과**다.
