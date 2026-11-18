"""Replay the fixed combined arm and compare individually identified edges after persistence."""
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import subprocess
import sys
from evaluation.record_binding.discourse.evaluate import edge_identity
from evaluation.record_binding.discourse.evaluate_scope import OUT, SOURCE
from evaluation.record_binding.first_loss import reader_packets, read
from evaluation.record_bound.rows import compiled_rows
from evaluation.record_full.evaluate import score
from team_memory.records import discourse_roles, policy_scope


def main():
    for name, digest in read(OUT / 'freeze.json')['files'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest() == digest, name
    docs = {d['id']: d for d in read('evaluation/record_full/gold.json')['documents']}
    raw = {d['id']: d for d in read(SOURCE / 'record-pair-v1/inputs.json')}
    prior = read(OUT / 'evaluation.json')['cases']
    assert set(raw) == set(docs) == {c['id'] for c in prior} and len(prior) == 68
    # Keep the trained parser's native dependencies isolated from the frozen scorer.
    worker = subprocess.run([sys.argv[1], '-m', 'evaluation.record_binding.discourse.policy_predictions'],
        input=json.dumps([c['pairs'] for c in prior]), text=True, capture_output=True, check=True)
    syntax = json.loads(worker.stdout)
    cases = []
    with TemporaryDirectory() as tmp:
        for c in prior:
            iid = c['id']
            item, gold = raw[iid], docs[iid]
            source, original = item['source'], item['original_raw']
            assert c['pairs'] == discourse_roles.candidates(source, original)
            assert hashlib.sha256(source['text'].encode()).hexdigest() == gold['source_sha256']
            old = c['results']['combined']
            traces = syntax['rows'][len(cases)]
            decisions = policy_scope.merge(old['decisions'], traces)
            results = []
            for roles in (old['decisions'], decisions):
                graph = discourse_roles.apply(source, original, lambda _: roles, model='paired')
                record = dict(source, record_graph=graph)
                rows = compiled_rows(record)
                result = score(rows, gold, source)
                errors = {edge_identity(e, record, rows) for e in result['incorrect_edges']}
                results.append((graph, result, errors))
            (g0, a, bad), (g1, b, now_bad) = results
            reader_packets(dict(source, record_graph=g1), Path(tmp) / iid)
            assert a['typed_edges'] == old['typed'] and a['complete'] == old['complete']
            missing_a, missing_b = set(a['missing_edges']), set(b['missing_edges'])
            assert g0['units'] == g1['units'] and g0['status'] == g1['status']
            assert [[c['assertions'], c['stance']] for c in g0['claims']] == [
                [c['assertions'], c['stance']] for c in g1['claims']]
            assert all(a[k] == b[k] for k in ('missing_nodes', 'missing_claims', 'stance_wrong', 'stance_missing'))
            changed = [dict(index=p['index'], span=p['context'], syntax=t)
                       for p, t, x, y in zip(c['pairs'], traces, old['decisions'], decisions) if x != y]
            cases.append(dict(id=iid, panel=c['panel'], before=a['typed_edges'], after=b['typed_edges'],
                old_complete=a['complete'], complete=b['complete'], lost=sorted(missing_b-missing_a),
                gained=sorted(missing_a-missing_b), new_fp=sorted(now_bad-bad),
                removed_fp=sorted(bad-now_bad), changes=changed))
    report = dict(spacy=syntax['spacy'], parser=syntax['parser'], cases=cases)
    Path('results/record-binding/policy-scope/evaluation.json').write_text(json.dumps(report,indent=2)+'\n')
    assert sum(c['before']['tp'] for c in cases) == 50
    assert all(not c['lost'] and not c['new_fp'] and (not c['old_complete'] or c['complete']) for c in cases)
    for panel in sorted({c['panel'] for c in cases}):
        selected = [c for c in cases if c['panel']==panel]
        print(panel, {k:sum(c['after'][k] for c in selected) for k in ('tp','fp','fn')},
              'complete',sum(c['complete'] for c in selected))
    print('changed', [c['id'] for c in cases if c['changes']])


if __name__ == '__main__':
    main()
