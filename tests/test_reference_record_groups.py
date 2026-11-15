"""Real LangExtract mechanics; examples/stubs do not measure model semantics."""
from copy import deepcopy
import json
import pytest
from team_memory.records.grouped import components,examples,compile_graph,construct
from team_memory.records.graph import linked_span,validate_graph,describe
from team_memory.adapters.records import RecordsAdapter
from team_memory.adapters.base import request
from team_memory.contracts.ports import CallContext
from team_memory.adapters.reader_bridge import evidence_from,witnesses_from


def source(text):
    return dict(id='test',owner='a',speaker='a',observed_at='2026-01-01T00:00:00Z',location='test:one',text=text)


def raw(rows):
    return json.dumps({'extractions':[{r:t,r+'_attributes':{'claim_group':g,'stance':stance}} for r,t,g,stance in rows]})


def test_reference_example_group_binding_and_exact_overlap():
    e=examples()[0];s=source(e.text);generator,_=components()
    graph=compile_graph(s,generator.format_handler.format_extraction_example(e.extractions))
    units={u['id']:u for u in graph['units']}
    first=graph['claims'][0];second=graph['claims'][1]
    assert '20 kg' in ' '.join(units[x]['quote'] for x in first['condition'])
    assert 'handles' in ' '.join(units[x]['quote'] for x in first['basis'])
    assert 'inspection' in ' '.join(units[x]['quote'] for x in second['condition'])
    assert first['condition']!=second['condition']
    validate_graph(s,graph)


def test_unavailable_quote_and_orphan_context_fail_without_source_loss():
    s=source('We defer launch.')
    for rows in [[('claim','We approve launch','a','decision')],[('basis','We defer launch','missing','unknown')]]:
        got=construct(s,lambda *_:raw(rows),model='stub')
        assert got['record_graph']['status']=='failed'
        assert got['text']==s['text'] and not got['record_graph']['claims']


def test_ambiguous_repeated_context_is_not_silently_first_matched():
    s=source('Only on Linux. Run A. Only on Linux. Run B.')
    with pytest.raises(ValueError,match='Ambiguous'):
        compile_graph(s,raw([('condition','Only on Linux','a','unknown'),('claim','Run B','a','decision')]))


def test_far_scope_and_within_claim_overlap_survive_store_and_reader_packet(tmp_path):
    text='For cold chambers only. '+'Unrelated archive note. '*8+'We defer the test because frost formed.'
    s=source(text)
    rows=[('condition','For cold chambers only','a','unknown'),('claim','We defer the test because frost formed','a','decision'),('basis','frost formed','a','unknown')]
    enriched=construct(s,lambda *_:raw(rows),model='stub')
    assert enriched['record_graph']['status']=='annotated'
    graph=deepcopy(enriched['record_graph']);ctx=CallContext('demo','a',frozenset(['records:write','records:read']))
    port=RecordsAdapter(tmp_path,'demo')
    result=port.handle(request('record.append',dict(source=enriched,expected_revision=0,idempotency_key='one'),workspace_id='demo',request_id='one'),context=ctx)
    assert result['status']=='ok',result
    snap=RecordsAdapter(tmp_path,'demo').snapshot();assert snap['sources'][0]['record_graph']==graph
    a=text.index('We defer');b=a+len('We defer the test')
    lo,hi=linked_span(enriched,a,b);assert lo==0
    evidence=evidence_from(dict(source_id='test',start=lo,end=hi,quote=text[lo:hi]),snap,1)
    bundle=dict(snapshot=snap,query=dict(text='test',time_scope='current',as_of=None,conditions=[]),evidence=[evidence],coverage='hits',unresolved_proposal_ids=[])
    witnesses=witnesses_from(bundle);assert witnesses[0]['record_context']['claims'][0]['condition']
    assert witnesses[0]['record_context']['claims'][0]['basis']
    assert describe(enriched,a,b)['claims']==[]  # no hidden out-of-packet context


def test_canonical_adapter_preserves_mixed_qualifiers_without_forcing_stance():
    from team_memory.records.grouped import construct_aligned
    s=source('We might retry next month. This is untested.')
    rows=[('claim','We might retry next month','a','proposal'),('claim','This is untested','a','observation')]
    old=construct(s,lambda *_:raw(rows),model='stub')
    new=construct_aligned(s,lambda *_:raw(rows),model='stub')
    assert old['record_graph']['status']=='failed'
    c=new['record_graph']['claims'][0]
    assert c['stance']=='unknown' and c['qualification']=='model_extracted_unverified'
    assert c['claim'] and len(c['claim'])==2
    validate_graph(s,new['record_graph'])


def test_canonical_adapter_uses_original_surface_not_normalized_model_text():
    from team_memory.records.grouped import construct_aligned
    s=source('In the afternoon, we may inspect the pipe.')
    rows=[('claim','we may inspect the pipe','a','proposal'),('time','in the afternoon','a','unknown')]
    new=construct_aligned(s,lambda *_:raw(rows),model='stub')
    assert new['record_graph']['status']=='annotated'
    units={u['id']:u for u in new['record_graph']['units']}
    assert units[new['record_graph']['claims'][0]['time'][0]]['quote']=='In the afternoon'
    bad=construct_aligned(s,lambda *_:raw([('claim','we approve the pipe','a','decision')]),model='stub')
    assert bad['record_graph']['status']=='failed'  # no fuzzy recovery of changed meaning


def test_canonical_adapter_does_not_assign_repeated_time_to_first_occurrence():
    from team_memory.records.grouped import construct_aligned
    s=source('Rain began at 14:00. The valve closed at 14:00.')
    rows=[('claim','The valve closed','a','observation'),('time','at 14:00','a','unknown')]
    new=construct_aligned(s,lambda *_:raw(rows),model='stub')
    assert new['record_graph']['status']=='failed'
    assert new['text']==s['text']  # no fabricated occurrence; unresolved raw source retained
