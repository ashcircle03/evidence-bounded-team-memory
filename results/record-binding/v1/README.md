# Records 연결 판단: 실제 레퍼런스와 학습까지 검증

2026-11-15. **기존 정답을 유지하면서 올바른 연결 5개를 추가했지만, 새 오류 2개가 생겨 기본 경로로 채택하지 않았다. 자연 기록은 개선되지 않았다.** 이전에 채택한 개별 assertion 속성 보존 경로를 유지한다.

## 무엇을 실제로 사용했는가

GLiNER2.5의 고정된 공개 코드·체크포인트를 사용했다. 인코더, 원문 구절 후보 생성, 자연 anchor 기반 record instance, 학습된 field assignment, native decoder까지 실행했다. 파서나 JSON 모양만 차용하지 않았다. 첫 68건에서 실제 `forward_groups_dense` 호출 68회와 strict 가중치 로드를 확인했다.

공개 모델의 그대로 사용은 실패했다. 완전한 주장보다 명사구를 고르는 경우가 많았고, 65개 native record에서 조건 5개·이유 4개만 출력했다. 기존 Qwen 주장과 정확히 대응된 anchor는 14개였고, 해당 필드를 통째로 교체하면 기존 정답 연결 3개가 사라졌다.

이후 **기존 평가셋을 학습에 사용하지 않고** 별도 합성 240건으로 원본 trainer를 통해 한 번 적응 학습했다. 4개 다른 도메인의 80건에서 실제 주장/필드 구절 F1으로 체크포인트를 선택했다. 여섯 epoch·180 optimizer step 동안 연결 손실과 nonzero gradient를 확인했다. Qwen은 재학습·재생성하지 않았으며, GLiNER2.5의 encoder와 heads 전체를 학습했다.

단순히 학습했다고 말하기 위해 loss만 본 것이 아니다. upstream의 기본 eval loss는 eval mode에서 record assignment 보조 손실을 포함하지 않으므로 실제 추론 기반 선택 callback을 사용했다. 또한 training-data sanitization round trip에서 field metadata가 사라지는 경로를 피하고, 원문 검증 후 처리된 anchor·list cardinality를 검사했다. [코드·학습 전제 분석](../../../docs/records-learned-binding.md)

## 정답·모델 출력·평가기준 고정 비교

68개 원문, 기존 Qwen 원출력, v3 gold/scorer, 난이도·근거 가용성 분포를 그대로 유지했다. 조건·이유만 변경하고 주장·주장 상태·시간·대상 정보는 보존한다. 원문에서 정확히 동일한 assertion span으로 연결할 수 없는 native anchor는 보류한다. QA 호출은 하지 않았다.

`교체`는 matched anchor의 조건/이유를 native 결과로 통째로 교체한다. `양성 제안만`은 명시적인 연결만 추가하고, 같은 원문 구절을 같은 주장에 다른 역할로 명시한 경우만 역할을 변경한다. 빈 목록을 기존 근거가 틀렸다는 뜻으로 취급하지 않는다. 양쪽 정책을 공개 모델과 적응 모델 각각에 적용하여 효과를 분리했다. 문항별로 더 좋은 결과를 골라 합치지 않았다.

| 조건 | 합성 연결 TP / FP / FN | 합성 연결 F1 | 합성 전체 정답 | 자연 연결 TP / FP / FN | 자연 전체 정답 | 기존 정답 보존 |
|---|---|---:|---:|---|---:|---|
| 기존 채택 경로 | 34 / 19 / 47 | 50.7% | 27/54 | 10 / 7 / 38 | 0/14 | 기준 |
| 공개 모델 + 교체 | 31 / 15 / 50 | 48.8% | 26/54 | 10 / 7 / 38 | 0/14 | 실패 |
| 공개 모델 + 양성 제안만 | 34 / 19 / 47 | 50.7% | 27/54 | 10 / 7 / 38 | 0/14 | 유지, 개선 없음 |
| 적응 모델 + 교체 | 34 / 14 / 47 | 52.7% | 28/54 | 10 / 6 / 38 | 0/14 | 실패 |
| 적응 모델 + 양성 제안만 | **39 / 21 / 42** | **55.3%** | **27/54** | **10 / 7 / 38** | **0/14** | **유지, 새 오류 발생** |

최종 후보는 기존 올바른 내용 **283/283**, 연결 **44/44**, 주장 상태 **187/187**, 완전 정답 문서 **27/27**을 유지했다. 그러나 합성 패널의 FP는 19→21, 불필요/불완전 추출 행은 10→12가 되어 사전 채택 조건을 만족하지 못했다. 자연 패널의 기존 오류도 그대로다. 연결의 순증가를 문서 전체 해결로 표현하지 않는다.

## 무엇이 복구됐고 어디에서 여전히 틀렸나

| 사례 | 추가로 맞힌 연결 | 해석 |
|---|---|---|
| e02-partial | 이유 1개 | 원문에 있는 이유를 기존 주장에 연결 |
| m02-partial | 이유 1개 | 원문에 있는 이유를 기존 주장에 연결 |
| m03-full | 조건 1개 + 이유 1개 | saline 범위와 residue-test 이유를 release 금지에 연결; freshwater에 옮기지 않음 |
| h04-full | 조건 1개 | 기존 주장에 적용 범위 연결 |

네 문서에서 다섯 연결을 추가했다. 해당 문서의 기존 오분류나 과잉 추출까지 모두 고친 것은 아니다.

새 FP 두 개는 **m06-full 한 문서**에서 발생했다. 원문은 `under reduced load`가 추정치에 적용된다고 밝히고, 중간에 무관한 구매 완료 기록을 둔다.

- 모델이 `reduced load`를 **구매 완료 주장에도 연결**했다. 실제 scope attachment 오류이며 저장기는 모델의 잘못된 연결을 그대로 옮겼다.
- 추정치 주장에도 같은 조건을 연결했지만, 구절에서 `under`를 빠뜨렸다. 고정 gold의 조건 단위 `under reduced load`를 충족하지 않아 이 연결도 FP/불완전 추출로 채점됐다. 두 번째 항목을 잘못된 대상 선택과 동일하게 해석하지 않는다. 점수를 유리하게 만들려고 gold나 matcher를 바꾸지 않았다.

`unbound:<claim-id>`와 `unmatched:<row-id>`는 새 span 분할 후 ID가 달라질 수 있으므로 incorrect-edge 문자열의 단순 집합 차이는 새 오류 개수가 아니다. 이 문서의 FP **1→3**, 원문·원출력·변경 행을 함께 대조해 위 두 추가 오류를 확인했다.

자연 기록 n03에서는 Azure/S3 비교 주장을 찾았지만, `Considering that ... in the future`의 이유를 native 단계부터 비웠다. n12에서도 `to ensure the charts render correctly`의 목적/이유를 native 단계부터 비웠다. 따라서 이 실패는 저장 과정이나 exact-anchor join만 고쳐서 복구할 수 없다.

보조 진단에서 적응 모델 자체의 조건/이유 링크는 합성 TP 4→20, FP 3→5로 바뀌었지만, 자연 패널 TP는 0→0이었다. 합성 학습이 제한된 연결 패턴을 학습시킨 효과는 확인했으나 자연 기록으로 충분히 전이됐다는 근거는 없다. 목적 표현·긴 담화적 이유 등은 이번 10개 학습 문형의 범위가 좁다는 한계도 있다. 검증 F1 95.1%는 그 별도 합성 문형에 대한 수치이며 프로젝트 benchmark 점수가 아니다.

## 검증·비용·산출물

- 기존 점수 68건 재현, gold/scorer와 코드·입력 hash 확인.
- 5개 경로 × 68문서 = **340건** 실제 저장→재시작→reader 전달 확인.
- 관련 계약 테스트 **107개** 통과.
- 122995: 실행 패키지의 transitive import 누락, 추론 전 FAILED/1:0, 86초. 누락 파일만 v1b에 추가했고 실패 원본을 보존했다.
- 122996: 공개 모델 68건, COMPLETED/0:0, 71초.
- 122997: 한 번의 학습·480회 별도 dev 추론·68회 고정 입력 추론, COMPLETED/0:0, 380초.
- 준비·실패 포함 **8.95 GPU분**, 유료 모델 API **0회**. 모든 서버 계산은 Slurm GPU1 계산 노드에서 conda+격리 환경으로 실행했다.
- 새 체크포인트: `/ceph_data/pjw031003/capstone-shared-knowledge/checkpoints/record-binding-adapt-v1/best`.

실행 후보는 `learned_binding.py`, `positive_binding.py`에 격리해 두었다. 기존 기본 생성기와 서비스 설정은 변경하지 않았다. 학습 설정을 추가로 바꾸거나 이 68건을 보고 재학습하지 않았다.

### 확인할 파일

- [고정 비교 전체 결과](adaptation-evaluation.json), [모든 원출력 연결 trace](adaptation-traces.json), [native 단계 진단](native-stage-diagnosis.json)
- [학습·실제 입력·선택 checkpoint 결과](record-adapt-122997.json), [Slurm/입력/gradient 검증](adaptation-verification.json)
- [공개 모델 원출력](record-binding-122996.json), [최초 비교](evaluation.json), [호환성 수정 기록](compatibility-v1b.json)
- [분리한 학습 데이터 생성](../../../evaluation/record_binding/training_data.py), [단일 적응 학습 계획](../../../evaluation/record_binding/ADAPTATION.md)

합성 54문서는 18개 이야기의 근거 변형이며, 자연 14문서는 기존 실패에서 고른 audit 패널이다. 이 결과를 독립 held-out 성능이나 기존 QA 20문항의 새 성과로 확대하지 않는다.
