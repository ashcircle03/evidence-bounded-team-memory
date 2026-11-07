"""Real retrieval/transport contracts with a stub decoder; not model scores."""
from copy import deepcopy
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

from tests import test_reference_qa as reference_tests
from team_memory.source_store import source_envelope


@unittest.skipUnless(reference_tests.AVAILABLE, 'reference dependencies and cached tokenizer required')
class ServiceTests(unittest.TestCase):
    def setUp(self):
        reference_tests.ReferenceQAIntegration.setUp(self)
        import nltk
        nltk.data.path.insert(0, str(Path(__file__).resolve().parents[1]/'.cache/reference-nltk'))
    source = reference_tests.ReferenceQAIntegration.source

    def make_service(self, path, client=None):
        from team_memory.service import TeamMemoryService
        from team_memory.reference_attributed import AttributedQA
        return TeamMemoryService(path, reader=AttributedQA(path, **self.options),
                                 generate=self.compare, client_state=client)

    def compare(self, system, content):
        data = json.loads(content)
        if not data['incoming']['source']['text'].startswith('I correct'):
            return '{"relations":[]}'
        old = next(e for e in data['earlier'] if '10 seconds' in e['source']['text'])
        return json.dumps(dict(relations=[dict(kind='correction', target=old['id'],
            old_quote='The timeout is 10 seconds.', new_quote=data['incoming']['source']['text'],
            reason='Explicit correction of the timeout under the same settings.')]))

    def respond(self, body):
        text = '\n'.join(m['content'] for m in body['messages'])
        if 'SUPPORTS' in text and 'IRRELEVANT' in text:
            return '{"answer":"SUPPORTS"}'
        # Return a literal source value with its actual Source number.
        blocks = re.findall(r'Source (\d+):\n(.*?)(?=\nSource \d+:|$)', text, re.S)
        number = next(n for n, b in blocks if 'The archive is Orion.' in b)
        return f'The archive is Orion [{number}].'

    def test_ingest_review_restart_and_qa_share_one_store(self):
        self.responder = self.respond
        root = Path(self.temp.name)/'shared'
        service = self.make_service(root)
        original = self.source('  The timeout is 10 seconds. The archive is Orion.\n')
        imported = service.handle(dict(operation='import_history', records=[original]))
        self.assertEqual(imported['status'], 'ok')
        self.assertEqual(self.calls, [])
        before = service.handle(dict(operation='ask', question='What is the archive?'))
        self.assertEqual(before['status'], 'ok')
        evidence = before['answers'][0]['evidence'][0]
        stored = service.store.load('sources')[evidence['source_id']]
        self.assertEqual(stored['source']['text'], original['source']['text'])
        self.assertEqual(stored['source']['text'][evidence['start']:evidence['end']], evidence['quote'])
        self.assertGreaterEqual(evidence['start'], 2)
        self.assertEqual(evidence['observed_at'], stored['observed_at'])
        incoming = self.source('I correct the earlier timeout: it is 20 seconds under the same settings.', 'test:bob')
        incoming.update(owner='Bob', observed_at='2026-01-02T00:00:00Z')
        incoming['source']['speaker'] = 'Bob'
        ingested = service.handle(dict(operation='ingest', source=incoming))
        pid = ingested['proposals'][0]['id']
        pending = service.handle(dict(operation='ask', question='What is the archive?'))
        self.assertEqual(pending['status'], 'ok')  # Unrelated correction does not block QA.
        self.assertIn('Orion', pending['raw'])
        self.assertEqual(pending['review_context']['relations'][0]['status'], 'pending')
        bad = service.handle(dict(operation='review', proposal_id=pid, actor='Bob', choice='approve'))
        self.assertEqual(bad['status'], 'invalid')
        good = service.handle(dict(operation='review', proposal_id=pid, actor='author', choice='approve'))
        self.assertEqual(good['status'], 'ok')
        after = self.make_service(root).handle(dict(operation='ask', question='What is the archive?'))
        self.assertEqual(after['status'], 'ok')
        self.assertEqual(after['review_context']['relations'][0]['status'], 'approved')
        self.assertTrue(any('"status": "approved"' in str(c['messages']) for c in self.calls))
        self.assertEqual(service.handle(dict(operation='ingest', source=incoming))['receipt']['replayed'], True)

    def test_direct_reader_keeps_same_initial_prompt_without_judge(self):
        from team_memory.reference_attributed import CitedSourceQA
        from team_memory.service import TeamMemoryService
        self.responder = self.respond
        path = Path(self.temp.name)/'paired'
        checked = self.make_service(path)
        checked.import_history([self.source('The archive is Orion.')])
        baseline = TeamMemoryService(path, reader=CitedSourceQA(path, **self.options), generate=self.compare)
        plain = baseline.ask('What is the archive?')
        direct_calls = deepcopy(self.calls)
        self.calls.clear()
        full = checked.ask('What is the archive?')
        self.assertEqual(plain['raw'], full['raw'])
        self.assertEqual(plain['answers'], full['answers'])
        self.assertEqual(direct_calls[0], self.calls[0])
        self.assertEqual(len(direct_calls), 1)
        self.assertEqual(len(self.calls), 2)

    def test_two_git_clones_merge_and_sync_without_ordinal_rebuild(self):
        base = Path(self.temp.name)/'git'
        base.mkdir()
        def git(path, *args):
            return subprocess.check_output(['git', '-C', str(path), '-c', 'user.name=Test',
                '-c', 'user.email=test@example.test', *args], text=True, stderr=subprocess.PIPE)
        left, right, remote = base/'left', base/'right', base/'remote.git'
        git(base, 'init', '--bare', str(remote))
        git(base, 'clone', str(remote), str(left))
        a = self.make_service(left/'shared')
        a.import_history([self.source('The base record is shared.')])
        git(left, 'add', 'shared'); git(left, 'commit', '-m', 'initial'); git(left, 'push', 'origin', 'HEAD')
        git(base, 'clone', str(remote), str(right))
        b = self.make_service(right/'shared')
        b.sync()
        a.ingest(self.source('Independent left report.', 'test:left'))
        b.ingest(self.source('Independent right report.', 'test:right'))
        git(left, 'add', 'shared'); git(left, 'commit', '-m', 'left'); git(left, 'push', 'origin', 'HEAD')
        git(right, 'add', 'shared'); git(right, 'commit', '-m', 'right')
        git(right, 'pull', '--no-rebase', '--no-edit', 'origin')
        self.assertEqual(self.make_service(right/'shared').handle(dict(operation='rebuild'))['status'], 'ok')
        git(right, 'add', 'shared')
        # No relations for these unrelated reports; sync has only local effects.
        self.assertEqual(git(right, 'status', '--porcelain').strip(), '')
        git(right, 'push', 'origin', 'HEAD'); git(left, 'pull', '--ff-only')
        self.assertEqual(a.sync()['status'], 'ok')
        self.assertEqual(a.store.load('sources'), b.store.load('sources'))
        self.assertEqual(len(a.store.load('sources')), 3)
        self.assertNotIn('timeline-client', git(left, 'ls-files'))
        self.assertNotIn('reference-index', git(left, 'ls-files'))

    def test_rejected_review_and_historical_scope_are_explicit(self):
        self.responder = self.respond
        service = self.make_service(Path(self.temp.name)/'rejected')
        service.import_history([self.source('The timeout is 10 seconds. The archive is Orion.')])
        incoming = self.source('I correct the earlier timeout: it is 20 seconds under the same settings.', 'test:next')
        p = service.ingest(incoming)['proposals'][0]
        service.review(p['id'], 'author', 'reject')
        result = service.ask('What is the archive?', temporal_scope='historical')
        self.assertEqual(result['temporal_scope'], 'historical')
        self.assertIsNone(result['review_context'])
        self.assertIn('Orion', result['raw'])

    def test_public_jsonl_cli_has_one_response_per_request(self):
        from io import StringIO
        from contextlib import redirect_stdout
        from unittest.mock import patch
        from team_memory.service import main
        self.responder = self.respond
        requests = [json.dumps(dict(operation='import_history', records=[self.source('The archive is Orion.')])),
                    json.dumps(dict(operation='ask', question='What is the archive?')),
                    'not-json', json.dumps(dict(operation='view'))]
        output = StringIO()
        argv = ['service', '--store', str(Path(self.temp.name)/'cli'), '--model-path', 'test-model',
                '--embedding-path', 'test-embedding', '--api-base', 'http://localhost:9999/v1']
        with patch('sys.argv', argv), patch('sys.stdin', StringIO('\n'.join(requests)+'\n')), \
             patch('team_memory.reference_qa.local_components', return_value=self.options), redirect_stdout(output):
            main()
        rows = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual(len(rows), 4)
        self.assertEqual([r['status'] for r in rows], ['ok','ok','invalid','ok'])
        self.assertEqual(rows[1]['schema_version'], 'team-memory/v2')


class DateContractTests(unittest.TestCase):
    def test_current_judge_excludes_only_approved_superseded_assertion(self):
        from team_memory import timeline
        from team_memory.source_store import SourceStore
        from team_memory.review_context import current_judge_text, assertion_reviews
        def env(text, who, day):
            return source_envelope(dict(owner=who, observed_at=f'2026-01-{day:02d}T00:00:00Z',
                source=dict(speaker=who, location=who, text=text)))
        old=env('The timeout is 10 seconds. The archive is Orion.', 'Alice', 1)
        new=env('I correct the timeout: it is 12 seconds under the same settings.', 'Bob', 2)
        with tempfile.TemporaryDirectory() as root:
            store=SourceStore(root)
            timeline.ingest(store,old,lambda *_:'{"relations":[]}')
            from team_memory.store import digest
            reply=json.dumps(dict(relations=[dict(kind='correction',target=digest(old),
                old_quote='The timeout is 10 seconds.',new_quote=new['source']['text'],reason='Explicit correction.')]))
            pid=timeline.ingest(store,new,lambda *_:reply)['proposals'][0]
            w=timeline.witness(old,old['source']['text'])
            context=dict(temporal_scope='current',relations=timeline.proposals(store))
            self.assertEqual(current_judge_text(w,context),w['quote'])
            timeline.review(store,pid,'Alice','approve')
            context['relations']=timeline.proposals(store)
            projected=current_judge_text(w,context)
            self.assertNotIn('10 seconds',projected)
            self.assertIn('The archive is Orion.',projected)
            self.assertEqual(w['quote'],old['source']['text'])
            self.assertEqual(assertion_reviews(w,context)[0]['status'],'superseded_assertion')
            self.assertEqual(current_judge_text(w,dict(context,temporal_scope='historical')),w['quote'])
            rival=deepcopy(context['relations'][0]);rival['id']='rival'
            rival['incoming']=dict(rival['incoming'],source_id='another-original',quote='14 seconds')
            context['relations'].append(rival)
            self.assertEqual(current_judge_text(w,context),w['quote'])

    def test_unverified_replacement_retains_original_and_is_not_ok(self):
        from threading import RLock
        from types import SimpleNamespace
        from team_memory.service import TeamMemoryService
        from team_memory.store import Store
        from team_memory.reference_attributed import repair_omitted_answer
        from team_memory.reference_qa import format_response
        witnesses = [dict(source_id=s, quote=f'The value is {v}.', start=0, end=16,
            speaker=s, location=s) for s,v in [('a',10),('b',20)]]
        draft = format_response('Q', 'The value is 10 [1].', witnesses)
        draft.update(draft_raw=draft['raw'], revised=False,
                     document_judgments=[dict(source_id='b',label='CONTRADICTS')])
        llm = SimpleNamespace(chat=lambda *_:SimpleNamespace(message=SimpleNamespace(content='The value is 999 [1][2].')))
        candidate = repair_omitted_answer('Q',draft,llm)
        with tempfile.TemporaryDirectory() as root:
            reader = SimpleNamespace(store=Store(root), lock=RLock(), ask=lambda _:candidate)
            service = TeamMemoryService(root, reader=reader, generate=lambda *_:'{"relations":[]}')
            result = service.ask('Q')
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['answer_revision']['original_raw'], 'The value is 10 [1].')
        self.assertEqual(result['answer_revision']['status'], 'unverified_candidate')
        self.assertFalse(result['aqa_semantic_preservation_verified'])

    def test_original_text_is_not_normalized(self):
        raw = dict(owner='A', observed_at='2026-01-01T00:00:00Z',
                   source=dict(speaker='A', location='test:a', text='  indented\n'))
        self.assertEqual(source_envelope(raw)['source']['text'], raw['source']['text'])

    def test_timezone_and_unknown_zone_order(self):
        from team_memory.reference_documents import documents
        def w(sid, stamp):
            return dict(source_id=sid, quote='A', start=0, end=1, speaker='A', location=sid, observed_at=stamp)
        early = w('earlier', '2025-01-01T09:00:00+09:00')
        late = w('later', '2025-01-01T01:00:00+00:00')
        self.assertEqual([x['source_id'] for x in documents([late, early])], ['earlier', 'later'])
        unknown = w('unknown', '2024-01-01T00:00:00')
        self.assertEqual([x['source_id'] for x in documents([late, unknown, early])], ['later', 'unknown', 'earlier'])


if __name__ == '__main__':
    unittest.main()
