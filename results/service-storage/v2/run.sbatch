#!/usr/bin/env bash
#SBATCH --job-name=capsm-storage-cost-v2
#SBATCH --partition=batch_ugrad
#SBATCH --account=ugrad
#SBATCH --nodes=1
#SBATCH --nodelist=aurora-g8
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --gres=gpu:1
#SBATCH --time=12:00:00
#SBATCH --qos=qos_pjw031003_2026_2
#SBATCH --no-requeue
#SBATCH --export=NONE
#SBATCH --chdir=/ceph_data/pjw031003/capstone-shared-knowledge
#SBATCH --output=/ceph_data/pjw031003/capstone-shared-knowledge/logs/sm-%j.log
set -euo pipefail
source /ceph_data/pjw031003/anaconda3/etc/profile.d/conda.sh
conda activate /ceph_data/pjw031003/capstone-shared-knowledge/runtime/cupmem-qwen3-v1
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=8 TOKENIZERS_PARALLELISM=false
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_IMPLICIT_TOKEN=1 HF_HUB_DISABLE_TELEMETRY=1
mkdir /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-storage-cost-v2/code
tar -xzf /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-storage-cost-v2/code.tar.gz -C /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-storage-cost-v2/code
export NLTK_DATA=/local_datasets/pjw031003/capstone-shared-knowledge/reference-nltk/120445
test -f "$NLTK_DATA/tokenizers/punkt_tab/english/ortho_context.tab"
unset OPENAI_API_KEY BAZE_API_KEY HF_TOKEN HUGGING_FACE_HUB_TOKEN
export PYTHONPATH=/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-storage-cost-v2/code:/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-record-groups-v1b/reference-extra:/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-quote-v2/reference-extra:/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-fix-v1/reference-extra
/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v1/reference-env/bin/python -u /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-storage-cost-v2/code/evaluation/storage_cost/run.py --packet /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-storage-cost-v2 --output /ceph_data/pjw031003/capstone-shared-knowledge/results/storage-cost-${SLURM_JOB_ID}.json
