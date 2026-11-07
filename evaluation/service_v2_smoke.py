"""Small actual-model integration check, not a new benchmark or model search."""
from hashlib import sha256
import importlib.metadata
import json
import os
from pathlib import Path
import sys
from threading import Lock
import time


def main(folder):
    cfg = json.loads((folder/'config.json').read_text())
    assert os.environ['SLURM_JOB_ID'] and os.environ['SLURMD_NODENAME']
    assert os.environ['CONDA_PREFIX'] == cfg['conda_prefix']
    for name, expected in cfg['code_sha256'].items():
        assert sha256((folder/'code'/name).read_bytes()).hexdigest() == expected
    import httpx
    from llama_index.core.llms import ChatMessage
    from team_memory.reference_qa import local_components
    from team_memory.reference_attributed import AttributedQA
    from team_memory.service import TeamMemoryService
    job = os.environ['SLURM_JOB_ID']
    target = Path(cfg['project'])/'results'/('service-v2-'+job+'.json')
    trace = target.with_suffix('.calls.jsonl').open('x')
    record = dict(status='running', job_id=job, source_version=cfg['source_version'],
        code_sha256=cfg['code_sha256'], schema_version='team-memory/v2', model=cfg['model_revision'],
        client_python=sys.executable, conda_prefix=os.environ['CONDA_PREFIX'],
        packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions()},
        import_paths={}, rows=[], requests=0, fresh_benchmark_score=False)
    import team_memory.service, llama_index.core, transformers
    record['import_paths'] = {m.__name__:m.__file__ for m in (team_memory.service, llama_index.core, transformers)}
    began = time.monotonic(); lock = Lock(); current = {'label':'initial'}
    def save():
        record['seconds'] = time.monotonic()-began
        tmp = target.with_suffix('.tmp'); tmp.write_text(json.dumps(record,ensure_ascii=False,indent=2)); tmp.replace(target)
    def request_hook(request):
        if not request.url.path.endswith('/chat/completions'): return
        with lock:
            if record['requests'] >= cfg['max_calls']: raise RuntimeError('Integration request limit reached')
            record['requests'] += 1
            request.extensions['team_memory_trace'] = dict(id=record['requests'], label=current['label'],
                request=json.loads(request.content), started=time.monotonic())
    def response_hook(response):
        response.read(); item = response.request.extensions.get('team_memory_trace')
        if item:
            with lock:
                trace.write(json.dumps(dict(item, response=response.json(),
                    seconds=time.monotonic()-item['started']),ensure_ascii=False)+'\n'); trace.flush()
    store = Path(cfg['project'])/'results'/('service-v2-store-'+job)
    def envelope(text, who, day):
        return dict(owner=who, observed_at=f'2026-01-{day:02d}T00:00:00Z',
            source=dict(speaker=who, location=f'smoke://{who}/{day}', text=text))
    old = envelope('  Under configuration A, the timeout is 10 seconds. The archive name is Orion. '
                   'We paused parallel trials because only one worker was permitted.\n', 'Alice', 1)
    new = envelope('Under configuration B, four workers are now permitted. A trial measured a timeout of 20 seconds. '
                   'The earlier one-worker restriction no longer applies; parallel trials can be reconsidered.', 'Bob', 2)
    correction = envelope('I explicitly correct the earlier timeout report for configuration A under the same settings: '
                          'the timeout is 12 seconds, not 10 seconds. The archive name remains Orion.', 'Bob', 3)
    save()
    try:
        with httpx.Client(trust_env=False, event_hooks={'request':[request_hook], 'response':[response_hook]}) as client:
            parts = local_components(cfg['model_path'], cfg['embedding'], os.environ['PRACTICAL_MODEL_URL'], http_client=client)
            def generate(system, content):
                return parts['llm'].chat([ChatMessage(role='system',content=system),
                    ChatMessage(role='user',content=content)]).message.content
            def service():
                return TeamMemoryService(store, reader=AttributedQA(store, **parts), generate=generate)
            app = service()
            def run(label, request):
                current['label'] = label
                result = app.handle(request)
                record['rows'].append(dict(label=label, request=request, result=result)); save()
                print('SERVICE_STEP', label, result['status'], flush=True)
                if result['status'] in ('error','invalid'): raise RuntimeError('Service operation failed: '+label)
                return result
            run('import', dict(operation='import_history', records=[old]))
            current['label'] = 'standalone_baseline'
            baseline = app.reader.ask('What is the archive name?')
            record['rows'].append(dict(label='standalone_baseline', result=baseline)); save()
            run('ordinary_qa', dict(operation='ask', question='What is the archive name?'))
            run('new_conditions', dict(operation='ingest', source=new))
            run('conditions_qa', dict(operation='ask', question='What timeout was reported under each configuration?'))
            proposals = run('correction', dict(operation='ingest', source=correction))['proposals']
            run('pending_qa', dict(operation='ask', question='What timeout is current for configuration A?'))
            approved = []
            for p in proposals:
                # A scripted test-owner action, never a real person's approval.
                # Only the explicit same-settings correction can be approved here.
                if p['kind']=='correction' and p['previous']['speaker']=='Alice' and '10 seconds' in p['previous']['quote']:
                    run('fixture_owner_approval', dict(operation='review', proposal_id=p['id'], actor='Alice', choice='approve'))
                    approved.append(p['id'])
            record['fixture_approved_proposals'] = approved
            run('current_qa', dict(operation='ask', question='What timeout is current for configuration A?'))
            run('unrelated_qa', dict(operation='ask', question='What is the archive name?'))
            run('historical_qa', dict(operation='ask', question='What timeout did Alice originally report for configuration A?', temporal_scope='historical'))
            app = service()
            run('restart_qa', dict(operation='ask', question='What is the archive name?'))
            record['source_count'] = len(app.store.load('sources'))
            assert record['source_count'] == 3
            assert any(e['source']['text'] == old['source']['text'] for e in app.store.load('sources').values())
            record['status'] = 'complete'
    except BaseException as exc:
        record.update(status='failed', error=type(exc).__name__+': '+str(exc)); raise
    finally:
        save(); trace.close()


if __name__ == '__main__':
    main(Path(sys.argv[1]))
