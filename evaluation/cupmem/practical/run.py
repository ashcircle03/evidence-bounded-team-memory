"""Run source-only event streams through both arms on one local Slurm model."""
from copy import deepcopy
import gzip
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
    from team_memory.cupmem_candidates import CUPMemCandidateMemory, SourceOnlyMemory, CachedEmbedding
    from team_memory.cupmem_practical import PracticalCUPMemService
    from team_memory.store import source_envelope, digest
    from team_memory.timeline import proposals

    for name, expected in cfg['code_sha256'].items():
        assert sha256((folder/'code'/name).read_bytes()).hexdigest() == expected, name
    upstream_verified = verify_source(Path(cfg['upstream']))
    blob = (folder/'inputs.json').read_bytes()
    assert sha256(blob).hexdigest() == cfg['input_sha256']
    job = os.environ['SLURM_JOB_ID']
    local = Path('/local_datasets/pjw031003/capstone-shared-knowledge/practical')/job
    local.mkdir(parents=True, exist_ok=False); (local/'inputs.json').write_bytes(blob)
    inputs = json.loads(blob)
    out = Path(cfg['project'])/'results'/('cup-practical-'+job+'.json')
    assert not out.exists()
    base_url = os.environ['PRACTICAL_MODEL_URL']
    assert base_url == 'http://127.0.0.1:'+str(31000+int(job)%20000)+'/v1'
    calls, lock, context = [], threading.Lock(), {}
    start = time.monotonic()
    raw_calls = out.with_suffix('.calls.jsonl').open('x')
    writer_log = gzip.open(out.with_suffix('.native.jsonl.gz'), 'xt')
    record = dict(status='running', job_id=job, source_version=cfg['source_version'],
        input_sha256=cfg['input_sha256'], code_sha256=cfg['code_sha256'],
        model='Qwen3-8B', upstream_revision='ea7d391103a151927cd29d2f01d87597a782bdcb',
        upstream_files_verified=upstream_verified, external_model_api_calls=0,
        full_pipeline_rerun=True, scope=inputs['scope'], rows=[])

    def save():
        record.update(calls=len(calls), seconds=time.monotonic()-start, current=dict(context))
        tmp = out.with_suffix('.tmp'); tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2)); tmp.replace(out)

    class LimitStop(BaseException): pass

    class LocalClient:
        def __init__(self, **kwargs):
            assert kwargs['base_url'] == base_url
            self.real = OpenAI(**kwargs, max_retries=0, timeout=90)
            self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

        def create(self, **kwargs):
            with lock:
                if len(calls) >= cfg['max_calls'] or time.monotonic()-start > cfg['client_seconds']-30:
                    raise LimitStop('Bounded run stopped')
                kwargs['max_tokens'] = 4096
                kwargs.setdefault('temperature', 0.0)
                kwargs.setdefault('response_format', {'type':'json_object'})
                kwargs['extra_body'] = {'chat_template_kwargs':{'enable_thinking':False}}
                row = dict(id=len(calls), context=dict(context), request=deepcopy(kwargs))
                calls.append(row)
            began = time.monotonic()
            try:
                value = self.real.chat.completions.create(**kwargs)
                row['response'] = value.model_dump(mode='json'); return value
            except Exception as exc:
                row['error_type'] = type(exc).__name__; raise
            finally:
                row['seconds'] = time.monotonic()-began
                with lock:
                    raw_calls.write(json.dumps(row, ensure_ascii=False)+'\n'); raw_calls.flush()

    save()
    try:
        llm = LLMClient(model='Qwen3-8B', api_key='local-no-secret', base_url=base_url, openai_cls=LocalClient)
        engine = CupMemEngine(llm=llm, embedding_model_path=cfg['embedding'], embedding_device='cpu',
                             trace_config=TraceConfig(enable_debug_trace=True))
        engine.embedding = CachedEmbedding(engine.embedding)
        reader = LocalClient(api_key='local-no-secret', base_url=base_url)

        def generate(system, content):
            return reader.create(model='Qwen3-8B', messages=[dict(role='system', content=system),
                dict(role='user', content=content)], temperature=0).choices[0].message.content

        for index, case in enumerate(inputs['cases']):
            arms = ['simple', 'cupmem'] if index%2 == 0 else ['cupmem', 'simple']
            for arm in arms:
                engine.reset()
                memory = CUPMemCandidateMemory(engine, lambda:list(calls)) if arm == 'cupmem' else SourceOnlyMemory(engine)
                service = PracticalCUPMemService(memory, generate, local/case['id']/arm, strategy=arm)
                item = dict(case_id=case['id'], arm=arm, steps=[])
                record['rows'].append(item)
                expected_sources = {}
                for ordinal, event in enumerate(case['events']):
                    context.clear(); context.update(case_id=case['id'], arm=arm, event=ordinal, label=event['label'])
                    began = time.monotonic(); first = len(calls)
                    if event['operation'] == 'review_reconsider':
                        selected = [p for p in proposals(service.store) if p['kind']=='reconsider' and p['status']=='pending']
                        requests = [dict(operation='review', proposal_id=p['id'], actor=p['reviewer'], choice='approve') for p in selected]
                        results = [service.handle(q) for q in requests]
                        result = dict(simulated_owner_review=True, requests=requests, results=results)
                    else:
                        request = {k: deepcopy(v) for k,v in event.items() if k!='label'}
                        sources = request.get('records', [request['source']] if 'source' in request else [])
                        for source in sources:
                            env = source_envelope(source); expected_sources[digest(env)] = env
                        result = service.handle(request)
                        if 'native_write' in result:
                            original = result.pop('native_write')
                            encoded = json.dumps(original, ensure_ascii=False, sort_keys=True)
                            writer_log.write(json.dumps(dict(context=dict(context), native_write=original), ensure_ascii=False)+'\n'); writer_log.flush()
                            result['native_write_archive'] = dict(file=out.with_suffix('.native.jsonl.gz').name,
                                context=dict(context), sha256=sha256(encoded.encode()).hexdigest())
                    item['steps'].append(dict(label=event['label'], request=event, result=result,
                        seconds=time.monotonic()-began, first_call_id=first, calls=len(calls)-first))
                    save(); print('PRACTICAL_STEP', case['id'], arm, event['label'], len(calls)-first, flush=True)
                item.update(complete=True, sources_preserved=service.store.load('sources')==expected_sources,
                            actual_source_ids=sorted(service.store.load('sources')), expected_source_ids=sorted(expected_sources),
                            final_proposals=proposals(service.store), runtime_ready=service.ready)
                if arm == 'cupmem':
                    snapshot = memory.snapshot()
                    writer_log.write(json.dumps(dict(context=dict(context), final_native_snapshot=snapshot), ensure_ascii=False)+'\n'); writer_log.flush()
                save()
        record['status'] = 'complete'
    except BaseException as exc:
        record.update(status='failed', error_type=type(exc).__name__, traceback=traceback.format_exc())
        raise
    finally:
        save(); raw_calls.close(); writer_log.close()


if __name__ == '__main__': main()
