"""Readable reporting only; reads the completed, frozen-score comparison."""
from pathlib import Path
from collections import Counter
import json


def pct(value):
    return '—' if value is None else f'{100 * value:.1f}%'


def main():
    root = Path('results/record-bound/v1')
    report = json.loads((root / 'evaluation.json').read_text())
    gold = {d['id']: d for d in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    incoming = json.loads((root / f"record-bound-{report['job_id']}.json").read_text())
    previous = json.loads(Path('results/record-strata/v1/record-strata-122970.json').read_text())
    rows = {(r['id'], r['arm']): r for r in previous['rows'] + incoming['rows']}
    table = [s for s in report['summary'] if s['difficulty'] == 'all']
    lines = ['# Records bound extraction: fixed-gold comparison', '',
             f"Job `{report['job_id']}`. Default adoption: **{report['adopt_default']}**.", '',
             '[한국어 원인 분석과 채택 판단](ANALYSIS.md)', '',
             'Gold, scorer, input source bytes, Qwen3-8B revision and decode settings were held fixed. '
             'The nested extraction contract, examples, source segment IDs and compiler are the intervention. '
             'Controls are 136 cached actual calls; the candidate has 68 new calls. '
             'This is records-only development evidence, not QA accuracy or held-out generalization.', '',
             '## Full-document quality', '',
             '| Panel | Arm | Stage | Content recall | Root recall | Link P / R / F1 | Complete | Extra rows | Boilerplate | Overmerged pairs | Wrong stance |',
             '|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|']
    for s in table:
        m = s['metrics']; e = m['typed_edges']
        lines.append(f"| {s['panel']} | {s['arm']} | {s['stage']} | {m['content_recall']['tp']}/{m['content_recall']['tp']+m['content_recall']['fn']} ({pct(m['content_recall']['recall'])}) | {pct(m['claim_recall']['recall'])} | {pct(e['precision'])} / {pct(e['recall'])} / {pct(e['f1'])} | {s['complete']}/{s['n']} | {s['extra_rows']} | {s['boilerplate_rows']} | {s['overmerged_pairs']} | {s['stance_wrong']} |")
    lines += ['', '`simple`: previous simple extraction; `ours`: previous grouped extraction; `bound`: new parent-bound extraction. '
              '`raw`: actual model JSON before compilation; `compiled`: stored graph. '
              'Extra rows count unmatched output rows, not every semantic error. Typed-edge FP, wrong stance and overmerging are separate. '
              'Content recall only establishes that required words/meaning-bearing anchors are present somewhere; it does not establish correct attachment.', '',
              '## Item preservation and adoption', '']
    for panel in ('balanced_synthetic', 'natural_audit'):
        ps = [p for p in report['preservation'] if gold[p['id']]['panel'] == panel]
        lines += [f"- {panel}: retained nodes {sum(p['retained_nodes'] for p in ps)}/{sum(p['protected_nodes'] for p in ps)}; "
                  f"retained edges {sum(p['retained_edges'] for p in ps)}/{sum(p['protected_edges'] for p in ps)}; "
                  f"old complete documents retained {sum(p['old_complete'] and p['new_complete'] for p in ps)}/{sum(p['old_complete'] for p in ps)}; "
                  f"newly recovered nodes {sum(len(p['new_nodes']) for p in ps)}, edges {sum(len(p['new_edges']) for p in ps)}."]
    lines += ['', '```json', json.dumps(report['gate'], indent=2), '```', '',
              'The gate was specified before inspecting candidate output. No per-case selection or gold-guided merging of two methods is used. '
              'If any gate fails, the new extractor stays opt-in and the existing default is retained.', '',
              '## Compilation and persistence', '']
    for arm in ('simple', 'ours', 'bound'):
        cases = [c for c in report['cases'] if c['arm'] == arm]
        missing_after = sum(len(set(c['compiled']['missing_nodes']) - set(c['raw']['missing_nodes'])) for c in cases)
        lost_edges = sum(len({tuple(e) for e in c['compiled']['missing_edges']} - {tuple(e) for e in c['raw']['missing_edges']}) for c in cases)
        lines.append(f'- {arm}: raw→stored lost required nodes {missing_after}; lost required links {lost_edges}.')
    lines += [f"- Candidate extraction status: {dict(Counter(c['status'] for c in report['cases'] if c['arm']=='bound'))}.",
              f"- Candidate append/restart/reader transport: {sum(r['transport']['stored_restarted'] for r in incoming['rows'])}/68; full source and metadata exactly retained.",
              f"- All {report['old_scores_exactly_reproduced']} previous case/arm scores reproduced exactly with the new representation adapter.",
              '- A passing transport check means that stored information reaches the reader; it does not mean the LLM extracted all correct information.', '',
              '## Cost and limits', '',
              f"- Candidate token usage: {json.dumps(report['cost'])}.",
              f"- Candidate program time including client setup/transport: {incoming['seconds']:.2f} seconds. Slurm total including preparation is in `slurm.txt` and `verification.json`.",
              '- 54 synthetic documents = 18 story families × three focal-evidence variants; nine predefined difficulty/availability cells remain six documents each. The 18 families also share six semantic templates. These are not 54 independent real-world situations.',
              '- 14 natural messages come from five failure-selected EverMem cases, so they are an audit panel rather than a representative benchmark estimate.',
              '- Availability describes two focal qualifiers, not whether the entire document has any extractable facts. All substantive original facts remain in the fixed gold.',
              '- Single-agent gold with finite anchors/spans; no independent human adjudication or unrestricted semantic entailment. Stated/inferred basis labels are retained, but their full semantic correctness is not comprehensively scored.',
              '- No new QA calls, training, paid API or dataset replication. No claim that existing QA answer accuracy was remeasured here.', '',
              '## Artifacts', '',
              '- [Design and integration](../../../docs/records-bound-extraction.md)',
              '- [Fixed protocol](../../../evaluation/record_bound/PROTOCOL.md)',
              '- [Per-document sources, outputs and error sets](cases.md)',
              '- [Difficulty and availability cells](strata.md)',
              '- [Machine-readable scores and preservation](evaluation.json)',
              '- [References](references.json), [source/input freeze](freeze.json), [comparison freeze](comparison-freeze.json)', '']
    (root / 'README.md').write_text('\n'.join(lines))
    lines = ['# Per-document records comparison', '',
             'Gold and scoring are fixed. Listed losses/gains are item sets, not aggregate substitutions. Full actual outputs follow each source.', '']
    for p in report['preservation']:
        d = gold[p['id']]; nodes = {n['id']: n for n in d['nodes']}
        lines += [f"## {p['id']} — {d['panel']} / {d['difficulty']} / {d['availability']}", '',
                  '```text', rows[(p['id'], 'bound')]['source']['text'], '```', '',
                  f"Complete: old {p['old_complete']} → candidate {p['new_complete']}.", '']
        for label, key in [('Lost required content', 'lost_nodes'), ('New required content', 'new_nodes')]:
            lines.append(f"{label}: " + ('; '.join(f"`{n}`: {nodes[n]['text']}" for n in p[key]) or 'none') + '\n')
        for label, key in [('Lost correct links', 'lost_edges'), ('New correct links', 'new_edges')]:
            lines.append(f"{label}: " + ('; '.join(f"`{e[0]} → {e[1]} → {e[2]}`: {nodes[e[2]]['text']}" for e in p[key]) or 'none') + '\n')
        for arm in ('simple', 'ours', 'bound'):
            c = next(c for c in report['cases'] if c['id'] == p['id'] and c['arm'] == arm)
            detail = {stage: {k: c[stage][k] for k in ('complete','missing_nodes','missing_claims','missing_edges','incorrect_edges','extra_rows','extra_claim_rows','boilerplate_rows','duplicate_rows','overmerged_record_pairs','stance_wrong')} for stage in ('raw','compiled')}
            detail.update(status=c['status'], diagnostics=c['diagnostics'], finish_reason=c['finish_reason'])
            lines += [f'### {arm}', '', '```json', rows[(p['id'], arm)]['raw'], '```', '', '```json', json.dumps(detail, ensure_ascii=False, indent=2), '```', '']
    (root / 'cases.md').write_text('\n'.join(lines))
    lines = ['# Fixed difficulty × evidence availability', '',
             '| Difficulty | Availability | Arm | Stage | Content R | Link P | Link R | Link F1 | Complete |',
             '|---|---|---|---|---:|---:|---:|---:|---:|']
    for s in report['summary']:
        if s['difficulty'] == 'all':
            continue
        m=s['metrics']; e=m['typed_edges']
        lines.append(f"| {s['difficulty']} | {s['availability']} | {s['arm']} | {s['stage']} | {pct(m['content_recall']['recall'])} | {pct(e['precision'])} | {pct(e['recall'])} | {pct(e['f1'])} | {s['complete']}/{s['n']} |")
    (root / 'strata.md').write_text('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
