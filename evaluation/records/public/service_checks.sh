#!/usr/bin/bash
#SBATCH -J rec-service
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-gpu=8
#SBATCH --mem-per-gpu=32G
#SBATCH -w aurora-g4
#SBATCH -t 0-02:00:00
#SBATCH -o /data/jsc66519075/harness/logs/rec-service-%A.out
# Service metrics for the current records-dev code, without new model inference:
#  1. replay stored Qwen outputs of a public run -> condition precision / recovery (score.sh)
#  2. provenance: store + cold restart of every document (full and compact storage)
#  3. QA 20 replay (evaluation.module_adapters.replay): answers and evidence preserved
# Usage (from /data/$USER/harness): sbatch -p batch_ugrad records-dev/evaluation/records/public/service_checks.sh <run dir> <name>
set -uo pipefail
H=/data/jsc66519075/harness; B=/local_datasets/records-124911-jsc66519075; REPO=$H/records-dev
RUN=$1; NAME=$2; OUT=$H/results/service-$NAME; mkdir -p "$OUT"
{ git -C $REPO log --oneline -1; git -C $REPO status --short; } > "$OUT/code.txt"
SNAP=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['snapshot_at'])" "$RUN/config.json")
CLIENT_PATH=$REPO:$B/client-packages:$B/reference-extras/sm-record-groups-v1b:$B/reference-extras/sm-cup-ref-quote-v2:$B/reference-extras/sm-cup-ref-fix-v1
export NLTK_DATA=/home/jsc66519075/nltk_data RECORD_INPUTS=$B/cache/panel.json TOKENIZERS_PARALLELISM=false OMP_NUM_THREADS=8

echo "== 1 replay + score"
rm -f "$OUT/records.jsonl"
PYTHONPATH=$CLIENT_PATH $H/env/bin/python $REPO/evaluation/records/public/replay_outputs.py "$RUN" "$OUT/records.jsonl" --variant default > "$OUT/replay.log" 2>&1
echo "replay exit=$?" | tee "$OUT/exit.txt"
PATH=/data/jsc66519075/anaconda3/envs/team-memory/bin:$PATH bash $B/score.sh "$OUT/records.jsonl" > "$OUT/score.json" 2> "$OUT/score.err"
echo "score bytes=$(wc -c < "$OUT/score.json")" | tee -a "$OUT/exit.txt"

echo "== 2 provenance"
PYTHONPATH=$CLIENT_PATH $H/env/bin/python $REPO/evaluation/records/public/check_provenance.py "$OUT/records.jsonl" $B/cache/panel.json "$OUT/provenance.json" --snapshot-at "$SNAP" > "$OUT/provenance.log" 2>&1
echo "provenance exit=$?" | tee -a "$OUT/exit.txt"

echo "== 3 QA20 replay"
mkdir -p $REPO/.cache
[ -e $REPO/.cache/qwen-tokenizer ] || ln -s /data/jsc66519075/models/Qwen3-8B $REPO/.cache/qwen-tokenizer
[ -e $REPO/.cache/reference-nltk ] || ln -s /home/jsc66519075/nltk_data $REPO/.cache/reference-nltk
rm -rf "$OUT/qa20"
(cd $REPO && PYTHONPATH=$REPO /data/jsc66519075/anaconda3/envs/team-memory/bin/python -m evaluation.module_adapters.replay --output "$OUT/qa20") > "$OUT/qa20.log" 2>&1
echo "qa20 exit=$?" | tee -a "$OUT/exit.txt"
