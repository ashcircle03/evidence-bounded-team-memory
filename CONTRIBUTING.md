# 기여 안내

팀 기록을 병합하는 규칙, 근거를 읽는 QA, 평가 재현은 각각 따로 변경하고 검토할 수 있다. 실패하는 예를 보고하려면 질문 또는 새 기록, 당시 시스템에 보였던 원문, 기대 판단, 실제 판단을 적어 이슈를 열어 주세요. 공개 이슈에는 공유 가능한 자료나 가상 사례를 사용해 주세요.

## 로컬 검증

저장소 루트에서 Python 3.12와 Git으로 실행한다. 두 명령은 모델 가중치나 API 키를 요구하지 않는다.

```sh
python3 -m unittest discover -s tests -v
python3 -m team_memory demo
```

CUPMem 원형 직렬화·프롬프트 연결 검사까지 실행하려면 아래 고정 버전을 준비한다. CI도 같은 버전을 사용한다. 이 검사는 모델 추론이나 유료 API를 호출하지 않는다.

```sh
git clone https://github.com/icedreamc/STALE.git .cache/cupmem-upstream
git -C .cache/cupmem-upstream checkout --detach ea7d391103a151927cd29d2f01d87597a782bdcb
cp evaluation/cupmem/upstream-manifest.json .cache/cupmem-upstream/UPSTREAM_MANIFEST.json
CUPMEM_UPSTREAM_ROOT="$PWD/.cache/cupmem-upstream" python3 -m unittest discover -s tests -v
```

원본이 없으면 해당 연결 검사는 명시적으로 건너뛴다. 별도 보관한 과거 캠페인 파일·데이터 캐시·대용량 원시 호출 로그가 필요한 검사도 `skipped`로 표시된다. 공개된 입력·출력·코드의 해시와 근거 경계 검사는 계속 실행한다. `results/`에는 개발 당시의 보고서도 포함되므로, 현재 구현과 확인 범위는 README의 **현재 개발 경로**를 기준으로 읽는다.

## 실험을 바꾸는 PR

1. 바꾸려는 판단을 한 문장으로 적는다. 예를 들어 동일 조건의 상충 관측 두 개가 모두 답에 남아야 한다.
2. 그 판단이 달라지는 최소 사례와, 계속 맞혀야 하는 기존 사례를 함께 확인한다.
3. PR에 실행 명령과 관측값을 적는다. QA는 **답 내용**과 **인용의 출처·구절**을 따로 표시한다. 평가에 정답 위치를 제공했다면 그 조건도 밝힌다.

기존 실험을 비교할 때는 먼저 저장된 출력으로 이전 점수를 재현한다. 새로운 프롬프트나 채점 기준으로 얻은 결과는 별도 실험으로 기록한다. [CPython 평가 재현 안내](evaluation/cpython/README.md)
