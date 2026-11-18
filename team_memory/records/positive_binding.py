"""Positive-only use of a learned binding proposal; absence is not refutation.

Keeps the original adapter as a replacement diagnostic. This adapter retains
unmentioned fields, adds positively predicted bindings, and changes a field's
role only when the same exact source interval is assigned to the other role
for that same assertion. No gold-based selection or cross-claim deletion.
"""
import json
from . import preserving, learned_binding


def bind(source, original_raw, prediction, *, model):
    baseline=preserving.compile_graph(source,original_raw,model=model)
    _,trace=learned_binding.bind(source,original_raw,prediction,model=model)
    if baseline['status']!='annotated' or trace['fallback']:
        return baseline,trace
    replacement=json.loads(trace['candidate_raw'])['extractions']
    groups=set(trace['changed_groups'])
    positive={}
    for row in replacement:
        role=next(r for r in ('claim','condition','basis','time','subject') if r in row)
        group=row[role+'_attributes']['claim_group']
        if role in ('condition','basis') and group in groups:
            span=preserving._aligned_span(source,row)
            positive.setdefault((group,span['start'],span['end']),{})[role]=row
    rows=[];seen=set();retyped=[]
    for row in json.loads(original_raw)['extractions']:
        role=next(r for r in ('claim','condition','basis','time','subject') if r in row)
        group=row[role+'_attributes']['claim_group']
        if role not in ('condition','basis'):
            rows.append(row);continue
        span=preserving._aligned_span(source,row);key=(group,span['start'],span['end'])
        if key in positive and role not in positive[key]:
            retyped.append(dict(group=group,old_role=role,new_roles=sorted(positive[key]),span=list(key[1:])))
            continue
        rows.append(row);seen.add((*key,role))
    added=[]
    for key,roles in positive.items():
        for role,row in roles.items():
            if (*key,role) not in seen:
                rows.append(row);seen.add((*key,role));added.append(dict(group=key[0],role=role,span=list(key[1:])))
    raw=json.dumps(dict(extractions=rows),ensure_ascii=False)
    candidate=preserving.compile_graph(source,raw,model=model+' + learned-positive-binding')
    trace.update(candidate_raw=raw,positive_additions=added,retyped=retyped,policy='positive_only')
    if candidate['status']!='annotated':
        trace.update(fallback=True,candidate_diagnostics=candidate['diagnostics']);return baseline,trace
    return candidate,trace
