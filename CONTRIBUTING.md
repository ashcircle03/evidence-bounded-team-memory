# 기여 안내

질문/새 기록, 당시 보였던 원문, 기대 판단, 실제 판단을 함께 제시해 주세요. 원문 인용의 존재와 의미적 지지를 나눠 적습니다. 공개 가능한 자료나 가상 사례를 사용합니다. 현재 연결 경로는 [service 명세](docs/service-v2.md), 후보/과거 경로는 [연구 이력](docs/research-history.md)을 따릅니다.

## 검사 환경

표준 라이브러리 코어와 reference 라이브러리 검사를 분리합니다. 전체 discover가 의존성 없이 실행된다고 가정하지 않습니다. 아래 코어 검사는 Python3.12와 Git을 사용합니다.

```sh
python3 - <<'PYCODE'
from pathlib import Path
import unittest
paths = sorted(p for p in Path('tests').glob('test_*.py')
               if not p.name.startswith(('test_reference_', 'test_contextual_'))
               and p.name != 'test_service.py')
suite = unittest.TestLoader().loadTestsFromNames(['tests.' + p.stem for p in paths])
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
PYCODE
python3 -m team_memory demo
python3 -m team_memory demo --followup
```

CUPMem 원형 어댑터 검사까지 하려면 아래 고정 소스를 준비합니다. 없으면 해당 검사는 skipped입니다. 과거 캠페인/캐시에 의존하는 검사의 skip도 성공으로 세지 않습니다.

```sh
git clone https://github.com/icedreamc/STALE.git .cache/cupmem-upstream
git -C .cache/cupmem-upstream checkout --detach ea7d391103a151927cd29d2f01d87597a782bdcb
cp evaluation/cupmem/upstream-manifest.json .cache/cupmem-upstream/UPSTREAM_MANIFEST.json
export CUPMEM_UPSTREAM_ROOT="$PWD/.cache/cupmem-upstream"
```

[환경 준비](docs/evaluation-guide.md)를 따른 Python3.11 reference 환경에서는:

```sh
.venv/bin/python - <<'PYCODE'
from pathlib import Path
import unittest
paths = sorted(p for p in Path('tests').glob('test_*.py')
               if p.name.startswith(('test_reference_', 'test_contextual_'))
               or p.name == 'test_service.py')
suite = unittest.TestLoader().loadTestsFromNames(['tests.' + p.stem for p in paths])
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful() or bool(result.skipped))
PYCODE
```

reference 검사는 실제 라이브러리·캐시된 tokenizer와 stub 모델/로컬 HTTP 서버를 사용합니다. 모델 가중치·유료 API를 호출하지 않습니다. sandbox가 localhost bind를 막으면 전송 검사가 실패할 수 있으므로 실패를 숨기지 말고 허용된 환경에서 해당 검사를 확인합니다. CI의 reference job은 skip도 실패로 처리합니다. 실행 명령의 최신 원본은 [workflow](.github/workflows/tests.yml)입니다.

## 실험을 바꾸는 PR

1. 어떤 판단을 개선하려는지와 재사용하는 레퍼런스의 실제 책임을 적습니다. 논문 아이디어, 저자 코드 재사용, 전체 재현을 구분합니다.
2. 입력·모델·평가 기준·중단 조건을 새 결과 전에 고정합니다. 이미 본 개발 사례와 새 사례를 구분합니다.
3. 바뀐 최소 사례와 계속 맞혀야 하는 기존 QA/인용을 함께 확인합니다. 추가 단계는 비용과 실패 경로도 비교합니다.
4. 재생 호출과 새 호출, 검색을 포함한 평가와 고정 근거 독해를 분리합니다. 정답 위치를 제공했다면 명시합니다.
5. 원출력·실패·채점 이유·환경·실제 사용량을 보존합니다. 동결 결과나 과거 source archive를 덮어쓰지 않습니다.
6. 문서에는 실제 적용 기본값과 실험 후보를 구분합니다. `ok`나 문자열 위치 일치를 의미 정답 인증으로 쓰지 않습니다.

팀 코드의 재사용 라이선스는 결정 전입니다. vendor 원본의 LICENSE/NOTICE는 유지하며 외부 자료의 출처·revision·변형 범위를 기록합니다.
