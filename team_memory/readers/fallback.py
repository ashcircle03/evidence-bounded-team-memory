"""Stage-level fallback to the last answer (LangChain with_fallbacks pattern).

No retries or alternative provider. An optional enrichment cannot discard its
input answer; failure is visible, and cancellation/BaseException still propagates.
"""
from copy import deepcopy


def stage_failure(previous, stage, error_type):
    result=deepcopy(previous)
    failure=dict(stage=stage,error_type=error_type)
    if failure not in result.setdefault('stage_failures',[]):
        result['stage_failures'].append(failure)
    warning=f'{stage} incomplete ({error_type}); available answer and evidence preserved'
    result['warnings']=list(dict.fromkeys(result.get('warnings',[])+[warning]))
    result['status']='partial'
    result['pipeline_status']='degraded'
    return result


def carry_diagnostics(previous, candidate):
    """An enrichment cannot certify that an earlier failed stage succeeded."""
    result=deepcopy(candidate)
    result['warnings']=list(dict.fromkeys(previous.get('warnings',[])+result.get('warnings',[])))
    failures=deepcopy(previous.get('stage_failures',[]))
    for item in result.get('stage_failures',[]):
        if item not in failures:failures.append(item)
    if failures:result['stage_failures']=failures
    if previous.get('status') in ('partial','error') or failures:
        result['status']='partial'
        result['pipeline_status']='degraded'
    return result


def preserve_answer(previous, stage, operation):
    try:
        return operation()
    except Exception as exc:
        return stage_failure(previous,stage,type(exc).__name__)
