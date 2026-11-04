# Evidence-Bounded Team Memory

팀원 각자의 AI가 Git으로 원문 기록을 공유할 때, 예전에 **무엇을 어떤 조건에서 결정했는지** 찾아 다시 쓸 수 있는지 연구하는 캡스톤 프로젝트다. 새 기록이 과거 판단에 영향을 주면 원작성자가 검토할 제안을 남긴다. 질문에 답할 때는 당시 출처와 승인 상태를 함께 확인한다.

예를 들어 한 팀원이 특정 블렌드에서 모델을 기각한 뒤, 다른 팀원이 다른 구성에서 개선을 측정할 수 있다. 검토할 사안은 새 구성이 원래 조건에서도 비교할 가치가 있는지다. 두 팀원의 관측은 각각 원래 조건과 출처에 연결해 보존한다.

## 현재 결과

CPython의 실제 기록 3건을 각각 처음 공개된 시점으로 복원해 5개 목표를 평가했다. 같은 Qwen2.5-3B-Instruct를 쓴 단순 검색과 재검토 모듈 모두 다섯 번 ‘기존 판단 유지’를 골랐다. **관련 과거 문서와 조치를 함께 맞힌 수는 단순 방식 2/5, 모듈 1/5**였다. 일반 QA에서는 정답을 뒷받침하는 구절이 아홉 번 모두 입력에 있었지만 답과 인용을 함께 맞힌 경우는 0/9였다. 현재 연구 판단은 단순 방식을 비교 기준으로 유지하고 재검토 모듈의 채택을 보류하는 것이다.

- [5개 목표와 QA 문항별 비교](results/cpython/report.ko.md)
- [평가 전에 고정한 기준](evaluation/cpython/PLAN.md) · [원출력](results/cpython/outputs.json) · [문항별 답과 인용 검증](results/cpython/score.json)
- [초기 Aimers·EverMemBench-Dynamic 실험 요약](results/development.ko.md)

## 실행해 보기

Python 3.12와 Git이 있는 환경에서 아래 두 명령을 실행한다. 기본 데모와 테스트는 Python 표준 라이브러리를 쓴다. 데모는 임시 Git 저장소와 두 복제본을 만들고, 팀원이 올린 기록의 승인·상충·정정을 차례로 재생한다.

```sh
python3 -m unittest discover -s tests -q
python3 -m team_memory demo
```

## 코드에서 살펴볼 곳

| 기능 | 진입점 |
|---|---|
| 원문·결정·검토 기록 저장 | [store.py](team_memory/store.py) · [merge.py](team_memory/merge.py) |
| 새 원문에 근거한 재검토 제안 | [reconsider.py](team_memory/reconsider.py) |
| 검색 결과에서 답과 인용 생성 | [retrieval.py](team_memory/retrieval.py) · [qa.py](team_memory/qa.py) |
| 각 팀원의 로컬 CLI | [명령 구현](team_memory/__main__.py) · `python3 -m team_memory --help` |

## CPython 결과 재생

기록 복원과 저장된 Qwen 출력의 재채점에는 GPU가 필요하지 않다. 저장소 루트에서 다음 명령을 실행한다. `build.py`는 고정된 CPython PEP 커밋과 각각의 첫 부모를 사용한다. `assess.py`는 사전 기준과 모델 입력 해시를 검사한 뒤 저장된 출력을 재생한다. 새 채점 파일에는 자동 채점값이 담기며, 공개된 [상세 검증 파일](results/cpython/score.json)에는 원문 행까지 대조한 결과가 추가로 들어 있다.

```sh
mkdir -p .cache
git clone --bare --single-branch --branch main --no-tags https://github.com/python/peps.git .cache/peps.git
python3 evaluation/cpython/build.py .cache/peps.git evaluation/cpython/inputs.json.gz
PYTHONPATH=. python3 evaluation/cpython/retrieve.py evaluation/cpython/inputs.json.gz evaluation/cpython/packets.json.gz .cache/ranks.json
PYTHONPATH=. python3 evaluation/cpython/assess.py .cache/ranks.json .cache/score.json --run results/cpython/outputs.json
```

프로젝트는 CPython PEP 문서를 당시 Git 객체에서 복원한다. 원문과 각 PEP의 저작권 표기는 [python/peps](https://github.com/python/peps)에서 볼 수 있다. 독립 검토에 참여할 때는 결과표를 열기 전에 [검토 양식](evaluation/cpython/review.md)과 복원한 입력만 사용한다.
