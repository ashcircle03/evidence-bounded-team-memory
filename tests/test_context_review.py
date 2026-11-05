import copy
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from team_memory.context_review import observation_units, neighborhood, revise, valid_evidence, NONE
from team_memory.evidence import FOLLOWUP
from team_memory.pair_selection import paragraphs
from team_memory.store import Store
from team_memory.sync import followups


def document(text, location='issue'):
    return dict(owner='Lee',observed_at='2020-01-02', source=dict(text=text,location=location,speaker='Lee'))

class Reader:
    def option_scores(self,system,content,count):
        choices=list(json.loads(content)['choices'].values())
        return [5 if 'returns NULL on empty input' in value else 1 if value==NONE else 0 for value in choices]

class ContextReviewTest(unittest.TestCase):
    def test_join_only_included_neighboring_paragraphs(self):
        text='Title\n\nThe reader fails with\n\nerror code NEGATIVE\n\nOnly on empty input.'
        env=document(text);blocks=[p.cite() for p in paragraphs('s',(env,'source_only'))]
        units=observation_units([blocks[2],blocks[1]],{'s':env})
        self.assertEqual(units[0]['quote'],'The reader fails with\n\nerror code NEGATIVE')
        self.assertEqual(observation_units([blocks[1],blocks[3]],{'s':env}),[blocks[1],blocks[3]])
        self.assertEqual(neighborhood(blocks[2],env),blocks[1:])

    def test_other_document_cannot_supply_the_reported_failure(self):
        original=document('Original condition.')
        foreign=document('Reader returns NULL on empty input.','other')
        a=paragraphs('a',(original,'source_only'))[0].cite()
        b=paragraphs('b',(foreign,'source_only'))[0].cite()
        base=dict(action='reassess',previous=a,incoming=a)
        r=revise(base,[a,b],{'a':original,'b':foreign},Reader())
        self.assertEqual(r['action'],'keep')

    def test_followup_rejects_modified_quote_and_appended_claim(self):
        with TemporaryDirectory() as temp:
            store=Store(Path(temp))
            old=document('Always return a value.','old');old['observed_at']='2020-01-01'
            new=document('Parser returns NULL on empty input.')
            a=store.put('sources',old);b=store.put('sources',new)
            wa=paragraphs(a,(old,'source_only'))[0].cite()
            wb=paragraphs(b,(new,'source_only'))[0].cite()
            base=dict(action='reassess',previous=wa,incoming=wb,reviewer='Lee',next_step=FOLLOWUP['REASSESS'])
            r=revise(base,[wb],{b:new},Reader())
            self.assertTrue(valid_evidence(r));r['strategy']='context-review'
            store.put('followups',r)
            bad=copy.deepcopy(r);bad['rationale']+=' Causes permanent data loss.'
            self.assertFalse(valid_evidence(bad));store.put('followups',bad)
            bad=copy.deepcopy(r);bad['observation_evidence']=dict(bad['observation_evidence'],speaker='Kim')
            self.assertFalse(valid_evidence(bad));store.put('followups',bad)
            self.assertEqual(len(followups(store)),1)
            self.assertEqual(followups(store)[0]['status'],'pending')

    def test_more_than_four_units_and_none_are_supported(self):
        env=document('Title\n\nNo result.\n\nNo result.\n\nNo result.\n\nParser returns NULL on empty input.\n\nRepair next.')
        blocks=[p.cite() for p in paragraphs('s',(env,'source_only'))]
        base=dict(action='reassess',previous=blocks[1],incoming=blocks[1])
        r=revise(base,blocks,{'s':env},Reader())
        self.assertEqual(r['action'],'reassess')
        self.assertIn('returns NULL on empty input',r['incoming']['quote'])
        self.assertEqual(revise(base,[blocks[1]],{'s':env},Reader())['action'],'keep')
