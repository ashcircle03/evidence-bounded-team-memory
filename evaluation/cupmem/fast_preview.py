"""Short, fresh inference through the existing direct team-memory system.

This is a development preview, not CUPMem or a STALE reproduction. No semantic
rules, prompts, historical scores, or trained weights are changed.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import sys
import time


def file_hash(path):
    h = sha256()
    with Path(path).open('rb') as f:
        while chunk := f.read(8 * 1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def save(path, data):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)


def main(config_path):
    config_path = Path(config_path).resolve()
    cfg = json.loads(config_path.read_text())
    assert os.environ.get('SLURM_JOB_ID') and os.environ.get('SLURMD_NODENAME')
    assert os.environ.get('CONDA_PREFIX') == cfg['conda_prefix']
    for key in ('OPENAI_API_KEY', 'BAZE_API_KEY', 'HF_TOKEN', 'HUGGING_FACE_HUB_TOKEN'):
        os.environ.pop(key, None)
    import torch
    assert torch.cuda.device_count() == 1
    job = os.environ['SLURM_JOB_ID']
    out = Path(cfg['project']) / 'results' / ('sm-' + job + '.json')
    assert not out.exists(), 'Never overwrite an earlier run'
    start = time.monotonic()
    record = dict(status='preparing', job_id=job, source_version=cfg['source_version'],
                  config_sha256=file_hash(config_path), model=cfg['model_repo'],
                  revision=cfg['model_revision'], node=os.environ['SLURMD_NODENAME'],
                  conda_prefix=os.environ['CONDA_PREFIX'], devices=[torch.cuda.get_device_name(0)],
                  scope='three pre-existing synthetic development streams; direct mode only',
                  external_model_api_calls=0, streams={})
    save(out, record)
    try:
        code = config_path.parent / 'code'
        for name, expected in cfg['source_files'].items():
            assert file_hash(code / name) == expected, name
        sys.path.insert(0, str(code))
        from evaluation.timeline.runner import stream
        local, shared = Path(cfg['model_path']), Path(cfg['model_shared'])
        ready = json.loads((shared / 'READY.json').read_text())
        assert ready['revision'] == cfg['model_revision']
        assert ready['files_sha256'] == cfg['model_files_sha256']
        local.mkdir(parents=True, exist_ok=True)
        for name, expected in cfg['model_files_sha256'].items():
            assert Path(name).name == name
            p = local / name
            if not p.exists():
                temporary = local / (name + '.preview-' + job)
                assert not temporary.exists()
                shutil.copyfile(shared / name, temporary)
                assert file_hash(temporary) == expected, name
                temporary.replace(p)
            else:
                assert file_hash(p) == expected, name
        extra = [p.name for p in local.iterdir() if p.is_file()
                 and p.suffix in ('.json', '.bin', '.safetensors', '.py', '.jinja')
                 and p.name not in cfg['model_files_sha256']]
        assert not extra, extra
        data = (config_path.parent / 'inputs.json').read_bytes()
        assert sha256(data).hexdigest() == cfg['input_sha256']
        data_path = Path('/local_datasets/pjw031003/capstone-shared-knowledge/fast-preview') / job
        data_path.mkdir(parents=True, exist_ok=False)
        (data_path / 'inputs.json').write_bytes(data)
        rows = json.loads(data)
        record.update(input_sha256=cfg['input_sha256'], model_files_verified=True,
                      source_files=cfg['source_files'], status='loading')
        save(out, record)
        from vllm import LLM, SamplingParams
        model = LLM(model=str(local), dtype='bfloat16', tensor_parallel_size=1,
                    max_model_len=8192, max_num_seqs=1, gpu_memory_utilization=0.90,
                    max_num_batched_tokens=4096, enable_chunked_prefill=True,
                    enforce_eager=True, seed=42, generation_config='vllm')
        tokenizer = model.get_tokenizer()
        calls_path = out.with_name('preview-calls-' + job + '.jsonl')
        calls_file = calls_path.open('x')

        class Generate:
            cap = 512
            last_usage = {}

            def __call__(self, system, content):
                if time.monotonic() - start > 490:
                    raise TimeoutError('Preview internal deadline; preserve partial results')
                messages = [dict(role='system', content=system), dict(role='user', content=content)]
                prompt = tokenizer.apply_chat_template(messages, tokenize=False,
                              add_generation_prompt=True, enable_thinking=False)
                tokens = tokenizer.encode(prompt, add_special_tokens=False)
                assert len(tokens) + self.cap <= 8192, 'No silent truncation'
                began = time.monotonic()
                result = model.generate([dict(prompt_token_ids=tokens)],
                            SamplingParams(temperature=0, max_tokens=self.cap, seed=42),
                            use_tqdm=False)[0]
                response = result.outputs[0]
                self.last_usage = dict(input_tokens=len(result.prompt_token_ids),
                                       output_tokens=len(response.token_ids))
                calls_file.write(json.dumps(dict(system=system, content=content, raw=response.text,
                    usage=self.last_usage, finish_reason=response.finish_reason,
                    seconds=time.monotonic()-began), ensure_ascii=False) + '\n')
                calls_file.flush()
                return response.text

        record.update(status='running', startup_seconds=time.monotonic()-start,
                      decoding=dict(temperature=0, seed=42, enable_thinking=False,
                                    max_context_tokens=8192, output_caps='unchanged timeline Reader'))
        save(out, record)
        for row in rows:
            item = stream(row, 'direct', Generate())
            record['streams'][row['id'] + '/direct'] = item
            save(out, record)
            print('STREAM_COMPLETE', row['id'], len(item['calls']), flush=True)
        calls_file.close()
        record.update(status='complete', seconds=time.monotonic()-start)
        save(out, record)
    except BaseException as e:
        record.update(status='failed', error=type(e).__name__ + ': ' + str(e),
                      seconds=time.monotonic()-start)
        save(out, record)
        raise


if __name__ == '__main__':
    main(sys.argv[1])
