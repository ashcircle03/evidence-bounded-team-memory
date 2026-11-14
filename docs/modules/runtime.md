# v2를 재사용하는 실제 다섯 모듈 연결

현재 진입점은 [`connect_v2`](../../team_memory/adapters/runtime.py)다. 기존 JSONL `service.py`를 교체하지 않는 명시적 opt-in 경로다. 모델·임베딩·인증된 호출 주체를 주입하면 원문 저장 → 비교 → 제안 → 작성자 검토 → QA를 연결한다. UI나 MCP 서버는 추가하지 않았다.

## 무엇을 재사용했는가

| 경계 | 재사용한 구현 | 추가한 연결 코드 |
|---|---|---|
| records | `Store.put`의 content-addressed 원자적 객체 쓰기, SourceStore 입력 검증, `review.state`의 원문 구절·투표 축약 | 명령 하나를 단일 immutable commit으로 저장, revision·idempotency·workspace/owner 확인 |
| relations | `compare_sources`의 원문 문장 ID 선택, `prepare_relation` 구절 검증 | snapshot 확인, 공개 ID 변환, 후보별 실패·기존 검토 상태 전달 |
| retrieval | 기존 dense/BM25 RRF·상태 연결 확장·CitationQueryEngine 구절 구성 | 생성 직전에서 멈춰 JSON evidence bundle 반환 |
| answering | 기존 synthesize → ConflictScore → 필요시 수정/AQA → 인용 보완 | 고정 bundle만 사용, 문장별 명시 인용 연결, 무인용 구절도 원문 그대로 보존 |
| gateway | v2의 명시적 ingest/review/ask 흐름 | ask에서 sync 제거, 명령 전송 전 intent 저장, ingest 부분 실패·재시도 연결 |

새 분류 모델·판단 프롬프트·추가 검사 모델은 없다. 상태 근거는 새 계약의 canonical rendering을 사용하므로 기존 v2의 상태 문맥과 바이트가 같다고 주장하지 않는다. source-only QA는 고정 근거에서 실제 모델 요청130개가 기존 기록과 정확히 일치했다.

## 연결 방법

```sh
python -m pip install -e '.[reference,contracts,dev]'
```

기존 v2에서 쓰던 `local_components`와 reader를 그대로 주입한다. 모델 실행은 Aurora에서는 Slurm 계산 노드에서 수행한다.

```python
from llama_index.core.llms import ChatMessage
from team_memory.readers.retrieval import local_components
from team_memory.readers.attribution import AttributedQA
from team_memory.adapters.runtime import connect_v2
from team_memory.adapters.base import request
from team_memory.adapters.legacy import public_source

parts = local_components(model_path, embedding_path, loopback_api_base)
def generate(system, content):
    return parts['llm'].chat([
        ChatMessage(role='system', content=system),
        ChatMessage(role='user', content=content),
    ]).message.content

gateway = connect_v2(
    'team-records', workspace_id='my-team',
    reader_factory=lambda store: AttributedQA(store, **parts),
    generate=generate,
    cache_root='private-module-cache',
)
# context는 MCP/API 인증 계층이 만든 CallContext다. 요청 본문의 actor를 쓰지 않는다.
snapshot = gateway.records.handle(request('snapshot.get', {'snapshot_id': None},
    workspace_id='my-team', request_id='read-1'), context=context)['data']
source = public_source({
    'owner': context.principal_id, 'observed_at': '2026-11-14T12:00:00Z',
    'source': {'speaker': 'Jaewon', 'location': 'notes/report.md',
               'text': 'Version 5 permits four writers.'},
})
ingest = gateway.handle(request('gateway.ingest', {
    'source': source, 'expected_revision': snapshot['revision'],
    'idempotency_key': 'report-v5',
}, workspace_id='my-team', request_id='ingest-1'), context=context)
answer = gateway.handle(request('gateway.ask', {
    'snapshot_id': None,
    'query': {'text': 'What changed?', 'time_scope': 'current',
              'as_of': None, 'conditions': []},
}, workspace_id='my-team', request_id='ask-1'), context=context)
```

기존 기록을 가져오는 초기 쓰기는 `record.append`, 새로운 보고를 비교까지 하는 쓰기는 `gateway.ingest`다. 타인 원문을 import할 권한은 `records:write`와 별도 `records:import`를 함께 갖춰야 한다. 승인 요청은 `gateway.review`에 proposal_id·choice·expected_revision·idempotency_key를 전달한다. 실제 principal은 이전 원문 owner와 일치해야 한다. endpoint 인증 자체는 팀원의 MCP/API 계층 책임이다.

`source.id`는 기존 native source hash를 그대로 사용할 수 있다. `public_source`가 이를 계산한다. 이미 외부에서 부여한 opaque source ID도 충돌 없이 보존한다. 검토 관계의 이전 history IDs도 DTO에 보존해 이후 기록을 과거 비교 문맥에 끼워 넣지 않는다.

## 저장과 전환 범위

- 기존 v2 sources/proposals/votes는 최초 연결에서 **한 번** 검증·가져온다. 원본 파일·ID·텍스트는 변경하지 않는다.
- 새 변경은 `module_commits/<hash>.json`에 기록한다. 명령의 native object delta와 idempotency 정보가 하나의 원자적 파일에 들어간다. 기존 reducer가 그 delta의 투표 상태를 계산한다.
- writer lock과 expected_revision으로 같은 checkout의 동시 쓰기를 직렬화한다. commit 이후 오류가 나면 실제 파일 존재를 대조해 성공 여부를 조정한다.
- 시작 시점 이후 기존 v2 파일을 별도 writer가 변경하면 STALE_SNAPSHOT으로 중단한다. 두 writer를 같은 저장소에서 혼용하지 않는다. 외부 v2 변경을 자동으로 무시하거나 덮어쓰지 않는다.
- Git으로 두 checkout에서 **서로 갈라진 module commit branch를 동시에 쓴 경우 자동 병합은 아직 제공하지 않는다.** 현재 조회는 STALE_SNAPSHOT으로 실패한다. 명시적인 병합 계약 없이 어느 branch를 승자로 선택하지 않는다. 기존 v2 Git 경로는 그대로 유지하며, 새 경로는 단일 writer 이력 또는 충돌 없는 fast-forward 공유 범위에서 사용한다.
- 캐시·모델 출력·gateway 재개 장부는 cache_root에 둔다. authoritative snapshot과 구분한다. 서로 다른 클라이언트가 같은 private cache를 공유하지 않는다.

따라서 이번 완료 범위는 **실제 다섯 포트의 단일 이력 연결과 기존 QA 보존**이다. 다중 branch 운영 전환이나 인증 서비스 완성까지 의미하지 않는다.

## v1.1: 답을 버리지 않는 주장별 변환

기존 답에는 인용이 없는 문장도 섞여 있었다. 그 문장을 삭제하거나 다른 문장의 인용을 복사하면 기존 답을 훼손한다. v1.1에서는 다음을 함께 반환한다.

- `original_text`: 기존 reader가 만든 최종 답의 정확한 바이트 표현(문자열).
- `claims[*].answer_span`: 그 답 안에서 해당 claim이 차지하는 `[start,end)` 범위.
- `unattributed`: 명시적 인용이 연결되지 않은 구절과 원래 범위. 확정된 claim으로 바꾸지 않는다.
- `partial` + `UNSUPPORTED_CLAIM`: 미연결 구절 또는 기존 단계의 미검증 상태가 있음을 알린다.
- `unverified_revision`: 기존 AQA가 source coverage만으로 교체 후보를 받아들였으면 이전 답·이전 근거 IDs와 후보를 함께 보존한다. 의미 보존을 검증했다고 표시하지 않는다.

검증기는 모든 claim·미연결 구절을 합쳤을 때 원문 답 전체를 빠짐없이 덮는지 검사한다. `claims`를 묶어 원래 답이라고 표시하면 미연결 부분을 잃을 수 있다. UI/API 소비자는 `original_text`와 미연결 경고를 함께 표시한다. 명시적 문장별 인용은 provenance 연결이며 의미 entailment 인증은 아니다. 복합문을 자동으로 원자적 주장들로 재작성하지 않는다.

요청 버전은 `team-memory.modules/v1.1`이다. 기존 v1 JSON 클라이언트는 명시적으로 버전을 갱신해야 하며, 기존 `team-memory/v2` API에는 변화가 없다.

## 확인된 결과와 한계

[실행 결과](../../results/module-adapters/README.md).

- 실제 파일 저장·비교 어댑터·재검토/정정·승인·재시작·retrieval·answering 연결을 검사했다. 이 연결 검사의 decoder는 stub이다.
- source-only 기존20문항은 정확히 같은 모델 요청에서만 기록된 Qwen 응답을 재생했다. 최종 답·기존 근거·공개 원문 답 모두20/20 보존됐다. 생성130요청이 정확히 일치했다.
- 8문항의11개 무인용 구절은 숨기지 않고 반환한다. 20/20 보존을 모든 문장의 인용이 완전하다는 뜻으로 해석하지 않는다.
- 검색은 실제 LlamaIndex/BM25를 쓰는 연결 검사에서 확인했고,20문항 대조는 **과거 검색 결과를 고정**했다. 재검색 정확도를 새로 측정하지 않았다.
- 새 canonical 상태 문맥의 실제 Qwen 의미 성능과 상태8 재추론은 아직 측정하지 않았다. 당시 Aurora는 기존 사용자 작업의 GPU 할당 때문에 QOSMaxGRESPerUser 상태였다. 기존 작업을 취소하거나 다른 작업으로 바꾸지 않았다.
- historical 조회, 분기 Git 자동 병합, 실제 인증 transport, 학습/모델 교체는 이번 연결 범위 밖이다. 지원하지 않는 과거 시점을 현재 상태로 대신하지 않는다.

```sh
python -m pytest -q tests/test_module_records.py tests/test_reference_module_adapters.py
TOKENIZERS_PARALLELISM=false python -m evaluation.module_adapters.replay
python scripts/check.py all --fail-on-skip
```
