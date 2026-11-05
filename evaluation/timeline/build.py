"""Development sequences and source-backed natural QA selection; keys stay local."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from team_memory.store import source_envelope, digest

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).parent


def write(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def envelope(text, location, owner, at):
    return source_envelope(dict(owner=owner,observed_at=at,source=dict(text=text,location=location,speaker=owner)))


def make_stream(uid, kind, natural, old, new, old_value, new_value, old_condition, new_condition,
                question, before_question, other_question, other_value, noise):
    start=datetime.fromisoformat(natural['envelope']['observed_at'])+timedelta(days=1)
    actor='Scenario author '+uid
    def env(text,i,who=actor):return envelope(text,f'scenario://timeline/{uid}/{i}',who,(start+timedelta(hours=i)).isoformat())
    original=env(old,1);distractor=env(noise,2,'Scenario colleague '+uid)
    incoming=env(new,3,actor if kind=='correction' else 'Scenario observer '+uid)
    docs=[natural['envelope'],original,distractor,incoming]
    old_id,new_id=digest(original),digest(incoming)
    def answer(sid,value,condition='',status='reported'):return dict(source_id=sid,aliases=[value],condition=condition,status=status)
    before=[answer(old_id,old_value,old_condition)]
    if kind in ('reconsider','coexist'):
        after=[answer(old_id,old_value,old_condition),answer(new_id,new_value,new_condition)]
        after_kind='conditional'
    elif kind in ('conflict','correction'):
        after=[answer(old_id,old_value,old_condition),answer(new_id,new_value,new_condition,'pending_correction' if kind=='correction' else 'reported')]
        after_kind='conflict'
    else:after=before;after_kind='single'
    final=[answer(new_id,new_value,new_condition,'approved_correction')] if kind=='correction' else after
    natural_key=dict(kind='single',answers=[answer(digest(docs[0]),natural['answer'])])
    keys={
       'natural_before':natural_key,'old_before':dict(kind='single',answers=before),
       'changed':dict(kind=after_kind,answers=after),'natural_after':natural_key,
       'reviewed':dict(kind='single' if kind=='correction' else after_kind,answers=final),
       'other_preserved':dict(kind='single',answers=[answer(old_id,other_value)])}
    steps=[dict(op='ingest',source=docs[0]),dict(op='ask',id='natural_before',question=natural['question']),
           dict(op='ingest',source=original),dict(op='ask',id='old_before',question=before_question),
           dict(op='ingest',source=distractor),dict(op='ingest',source=incoming),
           dict(op='ask',id='changed',question=question),dict(op='ask',id='natural_after',question=natural['question'])]
    if kind in ('reconsider','conflict','correction'):
        steps.append(dict(op='review',actor=actor,choice='approve',kind=kind,previous=old_id,incoming=new_id,
                          old_contains=old_value if kind!='reconsider' else '',new_contains=new_value))
    steps += [dict(op='ask',id='reviewed',question=question),dict(op='ask',id='other_preserved',question=other_question)]
    key=dict(kind=kind,old=old_id,new=new_id,expected_review=kind in ('reconsider','conflict','correction'),
             expected_relation=None if kind=='irrelevant' else kind,qa=keys,
             old_text=old,new_text=new,source_kind='synthetic workflow plus separate natural QA',natural_id=natural['id'])
    return dict(id=uid,steps=steps),key


def development():
    rows=[];keys={}
    for i,kind in enumerate(('reconsider','coexist','conflict','correction','irrelevant')):
        uid=f'dev-{i+1}';name=['Cedar','Birch','Maple','Pine','Oak'][i]
        natural=dict(id=uid+'-natural',answer='Orion',question='Where is the build artifact archive?',
                     envelope=envelope('The build artifact archive is Orion. No deployment decision was made in this note.',f'scenario://development/{uid}/natural','Build operator','2025-01-01T09:00:00Z'))
        other=f'The audit folder is {name}-audit.'
        if kind=='reconsider':
            old=f'The single-process {name} exporter took 40 seconds per batch. We suspended further {name} trials because deployment permits only one process. '+other
            new=f'Deployment now permits four processes. The four-process {name} exporter took 12 seconds per batch. The old single-process measurement remains unchanged.'
            a,b='single-process','four-process';q=f'What batch runtimes were measured for the {name} exporter under each process configuration?'
            before=f'What was the single-process batch runtime for the {name} exporter?';v,w='40 seconds','12 seconds'
        elif kind=='coexist':
            old=f'With the small-fixture input, {name} parsing took 40 seconds. '+other
            new=f'With the wide-fixture input, {name} parsing took 12 seconds. These observations concern different inputs; neither log retracts the other.'
            a,b='small-fixture','wide-fixture';q=f'What parsing times were recorded for {name} under the different fixture inputs?'
            before=f'What parsing time was recorded for {name} with the small-fixture input?';v,w='40 seconds','12 seconds'
        elif kind in ('conflict','correction'):
            old=f'Under release R7 settings, the {name} queue limit is 40 items. '+other
            new=(f'I correct my earlier R7 {name} queue-limit note: I transposed the count. Under the same release R7 settings, the limit is 12 items.' if kind=='correction' else f'My independent reading under the same release R7 settings gives the {name} queue limit as 12 items. We have not resolved the disagreement with the earlier report.')
            a=b='release R7';q=f'What is currently supported about the {name} queue limit under release R7, including any unresolved or pending report?'
            before=f'What {name} queue limit was reported for release R7?';v,w='40 items','12 items'
        else:
            old=f'The {name} batch limit is 40 items. We postponed {name} transport rollout because failover retries have not been validated. '+other
            new=f'The {name} user guide now has 12 pages after a heading cleanup. No transport run or failover test was performed.'
            a=b='';q=before=f'What batch limit was reported for {name}?';v,w='40 items','12 pages'
        row,key=make_stream(uid,kind,natural,old,new,v,w,a,b,q,before,f'Where is the audit folder for {name}?',name+'-audit',f'The {name} meeting minutes now use larger headings. This is a formatting update only.')
        rows.append(row);keys[uid]=key
    write(HERE/'development.json',rows);write(HERE/'development-key.json',keys)


if __name__=='__main__':development()
