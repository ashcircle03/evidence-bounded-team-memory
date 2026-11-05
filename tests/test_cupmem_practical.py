"""Practical-path integration and failure boundaries, not model accuracy tests."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from team_memory.cupmem_candidates import CUPMemCandidateMemory, SourceOnlyMemory, sources_for_hits
from team_memory.cupmem_practical import PracticalCUPMemService
from team_memory.store import capture, digest, source_envelope


def source(text, day=1, owner='Alice'):
    return source_envelope(dict(owner=owner, observed_at=f'2025-01-{day:02d}T00:00:00Z',
        source=dict(speaker=owner, location=f'source://{owner}/{day}', text=text)))


OLD = source('The folder is Cedar-audit. We stopped Cedar trials because deployment permits one process.')
NEW = source('Deployment now permits four processes.', 2, 'Bob')


class Engine:
    def __init__(self):
        self.embedding = self
        self.writes = []
        self.fail_at = None

    def rank(self, *, query_text, candidates, text_getter, top_k):
        return [dict(item=p, score=1.0) for p in candidates[:top_k]]

    def write_session(self, **kwargs):
        self.writes.append(deepcopy(kwargs))
        if self.fail_at == len(self.writes):
            raise RuntimeError('partial native failure')
        return dict(session_index=kwargs['session_index'])

    def answer_query(self, **kwargs):
        raise AssertionError('Must not generate and discard an intermediate answer')

    def reset(self):
        self.writes.clear()


class CandidateMemory(CUPMemCandidateMemory):
    def candidates(self, question):
        return dict(records=self.sources[:], memory_annotations={}, warnings=[])


class PracticalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.calls = []
        self.engine = Engine()
        self.memory = CandidateMemory(self.engine, lambda: [])
        self.service = PracticalCUPMemService(self.memory, self.generate, self.tmp.name)

    def generate(self, system, content):
        data = json.loads(content); self.calls.append((system, data))
        if 'earlier' in data:
            if not any('four processes' in p['quote'] for p in data['incoming']):
                return '{"relations":[]}'
            old = next(p['id'] for p in data['earlier'] if 'We stopped' in p['quote'])
            new = data['incoming'][0]['id']
            return json.dumps(dict(relations=[dict(kind='reconsider', old_claim=[old], new_claim=[new],
                old_condition=[old], old_reason=[old], new_condition=[new],
                reason='Reconsider the suspension because its deployment constraint changed.')]))
        p = next(p for p in data['passages'] if 'Cedar-audit' in p['quote'])
        return json.dumps(dict(kind='single', answers=[dict(text='Cedar-audit', evidence=[p['id']])]))

    def test_connected_single_readout_and_owner_only_review(self):
        self.assertEqual(self.service.ingest(OLD)['status'], 'ok')
        result = self.service.ingest(NEW)
        self.assertEqual(result['status'], 'ok'); p = result['proposals'][0]
        self.assertEqual(p['status'], 'pending')
        before = len(self.calls)
        answer = self.service.ask('What is the folder?')
        self.assertEqual(len(self.calls)-before, 1)
        self.assertEqual(answer['status'], 'ok')
        self.assertEqual(answer['answers'][0]['evidence'][0]['quote'], 'The folder is Cedar-audit.')
        self.assertEqual(self.service.review(p['id'], 'Bob', 'approve')['status'], 'invalid')
        self.assertEqual(self.service.review(p['id'], 'Alice', 'approve')['proposals'][0]['status'], 'approved')
        count = len(self.calls)
        again = self.service.ingest(NEW)
        self.assertTrue(again['replayed']); self.assertEqual(len(self.calls), count)
        self.assertEqual(again['proposals'][0]['status'], 'approved')
        self.assertEqual(len(self.service.store.load('sources')), 2)

    def test_shared_qa_exact_input_and_output_when_no_team_links(self):
        self.service.import_history([OLD, NEW])
        self.service.ask('What is the folder?')
        candidate_input = deepcopy(self.calls[-1])
        control = PracticalCUPMemService(SourceOnlyMemory(Engine()), self.generate,
            Path(self.tmp.name)/'simple', strategy='simple')
        control.import_history([OLD, NEW]); answer = control.ask('What is the folder?')
        self.assertEqual(candidate_input, self.calls[-1])
        self.assertEqual(answer['answers'][0]['text'], 'Cedar-audit')

    def test_native_candidate_failure_degrades_review_not_qa(self):
        self.service.ingest(OLD)
        def fail(_): raise RuntimeError('profile error')
        self.memory.candidates = fail
        self.assertEqual(self.service.ingest(NEW)['status'], 'partial')
        self.assertEqual(self.service.ask('What is the folder?')['status'], 'ok')

    def test_each_review_has_only_one_prior_source_and_the_actual_incoming(self):
        self.service.ingest(OLD); self.service.ingest(NEW)
        before = len(self.calls)
        unrelated = source('The Birch meeting moved to room B302.', 3, 'Cara')
        result = self.service.ingest(unrelated)
        self.assertEqual(result['status'], 'ok'); self.assertEqual(result['proposals'], [])
        self.assertEqual(len(result['review_traces']), 2)
        for _, payload in self.calls[before:]:
            self.assertEqual(len({p['source_id'] for p in payload['earlier']}), 1)
            self.assertEqual({p['source_id'] for p in payload['incoming']}, {digest(unrelated)})

    def test_candidate_mutation_blocks_further_operations(self):
        self.service.ingest(OLD)
        def mutate(_): raise AssertionError('native state changed')
        self.memory.candidates = mutate
        self.assertEqual(self.service.ingest(NEW)['status'], 'error')
        self.assertEqual(self.service.ask('What is the folder?')['status'], 'needs_rebuild')

    def test_bulk_native_writes_preserve_each_turn_and_new_session_index(self):
        result = self.service.import_history([OLD, NEW])
        self.assertEqual(result['status'], 'ok'); self.assertEqual(result['batches'], 1)
        call = self.engine.writes[0]
        self.assertEqual([json.loads(t['content']) for t in call['session']], [OLD, NEW])
        self.assertEqual(call['session_time'], NEW['observed_at'])
        self.assertEqual(len(self.calls), 0)
        later = source('Other project meeting is Tuesday.', 3)
        self.service.ingest(later)
        self.assertEqual(self.engine.writes[-1]['session_index'], 1)

    def test_failed_bulk_preserves_all_originals_and_rebuilds_exact_batches(self):
        self.engine.fail_at = 2
        result = self.service.import_history([OLD, NEW], max_batch_records=1)
        self.assertEqual(result['status'], 'error')
        self.assertEqual(len(self.service.store.load('sources')), 2)
        self.assertEqual(len(self.memory.sources), 1)
        self.assertEqual(self.service.ask('What is the folder?')['status'], 'needs_rebuild')
        self.engine.fail_at = None
        self.assertEqual(self.service.rebuild()['status'], 'ok')
        self.assertEqual(self.memory.sources, [OLD, NEW])
        self.assertEqual(len(self.engine.writes), 2)

    def test_import_invalid_before_any_mutation(self):
        for records in [[OLD, OLD], [OLD, {}], None]:
            self.assertEqual(self.service.import_history(records)['status'], 'invalid')
            self.assertEqual(self.service.store.load('sources'), {})
        self.assertEqual(self.service.import_history([OLD], max_batch_chars=10)['status'], 'invalid')
        self.assertEqual(self.service.store.load('sources'), {})

    def test_rebuild_preserves_votes_after_restart(self):
        self.service.ingest(OLD); p = self.service.ingest(NEW)['proposals'][0]
        self.service.review(p['id'], 'Alice', 'approve')
        restored = PracticalCUPMemService(CandidateMemory(Engine(), lambda: []), self.generate, self.tmp.name)
        self.assertEqual(restored.ask('What is the folder?')['status'], 'needs_rebuild')
        self.assertEqual(restored.rebuild()['status'], 'ok')
        self.assertEqual(restored._links()[0]['status'], 'approved')

    def test_unprocessed_source_cannot_leak_and_limits_are_explicit(self):
        self.service.ingest(OLD)
        capture(self.service.store, source('The folder is a future secret.', 5))
        answer = self.service.ask('What is the folder?')
        self.assertEqual(len(answer['source_origins']), 1)
        self.service.max_source_passages = 1
        self.assertEqual(self.service.ask('What is the folder?')['status'], 'error')

    def test_simple_compare_reuses_core_without_native_writer(self):
        def simple(system, content):
            p = json.loads(content)
            return json.dumps(dict(relations=[dict(kind='reconsider',
                old_evidence=[p['earlier'][1]['id']], new_evidence=[p['incoming'][0]['id']],
                reason='The condition changed.')]))
        engine = Engine(); control = PracticalCUPMemService(SourceOnlyMemory(engine), simple,
            Path(self.tmp.name)/'simple', strategy='simple')
        control.ingest(OLD); result = control.ingest(NEW)
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['proposals'][0]['status'], 'pending')
        self.assertEqual(engine.writes, [])


class CandidateProvenanceTests(unittest.TestCase):
    def test_multiturn_exact_origin_and_invalid_sibling_isolation(self):
        session = dict(session_id='s_000', session_index=0, session_time=NEW['observed_at'],
            user_turns=[dict(turn_id='t_0', content=json.dumps(OLD)), dict(turn_id='t_1', content=json.dumps(NEW))])
        item = dict(item_id='i1', bucket='b', local_track='t', status='ACTIVE', active_strength='STRONG',
                    evidence_chunk_ids=['c1'], source_delta_ids=[], revision_history=[])
        trace = dict(session_logs=[session], final_profile_snapshot=dict(active_profile={'b/t':[item]},
                     stale_archive=[], unknown_current=[]), chunk_bank=[dict(chunk_id='c1', session_id='s_000',
                     source_turn_ids=['t_1'])], delta_store=[])
        hit = dict(source='active', source_detail='strong_active', id='i1', bucket='b', local_track='t')
        result = sources_for_hits('query', [dict(hit, id='absent'), hit], trace, [OLD, NEW])
        self.assertEqual(result['records'], [NEW]); self.assertEqual(len(result['warnings']), 1)
        result = sources_for_hits('query', [hit], trace, [OLD])
        self.assertEqual(result['records'], []); self.assertEqual(len(result['warnings']), 1)


if __name__ == '__main__': unittest.main()
