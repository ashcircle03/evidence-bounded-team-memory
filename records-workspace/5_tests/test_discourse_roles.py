import json

import pytest

from team_memory.records import discourse_roles


def test_single_target_membership_survives_overlapping_roles():
    source=dict(id='s',owner='owner',speaker='writer',location='lab',observed_at='2026-01-01T00:00:00Z',
                text='Rooms with green lamps use linen covers. Inspect the lock. Keep the door closed.')
    def row(role,text,group):
        return {role:text,role+'_attributes':dict(claim_group=group,stance='decision' if role=='claim' else 'unknown')}
    raw=json.dumps(dict(extractions=[row('claim','Rooms with green lamps use linen covers','a'),
        row('subject','Rooms with green lamps','a'),row('claim','Inspect the lock','b'),
        row('claim','Keep the door closed','b'),row('subject','the door','b')]))
    calls=[]
    def predict(pairs):
        calls.extend(pairs)
        return ['condition']*len(pairs)
    result=discourse_roles.construct(source,lambda *_:raw,predict,model='fixture')
    assert [p['index'] for p in calls]==[1]
    assert calls[0]['context']['start']==calls[0]['target']['start']
    graph=result['record_graph'];g,h=graph['claims']
    assert g['condition'] and not g['subject'] and h['subject'] and not h['condition']
    unchanged=discourse_roles.apply(source,raw,lambda pairs:['keep']*len(pairs),model='fixture')
    assert h==unchanged['claims'][1] and unchanged['units']==graph['units']
    with pytest.raises(ValueError,match='Invalid discourse role'):
        discourse_roles.apply(source,raw,lambda _:[],model='fixture')


def test_changed_role_reuses_alignment_and_units(monkeypatch):
    from langextract import resolver
    from team_memory.records import grouped, preserving
    from unittest.mock import patch

    text = 'Inspect the door because the hinge is loose.'
    src = dict(id='s', text=text, owner='owner', speaker='writer', location='lab',
               observed_at='2026-01-01T00:00:00Z')
    raw = json.dumps({'extractions': [
        {'claim': 'Inspect the door', 'claim_attributes': {'claim_group': 'a', 'stance': 'decision'}},
        {'condition': 'because the hinge is loose', 'condition_attributes': {'claim_group': 'a', 'stance': 'unknown'}},
    ]})
    aligned = []
    original = resolver.Resolver.align

    def count(self, extractions, *args, **kwargs):
        aligned.extend(e.extraction_text for e in extractions)
        return original(self, extractions, *args, **kwargs)

    monkeypatch.setattr(resolver.Resolver, 'align', count)
    with patch.object(grouped, 'partition_units', wraps=grouped.partition_units) as partition:
        record = preserving.construct(src, lambda *_: raw, model='test', predict=lambda _: ['basis'])
    assert aligned == ['Inspect the door', 'because the hinge is loose']
    partition.assert_called_once()
    claim = record['record_graph']['claims'][0]
    assert claim['condition'] == [] and claim['basis_annotations'][0]['kind'] == 'stated'
