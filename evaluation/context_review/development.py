"""Freeze source-preserving context interventions around two previously selected witnesses."""
from pathlib import Path
from evaluation.decision_records.build import read, save, commit
from evaluation.pair_selection.trial import envelope
from team_memory.pair_selection import paragraphs
from team_memory.store import digest

HERE = Path(__file__).resolve().parent

def build():
    old = HERE.parent / 'role_review'
    rows = {r['id']: r for r in read(old / 'inputs.json')}
    keys = read(old / 'key.json')
    outputs = read(old.parents[1] / 'results/role_review/comparison.json')['results']
    data, key = [], {}
    for cid, label in keys.items():
        if label['topic'] not in ('freebsd-cwd', 'fsck-empty') or (label['scenario'], label['view']) != ('mixed', 'raw'):
            continue
        row = rows[cid]
        previous = outputs[cid]['referenced-review']['result']
        src = row['incoming']
        blocks = [p.cite() for p in paragraphs(digest(src), (src, 'source_only'))]
        focus = next(i for i, p in enumerate(blocks) if p == previous['incoming'])
        # An independently authored, earlier unrelated record supplies true distractor
        # passages with their own author/location, without fabricating source offsets.
        unrelated = envelope(commit('f4c21e89d7' if label['topic']=='freebsd-cwd' else 'c9486eb04d'))
        assert unrelated['observed_at'] < src['observed_at']
        decoys = [p.cite() for p in paragraphs(digest(unrelated), (unrelated,'source_only'))][1:]
        one = blocks[max(1,focus-1):min(len(blocks),focus+2)]
        two = blocks[max(1,focus-2):min(len(blocks),focus+3)]
        assert len(two)>len(one)
        need = len(two)-1
        # Use complete source paragraphs; report length differences explicitly.
        assert len(decoys)>=need, (label['topic'],len(decoys),need)
        variants = {'selected':[blocks[focus]], 'neighbors1':one, 'neighbors2':two,
                    'unrelated':[blocks[focus],*decoys[:need]]}
        for name, evidence in variants.items():
            for reverse in (False,True):
                uid = f'{label["topic"]}-{name}-{"reverse" if reverse else "forward"}'
                docs = list(reversed(evidence)) if reverse else evidence
                data.append(dict(id=uid, base=previous, passages=docs, report_id=digest(src), sources={digest(src):src,digest(unrelated):unrelated}))
                key[uid]=dict(topic=label['topic'],variant=name,reverse=reverse,
                              condition='long path with missing permissions and insufficient initial getcwd buffer' if label['topic']=='freebsd-cwd' else 'empty loose object file',
                              behavior='getcwd can give EACCES with small buffer although larger succeeds' if label['topic']=='freebsd-cwd' else 'fsck reports failed to read object / Invalid argument, from mmap EINVAL',
                              source=src,unrelated=unrelated,characters=sum(len(p['quote']) for p in docs),
                              focus_paragraph=focus,paragraph_indices=[i for i,p in enumerate(blocks) if p in evidence])
    assert len(data)==16
    save(HERE/'dev-inputs.json',data);save(HERE/'dev-key.json',key)

if __name__=='__main__':build()
