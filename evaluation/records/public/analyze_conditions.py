"""Why each of the 49 condition cases is missed, per run (same rule as public_score).

A case is a hit when a stored condition span equals the gold antecedent exactly
and the claim assertion it is attached to lies inside the gold consequent.
Misses are put in one first-failing category:
  failed_doc         the document has no accepted claims (status failed)
  role_missing       the antecedent text sits inside a claim span, not as a condition
  no_condition       no condition span overlaps the antecedent at all
  boundary           a condition overlaps the antecedent but its exact span differs
  claim_scope        the exact condition is attached, but the assertion is not inside
                     the consequent (for example the claim covers the whole sentence)
Also counts diagnostics reasons over all documents and keeps raw model outputs of a
few condition documents per run.

  python analyze_conditions.py <requirements.json> <out.json> name=path.jsonl ...
"""
from collections import Counter
import json
import sys
from pathlib import Path

SAMPLES = 4


def spans_of(graph, ids):
    units = {u['id']: u for u in graph['units']}
    runs = []
    for uid in ids:
        u = units[uid]
        if runs and runs[-1][1] <= u['start'] and not graph_text[0][runs[-1][1]:u['start']].strip():
            runs[-1][1] = u['end']
        else:
            runs.append([u['start'], u['end']])
    return [tuple(r) for r in runs]


graph_text = ['']


def analyze_case(case, row):
    text = case['text']
    graph_text[0] = text
    graph = row['graph']
    x = text.index(case['condition']); y = x + len(case['condition'])
    a = text.index(case['action']); b = a + len(case['action'])
    units = {u['id']: u for u in graph['units']}
    claims = graph['claims']
    detail = dict(status=graph['status'], claims=[], diagnostics=[d['reason'][:120] for d in graph.get('diagnostics', [])])
    hit = False
    exact_attached = []
    overlapping = []
    in_claim = False
    for c in claims:
        # Same as evaluation/record_layout/score.edges: first unit start .. last unit end.
        assertions = [(units[s['unit_ids'][0]]['start'], units[s['unit_ids'][-1]]['end']) if s['unit_ids'] else None
                      for s in (c.get('assertions') or [dict(unit_ids=c['claim'])])]
        conds = spans_of(graph, c['condition'])
        claim_runs = spans_of(graph, c['claim'])
        detail['claims'].append(dict(
            claim=[text[s:e] for s, e in claim_runs], condition=[text[s:e] for s, e in conds],
            subject=[text[s:e] for s, e in spans_of(graph, c['subject'])],
            basis=[text[s:e] for s, e in spans_of(graph, c['basis'])]))
        for s, e in claim_runs:
            if s <= x and y <= e:
                in_claim = True
        for s, e in conds:
            if (s, e) == (x, y):
                exact_attached.append(assertions)
                for asr in assertions:
                    if asr and a <= asr[0] < asr[1] <= b:
                        hit = True
            elif s < y and x < e:
                overlapping.append(text[s:e])
    if hit:
        category = 'hit'
    elif not claims:
        category = 'failed_doc'
    elif exact_attached:
        category = 'claim_scope'
    elif overlapping:
        category = 'boundary'
        detail['boundary'] = dict(gold=case['condition'], predicted=overlapping)
    elif in_claim:
        category = 'role_missing'
    else:
        category = 'no_condition'
    detail.update(gold_condition=case['condition'], gold_action=case['action'])
    return category, detail


def main():
    req, out = Path(sys.argv[1]), Path(sys.argv[2])
    runs = dict(arg.split('=', 1) for arg in sys.argv[3:])
    cases = {c['id']: c for c in json.loads(req.read_text())['cases']}
    report = dict(cases=len(cases), runs={})
    for name, path in runs.items():
        rows = {}
        reasons = Counter()
        statuses = Counter()
        claim_total = 0
        for line in Path(path).read_text().splitlines():
            row = json.loads(line)
            rows[row['id']] = row
            g = row['graph']
            statuses[g['status']] += 1
            claim_total += len(g['claims'])
            for d in g.get('diagnostics', []):
                reasons[d['reason'].split(':')[0] + ': ' + d['reason'].split(':', 1)[-1].strip()[:50]] += 1
        categories = Counter()
        per_case = {}
        for cid, case in cases.items():
            if cid not in rows:
                categories['missing_row'] += 1
                continue
            category, detail = analyze_case(case, rows[cid])
            categories[category] += 1
            per_case[cid] = dict(category=category, **detail)
        samples = []
        for cid in list(cases)[:SAMPLES]:
            if cid in rows:
                samples.append(dict(id=cid, text=cases[cid]['text'],
                                    calls=[c['output'][:1500] for c in rows[cid]['calls']]))
        report['runs'][name] = dict(categories=dict(categories), statuses=dict(statuses), claims=claim_total,
                                    diagnostics=dict(reasons.most_common(15)), cases=per_case, samples=samples)
        print(name, dict(categories), dict(statuses), 'claims', claim_total)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
