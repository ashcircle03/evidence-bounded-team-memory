"""Assemble complete scoring cards, including missing/blocked operations.

This module does not judge semantic correctness. Human/agent source inspection
must provide explicit ratings; an absent output is never a correct abstention.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from team_memory.store import digest, source_envelope
from .prepare import write


def build(inputs, key, result, calls):
    rows={(r['case_id'],r['arm']):r for r in result.get('rows',[])}
    cards, mapping, cost = {}, {}, []
    legacy='original_case_count' in key
    for case in inputs['cases']:
        visible={}
        for event in case['events']:
            for raw in event.get('records',[event['source']] if 'source' in event else []):
                env=source_envelope(raw);visible[digest(env)]=env
        for arm in ('simple','cupmem'):
            row=rows.get((case['id'],arm),{})
            steps={s['label']:s for s in row.get('steps',[])}
            for event in case['events']:
                if event['operation'] not in ('ask','ingest'):continue
                label=event['label'];step=steps.get(label,{})
                value=step.get('result',{})
                cid=sha256((case['id']+'|'+arm+'|'+label).encode()).hexdigest()[:16]
                mapping[cid]=dict(case_id=case['id'],arm=arm,label=label,
                                  operation=event['operation'])
                context=dict(case_id=case['id'],arm=arm,label=label)
                scoped=[c for c in calls if all(c['context'].get(k)==v for k,v in context.items())]
                card=dict(question=event.get('question'),status=value.get('status','not_executed'),kind=value.get('kind'),
                    errors=value.get('errors',[]),warnings=value.get('warnings',[]),
                    answers=value.get('answers',[]),proposals=value.get('proposals',[]),
                    raw=value.get('raw'),raw_review=value.get('raw_review'),
                    review_traces=value.get('review_traces',[]),
                    physically_executed=bool(scoped),physical_call_ids=[c['id'] for c in scoped])
                if event['operation']=='ask':
                    expected=key['cases'][case['id']]['questions'][label] if legacy else key['cases'][case['id']]['qa']
                    card['expected']=expected
                    locations=set()
                    for side in expected.get('expected_sides',[]):
                        locations.update(side.get('locations',[side['location']] if 'location' in side else []))
                    if 'evidence' in expected:locations.add(expected['evidence']['location'])
                    for answer in value.get('answers',[]):
                        locations.update(w['location'] for w in answer['evidence'])
                    card['source_records']={sid:env for sid,env in visible.items() if env['source']['location'] in locations}
                else:
                    card.update(expected=key['cases'][case['id']],source_records=visible)
                cards[cid]=card
            for step in row.get('steps',[]):
                scoped=[c for c in calls if c['context'].get('case_id')==case['id'] and c['context'].get('arm')==arm
                        and c['context'].get('label')==step['label']]
                cost.append(dict(case_id=case['id'],arm=arm,label=step['label'],operation=step['request']['operation'],
                    status=step['result'].get('status'),calls=step['calls'],seconds=step['seconds'],
                    prompt_tokens=sum(c.get('response',{}).get('usage',{}).get('prompt_tokens',0) or 0 for c in scoped),
                    completion_tokens=sum(c.get('response',{}).get('usage',{}).get('completion_tokens',0) or 0 for c in scoped),
                    calls_missing_usage=sum(not c.get('response',{}).get('usage') for c in scoped)))
    # Unfinished imports may have consumed calls but never produced a step.
    assigned={(c['case_id'],c['arm'],c['label']) for c in cost}
    unassigned=[c for c in calls if tuple(c['context'].get(k) for k in ('case_id','arm','label')) not in assigned]
    return dict(cards=cards,mapping=mapping,operation_costs=cost,
        unfinished_operation_calls=len(unassigned),unfinished_operation_call_ids=[c['id'] for c in unassigned],
        all_physical_calls=len(calls),program_status=result.get('status'),
        rating_fields=dict(qa=['answer_correct','citations_support_answer','unsupported_extra_claims','reason'],
            review=['supported_reconsideration','unnecessary_proposals','wrong_target_or_kind','reason']),
        rule='Status/schema/citation offsets alone never establish semantic success; not_executed and needs_rebuild fail service acceptance.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('inputs',type=Path);p.add_argument('key',type=Path)
    p.add_argument('result',type=Path);p.add_argument('calls',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args()
    value=build(json.loads(a.inputs.read_text()),json.loads(a.key.read_text()),json.loads(a.result.read_text()),
                [json.loads(s) for s in a.calls.read_text().splitlines()])
    write(a.output,value)
    print(json.dumps(dict(cards=len(value['cards']),calls=value['all_physical_calls'],
                         unfinished_calls=value['unfinished_operation_calls'],program_status=value['program_status'])))
