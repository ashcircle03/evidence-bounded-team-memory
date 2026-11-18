"""Project explicit relation edges into the unchanged group-based scoring interface.

The graph stores no duplicate assertions. Each edge view contains exactly its
target assertion and its context. Legacy record views remain unchanged.
"""
from copy import deepcopy
from evaluation.record_bound.rows import compiled_rows as legacy_rows


def compiled_rows(source):
    if source['record_graph']['version']!='records.graph/v4':return legacy_rows(source)
    old=deepcopy(source);old['record_graph']['version']='records.graph/v3'
    bindings=old['record_graph'].pop('context_bindings')
    rows=legacy_rows(old);g=source['record_graph'];units={u['id']:u for u in g['units']}
    anchors={(units[a['unit_ids'][0]]['start'],units[a['unit_ids'][-1]]['end']):a
             for c in g['claims'] for a in c['assertions']}
    for b in bindings:
        a=anchors[(b['target_start'],b['target_end'])]
        rows.append(dict(id=len(rows),role='claim',text=source['text'][b['target_start']:b['target_end']],group=b['id'],stance=a['stance']))
        rows.append(dict(id=len(rows),role=b['role'],text=source['text'][b['context_start']:b['context_end']],group=b['id'],stance='unknown',basis_kind=b['basis_kind']))
    return rows
