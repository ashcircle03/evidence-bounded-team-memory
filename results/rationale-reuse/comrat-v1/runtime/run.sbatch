#!/usr/bin/env bash
#SBATCH --job-name=capsm-cup-comrat-original-v1
#SBATCH --partition=batch_ugrad
#SBATCH --account=ugrad
#SBATCH --nodes=1
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
export PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=8
unset OPENAI_API_KEY BAZE_API_KEY HF_TOKEN HUGGING_FACE_HUB_TOKEN
export RATIONALE_ROOT=/local_datasets/pjw031003/capstone-shared-knowledge/rationale-reuse/$SLURM_JOB_ID
mkdir -p "$RATIONALE_ROOT"
curl -fLsS --retry 2 --connect-timeout 30 --max-time 180 https://zenodo.org/api/records/14176549/files/replication_package.zip/content -o "$RATIONALE_ROOT/comrat.zip"
python - "$RATIONALE_ROOT" <<'PY'
from pathlib import Path
from hashlib import sha256
import sys,zipfile
p=Path(sys.argv[1]);a=p/'comrat.zip'
assert sha256(a.read_bytes()).hexdigest()=='e50e3f67938f00bb7aafd81804f671b407b6a78f02f821449ad887894ae30e4f'
with zipfile.ZipFile(a) as z:
    for n in z.namelist():
        if not n.startswith('replication_package/Rationale-Analyses-Tool/') or n.endswith('/') or '/.streamlit/' in n: continue
        target=(p/n).resolve();assert p.resolve() in target.parents
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(n))
PY
conda create -y -p "$RATIONALE_ROOT/env" python=3.11 pip > "/ceph_data/pjw031003/capstone-shared-knowledge/logs/sm-$SLURM_JOB_ID-setup.log" 2>&1
conda activate "$RATIONALE_ROOT/env"
export MPLCONFIGDIR="$RATIONALE_ROOT/mpl" PIP_CACHE_DIR="$RATIONALE_ROOT/pip-cache"
python -m pip install -r "$RATIONALE_ROOT/replication_package/Rationale-Analyses-Tool/requirements.txt" >> "/ceph_data/pjw031003/capstone-shared-knowledge/logs/sm-$SLURM_JOB_ID-setup.log" 2>&1
python -m pip freeze > "/ceph_data/pjw031003/capstone-shared-knowledge/results/sm-$SLURM_JOB_ID-environment.txt"
python -u /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-comrat-original-v1/run.py /ceph_data/pjw031003/capstone-shared-knowledge/source/sm-cup-comrat-original-v1 "$RATIONALE_ROOT/replication_package/Rationale-Analyses-Tool"
