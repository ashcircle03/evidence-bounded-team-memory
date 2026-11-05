"""Explicit, idempotent local dispatch for the design audit; no login-node compute."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shlex
import subprocess

WORK = Path(__file__).resolve().parents[3]
CAMPAIGN = WORK/'campaigns/speakermem-dev'
LEDGER = CAMPAIGN/'campaign-dispatch.json'
REMOTE = '/ceph_data/pjw031003/capstone-shared-knowledge'
REMOTE_LEDGER = REMOTE+'/campaigns/speakermem-dev/campaign-dispatch.json'
HOST = 'pjw031003@aurora.khu.ac.kr'
SSH = ['ssh','-p','30080','-o','BatchMode=yes','-o','ConnectTimeout=15','-o','ControlPath=/private/tmp/team-memory-30080.sock',HOST]
SCP = ['scp','-P','30080','-o','BatchMode=yes','-o','ControlPath=/private/tmp/team-memory-30080.sock']

def call(args):
    return subprocess.check_output(args,text=True).strip()

def ssh(command):return call(SSH+[command])
def now():return datetime.now(timezone.utc).isoformat()
def save(data):
    tmp=LEDGER.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');tmp.replace(LEDGER)
def mirror():subprocess.run(SCP+[str(LEDGER),HOST+':'+REMOTE_LEDGER],check=True)

def submit(version,gpus,minutes,files):
    lock=CAMPAIGN/'design-review.dispatch.lock'
    with lock.open('x') as f:f.write(version)
    try:
        data=json.loads(LEDGER.read_text())
        if version in data['jobs']:raise RuntimeError('Version already has a dispatch entry; reconcile before retry')
        queue=ssh('squeue -r -h -u pjw031003 -o "%i|%T|%b"')
        print('queue',queue or '(empty)',flush=True)
        running=sum('RUNNING' in line for line in queue.splitlines())
        if running>=4 or len(queue.splitlines())>=8:raise RuntimeError('User queue limit reached')
        # Read server dispatch before any write; require all known job IDs to match.
        other=json.loads(ssh('cat '+REMOTE_LEDGER))
        assert other['project']==data['project']
        for v,j in other.get('jobs',{}).items():
            if v not in data['jobs'] or data['jobs'][v].get('job_id')!=j.get('job_id'):
                raise RuntimeError('Server dispatch diverged: '+v)
        open_jobs=[j for j in data['jobs'].values() if j.get('state') not in ('COMPLETED','FAILED','TIMEOUT','OUT_OF_MEMORY','CANCELLED')]
        if any(j.get('submission_intent')!='submitted' for j in open_jobs):raise RuntimeError('Unresolved submission intent')
        if gpus+sum(j['gpus'] for j in open_jobs)>4:raise RuntimeError('GPU concurrency cap')
        spent=sum(j.get('elapsed_seconds',j['wall_minutes']*60)*j['gpus'] for j in data['jobs'].values())
        if spent+60*minutes*gpus>60*data['budget']['single_gpu_minutes']:raise RuntimeError('GPU budget exceeded')
        src=CAMPAIGN/'source'/version
        for name in files:assert (src/name).is_file()
        hashes={name:sha256((src/name).read_bytes()).hexdigest() for name in files}
        dest=REMOTE+'/source/sm-'+version
        row=dict(source_version=version,source_sha256=hashes,submission_intent='prepared',job_id=None,
                 gpus=gpus,cpus=8 if gpus<2 else 16,ram_gb=16 if gpus==0 else 48*gpus,
                 wall_minutes=minutes,partition='batch_ugrad',account='ugrad',source_path=dest,state='PREPARED')
        data['jobs'][version]=row;save(data)
        ssh('mkdir -p '+shlex.quote(dest)+' '+REMOTE+'/logs '+REMOTE+'/results')
        subprocess.run(SCP+[str(src/name) for name in files]+[HOST+':'+dest+'/'],check=True)
        row['submission_intent']='submitting';save(data);mirror()
        reply=ssh('sbatch --parsable '+shlex.quote(dest+'/run.sbatch'))
        job=reply.split(';')[0]
        if not job.isdigit():raise RuntimeError('Ambiguous sbatch reply: '+reply)
        row.update(job_id=job,submission_intent='submitted',state='SUBMITTED',submitted_at=now(),
                   result_path=REMOTE+'/results/sm-'+job+'.json',log_path=REMOTE+'/logs/sm-'+job+'.log')
        save(data) # Preserve actual ID before mirror can fail.
        mirror();print('submitted',version,job,flush=True)
    finally:lock.unlink()

def status(version):
    data=json.loads(LEDGER.read_text());row=data['jobs'][version];job=row['job_id'];assert job
    print(ssh('squeue -r -u pjw031003 -o "%.24i %.12T %.12M %.12l %R"'))
    fields='JobID,State,ExitCode,Elapsed,ElapsedRaw,AllocCPUS,ReqMem,MaxRSS,TotalCPU,AllocTRES,NodeList'
    raw=ssh('sacct -n -P -j '+job+' --format='+fields)
    usage=[dict(zip(fields.split(','),x.split('|'))) for x in raw.splitlines() if x]
    head=next(x for x in usage if x['JobID']==job)
    row.update(state=head['State'],exit_code=head['ExitCode'],elapsed_seconds=int(head['ElapsedRaw']),usage=usage)
    data['checked_at']=now();save(data)
    if head['State']=='COMPLETED' and head['ExitCode']=='0:0':
        dest=CAMPAIGN/'results';dest.mkdir(exist_ok=True)
        subprocess.run(SCP+[HOST+':'+row['result_path'],str(dest/f'sm-{job}.json')],check=True)
        result=json.loads((dest/f'sm-{job}.json').read_text())
        assert result['status']=='complete' and str(result['job_id'])==job
        row['verified']=True;save(data)
    mirror();print(json.dumps(head))

if __name__=='__main__':
    import sys
    if sys.argv[1]=='submit':submit(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),sys.argv[5:])
    else:status(sys.argv[2])
