"""Audit deliverables and failed acceptance gates separately; no model calls."""
import gzip
from hashlib import sha256
import json

from .prepare import ROOT, HERE, write
from .score import OUT, LEGACY, TRANSFER
from .verify import verify


def read(path):
    return json.loads(path.read_text())


def audit():
    summary=read(OUT/'summary.json')
    decision=read(OUT/'decision.json')
    ledger=read(OUT/'goal-accounting.json')
    checks={}; artifacts=[]
    runtime=read(HERE/'final-runtime-freeze.json')
    data=read(HERE/'final-data-freeze.json')
    checks['runtime_prompt_protocol_hashes_unchanged']=all(sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in runtime['files_sha256'].items())
    checks['final_data_hashes_unchanged']=all(sha256((HERE/p).read_bytes()).hexdigest()==h for p,h in data['files_sha256'].items())
    checks['all_recorded_jobs_terminal']=all(j['state'] in ('COMPLETED','FAILED','TIMEOUT','OUT_OF_MEMORY','CANCELLED') for j in ledger['jobs'].values())
    checks['all_allocations_include_gpu']=all(j['gpus']>=1 for j in ledger['jobs'].values())
    checks['actual_gpu_budget']=sum(j['gpus']*j['elapsed_seconds']/60 for j in ledger['jobs'].values())<=ledger['goal_budget']['gpu_minutes']==240
    checks['unique_job_ids']=len({j['job_id'] for j in ledger['jobs'].values()})==len(ledger['jobs'])
    policy=read(OUT/'execution-policy-audit.json')
    checks['packaged_slurm_policy_and_source_hashes']=all(j['slurm_gpu_conda_no_requeue_no_node_pin'] and all(j['source_hashes_match'].values()) for j in policy['jobs']) and len(policy['jobs'])==len(ledger['jobs'])
    final_rows=[]
    for name in LEGACY+TRANSFER:
        folder=OUT/name
        manifest=read(folder/'artifact-manifest.json')
        hashes=all(sha256((folder/p).read_bytes()).hexdigest()==h for p,h in manifest['files_sha256'].items())
        inputs_path=ROOT/manifest['expected_input'];inputs=read(inputs_path)
        freeze=read(HERE/(manifest['source_version']+'-freeze.json'))
        result=json.loads(gzip.decompress((folder/'run.json.gz').read_bytes()))
        calls=[json.loads(s) for s in gzip.decompress((folder/'calls.jsonl.gz').read_bytes()).splitlines()]
        checked=verify(result,calls,inputs,freeze)
        checks[name+'/artifact_hashes']=hashes
        checks[name+'/input_sha']=sha256(inputs_path.read_bytes()).hexdigest()==manifest['actual_input_sha256']==result['input_sha256']
        checks[name+'/verification_reproduced']=checked==read(folder/'verification.json')
        accounting=read(folder/'accounting.json')
        checks[name+'/accounting_matches_export']=accounting==ledger['jobs'][manifest['source_version']]
        cards=read(folder/'cards.json');ratings=read(folder/'ratings.json')
        checks[name+'/all_semantic_ratings_have_reasons']=set(cards['cards'])==set(ratings['ratings']) and all(v.get('reason') for v in ratings['ratings'].values())
        checks[name+'/local_model_only']=checked['checks']['local_only'] and checked['checks']['model']
        artifacts.append(dict(name=name,job_id=manifest['job_id'],slurm_state=manifest['slurm_state'],
            program_complete=checked['checks']['program_complete'],mechanical_checks_pass=checked['mechanical_checks_pass'],
            error_reasons=sorted({e['reason'] for e in checked['errors']}),
            independent_semantic_validation=False))
        final_rows.extend(result['rows'])
    scored=read(OUT/'scored-cases.json')
    checks['all_20_legacy_questions_both_arms_accounted']=len(scored['legacy'])==40 and all(r['card']['status']!='not_executed' for r in scored['legacy'])
    checks['all_20_transfer_streams_both_arms_accounted']=len(scored['transfer'])==80 and all(r['card']['status']!='not_executed' for r in scored['transfer'])
    checks['old_failed_attempt_retained']=read(OUT/'legacy-pep-v1/accounting.json')['state']=='FAILED'
    checks['interrupted_native_capture_disclosed']=read(OUT/'legacy-pep-v1/native-capture.json')['gzip_complete'] is False
    checks['continuation_disclosed']=(HERE/'legacy-pep-continuation.json').is_file()
    checks['development_real_model_verified']=read(OUT/'dev-v2/verification.json')['mechanical_checks_pass']
    cli=read(OUT/'cli-smoke-v1/verification.json')
    checks['headless_cli_actual_model_verified']=cli['slurm']=='COMPLETED/0:0' and cli['program_complete'] and all(cli['checks'].values())
    tests=read(OUT/'tests.json')
    checks['local_tests_pass']=tests['exit_code']==0 and tests['passed']==223 and tests['skipped']==0 and sha256((OUT/'tests.log').read_bytes()).hexdigest()==tests['log_sha256']
    exported=read(OUT/'export-verification.json')
    checks['public_only_reproduction']=exported['score_reproduced'] and exported['audit_reproduced'] and exported['unit_tests']['exit_code']==0 and sha256((OUT/'export-tests.log').read_bytes()).hexdigest()==exported['unit_tests']['log_sha256']
    checks['required_artifacts_exist']=all((ROOT/p).is_file() for p in (
        'team_memory/cupmem_practical.py','team_memory/cupmem_candidates.py',
        'docs/cupmem-practical-v2.md','docs/practical-usage.md',
        'examples/practical_service.py','examples/practical_requests.jsonl',
        'results/cupmem/practical/README.md','results/cupmem/practical/cases.md',
        'results/cupmem/practical/decision.json','results/cupmem/practical/summary.json'))
    checks['rejection_matches_failed_acceptance']=not summary['gates']['candidate_adoption'] and not decision['candidate_adopted']
    mechanical_errors=[e for name in LEGACY+TRANSFER for e in read(OUT/name/'verification.json')['errors']]
    checks['no_observed_fabricated_or_future_witnesses']=not any(e['reason'] in ('invalid_original_witness','future_or_fabricated_input_passage','witness_not_in_actual_input') for e in mechanical_errors)
    checks['no_observed_unauthorized_promotions']=not any(e['reason'] in ('unapproved_promotion','final_unapproved_promotion','wrong_reviewer','unbound_owner_review') for e in mechanical_errors)
    requirements=[
        dict(requirement='Executable original-input service, module responsibilities, design rationale, and headless example',status='delivered',evidence=['docs/cupmem-practical-v2.md','docs/practical-usage.md','results/cupmem/practical/cli-smoke-v1/verification.json']),
        dict(requirement='Development QA5 and unrelated intake',status='met_on_known_development_only',evidence=['results/cupmem/practical/dev-v2/ratings.json','results/cupmem/practical/dev-v2/verification.json']),
        dict(requirement='Legacy20 same-model comparison and zero lost fully correct+cited items',status='measured_gate_met_with_low_absolute_quality',evidence=['results/cupmem/practical/summary.json','results/cupmem/practical/scored-cases.json'],caveat='7/20 both; content-only correct falls12 to9, native failure blocks10 candidate QA.'),
        dict(requirement='New20 frozen streams, reconsideration>=8/10 and no unnecessary negatives',status='evaluated_not_met_candidate_rejected',evidence=['evaluation/cupmem/practical/final-data-freeze.json','results/cupmem/practical/summary.json'],caveat='0/10 supported;9/10 valid negatives;20 controlled streams from10 independent reports.'),
        dict(requirement='Exact original citations and no unapproved promotion',status='met_for_observed_returned_outputs',evidence=['results/cupmem/practical/summary.json','results/cupmem/practical/dev-v2/verification.json'],caveat='416/416 literal witness instances; semantic correctness is separately poor. Caller authenticates owner identity.'),
        dict(requirement='QA call reduction>=50% while quality holds',status='invocation_reduction_met_quality_condition_not_met',evidence=['results/cupmem/practical/summary.json'],caveat='One call per invoked QA;10 blocked QA are reported separately. All ingestion/failed-call/GPU cost retained.'),
        dict(requirement='Preserve differently conditioned observations, decision vs correction vs approval, unrelated QA',status='implemented_and_development_verified_general_acceptance_not_met',evidence=['results/cupmem/practical/dev-v2/ratings.json','results/cupmem/practical/scored-cases.json','tests/test_cupmem_practical.py'],caveat='A valid state machine does not establish model semantic competence.'),
        dict(requirement='Frozen final evaluation once; choose retained/deferred design on failure',status='delivered',evidence=['results/cupmem/practical/decision.json','results/cupmem/practical/README.md','evaluation/cupmem/practical/legacy-pep-continuation.json']),
        dict(requirement='Slurm GPU/conda, budget, job identity and source preservation; no paid APIs',status='recorded_and_verified_for_this_campaign',evidence=['results/cupmem/practical/goal-accounting.json','evaluation/cupmem/dispatch.py','results/cupmem/practical/summary.json'])]
    result=dict(deliverable_audit_pass=all(checks.values()),performance_acceptance_pass=False,
        completion_scope='The explicit implementation + fixed evaluation + adoption-decision scope is delivered, using the objective\'s rejection-on-failure branch. The broader research solution and performance targets are not achieved.',
        checks=checks,requirements=requirements,executions=artifacts,
        remaining_within_this_goal=[],future_work_not_claimed_complete=['Long-document input budgeting','Semantically sufficient evidence selection','Reliable reconsideration reasoning','Original-source QA independent of native-write failure'])
    write(OUT/'completion-audit.json',result)
    assert result['deliverable_audit_pass'],{k:v for k,v in checks.items() if not v}
    return result


if __name__=='__main__':
    report=audit()
    print(json.dumps(dict(deliverable_audit_pass=report['deliverable_audit_pass'],performance_acceptance_pass=report['performance_acceptance_pass'],checks=len(report['checks'])),indent=2))
