#!/usr/bin/env bash
#SBATCH --job-name=capsm-record-groups-v1b
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
export VLLM_USE_V1=1 VLLM_WORKER_MULTIPROC_METHOD=spawn
mkdir /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-record-groups-v1b/code
tar -xzf /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-record-groups-v1b/code.tar.gz -C /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-record-groups-v1b/code
export NLTK_DATA=/local_datasets/pjw031003/capstone-shared-knowledge/reference-nltk/120445
test -f "$NLTK_DATA/tokenizers/punkt_tab/english/ortho_context.tab"
unset OPENAI_API_KEY BAZE_API_KEY HF_TOKEN HUGGING_FACE_HUB_TOKEN
# Isolated client-only dependencies, on the assigned compute node; never mutate old environments.
/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v1/reference-env/bin/python -m pip install --disable-pip-version-check --no-cache-dir --no-deps --target /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-record-groups-v1b/reference-extra langextract==1.7.2 absl-py==2.3.1 pandas==2.2.3 python-dateutil==2.9.0.post0 pytz==2025.2 tzdata==2025.2 more-itertools==10.8.0 six==1.17.0
PYTHONPATH=/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-record-groups-v1b/code:/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-record-groups-v1b/reference-extra:/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-quote-v2/reference-extra:/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-fix-v1/reference-extra /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v1/reference-env/bin/python -c 'from team_memory.records.grouped import components; components(); print("GROUPED_REFERENCE_IMPORT_OK")'
python -u /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-record-groups-v1b/serve.py
