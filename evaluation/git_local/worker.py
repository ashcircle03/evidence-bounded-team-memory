"""One fresh OS process per phase, with checkout-private derived state."""
import json
import os
from pathlib import Path
import sys
import time
from unittest.mock import patch


def main(packet, checkout, phase, output, prepare, canary):
    import httpx
    from team_memory.readers.retrieval import local_components
    from team_memory.readers.attribution import AttributedQA
    from team_memory.service import TeamMemoryService
    from team_memory.readers import indexing

    cfg = json.loads((packet/'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ['CONDA_PREFIX'] == cfg['conda_prefix']
    inputs = json.loads((packet/'inputs.json').read_text())
    report = dict(phase=phase, pid=os.getpid(), checkout=str(checkout), status='running',
                  endpoint=os.environ['PRACTICAL_MODEL_URL'], calls=0, rows=[], preparation=[],
                  document_batches=[], parsed_source_ids=[], query_embeddings=0)
    context = {}
    trace = output.with_suffix('.calls.jsonl').open('x')
    started = time.monotonic()
    def save():
        report['seconds'] = time.monotonic()-started
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    def request(req):
        if not req.url.path.endswith('/chat/completions'): return
        assert req.url.host == '127.0.0.1'
        assert report['calls'] < 200, 'Fixed phase call bound'
        report['calls'] += 1
        req.extensions['git_trace'] = dict(id=report['calls'], context=dict(context),
            request=json.loads(req.content), started=time.monotonic())
    def response(res):
        res.read()
        item = res.request.extensions.get('git_trace')
        if item:
            trace.write(json.dumps(dict(item, response=res.json(), seconds=time.monotonic()-item['started']), ensure_ascii=False)+'\n')
            trace.flush()
    try:
        with httpx.Client(trust_env=False, event_hooks={'request':[request], 'response':[response]}) as client:
            parts = local_components(cfg['model_path'], cfg['embedding'], os.environ['PRACTICAL_MODEL_URL'], http_client=client)
            cls = type(parts['embed_model'])
            original_embed, original_query = cls._get_text_embeddings, cls._get_query_embedding
            original_parse = indexing.document_nodes
            def embed(self, texts):
                report['document_batches'].append(dict(context=dict(context), texts=texts))
                return original_embed(self, texts)
            def query(self, text):
                report['query_embeddings'] += 1
                return original_query(self, text)
            def parse(*args, **kwargs):
                value = original_parse(*args, **kwargs)
                report['parsed_source_ids'].extend(sorted({n.ref_doc_id for n in value}))
                return value
            with patch.object(cls, '_get_text_embeddings', embed), patch.object(cls, '_get_query_embedding', query), patch.object(indexing, 'document_nodes', parse):
                for case in inputs['cases']:
                    cid = case['id']; path = checkout/'records'/cid
                    # No sync/comparator is substituted: this experiment explicitly
                    # exercises records/index preparation and the production QA path.
                    reader = AttributedQA(path, **parts)
                    def no_comparison(*args):
                        raise AssertionError('Relationship inference is outside this experiment')
                    svc = TeamMemoryService(path, reader=reader, generate=no_comparison)
                    context.clear(); context.update(case_id=cid, operation='prepare')
                    if prepare:
                        prepared = reader.prepare_index()
                        report['preparation'].append(dict(case_id=cid, result=prepared))
                        save()
                    questions = [dict(q, temporal_scope='historical') for q in case['questions']]
                    if canary and cid == inputs['cases'][0]['id']:
                        questions.append(dict(label='canary', temporal_scope='historical', question=(
                            'According to the storage probe report dated 2026-01-0'+str(canary)+
                            ', what is the depot marker for the Zephyr spare telemetry unit? Cite that report.')))
                    for q in questions:
                        context.clear(); context.update(case_id=cid, operation='ask', label=q['label'])
                        before=report['calls']; docbefore=len(report['document_batches']); parsebefore=len(report['parsed_source_ids'])
                        answer=svc.handle(dict(operation='ask', question=q['question'], temporal_scope=q['temporal_scope']))
                        report['rows'].append(dict(case_id=cid, label=q['label'], question=q['question'], result=answer,
                            calls=report['calls']-before, document_batches=len(report['document_batches'])-docbefore,
                            parsed_documents=len(report['parsed_source_ids'])-parsebefore))
                        save(); print('QA', phase, cid, q['label'], answer['status'], flush=True)
                    report.setdefault('index_paths', []).append(str(reader.index_dir))
        report['status']='complete'
    except BaseException as exc:
        report.update(status='failed', error=repr(exc)); raise
    finally:
        save(); trace.close()


if __name__ == '__main__':
    main(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), bool(int(sys.argv[5])), int(sys.argv[6]))
