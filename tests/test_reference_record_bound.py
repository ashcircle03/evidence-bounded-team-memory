import json
from copy import deepcopy
import pytest
from team_memory.adapters.legacy import public_source
from team_memory.records import bound,graph
from evaluation.record_groups.evaluate import transport

def source(text):return public_source(dict(owner='jo',observed_at='2026-01-01T00:00:00Z',source=dict(speaker='jo',location='test://bound',text=text)))
def record(root,**kw):return dict(root=root,details=kw.get('details',[]),condition=kw.get('condition',[]),basis=kw.get('basis',[]),time=kw.get('time',[]),subject=kw.get('subject',[]))
def span(segment,quote,**kw):return dict(segment=segment,quote=quote,**kw)
def compile(s,records,ignored=[]):return dict(s,record_graph=bound.compile_graph(s,json.dumps(dict(records=records,ignored=ignored))))

def test_examples_align_and_store(tmp_path):
    for i,e in enumerate(bound.examples()):
        s=source(' '.join(x['text'] for x in e['segments']))
        # IDs in examples follow explicit supplied segments; Punkt may join
        # semicolon clauses, but our examples deliberately remain sentences.
        assert [x['text'] for x in bound.segments(s)]==[x['text'] for x in e['segments']]
        got=compile(s,e['output']['records'],e['output']['ignored'])
        assert got['record_graph']['status']=='annotated'
        transport(got,tmp_path/str(i))

def test_repeated_quote_selects_segment(tmp_path):
    s=source('The motor stopped at noon. The lamp started at noon.')
    g=compile(s,[record(span(0,'The motor stopped',stance='observation'),time=[span(0,'at noon')]),record(span(1,'The lamp started',stance='observation'),time=[span(1,'at noon')])])
    by={u['id']:u for u in g['record_graph']['units']}
    times=[by[c['time'][0]]['start'] for c in g['record_graph']['claims']]
    assert times[0]!=times[1]
    transport(g,tmp_path)

def test_partial_keeps_valid_claim_and_valid_context(tmp_path):
    s=source('Stop the machine because the door is open. The room is cold.')
    g=compile(s,[record(span(0,'Stop the machine',stance='decision'),basis=[span(0,'the door is open',kind='stated')],time=[span(0,'tomorrow')]),record(span(1,'The room is cold',stance='observation'))])
    assert g['record_graph']['status']=='partial' and len(g['record_graph']['claims'])==2
    assert g['record_graph']['claims'][0]['basis']
    assert not g['record_graph']['claims'][0]['time'] and g['record_graph']['diagnostics']
    transport(g,tmp_path)

def test_bad_root_does_not_move_context():
    s=source('The room is cold. Keep the window closed.')
    g=compile(s,[record(span(0,'The room is hot',stance='observation'),condition=[span(0,'cold')]),record(span(1,'Keep the window closed',stance='decision'))])
    assert len(g['record_graph']['claims'])==1 and not g['record_graph']['claims'][0]['condition']

def test_stances_survive_and_are_validated(tmp_path):
    s=source('We could test the device; approval is pending.')
    got=compile(s,[record(span(0,'We could test the device',stance='proposal'),details=[span(0,'approval is pending',stance='observation',kind='qualification')])])
    c=got['record_graph']['claims'][0]
    assert [a['stance'] for a in c['assertions']]==['proposal','observation']
    transport(got,tmp_path)
    bad=deepcopy(got);bad['record_graph']['claims'][0]['assertions'][0]['unit_ids']=[]
    with pytest.raises(ValueError):graph.validate_graph(bad,bad['record_graph'])

def test_no_fuzzy_or_wrong_segment_repair():
    s=source('The valve is open. The hatch is closed.')
    got=compile(s,[record(span(1,'The valve is open',stance='observation')),record(span(0,'The valve is closed',stance='observation'))])
    assert got['record_graph']['status']=='failed' and not got['record_graph']['claims']
    assert got['text']==s['text']

def test_ignored_original_retained(tmp_path):
    s=source('Hello! The shipment arrived.')
    got=compile(s,[record(span(1,'The shipment arrived',stance='observation'))],[span(0,'Hello!',kind='salutation')])
    assert got['record_graph']['excluded'][0]['quote']=='Hello!' and got['text']==s['text']
    transport(got,tmp_path)
