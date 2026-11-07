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
    from team_memory.reference_claims import answer_from_sources as claims_reader
    from team_memory.reference_contextual import answer_from_sources as contextual_reader
    from team_memory.reference_retrieval import FeedbackRetriever
    from team_memory.store import digest
    from evaluation.reference_qa.expanded.run import iter_dialogue_messages

    job = os.environ['SLURM_JOB_ID']
    output = Path(config['project'])/'results'/f'contextual-{job}.json'
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
        reader = claims_reader if arm == 'retrieval_only' else contextual_reader
        answer = reader(case['question'], witnesses, parts['llm'])
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
            for case in cases['legacy']:
                evaluate('legacy', case, 'contextual', case['sources'])
            for topic in ['01', '02']:
                data = Path(config['dataset_root'])/'EverMemBench-Dynamic'/topic/'dialogue.json'
                sources = []
                for date, group, index, message in iter_dialogue_messages(json.loads(data.read_text())):
                    location = f"EverMemBench-Dynamic@{config['ever_revision']}/{topic}/{date}/{group}/{index}"
                    envelope = dict(owner=message['speaker'], observed_at=message['time'],
                        source=dict(text=message['dialogue'], location=location, speaker=message['speaker']))
                    sources.append(dict(source_id=digest(envelope), quote=message['dialogue'],
                        start=0, end=len(message['dialogue']), location=location,
                        speaker=message['speaker'], observed_at=message['time']))
                with redirect_stdout(sys.stderr):
                    retriever = FeedbackRetriever(sources, parts['tokenizer'], parts['llm'])
                for case in (c for c in cases['ever'] if c['topic']==topic):
                    # Reader-only arm isolates context preservation from retrieval.
                    evaluate('ever', case, 'reader_only', case['sources'])
                    context.clear()
                    context.update(split='ever', case_id=case['id'], arm='retrieval')
                    retrieved = retriever.retrieve(case['query'])
                    assert retrieved['trace']['initial_sources'] == case['sources'], case['id']
                    result['retrieval'].append(dict(id=case['id'], **retrieved))
                    save()
                    for arm in ['retrieval_only', 'combined']:
                        evaluate('ever', case, arm, retrieved['sources'])
            assert len(result['rows']) == 50
            assert len(result['retrieval']) == 10
            result['status'] = 'complete'
        finally:
            save()
            traces.close()


if __name__ == '__main__':
    main()
