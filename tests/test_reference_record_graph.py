"""Graph transmission tests; stub selectors are not semantic model evaluation."""
from copy import deepcopy
import json
from pathlib import Path
import pytest
import unittest
from tests import test_reference_module_adapters as flow
from team_memory.records.graph import construct,validate_graph,linked_span


def selected(*_):
    return json.dumps({'claims':[dict(claim=[1],condition=[0],basis=[0],time=[],subject=[],stance='decision')]})


class RecordGraphFlowTests(unittest.TestCase):
    setUp=flow.ModuleFlowTests.setUp
    compare=flow.ModuleFlowTests.compare
    respond=flow.ModuleFlowTests.respond
    make=flow.ModuleFlowTests.make
    call=flow.ModuleFlowTests.call
    source=flow.ModuleFlowTests.source
    ask=flow.ModuleFlowTests.ask
    def test_graph_survives_save_restart_compare_retrieve_answer(self):
        from team_memory.adapters.runtime import connect_v2
        from team_memory.readers.attribution import AttributedQA
        root=Path(self.temp.name)/'graph'
        builder=lambda source:construct(source,selected,model='test-stub')
        g=connect_v2(root,workspace_id='demo',reader_factory=lambda s:AttributedQA(s,**self.options),
                     generate=self.compare,record_builder=builder)
        old=self.source('Because version 4 only permits one writer. Keep one writer. Archive is Orion.')
        first=self.call(g,'gateway.ingest',dict(source=old,expected_revision=0,idempotency_key='old'))
        self.assertEqual(first['status'],'ok',first)
        graph=g.records.snapshot()['sources'][0]['record_graph']
        self.assertEqual(graph['status'],'annotated')
        # Immutable raw source and all claim links survive restart.
        g=connect_v2(root,workspace_id='demo',reader_factory=lambda s:AttributedQA(s,**self.options),generate=self.compare)
        self.assertEqual(g.records.snapshot()['sources'][0]['record_graph'],graph)
        new=self.source('Version 5 permits four writers. Retry the test.','jun','test:new')
        self.call(g,'gateway.ingest',dict(source=new,expected_revision=1,idempotency_key='new'))
        self.assertIn('record_graph',self.compare_calls[-1])
        answered=self.ask(g,'What is the archive?')
        self.assertIn(answered['status'],('ok','partial'),answered)
        self.assertTrue(any('record_context' in str(c['messages']) and 'model_extracted_unverified' in str(c['messages']) for c in self.calls))
        self.assertTrue(any('Because version 4' in e['quote'] for e in answered['data']['bundle']['evidence']))
        snapshot=answered['data']['bundle']['snapshot']
        self.assertEqual(snapshot['proposals'][0]['status'],'pending')
        pid=snapshot['proposals'][0]['id']
        reviewed=self.call(g,'gateway.review',dict(proposal_id=pid,choice='approve',expected_revision=snapshot['revision'],idempotency_key='review'))
        self.assertEqual(reviewed['status'],'ok',reviewed)
        approved=self.ask(g,'Was review approved?')
        self.assertEqual(approved['data']['bundle']['snapshot']['proposals'][0]['effect'],'authorize_reconsideration')
        self.assertIn('not replaced',str(approved['data']['answer']))

    def test_extraction_failure_retains_source_and_is_not_successful_empty(self):
        g=self.make(Path(self.temp.name)/'failed-graph')
        def bad(*_):return 'not json'
        g.record_builder=lambda source:construct(source,bad,model='test-stub')
        source=self.source('Archive is Orion.')
        result=self.call(g,'gateway.ingest',dict(source=source,expected_revision=0,idempotency_key='a'))
        self.assertEqual(result['status'],'partial',result)
        self.assertEqual(g.records.snapshot()['sources'][0]['text'],source['text'])
        self.assertEqual(g.records.snapshot()['sources'][0]['record_graph']['status'],'failed')

    def test_expansion_keeps_far_condition_and_repeated_quote_offsets(self):
        s=self.source('Only with version 4. '+'Nothing changes here. '*8+'We defer the test. Archive is Orion.')
        from team_memory.records.graph import sentence_units
        units=sentence_units(s);target=next(u['index'] for u in units if u['quote']=='We defer the test.')
        def model(*_):return json.dumps({'claims':[dict(claim=[target],condition=[0],basis=[],time=[],subject=[],stance='decision')]})
        source=construct(s,model,model='test-stub')
        unit=source['record_graph']['units'][target]
        a,b=linked_span(source,unit['start'],unit['end'])
        self.assertIn('Only with version 4.',source['text'][a:b])
        same=[u for u in source['record_graph']['units'] if u['quote']=='Nothing changes here.']
        self.assertEqual(len({u['id'] for u in same}),8)
        for u in same:self.assertEqual(source['text'][u['start']:u['end']],u['quote'])

    def test_graph_cannot_claim_approval_or_change_evidence(self):
        s=construct(self.source('Version 4. Keep one writer.'),selected,model='test-stub')
        bad=deepcopy(s);bad['record_graph']['claims'][0]['qualification']='approved'
        with pytest.raises(ValueError):validate_graph(bad,bad['record_graph'])
        bad=deepcopy(s);bad['record_graph']['units'][0]['quote']='Version 5.'
        with pytest.raises(ValueError):validate_graph(bad,bad['record_graph'])
        bad=deepcopy(s);bad['record_graph']['edges'][0]['target']='missing'
        with pytest.raises(ValueError):validate_graph(bad,bad['record_graph'])

    def test_valid_quote_ids_do_not_prove_semantic_role_correctness(self):
        source=self.source('Version 4 permits only one writer. We defer the experiment. Archive is Orion.')
        def wrong(*_):return json.dumps({'claims':[dict(claim=[1],condition=[2],basis=[],time=[],subject=[],stance='decision')]})
        record=construct(source,wrong,model='test-stub')
        # Structural validation deliberately cannot certify an unrelated archive
        # as the experiment's condition. The independent requirement catches it.
        validate_graph(record,record['record_graph'])
        from evaluation.record_graph.analyze import role_coverage
        rows=role_coverage(record,[dict(claim='We defer the experiment.',condition=['Version 4 permits only one writer.'])])
        self.assertFalse(rows[0]['required_links_present'])
