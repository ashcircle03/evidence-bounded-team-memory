"""Preserve final job evidence without converting execution failures to success."""
import argparse
import gzip
from hashlib import sha256
import json
from pathlib import Path
import shutil
import zlib

from .cards import build
from .prepare import write
from .verify import verify

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
CAMPAIGN=ROOT.parent/'campaigns/speakermem-dev'


def archive(version,inputs_path,key_path):
    ledger=json.loads((CAMPAIGN/'campaign-dispatch.json').read_text())
    job=ledger['jobs'][version];jid=job['job_id']
    assert job['state'] in ('COMPLETED','FAILED','TIMEOUT','OUT_OF_MEMORY','CANCELLED')
    out=ROOT/'results/cupmem/practical'/version.removeprefix('cup-practical-')
    out.mkdir(exist_ok=True)
    base=CAMPAIGN/'results';stem='cup-practical-'+jid
    raw=(base/(stem+'.json')).read_bytes()
    calls_raw=(base/(stem+'.calls.jsonl')).read_bytes()
    result=json.loads(raw);calls=[json.loads(s) for s in calls_raw.splitlines()]
    freeze=json.loads((HERE/(version+'-freeze.json')).read_text())
    assert sha256(inputs_path.read_bytes()).hexdigest()==freeze['input_sha256']
    assert result['input_sha256']==freeze['input_sha256']
    assert result['code_sha256']==freeze['code_sha256']
    inputs=json.loads(inputs_path.read_text());key=json.loads(key_path.read_text())
    write(out/'verification.json',verify(result,calls,inputs,freeze))
    write(out/'cards.json',build(inputs,key,result,calls))
    write(out/'accounting.json',job)
    for name,blob in [('run.json.gz',raw),('calls.jsonl.gz',calls_raw)]:
        (out/name).write_bytes(gzip.compress(blob,mtime=0))
    native=base/(stem+'.native.jsonl.gz')
    if native.exists():
        shutil.copyfile(native,out/'native.jsonl.gz')
        try:
            expanded=gzip.decompress(native.read_bytes())
            native_capture=dict(gzip_complete=True,expanded_bytes=len(expanded))
        except EOFError:
            decoder=zlib.decompressobj(31)
            expanded=decoder.decompress(native.read_bytes())
            native_capture=dict(gzip_complete=False,recoverable_prefix_bytes=len(expanded),
                note='Original interrupted gzip retained byte-for-byte. Prefix is not a complete native trace; physical call JSONL and Slurm cost are separately preserved.')
        write(out/'native-capture.json',native_capture)
    supervisor=base/('sm-'+jid+'.json')
    if supervisor.exists():shutil.copyfile(supervisor,out/'supervisor.json')
    write(out/'artifact-manifest.json',dict(job_id=jid,source_version=version,
        slurm_state=job['state'],exit_code=job['exit_code'],program_status=result['status'],
        slurm_and_program_complete=job['state']=='COMPLETED' and job['exit_code']=='0:0' and result['status']=='complete',
        actual_input_sha256=freeze['input_sha256'],expected_input=str(inputs_path.relative_to(ROOT)),
        physical_calls_logged=len(calls),last_snapshot_call_count=result.get('calls'),
        interrupted_capture_may_be_incomplete=result['status']!='complete',
        files_sha256={p.name:sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name!='artifact-manifest.json'}))
    return dict(job=jid,slurm=job['state'],program=result['status'],calls=len(calls),output=str(out))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('version');p.add_argument('inputs',type=Path);p.add_argument('key',type=Path)
    a=p.parse_args();print(json.dumps(archive(a.version,a.inputs.resolve(),a.key.resolve())))
