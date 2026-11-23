# retrieval 모듈

records가 발행한 snapshot을 색인하고, 질문에 맞는 **근거 묶음**을 만들고, 새 기록을 등록할 때 비교할
**과거 기록 후보**를 찾는다. 팀 지식(records)은 바꾸지 않고, 검색 색인·캐시만 쓴다.

## 입구 (포트)
`team_memory/adapters/retrieval.py` — records 포트(`adapters/records.py`)처럼 포트는 `adapters/`에 둔다.

| 연산 | 입력 → 출력 |
|---|---|
| `evidence.prepare` | snapshot → 색인 준비 (질문 경로 밖에서 미리) |
| `evidence.retrieve` | 질문 + snapshot + 예산 → 근거 묶음 (원문 구절·출처·조건·검토 상태) |
| `history.search` | 새 기록 + snapshot → 비교할 과거 기록 후보 (등록 시, 기능명세서 F02) |

## 이 폴더
**이 폴더(검색 쪽)는 답변 모델이나 `team_memory/readers`(answering)를 import하지 않는다.**

| 파일 | 원래 위치 (main) | 역할 |
|---|---|---|
| `retriever.py` | `readers/retrieval.py`의 `ReferenceQA` 일부 | **`Retriever`**: 색인(`import_history`, `prepare_index`)과 검색(`retrieve()` → 원문 구절 witness 목록). LLM 없이 만들 수 있다 |
| `stages.py` | `readers/retrieval_stages.py` | 검색 단계: 후보(LlamaIndex·BM25), 조건 필터, 점수 임계값, RRF 융합, 단계 조합 `StagedRetriever` |
| `reranking.py` | `readers/turn_reranking.py` | 회의록 후보를 바로 앞 발화와 함께 재순위 (F05) |
| `review_evidence.py` | `readers/context.py` 일부 + `readers/state_citations.py` | 정정·상충에 걸린 기록이면 **상대편 기록과 검토 상태를 근거로 추가** (F05) |
| `indexing.py` | `readers/indexing.py` | 색인 준비·캐시·잠금, records 주장 범위 단위 색인 |
| `feedback.py` | `experiments/readers/retrieval.py` | 실험용 피드백 검색 (`FeedbackRetriever`) |
| `search.py` | `readers/retrieval.py` | **호환용 `ReferenceQA(Retriever)`**: 검색은 `Retriever`에서 물려받고 답변 생성만 한다. answering 리더들이 이 클래스를 상속한다. 생성자와 `ask()` 동작은 main과 같다 |

## 함께 쓰는 곳
- `adapters/reader_bridge.py`: records 그래프 → 근거 묶음(조건·역할 포함) 변환. records와 retrieval이 공유한다.
- `readers/`: 답변·인용 리더(answering 쪽 코드). `search.ReferenceQA`를 확장하고, 검색기가 답변 형식에 이 리더들을 쓴다.

`main`과 경로가 다르다 (develop에서 정리). main에 합칠 때는 위 "원래 위치"로 되돌리거나 main 쪽을 함께 옮긴다.
