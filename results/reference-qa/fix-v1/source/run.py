"""Twenty existing QA requests, original histories, local Qwen; no answer key input."""
from hashlib import sha256
from importlib.metadata import version
import json
import os
from pathlib import Path
import sys
import time


def main():
    folder = Path(sys.argv[1])
    cfg = json.loads((folder/'config.json').read_text())
    job = os.environ['SLURM_JOB_ID']
    assert os.environ['CONDA_PREFIX'] == cfg['conda_prefix']
    assert os.environ['SLURMD_NODENAME']
    sys.path.insert(0, str(folder/'code'))
    import httpx
    from team_memory.reference_qa import ReferenceQA, local_components
    from team_memory.store import digest, source_envelope

    for name, expected in cfg['code_sha256'].items():
        assert sha256((folder/'code'/name).read_bytes()).hexdigest() == expected
    blob = (folder/'inputs.json').read_bytes()
    assert sha256(blob).hexdigest() == cfg['input_sha256']
    inputs = json.loads(blob)
    assert sum(e['operation']=='ask' for c in inputs['cases'] for e in c['events']) == 20
    output = Path(cfg['project'])/'results'/f'cup-reference-{job}.json'
    local = Path('/local_datasets/pjw031003/capstone-shared-knowledge/reference')/job
    local.mkdir(parents=True, exist_ok=False)
    (local/'inputs.json').write_bytes(blob)
    calls = output.with_suffix('.calls.jsonl').open('x')
    context, active = {}, {}
    began = time.monotonic()
    record = dict(status='running', job_id=job, input_sha256=cfg['input_sha256'],
        code_sha256=cfg['code_sha256'], source_version=cfg['source_version'],
        model='Qwen3-8B', profile=cfg.get('profile', 'standard'), external_model_api_calls=0, rows=[], calls=0,
        libraries={p:version(p) for p in ('llama-index-core','llama-index-llms-openai-like',
                                        'llama-index-embeddings-huggingface','transformers') +
                   (('llama-index-retrievers-bm25','bm25s','PyStemmer') if cfg.get('profile')=='team' else ())},
        scope='Exposed legacy development QA; upstream CitationQueryEngine, not a held-out benchmark')

    def save():
        record['seconds'] = time.monotonic()-began
        tmp = output.with_suffix('.tmp')
        tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2)); tmp.replace(output)

    def request_hook(request):
        if not request.url.path.endswith('/chat/completions'):
            return
        if record['calls'] >= cfg['max_calls'] or time.monotonic()-began > cfg['client_seconds']-100:
            raise RuntimeError('Diagnostic call/time cap reached')
        body = json.loads(request.content)
        n = len(parts['tokenizer'].apply_chat_template(body['messages'], tokenize=True,
            add_generation_prompt=True, enable_thinking=False))
        active.clear(); active.update(id=record['calls'], context=dict(context), request=body,
                                      rendered_prompt_tokens=n, started=time.monotonic())
        record['calls'] += 1

    def response_hook(response):
        response.read()
        if active:
            row = dict(active, seconds=time.monotonic()-active['started'],
                       response=response.json(), http_status=response.status_code)
            calls.write(json.dumps(row, ensure_ascii=False)+'\n'); calls.flush(); active.clear()

    save()
    with httpx.Client(trust_env=False, event_hooks={'request':[request_hook], 'response':[response_hook]}) as client:
        parts = local_components(cfg['model_path'], cfg['embedding'], os.environ['PRACTICAL_MODEL_URL'],
                                 http_client=client)
        try:
            for case in inputs['cases']:
                service = ReferenceQA(local/case['id'], profile=cfg.get('profile', 'standard'), **parts)
                row = dict(case_id=case['id'], steps=[]); record['rows'].append(row)
                sources = {}
                for event in case['events']:
                    context.clear(); context.update(case_id=case['id'], label=event['label'])
                    start = time.monotonic(); first = record['calls']
                    try:
                        if event['operation'] == 'import_history':
                            result = service.import_history(event['records'])
                            sources = {digest(source_envelope(e)):source_envelope(e) for e in event['records']}
                        else:
                            assert event['operation'] == 'ask'
                            result = service.ask(event['question'])
                    except Exception as exc:
                        result = dict(status='error', error_type=type(exc).__name__, error=str(exc))
                        if active:
                            calls.write(json.dumps(dict(active, error_type=type(exc).__name__), ensure_ascii=False)+'\n')
                            calls.flush(); active.clear()
                    row['steps'].append(dict(label=event['label'], result=result,
                        calls=record['calls']-first, seconds=time.monotonic()-start))
                    save()
                    print('REFERENCE_STEP', case['id'], event['label'], result['status'], flush=True)
                row['sources_preserved'] = service.store.load('sources') == sources
            record['status'] = 'complete'
        finally:
            save(); calls.close()


if __name__ == '__main__':
    main()
