"""Exercise answer.generate with fixed decoder strings; no model or retrieval scores."""
import argparse
import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Lock

from team_memory.adapters.answering import AnsweringAdapter
from team_memory.contracts.ports import CallContext


def run():
    root = Path(__file__).resolve().parents[2]
    cases = {c['name']: c for c in json.loads((root/'examples/contracts/cases.json').read_text())}
    rows = []
    specs = [
        ('answer-reconsider-is-not-correction', 'Review is authorized; no changed execution decision or successful experiment is recorded [1][2][3].'),
        ('answer-hook-v1', 'Parallel hooks crash in v1 [1].'),
        ('answer-hook-by-version', 'Parallel hooks crash in v1 [1]. The parallel hook issue is fixed in v2 [2].'),
        ('answer-unrelated-conflict-does-not-block', 'Hana owns the report [1].'),
        ('answer-pending-keeps-current', 'The recorded latency is 120ms [1]. The 90ms correction is pending and has not replaced 120ms [2][3].'),
        ('answer-conflict-both-alternatives', 'Hana reports 120ms [1]. Jun reports 90ms [2].'),
        ('disjoint-quotes', 'Hana owns the report [4]. The measurement was repeated [5].'),
    ]
    for name, draft in specs:
        source = 'answer-unrelated-conflict-does-not-block' if name == 'disjoint-quotes' else name
        case = deepcopy(cases[source])
        req = case['request']
        bundle = req['payload']['bundle']
        if name == 'disjoint-quotes':
            candidate = bundle['snapshot']['proposals'][0]['candidate']
            bundle['query']['text'] = 'Who owns the report and was the measurement repeated?'
            for side, evidence in zip(('previous','incoming'), bundle['evidence'][:2]):
                cut = evidence['quote'].index('.') + 1
                candidate[side].update(end=cut,quote=evidence['quote'][:cut])
                part = deepcopy(evidence)
                part.update(id='detail-'+side,start=cut+1,quote=evidence['quote'][cut+1:])
                bundle['evidence'].append(part)
        captured = {}
        class Decoder:
            lock = Lock()
            llm = None
            def generate_evidence(self, question, witnesses, review):
                captured['conditions_at_generation'] = [w.get('conditions', []) for w in witnesses]
                return dict(status='ok', raw=draft, citation_sources=witnesses)
        class ScopedDecoder(Decoder):
            def generate_scoped(self, query, evidence):
                from team_memory.readers.scoped import CitedFact, ScopedDraft
                # Synthetic generator outputs to exercise transport, not semantic evaluation.
                indices = {
                    'answer-hook-v1': [0], 'answer-hook-by-version': [0, 1],
                    'answer-reconsider-is-not-correction': [2],
                }[name]
                facts = [draft] if len(indices)==1 else ['Parallel hooks crash in v1 [1].', 'The parallel hook issue is fixed in v2 [2].']
                rows = [CitedFact(fact=fact, evidence_id=evidence[i]['id'], substring_quote=[evidence[i]['quote']])
                          for fact, i in zip(facts, indices)]
                return ScopedDraft(claims=rows, comparison='fixed response', same_answer=len(indices)==1, reason='')
        with TemporaryDirectory() as cache:
            port = AnsweringAdapter('demo',lambda store: ScopedDecoder(),Path(cache),snapshot_loader=lambda _:bundle['snapshot'])
            res = port.handle(req,context=CallContext('demo','hana',frozenset(['answer:generate'])))
        assert res['status']=='ok', res
        a=res['data']
        rows.append(dict(case=name, draft=draft, **captured, raw_preserved=a['original_text']==draft,
                         outcome=a['outcome'],claims=a['claims']))
    return rows


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args=parser.parse_args()
    args.output.write_text(json.dumps(run(), indent=2,ensure_ascii=False)+'\n')
