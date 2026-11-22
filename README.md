# records 모듈 (Evidence-Bounded Team Memory)

이 브랜치에는 **records 모듈과 실행에 필요한 의존 파일만** 있다. 팀원 모듈(retrieval, answering, relations,
gateway, readers), 평가·테스트·문서·결과는 `main`에 있다. 이 브랜치는 main으로 그대로 합치는 용도가 아니다.

records는 팀 기록의 **원문·출처·위치를 그대로 보존**하고, 원문 구절 위치로 **주장·조건·이유·시간·대상**을
연결해 저장한다. 모델이 뽑은 연결은 모두 `model_extracted_unverified`이며 승인으로 취급하지 않는다.

## 구성 (38개 파일)
```text
team_memory/
├── records/        추출·정렬·검증·보정
│   ├── preserving.py   construct() 진입점, build_blocks() 블록 처리
│   ├── grouped.py      LangExtract 프롬프트·예시 (한글 원문엔 한국어 예시)
│   ├── graph.py        record_graph 형식·검증(validate_graph)·출력(describe, linked_span)
│   ├── repair.py       조건 보정 (기본값)
│   ├── alignment.py    선택 정렬 alignment='source'
│   ├── segments.py, layout.py   블록 분할, 표·목록 좌표
│   ├── staged.py       선택 2단계 추출 builder
│   ├── compact.py      선택 압축 저장
│   ├── view.py         공통 주장 표현 claims_view()
│   ├── arguments.py    선택 QA-SRL 역할 레이어
│   └── discourse_roles.py, discourse_scope.py, policy_scope.py, pair_binding.py   선택 역할 보정·v4 호환
├── storage/, store.py  불변 객체 저장 (store.py는 과거 해시에 묶인 고정 파일)
├── review/state.py     제안·승인·거절 상태
├── adapters/           records 포트 (records.py), 저장↔공개 변환 (legacy.py), 공통 요청 처리 (base.py)
└── contracts/          팀 공통 스키마·검증·포트
```

## 설치
Python 3.11 이상. records에 필요한 외부 패키지는 jsonschema, pydantic, langextract, llama-index-core, nltk이다.
```sh
pip install -e '.[reference,dev]'
python -m nltk.downloader punkt_tab
```
NLTK 3.10 이상은 다른 계정이 소유한 데이터 폴더를 읽지 않는다. 본인 소유 폴더(예: `~/nltk_data`)를 쓴다.
`adapters/records.py`는 `fcntl`을 쓰므로 Linux에서 실행한다.

## 사용
```python
from functools import partial
from team_memory.records import preserving
from team_memory.adapters.records import RecordsAdapter

source = dict(id='src-A', owner='petr', speaker='secretary', observed_at='2026-11-20T09:00:00Z',
              location='minutes.md#L3', text='In dataset v1, Petr approved the draft.')
record = preserving.construct(source, generate, model='Qwen3-8B')   # generate(system, prompt) -> str
# 또는 RecordsAdapter(root, workspace_id, record_builder=partial(preserving.construct, generate=generate, model=...))
```
| 옵션 | 기본값 | 의미 |
|---|---|---|
| `repair_conditions` | **True** | 조건절을 claim으로 저장한 경우·`then`·문헌 번호·한 결과절의 조각 중복을 원문 규칙으로 보정 |
| `isolate_invalid` | **True** | 잘못된 행만 빼고 사유를 diagnostics에 남김 |
| `alignment` | `'token'` | `'source'`: 글자 단위 고유 위치 정렬 (한국어 조사, 문장부호 공백) |
| `segmentation` | `'legacy'` | `'compact'`: 제목·표 행은 호출 생략, 불릿 묶기, 긴 문단 분할 |
| `RecordsAdapter(storage=)` | `'full'` | `'compact'`: quote·edges를 저장하지 않고 읽을 때 복원 |

## 검증 (공개 개발셋, 팀원 Slurm 124911과 같은 입력·모델·채점, 2026-11-22)
| 지표 | 팀원 기준선 | 이 코드 |
|---|---|---|
| 원문·출처·위치 보존 (1,049건 저장→재시작) | — | 1,049 / 1,049 (전체·압축 저장) |
| 조건 정밀도 | 67.4% | 88.0% |
| 조건 복구 | 29 / 49 | 44 / 49 |
| QA 20문항 답·근거 유지 | 20 / 20 | 20 / 20 |
| 저장 후 역할 정밀도 | 16.2% | 15.8% |

평가 도구와 상세 결과는 이 브랜치에서 제외했다. 68문서 회귀(팀원 정답 51개 유지)는 아직 확인하지 않았다.
