# experiments — 후보와 과거 비교

기본 서비스가 자동으로 실행하는 모듈이 아니다. 기존 모델 후보를 역할별로 옮겼으며, 이름에 reference가 있었다는 이유로 검증된 운영 모듈로 해석하지 않는다.

| 경로 | 후보 | 기록 |
|---|---|---|
| `readers/joint.py` | 답과 근거를 함께 생성 | `docs/reference-joint.md` |
| `readers/claims.py` | 주장·근거 선택 | `docs/reference-claims.md` |
| `readers/contextual.py`, `connected.py` | 문맥/검색 피드백·근거 계획 | `docs/reference-contextual.md`, `reference-connected.md` |
| `readers/demonstrated.py`, `documents.py` | 공개 예시·문서 단위 후보 | `docs/reference-demonstrated.md`, `reference-documents.md` |
| `readers/nli.py` | 과거 NLI 인용 후보 | `docs/reference-attribution.md` |
| `readers/format.py`, `retrieval.py` | 후보용 형식·검색 보조 | 위 후보의 비교 기록 |
| `review/source_patch.py`, `decision_patch.py` | 원문/결정 patch 후보 | `results/source-patch/README.md` |

새 후보는 레퍼런스의 입력·출력·작동 조건을 적고, 현재 reader와 같은 입력으로 비교한다. 결과를 본 뒤 기본 코드나 정답 기준을 슬쩍 바꾸지 않는다. 채택 여부와 비용·회귀를 결과에 남긴다.

과거 source archive와 평가 입력은 이동·수정하지 않았다. `team_memory.reference_*`와 기존 patch import는 호환 경로로 남아 있다. 과거 CUPMem/초기 harness 파일은 기존 위치에서 재생용으로 유지한다.
