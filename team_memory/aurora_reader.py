"""Compute-node transport; independent of UI and the model-facing core."""
import json
import re
import shlex
import subprocess
import time
from datetime import datetime, timezone

class RemoteReader:
    def __init__(self, job, store):
        if not re.fullmatch(r'\d+',job):raise ValueError('numeric Slurm job ID required')
        self.job=job;self.store=store

    def __call__(self, system, content):
        project='/ceph_data/pjw031003/capstone-shared-knowledge'
        shell=('source /ceph_data/pjw031003/anaconda3/etc/profile.d/conda.sh; '
               'conda activate '+project+'/runtime/cupmem-qwen3-v1; '
               'python '+project+'/source/sm-cup-workbench-v1/rpc.py')
        command='srun --jobid='+self.job+' --overlap --nodes=1 --ntasks=1 --cpus-per-task=1 bash -c '+shlex.quote(shell)
        payload=dict(messages=[dict(role='system',content=system),dict(role='user',content=content)],
                     max_tokens=900)
        start=time.monotonic()
        result=subprocess.run(['ssh','-p','30080','-o','BatchMode=yes','-o','ConnectTimeout=8',
            '-o','ControlPath=/private/tmp/team-memory-30080.sock','pjw031003@aurora.khu.ac.kr',command],
            input=json.dumps(payload,ensure_ascii=False),text=True,capture_output=True,timeout=180)
        if result.returncode:
            raise RuntimeError('모델 연결에 실패했습니다. GPU 작업 종료 또는 SSH 상태를 확인하세요. '+result.stderr[-600:])
        response=json.loads(result.stdout)
        if 'error' in response:raise RuntimeError(str(response['error']))
        raw=response['choices'][0]['message']['content']
        self.store.put('workbench_calls',dict(system=system,content=content,raw=raw,
            usage=response.get('usage'),seconds=time.monotonic()-start,
            at=datetime.now(timezone.utc).isoformat(),job_id=self.job,model=response.get('model')))
        return raw

