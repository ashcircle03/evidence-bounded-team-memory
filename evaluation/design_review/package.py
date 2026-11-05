from hashlib import sha256
import json
from pathlib import Path
import zipfile
from .build import ROOT,HERE,write

WORK=ROOT.parent
CAMPAIGN=WORK/'campaigns/speakermem-dev'

def package(version,large=False,qa=False):
 path=CAMPAIGN/'source'/version;path.mkdir()
 if qa:
  for name in ['infer.py','packets.json']:(path/name).write_bytes((CAMPAIGN/'source/records-read-v31'/name).read_bytes())
 else:
  with zipfile.ZipFile(path/'infer.py','w',zipfile.ZIP_DEFLATED) as z:
   for p in (ROOT/'team_memory').glob('*.py'):z.write(p,'team_memory/'+p.name)
   z.write(HERE/'runner.py','__main__.py');z.write(HERE/'direct.py','direct.py')
  rows=json.loads((HERE/'inputs.json').read_text());oracle=json.loads((HERE/'oracle-windows.json').read_text())
  if large:rows=[r for r in rows if r['id'] in oracle]
  write(path/'packets.json',dict(rows=rows,oracle=oracle))
 checksum=sha256((path/'packets.json').read_bytes()).hexdigest()
 gpus=2 if large else 1;minutes=8 if qa else 20
 model='/local_datasets/pjw031003/capstone-shared-knowledge/models/Qwen2.5-14B-Instruct' if large else '$PWD/runtime/speakermem-v1/models/qwen'
 tail=' --count 136 --max-new-tokens 192' if qa else ' --large' if large else ''
 (path/'run.sbatch').write_text(f'''#!/usr/bin/env bash
#SBATCH --job-name=capsm-{version}
#SBATCH --partition=batch_ugrad
#SBATCH --account=ugrad
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={8*gpus}
#SBATCH --mem={48*gpus}G
#SBATCH --gres=gpu:{gpus}
#SBATCH --time=00:{minutes:02d}:00
#SBATCH --no-requeue
#SBATCH --chdir=/ceph_data/pjw031003/capstone-shared-knowledge
#SBATCH --output=/ceph_data/pjw031003/capstone-shared-knowledge/logs/sm-%j.log
set -euo pipefail
src="$PWD/source/sm-{version}"
stage=$(mktemp -d /tmp/capstone-design-XXXXXXXX)
trap 'rm -rf -- "$stage"' EXIT
data=/local_datasets/pjw031003/capstone-shared-knowledge/{version}
mkdir -p "$data"
cp "$src/packets.json" "$data/packets.$SLURM_JOB_ID.json"
printf '%s  %s\\n' {checksum} "$data/packets.$SLURM_JOB_ID.json" | sha256sum -c -
tar -xf "$PWD/results/system-119216/site.tar" -C "$stage" & pack=$!
mkdir "$stage/model"
cp {model}/*.json {model}/*.txt "$stage/model/" & meta=$!
weights=()
for f in {model}/*.safetensors; do cp "$f" "$stage/model/" & weights+=("$!"); done
wait "$pack"; wait "$meta"
for pid in "${{weights[@]}}"; do wait "$pid"; done
export PYTHONPATH="$stage:$stage/site-packages" PYTHONDONTWRITEBYTECODE=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 OMP_NUM_THREADS={8*gpus}
"$PWD/runtime/speakermem-v1/venv/bin/python" -u "$src/infer.py" "$data/packets.$SLURM_JOB_ID.json" "$stage/model" "$PWD/results/sm-$SLURM_JOB_ID.json" "$SLURM_JOB_ID"{tail}
''')

if __name__=='__main__':
 package('design-small-v1');package('design-large-v1',large=True);package('design-qa-v1',qa=True)
