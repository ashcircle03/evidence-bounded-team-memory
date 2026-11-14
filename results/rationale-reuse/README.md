# 공개 결정·근거 추출 구현: 조사와 원본 실행

2026-11-08. **CoMRAT의 공개 출력을 재현했지만, 우리 서비스의 필수 분류 단계로는
채택하지 않는다.** 기본 서비스 파일57개의 해시가 실행 전후 같으며 QA/정정 경로는
변경하지 않았다. 기존 QA20/상태8은 이번에 다시 평가하지 않았다.

구현 조사: [rationale-reuse-audit](../../docs/rationale-reuse-audit.md).
원본 출처: [CoMRAT 재현 패키지](https://zenodo.org/records/14176549),
[Kantara 재현 패키지](https://zenodo.org/records/13742395), CC-BY-4.0,
Mouna Dhaouadi, Bentley Oakes, Michalis Famelis.

## 원형을 어떻게 실행했는가

실제 `pages/commit.py:user_commit_page`를 호출했다. UI 입력·표시만 headless adapter로
대체하고 원래 전처리, 학습된 H5 두 개, 토크나이저 복원 데이터, padding, >0.5 기준을
유지했다. 새 분류기나 LLM 프롬프트를 작성하지 않았다. GitHub/API 자격증명 없이
계산 노드의 `/local_datasets`에 원본을 다운로드하고 SHA256을 확인했다.

Slurm `120443`: **COMPLETED / 0:0**, GPU1 예약, CPU8, RAM48G, 12h walltime,
conda Python3.11, 원 저자 TensorFlow2.13/Keras2.13.1. 총 할당 시간9분19초,
원본 함수34회 추론 구간8.42초. TensorFlow는 GPU 라이브러리를 로드하지 못해
**실제 추론은 계산 노드 CPU**에서 수행했다. GPU를 예약한 사실을 GPU 추론으로
표현하지 않는다. 로그인 노드에서는 계산하지 않았다. batch MaxRSS는337912K이며
비어 있는 최상위 MaxRSS를0으로 해석하지 않는다.

## 결과

| 검사 | 결과 | 의미 |
|---|---:|---|
| 저자 공개 예측 라벨 재현 | **24/24** | 예제12개 × Decision/Rationale. 정답 정확도가 아닌 실행 일치 |
| 같은 예제의 인간5명 다수결과 일치 | **20/24** | 작은 공개 사례 부분집합. 학습/선정 영향을 배제한 새로운 벤치마크가 아님 |
| 우리 이유 있는 과거 결정 탐지 | **2/4** | writer2건 성공, cache2건 누락. 중복 원문을 합치면 **1/2** |
| 우리 사실 기록 오탐 | **1/7** | relay interval을 이유 있는 결정으로 판단 |
| 원본 전처리가 만든 추가 빈 행 | **34** | 모든 입력이 한 줄이라 본문에 빈 문자열이 생김. 근거로 세지 않음 |
| 사전 고정한 후보 통과 조건 | **실패** | 전체 결정4건 탐지 및 사실 오탐0을 충족하지 못함 |

### 과거 기록별 판별

아래 확률은 원본 sigmoid 출력이며 보정된 신뢰도가 아니다. `D&R`은 빈 문자열을
제외한 문장에서 Decision과 Rationale을 모두 찾았는지 보는 적용성 진단이다.

| 원문 시나리오 | D 확률 | R 확률 | 기대 | 결과 |
|---|---:|---:|---|---|
| Cedar 업로드 상한500MB | .0422 | .0120 | 사실 | 유지 |
| Delta 회의요일Monday | .2847 | .0036 | 사실 | 유지 |
| JPEG quality80 측정600KB | .0326 | .4406 | 사실 | 유지 |
| Nimbus 조건W/build7 측정23ms | .0056 | .0010 | 사실 | 유지 |
| writer-reopen: version4 제약 때문에 병렬 쓰기 보류 | .8392 | .8655 | 이유 있는 결정 | 탐지 |
| writer-near-miss: 위와 동일한 과거 원문 | .8392 | .8655 | 이유 있는 결정 | 탐지 |
| cache-reopen: 정책 때문에 세션 캐싱 중단 | .1011 | .7255 | 이유 있는 결정 | **Decision 누락** |
| cache-near-miss: 위와 동일한 과거 원문 | .1011 | .7255 | 이유 있는 결정 | **Decision 누락** |
| Iris 온도40C | .0145 | .0442 | 사실 | 유지 |
| Mira 보관기간90일 | .1760 | .0928 | 사실 | 유지 |
| Sol interval6초 | .5268 | .9517 | 사실 | **오탐** |

cache 원문은 “We disabled user-session caching because the policy forbade keeping
session identifiers in memory after a request completed.”이다. 근거 라벨은 맞지만
결정 라벨이 없어서 AND 필터를 통과하지 못한다. 반대로 “For relay Sol, the interval
is 6 seconds.”는 근거를 표현하지 않았는데도 두 라벨이 모두 켜졌다.

새 보고의 두 사실 정정(온도/보관기간)도 D&R로 분류됐다. 원 저자의 Decision
정의에는 변경 행위가 포함되므로 D=1 자체가 잘못이라고 단정할 수 없다. 하지만
그 출력은 곧바로 '이유 있는 정책 결정'이나 '과거 결정 재검토'와 같지 않다.

### 이번 결과가 바꾼 판단

1. 저자의 학습된 분류기를 실행하는 데 성공했다. 기존 출력 일치가 있으므로 이
   파일럿의 실패를 우리 adapter가 모델을 잘못 호출한 문제로 설명할 근거는 없다.
2. 작은 커밋 분류기를 일반 팀 기록에 그대로 적용하면 누락과 오탐이 남는다.
   사후 threshold 변경이나 라벨 OR 조건으로 같은 사례를 맞추지 않는다.
3. 재검토 경로의 추출 결과가 기존 사실 정정을 억제하면 안 된다. ConDec의
   '자동 추출은 미검증 상태'라는 계약을 참고할 수 있지만 정확한 분류를 대신하지는 않는다.
4. 연구 초점은 일반 메모리 CRUD가 아니라 **decision/rationale extraction과
   applicable-condition 추론**에 더 직접적으로 연결되어야 한다. Kantara/ConDec는
   실제 구현 참고이고, DesignHunter는 조건별 대안·미채택 제안 보존의 직접적인
   연구 참고다. 아직 우리 재검토 문제 전체가 해결됐다는 증거는 없다.

## 파일 및 재검증

- [사전 고정 기준](comrat-v1/runtime/PROTOCOL.md), [입력](comrat-v1/runtime/inputs.json),
  [정답/비교 라벨](comrat-v1/keys.json), [freeze](comrat-v1/freeze.json).
- [실제 입력·확률·token IDs·출력](comrat-v1/result.json), [문항별 판정](comrat-v1/cases.json),
  [요약](comrat-v1/summary.json), [Slurm 자원 기록](comrat-v1/dispatch.json),
  [환경](comrat-v1/environment.txt), [로그](comrat-v1/run.log).
- `upstream-audit/`에는 두 배포본 파일 해시와 감사에 사용한 노트북 code cell이 있다.
  코드 출처/CC-BY-4.0을 함께 보존했고 인증 설정과 전체 노트북 출력은 포함하지 않았다.
- `.venv/bin/python -m evaluation.service_completion.score_comrat`는 Slurm 종료,
  프로그램 완료, 입력·평가기준·원본 모델·서비스 해시를 확인한 뒤 같은 결과를 계산한다.

이 결과는 EverMemBench, WikiContradict, STALE의 전체 성능도 아니고 QA 회귀 검증도
아니다. 다음 단계의 후보 선정 근거이며 기본 모듈 채택 결과와 분리한다.
