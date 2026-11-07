# QA 실패 재분석과 공개 구현 조사

2026-11-07. 새 GPU 작업·모델 호출·실행 코드 변경 없이120295의 실제 요청과
원출력, 로컬 연결 코드, 아래 저자 공개 구현을 대조했다. 기존 점수/키는 변경하지 않았다.

## 결론

현재 실험은 저자 구현을 보존한 비교가 아니라 여러 방법의 일부를 상당히 바꾼
Qwen 어댑터 비교다. 원 방법이나8B 모델의 한계로 실패를 확정할 근거는 부족하다.
특히 검색 선택권, 구절 복사 의존성, 입력 메타데이터 생략은 우리 연결에서 생겼다.
다음 QA 경로의 우선순위는 LongMemEval 공개 검색·독해 구현과 ALCE의 문단 ID 인용이다.
새 계획/검증 모듈 추가를 우선하지 않는다. 프로젝트 전체 baseline 교체 결정은 아니다.

## 실제 기록에서 확인한 사실

| 지점 | 확인된 증거 | 해석의 경계 |
|---|---|---|
| 추가 검색 | Ever10 모두 missing_queries=[]; 실제 추가 검색0; reader_only/combined 출력10개 모두 동일 | 반복 검색 자체의 유효성을 시험하지 못했다 |
| 검색 예시 | AF2개와 AQA 변형1개 모두 missing_queries=[]; AF 원 예시에는 이 필드가 없음 | 예시 편향 가설은 있으나 원인 분리 실험은 안 함 |
| 최초 검색 | FeedbackRetriever.original은 본문 BM25; metadata BM25도 별개로 존재 | embedding 모델을 로드했다고 이 경로가 dense 검색인 것은 아님 |
| 대화방 | 저장 location에 Group1/2/3이 있지만 실제 sources에는 source_id/record_author/recorded_at/text 네 필드만 존재 | 작성자·날짜를 줬다는 것과 대화방/프로젝트 맥락 보존은 다름 |
| 시간 순서 | 검색 순위 순으로 입력; Guoxin 문항에서5월·12월·1월·4월·6월 기록이 혼재 | 시간순 정렬의 효과는 아직 미측정 |
| breakpoint | 의미상 맞는 첫 구절은 RST backtick 생략과 들여쓴 목록 문맥 때문에 위치 복원 실패; 두 번째 구절은 빈 값이면 debugging이 꺼진다는 실제 오내용 | 형식 차이와 의미 변경을 같은 종류로 수리하면 안 됨 |
| 빈 근거 이후 | 유효 highlights=[]인데 생성 호출은 진행됨; 원출력은0과 highlight_id=2; 최종 답 제거 | 답 읽기와 인용 계약 실패를 분리해야 함; 원출력 정답을 최종 성공으로 재채점하지 않음 |
| 비용 | Ever direct 평균입력5,683토큰; 이전 joint 평균1,626토큰; 성공은 둘 다2/10 | 프롬프트도 달라 예시만의 인과 효과는 아님 |

로컬 근거: `reference_connected.py:66`, `reference_retrieval.py:39`,
`reference_demonstrated.py:133,152,184`, `reference_format.py:34`.
실제 요청: `results/reference-qa/demonstrated-v1/calls.jsonl`.

## 레퍼런스별 연결 의도와 구현

### IRCoT: 검색에 쓰는 추론과 마지막 답을 분리

고정 커밋 `3c1820f698eea5eeddb4fba3c56b64c961e063e4`.
검색기는 최초 질문 또는 마지막 생성 문장으로 다음 질의를 구성하고 기존 문단을
누적한다. 종료는 빈 생성/최대 문장수/답 형식으로 제어한다. 확인한 QA 설정은
검색 종료 후 원 질문을 복사해 별도 answer_main_question 단계에 전달한다.
우리 missing_queries optional gate와 다르다. 원 코드의 실제 제어 흐름을 보존할
때만 IRCoT 구현 비교라고 부를 수 있다.

- [검색 입력 구성](https://github.com/StonyBrookNLP/ircot/blob/3c1820f698eea5eeddb4fba3c56b64c961e063e4/commaqa/inference/ircot.py#L339)
- [종료 제어](https://github.com/StonyBrookNLP/ircot/blob/3c1820f698eea5eeddb4fba3c56b64c961e063e4/commaqa/inference/ircot.py#L933)
- [최종 QA 연결](https://github.com/StonyBrookNLP/ircot/blob/3c1820f698eea5eeddb4fba3c56b64c961e063e4/base_configs/ircot_qa_flan_t5_xl_hotpotqa.jsonnet#L80)

### LongMemEval: 찾기 위한 표현과 답의 원문을 구분

LongMemEval은 모델 이름이 아니라 벤치마크와 공개 실험 구현이다.
고정 커밋 `9e0b455f4ef0e2ab8f2e582289761153549043fc`.
검색 코드에는 BM25/Contriever/Stella/GTE가 있고 fact key 확장은 원 ID·시간과
연결된다. 생성 코드에는 원 기록을 복원하는 경로와 fact로 대체하는 별도 옵션이 있다.
원문 보존을 위해 default merge_key_expansion_into_value=none 또는 명시적 merge를
구별해야 한다. 검색용 fact를 최종 확정된 팀 지식으로 자동 승격하면 안 된다.

저자 구현의 읽기 입력은 시간순으로 정렬하고 세션 날짜와 역할을 보존한다.
run_generation.sh의 기본 reading_method=con은 --cot true인 단일 답변 호출이다.
문서마다 별도 노트를 만드는 경로는 con-separate이며 기본값과 다르다.
따라서 'CoN을 쓴다'는 이유만으로 별도 추출 모듈 여러 개를 만들 필요가 없다.

시간 범위 추출에는 범위를 내는 예시와 N/A 예시가 함께 있고, 코드상 ±2일 여유를
준다. 범위 밖 기록은 목록에서 삭제하지 않고 뒤로 이동한다. 이 처리를 우리 데이터의
시간 필터로 자동 채택할 근거는 없으며, 특히 '다음 독립 과제까지' 질문에 날짜를
추측해 검색 범위를 좁히는 것은 우선하지 않는다.

- [검색 구현](https://github.com/xiaowu0162/LongMemEval/blob/9e0b455f4ef0e2ab8f2e582289761153549043fc/src/retrieval/run_retrieval.py)
- [key 확장과 ID 보존](https://github.com/xiaowu0162/LongMemEval/blob/9e0b455f4ef0e2ab8f2e582289761153549043fc/src/retrieval/index_expansion_utils.py#L17)
- [기본 con과 con-separate 구분](https://github.com/xiaowu0162/LongMemEval/blob/9e0b455f4ef0e2ab8f2e582289761153549043fc/src/generation/run_generation.sh)
- [원 기록 복원·날짜 정렬·독해](https://github.com/xiaowu0162/LongMemEval/blob/9e0b455f4ef0e2ab8f2e582289761153549043fc/src/generation/run_generation.py#L46)
- [시간 조건과 후순위 이동](https://github.com/xiaowu0162/LongMemEval/blob/9e0b455f4ef0e2ab8f2e582289761153549043fc/src/index_expansion/temp_query_search_pruning.py#L39)

[논문](https://arxiv.org/html/2410.10813v2)의 중요한 적용 경계: 작은 모델의 긴 입력,
시간 범위 추론, CoN이 항상 이득인 것은 아니다. Llama3.1-8B에서 보고한 입력 길이
민감도를 Qwen3-8B의 임계값으로 옮기면 안 된다. 본 실험에서도 예시 입력 증가만으로
개선되지는 않았다. 이 사실이 특정 길이 임계값이나 예시의 해로움을 입증하지는 않는다.

### ALCE: 문단 인용과 좁은 구절 추출의 역할 분리

고정 커밋 `246c476a4edfc564266b7346b6e29ef4861ae937`.
기본 프롬프트는 답의 문장에 제공된 Document 번호를 인용하며, 매번 원문 문자열을
재생성하도록 요구하지 않는다. 문장별 최소 충분 출처를 권장한다. 자동 평가는
정답성과 citation recall/precision을 분리한다. 특히 여러 인용 중 불필요한 출처도
검사한다. 이것은 NLI를 온라인 답 차단기로 붙이는 것과 다르다.

우리 용도에서는 문단 ID 인용을 먼저 성립시키고 좁은 하이라이트를 부가 기능으로
분리하는 쪽이 단순하다. 단, 유효한 ID만으로 내용 지지가 확인되는 것은 아니며
ALCE 평가 모델도 우리 작성자/프로젝트/조건 판단의 정답기로 검증된 것은 아니다.
Confluence 사례의 값이 맞더라도 다른 테스트 보고서 인용은 별도 오류로 봐야 한다.

- [공개 프롬프트](https://github.com/princeton-nlp/ALCE/blob/246c476a4edfc564266b7346b6e29ef4861ae937/prompts/asqa_default.json)
- [인용 지지·불필요 인용 평가](https://github.com/princeton-nlp/ALCE/blob/246c476a4edfc564266b7346b6e29ef4861ae937/eval.py#L301)

### Attribute First / Self-RAG의 재사용 경계

AF 공식 코드는3단계 pipeline뿐 아니라 selection→CoT fusion의2단계도 제공한다.
따라서 우리 실패를2단계라는 이유로 설명할 수 없다. 차이는 실제 프롬프트·전달 형식·
검증기·모델·추가 검색 책임에 있다. 원 목적은 long-form QA/요약의 좁은 인용이며,
우리 모든 짧은 QA를 그 선택 단계 통과에 의존시켜야 한다는 근거는 아니다.
[공식 경로](https://github.com/lovodkin93/attribute-first-then-generate/blob/cc7b995dfb288da7982ae388994f182bef030b75/few_shot_experiments/run_full_pipeline.py)

Self-RAG의 검색 필요성/지지 판단은 reflection token 학습과 함께 설계됐다.
그 제어 역할만 일반 Qwen 지시문으로 바꾼 것을 같은 방법으로 간주하면 안 된다.
이번 우선안으로 Self-RAG 학습이나 추가 judge를 붙이지 않는다.
[저자 설명](https://selfrag.github.io/)

## 다음 설계 판단

1. 저자 검색 구현에서 실제 검색을 수행하고 원 기록을 반환하는 경로를 먼저 기준으로 삼는다.
   선택기의 optional missing_queries 판단으로 검색을 막지 않는다. dense 검색과 기존 BM25를
   같은 원문/질문/문맥 예산으로 비교할 수 있는 형태로 둔다.
2. 원 대화방/기록 식별자·작성자·날짜를 모델 입력까지 보존한다. 프로젝트 이름은
   실제 데이터에서 확인되는 경우만 쓴다. 보존한 자료를 시간순으로 읽히되 citation ID는 안정적이어야 한다.
3. 기본 독해는 원문을 받고 문단 ID를 인용한다. LongMemEval 기본 con과 direct를 구별한다.
   별도 자유 해석 계획, 필수 좁은 구절 복사, 불검증 온라인 judge를 기본 경로에 넣지 않는다.
4. 검색 실패와 독해 실패를 oracle evidence / 실제 검색으로 분리한다. 필요한 근거가
   이미 있는 S3 날짜·작성자 판단은 검색량 증가만으로 해결됐다고 주장할 수 없다.
5. 기존 점수는 유지하고 추가 진단에는 최소 필요 근거 확보, 작성자/대화방/시간 적용,
   문장별 인용 지지와 불필요 인용, 필수 답 유지, 실제 토큰 비용을 분리한다.
   Ever의 모든 R 관련 기록 회수 비율을 정답에 필요한 최소 근거 확보율로 해석하지 않는다.

이것은 다음 수정의 근거와 우선순위다. 새 구현 성능, QA 완성, 병합/재검토 해결을
주장하지 않는다. 같은10개 개발 문제의 반복 조정만으로 일반화 성능을 결론 낼 수 없다.
