"""Read-only instrumented upstream inference. Never reads evaluation labels."""
import hashlib
import inspect
import json
import os
from pathlib import Path
import time


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def install_trace(model):
    import torch
    from gliner2.inference.candidate_decoder import token_boundaries_to_character_offsets
    state = {}
    original_head = model.record_decoder.forward_groups_dense
    original_decode = model._decode_records
    signature = inspect.signature(original_decode)

    def head(*args, **kwargs):
        result = original_head(*args, **kwargs)
        state['dense'] = result
        return result

    def decode(*args, **kwargs):
        bound = signature.bind(*args, **kwargs).arguments
        dense = state['dense']; batch = bound['batch']; i = bound['sample_index']
        candidates = bound['candidates']; text = bound['text']; offset = bound['offset']
        specs = list(batch.record_specs[i].values())
        assert len(specs) == 1
        spec = specs[0]
        spans = dense.pool_spans[i].detach().cpu().tolist()
        pool = []
        for j, (start, end) in enumerate(spans):
            a, b = start - offset, end - offset
            if a < 0 or b > bound['text_len'] or b <= a:
                continue
            cs, ce = token_boundaries_to_character_offsets(a, b, bound['start_map'], bound['end_map'])
            pool.append(dict(index=j, start=cs, end=ce, text=text[cs:ce],
                probabilities={f.name: float(torch.sigmoid(candidates.pair_logits[i, f.query_id, j] / model.boundary_settings.pair_temperature)) for f in spec.fields}))
        probabilities = torch.sigmoid(dense.object_logits[i, 0] / model.boundary_settings.record_temperature).detach().cpu()
        assignments = torch.sigmoid(dense.assign_logits[i, 0] / model.boundary_settings.record_temperature).detach().cpu()
        anchors = []
        for p in pool:
            j = p['index']
            if probabilities[j] < .5 and p['text'] not in state['original_claims']:
                continue
            anchors.append(dict(index=j, text=p['text'], start=p['start'], end=p['end'],
                probability=float(probabilities[j]), selected=bool(probabilities[j] >= .5),
                assignments={f.name: [float(assignments[j, k, x['index'] + 1]) for x in pool] for k, f in enumerate(spec.fields) if f.name != 'claim'}))
        state['trace'] = dict(pool=pool, anchors=anchors,
            field_order=[f.name for f in spec.fields], threshold=.5,
            truncated=False, source_tokens=bound['text_len'])
        return original_decode(*args, **kwargs)

    model.record_decoder.forward_groups_dense = head
    model._decode_records = decode
    return state


def main(folder):
    cfg = json.loads((folder / 'config.json').read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ.get('SLURMD_NODENAME')
    assert os.environ['CONDA_PREFIX'] == cfg['conda_prefix']
    for name, expected in cfg['files_sha256'].items():
        assert sha(folder / name) == expected, name
    import torch
    from gliner2 import AutoExtractor
    from team_memory.records.learned_binding import predict
    torch.manual_seed(42); torch.set_num_threads(8)
    assert torch.cuda.device_count() == 1
    job = os.environ['SLURM_JOB_ID']
    output = Path(cfg['project']) / 'results' / f'record-trace-{job}.json'
    assert not output.exists()
    started = time.monotonic()
    result = dict(status='running', job_id=job, node=os.environ['SLURMD_NODENAME'], rows=[],
                  config=cfg, external_model_api_calls=0, training_steps=0, checkpoint_sha256={})
    def save():
        result['seconds'] = time.monotonic() - started
        tmp = output.with_suffix('.tmp'); tmp.write_text(json.dumps(result, ensure_ascii=False)); tmp.replace(output)
    try:
        items = json.loads((folder / 'inputs.json').read_text())
        for arm, path in cfg['checkpoints'].items():
            result['checkpoint_sha256'][arm] = sha(Path(path) / 'model.safetensors')
            model = AutoExtractor.from_pretrained(path, map_location='cuda'); model.eval()
            state = install_trace(model)
            for item in items:
                state['original_claims'] = item['claims']
                with torch.inference_mode():
                    prediction = predict(model, item['source'])
                result['rows'].append(dict(id=item['id'], arm=arm, prediction=prediction, trace=state.pop('trace')))
                print('TRACE', arm, item['id'], flush=True)
            del state['dense']; del model; torch.cuda.empty_cache(); save()
        result['status'] = 'complete'
    except BaseException as exc:
        result.update(status='failed', error=f'{type(exc).__name__}: {exc}'); raise
    finally:
        save()


if __name__ == '__main__':
    import sys
    main(Path(sys.argv[1]))
