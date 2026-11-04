# Evidence-Bounded Team Memory

[![Tests](https://github.com/ashcircle03/evidence-bounded-team-memory/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/ashcircle03/evidence-bounded-team-memory/actions/workflows/tests.yml)

팀원 각자의 AI가 Git으로 실험 기록을 주고받을 때, **과거 결정은 어떤 조건에서 내려졌고 새 근거가 들어오면 무엇을 다시 검토해야 할까?** 원문을 보존하고, 작성자가 검토할 병합 제안을 만들고, 각 답을 당시 출처까지 추적하는 연구 프로토타입이다.

[데모](#데모) · [시스템 구조](#시스템-구조) · [실험 결과](#실험-결과) · [재현 안내](evaluation/cpython/README.md) · [기여 안내](CONTRIBUTING.md)

## 데모

Python 3.12와 Git이 있으면 모델 다운로드 없이 두 팀원의 작업을 재생할 수 있다.

```sh
git clone https://github.com/ashcircle03/evidence-bounded-team-memory.git
cd evidence-bounded-team-memory
python3 -m team_memory demo
```

첫 번째 팀원은 시간 분할에서 성능 개선을 관측하지 못했다. 두 번째 팀원은 그룹 분할에서 개선을 관측하고 기록을 올린다. 데모는 임시 Git 저장소와 두 복제본으로 이 상황을 재현한다. 출력 JSON에서 다음 세 지점을 비교할 수 있다.

| 출력 필드 | 확인할 판단 |
|---|---|
| `after_pull_before_review` | 첫 팀원의 AI가 새 기록을 읽을 수 있다. 기존 기록은 승인 상태, 새 기록은 검토 대기 상태로 표시된다. |
| `after_both_reviews_and_pull` | 분할 조건이 다른 두 관측이 각각 출처를 갖고 남는다. |
| `unresolved_pair` | 같은 분할에서 상반된 결과가 나오면 양쪽 근거가 남는다. 이후 명시적으로 승인한 정정의 효과는 `after_explicit_correction`에서 볼 수 있다. |

이 데모의 관측값과 승인자는 가상이다. 실제 외부 문서를 사용한 평가는 아래에 따로 실었다.

## 시스템 구조

각 팀원은 자신의 체크아웃에서 CLI를 사용한다. Git이 기록을 전달하고 각 클라이언트가 같은 기록에서 검토 상태를 다시 계산한다.

| 단계 | 동작 | 구현 |
|---|---|---|
| 기록 | 원문·출처·관측 시점을 저장하고 작성자의 실험 기록을 연결한다. | [store](team_memory/store.py) · [writer](team_memory/writer.py) |
| 검토 | pull한 기록에서 조건 차이, 미해결 충돌, 정정 제안을 찾고 승인을 기록한다. | [merge](team_memory/merge.py) |
| 재검토 제안 | 새 원문과 현재 목표를 과거 결정에 대조해 작성자에게 검토할 조치를 제안한다. | [reconsider](team_memory/reconsider.py) |
| 질의 | 질문에 관련된 기록을 찾아 승인 상태를 표시한다. 모델을 쓸 때는 답이 가리키는 출처와 구절을 검사한다. | [retrieval](team_memory/retrieval.py) · [qa](team_memory/qa.py) |

명령 목록은 `python3 -m team_memory --help`로 볼 수 있다.

## 실험 결과

CPython PEP 초안 3건을 첫 공개 시점으로 복원했다. 사전에 정한 목표 5개에서 **대상 문서와 후속 조치를 모두 맞힌 횟수**는 단순 검색+Qwen이 2/5, 재검토 모듈이 1/5였다. 이 파일럿에서는 단순 검색을 기준선으로 유지한다. [목표별 비교와 당시 원문](results/cpython/report.ko.md)

두 방식이 공유하는 QA에서는 **정답 구절이 모델 입력에 9/9 있었고, 답과 출처를 함께 맞힌 결과는 0/9**였다. Qwen은 6번 기권했고 나머지 3번도 질문의 답을 담지 못했다. 같은 모델에 같은 문서로 인용 없이 답만 요청하면 2/9, 정답이 있는 구간을 미리 알려주고 답만 요청하면 8/9였다. 후자는 병목을 찾기 위한 사후 대조다. [문항별 QA 진단](results/cpython/qa-diagnosis.ko.md) · [GPU 원출력](results/cpython/outputs.json) · [대조 실험 원출력](results/cpython/qa-control-outputs.json)

- [CPython 평가 재현](evaluation/cpython/README.md) — GPU 없이 모델 입력을 복원하고 저장된 응답을 재채점한다.
- [사전 평가 계획](evaluation/cpython/PLAN.md) — 평가 대상과 성공·보류 조건을 확인한다.
- [Aimers 및 EverMemBench-Dynamic 개발 기록](results/development.ko.md) — 초기 설계와 개발셋 결과를 읽는다.
