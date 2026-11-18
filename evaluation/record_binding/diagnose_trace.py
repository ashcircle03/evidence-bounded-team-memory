"""Offline frozen-gold inspection of native traces, never an inference input."""
import json
from pathlib import Path
from evaluation.record_full.evaluate import matches


def normalize(value):
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in value.items() if k != 'confidence'}
    if isinstance(value, list):
        return sorted((normalize(v) for v in value), key=lambda x: json.dumps(x, sort_keys=True))
    return value


def main():
    root = Path('results/record-binding/v2')
    trace = json.loads((root/'record-trace-123008.json').read_text())
    assert trace['status'] == 'complete' and len(trace['rows']) == 136
    old = {a: {x['id']: x['prediction'] for x in json.loads(Path(p).read_text())['rows']}
           for a, p in [('native', 'results/record-binding/v1/record-binding-122996.json'),
                        ('adapted', 'results/record-binding/v1/record-adapt-122997.json')]}
    gold = {d['id']: d for d in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    rows = []; equal = 0; exact_equal = 0
    for record in trace['rows']:
        previous = old[record['arm']][record['id']]
        exact_equal += previous == record['prediction']
        assert normalize(previous) == normalize(record['prediction']), (record['arm'], record['id'])
        equal += 1
        d = gold[record['id']]; t = record['trace']
        for n in d['nodes']:
            if n['role'] not in ('condition', 'basis') or not n['required']:
                continue
            indices = [(i, p) for i, p in enumerate(t['pool']) if matches(p['text'], n)]
            exact = [(i, p) for i, p in indices if any(p['start'] == s['start'] and p['end'] == s['end'] for s in n['spans'])]
            core = next(x for x in d['nodes'] if x['record_id'] == n['record_id'] and x['role'] == 'claim')
            anchors = [a for a in t['anchors'] if matches(a['text'], core)]
            details = []
            for i, p in exact:
                details.append(dict(quote=p['text'], candidate_probability=p['probabilities'][n['role']],
                    anchor_assignments=[dict(quote=a['text'], selected=a['selected'],
                        anchor_probability=a['probability'], assignment_probability=a['assignments'][n['role']][i]) for a in anchors]))
            rows.append(dict(id=record['id'], panel=d['panel'], arm=record['arm'], node=n['id'], role=n['role'],
                expected_quote=n['text'], covering_candidates=len(indices), exact_candidates=details,
                covering_candidate_max_probability=max((p['probabilities'][n['role']] for _, p in indices), default=None),
                matching_recorded_anchors=len(anchors), selected_matching_anchors=sum(a['selected'] for a in anchors)))
    counts = []
    for panel in ('balanced_synthetic', 'natural_audit'):
        for arm in ('native', 'adapted'):
            ss = [r for r in rows if r['panel'] == panel and r['arm'] == arm]
            counts.append(dict(panel=panel, arm=arm, nodes=len(ss),
                any_covering_candidate=sum(bool(r['covering_candidates']) for r in ss),
                exact_gold_span_candidate=sum(bool(r['exact_candidates']) for r in ss),
                any_covering_candidate_above_threshold=sum((r['covering_candidate_max_probability'] or 0) >= .5 for r in ss),
                selected_matching_anchor=sum(bool(r['selected_matching_anchors']) for r in ss)))
    result = dict(semantic_outputs_reproduced=equal, bytewise_prediction_dicts_equal=exact_equal,
        note='Confidence values can differ numerically across executions; all spans and edges agree. Covering candidates can be oversized. Exact candidates are reported separately. Recorded anchor subset includes selected native and exact original Qwen anchors; absent unselected anchors were not exhaustively instrumented. The trace truncated=false field is a default marker, not a measured truncation check.',
        gold_used_only_after_inference=True, counts=counts, rows=rows)
    (root/'native-diagnosis.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    main()
