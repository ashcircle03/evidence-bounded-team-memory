#!/usr/bin/env bash
#SBATCH --job-name=capsm-cup-ref-quote-v2
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
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=8 TOKENIZERS_PARALLELISM=false
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_IMPLICIT_TOKEN=1 HF_HUB_DISABLE_TELEMETRY=1
export VLLM_USE_V1=1 VLLM_WORKER_MULTIPROC_METHOD=spawn
mkdir /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-quote-v2/code
tar -xzf /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-quote-v2/code.tar.gz -C /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-quote-v2/code
export NLTK_DATA=/local_datasets/pjw031003/capstone-shared-knowledge/reference-nltk/$SLURM_JOB_ID
/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v1/reference-env/bin/python -u /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-quote-v2/prepare_nltk.py
/ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-qa-v1/reference-env/bin/python -m pip install --disable-pip-version-check --no-input --no-deps --target /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-quote-v2/reference-extra scikit-learn==1.7.2
unset OPENAI_API_KEY BAZE_API_KEY HF_TOKEN HUGGING_FACE_HUB_TOKEN
python -u /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-ref-quote-v2/serve.py
