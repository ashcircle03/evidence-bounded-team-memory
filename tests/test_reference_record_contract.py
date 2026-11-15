"""Qualified reasons and overlapping roles survive the actual module boundary."""
from copy import deepcopy
import pytest
from team_memory.records import grouped
from team_memory.records.graph import validate_graph,describe
from evaluation.record_groups.evaluate import transport


def example_source(example):
    return dict(id='example',owner='author',speaker='author',observed_at='2026-01-01T00:00:00Z',location='example',text=example.text)


def extract(example):
    gen,_=grouped.components(grouped.CONTRACT_DESCRIPTION,grouped.contract_examples())
    raw=gen.format_handler.format_extraction_example(example.extractions)
    return grouped.construct_contract(example_source(example),lambda *_:raw,model='stub')


def test_actual_reference_preflight_matches_overlapping_runtime_contract():
    r=grouped.validate_contract_examples()
    assert len(r['independent_exact_rows'])==17
    assert all(x['exact'] for x in r['independent_exact_rows'])
    assert r['sequential_reference_report']['issues']  # disclosed, not silently ignored


def test_duplicate_roles_and_shared_basis_survive_storage_and_reader(tmp_path):
    s=extract(grouped.contract_examples()[0]);g=s['record_graph'];a,b=g['claims']
    assert g['version']=='records.graph/v2' and a['condition']==a['subject']
    assert a['basis']==b['basis'] and all(x['kind']=='stated' for c in (a,b) for x in c['basis_annotations'])
    assert transport(s,tmp_path)['claim_packets']==2
    d=describe(s,0,len(s['text']));assert all(c['basis_annotations'] for c in d['claims'])


def test_inferred_reason_cannot_silently_become_stated(tmp_path):
    s=extract(grouped.contract_examples()[1]);g=s['record_graph'];c=next(c for c in g['claims'] if c['basis'])
    assert all(a['kind']=='inferred' for a in c['basis_annotations'])
    assert transport(s,tmp_path)['claim_packets']==3
    bad=deepcopy(g);next(c for c in bad['claims'] if c['basis'])['basis_annotations'][0]['kind']='stated'
    with pytest.raises(ValueError,match='identity'):validate_graph(s,bad)
    missing=deepcopy(g);next(c for c in missing['claims'] if c['basis'])['basis_annotations']=[]
    with pytest.raises(ValueError,match='qualification'):validate_graph(s,missing)


def test_missing_kind_stays_unspecified_for_control():
    s=example_source(grouped.contract_examples()[0]);raw='{"extractions":[{"claim":"must remain unplugged","claim_attributes":{"claim_group":"a","stance":"decision"}},{"basis":"the inlet is wet","basis_attributes":{"claim_group":"a","stance":"unknown"}}]}'
    got=grouped.construct_contract(s,lambda *_:raw,model='stub',revised_input=False)
    assert got['record_graph']['claims'][0]['basis_annotations'][0]['kind']=='unspecified'
