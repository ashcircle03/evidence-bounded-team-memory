"""Optional role decisions over uniquely owned, already aligned source spans."""
from team_memory.records import preserving


def pairs_from_groups(source, groups, units):
    def endpoint(span):
        covered = [u for u in units if u['start'] < span['end'] and span['start'] < u['end']]
        return dict(start=span['start'], end=span['end'], text=source['text'][span['start']:span['end']],
                    sentence=source['text'][covered[0]['window_start']:covered[-1]['window_end']])
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


def candidates(source, raw):
    pairs = []

    def collect(batch):
        pairs.extend(batch)
        return ['keep'] * len(batch)

    preserving.compile_graph(source, raw, predict=collect)
    return pairs


def apply(source, raw, predict, *, model):
    return preserving.compile_graph(source, raw, model=model, predict=predict)


def construct(source, generate, predict, *, model):
    return preserving.construct(source, generate, model=model, predict=predict)
