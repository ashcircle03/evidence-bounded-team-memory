# 공개 개발셋 비교 (PR #2, Slurm 124911) — records 브랜치

팀원의 공유본 `/local_datasets/records-124911-jsc66519075` (aurora-g4 전용, 읽기 전용)을 그대로 쓴다.
보정기·채점 캐시·QA-SRL·QANom 채점 코드·124911 원래 결과가 들어 있고, 팀원이 재채점으로 일치를 확인했다(작업 125229).
Qwen3-8B와 vLLM 환경(0.8.5.post1, 124911과 같은 버전)은 우리 것을 쓴다.

| 조건 | 코드 | 보정기 | 비교 |
|---|---|---|---|
| A `124911` | 팀원 원래 결과 | 있음 | 기준선 (채점만) |
| B `default` | 이 브랜치 | 있음 | A |
| C `source` | 이 브랜치 + `alignment='source'` | 있음 | A, B |
| D `nopredict` | 이 브랜치 | 없음 | E의 기준 |
| E `staged` | 2단계 추출 `staged.construct` | 없음 (미지원) | D |
| (선택) `main` | main, 팀원 `run-qwen.sh` 그대로 | 있음 | A와 같으면 우리 환경이 124911을 재현 |

`run_variant.sh`는 팀원 `run-qwen.sh`와 같은 단계이고 `client.py`만 `client_variants.py`로 바꾼다.
`default` 조건의 client 코드는 팀원 client와 같다 (`finish_reason` 기록만 추가).

## 실행 (aurora)
```bash
# PC에서: 코드 묶음 복사
scp -P 30080 records-dev.bundle jsc66519075@aurora.khu.ac.kr:/data/jsc66519075/harness/

# master에서 (git만)
cd /data/jsc66519075/harness
git clone -b records/alignment-and-blocks records-dev.bundle records-dev
git -C records-dev worktree add ../records-main 93e8a15   # RUN_MAIN=1 일 때만 필요
mkdir -p logs

# 제출 (파티션은 sinfo / show-assoc 로 확인)
sbatch -p <batch 파티션> records-dev/evaluation/records/public/run_public.sbatch
# main 재현 확인까지:  RUN_MAIN=1 sbatch -p <batch 파티션> records-dev/evaluation/records/public/run_public.sbatch
squeue -u $USER
tail -f logs/records-public-<jobid>.out

# PC로 결과 가져오기
scp -P 30080 jsc66519075@aurora.khu.ac.kr:/data/jsc66519075/harness/results/records-public-<jobid>.tar.gz .
```

## 결과
`results/records-public-<jobid>/`
- `score-124911.json`, `score-<조건>.json`: 팀원 `score.sh` 출력 (역할 연결 F1, 조건 복구·정밀도 등)
- `<조건>/results/records-current-<jobid>.jsonl`: 문서별 그래프와 Qwen 호출 (조건 오답 분석용)
- `<조건>/variant.json`: 실제로 import된 `team_memory` 경로 (우리 브랜치인지 확인)
- `exit_codes.txt`, `<조건>.log`

## 주의
- `RECORDS_MODEL_DIR`의 Qwen 파일이 124911 해시와 다르면 `run_variant.sh`가 시작 전에 멈춘다.
- `staged`는 보정기 연동이 없어 `nopredict`와 비교한다.
