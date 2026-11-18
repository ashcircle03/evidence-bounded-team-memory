import json
from team_memory.records import discourse_scope

def test_scope_ingest_masks_unseen_overlap_without_removing_source_context():
    source=dict(id='s',owner='owner',speaker='writer',location='lab',observed_at='2026-01-01T00:00:00Z',
                text='First log entry. Students with permits can enter the hall. Store the trays because the shelf is full. End of log.')
    def row(role,text,group):
        return {role:text,role+'_attributes':dict(claim_group=group,stance='decision' if role=='claim' else 'unknown')}
    raw=json.dumps(dict(extractions=[row('claim','Students with permits can enter the hall','a'),
        row('condition','Students with permits','a'),row('claim','Store the trays','b'),
        row('condition','because the shelf is full','b')]))
    seen=[]
    def predict(pairs):
        seen.extend(pairs)
        return ['basis']*len(pairs)
    doc=discourse_scope.construct(source,lambda *_:raw,predict,{'disjoint':10},model='fixture')
    assert doc['text']==source['text']
    assert seen[0]['context']['sentence']=='Students with permits can enter the hall.'
    assert seen[1]['target']['sentence']=='Store the trays because the shelf is full.'
    a,b=doc['record_graph']['claims']
    assert a['condition'] and not a['basis']
    assert b['basis'] and not b['condition']
