# 구절은 있는데 연결이 잘못되는 문제

범위: records의 조건·이유 연결. QA, 검색기, 더 큰 모델, 평가셋 학습은 포함하지 않는다.

**실행 후 판단:** 대상 보존 계약은 구현했지만 새 Qwen 연결기는 기각했다.
고정 68문서에서 정답 typed link는 44→52, 오연결은 26→380,
완전 정답 문서는 27→13이었다. 동일 예측의 group 대조도 54/317로 나빴다.
따라서 저장 시 범위 확장이 이번 의미 오분류의 주원인이라는 해석은 지지되지 않는다.
원출력 자체에서 조건/이유 혼동과 무관한 대상 연결이 확인됐다.
[전체 결과](../results/record-binding/v4/README.md)를 함께 읽어야 한다.

## 확인된 원인과 아직 가설인 부분

1. **연결 대상의 정체성이 어댑터에서 사라진다.**
   `learned_binding.bind`는 레퍼런스가 반환한 정확한 주장 offset을 찾은 뒤
   `claim_group`으로 바꾼다. 그 그룹에 여러 assertion이 있으면 새 context는
   특정 assertion이 아니라 그룹에 저장된다. v3 reader와 평가용 표현도
   그룹 단위로 이를 전달한다. 원래 모델의 선택과 저장된 관계의 범위가 달라진다.
   이것은 코드에서 재현되는 계약 결함이다. 모든 의미 오분류의 원인이라는 뜻은 아니다.
2. **이전 Qwen 후보는 endpoint 생성과 관계 선택을 동시에 했다.**
   `anchored_binding`은 target group만 고정하고 context quote를 다시 생성했다.
   n12 원출력은 목적 구절만 고르지 않고 행동·목적을 합친 문장 전체를 basis로
   반환했다. n13에서는 주장을 포함한 문장을 condition으로 반환했다.
   원문에 있다는 검사만으로는 어느 주장에 어떤 관계로 연결되는지 보장할 수 없다.
3. **정확한 span이 있어도 학습된 연결 판단이 실패한다.**
   이전 native trace의 n03은 이유 후보 확률 0.68073이지만 올바른 anchor와의
   assignment 확률은 약 0.0000047이었다. 반대로 m06은 `reduced load`를
   procurement 쪽에 강하게 연결했다. span 탐지와 대상 연결은 다른 능력이다.
   10개 템플릿의 합성 학습 dev 성과만으로 자연 기록의 연결 능력을 주장할 수 없다.
   이 수치만으로 학습 분포와 모델 용량 중 어느 쪽이 유일한 원인인지는 판정하지 않는다.

실측 원출력과 확률은 `results/record-binding/v2/` 및
`docs/records-natural-binding-audit.md`에 보존되어 있다.

## 레퍼런스가 실제로 하는 일

| 구현 | 대상 판단에 쓰는 입력·연산 | 우리 쪽에서 잃거나 바꾼 부분 | 이번에 가져오는 부분 |
|---|---|---|---|
| GLiNER2 records head | anchor instance 표현과 field 표현을 합쳐 각 후보 span 및 NULL에 점수를 부여한다. decode 결과도 anchor span과 field span을 구분한다. | 정확한 anchor를 group ID로 축약했다. 관계 학습 분포의 전이도 보장되지 않았다. | 구체적인 instance를 저장까지 보존하고 연결하지 않음을 허용한다. |
| Graphiti edge extraction | source episode와 entity endpoints, 허용 관계 타입을 함께 입력한다. source/target을 구분하는 관계를 만든다. | 한쪽 구절을 새로 생성하면서 묶음에 붙였다. | 양쪽 endpoint를 먼저 고정하고 방향·타입을 판단한다. |
| PAIE | 사건·역할에 조건화된 start/end selector를 학습하며, 정답 span과의 matching 및 CE loss를 사용한다. | 역할 이름과 출력 형식만 가져와서는 학습된 연결 선택 능력이 생기지 않는다. | 역할 추출과 대상 조건화를 구분한다. Qwen에 그 supervised head가 있다는 주장은 하지 않는다. |

고정하여 읽은 실제 코드:

- [GLiNER2 records.py](https://github.com/fastino-ai/GLiNER2/blob/c379245ce9fe0fee03a530a320ddb1885847c4d6/gliner2/models/boundary/records.py)
- [GLiNER2 relations.py](https://github.com/fastino-ai/GLiNER2/blob/c379245ce9fe0fee03a530a320ddb1885847c4d6/gliner2/models/boundary/relations.py)
- [Graphiti extract_edges.py](https://github.com/getzep/graphiti/blob/3a8a78c997a07cceeb3411ede533b0f342d71c64/graphiti_core/prompts/extract_edges.py)
- [Graphiti edge_operations.py](https://github.com/getzep/graphiti/blob/3a8a78c997a07cceeb3411ede533b0f342d71c64/graphiti_core/utils/maintenance/edge_operations.py)
- [PAIE paie.py](https://github.com/mayubo2333/PAIE/blob/1917c46db1498e6115aa40897790d6b36a9b83e2/models/paie.py), [논문](https://aclanthology.org/2022.acl-long.466/)

Graphiti의 entity 관계를 proposition 관계로 바꾸는 것은 우리 적용이다.
해당 버전은 없는 endpoint를 materialize하는 경로도 있으므로, 기존 endpoint만
허용하는 이번 계약을 Graphiti 자체의 보장이라고 주장하지 않는다.
이번 실행은 이들의 학습된 모델을 재현한 것이 아니라, 실제 연결 단위를 유지하는
설계를 Qwen3-8B 입력·저장 계약에 적용한 비교다. LangExtract의 실제 exact aligner는 재사용한다.

## 수정 내용

`team_memory/records/pair_binding.py`는 기존 원출력의 정렬된 구절만 사용한다.
구절을 새로 생성하지 않고, context마다 개별 target에 `none / condition / basis`
중 하나를 선택한다. 동일 구절이 여러 주장의 근거일 수 있지만 각 연결을 별도로
명시해야 한다. 원문과 작성자·시각 등의 메타데이터는 그대로 입력한다.

`records.graph/v4.context_bindings`는 `target_start/end`와 `context_start/end`를
함께 저장한다. 원래 units·claims·assertions·stance·legacy edges는 변경하지 않는다.
뒤 모듈에는 두 구절과 정확한 방향, `model_extracted_unverified` 자격을 전달한다.
LLM이 선택한 관계가 승인 이벤트나 확정 사실이 되지는 않는다.

이는 새 의미 검사기를 뒤에 추가하는 방식이 아니다. 기존 연결 생성 경로와
저장 표현을 바꾼 후보이며, NONE은 기존 기록 삭제 권한을 갖지 않는다.
따라서 기존 오연결까지 자동으로 고치는 구현도 아니다.

## 비교와 한계

고정 68문서, 같은 Qwen3-8B와 기존 원문·추출 구절을 사용한다. 61문서의
263 context 요청에서 1,192개의 방향 있는 쌍을 판단한다. 기존 저장 실패 7문서는
그대로 실패로 포함한다. gold, scorer, 난이도·근거 가용성 분포는 변경하지 않는다.

동일한 새 원출력을 (a) 선택한 assertion에만 저장하거나 (b) 기존 group으로
넓혀 저장하는 대조를 둔다. 별도로 기존 accepted baseline과 비교한다.
과거 free-quote 방식과는 후보 범위·호출 수가 다르므로 동등 비용 실험이라고
부르지 않는다. 자연 14문서는 이미 본 실패 감사 사례이며 새 일반화 평가가 아니다.

고정 채택 기준과 결과는 `evaluation/record_binding/PAIR_PROTOCOL.md`와
`results/record-binding/v4/`에 둔다. 기존 내용·연결·stance·완전 정답 문서 보존,
두 패널 각각의 오연결·불필요 추출 비증가, 새 조건/이유 정답 증가를 모두 요구한다.
