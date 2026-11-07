# 평가를 읽고 재현하는 방법

2026-11-08. 이 안내는 **저장된 실행을 검증하는 것**과 **새 모델 출력을 얻는 것**을 분리한다. 최신 결과는 [service-v3](../results/service-v3/README.md), 이전 모든 단계는 [연구 이력](research-history.md)에 있다.

## 어떤 질문을 평가했는가

| 평가 축 | 성공으로 보려는 것 | 함께 읽을 실패 지표 |
|---|---|---|
| 일반 QA | 정답 내용과 필요한 원문 근거 | 정답 손실, 검색 누락, 잘못된 작성자·날짜·조건 |
| 상충 QA | 질문에 실제로 다른 답을 주는 양쪽 기록과 근거 | 한쪽 답 삭제, 무관한 충돌 때문에 기권 |
| 재검토 | 옛 결정의 이유와 새로 달라진 조건을 원문에 대응 | 대상/종류만 맞고 이유가 틀림, 음성에서 불필요 제안 |
| 상태 적용 | pending/rejected/approved를 시점에 맞게 구분 | 미승인 값을 현재값으로 승격, 거절 상태 누락 |
| 인용 | 출처·구절 존재와 해당 주장의 의미 지지 | 정확한 문자열이지만 설명을 지지하지 않음 |
| 협업·비용 | 재시작·Git 공유·상태 수렴·추적 가능성 | 잘못된 actor, 중복 처리, 모델 호출·실패·준비 비용 |

구조 검증(해시, ID, offset), 의미 검토(답·설명이 맞는지), 런타임 상태(COMPLETED/exit code)는 별도다. 하나가 통과했다고 나머지가 자동 성공하지 않는다.

## 데이터 구성과 평가 범위

- **EverMemBench-Dynamic:** 실제 공개 데이터셋의 대화/QA를 사용한다. 기존 개발10과 최신 다른 주제의6문항을 구분한다. 최신6문항은 topics03/04에서 F_SH/F_MH/F_TP 각1개씩 고정 해시로 선택했고, 두 reader에 같은 BM25 top8/512/64 묶음을 제공했다. 배포 hybrid 검색의 전수평가가 아니다.
- **WikiContradict:** 상충 문단쌍의 양쪽 답과 근거 보존을 본다. 기존8개와 중복하지 않는 최신6개를 사용한다. 원본 정답 키와 별도 원문 검토를 보존했다.
- **공개 Git/PEP:** 과거 결정과 후속 보고를 복원한다. 실제 문서라는 점과 평가를 위해 양성/음성 쌍을 구성했다는 점을 모두 밝힌다.
- **기존 QA20:** 여러 공개 원문과 조건/상충 변형을 포함한 반복 개발·회귀셋이다. 독립 holdout이나20개 모두 자연 EverMem 문항이 아니다. [공개 묶음](../evaluation/qa20/README.md).
- **최신 합성8흐름:**11개 QA시점과8개 새 보고를 실제 서비스에 넣었다. 승인자는 가상 fixture이며, source location의 설명적 이름이 모델에 보인다. 실제 Git 사건 일반화 증거로 쓰지 않는다.

원본 저장소·revision·선택 제외 목록은 [manifest](../evaluation/service_v3/dataset-manifest.json)와 [exclusions](../evaluation/service_v3/exclusions.json)에 있다. 원본 데이터셋의 분포와 작은 선택셋의 분포는 다르다.

## 최신 결과의 검증 순서

1. [PROTOCOL](../results/service-v3/PROTOCOL.md), [freeze-final](../results/service-v3/freeze-final.json): 실행 전에 고정한 기준·코드·입력 해시를 확인한다.
2. [inputs](../results/service-v3/inputs.json), [calls](../results/service-v3/calls.jsonl): 실제 질문·근거와 전송된 모델 요청/원출력을 확인한다.
3. [result](../results/service-v3/result.json):86개 QA출력과 실제 저장된 원문·제안·투표·스냅샷을 확인한다.
4. [ratings](../results/service-v3/ratings.json), [cards](../results/service-v3/blind-cards.json), [mapping](../results/service-v3/blind-mapping.json): 문항별 원문 기반 판정 이유를 본다. arm을 가렸으나 독립 사람 평가가 아니다.
5. [decision](../results/service-v3/decision.json)과 [deployment-decision](../results/service-v3/deployment-decision.json)을 함께 본다. 비용 규칙의 잠정 direct 선택과, 기존 QA 손실 때문에 전면 교체하지 않은 적용 결정을 구분한다.
6. [failure-audit](../results/service-v3/failure-audit.json), [accounting](../results/service-v3/accounting.json): 실제 입력에서 확인한 원인, 출력 잘림, 실패 시도까지 포함한 비용을 읽는다.

Wiki202의400shillings를20pounds와 같은 의미값으로 인정한 점수와, 질문 단위로20을 명시해야 한다는 엄격 점수는 보고서에 둘 다 있다. 상대차이와 설계 결론은 같다. Wiki235 원문의 지시어 모호성도 기록했으며 원본 정답 키를 사후 변경하지 않았다.

## 모델 없이 최신 결과 재검증

Python3.12와 Git으로 저장소를 받은 뒤 루트에서 실행한다. 아래 명령은 **복사본**을 검사하므로 고정 결과를 덮어쓰지 않는다. 새 모델 호출이나 GPU가 필요 없다.

```sh
python3 - <<'PYCODE'
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib, json, shutil
from evaluation.service_v3.verify import verify
from evaluation.service_v3.score import main as score
src = Path('results/service-v3')
freeze = json.loads((src / 'freeze-final.json').read_text())
packet = Path('evaluation/service_v3/runtime-final')
for name, expected in freeze['files'].items():
    assert hashlib.sha256((packet / name).read_bytes()).hexdigest() == expected, name
with TemporaryDirectory() as tmp:
    dst = Path(tmp) / 'comparison'
    shutil.copytree(src, dst)
    verify(dst)
    score(dst)
    for name in ('verification.json', 'blind-cards.json', 'blind-mapping.json', 'decision.json'):
        assert json.loads((dst / name).read_text()) == json.loads((src / name).read_text()), name
print('Frozen packet, structural checks and stored-rating decision reproduced.')
PYCODE
```

이 검증은 이미 작성된 ratings의 집계와 인용 구조를 재현한다. 의미 판정의 독립 재평가나 새로운 LLM 추론이 아니다. 최신 service에 의존하는 회귀 검사는 아래 환경을 준비한 뒤 [기여 안내](../CONTRIBUTING.md)의 명령을 실행한다. CPython/Git 입력 복원은 [이전 재현 안내](../evaluation/cpython/README.md)를 따른다.

## 실제 서비스·검사를 위한 환경

로컬 검사/CI는 Python3.11의 reference 의존성과 Python3.12 표준 라이브러리 검사를 분리한다. 다음은 reference 검사에 필요한 설치 예시다. 모델 서버를 설치·구동하는 명령은 아니다.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -r requirements-reference.txt
export NLTK_DATA="$PWD/.cache/reference-nltk"
.venv/bin/python -m nltk.downloader -d "$NLTK_DATA" punkt_tab stopwords
.venv/bin/python - <<'PYCODE'
from huggingface_hub import snapshot_download
snapshot_download('Qwen/Qwen3-8B', revision='b968826d9c46dd6066d109eabc6255188de91218',
    local_dir='.cache/qwen-tokenizer',
    allow_patterns=['tokenizer*', 'config.json', 'vocab.json', 'merges.txt', 'special_tokens_map.json'])
PYCODE
```

CPU torch는 **로컬 검사/CI용**이다. Aurora 실제 추론에서는 기존 CUDA·vLLM conda 환경을 사용했다. 이번 공개 정리에서 CUDA 환경을 클린 재설치하거나 논문 환경을 재현한 것은 아니다. 실제 서버/client interpreter·패키지·모델 해시는 result와 runtime config에 남아 있다. Python package pin만으로 서버 환경 전체가 재현된다고 보지 않는다.

## 새 모델 실행과 동결 실행 묶음

[실제 제출 묶음](../evaluation/service_v3/runtime-final/README.md)에 job120370의 config, sbatch, 서버/client 실행기, 작은 NLTK 자료와 **동결 source archive**를 원본 그대로 공개했다. 해시는 freeze와 일치한다. 모델 가중치·전체 데이터셋·과거 캠페인 환경은 포함하지 않는다.

새 실행은 별도 출력 디렉터리와 별도 config로 준비한다. 서버 경로·conda·계정·캐시를 자신의 환경에 맞춘다. 원 실험 설정은 Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`, nonthinking, temperature0, context32768, answer1024, judge384다. 원 데이터 revision을 유지하고 새 출력은 별도 채점한다.

`evaluation.service_v3.prepare`는 당시 프로젝트의 외부 campaign 경로를 사용하는 역사적 제출 준비 코드다. clean clone에서 그대로 실행 가능한 설치 명령으로 제공하지 않는다. 최신 공개 묶음은 그 외부 경로 없이 당시 source/config를 검토할 수 있게 만든 것이다. 새 job을 자동 제출하지 않는다.

Aurora 규칙: 계산 노드에 GPU 최소1개를 할당하고 conda를 활성화한다. 기본 walltime12시간, 작업 완료 즉시 종료하며 노드를 임의 고정하지 않는다. 로그인 노드에서 Python·재귀 탐색·데이터 처리·추론을 실행하지 않는다. 기존 job을 중복 제출/취소하지 않는다. 실제 새 실행 전 queue·dispatch와 해당 작업의 입력/자원 설정을 확인한다.

## 공개 범위

코드, 설정, 평가 입력/키, 실제 요청·응답, 실패 자료, 채점 이유, 자원 기록을 공개한다. 모델 가중치, 로컬 캐시, 인증정보와 비밀키는 제외한다. 과거 일부 대용량 raw trace는 원래 공개 범위대로 제외돼 있으며 해당 단계의 보고서와 manifest가 그 경계를 설명한다. upstream 자료의 권리는 원출처에 남고 팀 코드의 라이선스는 아직 결정 전이다.
