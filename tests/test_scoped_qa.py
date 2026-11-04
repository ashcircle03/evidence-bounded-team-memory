import json
import tempfile
import unittest
from team_memory.merge import replay, submit
from team_memory.qa import answer, read_answer
from team_memory.relation import exclusive_difference
from team_memory.store import Store

def add(store,owner,topic,value,quote,scope=None):
    return submit(store,dict(owner=owner,observed_at='2025-02-01T12:00:00Z',issue=topic,value=value,quote=quote,
        scope=scope or {},source=dict(speaker=owner,text=quote,location='test/'+owner)))

class Scoped(unittest.TestCase):
    def test_scope_or_shared_label_alone_is_not_a_contradiction(self):
        with tempfile.TemporaryDirectory() as d:
            s=Store(d)
            add(s,'a','release','red','The only sticker for the January release was red.')
            b=add(s,'b','release','July','The only calibration period for the January release was July.')
            self.assertFalse(b['targets'])
            c=add(s,'c','sticker archive','green','The only sticker for the January release was green.')
            self.assertEqual([t['action'] for t in c['targets']],['unresolved'])
            self.assertEqual(len(replay(s)),3)

    def test_bounds_and_changed_subjects_do_not_make_a_hard_conflict(self):
        for a,b in [
            ('At least 10 days','At least 12 days'),
            ('The sole manager in London was Kim.','The sole manager in Tokyo was Kim.'),
            ('We upload documents to X.','We upload documents to Y.'),
            ('Maybe the sole host was Anna.','Maybe the sole host was Brett.')]:
            self.assertIsNone(exclusive_difference(a,b))

    def test_scoped_gate_and_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            s=Store(d)
            for who,val in [('a','red'),('b','green')]:add(s,who,'release',val,'The only sticker for the January release was '+val+'.')
            c=add(s,'c','release','Bo','The only editor for the January release was Bo.')
            related=read_answer(answer(s,'What was the sticker for the January release?'),'What was the sticker?',lambda *_:'YES')['reader']
            self.assertEqual({(x['answer'],x['speaker'],x['status']) for x in related['alternatives']},{('green','b','pending'),('red','a','pending')})
            def no(instruction,text):
                if 'YES or NO' in instruction:return 'NO'
                return json.dumps({'id':c['id'],'field':'quote','span':'Bo'})
            ans=read_answer(answer(s,'Who was the January release editor?'),'Who was the editor?',no)['reader']
            self.assertEqual((ans['answer'],ans['id']),('Bo',c['id']))

    def test_one_source_cannot_supply_both_sides(self):
        with tempfile.TemporaryDirectory() as d:
            s=Store(d);c=add(s,'a','rollout','Oslo','The launch was moved from Oslo to Lyon.')
            def invalid(*_):
                return json.dumps({'kind':'conflict','sides':[{'id':c['id'],'field':'quote','span':v} for v in ('Oslo','Lyon')]})
            self.assertEqual(read_answer(answer(s,'Where was the launch?'),'Where?',invalid)['reader']['status'],'invalid_citation')

    def test_writer_abstentions_still_yield_a_proposal_and_two_source_ids(self):
        from team_memory.writer import ingest
        with tempfile.TemporaryDirectory() as d:
            st=Store(d); ids=[]
            for who,v in [('a','Aster'),('b','Cedar')]:
                e=dict(owner=who,observed_at='2025-01-10T12:00:00Z',
                       source=dict(speaker=who,location='archive/'+who,text='The only building for the planning session was '+v+'.'))
                added=ingest(st,e,lambda *_:'null');ids.append(added['source_id'])
            self.assertEqual(added['outcome'],'abstained')
            proposal,=added['source_proposals']
            self.assertEqual(set(ids),{w['id'] for w in proposal['sides']})
            self.assertEqual(proposal['status'],'unreviewed')
            result=read_answer(answer(st,'Which building held the planning session?'),'Which building?',lambda *_:'YES')
            self.assertEqual(set(ids),{w['id'] for w in result['reader']['alternatives']})

    def test_counts_with_the_wrong_unit_do_not_enter_the_semantic_gate(self):
        with tempfile.TemporaryDirectory() as d:
            st=Store(d)
            for who,v in [('a','4'),('b','6')]:
                add(st,who,'log',v,'The only signed copy for the planning session was exactly '+v+' pages.')
            asked='How many hours did the planning session take?'
            instructions=[]
            def abstain(ins,content):
                instructions.append(ins);return 'null'
            ans=read_answer(answer(st,asked),asked,abstain)
            self.assertEqual(ans['reader']['status'],'insufficient')
            self.assertEqual(len(instructions),1)
