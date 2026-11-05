"""Contract and cross-module checks; fake generation, real source/approval stores."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from team_memory.cupmem_service import CUPMemService
from team_memory.cupmem_adapter import CUPMemTeamMemory
from team_memory.cupmem_review import review_sources
from team_memory.core import passages, records_view
from team_memory.store import Store, capture, digest, source_envelope
from team_memory import timeline


def source(text, day=1, owner='Alice'):
    return source_envelope(dict(owner=owner, observed_at=f'2025-01-{day:02d}T00:00:00Z',
        source=dict(speaker=owner, location=f'source://{owner}/{day}', text=text)))


OLD = source('Cedar took 40 seconds with one process. We stopped Cedar trials because deployment permits one process. The folder is Cedar-audit.')
NEW = source('Deployment now permits four processes. Cedar took 12 seconds with four processes.', 2, 'Bob')


class Engine:
    def __init__(self):
        self.writes = []
        self.fail = False
        self.allowed = None
        self.rank_calls = []
        self.embedding = self

    def rank(self, *, query_text, candidates, text_getter, top_k):
        self.rank_calls.append(deepcopy(candidates))
        if self.allowed is not None:
            candidates = [p for p in candidates if p['source_id'] in self.allowed]
        return [dict(score=1.0, item=p) for p in candidates[:top_k]]

    def write_session(self, **kwargs):
        self.writes.append(kwargs)
        if self.fail: raise RuntimeError('simulated partial native write')
        return dict(session_index=kwargs['session_index'])

    def reset(self):
        self.writes = []


class Memory:
    def __init__(self):
        self.sources, self.source_generate = [], None
        self.engine = Engine()
        self.recorded_calls = lambda: []
        self.miss = False
        self.fail_query = False
        self.mutate = False

    def ingest(self, env, *, review_changes):
        assert review_changes is False
        log = self.engine.write_session(session=[env], session_index=len(self.sources), session_time=env['observed_at'])
        self.sources.append(env)
        return dict(native_write=log)

    def ask(self, question):
        if self.mutate: raise AssertionError('native query mutation')
        if self.fail_query: raise RuntimeError('native query failed')
        originals = []
        for i, env in enumerate(self.sources):
            text = json.dumps(env)
            originals.append(dict(text=text, content_sha256=sha256(text.encode()).hexdigest(),
                session_index=i, session_id=f's_{i:03d}', turn_id='t_0', session_time=env['observed_at'],
                uses=[dict(purpose='value', binding_id=str(i))]))
        return dict(question=question, answer={'answer': 'native diagnostic'}, provenance_errors=[],
            provenance=None if self.miss else dict(unresolved=[], original_turns_for_audit=originals, basis_bindings=[]))


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.memory = Memory()
        self.calls = []
        self.forced = None
        self.service = CUPMemService(self.memory, self.generate, Path(self.tmp.name)/'records')

    def generate(self, system, content):
        data = json.loads(content); self.calls.append((system, data))
        if self.forced is not None: return self.forced
        if system.startswith('Review the incoming'):
            if not any('four processes' in p['quote'] for p in data['incoming']):
                return '{"relations":[]}'
            old = next(p['id'] for p in data['earlier'] if 'We stopped' in p['quote'])
            new = next(p['id'] for p in data['incoming'] if 'Deployment' in p['quote'])
            return json.dumps(dict(relations=[dict(kind='reconsider', old_claim=[old], new_claim=[new],
                old_reason=[old], old_condition=[old], new_condition=[new],
                reason='The deployment constraint behind stopping trials changed.')]))
        hit = next(p for p in data['passages'] if 'Cedar-audit' in p['quote'])
        return json.dumps(dict(kind='single', answers=[dict(text='Cedar-audit', evidence=[hit['id']])]))

    def load_pair(self):
        a = self.service.ingest(OLD)
        b = self.service.ingest(NEW)
        self.assertEqual(a['status'], 'ok')
        self.assertEqual(b['status'], 'ok')
        self.assertEqual(len(b['proposals']), 1)
        return b['proposals'][0]

    def test_connected_intake_review_and_qa_preserve_originals(self):
        p = self.load_pair()
        self.assertEqual(p['reviewer'], 'Alice')
        self.assertEqual(p['status'], 'pending')
        self.assertEqual(p['support']['old_reason'][0]['quote'], OLD['source']['text'].split('. ')[1]+'.')
        self.assertEqual(self.service.review(p['id'], 'Bob', 'approve')['status'], 'invalid')
        approved = self.service.review(p['id'], 'Alice', 'approve')
        self.assertEqual(approved['proposals'][0]['status'], 'approved')
        result = self.service.ask('Which folder?', temporal_scope='historical')
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['answers'][0]['text'], 'Cedar-audit')
        self.assertEqual(self.calls[-1][1]['temporal_scope'], 'historical')
        self.assertEqual(self.calls[-1][1]['relations'][0]['status'], 'approved')
        self.assertEqual(set(self.service.store.load('sources')), {digest(OLD), digest(NEW)})
        self.assertFalse(result['answers'][0]['evidence'][0]['fully_superseded'])

    def test_duplicate_intake_does_not_run_model_and_refreshes_review_status(self):
        p = self.load_pair()
        self.service.review(p['id'], 'Alice', 'approve')
        before = (len(self.memory.engine.writes), len(self.calls))
        result = self.service.ingest(NEW)
        self.assertTrue(result['replayed'])
        self.assertEqual(result['proposals'][0]['status'], 'approved')
        self.assertEqual(before, (len(self.memory.engine.writes), len(self.calls)))

    def test_missing_native_provenance_uses_declared_original_retrieval(self):
        self.load_pair(); self.memory.miss = True
        result = self.service.ask('Which folder?')
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['answers'][0]['text'], 'Cedar-audit')
        self.assertIn('original_embedding_search', result['answers'][0]['evidence'][0]['source_origins'])
        self.assertTrue(any('provenance unavailable' in w for w in result['warnings']))

    def test_native_query_error_retains_cited_answer_as_partial(self):
        self.load_pair(); self.memory.fail_query = True
        result = self.service.ask('Which folder?')
        self.assertEqual(result['status'], 'partial')
        self.assertTrue(result['answers'])
        self.assertEqual(result['errors'][0]['stage'], 'native_query')

    def test_original_retrieval_failure_keeps_valid_native_originals(self):
        self.load_pair()
        with patch.object(self.memory.engine, 'rank', side_effect=RuntimeError('retrieval failure')):
            result = self.service.ask('Which folder?')
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['answers'][0]['text'], 'Cedar-audit')
        self.assertEqual(result['answers'][0]['evidence'][0]['source_origins'], ['native_provenance'])

    def test_empty_retrieval_is_insufficient_and_does_not_read_all_history(self):
        self.load_pair(); self.memory.miss = True; self.memory.engine.allowed = set()
        count = len(self.calls)
        result = self.service.ask('Unanswerable question')
        self.assertEqual(result['status'], 'insufficient')
        self.assertEqual(result['answers'], [])
        self.assertEqual(len(self.calls), count)

    def test_invalid_sibling_does_not_discard_valid_citation(self):
        self.load_pair()
        pid = next(p['id'] for p in passages(dict(sources=records_view([OLD]))) if 'folder' in p['quote'])
        self.forced = json.dumps(dict(kind='conditional', answers=[
            dict(text='Cedar-audit', evidence=[pid]), dict(text='invented', evidence=['unknown'])]))
        result = self.service.ask('Folder?')
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(len(result['answers']), 1)
        self.assertEqual(len(result['rejected_answers']), 1)

    def test_failed_write_preserves_source_and_requires_explicit_rebuild(self):
        self.service.ingest(OLD); self.memory.engine.fail = True
        self.assertEqual(self.service.ingest(NEW)['status'], 'error')
        self.assertIn(digest(NEW), self.service.store.load('sources'))
        self.assertEqual(self.service.ask('folder')['status'], 'needs_rebuild')
        self.memory.engine.fail = False
        result = self.service.rebuild()
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['source_count'], 2)
        count = len(self.memory.engine.writes)
        self.assertTrue(self.service.ingest(NEW)['replayed'])
        self.assertEqual(count, len(self.memory.engine.writes))

    def test_restart_requires_rebuild_and_preserves_review_votes(self):
        p = self.load_pair(); self.service.review(p['id'], 'Alice', 'approve')
        second = CUPMemService(Memory(), self.generate, self.service.store)
        self.assertEqual(second.ask('folder')['status'], 'needs_rebuild')
        self.assertEqual(second.rebuild()['status'], 'ok')
        self.assertEqual(timeline.proposals(second.store)[0]['status'], 'approved')

    def test_native_query_mutation_blocks_following_operations(self):
        self.load_pair(); self.memory.mutate = True
        result = self.service.ask('folder')
        self.assertEqual(result['status'], 'needs_rebuild')
        self.assertEqual(result['errors'][0]['stage'], 'native_query_state')

    def test_unprocessed_shared_source_never_enters_model_context(self):
        self.load_pair()
        future = source('NEVER_VISIBLE_FUTURE_CONTENT', 30)
        capture(self.service.store, future)
        self.service.ask('folder')
        self.assertNotIn('NEVER_VISIBLE', json.dumps(self.calls[-1]))
        self.assertFalse(any(p['source_id'] == digest(future) for p in self.memory.engine.rank_calls[-1]))

    def test_unrelated_report_does_not_create_proposal_or_supersede_observation(self):
        p = self.load_pair()
        other = source('Birch project changed its meeting room to B302.', 3)
        result = self.service.ingest(other)
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['proposals'], [])
        self.assertEqual(len(timeline.proposals(self.service.store)), 1)
        self.assertEqual(self.service.ask('folder')['answers'][0]['text'], 'Cedar-audit')

    def test_current_correction_is_scoped_and_historical_answer_survives(self):
        self.service.ingest(OLD)
        corrected = source('The earlier folder was a typo. The correct folder is Cedar-archive.', 4, 'Bob')
        self.forced = '{"relations":[]}'
        self.service.ingest(corrected)
        old_quote = 'The folder is Cedar-audit.'
        proposal = dict(kind='correction', previous=timeline.witness(OLD, old_quote),
            incoming=timeline.witness(corrected, corrected['source']['text']), reason='Explicit correction',
            reviewer='Alice', history=[digest(OLD)])
        pid = self.service.store.put('timeline_proposals', proposal)
        self.service.review(pid, 'Alice', 'approve')
        self.forced = None
        current = self.service.ask('What is the current folder?')
        self.assertEqual(current['status'], 'partial')
        self.assertTrue(current['answers'][0]['evidence'][0]['fully_superseded'])
        past = self.service.ask('What folder was originally recorded?', temporal_scope='historical')
        self.assertEqual(past['status'], 'ok')
        self.assertEqual(past['answers'][0]['text'], 'Cedar-audit')
        self.assertIn(digest(corrected), current['source_origins'])

    def test_invalid_request_and_output_are_structured(self):
        self.assertEqual(self.service.handle({'operation':'ingest','source':{}})['status'], 'invalid')
        self.assertEqual(self.service.handle({'operation':'ask'})['status'], 'invalid')
        self.service.ingest(OLD); self.forced = 'not JSON'
        result = self.service.ask('folder')
        self.assertEqual(result['status'], 'invalid')
        self.assertEqual(result['answers'], [])


class StructuredReviewTests(unittest.TestCase):
    def row(self):
        a = passages(dict(sources=records_view([OLD])))[1]['id']
        b = passages(dict(sources=records_view([NEW])))[0]['id']
        return dict(kind='reconsider', old_claim=[a], new_claim=[b], old_reason=[a],
                    old_condition=[a], new_condition=[b], reason='Deployment constraint changed')

    def test_missing_reason_is_not_accepted_as_reconsideration(self):
        row = self.row(); row['old_reason'] = []
        result = review_sources([OLD, NEW], NEW, lambda *_: json.dumps({'relations':[row]}))
        self.assertEqual(result['status'], 'invalid')
        self.assertEqual(result['proposals'], [])

    def test_swapped_or_unknown_evidence_is_rejected_individually(self):
        good = self.row(); wrong = dict(good, new_condition=good['old_condition'])
        result = review_sources([OLD, NEW], NEW, lambda *_: json.dumps({'relations':[wrong, good]}))
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(len(result['proposals']), 1)


class NativeAdapterTests(unittest.TestCase):
    def test_native_query_failure_cannot_hide_persistent_mutation(self):
        class MutatingEngine:
            def __init__(self): self.chunks = []
            def _build_sample_result(self, **kwargs):
                return dict(final_profile_snapshot={}, chunk_bank=list(self.chunks), delta_store=[])
            def answer_query(self, **kwargs):
                self.chunks.append({'unexpected': True})
                raise RuntimeError('failure after mutation')
        client = SimpleNamespace(parse_json_object_with_repair=lambda raw: (json.loads(raw), 'json'))
        with patch.dict(sys.modules, {'cup_mem.llm_layer.client':client}):
            adapter = CUPMemTeamMemory(MutatingEngine(), lambda: [])
            with self.assertRaisesRegex(AssertionError, 'persistent memory'):
                adapter.ask('query')

    def test_unbound_composer_is_diagnostic_not_fabricated_citation(self):
        class QueryEngine:
            def _build_sample_result(self, **kwargs):
                return dict(final_profile_snapshot={}, chunk_bank=[], delta_store=[])
            def answer_query(self, **kwargs):
                return dict(answer={'answer':'native'}, debug_trace={})
        client = SimpleNamespace(parse_json_object_with_repair=lambda raw: (json.loads(raw), 'json'))
        with patch.dict(sys.modules, {'cup_mem.llm_layer.client':client}):
            result = CUPMemTeamMemory(QueryEngine(), lambda: []).ask('query')
        self.assertEqual(result['answer']['answer'], 'native')
        self.assertEqual(result['citations'], [])
        self.assertTrue(result['provenance_errors'])


if __name__ == '__main__': unittest.main()
