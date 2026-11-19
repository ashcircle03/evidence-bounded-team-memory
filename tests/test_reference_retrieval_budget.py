"""Evidence budget keeps review state and both sides of its proposal before other evidence.

Real LlamaIndex/BM25 with mock embeddings and a stub decoder; not retrieval quality.
"""
import json
from pathlib import Path
import unittest

from tests import test_reference_qa as reference
from tests import test_reference_module_adapters as adapters


@unittest.skipUnless(reference.AVAILABLE, 'reference dependencies and tokenizer required')
class EvidenceBudgetTests(unittest.TestCase):
    setUp = adapters.ModuleFlowTests.setUp
    compare = adapters.ModuleFlowTests.compare
    respond = adapters.ModuleFlowTests.respond
    make = adapters.ModuleFlowTests.make
    call = adapters.ModuleFlowTests.call
    source = adapters.ModuleFlowTests.source

    def conflict_with_unrelated_record(self):
        g = self.make(Path(self.temp.name) / 'budget')
        self.call(g.records, 'record.append', dict(source=self.source('The timeout is 10 seconds.'),
                                                   expected_revision=0, idempotency_key='old'))

        def compare(_, content):
            d = json.loads(content)
            return json.dumps(dict(relations=[dict(kind='conflict', target=d['earlier'][0]['id'],
                old_sentence_ids=[0], new_sentence_ids=[0], reason='Incompatible timeouts under the same settings.')]))
        g.relations.generate = compare
        ingested = self.call(g, 'gateway.ingest', dict(source=self.source('The timeout is 20 seconds.', 'jun', 'test:new'),
                                                       expected_revision=1, idempotency_key='new'))
        self.assertEqual(ingested['status'], 'ok', ingested)
        appended = self.call(g.records, 'record.append', dict(source=self.source('Archive is Orion.', location='test:archive'),
            expected_revision=g.records.snapshot()['revision'], idempotency_key='archive'))
        self.assertEqual(appended['status'], 'ok', appended)
        return g

    def retrieve(self, g, limit):
        return self.call(g.retrieval, 'evidence.retrieve', dict(snapshot=g.records.snapshot(),
            query=dict(text='What timeouts are reported?', time_scope='current', as_of=None, conditions=[]),
            max_evidence=limit))

    @staticmethod
    def labels(response):
        out = []
        for e in response['data']['evidence']:
            out.append('state' if e['kind'] == 'review_state' else
                       '10s' if '10 seconds' in e['quote'] else '20s' if '20 seconds' in e['quote'] else 'other')
        return out

    def test_budget_keeps_state_and_both_sides_in_original_order(self):
        g = self.conflict_with_unrelated_record()
        full = self.retrieve(g, 10)
        self.assertEqual(full['status'], 'ok', full)
        self.assertEqual(sorted(self.labels(full)), ['10s', '20s', 'other', 'state'])
        pid = g.records.snapshot()['proposals'][0]['id']
        self.assertEqual(full['data']['unresolved_proposal_ids'], [pid])
        order = [e['id'] for e in full['data']['evidence']]

        cases = {3: ['10s', '20s', 'state'], 2: ['other', 'state'], 1: ['state']}
        for limit, expected in cases.items():
            with self.subTest(limit=limit):
                result = self.retrieve(g, limit)
                self.assertEqual(result['status'], 'partial', result)
                self.assertEqual(result['data']['coverage'], 'incomplete')
                self.assertEqual([e['code'] for e in result['errors']], ['BUDGET_EXCEEDED'])
                self.assertEqual(sorted(self.labels(result)), sorted(expected))
                ids = [e['id'] for e in result['data']['evidence']]
                self.assertEqual(ids, [i for i in order if i in ids])  # original order and IDs
                self.assertEqual(result['data']['unresolved_proposal_ids'], [pid])
        self.assertEqual(self.calls, [])

    def test_within_budget_is_unchanged(self):
        g = self.conflict_with_unrelated_record()
        full = self.retrieve(g, 10)
        exact = self.retrieve(g, len(full['data']['evidence']))
        self.assertEqual(exact['status'], 'ok')
        self.assertEqual(exact['data'], full['data'])

    def test_gateway_still_abstains_when_the_bundle_is_incomplete(self):
        g = self.conflict_with_unrelated_record()
        g.max_evidence = 3
        calls = len(self.calls)
        answer = self.call(g, 'gateway.ask', dict(query=dict(text='What timeouts are reported?', time_scope='current',
                                                             as_of=None, conditions=[]), snapshot_id=None))
        self.assertEqual(answer['status'], 'partial', answer)
        self.assertEqual(answer['data']['answer']['outcome'], 'abstained')
        self.assertEqual(sorted(self.labels(dict(data=answer['data']['bundle']))), ['10s', '20s', 'state'])
        self.assertEqual(len(self.calls), calls)


if __name__ == '__main__':
    unittest.main()
