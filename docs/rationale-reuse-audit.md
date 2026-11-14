# 결정·근거 추출 구현 재조사

2026-11-08. 목적은 새로운 범용 메모리 모듈을 만드는 것이 아니라, 이미 구현된
결정·근거 추출기를 원형으로 실행하고 적용 범위를 확인하는 것이다.
기존 기본 서비스는 `cup-completion-v3b`이며 이번 후보는 서비스와 연결하지 않는다.

## 후보와 실제 재사용 범위

| 후보 | 직접 확인한 구현/자료 | 우리 문제에 쓸 수 있는 부분 | 바로 대체할 수 없는 부분 |
|---|---|---|---|
| [CoMRAT](https://zenodo.org/records/14176549) | `pages/commit.py:user_commit_page`, `helpers.py:preprocess/load_models`, 학습된 BiLSTM 두 개, 토크나이저 복원용 데이터, 저자 예제 출력 | 원문에 Decision/Rationale이 있는지 학습된 분류기로 판별. **첫 원본 실행 대상으로 선택** | 이유와 결정의 관계 연결, 조건 변화, 승인, 재검토는 출력하지 않음 |
| [Kantara FSE2025 재현 패키지](https://zenodo.org/records/13742395) | 학습·추출·그래프·일반화 노트북, 공개 모델, 실제 중간 출력 | 결정과 근거를 서로 다른 노드로 유지하고 관계를 분석하는 구체적 기준. CoMRAT와 모델 바이트 일치 여부 확인 가능 | 문장 분류 결과를 곧바로 조건부 재검토 정답으로 취급할 수 없음. 아래 구현 감사 사항 있음 |
| [ConDec](https://github.com/cures-hub/cures-condec-jira) | `TextClassifier`, `ClassificationManagerForJiraIssueText`, 학습 CSV, GloVe, 테스트, 재현 설명 | 관련성 분류 후 세부 유형 분류. 자동 분류를 미검증 상태로 저장하고 사람 확인 후 학습에 사용 | Jira 의존 Java 구현. 우리 headless Python 시스템에 즉시 import 가능한 독립 모델은 아님 |
| [MUSE](https://github.com/cohentsofia/MUSE) | `AutomaticAnnotator`, `DocClassifier`, 실행 config, 공개 가중치 안내 | 관련 문단 판별 → 문제/해결책 span → 관계 → 근거의 단계별 입력 조건 | 과학 논문 문제–해결책 추출이며 근거는 합성 단계. GPT batch API가 포함된 전체 원형을 무료 로컬 실행으로 재현했다고 할 수 없음. 소스 감사만 수행, 실행은 안 함 |
| [DRMiner](https://arxiv.org/abs/2405.19623) | 원문 및 저자 publication page | 해결책과 찬반 근거의 연결을 별도 분류 과제로 학습 | 이번 검색에서 실행 가능한 공식 배포본을 확보하지 못함. 동명 Dockerfile 도구는 다른 연구. `kira995/drminer`는 조회 당시 size=0 |
| [SWE-Shield / DesignHunter](https://arxiv.org/html/2604.05955v1) | 원문 §3.1–3.3 | 대안별 적용 조건, 채택되지 않은 제안 보존, 조건에 해당하지 않는 경우 Neutral. 우리 문제의 더 직접적인 조건 표현 참고 | 이번 확인에서 공개 구현 위치를 확보하지 못함. 패치 준수 평가이며 과거 결정 재검토 자체의 벤치마크는 아님 |
| [OpenDecision](https://github.com/deepanwadhwa/OpenDecision) | README | 범용 선택·관계 판별 API | README의 범용 결정 API는 과거 개발 결정·근거 추출기를 학습했다는 증거가 아님. 이번 실행 대상에서 제외 |

DRMiner/DesignHunter 코드를 확보하지 못했다는 것은 비공개이거나 존재하지 않는다는
단정이 아니다. 검색 시점에 확인한 공식 본문·저자 페이지·공개 저장소 검색으로는
원형 실행에 필요한 자료를 찾지 못했다는 뜻이다.

## 저자 코드의 연결 의도와 실제 위험

### CoMRAT의 분류 단위

배포본은 `Decision`과 `Rationale`을 **독립적인 이진 라벨**로 예측한다.
`Decision`에는 행동·변경과 패치 동작 설명도 포함되므로, 라벨 하나만으로
“검토가 필요한 과거 정책 결정”이라고 판단하면 안 된다.

`pages/commit.py`는 매 실행마다 공개 데이터 전체로 `Tokenizer(num_words=1000,
oov_token='<OOV>')`를 복원하고, 그 데이터의 최대 sequence 길이로 padding한다.
이 설정을 다른 토크나이저로 바꾸면 공개 가중치와 맞지 않는다. 이번 실행은
원본 함수·전처리·가중치·0.5 threshold를 그대로 사용한다.

`helpers.preprocess`는 커밋 제목을 첫 줄 전체로 유지하고 본문을 따로 분리한다.
Signed-off-by, URL 등의 제거 규칙도 있다. 일반 팀 문서에서는 첫 줄에 여러
문장이 있을 수 있고 작성자/링크가 근거이므로, 전처리된 텍스트를 원문 저장소의
대체물로 쓰면 안 된다. 원본과 모든 전처리 출력이 함께 보존된다.

### Kantara의 학습 및 관계 입력 감사

재현 패키지 `Automated_extraction 1 (ML_DL models).ipynb`의 코드 cell20/26은
`Sequential()` 모델을 KFold loop 밖에서 생성한 뒤 각 fold에서 같은 모델에
`fit`을 계속한다. 따라서 이 코드의 후속 fold 점수는 독립적으로 새로 학습한
모델의 교차검증 결과와 같지 않다. cell22/28은 저장한 모델을 다시 불러와
데이터의 10%를 나누어 평가한다. 해당 표본이 모델 학습에서 제외되었다는 증거를
이 코드에서는 확인할 수 없다. 공개 가중치에 대한 원 데이터 재평가는 재현
확인으로만 사용하고, 새로운 일반화 성능이라고 보고하지 않는다.

`Application of Kantara to other contexts.ipynb` cell46의
`detect_contradiction_nli_one_pair`는 `sentence1 + sentence2`를 한 문자열로
`pipeline(model='roberta-large-mnli')`에 전달한다. MNLI의 두 텍스트 관계를
검사하려는 의도와 실제 입력 형태가 다르다. 이 코드가 존재한다는 사실과 그것이
논문의 모든 실행에 사용됐다는 주장은 구분한다. 검토한 배포본 경로를 그대로
채택할 근거는 부족하다.

`ChatGPT prompting.ipynb` cell19에는 모든 입력에 결정과 근거가 있다는
전제가 있다. 실제 입력도 양쪽 라벨을 가진 문장으로 미리 고른다. 이 추출 프롬프트를
일반 사실까지 포함한 전체 기록에 그대로 적용하는 것은 원래 과제의 전제를 바꾸는
것이다. 우리 실패처럼 사실을 이유 있는 결정으로 만들 위험이 있다.

관련 cell은 출력·인증값을 제외한 코드만 `results/rationale-reuse/upstream-audit/`에
출처와 함께 보존한다. 외부 코드를 우리 자체 설계 성과로 표현하지 않는다.

CoMRAT와 Kantara의 공개 decision/rationale H5 파일은 각각 byte-for-byte 같다.
Decision SHA256은 `3cbdc1624789eef8eb6847e32ff75b1a443158aebf6a9fd50020b138da196bab`,
Rationale SHA256은 `f0d316fb78fae532677e4d953a768d388d828e0026ea81175c27639d498950c0`이다.

### ConDec에서 확인한 운영 연결

[`TextClassifier.getKnowledgeElementsValidForTraining`](https://github.com/cures-hub/cures-condec-jira/blob/develop/src/main/java/de/uhd/ifi/se/decision/management/jira/classification/TextClassifier.java)은
미검증 텍스트를 학습 대상에서 제외한다. [`ClassificationManagerForJiraIssueText`](https://github.com/cures-hub/cures-condec-jira/blob/develop/src/main/java/de/uhd/ifi/se/decision/management/jira/classification/ClassificationManagerForJiraIssueText.java)는
관련성 이진 분류 후 세부 분류를 수행하며 결과를 `validated=false`로 저장한다.
자동 추출과 사람의 확인을 서로 다른 상태로 다루는 실제 서비스 구현 근거다.
우리의 원문/제안/승인 구분과 연결되지만, 이를 근거로 미검증 추출 결과가 기존
사실 정정을 막도록 하는 것은 정당화되지 않는다.

### MUSE의 단계 연결과 이식 범위

검토 commit은 `f7a40317db46145d0c90b221311d8324db5da1b9`이다.
[`AutomaticAnnotator.get_top_k_relevant_documents_with_rationale`](https://github.com/cohentsofia/MUSE/blob/f7a40317db46145d0c90b221311d8324db5da1b9/src/automatic_annotator_creation/automatic_annotator/automatic_annotator.py#L532)은
두 분류를 통과한 문단만 후속 추출에 넣는다. config의 `doc_classification_top_k=0.1`은
상위 자료로 고품질 지식집합을 구축하는 선택이며, 모든 사용자 질문을 지원해야 하는
우리 QA 검색에 그대로 이식할 recall 정책이 아니다.

`create_rationale_finding_prompt`는 결정 이유를 원문 chunk로 고정하지 않고
독립적으로 읽을 수 있는 2–3문장 설명으로 다시 쓰도록 한다. 우리 인용 계약에는
원문 span을 별도로 보존하는 단계가 필요하다. 또한 [DocClassifier의 비-Mistral
분기](https://github.com/cohentsofia/MUSE/blob/f7a40317db46145d0c90b221311d8324db5da1b9/src/paragraph_classification/doc_classifier/doc_classification_cascaded/doc_classifier_cascaded.py#L196)는
rationale 모델을 로드하면서 `relevant_classifier_checkpoint`를 넘긴다.
이 경로를 별도 검증 없이 “두 독립 분류기”로 사용할 수 없다. 이 관찰은 Mistral
분기나 논문의 모든 실행이 잘못됐다는 뜻은 아니다.

## 이번 실행과 다음 연결 조건

`cup-comrat-original-v1`, Slurm `120443`, GPU1 예약, conda, walltime12h.
34개 입력: 공개 예제12 + 알려진 팀 시나리오11개의 old/new 원문22.
headless adapter는 Streamlit의 입력·표시만 대체한다. 저자 함수를 직접 호출하고
실제 token IDs, 확률, 전처리 결과, 모델/입력 해시를 저장한다.

공개 예제의 기존 예측24개 라벨 일치 여부는 **실행 재현성**이다. 사람의 5명
라벨과의 일치도는 별도로 계산한다. 팀 old11개는 근거 있는 결정4개와 사실7개를
분리하는 작은 적용성 진단이며, 자연 데이터 일반화 벤치마크가 아니다.

후보 통과 조건은 공개 출력24/24 재현, 결정4개 탐지, 사실7개 오탐0이다.
통과해도 바로 서비스에 연결하지 않는다. 원문 근거와 새 보고의 조건을 비교하는
과제는 별도로 남는다. 실패하면 임계값/프롬프트를 덧붙여 같은 사례를 맞추지 않는다.

기존 QA20/상태8을 후보에 다시 흘리는 것은 이 선행 단계의 적용성이 확인된 후다.
이번처럼 후보가 서비스에 연결되지 않은 실행은 QA가 새로 20/20 통과했다는
증거가 아니다. 대신 기존 서비스 파일 해시가 변하지 않았는지를 확인한다.
