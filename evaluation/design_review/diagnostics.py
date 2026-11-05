"""Reproducible stage and paired-case summaries; does not change semantic ratings."""
from collections import Counter
import json
from .build import ROOT, write

OUT = ROOT / 'results/design_review'


def read(name):
    return json.loads((OUT / name).read_text())


def diagnostics():
    rows, counts = read('rows.json'), read('counts.json')
    assert len(rows) == 300
    stages, paired, gates = {}, {}, {}
    for group in counts:
        selected = [r for r in rows.values() if '/'.join((r['model'], r['view'], r['method'])) == group]
        positive = [r for r in selected if r['expected'] == 'review']
        negative = [r for r in selected if r['expected'] == 'keep']
        stages[group] = dict(
            positive_opened=sum(r['opened'] for r in positive),
            positive_correct_target=sum(r['opened'] and r['target'] for r in positive),
            positive_semantic_eligible=sum(bool(r['card_id']) for r in positive),
            positive_grounded=sum(r['grounded'] for r in positive),
            positive_wrong_target=sum(r['opened'] and not r['target'] for r in positive),
            positive_keep=sum(r['action'] == 'keep' for r in positive),
            positive_invalid=sum(r['action'] in ('invalid_output', 'execution_error') for r in positive),
            negative_false_positive=sum(r['opened'] for r in negative),
            negative_invalid=sum(r['action'] in ('invalid_output', 'execution_error') for r in negative),
            total_opened_without_strict_support=sum(r['opened'] and not r['grounded'] for r in selected))
        if group.endswith('/module'):
            gates[group] = dict(Counter(r['result'].get('basis', r['action']) for r in positive))
    for model in ('3b', '14b'):
        for view in ('raw', 'hidden'):
            direct = set(counts[f'{model}/{view}/direct-full']['successes'])
            module = set(counts[f'{model}/{view}/module']['successes'])
            paired[f'{model}/{view}'] = dict(both=sorted(direct & module),
                direct_only=sorted(direct - module), module_only=sorted(module - direct))
        full = set(counts[f'{model}/hidden/direct-full']['successes'])
        oracle = set(counts[f'{model}/hidden/direct-oracle']['successes'])
        paired[f'{model}/hidden/oracle_vs_full'] = dict(both=sorted(full & oracle),
            full_only=sorted(full - oracle), oracle_only=sorted(oracle - full))
    raw = {}
    for model, name in [('3b', 'small.json'), ('14b', 'large.json'), ('14b', 'large-factorial.json')]:
        raw.update({model + '/' + uid: r for uid, r in read(name)['results'].items()})
    raw.update({'3b/' + uid: r for uid, r in read('oracle-repair.json')['results'].items()
                if r['method'] == 'direct-oracle'})
    assert raw.keys() == rows.keys()
    at_cap = []
    for uid, r in raw.items():
        assert r['input_tokens'] <= 120000 and r['output_tokens'] <= 4096, uid
        for i, call in enumerate(r['calls']):
            if call['kind'] == 'generation' and call['usage']['output_tokens'] >= (192 if r['method'] == 'module' else 512):
                at_cap.append(dict(row=uid, call=i, output=call['output']))
    errors = {uid: r['result'] for uid, r in rows.items() if r['action'] in ('invalid_output', 'execution_error')}
    module_fp = {uid: r['result'] for uid, r in rows.items()
                 if r['method'] == 'module' and r['expected'] == 'keep' and r['opened']}
    write(OUT / 'diagnostics.json', dict(stages=stages, paired=paired, positive_module_exits=gates,
          generation_at_cap=at_cap, all_cases_within_budget=True,
          execution_errors=sum(r['action'] == 'execution_error' for r in rows.values()),
          invalid_outputs=len(errors), module_false_positives=module_fp))
    write(OUT / 'invalid-outputs.json', errors)
    print('diagnostics:', len(rows), 'rows;', len(errors), 'invalid;', len(at_cap), 'generations at cap')


if __name__ == '__main__':
    diagnostics()
