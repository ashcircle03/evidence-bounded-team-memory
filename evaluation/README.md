# 평가와 재현

운영 구현은 `team_memory/`, 평가 입력·동결·채점은 이 폴더, 실제 출력과 판단은 `results/`에 둔다. 테스트 통과, 저장된 출력 재생, 새 모델 추론은 다른 검증이다.

| 작업 | 진입점 |
|---|---|
| 전체 평가 범위와 해석 | [평가 안내](../docs/evaluation-guide.md) |
| 휴대 가능한 기존 QA20 입력·정답 키 | [qa20/](qa20/) |
| 현재 레퍼런스 조합 진단 | [reference_audit/PROTOCOL.md](reference_audit/PROTOCOL.md) |
| 상태·입출력 검증 | [service_completion/](service_completion/)와 [결과](../results/module-boundary/README.md) |
| 비교기 모델 선택 | [comparator_choice/PROTOCOL.md](comparator_choice/PROTOCOL.md) |
| 이전 reader 동일근거 비교 | [결과·사전 기준](../results/service-v3/README.md) |
| 과거 연구 순서 | [연구 이력](../docs/research-history.md) |

## 새 실행

입력·모델 revision·프롬프트·채점 키·중단/채택 기준을 출력 전에 고정한다. 정답 키와 이전 답을 모델 packet에 넣지 않는다. 개발 사례 반복을 새 holdout 성과로 표시하지 않는다.

새 source packet은 하위 패키지와 vendor 자원을 모두 포함해야 한다:

```sh
python -m team_memory.packaging /tmp/team-memory-code.tar.gz > /tmp/team-memory-code-sha256.json
python -m evaluation.service_v2_package_check /tmp/team-memory-code.tar.gz
```

campaign builder에서는 `team_memory.packaging.source_paths(repo_root)`를 사용한다. 필요한 `evaluation/` runner/config는 별도로 명시해 추가한다. packager는 모델·평가 키·결과를 자동 포함하지 않는다.

## 과거 실행

과거 `prepare*.py`에는 당시 파일 목록과 외부 캠페인 경로가 고정돼 있다. 현재 구조에 새 version 문자열만 붙여 옛 source manifest를 재사용하지 않는다. 재현은 해당 결과 폴더의 동결 source archive/config/입력 해시를 사용한다. 재설계한 패키지는 새 버전과 새 source manifest를 만든다.

동결 파일과 모델 원출력은 수정하지 않는다. 재개 시 실제 job ID를 먼저 조회하며 중복 제출하지 않는다. `COMPLETED`, 종료코드0:0, 프로그램 완료와 입력 해시를 함께 확인한 뒤 채점한다. 서버 계산은 Slurm 계산 노드에서 수행한다.
