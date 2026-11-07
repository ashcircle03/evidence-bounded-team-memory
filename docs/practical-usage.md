# 이전 practical 경로 재현

새 팀 연결에는 [service-v2](service-v2.md)를 사용한다. 아래는 이전 고정 실험의 경로다.

이 경로는 UI나 MCP 서버를 만들지 않는다. 호출자는 원문을 보내고 `answers`,
`proposals`, `status`를 받는다. 고정 평가 후 원문 검색·독해 경로를 개발 기반으로
유지하고 CUPMem native 작성과 자동 재검토 판단은 실험 기능으로 보류했다.
두 경로 모두 긴 문서와 의미적 인용에 한계가 있다.
[최종 평가](../results/cupmem/practical/README.md)와 [고정 명세](cupmem-practical-v2.md)를 함께 확인한다.

## Python 호출

실제 모델을 연결한 전체 예제는
[evaluation/cupmem/practical/run.py](../evaluation/cupmem/practical/run.py)에 있다.
입력 형식과 반환 형식을 확인하려면
[개발 입력](../evaluation/cupmem/practical/development.json)과
[개발 판정](../results/cupmem/practical/dev-v2/ratings.json)을 읽는다.
개발 판정은 새로운 사례에서의 성능을 의미하지 않는다.

```python
from team_memory.cupmem_candidates import SourceOnlyMemory
from team_memory.cupmem_practical import PracticalCUPMemService

# engine: 고정한 공식 CupMemEngine
# generate(system, content): 같은 로컬 모델의 JSON 생성 함수
memory = SourceOnlyMemory(engine)
service = PracticalCUPMemService(memory, generate, "team-records", strategy="simple")
result = service.handle({"operation": "ingest", "source": original_report})
answer = service.handle({"operation": "ask", "question": question,
                         "temporal_scope": "historical"})
```

`original_report`의 필드는 `owner`, 시간대가 있는 `observed_at`, 그리고
`source: {speaker, location, text}`다. 사람이 미리 정리한 주장·정답·관계 라벨을
요구하지 않는다. 기존 자료 묶음의 최초 입력에는 `import_history`와 `records`를
사용한다. 새 기록의 `ingest`와 달리 최초 묶음 입력 자체에서는 검토 제안을
만들지 않는다.

## JSONL 호출

[practical_service.py](../examples/practical_service.py)는 한 줄에 요청 JSON 하나를
받고 응답 JSON 하나를 출력하는 얇은 연결 예제다. Aurora 작업 `119837`에서
실험 후보 `--strategy cupmem`으로 실제 Qwen3-8B 원문 두 개와 질문 하나를 처리했고 `COMPLETED/0:0` 및 프로그램
완료를 확인했다. 대기 상태 재검토 제안, 두 조건의 측정값과 원문 인용을
반환했다. GPU 사용 시간은 1분 48초다.
[실제 응답](../results/cupmem/practical/cli-smoke-v1/responses.json) ·
[검증 결과](../results/cupmem/practical/cli-smoke-v1/verification.json)
아래 호출은 **이미 확보한 Slurm GPU 계산 노드, 활성화한 conda, 같은 할당의
로컬 Qwen3-8B 서버** 안에서 수행한다. 새 작업을 자동으로 제출하지 않는다.

```sh
python examples/practical_service.py \
  --upstream /path/to/STALE-at-ea7d391103a1 \
  --embedding /path/to/pinned-embedding-model \
  --store /path/to/team-records \
  --base-url http://127.0.0.1:PORT/v1 \
  --strategy simple \
  < examples/practical_requests.jsonl > responses.jsonl
```

예제 입력은 이미 평가한 Cedar 개발 흐름의 원문 두 개와 질문 하나다.
위 명령은 채택한 개발 기반을 선택한다. 보존된 CLI 결과를 같은 방식으로
재현하려면 `--strategy cupmem`을 사용한다. simple의 실모델 검증은 고정된
쌍별 평가에 포함되어 있으며 별도 CLI 성능 측정으로 주장하지 않는다.
`--strategy simple`은 원문 검색·독해와 단순 비교만 사용하며 CUPMem 기억을
작성하지 않는다. 두 경로의 저장소를 분리한다. 원형 모델·임베딩·환경은
[제출 설정 생성 코드](../evaluation/cupmem/practical/prepare.py)와 각 실행의
동결 manifest에 기록되어 있다. 이 CLI는 외부 유료 API로 우회하지 않는다.
실험 고정 이후 constructor 기본값은 바꾸지 않았다. Python 호출도 위처럼
`strategy="simple"`을 명시한다. 자동 제안의 의미적 정확성은 채택 기준에
미달했으므로, 반환된 제안을 확정 지식으로 사용하지 않는다.

## 응답과 검토 처리

`ok`는 처리 성공 표시이며 답의 의미가 맞다는 자동 판정이 아니다. `partial`은
`warnings`와 반환된 각 근거를 함께 확인해야 한다. `error`, `invalid`,
`needs_rebuild`, 실행되지 않은 요청을 올바른 기권으로 취급하지 않는다.

제안은 `pending`으로 저장된다. 원작성자의 실제 의사를 받은 호출자만 다음
형식으로 검토를 전달한다. 신원 인증과 Git 전송은 호출자의 책임이다.

```json
{"operation":"review","proposal_id":"RETURNED_ID","actor":"ORIGINAL_OWNER","choice":"approve"}
```

재검토 승인은 과거 관측의 삭제나 새로운 최종 결정의 승인과 같지 않다.
조건이 다른 관측은 원문과 함께 보존한다. 질문과 겹치는 관계와 실제 검토
상태만 답에 연결한다.

## 현재 알려진 제한

- 원문은 디스크에 남지만 파생 CUPMem 엔진은 재시작 후 명시적인 `rebuild`가
  필요하다. 이 작업은 모델 호출을 발생시킨다.
- 긴 자료 묶음의 native 적재는 작고 짧은 개발 흐름보다 훨씬 비싸다. 적재
  실패 시 현재 후보는 이후 QA도 `needs_rebuild`로 막는다.
- 검색한 구절에서 전체 문서로 확장하는 현재 독해 입력은 긴 문서에서 모델
  문맥 한도를 초과할 수 있다. 현재 PEP 회귀에서 실제 발생한 실패이며, 이를
  일반 문서 처리 지원으로 표현하지 않는다.
- 정확한 출처 ID와 문자 위치가 있어도 선택 구절이 답을 뒷받침하지 않을 수
  있다. 최종 평가에서는 위치 일치와 의미적 지지를 따로 채점한다.
- 단일 프로세스가 한 서비스 디렉터리를 소유한다. 이 예제는 분산 잠금이나
  Git 원격 병합을 구현하지 않는다.
