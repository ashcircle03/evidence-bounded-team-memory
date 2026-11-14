"""Aggregate the frozen comparison and source-reviewed QA judgments, without tuning."""
import json
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / 'results/comparator-choice'


def read(path):
    return json.loads(path.read_text())


def qa_rows(result):
    return {r['case_id'] + '/' + r['label']: r for r in result['rows']
            if r['request']['operation'] == 'ask'}


def main():
    comparator = read(RESULTS / 'comparison.json')
    baseline = read(ROOT / 'results/module-boundary/v1/result.json')
    base_rows = qa_rows(baseline)
    production = read(ROOT / 'results/module-boundary/v1/freeze.json')['config']['code_sha256']
    for name, value in production.items():
        if name.startswith('team_memory/'):
            assert sha256((ROOT / name).read_bytes()).hexdigest() == value, name
    jobs = []
    for phase in ('oracle', 'compare-8b', 'compare-14b', 'flow-8b', 'flow-14b'):
        folder = RESULTS / (phase + '-v1')
        result, dispatch = read(folder / 'result.json'), read(folder / 'dispatch.json')
        verified = read(folder / 'verification.json')
        assert verified['slurm_complete'] and verified['program_complete'] and verified['packet_hashes_valid']
        assert result['job_id'] == dispatch['job_id']
        calls = [json.loads(line) for line in (folder / 'calls.jsonl').read_text().splitlines()]
        assert len(calls) == result['calls']
        if phase.startswith('flow-'):
            compare_folder = RESULTS / (phase.replace('flow-', 'compare-') + '-v1')
            actual = {r['case_id']: r for r in read(compare_folder / 'result.json')['selectors']}
            for selector in result['selectors']:
                assert all(selector[k] == actual[selector['case_id']][k] for k in ('system', 'content', 'raw'))
        jobs.append(dict(phase=phase, job_id=dispatch['job_id'], state=dispatch['state'],
                         exit_code=dispatch['exit_code'], gpus=dispatch['gpus'],
                         elapsed_seconds=dispatch['elapsed_seconds'],
                         gpu_minutes=dispatch['gpus'] * dispatch['elapsed_seconds'] / 60,
                         calls=len(calls),
                         prompt_tokens=sum(c['response']['usage']['prompt_tokens'] for c in calls),
                         completion_tokens=sum(c['response']['usage']['completion_tokens'] for c in calls)))
    old_ratings = read(ROOT / 'results/module-boundary/v1/ratings.json')
    ratings = read(RESULTS / 'flow-14b-v1/ratings.json')
    rows = qa_rows(read(RESULTS / 'flow-14b-v1/result.json'))
    assert set(ratings) == set(rows) and len(rows) == 45
    state_keys = ['release-correction/pending', 'release-correction/approved',
                  'rejected-calendar/rejected', 'new-temperature/pending',
                  'new-temperature/approved', 'new-retention/current',
                  'new-retention/proposal', 'new-vote-conflict/current']
    legacy_keys = [k for k in rows if k.startswith('legacy-')]
    assert len(legacy_keys) == 20
    preserved = {k: all(rows[k]['result'].get(f) == base_rows[k]['result'].get(f)
                        for f in ('raw', 'answers')) for k in base_rows}
    scores = {}
    for name, rs in [('8b-reference', old_ratings), ('14b-comparator', ratings)]:
        scores[name] = dict(
            legacy_answer_and_evidence=sum(rs[k]['answer_correct'] and rs[k]['source_evidence_complete'] for k in legacy_keys),
            state_answer_and_state_evidence=sum(rs[k]['answer_correct'] and rs[k]['state_citation_complete'] for k in state_keys),
            state_strict_all_evidence=sum(rs[k]['answer_correct'] and rs[k]['source_evidence_complete'] and rs[k]['state_citation_complete'] for k in state_keys))
    new_flow = {}
    for arm in ('8b', '14b'):
        rs = read(RESULTS / ('flow-' + arm + '-v1') / 'ratings.json')
        rs = {k: v for k, v in rs.items() if 'desired_reconsideration_flow_met' in v}
        assert len(rs) == 8
        families = {k.split('/')[0] for k in rs}
        new_flow[arm] = dict(
            answer_correct=sum(r['answer_correct'] for r in rs.values()),
            desired_flow_checkpoints=sum(r['desired_reconsideration_flow_met'] for r in rs.values()),
            both_checkpoints_correct=sum(all(r['desired_reconsideration_flow_met'] for k, r in rs.items() if k.startswith(f + '/')) for f in families),
            qa_count=8, families=4)
    oracle = read(RESULTS / 'oracle-v1/semantic-summary.json')
    gates = dict(oracle_reader=oracle['stage_a_pass'], comparator=comparator['comparator_gate'],
                 legacy_preserved=scores['14b-comparator']['legacy_answer_and_evidence'] == 20,
                 state_preserved=scores['14b-comparator']['state_answer_and_state_evidence'] == 8,
                 new_flow_all_conditions_preserved=new_flow['14b']['desired_flow_checkpoints'] == 8)
    summary = dict(adopt_14b=all(gates.values()), selected_comparator='Qwen3-8B (existing default)',
                   production_changed=False, gates=gates, comparison=comparator['models'],
                   regression=scores, exact_known_raw_and_answer_evidence_matches=preserved,
                   new_flow=new_flow, jobs=jobs,
                   total_gpu_minutes=sum(j['gpu_minutes'] for j in jobs),
                   total_calls=sum(j['calls'] for j in jobs),
                   total_prompt_tokens=sum(j['prompt_tokens'] for j in jobs),
                   total_completion_tokens=sum(j['completion_tokens'] for j in jobs),
                   limits=['Authored diagnostic cases, four matched decision families, not independent public benchmark.',
                           'Same implementation agent rated meanings; no independent adjudicator.',
                           'Different checkpoint generations and GPU counts; not size-only or equal-hardware speed experiment.',
                           'Single fixed run per arm; no claim of statistically stable gains.',
                           'Existing QA20 contains only three natural EverMem items; no full EverMem or Wiki score.'])
    (RESULTS / 'decision.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
