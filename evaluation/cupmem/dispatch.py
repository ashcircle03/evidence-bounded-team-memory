"""Apply the CUPMem goal's additional budget before the existing idempotent dispatcher."""
import json
from pathlib import Path
import re
import sys
from evaluation.timeline.dispatch import LEDGER, submit, status


def validate_submission(script, gpus):
    if gpus < 1:
        raise RuntimeError('User policy: every new compute allocation must request at least one GPU')
    directives=[line.strip() for line in script.splitlines() if line.lstrip().startswith('#SBATCH')]
    if not any(re.fullmatch(r'#SBATCH\s+--gres=gpu:'+str(gpus),line) for line in directives):
        raise RuntimeError('GPU count in sbatch must match the dispatch reservation')
    if any('--nodelist' in line or re.search(r'\s-w(?:\s|=)',line) for line in directives):
        raise RuntimeError('Do not pin a compute node')
    if not any('--no-requeue' in line for line in directives):
        raise RuntimeError('Explicit --no-requeue required')
    if not re.search(r'^\s*conda activate\s+\S+',script,re.M):
        raise RuntimeError('Explicit conda activation required before execution')


def dispatch(version, gpus, minutes, files):
    assert version.startswith('cup-')
    script=LEDGER.parent/'source'/version/'run.sbatch'
    validate_submission(script.read_text(),gpus)
    data=json.loads(LEDGER.read_text())
    goal=data['goal_budgets']['cupmem']
    terminal={'COMPLETED','FAILED','TIMEOUT','OUT_OF_MEMORY','CANCELLED'}
    used=sum((j.get('elapsed_seconds',0) if j.get('state') in terminal else j['wall_minutes']*60)
             for v,j in data['jobs'].items() if v.startswith('cup-') and j['gpus']==0)
    if gpus==0 and used+minutes*60>goal['cpu_minutes']*60:
        raise RuntimeError('CUPMem CPU goal budget exceeded, including failed attempts')
    gpu_used=sum((j.get('elapsed_seconds',0) if j.get('state') in terminal else j['wall_minutes']*60)*j['gpus']
                 for v,j in data['jobs'].items() if v.startswith('cup-'))
    if gpu_used+gpus*minutes*60>goal['gpu_minutes']*60:
        raise RuntimeError('CUPMem GPU goal budget exceeded, including failed attempts')
    submit(version,gpus,minutes,files)


if __name__=='__main__':
    if sys.argv[1]=='submit':dispatch(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),sys.argv[5:])
    else:status(sys.argv[2])
