# answering 모듈

retrieval이 만든 **근거 묶음만으로** 답변을 만든다. 근거를 새로 찾거나, 승인하거나, 숨은 원문을 추가하지 않는다.
근거가 없거나 불완전하면 답변하지 않고(abstain) 이유를 남긴다.

## 입구 (포트)
`team_memory/adapters/answering.py` — `answer.generate`: 근거 묶음 → 답변(주장별 인용·조건·상충 표시). records·retrieval 포트처럼 `adapters/`에 둔다.
포트는 snapshot 확인, 리더 생성, 실패 → 계약 오류 변환, 진단 저장만 하고 단계는 `pipeline.py`를 부른다.

## 구성
| | 파일 | 원래 위치 (main) | 역할 |
|---|---|---|---|
| ① | `scoped.py` | `readers/scoped.py` | 조건이 여러 개면 조건별 구조화 답변 (한 번의 모델 호출, 원문 증인과 함께) |
| ② | `pipeline.py` | `adapters/answering.py` 본문 | 기계적 검증: 근거 완전성(`evidence_problem`), 경로 선택(`use_scoped`), 문장별 인용 소유권·미인용 문장 분리·상충 표시(`claims_from_result`) |
| ③ | `context.py` | `readers/context.py` | 검토 상태(정정·재검토)를 답변 프롬프트 문맥으로 연결 |
| ④ | `fallback.py` | `readers/fallback.py` | 단계 실패 시 직전 답변 유지 / 근거 없으면 보류 |
| | `generation.py` | `readers/retrieval.py` | `ReferenceQA(Retriever)`: 검색은 retrieval에서 물려받고 답변 생성만 한다. 생성자·`ask()`는 main과 같다 |
| | `prompts.py` | `readers/prompts.py` | ConflictScore·LlamaIndex 인용 프롬프트 |
| ⑤ | `strategies/checking.py` | `readers/checking.py` | `ConflictCheckedQA`: ConflictScore 방식 상충 검토 |
| ⑤ | `strategies/attribution.py` | `readers/attribution.py` | `AttributedQA`: AQA 누락 보정, `attach_citations` 인용 보정 |
| ⑤ | `strategies/citations.py` | `readers/citations.py` | ALCE식 인용 문구 붙이기 |
| ⑥ | `team_memory/experiments/readers/` | 같음 | 실험 리더 (기본 경로 밖) |

`run_strategies`는 리더 클래스가 켠 전략(⑤)만 main과 같은 순서로 실행한다: 생성 → ConflictScore 검토 → AQA 보정 → 인용 보정.
지금은 **동작을 바꾸지 않은 구조 정리**다. ⑤를 기본으로 끄는 것은 QA 20문항 정확 재생이 깨지므로 GPU 평가와 함께 따로 한다.

## 의존 방향
answering → retrieval(`Retriever`, `review_evidence`) 한쪽뿐이다. retrieval은 answering을 import하지 않는다.

## main과 다른 점
main의 `team_memory.readers.*`와 `team_memory.retrieval.search`(develop 이전 경로)는 위 표의 경로로 옮겼다.
main의 `evaluation/answering_port/state_guard.py`가 패치하는 `team_memory.adapters.answering.attach_citations`는 이제 `team_memory.answering.pipeline.attach_citations`다.
