"""Audit a stopped pilot without promoting partial work to a completed run.

Offline only. Physical attempts, uncertain usage, source archives, saved answers,
and complete case traces are checked independently of their semantic quality.
The original complete-run verifier and frozen inference source are unchanged.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import tarfile

from .audit import canonical, digest
from .official import state_hash
from .upstream import DATA_REVISION, DATA_SHA256, REVISION


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def audit_events(events, config):
    """Replay reservations in file order, including SDK retries and errors."""
    limits = config['limits']
    requests, terminal, pending = {}, {}, {}
    observed_in = observed_out = reserved_in = reserved_out = 0
    uncertain, censored, models, statuses = [], [], Counter(), Counter()
    groups = defaultdict(lambda: dict(requests=0, observed_input_tokens=0,
                                      observed_output_tokens=0, uncertain_request_ids=[]))
    for event in events:
        rid = event['request_id']
        kind = event['event']
        if kind == 'request':
            require(rid == len(requests) + 1, 'Duplicate or nonsequential physical request ID')
            body = event['body']
            require(event['body_sha256'] == digest(body), 'Changed request body')
            require(event['endpoint'] == config['policy']['base_url'].rstrip('/') + '/chat/completions',
                    'Unapproved destination')
            require(body['model'] in config['policy']['models'], 'Unapproved model')
            context = event['context']
            expected_model = (context['model'] if context['phase'] == 'compatibility_probe'
                              else config['judge'] if context['phase'] == 'official_judge'
                              else config['actor'])
            require(body['model'] == expected_model, 'Model role differs from configured actor/judge')
            policy = config['policy']['models'][body['model']]
            require(all(isinstance(m['content'], str) for m in body['messages']), 'Nontext input')
            ri = len(canonical(body['messages']).encode()) + 64 * len(body['messages']) + 256
            ro = body[policy['output_limit_field']]
            require(0 < ro <= policy['output_limit'], 'Unexpected output cap')
            require((ri, ro) == (event['input_reservation'], event['output_reservation']),
                    'Reservation does not match actual input')
            require(rid <= limits['requests'], 'Physical request cap exceeded')
            require(observed_in + reserved_in + ri <= limits['input_tokens'], 'Input reservation cap exceeded')
            require(observed_out + reserved_out + ro <= limits['output_tokens'], 'Output reservation cap exceeded')
            requests[rid] = event
            pending[rid] = (ri, ro)
            reserved_in += ri
            reserved_out += ro
            ctx = event['context']
            group = (ctx.get('uid', 'compatibility'), ctx.get('arm', 'probe'), ctx['phase'])
            groups[group]['requests'] += 1
            continue
        require(kind in ('response', 'transport_error'), 'Unknown audit event')
        require(rid in requests and rid not in terminal, 'Orphan or duplicate terminal event')
        terminal[rid] = event
        ctx = requests[rid]['context']
        group = (ctx.get('uid', 'compatibility'), ctx.get('arm', 'probe'), ctx['phase'])
        if kind == 'transport_error':
            uncertain.append(rid)
            groups[group]['uncertain_request_ids'].append(rid)
            continue
        statuses[event['status']] += 1
        body = event['body']
        usage = body.get('usage', {}) if isinstance(body, dict) else {}
        inp, out = usage.get('prompt_tokens'), usage.get('completion_tokens')
        known = all(type(n) is int and n >= 0 for n in (inp, out))
        require(known == event['usage_known'], 'Usage-known flag is incorrect')
        if known:
            ri, ro = pending.pop(rid)
            require(inp <= ri and out <= ro, 'Provider exceeded reservation')
            reserved_in -= ri
            reserved_out -= ro
            observed_in += inp
            observed_out += out
            groups[group]['observed_input_tokens'] += inp
            groups[group]['observed_output_tokens'] += out
        else:
            uncertain.append(rid)
            groups[group]['uncertain_request_ids'].append(rid)
        if isinstance(body, dict):
            if 'model' in body:
                models[body['model']] += 1
            if any(c.get('finish_reason') == 'length' for c in body.get('choices', [])):
                censored.append(rid)
    require(set(requests) == set(terminal), 'Unterminated physical request; cannot finish audit')
    require(set(pending) == set(uncertain), 'Lost uncertain reservation')
    summary = dict(requests=len(requests), observed_input_tokens=observed_in,
                   observed_output_tokens=observed_out,
                   reserved_or_uncertain_input_tokens=reserved_in,
                   reserved_or_uncertain_output_tokens=reserved_out,
                   uncertain_request_ids=uncertain, censored_request_ids=censored, limits=limits)
    detail = dict(reported_models=dict(models), http_statuses=dict(statuses),
                  transport_errors=[dict(request_id=r, error_type=terminal[r]['error_type'])
                                    for r in uncertain if terminal[r]['event'] == 'transport_error'],
                  groups=[dict(uid=k[0], arm=k[1], phase=k[2], **v) for k, v in sorted(groups.items())])
    return summary, detail, requests, terminal


def verify_writer_trace(trace, uid, requests):
    meta = trace['sample_meta']
    require(meta['uid'] == uid, 'Trace UID mismatch')
    require(meta['session_mode'] == 'full', 'Incomplete session mode')
    require(meta['selected_session_indices'] == list(range(50)), 'Not all50 sessions selected')
    require(all(meta[k] is None for k in ('M_old', 'M_new', 'explanation', 'relevant_session_index')),
            'Gold fields present in CUPMem sample metadata')
    count = trace['completed_session_count']
    require(0 <= count <= 50 and [s['session_index'] for s in trace['session_logs']] == list(range(count)),
            'Session trace gaps')
    matched = 0
    for session in trace['session_logs']:
        candidates = []
        for req in requests.values():
            ctx = req['context']
            if ctx.get('uid') != uid or ctx.get('arm') != 'cupmem' or ctx['phase'] != 'ingest':
                continue
            try:
                payload = json.loads(req['body']['messages'][1]['content'])
            except (IndexError, ValueError):
                continue
            if isinstance(payload, dict) and {'session_id', 'user_turns', 'bucket_track_schema'} <= payload.keys():
                require(set(payload) == {'session_id', 'user_turns', 'bucket_track_schema'}, 'Unexpected writer fields')
                if payload['session_id'] == session['session_id']:
                    candidates.append(payload)
        require(candidates, 'No actual writer request for session')
        require(all(p['user_turns'] == session['user_turns'] for p in candidates), 'Writer source differs from trace')
        matched += 1
    return matched


def verify_judge_answers(request, query_logs, answers):
    """Check exact original judge task sections, keeping its gold prefix separate."""
    user = request['body']['messages'][1]['content']
    sections = []
    for i, name in enumerate(('Explicit Probing', 'Adversarial Robustness', 'Implicit Task'), 1):
        sections.append(f'[Dimension {i}: {name}]\nQuestion {i}: {query_logs[f"dim{i}_query"]["query_text"]}'
                        f'\nTarget Model Response {i}: {answers[f"dim{i}_response"]}')
    marker = '\n--------------------------------------------------\n'
    expected_suffix = marker.join(sections)
    # The pinned official function uses two newlines before every separator.
    expected_suffix = expected_suffix.replace(marker, '\n' + marker)
    prefix, separator, actual_suffix = user.partition('[Dimension 1: Explicit Probing]')
    require(separator and (separator + actual_suffix).rstrip('\n') == expected_suffix,
            'Judge question/target answer differs from this arm')
    return prefix


def verify_composer_output(request, response, query_log):
    payload = json.loads(request['body']['messages'][1]['content'])
    require(set(payload) == {'query', 'parsed_query', 'canonical_answer_grounding', 'premise_verdict',
                            'action_readiness_verdict', 'constraint_set'}, 'Not the native composer request')
    require(payload['query'] == query_log['query_text'], 'Composer question differs from trace')
    require(json.loads(response['body']['choices'][0]['message']['content']) == query_log['answer'],
            'Composer answer/rationale differs from saved trace')


def verify_case(item, selected, folder, requests, terminal):
    uid = selected['uid']
    trace = read(folder / (uid + '.cupmem.json'))
    direct = read(folder / (uid + '.direct.json'))
    require(item['answers'] == read(folder / (uid + '.answers.json')), 'Answer files disagree')
    require(item['judgments'] == read(folder / (uid + '.judgments.json')), 'Judgment files disagree')
    require(trace['input_sha256'] == selected['input_sha256'], 'Selected input hash differs')
    require(trace['completed_session_count'] == 50 and trace['completed_query_count'] == 3, 'Incomplete case')
    matched_writer_sessions = verify_writer_trace(trace, uid, requests)
    checks = trace['memory_immutability_checks']
    expected_checks = [(phase, f'dim{i}_query') for i in range(1, 4) for phase in ('query_start', 'query_complete')]
    require([(c['phase'], c['query']) for c in checks] == expected_checks, 'Missing query boundary checks')
    require({c['state_sha256'] for c in checks} == {state_hash(trace)}, 'Query-time memory changed')
    case_requests = {r: v for r, v in requests.items() if v['context'].get('uid') == uid}
    scores = []
    for i in range(1, 4):
        query, response = f'dim{i}_query', f'dim{i}_response'
        require(trace['query_logs'][query]['answer']['answer'] == item['answers']['cupmem'][response],
                'Native answer differs from saved answer')
        native_outputs = []
        for rid, req in case_requests.items():
            ctx = req['context']
            if ctx.get('arm') != 'cupmem' or ctx.get('query_label') != query:
                continue
            res = terminal[rid]
            if res['event'] != 'response' or res['status'] != 200:
                continue
            try:
                payload = json.loads(res['body']['choices'][0]['message']['content'])
                actual_input = json.loads(req['body']['messages'][1]['content'])
            except (KeyError, IndexError, ValueError):
                continue
            if isinstance(payload, dict) and 'answer' in payload and 'constraint_set' in actual_input:
                verify_composer_output(req, res, trace['query_logs'][query])
                native_outputs.append(rid)
        require(native_outputs, 'Missing raw native composer answer')
        require(direct['answers'][response] == item['answers']['direct'][response], 'Direct answers disagree')
        matching = [(r, q) for r, q in case_requests.items() if q['context'].get('arm') == 'direct'
                    and q['context'].get('query_label') == query and q['context']['phase'] == 'answer'
                    and terminal[r]['event'] == 'response' and terminal[r]['status'] == 200]
        require(matching, 'Missing actual direct call')
        rid, req = matching[-1]
        metadata = next(m for m in direct['request_metadata'] if m['query'] == query)
        require(digest(req['body']['messages']) == metadata['input_sha256'], 'Direct input hash mismatch')
        require(terminal[rid]['body']['choices'][0]['message']['content'] == direct['answers'][response],
                'Raw direct output mismatch')
    gold_prefixes = []
    for arm, judged in item['judgments'].items():
        matches = [(r, q) for r, q in case_requests.items() if q['context'].get('arm') == arm
                   and q['context']['phase'] == 'official_judge' and terminal[r]['event'] == 'response'
                   and terminal[r]['status'] == 200]
        require(matches, 'Missing physical judge response')
        rid, req = matches[-1]
        gold_prefixes.append(verify_judge_answers(req, trace['query_logs'], item['answers'][arm]))
        require(json.loads(terminal[rid]['body']['choices'][0]['message']['content']) == judged['ratings'],
                'Official ratings differ from raw judge output')
        passes = {f'dim{i}': judged['ratings'][f'dim{i}_eval']['pass'] for i in range(1, 4)}
        require(all(type(v) is bool for v in passes.values()), 'Malformed pass flag')
        scores.append(dict(arm=arm, passes=passes, passed=sum(passes.values()), total=3, judge_request_id=rid))
    require(len(set(gold_prefixes)) == 1, 'Judge arms received different gold context')
    return dict(uid=uid, type=selected['type'], sessions=50, queries=3,
                memory_boundary_checks=6, persistent_memory_sha256=state_hash(trace),
                actual_writer_sessions_verified=matched_writer_sessions, official_scores=scores,
                direct_truncation=direct['request_metadata'],
                semantic_correctness='Not established by artifact integrity; see separate source audit')


def verify(result_path, source, folder, ledger_path):
    result, config, ledger = read(result_path), read(source / 'config.json'), read(ledger_path)
    job = ledger['jobs'][result['source_version']]
    require(result['status'] == 'budget_stopped', 'This verifier is only for a budget-stopped pilot')
    require(result['error_type'] == 'BudgetStop', 'Unexpected terminal reason')
    require(str(job['job_id']) == str(result['job_id']), 'Wrong ledger job')
    require(job['state'] == 'FAILED' and job['exit_code'] == '1:0', 'Unexpected Slurm terminal state')
    require(result['config_sha256'] == sha(source / 'config.json'), 'Config hash mismatch')
    for name, expected in job['source_sha256'].items():
        require(sha(source / name) == expected, 'Frozen source changed: ' + name)
    require(sha(source / 'harness.tar.gz') == config['harness_archive_sha256'], 'Archive hash mismatch')
    with tarfile.open(source / 'harness.tar.gz') as archive:
        members = {m.name.removeprefix('./'): m for m in archive.getmembers() if m.isfile()}
        require(set(members) == set(config['harness_files']), 'Unexpected archive contents')
        for name, expected in config['harness_files'].items():
            require(hashlib.sha256(archive.extractfile(members[name]).read()).hexdigest() == expected,
                    'Archive member hash mismatch: ' + name)
    require(result['upstream_revision'] == REVISION and result['dataset_revision'] == DATA_REVISION
            and result['dataset_sha256'] == DATA_SHA256, 'Runtime provenance differs from pinned source/data')
    require(result['verified_upstream_files'] == 72 and result['type_counts'] == {'T1': 200, 'T2': 200},
            'Runtime data/source verification incomplete')
    require(result['conda_prefix'] == config['conda_prefix'] and
            Path(result['python']).parent == Path(config['conda_prefix']) / 'bin', 'Wrong runtime environment')
    require(result['selection'] == config['selection'], 'Selection changed')
    events = [json.loads(line) for line in (folder / 'http.jsonl').read_text().splitlines()]
    accounting, detail, requests, terminal = audit_events(events, config)
    require(accounting == result['accounting'], 'Physical audit disagrees with reported accounting')
    require(accounting['requests'] == config['limits']['requests'], 'Request cap was not exhausted')
    require(not accounting['censored_request_ids'], 'Length-censored output requires separate handling')
    selected = {r['uid']: r for r in config['selection']}
    completed = [verify_case(r, selected[r['uid']], folder, requests, terminal) for r in result['completed']]
    require(len({r['uid'] for r in completed}) == len(completed) < len(selected), 'Unexpected completion count')
    partials = []
    for uid in selected.keys() - {r['uid'] for r in completed}:
        partial = read(folder / (uid + '.cupmem.partial.json'))
        matched_sessions = verify_writer_trace(partial, uid, requests)
        partials.append(dict(uid=uid, completed_sessions=partial['completed_session_count'],
                             completed_queries=partial['completed_query_count'],
                             actual_writer_sessions_verified=matched_sessions,
                             label='Last persisted session boundary; later physical attempts count in audit'))
    files = [result_path, source / 'config.json', folder / 'http.jsonl']
    files += [folder / (r['uid'] + suffix) for r in completed
              for suffix in ('.cupmem.json', '.direct.json', '.answers.json', '.judgments.json')]
    files += [folder / (p['uid'] + '.cupmem.partial.json') for p in partials]
    return dict(status='audited_partial_not_completed', label='Alternate-model stopped pilot; not a benchmark score',
                job_id=result['job_id'], slurm_state=job['state'], exit_code=job['exit_code'],
                slurm_elapsed_seconds=job['elapsed_seconds'], program_elapsed_seconds=result['elapsed_seconds'],
                usage_records=job['usage'], accounting=accounting, http_audit=detail,
                complete_cases=completed, partial_cases=partials,
                source_archive_sha256=config['harness_archive_sha256'],
                dataset_verification='Pinned hash checked by executed runner on compute node; dataset not copied or rehashed locally',
                currency_cost='BAZE currency/credit debit unavailable; token usage is not a monetary bill',
                artifacts=[dict(path=str(p), sha256=sha(p)) for p in files])


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ('result', 'source', 'folder', 'ledger', 'output'):
        p.add_argument(name, type=Path)
    args = p.parse_args()
    report = verify(args.result, args.source, args.folder, args.ledger)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'job_id', 'accounting')}, indent=2))
