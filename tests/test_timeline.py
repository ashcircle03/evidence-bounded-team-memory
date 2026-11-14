import json
from pathlib import Path
import tempfile
import unittest
from team_memory.store import Store, digest, capture
from team_memory import timeline as t


def env(text, actor='A', day=1):
    return dict(owner=actor, observed_at=f'2025-01-{day:02}T00:00:00.000000+00:00',
                source=dict(speaker=actor,location=f'test://{actor}/{day}',text=text))


class TimelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.store=Store(Path(self.tmp.name)/'records')
        self.old=env('The timeout is 10 seconds. The archive is Orion.')
        t.ingest(self.store,self.old,lambda *a: '{}')

    def propose(self, kind='correction', actor='B', day=2, value='20'):
        new=env(f'I correct the earlier timeout: it is {value} seconds under the same settings.',actor,day)
        p=dict(kind=kind,target=digest(self.old),old_quote='The timeout is 10 seconds.',
               new_quote=new['source']['text'],reason='The old timeout measurement is explicitly corrected.')
        result=t.ingest(self.store,new,lambda *a:json.dumps(dict(relations=[p])))
        return new,result['proposals'][0]

    def test_approval_applies_to_assertion_not_whole_source(self):
        new,pid=self.propose();before=self.store.load('sources')
        w=t.witness(self.old,self.old['source']['text'])
        self.assertEqual(t.assertion_status(w,'10 seconds',t.proposals(self.store)),'reported')
        self.assertEqual(t.assertion_status(t.witness(new,new['source']['text']),'20 seconds',t.proposals(self.store)),'pending_correction')
        t.review(self.store,pid,'A','approve')
        self.assertEqual(t.assertion_status(w,'10 seconds',t.proposals(self.store)),'superseded_assertion')
        self.assertEqual(t.assertion_status(w,'Orion',t.proposals(self.store)),'reported')
        self.assertEqual(self.store.load('sources'),before)

    def test_reconsider_approval_does_not_invalidate_old_observation(self):
        _,pid=self.propose(kind='reconsider');t.review(self.store,pid,'A','approve')
        self.assertEqual(t.assertion_status(t.witness(self.old,self.old['source']['text']),'10 seconds',t.proposals(self.store)),'reported')

    def test_original_owner_and_exact_proposal_required(self):
        _,pid=self.propose()
        with self.assertRaises(ValueError):t.review(self.store,pid,'B','approve')
        with self.assertRaises(ValueError):t.review(self.store,'missing','A','approve')
        self.store.put('timeline_votes',dict(proposal=pid,actor='B',choice='approve'))
        self.assertEqual(t.proposals(self.store)[0]['status'],'pending')
        t.review(self.store,pid,'A','reject')
        with self.assertRaises(ValueError):t.review(self.store,pid,'A','approve')

    def test_conflicting_reviews_preserved(self):
        _,pid=self.propose();t.review(self.store,pid,'A','approve')
        self.store.put('timeline_votes',dict(proposal=pid,actor='A',choice='reject'))
        self.assertEqual(t.proposals(self.store)[0]['status'],'review_conflict')
        self.assertEqual(t.assertion_status(t.witness(self.old,self.old['source']['text']),'10 seconds',t.proposals(self.store)),'reported')

    def test_duplicate_arrival_does_not_call_model_again(self):
        def forbidden(*a):raise AssertionError('unexpected model call')
        self.assertTrue(t.ingest(self.store,self.old,forbidden)['replayed'])

    def test_invalid_sibling_is_isolated_and_raw_source_survives(self):
        new=env('New measurement.',day=2)
        good=dict(kind='conflict',target=digest(self.old),old_quote='10 seconds',new_quote='New measurement.',reason='different')
        bad=dict(good,target='future-source')
        r=t.ingest(self.store,new,lambda *a:json.dumps(dict(relations=[good,bad])))
        self.assertTrue(r['errors']);self.assertEqual(len(t.proposals(self.store)),1)
        self.assertEqual(r['errors'][0]['index'],1)
        self.assertIn(digest(new),self.store.load('sources'))

    def test_index_must_quote_source_and_cannot_set_approval(self):
        self.store=Store(Path(self.tmp.name)/'indexed')
        t.ingest(self.store,self.old,lambda *a:'{"decisions":[]}','indexed')
        new=env('We retain CSV because the converter is unavailable.',day=2)
        responses=iter([json.dumps(dict(relations=[])),json.dumps(dict(decisions=[dict(decision='We adopt JSON.',basis='',scope='')]))])
        r=t.ingest(self.store,new,lambda *a:next(responses),'indexed')
        self.assertTrue(r['errors'])
        self.assertNotIn(digest(new),{c['source_id'] for c in t.decision_index(self.store)})
        self.assertIn('quotation',r['errors'][0]['error'])

    def test_modes_do_not_share_derived_history(self):
        with self.assertRaises(ValueError):t.ingest(self.store,env('Another source.',day=2),lambda *a:'{}','indexed')

    def test_another_agents_processing_does_not_skip_local_context(self):
        from team_memory.timeline_cli import process_sources
        sender=Store(Path(self.tmp.name)/'sender')
        new=env('The timeout is now 20 seconds.',actor='B',day=2)
        t.ingest(sender,new,lambda *a:'{"relations":[]}')
        # Transport only shared objects; each client has private receipts.
        for sid,e in sender.load('sources').items():self.store.put('sources',e)
        calls=[]
        def reader(s,x):calls.append(json.loads(x));return '{"relations":[]}'
        process_sources(self.store,reader,'direct')
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0]['incoming']['id'],digest(new))
        self.assertEqual([e['id'] for e in calls[0]['earlier']],[digest(self.old)])

    def test_future_source_not_in_prompt(self):
        calls=[]
        future=env('Later private result should not leak.',day=4)
        capture(self.store,future)  # Git has transported a batch; it has not all been ingested.
        new=env('We postpone migration because tests failed.',day=2)
        def generate(s,x):
            calls.append(json.loads(x));return '{"relations":[]}'
        t.ingest(self.store,new,generate)
        self.assertEqual([x['id'] for x in calls[0]['earlier']],[digest(self.old)])
        def ask_reader(s,x):
            self.assertNotIn(digest(future),{e['id'] for e in json.loads(x)['sources']})
            return '{"kind":"insufficient","answers":[]}'
        t.ask(self.store,'What was known?',ask_reader)

    def test_qa_checks_quote_and_derives_status(self):
        new,pid=self.propose()
        answer=dict(kind='single',answers=[dict(source=digest(new),quote=new['source']['text'],answer='20 seconds',condition='',status='approved')])
        r=t.ask(self.store,'What timeout was reported?',lambda *a:json.dumps(answer))
        self.assertEqual(r['answers'][0]['status'],'pending_correction')
        answer['answers'][0]['answer']='999 seconds'
        self.assertEqual(t.ask(self.store,'Timeout?',lambda *a:json.dumps(answer))['kind'],'invalid')

    def test_two_approved_replacements_do_not_pick_latest(self):
        _,one=self.propose();_,two=self.propose(day=3,value='30')
        t.review(self.store,one,'A','approve');t.review(self.store,two,'A','approve')
        w=t.witness(self.old,self.old['source']['text'])
        self.assertEqual(t.assertion_status(w,'10 seconds',t.proposals(self.store)),'correction_conflict')


if __name__=='__main__':unittest.main()
