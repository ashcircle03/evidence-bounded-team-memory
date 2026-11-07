# 개발·실험 프로세스 추가 감사

2026-11-07. 평가 지표와 모델 선정 감사에 이어 실행 경로, 계약, 재현 환경,
테스트와 실험 의사결정 구조를 점검했다. 아래 재현은 로컬에서 수행했으며
모델 호출·서버 작업·기존 동결 코드 및 점수 변경은 없다.

## 우선 처리할 확인 사항

### 1. 독해 실험 경로와 실제 입력 경로가 다르다

`evaluation/reference_qa/documents/run.py:89`는 legacy의 고정 sources를 reader에
직접 넣는다. Ever도 별도 prepare에서 생성한 witness를 사용한다. 이 실험 자체는
유효하지만 import_history→검색→QA 전체 경로의 보존 검사가 아니다.

재현: `ReferenceQA._witness`에 source의 observed_at이 존재하는 입력을 주면
반환에는 source_id/quote/start/end/location/speaker만 있고 observed_at은 없다.
그 반환을 새 documents reader의 documents()에 넣으면 recorded_at=None이다.
초기 CitationQueryEngine의 prompt에는 날짜 metadata가 들어갈 수 있지만
반환 witness를 받는 후속 모듈에서 날짜를 복원할 수 있다는 보장은 없다.
최근 실험 입력에는 날짜가 실제로 있었으므로 그 결과가 잘못됐다는 뜻은 아니다.

조치: 팀원이 사용할 실제 import/ask 진입점 하나에서 재시작까지 포함한 작은
계약 검사를 둔다. source_id·원문·작성자·기록시간·대화방·검토상태가 어느 경계에서
필수인지 명시하고 실제 출력에서 확인한다. reader에 이상적인 입력을 바로 넣은
단계 검사는 유지하되 end-to-end 증거와 구분한다.

### 2. '기존 답 보존' 보호의 범위가 제한적이다

`reference_fallback.preserve_answer`는 예외가 발생하면 이전 결과를 보존한다.
성공 응답이 의미적으로 틀린 경우까지 막는 함수는 아니다.
`reference_attributed._repair_omitted_answer:52`는 status와 source ID 포함 관계로
교체를 허용한다. 코드 주석도 semantic verifier가 아님을 명시한다.

재현: A가10, B가20이라고 하는 fixture에서 기존 답10[1]에 대해 수정 응답
999[1][2]를 반환하는 stub을 연결하면 aqa_candidate_accepted=True다.
두 ID가 남아도 기존 답이나 조건은 보존되지 않는다. 실제 Qwen이 이 fixture에서
999를 생성했다는 결과가 아니라 교체 규칙의 보장 범위를 보여주는 결정적 반례다.

조치: 소스 ID 보존을 의미 보존으로 부르지 않는다. original/candidate/채택 사유를
명시적으로 보존하고, 추가 정보 보강과 기존 주장의 대체를 서로 다른 동작으로 둔다.
다른 LLM judge를 하나 더 붙이면 해결된다고 가정하지 않는다. 실제 원문을 기준으로
값·조건·상충 답이 바뀌는 회귀와 무변경 대조를 먼저 구성한다.

### 3. 권장 구현과 기본 실행 경로가 일치하지 않는다

- 결과 decision은 selected_profile=attributed다.
- reference_qa CLI default는standard다.
- practical-usage는PracticalCUPMemService(strategy='simple')를 안내한다.
- 최신 documents는별도source 입력용 API/CLI로 남아 있다.

각 문서는 범위를 설명하고 있어 명시적 옵션으로 실행할 수 있다. 그러나 '우리 모델을
돌린다'는 동일한 말로 서로 다른 경로를 실행할 여지가 있다. reference 모듈15개가
있다는 것 자체가 실행 복잡도의 증거는 아니지만 supported/experimental/replay-only
구분이 호출자에게 자동으로 전달되지 않는다.

조치: 하나의 지원 실행 명령과 manifest를 정하고 model/profile/schema/source revision을
응답 메타데이터에 남긴다. 과거 실험 코드는 재현용으로 보존하되 제품 경로에서 고르는
실험 옵션 목록과 분리한다. 기존 고정 구현을 임의 변경하는 대신 버전 있는 실행 설정을 쓴다.

### 4. 코드 해시 동결과 환경 재현은 별개다

documents-v1은 code/config/data 해시와 Qwen revision을 보존했다. 이 강점은 유지한다.
하지만 실제 client는 과거 cup-ref-qa-v1/reference-env의 Python을 exec하고,
quote-v2와fix-v1의 reference-extra 디렉터리를 PYTHONPATH로 합친다.
CONDA_PREFIX 검사는 그 문자열만 확인하며 실제 client interpreter를 증명하지 않는다.
모델 서버의 conda Python과 client의 venv Python이 다른 혼합 환경이다.

최근 packet에는 이 외부 환경 전체의 dependency lock/hash, 실제 import 경로,
embedding 가중치 digest가 포함되지 않는다. 이것은 환경이 변했다는 증거가 아니라
현재 동결 자료만으로 새 환경을 똑같이 복원했음을 증명할 수 없는 범위다.

조치: 모델 서버와 client 각각 sys.executable, Python/Torch/Transformers/vLLM/주요
라이브러리 버전과 import 위치, 모델·tokenizer·embedding revision을 남긴다.
과거 작업 디렉터리 여러 개를 전제로 하지 않는 설치 명령/lock을 만든다.
새 환경에서 작은 실행을 확인한 뒤 의미 성능 실험을 한다.

### 5. 로컬 테스트와 깨끗한 설치 환경의 테스트가 다르다

현재 .github/workflows/tests.yml은 Python3.12를 설정하고 unittest discover를 실행하지만
새 reference 의존성 설치 단계가 없다. 최신 tests/test_reference_documents.py는
llama_index를 사용하는 모듈을 최상단에서 import한다.

로컬 stdlib-only 모의 환경(`python3 -S -m unittest tests.test_reference_documents`)에서
ModuleNotFoundError: llama_index를 재현했다. 이 실행은로컬Python3.14였고 실제 GitHub
CI를 실행한 것이 아니다. 따라서원격CI 실패를관측했다고주장하지 않는다.
다만 현재 workflow에 새 테스트를 포함할 때 의존성 설치 경로가 필요함은 확인했다.

조치: 기본 저장/상태 계약 테스트와 reference 의존성 테스트 job을 명확히 분리하고
후자에는 고정 설치 단계를 둔다. 단순 skip으로 전체 성공처럼 보이게 하지 않는다.
현재 많은 reference 파일이 untracked이므로 팀 공유용 commit/manifest를 만들기 전
클린 체크아웃 재현도 필요하다. 기존 tar/hash 실행 기록은 별도 재현 근거로 유지한다.

## 실험 의사결정에서 추가로 개선할 사항

### 6. 레퍼런스 도입과 효과 검증 사이에 호환성 확인이 약하다

NOTICE에는 변경점이 잘 기록되어 있다. 그러나 모델·예시·출력 형식·문단 단위·원 과제의
가정이 바뀐 어댑터가 여럿이다. LongMemEval의 원 데이터 변환 대신우리 chunk를 쓰거나,
Attribute First의출력을 typed short-answer로바꾼것은 정당한연구선택일 수 있지만
원 방법의효과가 그대로넘어온다고가정할 수 없다.

조치: 각 도입에 원 문제/필수 가정/그대로 가져온 코드/바꾼 부분/기대 효과/실패 시
판단을 짧게 연결한다. 계산·파싱의등가성을점검할 수 있는부분은원구현과같은입력으로
비교한다. 가능한작은공식예제로환경과프로토콜연결부터확인하며 매번논문전체재현을
선행조건으로강제하지는않는다.

### 7. 개별 실험은 동결하지만 연구 전체의 중단·재검토 조건은 약하다

개별 PROTOCOL과freeze는많이있지만 전체decision에는과거추천/실험기각/새후보가
여러중첩필드로누적된다. root progress에는latest_job120296과함께job_id119960,
answer_and_citation20, remaining0가남는다. 이것은과거선택결과와최신실험결과의
범위혼합이며프로젝트전체해결로오독할수있다.

조치: 한 실험이 어떤 개발 결정을 바꿀 수 있는지 먼저 적고, 이전과 다른 가정이
없으면 재실험하지 않는다. '이 방법이 틀렸다' 대신 정확한 모델·입력·변경점에서
지원되지 않은 가설과 재검토 조건을 남긴다. 완료 상태도 실행 완료/채점 완료/
채택 여부/제품 연결 완료를 분리한다. 모든 이전 판단을 새벽부터 다시 읽어야만
현재 상태를 알 수 있는 기록 구조를 줄인다.

### 8. 비용 비교의 범위와 공정성

실제 GPU 사용에 준비시간을 포함한 점은 좋다. 다만고정된direct→con 및BM25→dense
순서와모델prefix cache가있어관측latency를방법자체의속도로바로해석할수없다.
기존costs.json은arm별token과작업전체GPU시간을기록하지만색인구축/준비/단건질의의
상각범위를분리하지않는다. 출처입력만읽는CLI도사용하지않는embedding을로드한다.

조치: 색인구축비용, cold/warm 준비비용, 질의당비용을나누고순서를균형배치한다.
이는정확도실험을더많이하자는뜻이아니며기존실행기록에비용의범위를명확히하자는뜻이다.
GPU12시간 walltime은유지하고, 별도로계획한호출/입력처리가끝나면종료하는현재방식도유지한다.

## 권장 우선순위

1. 실제 지원 입출력 경로와 버전 계약 하나를 정하고 날짜 유실/보존 보장 범위를 정리.
2. 깨끗한 환경의 설치·테스트·실제 작은 통합 실행을 성립시킴.
3. 직전 평가·모델 선정 감사의 calibration과 동일 기준선 비교를 수행.
4. 그 뒤에 근거가 확인된 병목 하나만 바꾸고, 채택/기각 조건에 따라 한 번 결정.

새 평가 프레임워크나 더 많은 모델 단계를 만드는 것이 이 감사의 해결책은 아니다.
서버 제출 장부, 명시적 입력/출력 저장, 원문 해시, 실패 결과 보존은 이미 있는 장점이므로 유지한다.
