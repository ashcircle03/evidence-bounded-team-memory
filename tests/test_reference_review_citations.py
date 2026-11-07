from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from team_memory.store import digest
from team_memory.source_store import SourceStore, source_envelope
from team_memory import timeline


class ReviewCitationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.store=SourceStore(self.tmp.name)
        def env(text,who,day):
            return source_envelope(dict(owner=who,observed_at=f'2026-01-{day:02d}T00:00:00Z',
                source=dict(speaker=who,location=who,text=text)))
        self.old=env('The deadline is Thursday. The team name is Cedar.','A',1)
        self.new=env('I correct the deadline to Friday for the same release.','B',2)
        timeline.ingest(self.store,self.old,lambda *_:'{"relations":[]}')
        reply=json.dumps(dict(relations=[dict(kind='correction',target=digest(self.old),
            old_quote='The deadline is Thursday.',new_quote=self.new['source']['text'],reason='Explicit same-release correction.')]))
        self.pid=timeline.ingest(self.store,self.new,lambda *_:reply)['proposals'][0]
    def context(self):return dict(temporal_scope='current',relations=timeline.proposals(self.store))

    def test_pending_approval_snapshots_remain_distinct_and_verifiable(self):
        from team_memory.review_citations import review_sources
        pending=review_sources(self.store,self.context())[0]
        self.assertEqual(pending['vote_ids'],[])
        self.assertIn('is pending',pending['quote'])
        timeline.review(self.store,self.pid,'A','approve')
        approved=review_sources(self.store,self.context())[0]
        self.assertIn('has been approved',approved['quote'])
        self.assertNotEqual(pending['snapshot_id'],approved['snapshot_id'])
        self.assertEqual(len(approved['vote_ids']),1)
        for item in (pending,approved):
            saved=self.store.load('review_snapshots')[item['snapshot_id']]
            self.assertEqual(saved,item['record_snapshot'])
            self.assertEqual(digest(saved),item['snapshot_id'])
            self.assertIsNone(item['observed_at'])
        for vid in approved['vote_ids']:
            self.assertEqual(approved['record_snapshot']['votes'][vid],self.store.load('timeline_votes')[vid])

    def test_conflicting_votes_cannot_be_rendered_as_approval(self):
        from team_memory.review_citations import review_sources
        for choice in ('approve','reject'):
            self.store.put('timeline_votes',dict(proposal=self.pid,actor='A',choice=choice))
        w=review_sources(self.store,self.context())[0]
        self.assertIn('approval is unresolved',w['quote'])
        self.assertNotIn('has been approved',w['quote'])

    def test_stale_context_is_rejected(self):
        from team_memory.review_citations import review_sources
        context=self.context();timeline.review(self.store,self.pid,'A','approve')
        with self.assertRaises(ValueError):review_sources(self.store,context)

    def test_exact_quote_adapter_keeps_answer_and_original_citation(self):
        import nltk
        nltk.data.path.insert(0,str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))
        from team_memory.review_citations import review_sources
        from team_memory.reference_qa import format_response
        from team_memory.reference_quotes import add_quote_citations
        original=timeline.witness(self.old,self.old['source']['text'])
        raw='The deadline was Thursday [1]. The correction is pending.'
        result=format_response('What is the status?',raw,[original])
        llm=SimpleNamespace(chat=lambda *_:SimpleNamespace(message=SimpleNamespace(content=json.dumps(dict(question="What is the status?",answer=[
            dict(fact='The correction is pending.',substring_quote=['The correction is pending.'])])))))
        out=add_quote_citations('What is the status?',result,llm,review_witnesses=review_sources(self.store,self.context()))
        self.assertEqual(out['status'],'ok')
        self.assertEqual(out['raw'],'The deadline was Thursday [1]. [2] The correction is pending.')
        self.assertEqual(out['answers'][0]['evidence'][0],original)
        self.assertEqual(out['answers'][0]['evidence'][1]['evidence_type'],'review_state')
        # A fake approved sentence is not a substring of a pending snapshot.
        llm.chat=lambda *_:SimpleNamespace(message=SimpleNamespace(content=json.dumps(dict(question="What is the status?",answer=[
            dict(fact='The correction is pending.',substring_quote=['The correction has been approved.'])]))))
        bad=add_quote_citations('What is the status?',result,llm,review_witnesses=review_sources(self.store,self.context()))
        self.assertEqual(bad['status'],'partial')
        self.assertEqual(bad['raw'],raw)
