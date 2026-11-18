"""Author inputs/keys before inference; no model outputs used to set difficulty."""
import json
from pathlib import Path
from team_memory.adapters.legacy import public_source

# (role, source span); slots are focal linkage requirements, not hidden answers
# that a reader should reconstruct when their supporting text is omitted.
FAMILIES = [
 ('e01','easy','use liner K6', 'decision',('condition','chilled parcels'),('basis','the foam prevents condensation'),
  [('a','For {v}, '),('core','{v}'),('b',' because {v}'),('literal','.')]),
 ('e02','easy','close gate R8','decision',('time','on Thursday'),('basis','the hinge needs repair'),
  [('core','{v}'),('a',' {v}'),('b',' because {v}'),('literal','.')]),
 ('e03','easy','do not ship kit M3','decision',('condition','cracked containers'),('basis','the seal failed inspection'),
  [('a','For {v}, '),('core','{v}'),('b',' because {v}'),('literal','.')]),
 ('e04','easy','we might trial paint Q9','proposal',('condition','inland stations'),('claim','This trial is not approved.'),
  [('a','For {v}, '),('core','{v}'),('literal','.'),('b',' {v}')]),
 ('e05','easy','the sensor check is complete','observation',('time','on Tuesday'),('condition','firmware 6'),
  [('a','Recorded event time: {v}. '),('core','{v}'),('b',' for {v}'),('literal','.')]),
 ('e06','easy','I suspect relay P4 may last 80 days','uncertainty',('condition','dry rooms'),('claim','This estimate is untested.'),
  [('a','For {v}, '),('core','{v}'),('literal','.'),('b',' {v}')]),
 ('m01','medium','we postpone the gravel survey','decision',('condition','sector D2'),('basis','the access bridge is closed'),
  [('a','This survey decision applies to {v}. '),('literal','The cabinet label is copper. '),('core','{v}'),('b',' because {v}'),('literal','.')]),
 ('m02','medium','switch the beacon to standby','decision',('time','after the morning inspection'),('basis','the battery is leaking'),
  [('a','Timing for the following beacon instruction: {v}. '),('literal','The antenna colour remains white. '),('core','{v}'),('b',' because {v}'),('literal','.')]),
 ('m03','medium','do not release batch U5','decision',('condition','saline batches'),('basis','the residue test failed'),
  [('a','The following release instruction applies to {v}. '),('core','{v}'),('b',' because {v}'),('literal','. Freshwater batches remain eligible for release.')]),
 ('m04','medium','we could pilot filter J2','proposal',('condition','remote clinics'),('claim','This pilot is a suggestion, not an authorization.'),
  [('a','Scope of the filter pilot: {v}. '),('literal','The spare tubing is blue. '),('core','{v}'),('literal','.'),('b',' {v}')]),
 ('m05','medium','the valve calibration finished','observation',('time','on Friday afternoon'),('condition','bench T7'),
  [('a','The calibration event occurred {v}. '),('literal','The office clock was repaired. '),('core','{v}'),('b',' on {v}'),('literal','.')]),
 ('m06','medium','I suspect drive L4 may reach 70 cycles','uncertainty',('condition','under reduced load'),('claim','No measurement supports this estimate yet.'),
  [('a','Operating scope of this estimate: {v}. '),('literal','The procurement task is complete. '),('core','{v}'),('literal','.'),('b',' {v}')]),
 ('h01','hard','halt compressor Z4','decision',('condition','pressure above 9 bar'),('basis','its casing has fractured'),
  [('a','Scope of the compressor instruction: {v}. '),('noise',''),('core','{v}'),('b',' because {v}'),('literal','. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.')]),
 ('h02','hard','resume the compass test','decision',('time','at 14:20'),('basis','the replacement mount passed inspection'),
  [('a','The time of the compass instruction is {v}. '),('noise',''),('core','{v}'),('b',' because {v}'),('literal','. Independently, the camera check begins at 14:20 because its lens is clean.')]),
 ('h03','hard','do not publish the terrain map','decision',('condition','commercial reuse'),('basis','the licence excludes commercial distribution'),
  [('a','The map instruction below concerns {v}. '),('noise',''),('core','{v}'),('b',' because {v}'),('literal','. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.')]),
 ('h04','hard','we might trial pack G8','proposal',('condition','desert depots'),('claim','This proposed trial has no deployment approval.'),
  [('a','The pack trial applies to {v}. '),('noise',''),('core','{v}'),('literal','.'),('b',' {v}'),('literal',' Independently, the warehouse rollout is approved.')]),
 ('h05','hard','the pressure audit ended','observation',('time','at 16:40'),('condition','rig C9'),
  [('a','The pressure audit ended {v}. '),('b','The pressure audit concerns {v}. '),('noise',''),('core','{v}'),('literal','. Separately, the noise audit starts at 16:40 on rig B7.')]),
 ('h06','hard','I suspect coil N8 may handle 18 amperes','uncertainty',('condition','in nitrogen'),('claim','This capacity is conjectural and has not been measured.'),
  [('a','The coil estimate concerns operation {v}. '),('noise',''),('core','{v}'),('literal','.'),('b',' {v}'),('literal',' A separate steel cable was measured at 12 amperes in air.')]),
]
NOISE=' '.join(['The delivery folder contains a yellow form.','The stock counter remains seven.','The break room has two chairs.','The printer tray contains plain paper.']*2)+' '


def main():
    out=Path(__file__).parent;inputs=[];keys=[]
    for i,(fid,diff,core,stance,a,b,parts) in enumerate(FAMILIES):
        for j,availability in enumerate(['full','partial','none']):
            visible={'a','b'} if availability=='full' else ({'a'} if i%2==0 else {'b'}) if availability=='partial' else set()
            values={'core':core,'a':a[1],'b':b[1]};segments=[]
            for kind,template in parts:
                if kind=='noise':segments.append(NOISE)
                elif kind=='literal':segments.append(template)
                elif kind=='core' or kind in visible:segments.append(template.format(v=values[kind]))
            text=''.join(segments)
            source=public_source(dict(owner=f'author-{i+1}',observed_at='2026-02-01T09:00:00Z',source=dict(speaker=f'author-{i+1}',location='synthetic://records-strata/'+fid,text=text)))
            # No difficulty or availability tags in model-visible metadata.
            source['location']='synthetic://records-strata/'+source['id']
            # Recompute source ID after canonical metadata change.
            source=public_source(dict(owner=source['owner'],observed_at=source['observed_at'],source=dict(speaker=source['speaker'],location=source['location'],text=text)))
            iid=f'{fid}-{availability}';inputs.append(dict(id=iid,family=fid,panel='balanced_synthetic',difficulty=diff,availability=availability,source=source,arms=['simple','ours'] if (i+j)%2==0 else ['ours','simple']))
            slots=[dict(role=role,text=quote,available=tag in visible) for tag,(role,quote) in zip(['a','b'],[a,b])]
            forbidden=[]
            if fid=='h01':forbidden=['below 1 bar','the buffer is empty']
            if fid=='h03':forbidden=['classroom teaching','the teacher granted permission']
            if fid=='h04':forbidden=['the warehouse rollout is approved']
            if fid=='h05':forbidden=['rig B7']
            if fid=='h06':forbidden=['12 amperes','in air']
            keys.append(dict(id=iid,core=core,stance=stance,slots=slots,forbidden=forbidden,
                # Quoted group key can itself be an assertion, but does not count
                # as an extraction: only actual role rows are evaluated.
                allow_unspecified_basis=True))
    # Existing natural messages: an explicitly failure-selected secondary audit,
    # never pooled into the balanced synthetic matrix or independent-case count.
    old=json.loads(Path('evaluation/record_contract/inputs.json').read_text())['sources'][:14]
    natural=[
      ('has been completed','observation',[], 'medium','full'),
      ('are due today','observation',[('time','Thursday',True)],'medium','full'),
      ('recommendation report will be provided','proposal',[('time','early next week',True)],'medium','full'),
      ('I will start designing','proposal',[('time','Today',True),('subject','Bucket Policy and directory structure',True)],'medium','full'),
      ('has been uploaded to Confluence','observation',[],'medium','full'),
      ('proposal is approved','observation',[('subject','file storage solution',False)],'hard','partial'),
      ('feedback message should be consistent','decision',[('condition','regardless of whether the email entered by the user exists or not',True),('basis','user enumeration attacks',True)],'medium','full'),
      ('must be forcibly routed','decision',[('condition','ACCOUNT_STATUS_LOCKED',True)],'easy','full'),
      ('requiring explicit interruption','observation',[('condition','where an account is locked',True)],'medium','full'),
      ('will be halted','question',[('condition','after the backend triggers this strategy',True),('subject','ERR_POLICY_LOCKED_ACCOUNT_V1',False)],'hard','partial'),
      ('avoid sending users redundant or potentially confusing automated messages','observation',[('subject','downstream automated notifications',False)],'hard','partial'),
      ('start researching dynamic refresh solutions','proposal',[('time','afternoon',True)],'medium','full'),
      ('implemented using polling','decision',[('basis',"our message push service isn't fully ready yet",True)],'hard','full'),
      ('use the polling solution for now','decision',[('time','for now',True),('basis',"message push service isn't fully ready",False)],'hard','partial'),
    ]
    for i,(item,annotation) in enumerate(zip(old,natural)):
        core,stance,slots,diff,availability=annotation;iid=f'n{i+1:02}'
        inputs.append(dict(id=iid,family=item['case_id'],panel='natural_audit',difficulty=diff,availability=availability,source=item['source'],arms=['simple','ours'] if i%2==0 else ['ours','simple']))
        keys.append(dict(id=iid,core=core,stance=stance,slots=[dict(role=r,text=t,available=v) for r,t,v in slots],forbidden=['your understanding is completely correct'] if i==10 else [],allow_unspecified_basis=True))
    for key in keys:
        if key['id']=='n13':key['slots'][0]['optional']=True  # plausible implicit rationale; omission permitted
        if key['id']=='n06':key['acceptable_stances']=['decision','observation']
        if key['id'] in ('n03','n04','n12'):key['acceptable_stances']=['decision','proposal']
    for item,key in zip(inputs,keys):
        assert key['core'].casefold() in item['source']['text'].casefold(),item['id']
        for slot in key['slots']:
            if slot['available']:assert slot['text'].casefold() in item['source']['text'].casefold(),(item['id'],slot)
    (out/'inputs.json').write_text(json.dumps(dict(version='records-strata-v1',items=inputs),ensure_ascii=False,indent=2)+'\n')
    (out/'keys.json').write_text(json.dumps(dict(version='records-strata-v1',reviewer='implementation agent; pre-run authored, not independent annotation',items=keys),ensure_ascii=False,indent=2)+'\n')
    print('54 balanced synthetic inputs from18 families +14 natural messages from5 prior case groups;136 fresh calls')


if __name__=='__main__':main()
