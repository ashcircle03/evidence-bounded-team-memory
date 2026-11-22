"""Gold graphs here exercise transport only. They never enter inference datasets."""
import unittest
from copy import deepcopy

from team_memory.adapters.reader_bridge import evidence_from
from team_memory.records.graph import construct


class ClaimTransport(unittest.TestCase):
    def setUp(self):
        import json
        text = 'SEL. Score rose. CONF. Score fell.'
        self.source = construct(dict(id='report', text=text, owner='team', speaker='team',
            observed_at='2026-01-01T00:00:00Z', location='log'), lambda *_: json.dumps({'claims': [
            dict(claim=[i+1], condition=[i], subject=[], basis=[], time=[], stance='observation')
            for i in (0, 2)]}), model='contract')
        self.snapshot = dict(sources=[self.source])

    def hit(self, start, end):
        text = self.source['text']
        return evidence_from(dict(source_id='report', start=start, end=end, quote=text[start:end]),
                             self.snapshot, 1)

    def test_joint_and_individual_hits(self):
        from team_memory.adapters.reader_bridge import claim_views
        from team_memory.contracts.validation import check_answer, ContractError
        from team_memory.readers.scoped import CitedFact, ScopedDraft, public_answer
        for a, b, expected in [(0, 34, [('SEL.', 'Score rose.'), ('CONF.', 'Score fell.')]),
                                (0, 16, [('SEL.', 'Score rose.')]), (17, 34, [('CONF.', 'Score fell.')])]:
            hit = self.hit(a,b)
            views = claim_views([hit], self.snapshot)
            self.assertEqual([(v['conditions'][0], v['record_claim']['claim'][0]['quote'])
                              for v in views], expected)
            for view in views:
                for role in ('claim','condition'):
                    for span in view['record_claim'][role]:
                        self.assertEqual(self.source['text'][span['start']:span['end']], span['quote'])
            if len(views) == 2:
                snapshot = dict(self.snapshot,id='s1',as_of='2026-01-02T00:00:00Z',revision=1,proposals=[])
                bundle = dict(snapshot=snapshot, evidence=[hit],coverage='hits',unresolved_proposal_ids=[],
                              query=dict(text='What changed?',time_scope='current',as_of=None,conditions=[]))
                draft = ScopedDraft(claims=[CitedFact(fact=v['record_claim']['claim'][0]['quote'],
                    evidence_id=v['id'],substring_quote=[v['quote']]) for v in views],
                    comparison='Different directions',same_answer=False,reason='')
                answer = public_answer(draft,bundle,views)
                check_answer(answer,bundle)
                swapped = deepcopy(answer)
                first, second = swapped['claims']
                first['conditions'],second['conditions'] = second['conditions'],first['conditions']
                with self.assertRaisesRegex(ContractError,'conditions differ'):
                    check_answer(swapped,bundle)

    def test_official_answer_generate_keeps_joint_claim_ownership(self):
        from pathlib import Path
        from tempfile import TemporaryDirectory
        from threading import Lock
        from team_memory.adapters.answering import AnsweringAdapter
        from team_memory.adapters.base import request
        from team_memory.contracts.ports import CallContext
        from team_memory.readers.scoped import CitedFact, ScopedDraft, model_passage

        captured = []
        class Decoder:
            lock = Lock()
            def generate_scoped(self, query, evidence):
                rows = []
                for view in evidence:
                    item = model_passage(view, ('id','quote','conditions'))
                    captured.append((item['conditions'], item['record_claim']['claim'][0]['quote']))
                    rows.append(CitedFact(fact=item['quote'],evidence_id=item['id'],
                                          substring_quote=[item['quote']]))
                return ScopedDraft(claims=rows,same_answer=False,comparison='Opposing changes',reason='')

        snapshot=dict(self.snapshot,id='s1',as_of='2026-01-02T00:00:00Z',revision=1,proposals=[])
        bundle=dict(snapshot=snapshot,evidence=[self.hit(0,len(self.source['text']))],coverage='hits',
                    unresolved_proposal_ids=[],query=dict(text='Compare scores',conditions=[],
                    time_scope='current',as_of=None))
        with TemporaryDirectory() as folder:
            port=AnsweringAdapter('team',lambda store:Decoder(),Path(folder),snapshot_loader=lambda _:snapshot)
            req=request('answer.generate',dict(bundle=bundle),workspace_id='team',request_id='compare')
            response=port.handle(req,context=CallContext('team','team',frozenset(['answer:generate'])))
        self.assertEqual(response['status'],'ok',response['errors'])
        self.assertEqual(response['data']['outcome'],'conditional')
        self.assertEqual(captured,[(['SEL.'],'Score rose.'),(['CONF.'],'Score fell.')])
        self.assertEqual([c['evidence_ids'] for c in response['data']['claims']],[['e1'],['e1']])


class LayoutCoordinates(unittest.TestCase):
    def test_table_and_list_ranges(self):
        from team_memory.records.layout import layout
        text = ('| score | split | error |\n| --- | --- | --- |\n'
                '| 4.2 | North | 0.4 |\n| 4.2 | South | 0.5 |\n\n'
                '- North: +4.2, 95% CI [-1, +5]\n')
        first,second,listing=layout(text)
        self.assertEqual([c['quote'] for c in first['headers']], ['score','split','error'])
        self.assertEqual([c['quote'] for c in listing['cells']], ['+4.2','95% CI [-1, +5]'])
        self.assertNotEqual(first['cells'][0]['start'],second['cells'][0]['start'])
        for row in (first,second,listing):
            for c in row['cells']+row.get('headers',[]):
                self.assertEqual(text[c['start']:c['end']],c['quote'])

    def test_table_preserves_coordinates_without_a_decoder(self):
        from team_memory.records.layout import construct
        text='| metric | split |\n| --- | --- |\n| 4 | North |\n| 6 | South |\n'
        source=dict(id='table',text=text,owner='team',speaker='team',observed_at='2026-01-01T00:00:00Z',location='log')
        def unexpected(*args):
            self.fail('table attempted generation')
        result=construct(source,unexpected,model='fixture',cell_generate=unexpected)['record_graph']
        self.assertFalse(result['claims'])
        self.assertEqual([[c['quote'] for c in r['cells']] for r in result['layout']],
                         [['4','North'],['6','South']])
        self.assertEqual(result['layout'][1]['headers'][0]['quote'],'metric')
