"""Launch the pinned local server inside the same GPU Slurm allocation.

This owns only its child server, never a Slurm job or another server. It stages
explicit model files, records hashes/arguments, waits for loopback readiness,
and runs the fresh official pilot. No credentials or hosted model APIs.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import time
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, build_opener

from .local_official import validate_config, validate_runtime
from .official import save


def sha(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while block := stream.read(8 * 1024 * 1024):
            value.update(block)
    return value.hexdigest()


def server_command(config):
    serve = config['serving']
    if (serve['tensor_parallel_size'] != 2 or serve['max_num_seqs'] != 1
            or serve['gpu_memory_utilization'] != 0.90 or serve['max_num_batched_tokens'] != 4096):
        raise ValueError('Serving resources differ from the declared two-GPU configuration')
    port = urlsplit(config['base_url']).port
    return [sys.executable, '-m', 'vllm.entrypoints.openai.api_server',
            '--model', config['model_path'], '--served-model-name', config['actor'],
            '--host', '127.0.0.1', '--port', str(port), '--dtype', 'bfloat16',
            '--tensor-parallel-size', '2', '--distributed-executor-backend', 'mp',
            '--max-model-len', str(config['max_model_len']),
            '--rope-scaling', json.dumps(serve['rope_scaling'], separators=(',', ':')),
            '--gpu-memory-utilization', '0.90', '--max-num-seqs', '1',
            '--enable-chunked-prefill', '--max-num-batched-tokens', '4096',
            '--enforce-eager', '--guided-decoding-backend', 'xgrammar',
            '--generation-config', 'vllm', '--seed', str(serve['seed'])]


def stage_model(config):
    """Copy only manifest-listed verified weights to node-local storage."""
    local, shared = Path(config['model_path']), Path(config['model_shared'])
    ready = json.loads((shared / 'READY.json').read_text())
    if (ready['repository'] != config['model_repo'] or ready['revision'] != config['model_revision']
            or ready['files_sha256'] != config['model_files_sha256']):
        raise ValueError('Prepared shared model does not match the frozen revision/hashes')
    local.mkdir(parents=True, exist_ok=True)
    extras = [p.name for p in local.iterdir() if p.is_file() and p.name not in config['model_files_sha256']
              and p.suffix in {'.json', '.py', '.jinja', '.safetensors', '.bin', '.model'}]
    if extras:
        raise ValueError('Unmanifested loadable files in local model directory: ' + ', '.join(extras))
    actual = {}
    for name, expected in config['model_files_sha256'].items():
        if Path(name).name != name:
            raise ValueError('Model manifest may contain only explicit flat filenames')
        target = local / name
        if not target.exists():
            temporary = local / (name + '.stage-' + os.environ['SLURM_JOB_ID'])
            if temporary.exists():
                raise FileExistsError('Partial stage already exists; preserve it')
            shutil.copyfile(shared / name, temporary)
            if sha(temporary) != expected:
                raise ValueError('Model staging hash mismatch: ' + name)
            temporary.replace(target)
        actual[name] = sha(target)
        if actual[name] != expected:
            raise ValueError('Existing local model hash mismatch: ' + name)
    return actual


def stop_child(process):
    report = dict(signal_sent=False, errors=[])
    if process is None:
        return report
    # A private process group was created specifically for this server.
    try:
        os.killpg(process.pid, signal.SIGTERM)
        report['signal_sent'] = True
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            process.poll()
            try:
                os.killpg(process.pid, 0)
            except ProcessLookupError:
                break
            time.sleep(0.1)
        else:
            os.killpg(process.pid, signal.SIGKILL)
            report['forced_group_kill'] = True
        process.wait(timeout=10)
    except ProcessLookupError:
        process.poll()
    except Exception as exc:
        report['errors'].append(dict(type=type(exc).__name__, message=str(exc)))
    return report


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise RuntimeError('Loopback readiness must not redirect')


def local_env():
    env = dict(os.environ)
    for name in ('OPENAI_API_KEY', 'BAZE_API_KEY', 'HF_TOKEN', 'HUGGING_FACE_HUB_TOKEN'):
        env.pop(name, None)
    env.update(HF_HUB_DISABLE_IMPLICIT_TOKEN='1', HF_HUB_DISABLE_TELEMETRY='1')
    return env


def run(config_path):
    if not os.environ.get('SLURM_JOB_ID') or not os.environ.get('SLURMD_NODENAME'):
        raise RuntimeError('Slurm compute node required')
    config_path = Path(config_path).resolve()
    config = json.loads(config_path.read_text())
    validate_config(config)
    import torch
    validate_runtime(config, os.environ, sys.executable, torch.cuda.device_count())
    if torch.cuda.device_count() != 2:
        raise RuntimeError('This pinned launch requires exactly two allocated GPUs')
    job, project = os.environ['SLURM_JOB_ID'], Path(config['project'])
    path = project / 'results' / ('cup-launch-' + job + '.json')
    if path.exists():
        raise FileExistsError('Do not overwrite earlier launch evidence')
    server_log = project / 'logs' / ('cup-vllm-' + job + '.log')
    record = dict(status='preparing', job_id=job, config_sha256=sha(config_path),
                  model_repo=config['model_repo'], model_revision=config['model_revision'],
                  serving=config['serving'], conda_prefix=os.environ['CONDA_PREFIX'],
                  python=sys.executable, node=os.environ['SLURMD_NODENAME'],
                  server_log=str(server_log), external_model_api_calls=0)
    started, process, pilot = time.monotonic(), None, None
    previous_term = signal.getsignal(signal.SIGTERM)
    def terminated(signum, frame):
        raise KeyboardInterrupt('Slurm SIGTERM received')
    signal.signal(signal.SIGTERM, terminated)
    try:
        record['versions'] = {name: importlib.metadata.version(name) for name in
                              ('torch', 'transformers', 'vllm', 'openai')}
        expected_versions = dict(torch='2.6.0', transformers='4.51.3', vllm='0.8.5.post1', openai='1.78.1')
        if record['versions'] != expected_versions:
            raise ValueError('Prepared runtime versions changed')
        record['torch_cuda'] = torch.version.cuda
        record['installed_packages'] = json.loads(subprocess.check_output(
            [sys.executable, '-m', 'pip', 'list', '--format=json'], text=True))
        record['allocated_devices'] = [dict(name=torch.cuda.get_device_name(i),
            total_memory=torch.cuda.get_device_properties(i).total_memory,
            capability=list(torch.cuda.get_device_capability(i))) for i in range(2)]
        record['nvidia_smi'] = subprocess.check_output(
            ['nvidia-smi', '--query-gpu=uuid,name,driver_version,memory.total', '--format=csv,noheader'], text=True)
        record['model_files_sha256'] = stage_model(config)
        packet_source = Path(config['context_packets_source'])
        packet_local = Path(config['context_packets_path'])
        if not str(packet_local).startswith('/local_datasets/'):
            raise ValueError('Dataset-derived model packets must be read from node-local datasets')
        if sha(packet_source) != config['context_packets_sha256']:
            raise ValueError('Prepared direct packet archive changed')
        packet_local.parent.mkdir(parents=True, exist_ok=True)
        if not packet_local.exists():
            staging = packet_local.with_suffix('.stage-' + job)
            if staging.exists():
                raise FileExistsError('Preserve earlier packet staging evidence')
            shutil.copyfile(packet_source, staging)
            if sha(staging) != config['context_packets_sha256']:
                raise ValueError('Direct packet staging hash mismatch')
            staging.replace(packet_local)
        if sha(packet_local) != config['context_packets_sha256']:
            raise ValueError('Existing node-local direct packets changed')
        record['context_packets_sha256'] = sha(packet_local)
        command = server_command(config)
        record['command'] = command
        host, port = '127.0.0.1', urlsplit(config['base_url']).port
        with socket.socket() as probe:
            if probe.connect_ex((host, port)) == 0:
                raise RuntimeError('Configured port already has a server; do not reuse or stop it')
        env = dict(local_env(), VLLM_USE_V1='1', VLLM_NO_USAGE_STATS='1', DO_NOT_TRACK='1',
                   HF_HUB_OFFLINE='1', HF_HUB_DISABLE_IMPLICIT_TOKEN='1', HF_HUB_DISABLE_TELEMETRY='1')
        record['status'] = 'starting_server'
        save(path, record)
        with server_log.open('x') as log:
            process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                       env=env, start_new_session=True)
            record['server_pid'] = process.pid
            deadline = time.monotonic() + config['server_startup_seconds']
            base = 'http://127.0.0.1:' + str(port)
            opener = build_opener(ProxyHandler({}), NoRedirect())
            while True:
                if process.poll() is not None:
                    raise RuntimeError('Local server exited before readiness')
                try:
                    with opener.open(base + '/health', timeout=2) as response:
                        healthy = response.status == 200
                except (OSError, TimeoutError):
                    healthy = False
                if healthy:
                    break
                if time.monotonic() >= deadline:
                    raise TimeoutError('Fixed server startup deadline exceeded')
                time.sleep(2)
            with opener.open(base + '/v1/models', timeout=5) as response:
                record['model_catalog'] = json.load(response)
            if config['actor'] not in [m['id'] for m in record['model_catalog']['data']]:
                raise ValueError('Local served alias differs from frozen actor')
            record.update(status='running_pilot', startup_elapsed_seconds=time.monotonic() - started)
            save(path, record)
            pilot = subprocess.Popen([sys.executable, '-u', '-m', 'evaluation.cupmem.local_official',
                                      str(config_path)], env=local_env())
            returncode = pilot.wait()
            record['pilot_exit_code'] = returncode
            if returncode:
                raise RuntimeError('Pilot failed or stopped; preserve partial native evidence')
            result = json.loads((project / 'results' / ('sm-' + job + '.json')).read_text())
            if result['status'] != 'complete' or result['config_sha256'] != record['config_sha256']:
                raise ValueError('Pilot completion/config mismatch')
            record['status'] = 'complete'
    except BaseException as exc:
        record.update(status='failed', error_type=type(exc).__name__, error=str(exc))
        raise
    finally:
        try:
            if pilot is not None and pilot.poll() is None:
                pilot.terminate()
                try:
                    pilot.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    pilot.kill()
                    pilot.wait(timeout=10)
        except Exception as exc:
            record['pilot_cleanup_error'] = dict(type=type(exc).__name__, message=str(exc))
        finally:
            try:
                record['server_cleanup'] = stop_child(process)
            except Exception as exc:
                record['server_cleanup_error'] = dict(type=type(exc).__name__, message=str(exc))
            finally:
                signal.signal(signal.SIGTERM, previous_term)
                record['elapsed_seconds'] = time.monotonic() - started
                if process is not None:
                    record['server_exit_code'] = process.poll()
                save(path, record)
        if (record.get('pilot_cleanup_error') or record.get('server_cleanup_error')
                or record.get('server_cleanup', {}).get('errors')):
            if record['status'] == 'complete':
                record['status'] = 'cleanup_failed'
                save(path, record)
                raise RuntimeError('Local server cleanup failed; see launch evidence')


if __name__ == '__main__':
    run(sys.argv[1])
