"""Mechanical audit of the connected run; semantic scoring remains separate."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from team_memory.store import source_envelope, digest
from team_memory.timeline import valid_witness


def verify(result, calls, inputs, freeze):
    expected = {digest(source_envelope(s)): source_envelope(s) for s in inputs['sources']}
    checks = {
        'program_complete': result.get('status') == 'complete',
        'input_hash_matches': result.get('input_sha256') == freeze['input_sha256'],
        'source_hashes_match': result.get('code_sha256') == freeze['code_sha256'],
        'connected_run_not_saved_selection_replay': result.get('full_pipeline_rerun') is True,
        'source_preservation': result.get('sources_preserved') == expected,
        'runtime_ready': result.get('derived_runtime_ready') is True,
        'duplicate_no_extra_calls': result.get('duplicate_no_extra_calls') is True,
        'physical_call_count': result.get('calls') == len(calls),
        'physical_call_ids': sorted(c['id'] for c in calls) == list(range(len(calls))),
        'no_external_provider': result.get('external_model_api_calls') == 0,
        'all_local_actor': all(c['request']['model'] == 'Qwen3-8B' for c in calls),
    }
    statuses, citations, invalid_citations, errors, warnings = {}, 0, [], [], []
    approved = set()
    for step in result['steps']:
        row = step['result']; label = step['label']; statuses[label] = row['status']
        common = {'schema_version', 'operation', 'status', 'answers', 'proposals', 'warnings', 'errors'}
        if not common <= row.keys() or row['schema_version'] != 'team-memory-service/v1':
            errors.append(dict(label=label, reason='response_contract'))
        for answer in row['answers']:
            if not answer['text'].strip() or not answer['evidence']:
                errors.append(dict(label=label, reason='empty_answer_or_support'))
            for witness in answer['evidence']:
                citations += 1
                if not valid_witness(witness, expected):
                    invalid_citations.append(dict(label=label, witness=witness))
        for p in row['proposals']:
            for w in [p['previous'], p['incoming'], *[w for v in p.get('support', {}).values() for w in v]]:
                if not valid_witness(w, expected):
                    invalid_citations.append(dict(label=label, witness=w))
            if p['reviewer'] != expected[p['previous']['source_id']]['owner']:
                errors.append(dict(label=label, reason='wrong_reviewer'))
            if row['operation'] == 'review':
                request = step['request']
                if request['actor'] != p['reviewer'] or request['proposal_id'] != p['id']:
                    errors.append(dict(label=label, reason='unbound_approval'))
                if request['choice'] == 'approve': approved.add(p['id'])
            elif p['status'] == 'approved' and p['id'] not in approved:
                errors.append(dict(label=label, reason='approval_without_owner_action'))
        warnings.extend(dict(label=label, warning=w) for w in row['warnings'])
    checks['citation_offsets_and_roles'] = not invalid_citations
    checks['response_and_approval_contract'] = not errors
    mandatory = {'initial_report', 'changed_condition', 'duplicate_report', 'unrelated_report'}
    mandatory |= {'before_review/'+q['id'] for q in inputs['questions']}
    mandatory |= {'after_review/'+q['id'] for q in inputs['questions'][:2]}
    checks['all_required_operations_present'] = mandatory <= statuses.keys()
    checks['no_operation_failed'] = all(s in ('ok', 'partial', 'insufficient') for s in statuses.values())
    future_leaks = []
    for call in calls:
        content = json.dumps(call['request'], ensure_ascii=False)
        if call['operation'] not in ('unrelated_report', 'after_review/runtimes', 'after_review/folder'):
            if inputs['sources'][2]['source']['text'] in content:
                future_leaks.append(call['id'])
    checks['no_future_unrelated_report_in_earlier_requests'] = not future_leaks
    finishes = [choice.get('finish_reason') for c in calls for choice in c.get('response', {}).get('choices', [])]
    checks['no_length_censored_response'] = 'length' not in finishes
    return dict(mechanical_checks_pass=all(checks.values()), checks=checks, statuses=statuses,
                citation_count=citations, invalid_citations=invalid_citations, contract_errors=errors,
                warnings=warnings, future_leaks=future_leaks,
                semantic_accuracy='Not measured by this verifier; inspect per-question outputs against service-expected.json')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('result', type=Path)
    parser.add_argument('calls', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    freeze = json.loads((here/'service-freeze.json').read_text())
    raw = (here/'service-inputs.json').read_bytes()
    assert sha256(raw).hexdigest() == freeze['input_sha256']
    assert sha256((here/'service-expected.json').read_bytes()).hexdigest() == freeze['expected_sha256']
    report = verify(json.loads(args.result.read_text()),
                    [json.loads(line) for line in args.calls.read_text().splitlines()], json.loads(raw), freeze)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(0 if report['mechanical_checks_pass'] else 1)


if __name__ == '__main__': main()
