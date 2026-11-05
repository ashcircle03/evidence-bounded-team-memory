"""Verify physical model evidence and state contracts; never infer semantic success."""
from hashlib import sha256
import json
from pathlib import Path

from team_memory.store import digest, source_envelope
from team_memory.timeline import valid_witness


def verify(result, calls, inputs, freeze):
    checks = dict(program_complete=result.get('status')=='complete',
        input_sha=result.get('input_sha256')==freeze['input_sha256'],
        runtime_sha=result.get('code_sha256')==freeze['code_sha256'],
        full_pipeline=result.get('full_pipeline_rerun') is True,
        local_only=result.get('external_model_api_calls')==0,
        call_count=result.get('calls')==len(calls),
        call_ids=sorted(c['id'] for c in calls)==list(range(len(calls))),
        model=all(c['request']['model']=='Qwen3-8B' for c in calls),
        physical_success=all('error_type' not in c and c.get('response',{}).get('choices') and all(ch.get('finish_reason')=='stop'
            for ch in c['response'].get('choices',[])) for c in calls))
    expected = {(c['id'],arm) for c in inputs['cases'] for arm in ('simple','cupmem')}
    actual = [(r['case_id'],r['arm']) for r in result['rows']]
    checks['exact_case_arm_set'] = len(actual)==len(expected) and set(actual)==expected
    casebook = {c['id']:c for c in inputs['cases']}
    errors, citation_count, bindings, qa_calls = [], 0, [], []
    for row in result['rows']:
        case = casebook[row['case_id']]; visible, approved = {}, set()
        if not row.get('complete') or not row.get('sources_preserved') or not row.get('runtime_ready'):
            errors.append(dict(case=row['case_id'],arm=row['arm'],reason='unfinished_or_changed_state'))
        if [s['request'] for s in row['steps']] != case['events']:
            errors.append(dict(case=row['case_id'],arm=row['arm'],reason='event_order_or_input_mismatch'))
        for ordinal, step in enumerate(row['steps']):
            event, response = step['request'], step['result']
            label = dict(case_id=row['case_id'], arm=row['arm'], event=ordinal, label=step['label'])
            scoped = [c for c in calls if c['context']==label]
            if len(scoped)!=step['calls']:
                errors.append(dict(**label, reason='physical_call_binding'))
            if event['operation']=='review_reconsider':
                if not response.get('simulated_owner_review') or len(response['requests'])!=len(response['results']):
                    errors.append(dict(**label,reason='invalid_review_script'))
                for request,reviewed in zip(response['requests'],response['results']):
                    if reviewed['status']!='ok':
                        errors.append(dict(**label,reason='owner_review_failed')); continue
                    for p in reviewed['proposals']:
                        owner = visible.get(p['previous']['source_id'],{}).get('owner')
                        if request['actor']!=owner or p['reviewer']!=owner or request['proposal_id']!=p['id'] or p['status']!='approved':
                            errors.append(dict(**label,reason='unbound_owner_review'))
                        else: approved.add(p['id'])
                if scoped: errors.append(dict(**label,reason='review_performed_inference'))
                continue
            records = event.get('records', [event['source']] if 'source' in event else [])
            for raw in records:
                env = source_envelope(raw); visible[digest(env)] = env
            if response.get('status') not in ('ok','partial','insufficient'):
                errors.append(dict(**label,reason='operation_failed',status=response.get('status')))
            if not {'schema_version','operation','status','answers','proposals','warnings','errors'} <= response.keys():
                errors.append(dict(**label,reason='missing_response_contract'))
                continue
            witnesses = []
            for answer in response['answers']:
                witnesses.extend(answer['evidence']); citation_count += len(answer['evidence'])
                if not answer['text'].strip() or not answer['evidence']:
                    errors.append(dict(**label,reason='empty_answer'))
            for p in response['proposals']:
                witnesses.extend([p['previous'],p['incoming']])
                witnesses.extend(w for group in p.get('support',{}).values() for w in group)
                witnesses.extend(w for group in p.get('selected_evidence',{}).values() for w in group)
                if p['reviewer']!=visible[p['previous']['source_id']]['owner']:
                    errors.append(dict(**label,reason='wrong_reviewer'))
                if p['status']=='approved' and p['id'] not in approved:
                    errors.append(dict(**label,reason='unapproved_promotion'))
            if any(not valid_witness(w, visible) for w in witnesses):
                errors.append(dict(**label,reason='invalid_original_witness'))
            raw = response.get('raw') or response.get('raw_review')
            if response.get('replayed'):
                if scoped: errors.append(dict(**label,reason='duplicate_inference'))
                continue
            traces = response.get('review_traces', [])
            if traces and any(p['previous']['source_id'] not in {t['previous_source_id'] for t in traces}
                              for p in response['proposals']):
                errors.append(dict(**label,reason='proposal_without_pair_review'))
            outputs = traces or ([dict(raw=raw)] if raw is not None else [])
            for trace in outputs:
                matched = []
                for call in scoped:
                    if not any(ch.get('message',{}).get('content')==trace['raw']
                               for ch in call.get('response',{}).get('choices',[])):
                        continue
                    try: body = json.loads(call['request']['messages'][-1]['content'])
                    except (ValueError,KeyError,TypeError): continue
                    if 'previous_source_id' in trace:
                        if {p['source_id'] for p in body.get('earlier',[])} != {trace['previous_source_id']}:
                            continue
                        if {p['source_id'] for p in body.get('incoming',[])} != {trace['incoming_source_id']}:
                            continue
                        if trace['incoming_source_id'] != digest(source_envelope(event['source'])):
                            errors.append(dict(**label,reason='pair_changed_incoming'))
                    matched.append(call)
                if len(matched)!=1:
                    errors.append(dict(**label,reason='unbound_model_output')); continue
                call = matched[0]; payload = json.loads(call['request']['messages'][-1]['content'])
                parts = payload.get('passages',payload.get('earlier',[])+payload.get('incoming',[]))
                if any(not valid_witness(p,visible) for p in parts):
                    errors.append(dict(**label,reason='future_or_fabricated_input_passage'))
                by_id = {p['id']:p for p in parts}
                selected = [w for w in witnesses if 'id' in w]
                if 'previous_source_id' in trace:
                    selected = [w for w in selected if w['source_id'] in
                                (trace['previous_source_id'],trace['incoming_source_id'])]
                if any(w['id'] not in by_id or any(w.get(k)!=by_id[w['id']].get(k)
                    for k in ('source_id','quote','start','end','owner','speaker','location')) for w in selected):
                    errors.append(dict(**label,reason='witness_not_in_actual_input'))
                if event['operation']=='ask':
                    if payload.get('question')!=event['question'] or payload.get('temporal_scope')!=event.get('temporal_scope','current'):
                        errors.append(dict(**label,reason='question_or_scope_changed'))
                    qa_calls.append(dict(**label,calls=step['calls'],seconds=step['seconds'],
                        input_sha256=sha256(json.dumps(call['request'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()))
                bindings.append(dict(**label,physical_call_id=call['id'],passage_ids=list(by_id)))
        if set(visible)!=set(row.get('actual_source_ids',[])):
            errors.append(dict(case_id=row['case_id'],arm=row['arm'],reason='source_coverage'))
        for p in row.get('final_proposals',[]):
            if p['status']=='approved' and p['id'] not in approved:
                errors.append(dict(case_id=row['case_id'],arm=row['arm'],reason='final_unapproved_promotion'))
    checks['contracts_and_actual_evidence'] = not errors
    return dict(mechanical_checks_pass=all(checks.values()),checks=checks,errors=errors,
                qa_citation_instances=citation_count,qa_calls=qa_calls,bindings=bindings,
                semantic_accuracy='Requires the separate predeclared key and original-source manual scoring')


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('result',type=Path);p.add_argument('calls',type=Path)
    p.add_argument('inputs',type=Path);p.add_argument('freeze',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();f=json.loads(a.freeze.read_text());blob=a.inputs.read_bytes()
    assert sha256(blob).hexdigest()==f['input_sha256']
    report=verify(json.loads(a.result.read_text()),[json.loads(x) for x in a.calls.read_text().splitlines()],json.loads(blob),f)
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('mechanical_checks_pass','checks','errors','qa_citation_instances')},ensure_ascii=False))
    raise SystemExit(0 if report['mechanical_checks_pass'] else 1)
