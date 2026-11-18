"""Source-authored record inventory. Never imports model outputs."""
import json,re
from pathlib import Path


def R(core,stance='observation',**roles):return dict(core=core,stances=stance.split('|'),**roles)

# Whole source inventories: every substantive assertion, instruction, rationale,
# qualification and method is assigned; conversational acknowledgements excluded.
NATURAL={
'n01':[
 R('the task "Verify the accuracy of alarm rule creation and trigger logic" for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed'),
 R('All test cases have passed',caveat=['including various single conditions, combined conditions, and boundary value scenarios']),
 R('The few issues discovered yesterday have also all been regression verified and passed',time=['yesterday']),
 R('The final test report has been uploaded to Confluence')],
'n02':[
 R('Today is Thursday',time=['Today','Thursday']),
 R('your medication check-in module and family member invitation interface are due today','observation|decision',time=['today','Thursday'],recipient=['@Hanqiang Liang and @Huihong Tian']),
 R('Please make sure to complete the delivery today','decision',time=['today','Thursday'],subject=['your medication check-in module and family member invitation interface']),
 R('Other colleagues, please also share your plans and progress for today','decision',time=['today','Thursday'])],
'n03':[
 R("today I'm starting a new design task: [Designing a File Storage Solution]",'decision|proposal',time=['today']),
 R('I will focus on comparing Azure Blob and AWS S3','decision|proposal',basis=['our system will need to store a large number of supporting documents, reports, etc. in the future']),
 R('The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack','decision|proposal'),
 R('A preliminary selection recommendation report will be provided early next week','decision|proposal',time=['early next week'])],
'n04':[
 R('I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday',time=['last Friday']),
 R('AWS S3 has a slight advantage',condition=['From the perspective of cost and ecosystem integration']),
 R('our other projects are also on AWS'),
 R('I will start designing the Bucket Policy and directory structure based on S3','decision|proposal',time=['Today'],method=['isolating by tenant and file type'],optional_basis=['AWS S3 has a slight advantage','our other projects are also on AWS'])],
'n05':[
 R('the complete technical design document (based on AWS S3) has been uploaded to Confluence'),
 R('It includes three main parts: bucket permission policies, lifecycle rules, and recommended directory structure',subject=['the complete technical design document (based on AWS S3)']),
 R('please review it','decision',subject=['the complete technical design document (based on AWS S3)'],recipient=['@Mingzhi Li Boss Li'])],
'n06':[
 R("I've finished reviewing the document on the file storage solution"),
 R('The design is very comprehensive',caveat=['especially the considerations for tenant data isolation and cost optimization']),
 R('The proposal is approved and can be finalized','decision|observation',subject=['the file storage solution'])],
'n07':[
 R('our main security consideration is to prevent "user enumeration attacks."',condition=['forgot password']),
 R('the feedback message should be consistent','decision',condition=['forgot password','regardless of whether the email entered by the user exists or not'],basis=['prevent "user enumeration attacks."'],method=['such as "If this email address is registered, you will receive an email containing a password reset link,"','instead of directly prompting "user does not exist."']),
 R('Please ensure the UI copy adheres to this principle','decision',subject=['the feedback message should be consistent'])],
'n08':[
 R('must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction','decision',condition=['all accounts marked as `ACCOUNT_STATUS_LOCKED`']),
 R('please assess the scope of impact on the backend','decision',recipient=['@Xinjie Li @Xuexin Yin'])],
'n09':[
 R('The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`',caveat=["defined as 'Explicit Status Alert Policy'"]),
 R('requiring explicit interruption of user operations and guidance to manual channels','observation|decision',condition=['where an account is locked'],subject=['`ERR_POLICY_LOCKED_ACCOUNT_V1`'])],
'n10':[
 R("I've reviewed the document"),
 R('This strategy will be handled by `ExplicitStateAlertModule`'),
 R('the parameter `halt_downstream_triggers` is set to `true`'),
 R('all downstream automated notifications (emails, SMS) will be halted','question',condition=['after the backend triggers this strategy'],caveat=['right?'])],
'n11':[R('your understanding is completely correct',unresolved=['Confirmed proposition is not contained in this source.']),R('This is to avoid sending users redundant or potentially confusing automated messages',unresolved=['Antecedent of This and your understanding is outside this source; no policy code or interrupted event can be invented.'])],
'n12':[
 R('The data structure looks very clear'),
 R('I plan to complete the static data integration this morning','proposal|decision',time=['this morning'],basis=['to ensure the charts render correctly']),
 R("I'll start researching dynamic refresh solutions",'proposal|decision',time=['In the afternoon']),
 R('initially considering WebSocket','proposal',condition=['if the backend supports it'])],
'n13':[
 R('WebSocket is the best solution','observation|decision'),
 R("our message push service isn't fully ready yet"),
 R('This task can be implemented using polling for now','proposal|decision',time=['for now'],method=['by requesting the interface every 10 seconds'],basis=['avoid blocking your current task'],optional_basis=["our message push service isn't fully ready yet"]),
 R('we can upgrade it uniformly','proposal',condition=['Once the WebSocket service is stable later'],time=['later'])],
'n14':[
 R("I'll use the polling solution for now",'decision|proposal',time=['for now'],unresolved=['The rationale for polling is absent from this message.']),
 R("I'll adjust the plan",'decision|proposal')],
}

# Semantically immaterial lead-ins may be absent in extracted spans. They are
# fixed from source grammar, not selected to match one arm's outputs.
STOP={'a','an','the','this','that','these','those','i','we','it','our','your','its','my','their','for','to','of','on','at','in','by','with','from','as','is','are','was','were','be','been','being','have','has','had','and','or','then','please','all','also','such','e','g'}
def tokens(s):return re.findall(r"[\w]+",s.casefold())
def anchors(s):return [t for t in tokens(s) if t not in STOP]

def intervals(text,quote):
    hits=list(re.finditer(re.escape(quote),text,re.I))
    if not hits:raise ValueError('Gold quote absent: '+quote)
    return [dict(start=m.start(),end=m.end(),quote=text[m.start():m.end()]) for m in hits]

def main():
    old=Path('evaluation/record_strata');inputs=json.loads((old/'inputs.json').read_text())['items'];oldkeys={x['id']:x for x in json.loads((old/'keys.json').read_text())['items']}
    from evaluation.record_strata.build import FAMILIES
    family={x[0]:x for x in FAMILIES};docs=[]
    for item in inputs:
        iid=item['id'];s=item['source'];text=s['text']
        if iid.startswith('n'):records=NATURAL[iid]
        else:
            fid=item['family'];key=oldkeys[iid];main=R(key['core'],key['stance'])
            for slot in key['slots']:
                if slot['available']:main.setdefault('caveat' if slot['role']=='claim' else slot['role'],[]).append(slot['text'])
            records=[main]
            extras={'m01':['The cabinet label is copper'],'m02':['The antenna colour remains white'],'m03':['Freshwater batches remain eligible for release'],'m04':['The spare tubing is blue'],'m05':['The office clock was repaired'],'m06':['The procurement task is complete']}
            records += [R(t) for t in extras.get(fid,[])]
            if fid.startswith('h'):records += [R(t) for t in ('The delivery folder contains a yellow form','The stock counter remains seven','The break room has two chairs','The printer tray contains plain paper')]
            extra={
             'h01':R('start pump B2','decision',condition=['below 1 bar'],basis=['the buffer is empty']),
             'h02':R('the camera check begins','observation',time=['at 14:20'],basis=['its lens is clean']),
             'h03':R('publish the sketch','decision',condition=['for classroom teaching'],basis=['the teacher granted permission']),
             'h04':R('the warehouse rollout is approved','observation|decision'),
             'h05':R('the noise audit starts','observation',time=['at 16:40'],condition=['on rig B7']),
             'h06':R('A separate steel cable was measured at 12 amperes','observation',condition=['in air'])}
            if fid in extra:records.append(extra[fid])
        nodes=[];edges=[];optional_edges=[];rs=[]
        for j,record in enumerate(records):
            rid=f'r{j+1}';entry=dict(id=rid,core=rid+':claim',unresolved=record.get('unresolved',[]));rs.append(entry)
            for role,quotes in [('claim',[record['core']])]+[(role,record.get(role,[])) for role in ('condition','basis','time','subject','recipient','caveat','method','optional_basis')]:
                for k,q in enumerate(quotes):
                    # Natural spelling is retained; article/preposition variants use
                    # common material-token anchors plus strict provenance separately.
                    spans=intervals(text,q);nid=f'{rid}:{role}'+('' if role=='claim' else str(k+1));optional=role=='optional_basis';kind='basis' if optional else role
                    # Repeated timestamps are source occurrences, not interchangeable
                    # evidence. Foil time uses last occurrence; main time uses first.
                    if item['family'] in ('h02','h05') and role=='time':spans=[spans[0] if j==0 else spans[-1]]
                    node=dict(id=nid,record_id=rid,role=kind,text=q,anchors=anchors(q),spans=spans,required=not optional)
                    if role=='claim':node['stances']=record['stances']
                    elif role=='caveat':node['stances']=['observation','uncertainty','question'] if q=='right?' else ['observation','uncertainty']
                    if not node['anchors']:raise ValueError((iid,q,'empty anchors'))
                    nodes.append(node)
                    if role!='claim':(optional_edges if optional else edges).append([rid,kind,nid])
        # Each source has its own provenance contract; speaker is not @recipient.
        docs.append(dict(id=iid,panel=item['panel'],difficulty=item['difficulty'],availability=item['availability'],source_sha256=__import__('hashlib').sha256(text.encode()).hexdigest(),source={k:s[k] for k in ('id','owner','speaker','observed_at','location')},records=rs,nodes=nodes,edges=edges,optional_edges=optional_edges,label_note='n06 full-document subject corrected; original secondary stratum retained only as historical label' if iid=='n06' else None))
    out=Path('evaluation/record_full');(out/'gold.json').write_text(json.dumps(dict(version='records-full-v1',annotation='source-authored by implementation agent; no independent human adjudicator; known development outputs previously observed',documents=docs),ensure_ascii=False,indent=2)+'\n')
    print(len(docs),'documents',sum(len(d['records']) for d in docs),'records',sum(len(d['nodes']) for d in docs),'nodes',sum(len(d['edges']) for d in docs),'required edges')
if __name__=='__main__':main()
