# 팀 지식 QA와 재검토 파일럿

[사전 계획](PROTOCOL.md) · [문항 및 채점 기준](cases.json) · [실험 동결 정보](freeze.json)

실행 코드는 `c0a56a7`에서 고정했다. 평가 사례는 그 이후에 작성했다. 두 방식에 각각 52개 입력이 있다. 모델에 전달하는 패킷에는 질문 또는 프로젝트 목표와 해당 방식이 검색한 원문만 들어간다. 정답과 기대 조치는 재생·채점 단계에서 사용한다.

| 묶음 | 각 방식의 횟수 | 무엇을 확인하는가 |
|---|---:|---|
| 일반 QA | 10 | 고정된 Git 커밋의 서로 다른 PEP 10건에서 답과 실제 출처를 함께 반환 |
| 무관한 충돌 | 10 | 같은 질문에 해당 프로젝트의 회의 일정에 관한 상충 기록 두 개를 추가했을 때 기존 정답 보존 |
| 답이 갈리는 충돌 | 10 | 같은 사안에 다른 값을 보고한 가상 기록을 추가했을 때 두 값과 각각의 출처 반환 |
| 재검토 | 20 | 이전 결정 20건 중 올바른 결정을 찾아 실제 조건 변화에 대응. 재검토 필요 10건과 현행 유지 10건 |
| 개발 회귀 | 2 | 기존에 맞혔던 EverMem topic 01 질문에서 정확한 답과 같은 출처 보존 |

원래 QA의 검색 모집단은 각 PEP의 첫 140줄, 총 16개 문서다. 앞선 CPython GPU 입력에 이 10개 목표 PEP가 직접적인 근거 문서로 들어간 경우는 없었다. 같은 CPython 생태계의 선별 사례로 다른 프로젝트에서의 성능을 대표하지 않는다. 충돌은 연구자가 만든 반사실적 보고이며 번호 붙은 원본 PEP는 변경하지 않았다. 재검토 20건은 이 프로젝트가 작성한 모의 업무 기록이다. 사람 간 독립 주석 일치도는 측정하지 않았다.

## 데이터 준비와 입력 재현

저장소 루트에서 실행한다. 표준 라이브러리와 Git이 필요하다. `/path/to/topic-01/dialogue.json`은 고정 리비전의 EverMemBench-Dynamic에서 받는 원본 파일이다. 코드는 2025년 1월의 원문 528개만 사용한다. [PEP 원문 이력](https://github.com/python/peps) · [EverMem 원본과 리비전](https://huggingface.co/datasets/EverMind-AI/EverMemBench-Dynamic/tree/a6b210a32248e841967b7b64a64281d2ff3f669d/01)

```sh
mkdir -p .cache
git init --bare .cache/pilot-peps.git
git --git-dir=.cache/pilot-peps.git fetch --depth=1 https://github.com/python/peps.git 16991a9ce7b223b38f0b473f51a8a7d94c8b9249
PYTHONPATH=. python3 evaluation/team_pilot/pilot.py prepare .cache/pilot-peps.git /path/to/topic-01/dialogue.json .cache/pilot-packets.json
python3 -c 'import hashlib,json,pathlib; d=pathlib.Path(".cache/pilot-packets.json").read_bytes(); assert hashlib.sha256(d).hexdigest()==json.load(open("evaluation/team_pilot/freeze.json"))["packet_sha256"]; print("104 inputs match")'
```

## 실제 Qwen 응답으로 Git 재생하기

위 bare PEP 저장소만 준비하면 모델과 EverMem 데이터 없이 실행할 수 있다.

```sh
PYTHONPATH=. python3 evaluation/team_pilot/git_replay.py .cache/pilot-peps.git
```

공개 PEP 원문에서 시간대 폴백을 묻는 질문과, 과거 결정 20건이 있는 두 복제본의 후속 측정 도착을 재생한다. 실제 GPU 응답은 시스템·사용자 입력 해시가 정확히 맞을 때만 사용한다. 출력에서 QA의 원문 위치, 작성자 검토 전의 두 인용, 검토 승인 후에도 남은 원기록을 확인할 수 있다. 업무 기록과 승인 행위는 모의 사례이며 모델 응답은 작업 119269의 실측값이다.

## Qwen 실행과 채점

같은 모델 리비전과 BF16, 입력 최대 8,192토큰, 응답 최대 64토큰, greedy decoding을 두 방식 모두에 쓴다. `infer.py`는 CUDA, PyTorch, Transformers와 로컬 모델 가중치가 필요하다. 실행 중에는 문항별 원출력을 남기며 104개 모두 완료된 경우에만 완성된 결과 파일을 쓴다. GPU 작업 전에 입력 해시를 확인한다.

```sh
python3 evaluation/team_pilot/infer.py .cache/pilot-packets.json /path/to/Qwen2.5-3B-Instruct .cache/pilot-run.json local-run
PYTHONPATH=. python3 evaluation/team_pilot/pilot.py replay .cache/pilot-peps.git /path/to/topic-01/dialogue.json .cache/pilot-outcomes.json --recording .cache/pilot-run.json
python3 evaluation/team_pilot/score.py .cache/pilot-outcomes.json .cache/pilot-graded.json
```

`simple`은 구절별 BM25로, `candidate`는 구절 순위에 문서 맥락·문서별 노출 한도·결정 및 관측 단서를 더해 같은 Qwen에 보낼 근거를 고른다. 두 방식의 응답 형식과 최대 구절 수는 같다. 자동 채점은 답의 사전 별칭, 출처, 구절, 조치를 검사한다. 실제 질문에 답하는 문맥인지 검토한 판정은 자동값과 분리한다.

[최종 평가와 채택 판단](../../results/team_pilot/README.md) · [동결한 입력의 문항별 근거 포함 여부](../../results/team_pilot/input-coverage.json)

## 답과 인용을 함께 검토하기

자동 채점은 답의 별칭과 출처가 맞아도 해당 문장이 질문의 답을 뒷받침하는지 놓칠 수 있다. `adjudicate.py`는 방식 이름과 자동 점수를 가리고, 같은 문항·조건에서 답과 근거가 같으면 한 번만 판정하게 한다. 각 카드에 질문에 대한 답, 인용 구절의 의미, 또는 재검토 조치의 적절성을 근거로 `correct`와 `basis`를 기입한다. 아래 마지막 명령은 모든 카드의 판정이 있어야 완료되며, 자동 점수와 문맥 검토 점수를 함께 보존한다.

```sh
python3 evaluation/team_pilot/adjudicate.py .cache/pilot-packets.json .cache/pilot-graded.json > .cache/review-cards.json
# 검토자는 review-cards.json의 correct, basis만 기입한다.
python3 evaluation/team_pilot/adjudicate.py .cache/pilot-packets.json .cache/pilot-graded.json --ratings .cache/review-cards.json > .cache/pilot-reviewed.json
```


## 공개된 최종 성적 재생

입력을 준비한 후, 아래 명령은 새 추론 없이 작업 119269의 원출력을 재채점한다.

```sh
PYTHONPATH=. python3 evaluation/team_pilot/pilot.py replay .cache/pilot-peps.git /path/to/topic-01/dialogue.json .cache/pilot-outcomes.json --recording results/team_pilot/outputs.json
python3 evaluation/team_pilot/score.py .cache/pilot-outcomes.json .cache/pilot-graded.json
python3 evaluation/team_pilot/adjudicate.py .cache/pilot-packets.json .cache/pilot-graded.json --ratings results/team_pilot/review-cards.json > .cache/pilot-reviewed.json
python3 -c 'import json; x=json.load(open(".cache/pilot-reviewed.json")); s=json.load(open("results/team_pilot/summary.json")); assert (x["automatic_summary"], x["reviewed_summary"]) == (s["automatic"], s["reviewed"]); print("Both summaries match")'
```
