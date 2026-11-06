# QA20: 팀 공유용 고정 평가 패키지

원문 검색·작성자 식별·상충 답 보존·조건별 답변을 확인하는 **기존 개발/회귀20문항**이다. 새로운 비공개 테스트셋, 전체 EverMemBench, Git 재검토20흐름과 구분한다. 이 폴더만 복사해도 데이터 검증·요청 생성·채점 집계가 가능하다. 도구는 Python3.10 이상 표준 라이브러리만 사용한다.

## 바로 가져오기

```bash
git clone https://github.com/ashcircle03/evidence-bounded-team-memory.git
cd evidence-bounded-team-memory/evaluation/qa20
python3 evaluate.py verify
```

예상: `packet_valid: true`, `histories: 7`, `questions: 20`.

기존 실제 출력과 판정을 재집계하여 도구를 확인할 수 있다. **이 명령은 모델을 실행하지 않는다.**

```bash
python3 evaluate.py score \
  --predictions reference/checked-v1-predictions.jsonl \
  --ratings reference/checked-v1-ratings.json
```

예상: `answer_and_required_citation: 19`, `invalid_original_citations: []`. 부연 문장의 인용 누락2건은 별도 진단에 남는다.19/20이 모든 부연 문장의 인용 완전성을 뜻하지 않는다.

## 무엇이 들어 있나

| 파일 | 용도 | 모델에게 제공 |
|---|---|---|
| `data/inputs.json` | 원래 순서를 보존한7개 전체 기록 묶음과20개 질문 | 예 |
| `data/questions.jsonl` | 문항 ID·history ID·원래 질문 문자열 목록 | 예 |
| `evaluator/key.json` | 필수 답·조건·근거 출처·기존 기준 | **아니오: 채점자 전용** |
| `reference/*predictions.jsonl` | 공개된19/20 구성의 실제 답과 반환 인용 | 아니오 |
| `reference/*ratings.json` | 그 출력에만 해당하는 기존 판정과 이유 | 아니오 |
| `reference/requirements-baseline.txt` | 기존 구성의 선택 의존성 버전 | 실행 환경 참고 |
| `manifest.json` | 데이터·도구 해시, 출처 커밋, 구성 정보 | 검증용 |
| `evaluate.py` | 검증, 요청 생성, 출력 변환, 판정 양식, 집계 | 평가 도구 |

데이터는 공개 커밋 `bd3d36cb5d3a51461ba81f9c64367a256bbacddf`의 `evaluation/cupmem/practical/legacy.json`과 `legacy-key.json`에서 **바이트 그대로** 가져왔다. 원문 저자·위치·시각과 원래 출처 표기를 유지하며 새로 라이선스를 부여하지 않는다.

| 구성 | 문항 수 |
|---|---:|
| 공개 Git 문서 일반 QA |5|
| 공개 Python PEP 일반 QA |8|
| 공개 문서에 통제 반대 기록을 추가한 상충 QA |3|
| 조건이 다른 기록의 공존 QA |1|
| EverMemBench-Dynamic 원본에서 발췌한 QA |3|
| 합계 |20|

기록 입력은 묶음 간 중복을 포함해1,276건, 전체에서 중복 제거한 원문은786개다. 질문 문구가 같고 기록 조건만 다른 사례도 있으므로 독립적인 자연 질문20개라고 부르지 않는다.

## 자신의 모듈로 새로 평가하기

1. **기록 묶음마다 메모리를 초기화**한다. 다른 묶음의 반대 기록이나 정답이 섞이면 안 된다. 같은 묶음 안에서는 입력·질문 순서를 유지한다.
2. 전체 `import_history.records`를 제공하고 각 `ask.question`을 실행한다. 정답 문단만 미리 골라 주거나 기록을 생략하지 않는다. `question`은 질문과 `as_of`를 담은 JSON **문자열**이다. 기존 실행과 같은 입력을 비교하려면 그대로 전달한다. 해석해 프롬프트를 바꿨으면 변경 사항을 보고한다.
3. 모델 입력에는 `data/`만 사용한다. `evaluator/`, `reference/`의 정답·기존 답·선택 근거를 사용하지 않는다. 실제 요청/응답과 모델·검색 설정을 별도로 보관한다.
4. 다음 형식의 `predictions.jsonl`을 문항당 한 줄, 정확히20줄 만든다. 실패 문항도 생략하지 않고 빈 답·빈 인용·`status: "error"`로 남긴다.

```json
{"id":"legacy-d474ab3d7822c8ac/qa-0","answer":"모델의 실제 답변 [1]","citations":[{"number":1,"source_id":"원문 ID","quote":"선택한 원문 구절","start":0,"end":10}],"status":"ok"}
```

위는 형식 설명이며 실제 정답 예제가 아니다. `start/end`는 **원문 문자열의0부터 시작하는 문자 위치이며 end는 미포함**이다. 바이트 위치나 UTF-16 단위로 바꾸지 않는다. `source_id`는 `evaluate.source_id(record)`로 만들 수 있다. 원문 envelope를 `ensure_ascii=False, sort_keys=True, indent=2` JSON으로 직렬화하고 줄바꿈을 붙인 UTF-8의 SHA256 앞24자리다. `location`, `speaker`를 인용에 추가하면 원문과 일치해야 한다. 번호 인용을 쓴다면 `number`에 실제 답의 인용 번호를 기록한다. 선택된 인용이 한 개뿐이어도 답이[3]을 썼다면 번호를1로 다시 매기지 않는다. 답변의 인용 표기가 어떤 인용 객체를 가리키는지도 채점자가 확인한다.

기존 JSONL 모듈 인터페이스를 사용할 때는 요청 파일을 자동 생성할 수 있다. `requests`는 새 폴더를 요구하고 기존 입력을 덮어쓰지 않는다.

```bash
python3 evaluate.py requests --out requests
```

생성된7개 `requests/<history-id>.jsonl`을 각각 별도의 깨끗한 저장소에서 실행한다. 첫 줄은 전체 기록 적재, 뒤의 줄은 질문이다. 한 요청당 JSON 응답 한 줄을 같은 이름의 `responses/<history-id>.jsonl`에 저장한다. 기존 모듈의 `raw`와 `answers[].evidence` 응답은 다음 명령으로 변환한다.

```bash
python3 evaluate.py collect --responses responses > predictions.jsonl
```

직접 `predictions.jsonl` 형식으로 출력하는 모듈은 `collect`가 필요 없다.

## 같은 기준으로 채점하기

```bash
python3 evaluate.py ratings --predictions predictions.jsonl > my-ratings.json
# evaluator/key.json과 실제 원문을 보며 my-ratings.json의 null과 reason을 작성한다.
python3 evaluate.py score --predictions predictions.jsonl --ratings my-ratings.json
```

판정은 문항별로 다음을 적는다.

- `answer_correct`: 필수 답과 조건이 모두 맞는가. 상충 사례는 양쪽 기록을 보존하고, 공존 사례는 조건을 구분했는가.
- `citations_support_answer`: 선택한 인용이 그 답과 조건을 실제로 지지하는가. 답에 쓰인 번호와 인용 객체의 연결도 확인한다.
- `unsupported_extra_claims`: 근거 없는 추가 주장이나 다른 대상/동작에 대한 답을 섞었는가.
- `claim_level_citation_gap`: 필수 답 이외의 부연 문장에 인용 누락이 있는가. 기존 필수 답 점수와 별도로 기록한다.
- `reason`: 원문을 기준으로 한 판정 이유. 모르는 항목을 자동으로 정답 처리하지 않는다.

기존 일차 성공 기준은 **답 정확 + 인용 지지 + 근거 없는 추가 주장 없음**이다. 도구는20문항 누락·중복, 인용의 원문 ID·문자 위치·문자열 일치를 검사하고 명시한 의미 판정을 집계한다. **의미 정답을 자동 판단하는 스크립트가 아니다.** 인용 문자열이 있다는 사실만으로 의미적 지지를 인정하지 않는다. 실제 모델에게 어떤 문맥을 보냈는지는 별도 호출 로그가 필요하다.

판정 파일은 예측 파일의 SHA256에 묶인다. 새 모델 출력에 기존19/20 판정 파일을 그대로 사용하면 거절된다. 채점 기준을 적용할 때는 모델 이름을 가리고 독립된 팀원이 판정하는 편이 좋다. 기존 참조 판정은 개발에 참여한 AI가 작성했으며 독립 사람 평가가 아니었다.

## 기존 Qwen 기준선을 다시 실행하려면

데이터와 기준의 공유는 모델 가중치를 포함하지 않는다. 기준선 구현은 위 공개 커밋의 `team_memory.reference_qa --profile checked`이다. 진행 중인 수정과 섞이지 않도록 해당 커밋을 별도 checkout해서 사용한다.

- Qwen/Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`, BF16, 비사고 모드, temperature0, 문맥32,768, 생성 상한1,024.
- vLLM0.8.5.post1의 로컬 OpenAI 호환 endpoint, 모델 이름 `Qwen3-8B`. 문서 판정은384토큰 상한이며 동일 모델을 사용한다.
- 동일한 팀 임베딩 가중치 폴더를 사용한다. 보존된 설정은 MiniLM-L6-H384 계열, mean pooling·L2 정규화·최대256토큰이다. 모델 이름만 보고 다른 가중치로 대체하면 동일 검색 조건이 아니다. [보존된 설정](../../results/reference-qa/embedding-config/comparison.json)을 참고한다.
- Python 환경은 `reference/requirements-baseline.txt`, 실제 호출은 [원래 실행 설정](../../results/reference-qa/parse-v1/config.json)을 참고한다. 서버의 절대 경로는 각자 환경으로 바꾸되 가중치·설정은 기록한다.
- Aurora에서 실행한다면 GPU를 포함한 Slurm 계산 노드와 conda 환경에서 실행한다. 로그인 노드에서 모델·색인을 실행하지 않는다. 이 패키지는 작업을 자동 제출하지 않는다.

계산 노드에서 모델 서버와 의존성을 준비한 후, 기존 CLI에 요청을 전달하는 형태는 다음과 같다. 각 반복의 STORE_ROOT 아래 저장소는 처음에는 없어야 한다. `PYTHONPATH`는 고정 커밋을 checkout한 코드 경로로 지정한다.

```bash
# 아래 경로 변수들은 자신의 환경에서 지정한다.
# QA20_PYTHON: 의존성이 설치된 Python, QA20_CODE: 고정 커밋 checkout 경로
# QA20_MODEL: Qwen 가중치, QA20_EMBED: 동일 임베딩 가중치
# QA20_API: 예 http://127.0.0.1:8000/v1, QA20_STORES: 새 저장소 경로
mkdir responses
for request in requests/*.jsonl; do
  history="$(basename "$request" .jsonl)"
  PYTHONPATH="$QA20_CODE" "$QA20_PYTHON" -m team_memory.reference_qa \
    --profile checked --store "$QA20_STORES/$history" \
    --model-path "$QA20_MODEL" --embedding-path "$QA20_EMBED" \
    --api-base "$QA20_API" < "$request" > "responses/$history.jsonl"
done
python3 evaluate.py collect --responses responses > predictions.jsonl
```

환경에 따라 개인 NLTK 데이터(`stopwords`, `punkt_tab`)가 필요하다. [기준선 환경 안내](../../docs/reference-reuse.md#사용)를 따른다. 모델·서빙 구현 차이에 따른 출력 차이가 있을 수 있으므로 새 실행의19/20을 미리 보장하지 않는다. 제공한 참조 출력은 기존 실제 호출과 파서 복구 재생의 결과이며, 이 패키지를 만들면서 새 GPU 추론을 실행한 것은 아니다.
