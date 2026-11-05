"""Freeze exact executable sources and explicit data for one versioned allocation."""
import json
from pathlib import Path
from hashlib import sha256
import sys
import zipfile
from .build import ROOT,HERE


def package(version, inputs, minutes):
    dst=ROOT.parent/'campaigns/speakermem-dev/source'/version;dst.mkdir(exist_ok=False)
    blob=json.dumps(dict(streams=inputs),ensure_ascii=False).encode()
    (dst/'packets.json').write_bytes(blob)
    with zipfile.ZipFile(dst/'infer.py','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted((ROOT/'team_memory').glob('*.py')):z.write(p,'team_memory/'+p.name)
        z.write(HERE/'runner.py','__main__.py')
        z.write(ROOT/'evaluation/design_review/runner.py','runtime.py')
        z.write(ROOT/'evaluation/design_review/direct.py','direct.py')
    base=(ROOT.parent/'campaigns/speakermem-dev/source/design-large-factorial-v1/run.sbatch').read_text()
    base=base.replace('design-large-factorial-v1',version).replace('00:40:00',f'00:{minutes:02}:00')
    base=base.replace('9cfb7aec6eef719aff42ac5e812a4995174846999a7c2810cc9bc3783c19a58e',sha256(blob).hexdigest())
    base=base.replace(' --large','')
    (dst/'run.sbatch').write_text(base)
    print(dst)


if __name__=='__main__':
    package(sys.argv[1],json.loads(Path(sys.argv[2]).read_text()),int(sys.argv[3]))
