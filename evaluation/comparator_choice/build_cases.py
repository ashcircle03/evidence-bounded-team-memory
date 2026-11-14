"""New authored diagnostic panel; labels/required evidence stay outside actor inputs."""
import json
from pathlib import Path
from hashlib import sha256
from .prepare import ROOT,HERE,write


def main():
    cases=[];keys={}
    def add(cid,family,kind,old,new,old_required,new_required,explanation):
        def env(text,who,day):return dict(owner=who,observed_at=f'2026-07-{day:02d}T09:00:00Z',
            source=dict(speaker=who,location=f'authored-choice://{sha256(cid.encode()).hexdigest()[:16]}/{day}',text=text))
        cases.append(dict(id=cid,split='new_authored',initial=[env(old,'Alex',1)],incoming=env(new,'Blair',2)))
        keys[cid]=dict(family=family,kind=kind,old_required=old_required,new_required=new_required,reason=explanation)
    families=[
      ('resume',
       'We postponed unattended ingestion from the Harbor API because version2 cannot resume a download after a disconnected connection. Manual ingestion remains the plan.',
       'Harbor API version3 now provides continuation tokens for interrupted downloads. In a fault-injection test, the client resumed from the token after the connection was cut and completed the download.',
       'Our revised HTTP client reduces Harbor API version2 request latency by 18 percent. Version2 still cannot resume a download after a disconnected connection.',
       ['postponed','version2','cannot resume'],['version3','continuation tokens','connection was cut'],
       'New API version removes the interruption constraint; review unattended ingestion for version3, not rewrite version2 history.'),
      ('edge',
       'We rejected deployment of the Atlas classifier to the 8 GB field device because its original model requires 32 GB of memory. Deployment also requires at least 90 percent accuracy.',
       'The quantized Atlas model uses 6.2 GB on the same 8 GB field device. The held-out accuracy of that quantized model is 92 percent.',
       'The original Atlas classifier now processes images 25 percent faster on a 64 GB workstation. It still requires 32 GB of memory, and no model fitting the 8 GB field device was tested.',
       ['rejected','8 GB','32 GB','90 percent'],['quantized','6.2 GB','8 GB','92 percent'],
       'A distinct quantized model satisfies the original memory and accuracy constraints; original32GB remains a true observation.'),
      ('permit',
       'We suspended night-sky observations from the rooftop because the access permit allowed entry only between 08:00 and 18:00. The camera itself was operational.',
       'The amended rooftop permit allows entry between 22:00 and 02:00 for the next two weeks. No night-sky observation has been conducted under this amended permit yet.',
       'The camera now records sharper daylight images after a lens upgrade. Rooftop access is still restricted to 08:00 through 18:00.',
       ['suspended','08:00','18:00'],['22:00','02:00','two weeks'],
       'Time-limited new access permits reviewing the night-observation plan; approval is not evidence that observations succeeded.'),
      ('consent',
       'We withheld release of the 60-record interview dataset because the consent forms did not authorize sharing records with external researchers. The records remain stored internally.',
       'Participants for 24 of the 60 records have signed new consent permitting external noncommercial research use of those 24 records. Consent for the remaining 36 records has not changed.',
       'We renamed fields in all 60 interview records to make internal analysis easier. No participant has changed their consent, and external research sharing is still unauthorized.',
       ['withheld','60-record','did not authorize','external'],['24','noncommercial','36','not changed'],
       'Review a restricted24-record release, never infer permission for all60 or commercial use.')]
    for family,old,pos,neg,ow,nw,why in families:
        add('new-'+family+'-reconsider',family,'reconsider',old,pos,ow,nw,why)
        add('new-'+family+'-negative',family,'none',old,neg,ow,[],
            'The new report explicitly leaves the blocking premise unchanged; topic overlap or another improvement does not warrant a proposal.')
    corrections=[
      ('pressure','For pump Delta at test setting R, the recorded pressure is 70 kPa. The operator is Hana.',
       'I correct the earlier Delta test-setting-R pressure entry: the correct value is 75 kPa, not 70 kPa. The operator is still Hana.',
       ['Delta','R','70 kPa'],['correct','Delta','R','75 kPa']),
      ('deadline','The deadline for submitting the Cedar report is 15 August 2026. Its reviewer is Rina.',
       'I explicitly correct our earlier Cedar report deadline entry to 18 August 2026. Rina is still its reviewer.',
       ['Cedar','15 August 2026'],['correct','Cedar','18 August 2026']),
      ('capacity','The configured capacity of tank Vega is 120 liters. Its inspection owner is Min.',
       'I retract the 120-liter entry for tank Vega and correct its configured capacity to 150 liters. Min remains the inspection owner.',
       ['Vega','120 liters'],['retract','Vega','150 liters']),
      ('cooldown','The configured cooldown for instrument Lyra is 12 minutes. The operating mode is standard.',
       'I correct our previous Lyra standard-mode cooldown record: its configured cooldown is 15 minutes. The operating mode is unchanged.',
       ['Lyra','12 minutes'],['correct','Lyra','15 minutes'])]
    for cid,old,new,ow,nw in corrections:
        add('new-'+cid+'-correction',cid,'correction',old,new,ow,nw,
            'Explicit correction of the same fact; approval changes only that assertion, not the unchanged owner or other attributes.')
    coexist=[
      ('threads','For dataset D and build12, the parser processes 100 files per minute with one worker.',
       'For dataset D and build12, the parser processes 260 files per minute with four workers.',
       ['100','one worker'],['260','four workers']),
      ('altitude','The measured boiling point of water at the sea-level site was 100 degrees Celsius.',
       'The measured boiling point of water at the 3000-meter site was 90 degrees Celsius.',
       ['sea-level','100'],['3000-meter','90']),
      ('partition','On the validation split, classifier Nova achieved 94 percent accuracy.',
       'On the geographically separate test split, classifier Nova achieved 86 percent accuracy.',
       ['validation','94'],['test split','86']),
      ('lighting','The camera detector measured 0.91 recall on the daylight-image set.',
       'The camera detector measured 0.68 recall on the low-light-image set.',
       ['0.91','daylight'],['0.68','low-light'])]
    for cid,old,new,ow,nw in coexist:
        add('new-'+cid+'-coexist',cid,'coexist',old,new,ow,nw,
            'Different explicitly named conditions; retain both observations without an approval request.')
    conflicts=[
      ('checksum','For artifact Rho build9, I recorded the published checksum as aa731.',
       'For the same artifact Rho build9, I recorded the published checksum as bb842. I have not withdrawn either report.',
       ['Rho','build9','aa731'],['Rho','build9','bb842']),
      ('port','For service Kappa deployment D2, my configuration report lists the listening port as 8081.',
       'For the same service Kappa deployment D2, my configuration report lists the listening port as 8082. This is my independent report, not a retraction of the earlier report.',
       ['Kappa','D2','8081'],['Kappa','D2','8082']),
      ('checksum-count','For archive Sigma revision5, my report counts 420 records in the published archive.',
       'For that same archive Sigma revision5, my report counts 427 records in the published archive. The discrepancy has not been resolved.',
       ['Sigma','revision5','420'],['Sigma','revision5','427']),
      ('measurement','For sensor Tau in calibration run C8 at 20 degrees Celsius, I measured an offset of 0.4 volts.',
       'For the same sensor Tau in calibration run C8 at 20 degrees Celsius, I measured an offset of 0.7 volts. Neither measurement has been retracted.',
       ['Tau','C8','20 degrees','0.4'],['Tau','C8','20 degrees','0.7'])]
    for cid,old,new,ow,nw in conflicts:
        add('new-'+cid+'-conflict',cid,'conflict',old,new,ow,nw,
            'Same explicitly fixed subject and conditions, incompatible claims, no authorized correction; preserve unresolved reports.')
    assert len(cases)==20
    # Deterministic interleaving, not grouped labels or a key in the actor packet.
    cases.sort(key=lambda c:sha256(c['id'].encode()).hexdigest())
    known=json.loads((ROOT/'evaluation/service_completion/inputs.json').read_text())
    known_cases=[dict(id=c['id'],split='known_regression',initial=c['initial'],incoming=c['incoming']) for c in known['streams']+known['transfer']]
    write(HERE/'compare-inputs.json',dict(cases=cases+known_cases))
    write(HERE/'new-key.json',dict(scope='New authored20; four paired reconsider/negative families, not independent natural benchmark',cases=keys))
    write(HERE/'data-freeze.json',dict(files={n:sha256((HERE/n).read_bytes()).hexdigest() for n in ('compare-inputs.json','new-key.json','PROTOCOL.md')},
        production_sha256=json.loads((ROOT/'results/module-boundary/v1/freeze.json').read_text())['config']['code_sha256']))
    print('Frozen new20 + known11, evaluator key kept outside model packets.')


if __name__=='__main__':main()
