"""Representation adapters only; frozen gold and scorer are not modified."""
import json
from evaluation.record_full.evaluate import compiled_rows as legacy_compiled
from evaluation.record_groups.evaluate import linked_text

def raw_rows(raw):
    parsed=json.loads(raw);rows=[]
    for i,c in enumerate(parsed['records']):
        for item in [c['root']]+c['details']:
            rows.append(dict(id=len(rows),role='claim',text=item['quote'],group=str(i),stance=item['stance']))
        for role in ('condition','basis','time','subject'):
            for item in c[role]:rows.append(dict(id=len(rows),role=role,text=item['quote'],group=str(i),stance='unknown',basis_kind=item.get('kind','unspecified')))
    return rows

def compiled_rows(source):
    if source['record_graph']['version']!='records.graph/v3':return legacy_compiled(source)
    rows=[]
    for c in source['record_graph']['claims']:
        for a in c['assertions']:
            cc=dict(c,claim=a['unit_ids'])
            for text in linked_text(source,cc,'claim'):rows.append(dict(id=len(rows),role='claim',text=text,group=c['id'],stance=a['stance']))
        for role in ('condition','basis','time','subject'):
            for text in linked_text(source,c,role):rows.append(dict(id=len(rows),role=role,text=text,group=c['id'],stance='unknown'))
    return rows
