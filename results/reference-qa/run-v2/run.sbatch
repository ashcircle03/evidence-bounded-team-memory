#!/usr/bin/env bash
#SBATCH --job-name=capsm-cup-ref-qa-v2
#SBATCH --partition=batch_ugrad
#SBATCH --account=ugrad
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --gres=gpu:1
#SBATCH --time=00:20:00
#SBATCH --no-requeue
#SBATCH --export=NONE
#SBATCH --chdir=/ceph_data/pjw031003/capstone-shared-knowledge
#SBATCH --output=/ceph_data/pjw031003/capstone-shared-knowledge/logs/sm-%j.log
set -euo pipefail
source /ceph_data/pjw031003/anaconda3/etc/profile.d/conda.sh
conda activate /ceph_data/pjw031003/capstone-shared-knowledge/runtime/cupmem-qwen3-v1
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=8 TOKENIZERS_PARALLELISM=false
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_IMPLICIT_TOKEN=1 HF_HUB_DISABLE_TELEMETRY=1
export VLLM_USE_V1=1 VLLM_WORKER_MULTIPROC_METHOD=spawn
mkdir /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v2/code
tar -xzf /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v2/code.tar.gz -C /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v2/code
unset OPENAI_API_KEY BAZE_API_KEY HF_TOKEN HUGGING_FACE_HUB_TOKEN
export NLTK_DATA=/local_datasets/pjw031003/capstone-shared-knowledge/reference-nltk/$SLURM_JOB_ID
timeout 120 /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v1/reference-env/bin/python /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v2/prepare_nltk.py
python -u /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v2/serve.py
