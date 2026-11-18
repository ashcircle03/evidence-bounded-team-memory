"""Optional role correction over existing, uniquely owned LangExtract source spans."""
import json
from collections import defaultdict

from team_memory.records import preserving


def candidates(source, raw):
    graph = preserving.compile_graph(source, raw)
    if graph['status'] != 'annotated':
        return []
    groups = defaultdict(list)
    for index, row in enumerate(json.loads(raw)['extractions']):
        span = preserving._aligned_span(source, row)
        groups[span['group']].append(dict(span, index=index))
    def endpoint(span):
        units = [u for u in graph['units'] if u['start'] < span['end'] and span['start'] < u['end']]
        return dict(start=span['start'], end=span['end'], text=source['text'][span['start']:span['end']],
                    sentence=source['text'][units[0]['window_start']:units[-1]['window_end']])
    pairs = []
    for members in groups.values():
        targets = [s for s in members if s['role']=='claim']
        if len(targets)!=1:
            continue
        target = targets[0]
        for span in members:
            if span['role'] not in ('condition','basis','subject','time'):
                continue
            if span['start']<=target['start'] and target['end']<=span['end']:
                continue
            pairs.append(dict(index=span['index'], old_role=span['role'], target=endpoint(target),
                              context=endpoint(span)))
    return pairs


def apply(source, raw, predict, *, model):
    """predict(pairs) returns one condition/basis/keep decision per pair in order."""
    pairs = candidates(source, raw)
    decisions = predict(pairs) if pairs else []
    if len(decisions)!=len(pairs) or any(r not in ('condition','basis','keep') for r in decisions):
        raise ValueError('Invalid discourse role decision batch')
    parsed = json.loads(raw) if pairs else None
    changed = False
    for pair, role in zip(pairs, decisions):
        old = pair['old_role']
        if role in ('keep',old):
            continue
        row = parsed['extractions'][pair['index']]
        attrs = dict(row[old+'_attributes'])
        attrs.pop('basis_kind', None)
        if role=='basis':
            attrs['basis_kind']='stated'
        parsed['extractions'][pair['index']]={role:row[old],role+'_attributes':attrs}
        changed=True
    graph=preserving.compile_graph(source,json.dumps(parsed) if changed else raw,model=model)
    if changed and graph['status']!='annotated':
        raise ValueError('Role rewrite failed original graph contract')
    return graph


def construct(source, generate, predict, *, model):
    """Ingestion builder using the accepted extraction prompt and external role predictor."""
    if 'record_graph' in source:
        raise ValueError('Do not overwrite immutable extraction')
    generator, _ = preserving.grouped.components()
    metadata={key:source[key] for key in ('id','owner','speaker','observed_at','location')}
    prompt=generator.render(source['text'],additional_context=json.dumps(metadata,ensure_ascii=False))
    raw=generate('Extract grounded records using the supplied format and examples.',prompt)
    return dict(source,record_graph=apply(source,raw,predict,model=model))
