import json
from copy import deepcopy
import pytest
from team_memory.records import pair_binding, preserving, graph
from evaluation.record_groups.evaluate import transport
from evaluation.record_binding.pair_rows import compiled_rows


def fixture():
    s=dict(id='source',owner='a',speaker='a',observed_at='2026-01-01T00:00:00Z',location='test',
        text='The drawer is empty. Keep the valve shut because the seal is cracked.')
    raw=json.dumps(dict(extractions=[
        dict(claim='The drawer is empty',claim_attributes=dict(claim_group='a',stance='observation')),
        dict(claim='Keep the valve shut',claim_attributes=dict(claim_group='a',stance='decision')),
        dict(claim='the seal is cracked',claim_attributes=dict(claim_group='b',stance='observation'))]))
    return s,raw


def predictions(s,raw):
    cat=pair_binding.catalog(s,raw);out={}
    for q in cat['queries']:
        out[q['context']['id']]=json.dumps({t['id']:'basis' if q['context']['quote']=='the seal is cracked' and t['quote']=='Keep the valve shut' else 'none' for t in q['targets']})
    return out


def test_target_identity_is_not_promoted_to_group_scope(tmp_path):
    s,raw=fixture();base=preserving.compile_graph(s,raw);g,t=pair_binding.bind(s,raw,predictions(s,raw),model='test')
    assert g['claims']==base['claims'] and g['units']==base['units'] and g['edges']==base['edges']
    assert len(g['context_bindings'])==1
    b=g['context_bindings'][0];assert s['text'][b['target_start']:b['target_end']]=='Keep the valve shut'
    enriched=dict(s,record_graph=g);view=compiled_rows(enriched)
    edge_rows=[r for r in view if r['group']==b['id']]
    assert [r['text'] for r in edge_rows if r['role']=='claim']==['Keep the valve shut']
    assert transport(enriched,tmp_path/'store')['stored_restarted']
    ctx=graph.describe(enriched,0,len(s['text']))
    assert ctx['context_bindings'][0]['target_quote']=='Keep the valve shut'
    assert ctx['context_bindings'][0]['context_quote']=='the seal is cracked'


def test_none_does_not_delete_or_rewrite_original_assertions():
    s,raw=fixture();cat=pair_binding.catalog(s,raw)
    out={q['context']['id']:json.dumps({t['id']:'none' for t in q['targets']}) for q in cat['queries']}
    g,t=pair_binding.bind(s,raw,out,model='test')
    assert not g['context_bindings']
    assert g['claims']==preserving.compile_graph(s,raw)['claims']


def test_invented_target_and_missing_response_are_explicit_failures():
    s,raw=fixture();out=predictions(s,raw);key=next(iter(out));out[key]='{"invented":"basis"}'
    g,t=pair_binding.bind(s,raw,out,model='test')
    assert g['status']=='partial' and t['rejected']
    graph.validate_graph(s,g)


def test_corrupt_binding_target_or_identity_cannot_be_stored():
    s,raw=fixture();g,_=pair_binding.bind(s,raw,predictions(s,raw),model='test')
    for name,value in [('target_start',0),('id','forged')]:
        bad=deepcopy(g);bad['context_bindings'][0][name]=value
        with pytest.raises(ValueError):graph.validate_graph(s,bad)


def test_one_context_can_explicitly_support_two_distinct_assertions():
    s,raw=fixture();cat=pair_binding.catalog(s,raw);out=predictions(s,raw)
    q=next(q for q in cat['queries'] if q['context']['quote']=='the seal is cracked')
    out[q['context']['id']]=json.dumps({t['id']:'basis' for t in q['targets']})
    g,_=pair_binding.bind(s,raw,out,model='test')
    assert len(g['context_bindings'])==2  # Shared source does not imply shared targets automatically.
