"""Verify a completed local pilot from frozen source and physical HTTP evidence.

No model calls or semantic scoring. A live/failed/censored run cannot pass this
completion verifier. Native scores remain provisional non-independent judgments.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import tarfile

from .audit import digest
from .partial_verify import audit_events, read, require, sha, verify_case
from .upstream import DATA_REVISION, DATA_SHA256, REVISION


def serving_checks(rows, requests, terminal, config):
    preflight, checks = {}, {}
    indexed = defaultdict(list)
    for row in rows:
        number = row['logical_context_check']
        if row['event'] == 'context_preflight':
            require(number not in preflight, 'Duplicate context preflight')
            require(row['compatible'] and row['thinking'] is False, 'Incompatible context/thinking mode')
            require(row['max_model_len'] == config['max_model_len'], 'Context limit changed')
            require(row['actual_qwen_input_tokens'] + row['output_reservation'] <= config['max_model_len'],
                    'Input/output sum exceeds declared context')
            require(row['direct_protocol'] == config['direct_protocol'], 'Protocol changed')
            preflight[number] = row
            indexed[(row['messages_sha256'], digest(row['context']), row['output_reservation'])].append(row)
        elif row['event'] == 'server_usage_check':
            require(number in preflight and number not in checks, 'Orphan/duplicate server usage check')
            before = preflight[number]
            require(row['context'] == before['context'] and row['messages_sha256'] == before['messages_sha256'],
                    'Server usage bound to another input')
            require(row['compatible'] and row['usage_present'], 'Server usage missing or incompatible')
            require(row['expected_qwen_input_tokens'] == row['reported_prompt_tokens'] == before['actual_qwen_input_tokens'],
                    'Server/local token counts differ')
            require(row['reported_model'] == config['actor'], 'Unexpected response model')
            checks[number] = row
        else:
            raise ValueError('Unknown context audit event')
    require(set(preflight) == set(range(1, len(preflight) + 1)), 'Logical context sequence has gaps')
    bound_responses = {}
    for rid, request in requests.items():
        body = request['body']
        require(body.get('chat_template_kwargs') == {'enable_thinking': False}, 'Thinking option missing/changed')
        possible = indexed[(digest(body['messages']), digest(request['context']), body['max_tokens'])]
        require(possible, 'Physical request has no compatible actual-token preflight')
        require(len({p['actual_qwen_input_tokens'] for p in possible}) == 1, 'Same input has inconsistent token counts')
        response = terminal[rid]
        if response['event'] == 'response' and response['status'] == 200:
            payload = response['body']
            require(payload.get('model') == config['actor'], 'Physical response reports another model')
            count = payload.get('usage', {}).get('prompt_tokens')
            require(count == possible[0]['actual_qwen_input_tokens'], 'Physical successful response token mismatch')
            matching = [check for check in checks.values() if check['response_id'] == payload.get('id')]
            require(len(matching) == 1, 'Successful response lacks unique server-usage check')
            check = matching[0]
            require(check['messages_sha256'] == digest(body['messages']) and check['context'] == request['context'],
                    'Physical response check belongs to another request')
            require(check['logical_context_check'] not in bound_responses, 'One response check reused')
            bound_responses[check['logical_context_check']] = rid
    require(set(checks) == set(bound_responses), 'Server-usage check lacks actual successful HTTP response')
    return dict(logical_preflights=len(preflight), verified_successful_responses=len(checks),
                preflights_without_returned_response=sorted(set(preflight) - set(checks)),
                actual_input_range=[min(r['actual_qwen_input_tokens'] for r in preflight.values()),
                                    max(r['actual_qwen_input_tokens'] for r in preflight.values())])


def verify(result_path, source, folder, ledger_path, launch_path, packets_path):
    result, config, ledger, launch = read(result_path), read(source / 'config.json'), read(ledger_path), read(launch_path)
    job = ledger['jobs'][result['source_version']]
    require(result['status'] == 'complete' and launch['status'] == 'complete', 'Program/server lifecycle incomplete')
    require(job['state'] == 'COMPLETED' and job['exit_code'] == '0:0', 'Slurm did not complete successfully')
    require(str(job['job_id']) == str(result['job_id']) == str(launch['job_id']), 'Wrong job evidence')
    require(result['config_sha256'] == launch['config_sha256'] == sha(source / 'config.json'), 'Config differs')
    for name, expected in job['source_sha256'].items():
        require(sha(source / name) == expected, 'Frozen submitted source changed: ' + name)
    require(sha(source / 'harness.tar.gz') == config['harness_archive_sha256'], 'Source archive changed')
    with tarfile.open(source / 'harness.tar.gz') as archive:
        members = archive.getmembers()
        require(len(members) == len(config['harness_files']) and all(m.isfile() for m in members), 'Archive membership changed')
        require({m.name for m in members} == set(config['harness_files']), 'Unexpected archive names')
        for member in members:
            require(hashlib.sha256(archive.extractfile(member).read()).hexdigest() == config['harness_files'][member.name],
                    'Archive source hash differs: ' + member.name)
    require(result['upstream_revision'] == REVISION and result['dataset_revision'] == DATA_REVISION
            and result['dataset_sha256'] == DATA_SHA256, 'Source/data revision changed')
    require(result['verified_upstream_files'] == 72 and result['type_counts'] == {'T1': 200, 'T2': 200}, 'Source/data verification missing')
    require(result['selection'] == config['selection'], 'Case selection changed')
    require(result['conda_prefix'] == launch['conda_prefix'] == config['conda_prefix'], 'Conda mismatch')
    require(Path(result['python']).parent == Path(config['conda_prefix']) / 'bin', 'Wrong Python executable')
    require(launch['model_files_sha256'] == config['model_files_sha256'], 'Weights changed')
    require(launch['model_revision'] == result['model_revision'] == config['model_revision'], 'Model revision differs')
    require(launch['serving'] == result['serving'] == config['serving'], 'Serving configuration differs')
    require(launch['external_model_api_calls'] == 0 and result['judge_is_independent'] is False, 'Misreported provider/judge')
    require(len(result['compatibility_probes']) == 3 and all(p['passed'] for p in result['compatibility_probes']), 'Compatibility probes incomplete')
    policy = dict(config, limits=config['local_limits'], policy=dict(base_url=config['base_url'], models={
        config['actor']: dict(output_limit_field='max_tokens', output_limit=config['max_output_tokens'])}))
    events = [json.loads(line) for line in (folder / 'http.jsonl').read_text().splitlines()]
    accounting, detail, requests, terminal = audit_events(events, policy)
    require(accounting == result['accounting'], 'Reported physical accounting differs')
    require(not accounting['censored_request_ids'], 'Length-censored output is not a complete reproduction')
    context = serving_checks([json.loads(line) for line in (folder / 'context-checks.jsonl').read_text().splitlines()],
                             requests, terminal, config)
    require(sha(packets_path) == config['context_packets_sha256'] == result['context_packets_sha256']
            == launch['context_packets_sha256'], 'Frozen direct packets changed')
    packets = read(packets_path)
    selected_packets = {(p['uid'], p['query_label']): p for p in packets['packets'] if p['variant'] == config['direct_protocol']}
    require(len(selected_packets) == 6, 'Expected six selected direct inputs')
    for request in requests.values():
        ctx = request['context']
        if ctx.get('arm') == 'direct' and ctx['phase'] == 'answer':
            packet = selected_packets[(ctx['uid'], ctx['query_label'])]
            require(request['body']['messages'] == packet['messages'], 'Actual direct input differs from frozen packet')
            require(digest(packet['messages']) == packet['messages_sha256'], 'Direct packet hash differs')
    selected = {row['uid']: row for row in config['selection']}
    require(len(result['completed']) == 2 and {row['uid'] for row in result['completed']} == set(selected), 'Two full cases required')
    cases = [verify_case(row, selected[row['uid']], folder, requests, terminal) for row in result['completed']]
    return dict(status='verified_completed_local_pilot', job_id=result['job_id'],
                label='Two-case alternate-model/tokenizer protocol pilot, not a benchmark-wide score',
                cases=cases, accounting=accounting, http_audit=detail, serving_checks=context,
                source_archive_sha256=config['harness_archive_sha256'], input_packets_sha256=sha(packets_path),
                slurm_elapsed_seconds=job['elapsed_seconds'], allocated_gpu_minutes=job['elapsed_seconds'] * job['gpus'] / 60,
                usage_records=job['usage'], judge_is_independent=False, semantic_source_audit='required separately',
                external_model_api_calls=0, currency_cost='No hosted model API; GPU allocation time is reported, not a currency bill')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('result', 'source', 'folder', 'ledger', 'launch', 'packets', 'output'):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    value = verify(args.result, args.source, args.folder, args.ledger, args.launch, args.packets)
    args.output.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: value[k] for k in ('status', 'job_id', 'accounting', 'allocated_gpu_minutes')}, indent=2))
