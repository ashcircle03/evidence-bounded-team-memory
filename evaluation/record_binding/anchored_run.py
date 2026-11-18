"""One fixed Qwen context-edge pass; no gold, training, retries or new claims."""
import json
import os
from pathlib import Path
from hashlib import sha256
import time

from team_memory.records.anchored_binding import request


def main(folder):
    import httpx
    cfg = json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURMD_NODENAME') and os.environ.get('CONDA_PREFIX') == cfg['conda_prefix']
    for table, base in [('code_sha256', folder/'code'), ('data_sha256', folder)]:
        for name, h in cfg[table].items():
            assert sha256((base/name).read_bytes()).hexdigest() == h, name
    job = os.environ['SLURM_JOB_ID']
    out = Path(cfg['project'])/'results'/f'record-anchored-{job}.json'
    assert not out.exists()
    result = dict(status='running', job_id=job, model_revision=cfg['model_revision'],
                  code_sha256=cfg['code_sha256'], data_sha256=cfg['data_sha256'],
                  calls=0, rows=[], external_model_api_calls=0, training_steps=0)
    start = time.monotonic()
    def save():
        result['seconds'] = time.monotonic()-start
        tmp = out.with_suffix('.tmp'); tmp.write_text(json.dumps(result, ensure_ascii=False, indent=2)); tmp.replace(out)
    try:
        with httpx.Client(trust_env=False, timeout=240) as client, out.with_suffix('.calls.jsonl').open('x') as trace:
            for item in json.loads((folder/'inputs.json').read_text()):
                body = request(item['source'], item['original_raw'])
                assert result['calls'] < cfg['max_calls']; result['calls'] += 1
                response = client.post(os.environ['PRACTICAL_MODEL_URL']+'/chat/completions', json=body)
                response.raise_for_status(); data = response.json()
                trace.write(json.dumps(dict(id=result['calls'], item_id=item['id'], request=body, response=data), ensure_ascii=False)+'\n'); trace.flush()
                result['rows'].append(dict(id=item['id'], source=item['source'], raw=data['choices'][0]['message']['content'],
                                           finish_reason=data['choices'][0]['finish_reason'], usage=data.get('usage')))
                save(); print('ROW', result['calls'], item['id'], flush=True)
        assert result['calls'] == 68
        result['status'] = 'complete'
    except BaseException as exc:
        result.update(status='failed', error=f'{type(exc).__name__}: {exc}'); raise
    finally:
        save()


if __name__ == '__main__':
    import sys
    main(Path(sys.argv[1]))
