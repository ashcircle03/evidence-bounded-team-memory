# 한정된 명사구가 가리키는 정책 적용 범위

동일한 Qwen 추출 원출력, 기존 GUM 판정, 정답 및 채점기로 비교했다. 68문서에서 개별 정답 연결 50개를 보존하고 n08에서 하나를 복구했다. 오연결은 20개에서 19개로 줄었다. 새 문서 성능 및 QA 정확도는 이번 실험의 측정 대상 밖이다.

| 자료 | 정답 연결 | 오연결 | 완전 정답 문서 |
|---|---:|---:|---:|
| 합성 54문서 | 40 → 40 | 13 → 13 | 30 → 30 |
| 자연 14문서 | 10 → 11 | 7 → 6 | 0 → 0 |

n08의 고정 채점기는 원문 위치 [45,91)의 제한된 계정 집합을 r1 정책의 condition으로 요구한다. 구문 분석 결과 accounts는 routed의 수동 주어, marked는 accounts의 수식절, must는 routed의 조동사다. 조건 연결을 포함한 두 필수 연결 모두 정답이지만, Qwen이 추출한 별개 수신 확인 인사도 여전히 주장으로 저장된다. n03은 기존 분류 판단과 교정 임계값을 그대로 사용했다. 전체 문서에서 새로 생긴 오연결과 사라진 정답을 각각 식별자로 비교했다. 새 records를 저장하고 다시 연 뒤 reader의 각 주장이 받은 역할별 구절 ID와 출처 메타데이터를 확인했다. [문서별 결과](evaluation.json)

## 어떤 자료를 어떻게 사용했나

- Alohaly 등의 ABAC 연구는 정책 주체·객체와 각각을 제한하는 속성을 구별해 후보를 찾고 분류한다. 저자들의 반합성 851문장에는 주체 속성 867건, 객체 속성 932건이 주석돼 있다. 원자료는 요청 배포이며, 이 연구에서 가져온 부분은 주체와 속성의 연결을 먼저 식별하는 설계다. 저자 분류기를 재현하거나 이 자료로 학습하지 않았다. [원 논문](https://doi.org/10.1186/s42400-018-0019-2)
- 공개 RAGent 원본 자료의 collected_train 행 163은 적용 대상에서 저자를 제외하는 예외를 별도 deny 규칙으로 표현한다. 이 형식을 단일 condition으로 바꾸면 허용·거부 구분을 잃을 수 있어 이번 적용 범위에서 제외했다. [원본 정책 주석](https://github.com/paperwave/RAGent/blob/main/data/document_folds/overall_acp.csv)
- UD English EWT r2.15 학습 분할의 email-enronsent41_01-0046에서 quantity와 shown은 명사–수식절로 연결되고 수량에 관한 규격을 shall로 표현한다. 같은 구문이 적용 범위 해석과 무관한 예측에도 쓰인다(newsgroup-groups.google.com_misc.consumers_628669ce346c590d_ENG_20040527_065700-0027). EWT는 구문 주석 대조에 사용했다. 실행에 쓴 spaCy 모델은 자체 모델 메타데이터에 OntoNotes 5를 기재한다. [공개 학습 분할](https://github.com/UniversalDependencies/UD_English-EWT/blob/r2.15/en_ewt-ud-train.conllu) · [실행 모델](https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-3.7.1)
- 단일 주장에 귀속된 subject가 보편 한정사와 제한절 전체를 포함하고 그 주어의 술어에 must 또는 shall이 직접 연결될 때 기존 보류를 condition으로 바꾼다. 기존 원문 위치·주장·stance는 보존한다. 수식절 없는 주체, 객체, 관찰 결과, 잘린 구절과 비제한절은 대조 예제에서 보류했다. 외부 양성은 RFC 5049 §3에서 확인했다. 조동사의 인식적 용법이나 복잡한 예외까지 정책 의미를 보장하는 분류기는 아니다. [독립 규격 문장](https://www.rfc-editor.org/rfc/rfc5049#section-3)

## 재현

records의 선택적 생성 진입점은 team_memory.records.policy_scope.construct다. 기존 generate, predict, training_counts에 로드된 영어 parser를 parse 인자로 더한다. 업무 서비스의 기본 추출 경로는 기존 설정을 사용한다.

평가에는 기존 프로젝트 환경과 별개의 Python 3.11 parser 환경을 썼다. 후자에는 spaCy 3.7.5, en_core_web_sm 3.7.1, NumPy 1.26.4, Click <8.2, Typer <0.13을 사용했다. 모델 wheel의 SHA-256은 86cc141f63942d4b2c5fcee06630fd6f904788d2f0ab005cce45aadb8fb73889다. PARSER_PYTHON을 해당 환경의 Python 경로로 설정하고 저장소 루트에서 실행한다.

```bash
"$PARSER_PYTHON" -m evaluation.record_binding.discourse.check_policy_scope
NLTK_DATA="$PWD/.cache/reference-nltk" .venv/bin/python -m evaluation.record_binding.discourse.evaluate_policy "$PARSER_PYTHON"
```
