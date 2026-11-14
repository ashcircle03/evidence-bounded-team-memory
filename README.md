# Evidence-Bounded Team Memory

[![Tests](https://github.com/ashcircle03/evidence-bounded-team-memory/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/ashcircle03/evidence-bounded-team-memory/actions/workflows/tests.yml)

**팀이 Git으로 공유하는 기록에서 조건·출처·승인 상태를 보존하며 답하고, 과거 결정의 재검토를 제안하는 연구 프로토타입.**

[팀 개발 계약](docs/modules/README.md) · [모듈 지도](docs/architecture.md) · [시작하기](#시작하기) · [JSONL API](docs/service-v2.md) · [개발 안내](CONTRIBUTING.md) · [평가 결과](results/README.md) · [전체 문서](docs/INDEX.md)

## 할 수 있는 일

- 원문·작성자·시간을 보존하고, 질문에 대한 답과 원문 근거를 반환한다.
- 새 기록을 과거 기록과 비교해 정정·재검토·상충 후보를 만든다.
- 제안과 작성자 승인을 구분하고, 원문과 검토 상태를 각각 인용한다.
- 각 checkout에서 독립적으로 동작한다. Git 전송, 인증, MCP와 UI는 호출자가 맡는다.

**자동 지식 병합이 완성된 시스템은 아니다.** 재검토를 정정으로 오분류하거나 불필요한 제안을 만드는 문제가 남아 있다. 답변의 `ok`와 정확한 인용 위치가 의미 정답을 보장하지 않는다.

## 모듈 구조

팀 협업은 **records / relations / retrieval / answering / gateway** 다섯 책임으로 나눈다. [입출력·권한·실패 계약 v1.1](docs/modules/README.md), [실제 v2 연결·사용법](docs/modules/runtime.md), [공통 예제와 독립 테스트](examples/contracts/README.md)를 먼저 읽는다. 어댑터는 opt-in으로 연결됐으며 기존 v2 API도 유지한다. 새 경로의 분기 Git 자동 병합은 아직 지원하지 않는다.

```text
team_memory/
├── service.py            # 공개 JSONL API와 전체 흐름 조정
├── contracts/            # 협업용 schema·ports·검증·conformance (v2와 구분)
├── adapters/             # 기존 v2를 다섯 포트로 연결하는 실제 구현
├── storage/              # 불변 객체·원문 저장
├── review/               # 관계 비교·근거 결합·제안·작성자 검토 상태
├── readers/              # 검색·QA·상태 문맥·인용
├── experiments/          # 별도 평가한 reader와 패치 후보
└── _vendor/              # 재사용한 외부 구현·프롬프트·라이선스
evaluation/               # 데이터 구성·동결 기준·재생·채점
results/                  # 측정 결과·실패·원출력·판정 기록
tests/                    # 저장·상태·모듈 연결·전송·회귀 계약
docs/                     # 설계 의도·입출력·개발·연구 이력
```

| 수정할 대상 | 구현 진입점 | 책임과 계약 |
|---|---|---|
| 원문·저장 형식 | [storage/](team_memory/storage/) | [저장소 계약](team_memory/storage/README.md) |
| 정정·재검토·작성자 검토 | [review/](team_memory/review/) | [관계와 상태 계약](team_memory/review/README.md) |
| 검색·답변·인용 | [readers/](team_memory/readers/) | [reader 단계별 입출력](team_memory/readers/README.md) |
| API 연결·오류 반환 | [service.py](team_memory/service.py) | [요청·응답 명세](docs/service-v2.md) |
| 새로운 실험 후보 | [experiments/](team_memory/experiments/) | [기본 경로와의 경계](team_memory/experiments/README.md) |

기존 `team_memory.reference_*`, `timeline`, `source_store` import와 실행 명령은 호환 경로로 유지한다. 새 코드는 위 경로를 사용한다. `store.py`는 과거 데이터셋의 해시 검증에 묶인 원본이므로 그대로 보존한다. [호환·과거 경로 안내](docs/architecture.md).

## 시작하기

Python3.11 이상과 Git이 필요하다. 모델 없이 공유·검토 과정을 확인하는 **고정 응답 데모**:

```sh
git clone https://github.com/ashcircle03/evidence-bounded-team-memory.git
cd evidence-bounded-team-memory
python3 -m team_memory demo
python3 -m team_memory demo --followup
```

실제 QA 개발 환경:

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -e '.[reference,dev]'
```

모델·tokenizer·임베딩·NLTK 자료는 [환경 안내](docs/evaluation-guide.md)에 따라 별도로 준비한다. 패키지 설치가 모델을 내려받거나 GPU 작업을 제출하지 않는다.

```sh
.venv/bin/python -m team_memory.service \
  --store /path/to/checkout/shared-records \
  --model-path /path/to/Qwen3-8B \
  --embedding-path /path/to/embedding \
  --api-base http://127.0.0.1:PORT/v1 \
  --reader attributed < requests.jsonl > responses.jsonl
```

기본 reader는 `attributed`, 단순 비교 경로는 `direct`다. 설치 후 `team-memory` 명령도 같은 API를 실행한다. [API 명세와 요청 예제](docs/service-v2.md)를 참고한다. Aurora 계산은 Slurm 할당에서 수행하며 로그인 노드에서는 실행하지 않는다.

## 검증과 현재 한계

기존 개발20문항의 핵심 답·필요 근거는 마지막 완료된 실행에서20/20 유지됐다. 하지만 알려진 재검토 양성2건의 관계 분류는0/2이며, 무관한 보고2건에도 불필요한 제안을 만들었다. 이는 소규모 개발 결과이며 독립 벤치마크 성능이 아니다.

- [최근 완료된 구현·상태 검증](results/module-boundary/README.md)
- [비교기8B/14B의 채택 판단](results/comparator-choice/README.md)
- [원형과 현재 모듈 연결 감사](docs/reference-composition-audit.md): 후속 동일근거 비교는 별도 실행 기록으로 관리한다.
- [실험 결과 상세와 이전 비교](docs/status-2026-11-08.md)

```sh
.venv/bin/python scripts/check.py core
.venv/bin/python scripts/check.py reference --fail-on-skip
```

reference 검사는 캐시된 tokenizer와 NLTK 자료, stub 모델·로컬 HTTP 서버를 사용한다. 실제 모델 추론 점수와 구분한다. 준비물과 전체 검사는 [기여 안내](CONTRIBUTING.md)에 있다.

## 기여와 라이선스

변경할 모듈의 책임과 실패 사례부터 확인하고, 기존 답·근거와 상태 계약을 유지하는지 검증해 주세요. [개발 절차](CONTRIBUTING.md) · [평가 재현](evaluation/README.md).

**팀 코드의 재사용 라이선스는 아직 결정 전이다.** 공개 저장소를 오픈소스 라이선스 부여로 해석하지 않는다. 외부 구현·자료의 LICENSE/NOTICE는 각각 유지한다. 모델 가중치와 인증정보는 포함하지 않는다.
