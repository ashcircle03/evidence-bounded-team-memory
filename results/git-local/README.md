# 두 독립 환경의 Git 교환과 실제 Qwen QA

**records 저장 → 각자 색인 준비 → Git 교환 → 실제 Qwen QA 경로의 회귀 검증을 통과했다.** 기존20문항을6단계에서 새로 답한120개 출력 모두 기존 답변 문장과 답·인용 객체가 정확히 같았다. 과거 답변 재생은 사용하지 않았다. 제품 모듈을 추가하거나 프롬프트를 바꾸지 않았다.

[상세 검증](v1c/verification.json) · [124개 질문·답·원문 근거](v1c/cases.md) · [판정](v1c/score.json) · [원출력/실제 호출](v1c/) · [실행 전 프로토콜](v1c/runtime/PROTOCOL.md)

## 실제 실행 결과

| 단계 | 기존20 답·근거 보존 | 문서 분할 | 임베딩한 청크 | 실제 Qwen 호출 |
|---|---:|---:|---:|---:|
| A 최초 준비·QA |20/20|1,276|1,414|130|
| B Git clone·독립 준비·QA |20/20|1,276|1,414|130|
| B에서 기록 추가 → A pull·준비·QA |20/20|7|7|138|
| A QA 프로세스 종료·새 실행 |20/20|0|0|138|
| A에서 수정 버전+신규 기록 → B pull·준비·QA |20/20|14|14|137|
| B QA 프로세스 종료·새 실행 |20/20|0|0|137|

7개 기존 기록 집합(합계1,276개 원문)을 유지한 실험이다. 첫 clone은 자기 색인을 처음 만들어야 한다. 이후 집합마다1건 추가, 수정 버전1건+별도 신규1건을 전달했다. 수신 측은 기대한 새 source ID만 분할·임베딩했고 원래1,276개 원문은 유지됐다. 송신 측도 각각7건/14건만 처리했다. 무변경 준비는 A/B 모두 분할·임베딩0건이었다. 질문124개 전부 문서 분할·임베딩0건이다.

새 기록 확인 질문4개는 별도 판정했다. A pull/재시작에서는2026-01-01 보고의 `violet`을 새 원문과 함께 답했다. B pull/재시작에서는2026-01-02 수정 보고의 `amber`를 답하고, 이전 `violet`도2026-01-01로 구분해 양쪽 원문을 인용했다.4개 모두 질문에 맞는 답과 필요한 원문 근거를 확인했다. 승인된 현재 상태를 묻거나 자동 승인한 실험은 아니다.

인용174개의 원문 source ID, 구절, offset, 작성자, 시각을 확인했다. A/B 최종 source 객체 집합이 같고, 양쪽 Git HEAD는 `a9dbdc47f44888e395cae56feef4c73076ba4679`로 일치했다. Git 추적 대상은 원문 JSON뿐이며 양쪽 working tree가 깨끗했다.

## 환경과 재현 범위

A/B는 한 Aurora 계산 노드의 독립 checkout이다. 각각 별도 GPU의 Qwen3-8B 서버, 별도 OS 프로세스, 별도 색인·캐시를 사용한다. 공유하는 것은 읽기 전용 체크포인트 파일뿐이다. Git remote는 같은 노드의 bare 저장소이며 Git clone/push/pull을 실제 실행했다. 두 물리 PC/서로 다른 OS/WAN 네트워크 성능을 측정한 것은 아니다.

production `SourceStore → prepare_index → TeamMemoryService.ask`를 사용했다. 분할·임베딩 계수용 래퍼는 원래 구현을 호출하며 decoder를 교체하지 않았다. 원래20문항과 모든 원문을 그대로 사용했고, 기존 정답/이전 답변은 runtime 패킷에 넣지 않았다. 과거 답과의 대조는 출력이 확정된 뒤 로컬에서 수행했다.

Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`, non-thinking, temperature0, context32768, 기본 생성 예산1024. 서로 다른6개 QA worker PID와2개 Qwen backend를 확인했다. 재시작은 QA 클라이언트 OS 프로세스의 종료·새 실행이며 Qwen backend는 유지된다. backend의 prompt-prefix KV cache는 답변 재생이 아니다.

실제810회 HTTP 호출 모두 서로 다른 생성 응답 ID, 양수 생성 토큰, 정상 `stop` 종료를 확인했다. 입력1,200,561/출력138,883토큰이며 외부 유료 API0회다. 입력·코드 패킷 해시와 체크포인트 해시를 검사했다. 원문 JSON과 벡터 저장소는 각 checkout에 존재하며 벡터·캐시는 Git으로 전달하지 않았다.

## 평가 해석과 남은 범위

- **120개 독립 문제를 맞힌 결과가 아니다.** 반복 사용한 기존20문항을6번 실행한 보존 검사다. 이 중 자연 EverMem3문항이 있지만 전체 벤치마크나 새 일반화 성능은 아니다.
- 기존20개는 답 문장과 답/근거 객체가 모두 이전과 같아 기존 원문 기반 판정을 승계했다. 새 확인 질문4개는 구현자가 원문과 직접 대조했다. 독립 평가자·블라인드 평가는 아니다.
- 기존과 동일하게 매 단계8개 응답에 추가 인용 검사 `partial` 경고가 남는다. 기존 답·필요 근거 보존이 모든 내부 검사의 완전한 성공을 의미하지 않는다.
- 변경분 처리 주장은 **문서 분할·임베딩**에 해당한다. source manifest 전체 조회와 vector 저장 파일/BM25 재구성 비용은 남아 있다. 전체 I/O가 변경분에만 비례한다고 주장하지 않는다.
- 수정은 기존 hash-addressed 원문을 덮어쓰는 방식이 아니라 새 버전 추가다. 과거 버전과 근거는 남는다.
- 관계 추론·승인·동시 divergent branch merge는 이 실험에 포함하지 않는다. `prepare_index`를 명시적으로 부르는 records/index 경로를 검증했다. 서비스 전체 `sync`의 최초 clone 시 과거 기록 bootstrap은 별도 통합 과제다.

## 실패·실제 비용

| 작업 | 종료 | 시간 | GPU | 실제 GPU분 |
|---|---|---:|---:|---:|
|122929|FAILED/1:0|1분43초|2|3.43|
|122930|FAILED/1:0|8분56초|2|17.87|
|122931|COMPLETED/0:0|44분43초|2|89.43|
|합계||| |110.73|

첫 시도는 서버 Git2.25가 `--initial-branch`를 지원하지 않아 종료했다. 두 번째는 빈 clone이`master`를 만들어 첫`push main`이 실패했다. 두 시도 모두 QA0회이며 [첫 실패](v1-failed/README.md), [두 번째 실패](v1b/README.md)에 원본을 남겼다.122931은 두 번째 시도에서 이미 커밋한 원문만 clone하고 모든 source 객체를 입력과 대조해 재사용했다. 색인·영수증·답은 재사용하지 않았다. 수정은 Git 호환 초기화에 한정했으며 모델·입력·프롬프트를 바꾸지 않았다.

모든 작업은 GPU2·CPU16·RAM96G·12시간 상한·`--no-requeue`·conda로 계산 노드에서 실행했다.122931의 batch MaxRSS는4,526,492K이며 GPU 메모리 피크 측정값은 아니다. 실패를 포함한 사용량을 dispatch에 남겼고 종료 후 사용자 queue가 비어 있는 것을 확인했다.

## 재검증

```sh
NLTK_DATA="$PWD/.cache/reference-nltk" TOKENIZERS_PARALLELISM=false \
  .venv/bin/python -m pytest tests/test_reference_index_lifecycle.py tests/test_service.py -q
.venv/bin/python -m evaluation.git_local.verify results/git-local/v1c
```

첫 명령은 로컬 계약 검사24개이며 실제 모델 성과에 포함하지 않는다. 두 번째는 보존된 실제 결과의 provenance/구조 검증이다. 새 Qwen 실행은 `runtime/`의 고정 config/sbatch/archive를 사용해야 하며 Slurm 없이 로그인 노드에서 실행하지 않는다. 현재 runner는 seed 없이 새 Git 저장소를 만드는 재현을 위해 `push -u`를 명시했고 로컬 양방향 Git 테스트로 확인했다. 실행된 정확한 버전은 `v1c/runtime/code.tar.gz`에 보존했다. 오프라인 verifier에 추가한 토큰·상태 집계는 모델 실행이나 정답 기준을 바꾸지 않는다.

**판단:** 각자 로컬 원문·파생 색인을 보유하고 Git으로 원문만 공유하는 구조를 유지한다. 이번 범위에서 제품 코드의 추가 수정이 필요한 보존 실패는 발견하지 못했다. 서비스 전체 bootstrap·동시 병합·남은 검사 경고까지 해결됐다는 뜻은 아니다.
