"""Export a new topic from pinned public data, inside a CPU allocation only."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

job = os.environ['SLURM_JOB_ID']
src = Path(__file__).parent
manifest = json.loads((src / 'manifest.json').read_text())['datasets'][0]
root = Path('/local_datasets/pjw031003/capstone-shared-knowledge/datasets-v1/EverMemBench-Dynamic')
root.mkdir(parents=True, exist_ok=True)
data = {}
for spec in manifest['files']:
    if not spec['path'].startswith('02/'):
        continue
    target = root / spec['path']
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        url = 'https://huggingface.co/datasets/{}/resolve/{}/{}'.format(manifest['repo'], manifest['revision'], spec['path'])
        tmp = target.with_suffix('.download-' + job)
        subprocess.run(['curl', '-fLsS', '--connect-timeout', '15', '--max-time', '90', '--retry', '1', '-o', str(tmp), url], check=True)
        tmp.replace(target)
    blob = target.read_bytes()
    assert len(blob) == spec['bytes']
    assert hashlib.sha1(('blob %d\0' % len(blob)).encode() + blob).hexdigest() == spec['git_blob_sha1']
    data[spec['path']] = json.loads(blob)
result = dict(status='complete', job_id=job, revision=manifest['revision'], data=data)
out = Path('/ceph_data/pjw031003/capstone-shared-knowledge/results') / ('sm-' + job + '.json')
out.write_text(json.dumps(result, ensure_ascii=False))
print(json.dumps(dict(status='complete', job_id=job, files=list(data))))
