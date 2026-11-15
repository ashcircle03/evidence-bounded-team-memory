"""Render every fixed source/output for human-readable inspection; no scoring."""
import json
from pathlib import Path
from evaluation.record_groups.evaluate import linked_text
from team_memory.records.graph import ROLES
from team_memory.records.grouped import compile_graph


def main(folder,job):
    result=json.loads((folder/f'record-contract-{job}.json').read_text())
    traces=[json.loads(x) for x in (folder/f'record-contract-{job}.calls.jsonl').read_text().splitlines()]
    inputs=json.loads(Path('evaluation/record_contract/inputs.json').read_text())['sources']
    traces={(t['source_id'],t['arm']):t for t in traces}
    rows={(r['source']['id'],r['arm']):r for r in result['rows']}
    lines=['# All-source review cards','No scores; review alongside the original source.']
    for i,item in enumerate(inputs):
        s=item['source'];lines.extend([f'\n## {i}. {item["case_id"]} — {s["id"]}',s['text']])
        for arm in ('control','revised'):
            row=rows[(s['id'],arm)];g=row['source']['record_graph'];trace=traces[(s['id'],arm)]
            lines.append(f'\n### {arm}: {g["status"]}; call {trace["id"]}')
            if g['status']=='failed':
                try:compile_graph(s,trace['response']['choices'][0]['message']['content'],canonical=True,basis_types=True)
                except Exception as exc:lines.append('Compiler error: '+type(exc).__name__+': '+str(exc))
                lines.extend(['```json',trace['response']['choices'][0]['message']['content'],'```'])
            for c in g['claims']:
                lines.append(f'- {c["id"]} ({c["stance"]})')
                for r in ROLES:
                    spans=linked_text(row['source'],c,r)
                    if spans:lines.append(f'  - {r}: '+json.dumps(spans,ensure_ascii=False))
                if c['basis_annotations']:lines.append('  - reason kinds: '+str(sorted({a['kind'] for a in c['basis_annotations']})))
    (folder/'review-cards.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]),sys.argv[2])
