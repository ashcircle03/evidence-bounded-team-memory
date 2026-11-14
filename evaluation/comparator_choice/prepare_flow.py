"""Replay observed comparator output into fixed8B QA; no labels are repaired."""
import json,sys
from .prepare import ROOT,HERE,prepare,write


QUESTIONS={
    'new-resume-reconsider':'Why was unattended Harbor ingestion postponed, and what does the new report change about that decision?',
    'new-edge-reconsider':'What blocked Atlas deployment to the field device, and what new evidence warrants reconsidering that deployment under its requirements?',
    'new-permit-reconsider':'Why were night-sky observations suspended, what is the scope of the new access permission, and have observations under it happened?',
    'new-consent-reconsider':'What part of the interview dataset could now be considered for external release, under what conditions, and what remains restricted?'}


def inputs_for(arm):
    original=json.loads((HERE/'compare-inputs.json').read_text());cases=[]
    for c in original['cases']:
        if c['id'] not in QUESTIONS:continue
        cases.append(dict(c,steps=[dict(label='pending-reason',operation='ask',question=QUESTIONS[c['id']]),
            dict(label='approve',operation='review_fixture',choice='approve'),dict(label='restart',operation='restart'),
            dict(label='approved-state',operation='ask',question='What has Alex approved, what remains established from the earlier report, and what would still need to be tested or decided?')]))
    if arm=='14b':
        known=json.loads((ROOT/'evaluation/service_completion/inputs.json').read_text())
        cases += [dict(c,split='known_regression') for c in known['streams']+known['transfer']]
        for c in known['legacy']:
            assert c['events'][0]['operation']=='import_history'
            cases.append(dict(id=c['id'],split='legacy',initial=c['events'][0]['records'],steps=c['events'][1:]))
    return dict(cases=cases)


def main(arm):
    folder=ROOT/'results/comparator-choice'/('compare-'+arm+'-v1')
    result=json.loads((folder/'result.json').read_text())
    assert result['status']=='complete'
    inputs=inputs_for(arm);ids={c['id'] for c in inputs['cases'] if 'incoming' in c}
    assert inputs==json.loads((HERE/('planned-flow-'+arm+'.json')).read_text())
    replays={r['case_id']:r for r in result['selectors'] if r['case_id'] in ids}
    assert set(replays)==ids
    prepare('flow-'+arm+'-v1','flow',inputs,replays=replays)


if __name__=='__main__':main(sys.argv[1])
