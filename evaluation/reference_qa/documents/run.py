"""Frozen paired development comparison on Aurora; keys stay evaluator-only."""
from contextlib import redirect_stdout
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import time


TRACE_KEY = 'reference_trace'


def main():
    folder = Path(sys.argv[1])
    config = json.loads((folder/'config.json').read_text())
    assert os.environ['SLURMD_NODENAME']
    assert os.environ['CONDA_PREFIX'] == config['conda_prefix']
    for name, digest in config['code_sha256'].items():
        assert sha256((folder/'code'/name).read_bytes()).hexdigest() == digest, name
    for name, digest in config['data_sha256'].items():
        assert sha256((folder/name).read_bytes()).hexdigest() == digest, name
    sys.path.insert(0, str(folder/'code'))
    import httpx
    from team_memory.reference_qa import local_components
    from team_memory.reference_documents import answer_from_sources

    job = os.environ['SLURM_JOB_ID']
    output = Path(config['project'])/'results'/f'documents-{job}.json'
    result = dict(status='running', job_id=job, source_version=config['source_version'],
                  code_sha256=config['code_sha256'], data_sha256=config['data_sha256'],
                  rows=[], retrieval=[], calls=0, external_model_api_calls=0)
    traces = output.with_suffix('.calls.jsonl').open('x', encoding='utf-8')
    started = time.monotonic()
    context = {}

    def save():
        result['seconds'] = time.monotonic()-started
        temporary = output.with_suffix('.tmp')
        temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        temporary.replace(output)

    def on_request(request):
        if not request.url.path.endswith('/chat/completions'):
            return
        if result['calls'] >= config['max_calls'] or time.monotonic()-started > config['client_seconds']-60:
            raise RuntimeError('Fixed request/time limit reached')
        body = json.loads(request.content)
        tokens = len(parts['tokenizer'].apply_chat_template(body['messages'], tokenize=True,
            add_generation_prompt=True, enable_thinking=False))
        assert tokens+body['max_tokens'] <= 32768
        request.extensions[TRACE_KEY] = dict(id=result['calls'], context=dict(context),
                                          request=body, rendered_prompt_tokens=tokens)
        result['calls'] += 1

    def on_response(response):
        response.read()
        trace = response.request.extensions.get(TRACE_KEY)
        if trace:
            traces.write(json.dumps(dict(trace, response=response.json(),
                                        http_status=response.status_code), ensure_ascii=False)+'\n')
            traces.flush()

    def evaluate(split, case, arm, witnesses):
        context.clear()
        context.update(split=split, case_id=case['id'], arm=arm)
        first_call, began = result['calls'], time.monotonic()
        answer = answer_from_sources(case['question'], witnesses, parts['llm'], reading=arm.split('_')[-1])
        result['rows'].append(dict(**context, question=case['question'],
            retrieval_sources=witnesses, result=answer,
            calls=result['calls']-first_call, seconds=time.monotonic()-began))
        save()
        print('STEP', split, case['id'], arm, answer['status'], flush=True)

    cases = json.loads((folder/'inputs.json').read_text())
    save()
    with httpx.Client(trust_env=False, event_hooks={'request':[on_request], 'response':[on_response]}) as client:
        with redirect_stdout(sys.stderr):
            parts = local_components(config['model_path'], config['embedding'],
                                     os.environ['PRACTICAL_MODEL_URL'], http_client=client)
        try:
            retrieval_path=Path(config['project'])/'results'/f'documents-{job}.retrieval.json'
            retrieval=json.loads(retrieval_path.read_text())
            assert retrieval['status']=='complete' and retrieval['job_id']==job
            assert retrieval['code_sha256']==config['code_sha256']
            result['retrieval']=retrieval['retrieval']
            result['retrieval_sha256']=sha256(retrieval_path.read_bytes()).hexdigest()
            selected={r['id']:r for r in result['retrieval']}
            for case in cases['legacy']:
                for arm in ('direct','con'):
                    evaluate('legacy',case,arm,case['sources'])
            for case in cases['ever']:
                assert selected[case['id']]['initial_sources']==case['sources']
                for retriever, sources in [('bm25',case['sources']),('dense',selected[case['id']]['sources'])]:
                    for reading in ('direct','con'):
                        evaluate('ever',case,retriever+'_'+reading,sources)
            assert len(result['rows'])==80 and result['calls']==80
            result['status'] = 'complete'
        finally:
            save()
            traces.close()


if __name__ == '__main__':
    main()
