"""State/data boundary regressions; no LLM accuracy claims."""
import json
import tempfile
import unittest
from copy import deepcopy
from types import SimpleNamespace
from team_memory import timeline
from team_memory.source_store import SourceStore, source_envelope
from team_memory.store import digest


class StateBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.store=SourceStore(self.tmp.name)
        def source(text,who,day):
            return source_envelope(dict(owner=who,observed_at=f'2026-02-{day:02d}T09:00:00Z',
                source=dict(speaker=who,location=f'test:{who}',text=text)))
        self.old=source('The retry limit is 3. The maintainer is Lee.','A',1)
        self.new=source('I correct the retry limit to 4. Lee is still the maintainer.','B',2)
        timeline.ingest(self.store,self.old,lambda *_:'{"relations":[]}')
        self.proposal=dict(kind='correction',target=digest(self.old),
            old_quote=self.old['source']['text'],new_quote=self.new['source']['text'],
            old_assertion='The retry limit is 3.',new_assertion='I correct the retry limit to 4.',
            reason='Only the retry limit changes.')

    def ingest(self,proposal=None):
        result=timeline.ingest(self.store,self.new,lambda *_:json.dumps(dict(relations=[proposal or self.proposal])))
        return result

    def test_approval_affects_changed_assertion_not_context_or_original(self):
        from team_memory.review_context import current_judge_text
        pid=self.ingest()['proposals'][0]
        before=deepcopy(self.store.load('sources'))
        timeline.review(self.store,pid,'A','approve')
        links=timeline.proposals(self.store);w=timeline.witness(self.old,self.old['source']['text'])
        self.assertEqual(timeline.assertion_status(w,'3',links),'superseded_assertion')
        self.assertEqual(timeline.assertion_status(w,'Lee',links),'reported')
        text=current_judge_text(w,dict(temporal_scope='current',relations=links))
        self.assertNotIn('limit is 3',text);self.assertIn('The maintainer is Lee.',text)
        self.assertEqual(self.store.load('sources'),before)

    def test_scope_cannot_escape_cited_context(self):
        bad=dict(self.proposal,old_quote='The retry limit is 3.',old_assertion='The maintainer is Lee.')
        result=self.ingest(bad)
        self.assertEqual(result['proposals'],[]);self.assertTrue(result['errors'])
        self.assertEqual(self.store.load('timeline_proposals'),{})

    def test_pending_and_rejected_do_not_apply_but_remain_readable(self):
        from team_memory.review_context import expand_review_context,resolution_view,current_judge_text
        from llama_index.core.schema import TextNode,NodeWithScore
        pid=self.ingest()['proposals'][0]
        node=TextNode(text=self.old['source']['text'],metadata=dict(source_id=digest(self.old),parent_start=0,parent_end=len(self.old['source']['text'])))
        w=timeline.witness(self.new,self.new['source']['text'])
        for state in ('pending','rejected'):
            if state=='rejected':timeline.review(self.store,pid,'A','reject')
            nodes,ctx=expand_review_context([NodeWithScore(node=node)],self.store.load('sources'),timeline.proposals(self.store),'current')
            self.assertEqual(ctx['relations'][0]['status'],state)
            self.assertEqual(len(nodes),2)
            view=resolution_view(ctx)[0];self.assertFalse(view['change_applied'])
            self.assertEqual(view['retained_assertion']['quote'],'The retry limit is 3.')
            self.assertNotIn('limit to 4',current_judge_text(w,ctx))
            self.assertEqual(current_judge_text(w,dict(ctx,temporal_scope='historical')),w['quote'])

    def test_date_author_survive_judge_revision_and_aqa(self):
        from team_memory.reference_checked import ConflictCheckedQA,review_messages
        from team_memory.reference_attributed import aqa_messages
        from team_memory.reference_qa import format_response
        from threading import RLock
        w=timeline.witness(self.old,self.old['source']['text']);w['observed_at']=self.old['observed_at']
        seen=[]
        def chat(messages,**kwargs):
            seen.extend(m.content for m in messages)
            return SimpleNamespace(message=SimpleNamespace(content='{"answer":"SUPPORTS"}'))
        reader=object.__new__(ConflictCheckedQA);reader.lock=RLock();reader.llm=SimpleNamespace(chat=chat)
        draft=format_response('What limit?','3 [1].',[w]);reader._review('What limit?',draft)
        seen+= [m.content for m in review_messages('Q','3',[w],[])]
        seen+= [m.content for m in aqa_messages('Q',[w])]
        rendered=[s for s in seen if 'Source 1:' in s]
        self.assertEqual(len(rendered),3)
        self.assertTrue(all('recorded_at: 2026-02-01T09:00:00' in s and 'record_author: A' in s for s in rendered))


class SourceSelectorTests(unittest.TestCase):
    def setUp(self):
        import nltk
        from pathlib import Path
        nltk.data.path.insert(0,str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))

    def test_ids_restore_original_case_and_narrow_scope_without_extra_call(self):
        from team_memory.source_comparison import compare_sources
        def env(sid,text):return dict(id=sid,source=dict(text=text,speaker='A',location=sid))
        old='For unit C, the cap is 500 MB. The owner is Hana.'
        new='I correct the cap to 480 MB. Hana is unchanged.'
        request=dict(earlier=[env('old',old)],incoming=env('new',new));calls=[]
        def generate(system,content):
            calls.append(json.loads(content))
            return json.dumps(dict(relations=[dict(kind='correction',target='old',old_sentence_ids=[0,1],
                new_sentence_ids=[0,1],old_assertion_id=0,new_assertion_id=0,reason='Explicit change.')]))
        out=json.loads(compare_sources(generate,json.dumps(request)))['relations'][0]
        self.assertEqual(len(calls),1)
        self.assertNotIn('text',calls[0]['earlier'][0]['source'])
        self.assertEqual(out['old_quote'],old)
        self.assertEqual(out['old_assertion'],'For unit C, the cap is 500 MB.')
        self.assertNotIn('Hana',out['old_assertion'])
        self.assertEqual(request['earlier'][0]['source']['text'],old)
        def bad(*_):return json.dumps(dict(relations=[dict(kind='correction',target='old',old_sentence_ids=[99],new_sentence_ids=[0],old_assertion_id=99,new_assertion_id=0,reason='bad')]))
        failed=json.loads(compare_sources(bad,json.dumps(request)))
        self.assertEqual(failed['relations'],[])
        self.assertIn('Sentence IDs',failed['selection_errors'][0]['error'])
        self.assertIn('99',failed['model_output'])

    def test_coexistence_is_information_not_a_pending_change(self):
        from team_memory.source_comparison import compare_sources
        request=dict(earlier=[dict(id='old',source=dict(text='A result.',speaker='A'))],incoming=dict(id='new',source=dict(text='B result.',speaker='B')))
        def generate(*_):return json.dumps(dict(relations=[dict(kind='coexist',target='old',old_sentence_ids=[0],new_sentence_ids=[0],reason='Different settings.')]))
        out=json.loads(compare_sources(generate,json.dumps(request)))
        self.assertEqual(out['relations'],[])
        self.assertEqual(len(out['informational_relations']),1)
