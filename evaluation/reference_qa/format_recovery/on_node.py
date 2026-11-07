"""Execute frozen fusion requests. Export native reference messages for offline review."""
from hashlib import sha256
import json
import os
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener


def main():
    folder = Path(__file__).resolve().parent
    cfg = json.loads((folder/'config.json').read_text())
    job = os.environ['SLURM_JOB_ID']
    assert os.environ['SLURMD_NODENAME'] and os.environ['CONDA_PREFIX']==cfg['conda_prefix']
    for name,expected in cfg['input_hashes'].items():
        assert sha256((folder/name).read_bytes()).hexdigest()==expected, name
    requests = json.loads((folder/'requests.json').read_text())
    assert len(requests)==cfg['expected_fusion_calls']
    endpoint = os.environ['PRACTICAL_MODEL_URL']
    assert endpoint.startswith('http://127.0.0.1:') and endpoint.endswith('/v1')
    http = build_opener(ProxyHandler({}))
    calls = []
    path = Path(cfg['project'])/'results'/('format-'+job+'.json')
    result = dict(status='running',job_id=job,calls=calls,source_version=cfg['source_version'],
                  input_hashes=cfg['input_hashes'],model=cfg['model_revision'],external_model_api_calls=0)
    def save():
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2))
        tmp.replace(path)
    save()
    for item in requests:
        body=item['body']
        assert body['model']=='Qwen3-8B' and body['temperature']==0 and body['max_tokens']==1024
        req=Request(endpoint+'/chat/completions',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
        with http.open(req,timeout=120) as response:
            calls.append(dict(id=item['id'],key=item['key'],request=body,response=json.load(response),http_status=response.status))
        save()
    # Evaluator-only export, after all model calls. No R labels enter a prompt.
    groups=json.loads((folder/'reference-locations.json').read_text())
    locations={loc for g in groups for loc in g['gold_reference_locations']}
    selected={}
    dataset=Path('/local_datasets/pjw031003/capstone-shared-knowledge/datasets-v1/EverMemBench-Dynamic')
    for topic in ('01','02'):
        for day in json.loads((dataset/topic/'dialogue.json').read_text()):
            for group,messages in day['dialogues'].items():
                for i,m in enumerate(messages or [],1):
                    loc=f"EverMemBench-Dynamic@{cfg['ever_revision']}/{topic}/{day['date']}/{group}/{i}"
                    if loc in locations:selected[loc]=m
    assert set(selected)==locations
    result.update(status='complete',native_references=selected)
    save()


if __name__=='__main__':main()
