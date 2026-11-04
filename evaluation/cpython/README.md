# CPython 파일럿 재현

CPython PEP의 고정된 Git 객체에서 당시 문서와 질문을 복원하고, 저장된 Qwen 응답을 원래 코드로 재채점한다. CPU, Git, Python 3.12 표준 라이브러리로 실행할 수 있다. 아래 명령은 모두 **프로젝트 루트**에서 실행한다.

## 1. 당시의 입력 복원

세 사건과 그 첫 부모를 포함하는 PEP 저장소가 필요하다. 기존 bare clone이 있으면 첫 두 줄을 건너뛰고 마지막 인수로 그 경로를 전달한다.

```sh
mkdir -p .cache
git clone --bare --single-branch --branch main --no-tags https://github.com/python/peps.git .cache/peps.git
PYTHONPATH=. python3 evaluation/cpython/replay.py .cache/peps.git
```

스크립트는 스냅샷과 모델 입력 패킷을 만들고 원래 압축 파일의 SHA-256을 확인한다. 이어서 모델 호출 29개의 입력 해시와 최종 출력 24개를 대조한다. 정상 실행 시 대상·조치 결합 정답은 direct 2, checked 2, module 1이며 QA는 0/9다. CPU 재생은 새 모델 응답을 생성하지 않는다. [사전 계획과 실험 범위](PLAN.md) · [원래 채점 결과](../../results/cpython/score.json)

## 2. QA의 실제 입력과 원출력 대조

```sh
PYTHONPATH=. python3 evaluation/cpython/audit_qa.py --dump-inputs .cache/qa-prompts.jsonl > .cache/qa-audit.json
diff -u results/cpython/qa-audit.json .cache/qa-audit.json
PYTHONPATH=. python3 evaluation/cpython/qa_controls.py score results/cpython/qa-control-outputs.json > .cache/qa-control-score.json
```

- `.cache/qa-prompts.jsonl`에는 검증한 9회 각각의 시스템 지시문과 사용자 입력 전체가 있다. 사용자 입력의 `messages[n].sentences`에 문서별 구간이 들어 있다. 문서 번호는 각 메시지 객체의 `n` 필드로 확인한다.
- `qa-audit.json`은 정답 구절의 문서·구간 번호, 모델 원출력, 인용 검사 결과를 담는다. 정답 인용을 실제 코드에 넣는 양성 대조도 포함한다.
- `qa-control-score.json`은 대조 실험의 36개 응답을 재채점한다. `answer_key_match`는 인용을 요청하지 않은 답 내용, `grounded_correct`는 원래 기준의 답과 인용, `whitespace_only_repair_correct`는 유일하게 대응하는 원문 구절로 공백만 복원한 진단값이다. [9회 각각의 해석](../../results/cpython/qa-diagnosis.ko.md)

## 3. 같은 모델로 대조 실험 다시 실행하기 (GPU)

CUDA 환경과 로컬 Qwen2.5-3B-Instruct 체크포인트가 필요하다. 원래 가중치 리비전은 `aa8e72537993ba99e69dfaafa59ed015b17504d1`이다. 진단용 입력을 만드는 단계에서만 정답 위치를 사용한다. 모델에 전송하는 패킷에는 질문, 선택된 구간과 출력 지시만 들어간다.

```sh
PYTHONPATH=. python3 evaluation/cpython/qa_controls.py prepare .cache/qa-controls.json.gz
PYTHONPATH=. python3 evaluation/cpython/qa_controls.py infer .cache/qa-controls.json.gz /path/to/local/qwen .cache/new-outputs.json local-run
PYTHONPATH=. python3 evaluation/cpython/qa_controls.py score .cache/new-outputs.json
```

## 자료와 검토 순서

- [python/peps](https://github.com/python/peps) — 원문과 각 문서의 저작권 표기. 이 실험은 사건이 일어났을 때의 Git 객체를 사용한다.
- [events.json](events.json) · [build.py](build.py) · [retrieve.py](retrieve.py) — 사건의 커밋, 질문, 당시 입력을 복원하는 방법.
- [review.md](review.md) — 독립 검토를 맡은 팀원은 입력을 복원한 뒤 이 양식부터 작성한다. 사전 정답과 모델 출력은 제출 후 열람한다.
- [freeze.json](freeze.json) · [assess.py](assess.py) — 동결 시점의 해시와 채점 구현. 공개된 상세 채점 파일에는 당시 원문 행까지 대조한 정보가 추가돼 있다.
