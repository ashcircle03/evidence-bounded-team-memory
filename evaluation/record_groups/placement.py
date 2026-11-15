"""Separate wrong/missing role label from context absent from the claim group.

Supplementary diagnosis, not a change to frozen pass/fail criteria.
"""
import json
from pathlib import Path
from .evaluate import covers
from team_memory.records.graph import ROLES


def diagnose(source,p):
    units={u['id']:u for u in source['record_graph']['units']}
    claims=[c for c in source['record_graph']['claims'] if covers(source['text'],p['anchor'],[units[x] for x in c['claim']])]
    rows=[]
    for role in ('condition','basis'):
        for text in p[role]:
            if any(covers(source['text'],text,[units[x] for x in c[role]]) for c in claims):where='expected_role'
            elif any(covers(source['text'],text,[units[x] for r in ROLES for x in c[r]]) for c in claims):where='same_claim_group_other_role'
            elif claims:where='source_only_or_other_claim'
            else:where='claim_anchor_not_extracted'
            rows.append(dict(expected_role=role,text=text,placement=where))
    return rows


def main(folder,job):
    result=json.loads((folder/f'record-groups-{job}.json').read_text())
    old=json.loads(Path('results/record-graph/v2/record-graph-122843.json').read_text())
    probes=json.loads(Path('evaluation/record_groups/key.json').read_text())['probes']
    rows=[dict(arm='baseline',source=s) for s in old['sources']]+result['rows'];report=[]
    for row in rows:
        for p in probes:
            if p['source_id']==row['source']['id']:
                report.append(dict(arm=row['arm'],source_id=p['source_id'],anchor=p['anchor'],requirements=diagnose(row['source'],p)))
    (folder/'placement.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]),sys.argv[2])
