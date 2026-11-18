"""Run prebuilt paired requests against the campaign's compute-node localhost vLLM server."""
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit
import httpx


def main(request_path, output_path):
    url=os.environ['PRACTICAL_MODEL_URL']
    if urlsplit(url).hostname != '127.0.0.1' or not os.environ.get('SLURM_JOB_ID') or not os.environ.get('CONDA_PREFIX'):
        raise RuntimeError('Expected local compute-node service inside the campaign conda environment')
    jobs=json.loads(Path(request_path).read_text())
    if not jobs:raise ValueError('Empty question set')
    traces=[]
    with Path(output_path).open('x') as f, httpx.Client(trust_env=False,timeout=240) as client:
        for job in jobs:
            response=client.post(url+'/chat/completions',json=job['body'])
            response.raise_for_status()
            traces.append(dict(qid=job['qid'],arm=job['arm'],response=response.json()))
        json.dump(traces,f,ensure_ascii=False)

if __name__=='__main__':
    main(*sys.argv[1:])
