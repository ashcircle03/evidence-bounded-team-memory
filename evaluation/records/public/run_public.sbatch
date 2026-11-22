#!/usr/bin/bash
#SBATCH -J records-public
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-gpu=8
#SBATCH --mem-per-gpu=32G
#SBATCH -w aurora-g4
#SBATCH -t 0-06:00:00
#SBATCH -o logs/records-public-%A.out
# The teammate's public development comparison (Slurm 124911) on this branch.
# Submit from /data/$USER/harness (logs/ must exist):
#   sbatch -p <batch partition> records-dev/evaluation/records/public/run_public.sbatch
# Conditions (VARIANTS): default source nopredict staged. RUN_MAIN=1 also reruns main
# with the teammate's own run-qwen.sh (checks that this environment reproduces 124911).
set -uo pipefail
H=/data/$USER/harness
BUNDLE=${RECORDS_BUNDLE:-/local_datasets/records-124911-jsc66519075}
REPO=${REPO:-$H/records-dev}
VARIANTS=${VARIANTS:-"default source nopredict staged"}
export RECORDS_BUNDLE=$BUNDLE
export RECORDS_MODEL_DIR=${RECORDS_MODEL_DIR:-/data/$USER/models/Qwen3-8B}
export RECORDS_CONDA_PREFIX=${RECORDS_CONDA_PREFIX:-$H/env}

OUT=$H/results/records-public-$SLURM_JOB_ID
mkdir -p "$OUT"
{ hostname; date -Is; git -C "$REPO" rev-parse HEAD; echo "variants=$VARIANTS run_main=${RUN_MAIN:-0}"; } > "$OUT/run.txt"

for v in $VARIANTS; do
  echo "== variant $v $(date -Is)"
  bash "$REPO/evaluation/records/public/run_variant.sh" "$OUT/$v" "$REPO" "$v" > "$OUT/$v.log" 2>&1
  echo "$v exit=$?" | tee -a "$OUT/exit_codes.txt"
done
if [[ ${RUN_MAIN:-0} == 1 ]]; then
  echo "== main (teammate run-qwen.sh) $(date -Is)"
  bash "$BUNDLE/run-qwen.sh" "$OUT/main" "$H/records-main" > "$OUT/main.log" 2>&1
  echo "main exit=$?" | tee -a "$OUT/exit_codes.txt"
fi

# Scoring (no inference): the 124911 baseline and every new run, with the teammate's score.sh.
# score.sh calls `python` from PATH; do not depend on the submitting shell's conda env.
export PATH=${SCORE_PYTHON_BIN:-/data/$USER/anaconda3/envs/team-memory/bin}:$PATH
bash "$BUNDLE/score.sh" > "$OUT/score-124911.json" 2> "$OUT/score-124911.err"
for f in "$OUT"/*/results/records-current-*.jsonl; do
  [[ -e $f ]] || continue
  name=$(basename "$(dirname "$(dirname "$f")")")
  bash "$BUNDLE/score.sh" "$f" > "$OUT/score-$name.json" 2> "$OUT/score-$name.err"
done
tar -czf "$OUT.tar.gz" -C "$H/results" --exclude='*/verified-model' "records-public-$SLURM_JOB_ID"
echo "done: $OUT  archive: $OUT.tar.gz"
