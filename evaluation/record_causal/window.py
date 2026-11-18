"""One-factor source-window diagnostic. No gold, scorer, or semantic repair."""
import json
from pathlib import Path
from hashlib import sha256
import os
import time

from team_memory.records import bound


def segments(source):
    return [dict(id=0, start=0, end=len(source['text']), text=source['text'])]


def prompt(source):
    # Unchanged instruction/examples. Only SOURCE.segments is replaced.
    original = bound.prompt(source)
    prefix, payload = original.rsplit('\nSOURCE:\n', 1)
    data = json.loads(payload)
    data['segments'] = segments(source)
    return prefix + '\nSOURCE:\n' + json.dumps(data, ensure_ascii=False)


def request(source):
    return dict(model='Qwen3-8B', messages=[dict(role='system', content=bound.SYSTEM), dict(role='user', content=prompt(source))],
                temperature=0, max_tokens=2048, chat_template_kwargs=dict(enable_thinking=False), seed=42,
                guided_json=bound.schema(1))


def alignment_audit(source, raw):
    """Same upstream exact aligner, now within the entire original document."""
    accepted = []; rejected = []
    try:
        parsed = json.loads(raw)
        import jsonschema
        jsonschema.validate(parsed, bound.schema(1))
        for i, record in enumerate(parsed['records']):
            for role in ('root', 'details', 'condition', 'basis', 'time', 'subject'):
                items = [record[role]] if role == 'root' else record[role]
                for j, item in enumerate(items):
                    path = f'records[{i}].{role}[{j}]'
                    try:
                        accepted.append(dict(path=path, **bound.align(source, item, segments(source))))
                    except Exception as exc:
                        rejected.append(dict(path=path, reason=f'{type(exc).__name__}: {exc}'))
    except Exception as exc:
        rejected.append(dict(path='root', reason=f'{type(exc).__name__}: {exc}'))
    return dict(accepted=accepted, rejected=rejected)


def main(folder):
    import httpx
    cfg = json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURMD_NODENAME') and os.environ.get('CONDA_PREFIX') == cfg['conda_prefix']
    for table, base in [('code_sha256',folder/'code'),('data_sha256',folder)]:
        for name, h in cfg[table].items():
            assert sha256((base/name).read_bytes()).hexdigest() == h, name
    job = os.environ['SLURM_JOB_ID']
    out = Path(cfg['project'])/'results'/f'record-window-{job}.json'
    assert not out.exists()
    result = dict(status='running',job_id=job,model_revision=cfg['model_revision'],code_sha256=cfg['code_sha256'],
                  data_sha256=cfg['data_sha256'],calls=0,rows=[],external_model_api_calls=0)
    start = time.monotonic()
    def save():
        result['seconds'] = time.monotonic()-start
        tmp = out.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2));tmp.replace(out)
    try:
        with httpx.Client(trust_env=False,timeout=240) as client,out.with_suffix('.calls.jsonl').open('x') as trace:
            for item in json.loads((folder/'inputs.json').read_text())['items']:
                body = request(item['source']);assert result['calls'] < cfg['max_calls'];result['calls'] += 1
                response = client.post(os.environ['PRACTICAL_MODEL_URL']+'/chat/completions',json=body)
                response.raise_for_status();data=response.json()
                trace.write(json.dumps(dict(id=result['calls'],item_id=item['id'],request=body,response=data),ensure_ascii=False)+'\n');trace.flush()
                raw=data['choices'][0]['message']['content']
                result['rows'].append(dict(id=item['id'],source=item['source'],raw=raw,alignment=alignment_audit(item['source'],raw)))
                save();print('ROW',result['calls'],item['id'],flush=True)
        assert result['calls'] == 68
        result['status'] = 'complete'
    except BaseException as exc:
        result.update(status='failed',error=f'{type(exc).__name__}: {exc}');raise
    finally:
        save()


if __name__ == '__main__':
    import sys
    main(Path(sys.argv[1]))
