"""One live connected development run, without gold labels in model inputs."""
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace
import traceback


def main():
    folder = Path(__file__).resolve().parent
    cfg = json.loads((folder/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ.get('SLURMD_NODENAME')
    assert os.environ['CONDA_PREFIX'] == cfg['conda_prefix']
    sys.path[:0] = [str(folder/'code'), cfg['upstream']]
    from cup_mem import CupMemEngine, LLMClient, TraceConfig
    from openai import OpenAI
    from evaluation.cupmem.upstream import verify_source
    from team_memory.cupmem_adapter import CUPMemTeamMemory
    from team_memory.cupmem_service import CUPMemService
    from team_memory.store import digest
    from team_memory.timeline import proposals

    for name, expected in cfg['code_sha256'].items():
        assert sha256((folder/'code'/name).read_bytes()).hexdigest() == expected, name
    upstream_verified = verify_source(Path(cfg['upstream']))
    blob = (folder/'inputs.json').read_bytes()
    assert sha256(blob).hexdigest() == cfg['input_sha256']
    job = os.environ['SLURM_JOB_ID']
    local = Path('/local_datasets/pjw031003/capstone-shared-knowledge/service')/job
    local.mkdir(parents=True, exist_ok=False)
    (local/'inputs.json').write_bytes(blob)
    data = json.loads((local/'inputs.json').read_text())
    out = Path(cfg['project'])/'results'/('cup-service-'+job+'.json')
    assert not out.exists()
    calls, lock = [], threading.Lock()
    start = time.monotonic()
    calls_file = out.with_suffix('.calls.jsonl').open('x')
    record = dict(status='running', job_id=job, input_sha256=cfg['input_sha256'],
        source_version=cfg['source_version'], code_sha256=cfg['code_sha256'],
        model='Qwen3-8B', upstream_revision='ea7d391103a151927cd29d2f01d87597a782bdcb',
        upstream_files_verified=upstream_verified, full_pipeline_rerun=True,
        scope='One existing synthetic development flow plus an unrelated report; not a benchmark',
        sources=data['sources'], steps=[], current_operation='setup', external_model_api_calls=0)

    def save():
        record.update(calls=len(calls), seconds=time.monotonic()-start)
        tmp = out.with_suffix('.tmp')
        tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2)); tmp.replace(out)

    class LimitStop(BaseException): pass

    class LocalClient:
        def __init__(self, **kwargs):
            assert kwargs['base_url'] == 'http://127.0.0.1:28382/v1'
            self.real = OpenAI(**kwargs, max_retries=0, timeout=90)
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

        def create(self, **kwargs):
            with lock:
                if len(calls) >= cfg['max_calls'] or time.monotonic()-start > cfg['client_seconds']-30:
                    raise LimitStop('Bounded development run stopped')
                kwargs['max_tokens'] = 4096
                kwargs.setdefault('temperature', 0.0)
                kwargs.setdefault('response_format', {'type':'json_object'})
                kwargs['extra_body'] = {'chat_template_kwargs':{'enable_thinking':False}}
                row = dict(id=len(calls), operation=record['current_operation'], request=kwargs)
                calls.append(row)
            began = time.monotonic()
            try:
                result = self.real.chat.completions.create(**kwargs)
                row['response'] = result.model_dump(mode='json')
                return result
            except Exception as exc:
                row['error_type'] = type(exc).__name__; raise
            finally:
                row['seconds'] = time.monotonic()-began
                with lock:
                    calls_file.write(json.dumps(row, ensure_ascii=False)+'\n'); calls_file.flush()

    service = None
    save()
    try:
        llm = LLMClient(model='Qwen3-8B', api_key='local-no-secret',
            base_url='http://127.0.0.1:28382/v1', openai_cls=LocalClient)
        engine = CupMemEngine(llm=llm, embedding_model_path=cfg['embedding'], embedding_device='cpu',
                             trace_config=TraceConfig(enable_debug_trace=True))
        reader = LocalClient(api_key='local-no-secret', base_url='http://127.0.0.1:28382/v1')

        def generate(system, content):
            return reader.create(model='Qwen3-8B', messages=[dict(role='system', content=system),
                dict(role='user', content=content)], temperature=0).choices[0].message.content

        service = CUPMemService(CUPMemTeamMemory(engine, lambda:list(calls)), generate, local/'records')

        def operation(label, request):
            record['current_operation'] = label
            value = service.handle(request)
            record['steps'].append(dict(label=label, request=request, result=value))
            save(); print('SERVICE_STEP', label, value['status'], 'calls', len(calls), flush=True)
            return value

        operation('initial_report', dict(operation='ingest', source=data['sources'][0]))
        arrival = operation('changed_condition', dict(operation='ingest', source=data['sources'][1]))
        before = len(calls)
        duplicate = operation('duplicate_report', dict(operation='ingest', source=data['sources'][1]))
        record['duplicate_no_extra_calls'] = len(calls) == before and duplicate.get('replayed') is True
        for q in data['questions']:
            operation('before_review/'+q['id'], dict(operation='ask', question=q['question'], temporal_scope=q['scope']))
        # Explicit simulated owner action on the toy records; never represented as autonomous approval.
        record['owner_review_simulated'] = True
        for p in arrival['proposals']:
            if p['kind'] == 'reconsider':
                operation('simulated_owner_review', dict(operation='review', proposal_id=p['id'],
                    actor=p['reviewer'], choice='approve'))
        operation('unrelated_report', dict(operation='ingest', source=data['sources'][2]))
        for q in data['questions'][:2]:
            operation('after_review/'+q['id'], dict(operation='ask', question=q['question'], temporal_scope=q['scope']))
        record.update(status='complete', sources_preserved=service.store.load('sources'),
                      final_proposals=proposals(service.store), derived_runtime_ready=service.ready,
                      expected_source_ids=[digest(s) for s in service.memory.sources])
    except BaseException as exc:
        record.update(status='failed', error_type=type(exc).__name__, traceback=traceback.format_exc())
        raise
    finally:
        if service:
            try: record['native_snapshot'] = service.memory.snapshot()
            except Exception as exc: record['snapshot_error_type'] = type(exc).__name__
        save(); calls_file.close()


if __name__ == '__main__': main()
