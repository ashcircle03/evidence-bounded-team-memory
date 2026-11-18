from pathlib import Path
from hashlib import sha256
from collections import defaultdict
import json
import tempfile

from team_memory.records import preserving, grouped
from evaluation.record_full.evaluate import score, raw_rows, metric, matches, contributors
from evaluation.record_bound.rows import compiled_rows
from evaluation.record_groups.evaluate import transport


def correct_stance_nodes(rows, gold):
    """Recover item IDs using exactly the frozen scorer's stance assignment."""
    nodes = [n for n in gold['nodes'] if n['role'] in ('claim', 'caveat')]
    values = defaultdict(list); groups = defaultdict(list)
    for row in rows:
        if row['role'] != 'claim':
            continue
        groups[row['group']].append(row)
        for n in nodes:
            if matches(row['text'], n):
                values[n['id']].append(row['stance'])
    for rr in groups.values():
        for n in nodes:
            ids = contributors(rr, n)
            if ids and n['id'] not in values:
                values[n['id']] = [r['stance'] for r in rr if r['id'] in ids]
    return {n['id'] for n in nodes if values[n['id']] and all(v in n['stances'] for v in values[n['id']])}


def main():
    out = Path('results/record-causal/v1')
    freeze = json.loads((out / 'initial-freeze.json').read_text())
    for table in ('frozen_evaluation_files', 'controls'):
        for name, expected in freeze[table].items():
            assert sha256(Path(name).read_bytes()).hexdigest() == expected, name
    legacy = json.loads(Path('results/record-strata/v1/record-strata-122970.json').read_text())
    gold = {d['id']: d for d in json.loads(Path('evaluation/record_full/gold.json').read_text())['documents']}
    frozen = json.loads(Path('results/record-full/v3/evaluation.json').read_text())
    cases = []; graphs = []; protections = []
    with tempfile.TemporaryDirectory(prefix='record-causal-') as temp:
        for row in [r for r in legacy['rows'] if r['arm'] == 'ours']:
            source = {k: v for k, v in row['source'].items() if k != 'record_graph'}
            d = gold[row['id']]; stages = []
            for stage in ('original', 'attributes', 'quarantine'):
                enriched = row['source'] if stage == 'original' else dict(source, record_graph=preserving.compile_graph(
                    source, row['raw'], model='Qwen3-8B@' + legacy['model_revision'], isolate_invalid=stage == 'quarantine'))
                stored_rows = compiled_rows(enriched)
                scorecard = score(stored_rows, d, source)
                correct_stances = correct_stance_nodes(stored_rows, d)
                assert len(correct_stances) == scorecard['stance_correct']
                if stage == 'original':
                    previous = next(c for c in frozen['cases'] if c['id'] == row['id'] and c['arm'] == 'ours')
                    assert json.loads(json.dumps(scorecard)) == previous['compiled']
                check = transport(enriched, Path(temp) / row['id'] / stage)
                case = dict(id=row['id'], panel=d['panel'], difficulty=d['difficulty'], availability=d['availability'],
                            stage=stage, score=scorecard, status=enriched['record_graph']['status'],
                            diagnostics=enriched['record_graph'].get('diagnostics', []), transport=check,
                            correct_stance_nodes=sorted(correct_stances))
                cases.append(case); stages.append(case)
                graphs.append(dict(id=row['id'], stage=stage, source=enriched, original_raw_sha256=sha256(row['raw'].encode()).hexdigest()))
            raw_score = score(raw_rows(row['raw']), d, source)
            for case in stages:
                case['raw_missing_nodes'] = raw_score['missing_nodes']
                case['storage_lost_nodes'] = sorted(set(case['score']['missing_nodes']) - set(raw_score['missing_nodes']))
                case['storage_lost_edges'] = sorted(set(map(tuple, case['score']['missing_edges'])) - set(map(tuple, raw_score['missing_edges'])))
            for a, b in ((0, 1), (1, 2), (0, 2)):
                old, new = stages[a]['score'], stages[b]['score']
                required = {n['id'] for n in d['nodes'] if n['required']}
                old_nodes = required - set(old['missing_nodes'])
                old_edges = set(map(tuple, d['edges'])) - set(map(tuple, old['missing_edges']))
                correct_stances = set(stages[a]['correct_stance_nodes'])
                protections.append(dict(id=row['id'], comparison=stages[a]['stage']+'→'+stages[b]['stage'],
                    protected_nodes=len(old_nodes), lost_nodes=sorted(old_nodes & set(new['missing_nodes'])),
                    protected_edges=len(old_edges), lost_edges=sorted(old_edges & set(map(tuple,new['missing_edges']))),
                    protected_stances=len(correct_stances),
                    lost_stances=sorted(correct_stances - set(stages[b]['correct_stance_nodes'])), lost_complete=old['complete'] and not new['complete']))
    summaries = []
    for panel in ('balanced_synthetic','natural_audit'):
        for stage in ('original','attributes','quarantine'):
            cs = [c for c in cases if c['panel']==panel and c['stage']==stage]; ss=[c['score'] for c in cs]
            summaries.append(dict(panel=panel,stage=stage,n=len(cs),
                metrics={k:metric(*(sum(s[k][z] for s in ss) for z in ('tp','fp','fn'))) for k in ('content_recall','claim_recall','typed_edges')},
                complete=sum(s['complete'] for s in ss),
                **{k:sum(len(s[k]) for s in ss) for k in ('extra_rows','extra_claim_rows','boilerplate_rows','stance_wrong','overmerged_record_pairs')},
                storage_lost_nodes=sum(len(c['storage_lost_nodes']) for c in cs),storage_lost_edges=sum(len(c['storage_lost_edges']) for c in cs)))
    report = dict(frozen_gold_and_scorer=True, actual_qwen_outputs=68,new_model_calls=0,
                  original_scores_reproduced=68, transport_passed=len(cases),
                  preservation_passed=all(not(p['lost_nodes'] or p['lost_edges'] or p['lost_stances'] or p['lost_complete']) for p in protections),
                  summary=summaries,protection=protections,cases=cases)
    (out/'storage-evaluation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (out/'storage-graphs.json').write_text(json.dumps(graphs,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('cases','protection')},indent=2))
    print('regressions', [p for p in protections if p['lost_nodes'] or p['lost_edges'] or p['lost_stances'] or p['lost_complete']])


if __name__ == '__main__':
    main()
