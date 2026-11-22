# readers (답변·인용 리더)

retrieval 검색기(`team_memory/retrieval/search.py`)가 import해서 develop에 포함된 **answering 쪽 코드**다.
검색 자체는 `team_memory/retrieval/`에 있다.

| 파일 | 역할 |
|---|---|
| `attribution.py` | 답변 생성과 사후 인용 (`AttributedQA`, 상충 검사 `ConflictCheckedQA`) |
| `checking.py` | 근거 지지 검사 (ConflictScore 방식) |
| `citations.py`, `state_citations.py` | 원문 인용, 검토 상태 인용 |
| `scoped.py` | 조건 범위에 맞춘 답변 (`generate_scoped`, `public_answer`) |
| `context.py`, `prompts.py`, `fallback.py` | 문맥 구성, 프롬프트, 답변 보존·보류 |
