# readers (답변·인용 리더)

**answering 쪽 코드**다. 검색은 `team_memory/retrieval/`에 있고, retrieval은 이 폴더를 import하지 않는다.
여기 리더들은 `retrieval/search.py`의 `ReferenceQA`를 확장하고, 검토 상태 근거는 `retrieval/review_evidence.py`에서 가져온다.

| 파일 | 역할 |
|---|---|
| `attribution.py` | 답변 생성과 사후 인용 (`AttributedQA`, 상충 검사 `ConflictCheckedQA`) |
| `checking.py` | 근거 지지 검사 (ConflictScore 방식) |
| `citations.py` | 원문 인용 |
| `scoped.py` | 조건 범위에 맞춘 답변 (`generate_scoped`, `public_answer`) |
| `context.py` | 검토 상태를 답변 프롬프트에 반영 (근거 조립 함수는 retrieval/review_evidence.py로 이동) |
| `prompts.py`, `fallback.py` | 프롬프트, 답변 보존·보류 |
