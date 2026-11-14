# 기여 안내

먼저 [모듈 지도](docs/architecture.md)에서 변경할 책임을 찾는다. 운영 경로는 `service → storage/review/readers`이며, 새 실험 후보는 `team_memory/experiments`, 평가 코드는 `evaluation`, 측정 결과는 `results`에 둔다. 호환 파일과 `_vendor`에 새 프로젝트 로직을 넣지 않는다.

## 개발 환경

Python3.11을 reference 개발 환경으로 사용한다. 코어는 Python3.12에서도 CI 검사한다.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -e '.[reference,dev]'
```

저장·상태 코어만 수정한다면 `.[dev]`로 설치할 수 있다. 실제 모델 가중치와 API key는 단위 테스트에 필요 없다. reference 검사에는 별도 NLTK 자료와 캐시된 tokenizer가 필요하다. 준비 명령은 [평가 환경 안내](docs/evaluation-guide.md)와 [CI](.github/workflows/tests.yml)에 있다.

## 로컬과 CI의 같은 검사

```sh
.venv/bin/python scripts/check.py core
.venv/bin/python scripts/check.py reference --fail-on-skip
# 둘을 한 번에 실행
.venv/bin/python scripts/check.py all
```

`pytest` 기반으로 unittest 클래스와 함수형 테스트를 모두 수집한다. reference 선택에는 NLTK/JSON Patch를 쓰는 관계·패치 검사도 포함한다. 코어의 과거 외부 캐시 검사에서 skip이 발생하면 재현하지 못한 범위를 보고한다. reference job은 skip도 실패다. 로컬 HTTP 전송 검사는 localhost bind가 가능한 환경에서 실행한다.

CUPMem 원형 어댑터의 오프라인 검사에는 다음 고정 소스를 사용한다. 없으면 관련 검사가 skip될 수 있다.

```sh
git clone https://github.com/icedreamc/STALE.git .cache/cupmem-upstream
git -C .cache/cupmem-upstream checkout --detach ea7d391103a151927cd29d2f01d87597a782bdcb
cp evaluation/cupmem/upstream-manifest.json .cache/cupmem-upstream/UPSTREAM_MANIFEST.json
export CUPMEM_UPSTREAM_ROOT="$PWD/.cache/cupmem-upstream"
```

모델 호출 없는 공유 흐름과 배포 패키지도 확인한다.

```sh
.venv/bin/python -m team_memory demo
.venv/bin/python -m team_memory demo --followup
.venv/bin/python -m team_memory.packaging /tmp/team-memory-code.tar.gz > /tmp/team-memory-code-manifest.json
.venv/bin/python -m evaluation.service_v2_package_check /tmp/team-memory-code.tar.gz
.venv/bin/python -m pip wheel --no-deps --no-build-isolation . -w /tmp/team-memory-wheels
```

archive 경로가 이미 있으면 덮어쓰지 않는다. 다른 새 이름을 사용한다. 모델 다운로드·추론·학습은 위 검사와 구분하며 Aurora에서는 Slurm 계산 노드에서 실행한다.

## 변경 제출

- **문제:** 실제 입력, 당시 보였던 원문, 기대 결과와 관측한 실패를 적는다. 공개 가능한 자료나 합성 최소 사례를 사용한다.
- **책임:** 어느 모듈의 어떤 계약을 바꾸는지, 앞뒤 모듈에 필요한 정보가 무엇인지 설명한다.
- **근거:** 논문 아이디어, 저자 코드 재사용, 전체 재현을 구분한다. 원형의 조건과 달라지는 부분을 명시한다.
- **검증:** 바뀐 실패와 기존 성공을 함께 확인한다. 출처 위치 일치와 의미 지지를 구분한다. `ok`를 정답 인증으로 쓰지 않는다.
- **비용:** 새 모델 단계는 호출·토큰·실패 경로·준비 시간을 함께 기록한다. 구조 정리만 했다면 모델 성능 향상으로 보고하지 않는다.
- **호환:** 저장 ID, 원문, 상태, CLI/import, 기존 결과 archive를 유지하는지 확인한다.

## 실험과 결과

입력·모델·프롬프트·평가·중단/채택 기준은 결과 전에 고정한다. 개발에 반복 사용한 이야기와 새 사례를 구분한다. 원출력·실패·채점 이유·환경·실제 비용을 보존한다. 재생과 새 추론, 검색 포함 평가와 고정 근거 독해를 구분한다. [평가 안내](evaluation/README.md).

동결 manifest나 source archive를 구조 정리 때문에 덮어쓰지 않는다. 새 모듈 경로를 포함하는 패킷은 `team_memory.packaging.source_paths`로 만들고 새 실행 버전을 사용한다. `team_memory/store.py`는 과거 데이터의 해시 기준이라 원본 위치에 유지한다.

## 라이선스

팀 코드의 재사용 라이선스는 결정 전이다. 임의로 라이선스를 추가하지 않는다. vendor 원본의 LICENSE/NOTICE와 자료의 출처·revision·변형 범위를 유지한다.
