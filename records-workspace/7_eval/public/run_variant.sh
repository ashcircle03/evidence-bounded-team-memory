#!/usr/bin/env bash
# Same steps as the teammate's run-qwen.sh (bundle /local_datasets/records-124911-*),
# with ONE difference: client.py is replaced by this repo's client_variants.py so a
# builder variant can be selected. The bundle itself is only read.
#   bash run_variant.sh <new run dir> <repo root> <default|source|nopredict|staged>
# Needs: Slurm allocation on aurora-g4, RECORDS_MODEL_DIR, RECORDS_CONDA_PREFIX (vLLM env),
# RECORDS_BUNDLE (default /local_datasets/records-124911-jsc66519075).
set -euo pipefail
umask 077
root=$(realpath "${RECORDS_BUNDLE:-/local_datasets/records-124911-jsc66519075}")
work=$(realpath -m "${1:?Provide a new writable run directory}")
repo=$(realpath "${2:?Provide your repository root}")
variant=${3:?Provide a variant: default, source, nopredict or staged}
input=$(realpath "${4:-$root/cache/panel.json}")
[[ -n ${SLURM_JOB_ID:-} && ${SLURMD_NODENAME:-} == aurora-g4 ]]
mkdir -- "$work"
mkdir -- "$work/results"
cp "$root/submission/"{config.json,serve.py,client.py} "$work/"
cp "$work/client.py" "$work/client.original.py"
cp "$repo/evaluation/records/public/client_variants.py" "$work/client.py"
env_prefix=${RECORDS_CONDA_PREFIX:-${CONDA_PREFIX:?Activate the Qwen vLLM conda environment}}
model_dir=$(realpath "${RECORDS_MODEL_DIR:?Set Qwen3-8B checkpoint directory}")
export RECORDS_BUNDLE_MODEL="$model_dir"
export CONDA_PREFIX="$env_prefix"
export PATH="$env_prefix/bin:$PATH"
export PYTHONDONTWRITEBYTECODE=1 TOKENIZERS_PARALLELISM=false OMP_NUM_THREADS=8
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_IMPLICIT_TOKEN=1 HF_HUB_DISABLE_TELEMETRY=1
export VLLM_USE_V1=1 VLLM_WORKER_MULTIPROC_METHOD=spawn
export RECORD_INPUTS="$input"
export RECORDS_VARIANT="$variant"
# records splits sentences with NLTK punkt_tab. Use the first folder that really has it,
# and stop before starting vLLM when none does (job 125230 failed on this).
nltk_dir=""
for candidate in ${NLTK_DATA_DIR:-} "$root/nltk_data" \
    /local_datasets/pjw031003/capstone-shared-knowledge/reference-nltk "/data/$USER/harness/nltk_data"; do
  if [[ -d "$candidate/tokenizers/punkt_tab/english" ]]; then nltk_dir=$(realpath "$candidate"); break; fi
done
if [[ -z $nltk_dir ]]; then
  echo "NLTK punkt_tab not found. Download it once, e.g.:" >&2
  echo "  python -m nltk.downloader -d /data/$USER/harness/nltk_data punkt_tab stopwords" >&2
  exit 2
fi
export NLTK_DATA="$nltk_dir"
echo "NLTK_DATA=$NLTK_DATA"
"$env_prefix/bin/python" - "$root" "$work" "$repo" <<'PY'
import json, os, sys
from pathlib import Path
root, work, repo = map(Path, sys.argv[1:])
path = work/'config.json'
cfg = json.loads(path.read_text())
extras = root/'reference-extras'
cfg.update(project=str(work), conda_prefix=os.environ['CONDA_PREFIX'], model_shared=os.environ['RECORDS_BUNDLE_MODEL'],
           role_dir=str(root/'role'), python_client=str(Path(os.environ['CONDA_PREFIX'])/'bin/python'),
           embedding=str(root/'projects/runtime/speakermem-v1/models/embed'),
           reference_extras=':'.join(str(extras/name) for name in (
               'sm-record-groups-v1b', 'sm-cup-ref-quote-v2', 'sm-cup-ref-fix-v1')))
model_dir = Path(cfg['model_shared'])
if not (model_dir/'READY.json').is_file():
    import hashlib
    for name, expected in cfg['model_files_sha256'].items():
        with (model_dir/name).open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != expected:
                raise ValueError(f'Model file hash mismatch: {name}')
    model_view = work/'verified-model'
    model_view.mkdir()
    for item in model_dir.iterdir():
        (model_view/item.name).symlink_to(item)
    (model_view/'READY.json').write_text(json.dumps({
        'revision': cfg['model_revision'], 'files_sha256': cfg['model_files_sha256'],
    }))
    cfg['model_shared'] = str(model_view)
path.write_text(json.dumps(cfg, indent=2))
(work/'service.py').write_text(
    'import os, sys\n'
    f'os.environ["PYTHONPATH"] = {":".join((str(repo), str(root/"client-packages"), cfg["reference_extras"]))!r}\n'
    # Pass NLTK data to the client explicitly, whatever environment serve.py gives it.
    f'os.environ["NLTK_DATA"] = {os.environ["NLTK_DATA"]!r}\n'
    'os.execv(sys.executable, [sys.executable, "-u", "client.py"])\n'
)
PY
cd "$work"
"$env_prefix/bin/python" -u serve.py
