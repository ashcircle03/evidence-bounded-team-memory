"""Freeze an original CoMRAT pilot; labels never enter the actor packet."""
import csv
from datetime import datetime, timezone
from hashlib import sha256
import io
import json
from pathlib import Path
import shutil
import zipfile


def main():
    repo = Path(__file__).resolve().parents[2]
    version = 'cup-comrat-original-v1'
    folder = repo.parent/'campaigns/speakermem-dev/source'/version
    report = repo/'results/rationale-reuse/comrat-v1'
    folder.mkdir(exist_ok=False)
    report.mkdir(parents=True, exist_ok=False)
    archive = Path('/private/tmp/team-memory-rationale-research/comrat.zip')
    assert sha256(archive.read_bytes()).hexdigest() == 'e50e3f67938f00bb7aafd81804f671b407b6a78f02f821449ad887894ae30e4f'
    inputs, keys = [], []
    with zipfile.ZipFile(archive) as z:
        name = next(n for n in z.namelist() if n.endswith('(Labelling task).csv'))
        for row in csv.DictReader(io.StringIO(z.read(name).decode()), delimiter=';'):
            if row['Predicted_D'] not in ('0', '1'): continue
            key = f'published-{len(inputs)+1:02d}'
            inputs.append(dict(id=key, group='published_prediction_replay', text=row['Commit message sentence']))
            keys.append(dict(id=key, published_decision=int(row['Predicted_D']),
                             published_rationale=int(row['Predicted_R']),
                             human_decisions=[int(row[f'Decision {i}']) for i in range(1,6)],
                             human_rationales=[int(row[f'Rationale {i}']) for i in range(1,6)]))
    old = json.loads((repo/'evaluation/service_completion/inputs.json').read_text())
    for scenario in old['streams']+old['transfer']:
        for side, records in [('old',scenario['initial']), ('new',[scenario['incoming']])]:
            for i, record in enumerate(records):
                key = f"{scenario['id']}/{side}/{i}"
                inputs.append(dict(id=key, group='known_team_transfer', text=record['source']['text']))
                if side == 'old':
                    keys.append(dict(id=key, reasoned_decision=scenario['id'].startswith(('writer-', 'cache-')),
                                     note='Task-level routing diagnostic, not the upstream definition of every Decision label.'))
    protocol = '''# Original CoMRAT pilot (frozen before model outputs)

Execute the released pages/commit.py:user_commit_page, helpers.preprocess,
helpers.load_models, Tokenizer fitting on released data, padding and >0.5
threshold unchanged. Only Streamlit input/output is replaced by headless calls;
weights are cached between documents. All token IDs/probabilities and output rows
are retained. No QA/review/service code import or modification. No new training,
threshold sweep, or Qwen prompt. Published example labels stay local for scoring.

1. Replay all 12 published predictions in the user-study CSV. Match the first
   row (the original already-preprocessed sentence is presented as a title).
   Retain any additional empty-body rows; report them as preprocessing artifacts.
   This is execution fidelity, NOT held-out accuracy. Compare human-vote labels
   separately and do not call the author's predicted labels ground truth.
2. Run the 22 complete raw old/new documents from our 11 known scenarios with
   upstream preprocessing. For the 11 old documents, assess whether both
   Decision and Rationale are detected (possibly in separate nonempty rows):
   4 reasoned decision records, 7 factual measurement/configuration records.
   Empty strings cannot provide evidence. Errors are failures, not negatives.
   This narrow authored diagnostic is NOT a natural benchmark; writer/cache
   source texts repeat across positive/negative reports.
3. Keep every source string and inspect whether preprocessing strips source
   context. A sentence label does not pair decisions with reasons or establish
   changed conditions, conflict, approval or reconsideration.

Candidate routing gate: published labels 24/24 reproduced, all 4 reasoned old
records detected, zero of 7 fact-only old records routed as reasoned decisions.
Even passing is only permission for a separate pair-level experiment, not adoption
in default service. If failed, do not prompt-tune the gate or rerun full QA.

GPU1 reserved; conda Python3.11; Slurm12h. Original TensorFlow2.13 dependencies.
Record whether TensorFlow actually uses GPU or CPU; allocation is not evidence of
GPU inference. Original requirements installed in an isolated environment only.
No paid API or GitHub credentials. Download/extract dataset/models on compute-node
/local_datasets and verify archive SHA256; no login-node computation.
'''
    (folder/'inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
    (folder/'PROTOCOL.md').write_text(protocol)
    shutil.copyfile(repo/'evaluation/service_completion/comrat_original.py',folder/'run.py')
    project='/ceph_data/pjw031003/capstone-shared-knowledge'
    remote=project+'/source/sm-'+version
    config=dict(source_version=version,project=project,sha256={n:sha256((folder/n).read_bytes()).hexdigest()
                                                           for n in ['inputs.json','PROTOCOL.md','run.py']})
    (folder/'config.json').write_text(json.dumps(config,indent=2)+'\n')
    script=f'''#!/usr/bin/env bash
#SBATCH --job-name=capsm-{version}
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
#SBATCH --chdir={project}
#SBATCH --output={project}/logs/sm-%j.log
set -euo pipefail
source /ceph_data/pjw031003/anaconda3/etc/profile.d/conda.sh
conda activate {project}/runtime/cupmem-qwen3-v1
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
conda create -y -p "$RATIONALE_ROOT/env" python=3.11 pip > "{project}/logs/sm-$SLURM_JOB_ID-setup.log" 2>&1
conda activate "$RATIONALE_ROOT/env"
export MPLCONFIGDIR="$RATIONALE_ROOT/mpl" PIP_CACHE_DIR="$RATIONALE_ROOT/pip-cache"
python -m pip install -r "$RATIONALE_ROOT/replication_package/Rationale-Analyses-Tool/requirements.txt" >> "{project}/logs/sm-$SLURM_JOB_ID-setup.log" 2>&1
python -m pip freeze > "{project}/results/sm-$SLURM_JOB_ID-environment.txt"
python -u {remote}/run.py {remote} "$RATIONALE_ROOT/replication_package/Rationale-Analyses-Tool"
'''
    (folder/'run.sbatch').write_text(script)
    (report/'keys.json').write_text(json.dumps(keys,indent=2)+'\n')
    shutil.copytree(folder,report/'runtime')
    frozen=dict(created_at=datetime.now(timezone.utc).isoformat(),files={p.name:sha256(p.read_bytes()).hexdigest()
                   for p in folder.iterdir()},archive_sha256=sha256(archive.read_bytes()).hexdigest(),
                   keys_sha256=sha256((report/'keys.json').read_bytes()).hexdigest(),
                   service_sha256={str(p.relative_to(repo)):sha256(p.read_bytes()).hexdigest()
                                   for p in sorted((repo/'team_memory').glob('*.py'))})
    (report/'freeze.json').write_text(json.dumps(frozen,indent=2)+'\n')
    (report.parent/'progress.json').write_text(json.dumps(dict(status='frozen_not_submitted',version=version),indent=2)+'\n')
    print(folder, len(inputs), 'documents')


if __name__=='__main__': main()
