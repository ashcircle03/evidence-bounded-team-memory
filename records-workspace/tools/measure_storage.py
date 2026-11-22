import json, sys, zlib
from copy import deepcopy
sys.path.insert(0, '.')
from team_memory.store import encoded
data = json.load(open(sys.argv[1], encoding='utf-8'))
def walk(x):
    if isinstance(x, dict):
        if 'record_graph' in x and 'text' in x: yield x
        for v in x.values(): yield from walk(v)
    elif isinstance(x, list):
        for v in x: yield from walk(v)
recs = list({r['id']: r for r in walk(data)}.values())
def strip_quotes(g):
    for u in g['units']: u.pop('quote', None)
    for row in g.get('layout', []):
        for c in row['cells'] + row.get('headers', []) + ([row['label']] if row.get('label') else []):
            if c: c.pop('quote', None)
    for e in g.get('excluded', []): e.pop('quote', None)
tot = dict(full=0, noquote=0, noedges=0, compact=0, text=0, fz=0, qz=0, ez=0)
vers = {}
for r in recs:
    g = r['record_graph']; vers[g['version']] = vers.get(g['version'], 0) + 1
    a = encoded(r); tot['full'] += len(a); tot['fz'] += len(zlib.compress(a, 9))
    tot['text'] += len(r['text'].encode())
    q = deepcopy(r); strip_quotes(q['record_graph']); b = encoded(q); tot['noquote'] += len(b); tot['qz'] += len(zlib.compress(b, 9))
    e = deepcopy(r); e['record_graph']['edges'] = []; c = encoded(e); tot['noedges'] += len(c); tot['ez'] += len(zlib.compress(c, 9))
    tot['compact'] += len(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
f = tot['full']
print(f"records={len(recs)} versions={vers}")
print(f"full {f:,} B | text {tot['text']/f:.1%}")
print(f"quote share  raw {1-tot['noquote']/f:.1%}  zlib {1-tot['qz']/tot['fz']:.1%}")
print(f"edges share  raw {1-tot['noedges']/f:.1%}  zlib {1-tot['ez']/tot['fz']:.1%}")
print(f"indent/whitespace share {1-tot['compact']/f:.1%}")
