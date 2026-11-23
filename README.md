# records + retrieval (Evidence-Bounded Team Memory)

이 브랜치에는 **records 모듈과 retrieval 모듈, 그리고 두 모듈이 실행에 필요한 의존 파일만** 있다.
records는 `records` 브랜치의 최신본, retrieval은 `main`의 최신본(PR #4, 2026-11-22)이다.
answering·relations·gateway 포트, 평가·테스트·문서·결과는 `main`에 있다. 이 브랜치는 main으로 그대로 합치는 용도가 아니다.

- **records**: 팀 기록의 원문·출처·위치를 보존하고, 원문 구절 위치로 주장·조건·이유·시간·대상을 연결해 저장한다.
- **retrieval**: records snapshot을 색인하고, 질문에 맞는 근거 묶음을 만들고(`evidence.retrieve`), 등록 시 비교할 과거 기록 후보를 찾는다(`history.search`). 회의록 후보는 앞 발화로 재순위한다.

## 구성
```text
team_memory/
├── records/                 records 모듈 (추출·정렬·검증·조건 보정, 2단계·압축·공통 표현은 선택)
├── retrieval/               retrieval 모듈: retriever.py(Retriever 색인·검색), stages.py, reranking.py,
│                            review_evidence.py, indexing.py, feedback.py — answering을 import하지 않음
│                            search.py는 호환용 ReferenceQA(검색 + 답변 생성) — 지도: team_memory/retrieval/README.md
├── adapters/                포트: records.py, retrieval.py / 공용: legacy.py, reader_bridge.py, base.py
├── storage/, store.py       불변 저장 (store.py는 과거 해시에 묶인 고정 파일)
├── review/                  state.py 제안·승인 상태, policy.py 검토 정책
├── readers/                 답변·인용 리더 (answering 쪽 코드, ReferenceQA를 확장)
├── experiments/readers/     검색기·리더가 import하는 실험 리더
├── _vendor/                 외부 구현 (alce, attribute_first, conflictscore, langchain_citation) + LICENSE·NOTICE
└── contracts/               팀 공통 스키마·검증·포트 (main 최신본 + records 영수증 검사 수정)
```
retrieval 파일은 main의 `readers/`에서 `retrieval/`로 옮기고, 검색(`Retriever`)과 답변 생성(`ReferenceQA`)을 나눴다.
main과 경로가 다르다 (원래 위치는 retrieval/README.md).

## 설치
Python 3.11 이상, Linux (`adapters/records.py`가 `fcntl`을 쓴다).
```sh
pip install -e '.[reference,dev]'
python -m nltk.downloader -d ~/nltk_data punkt_tab stopwords
```
NLTK 3.10 이상은 다른 계정 소유의 데이터 폴더를 읽지 않는다. 본인 소유 폴더를 쓴다.

## records 기본값
| 옵션 | 기본값 | 의미 |
|---|---|---|
| `repair_conditions` | True | 조건절·then·문헌 번호·결과절 조각 중복을 원문 규칙으로 보정 |
| `isolate_invalid` | True | 잘못된 행만 빼고 사유를 diagnostics에 남김 |
| `alignment` | `'token'` | `'source'`: 글자 단위 고유 위치 정렬 |
| `RecordsAdapter(storage=)` | `'full'` | `'compact'`: quote·edges를 읽을 때 복원 |

records 검증(공개 개발셋, 팀원 Slurm 124911과 같은 조건): 원문·출처·위치 보존 1,049/1,049, 조건 정밀도 67.4% → 88.0%,
조건 복구 29/49 → 44/49, QA 20문항 답·근거 20/20 유지. retrieval 평가는 main의 `evaluation/retrieval_dataset/`를 본다.
