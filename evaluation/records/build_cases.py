"""Build reviewable record-state fixtures; relation labels are oracle inputs."""
import json
from pathlib import Path


STORIES = {
    'correction': ('Under config A, latency is 120ms. Owner is Hana.',
                   'Correction under config A: latency is 90ms. Owner is still Hana.',
                   'Under config A, latency is 120ms.', 'Correction under config A: latency is 90ms.'),
    'reconsider': ('Keep one writer because version 4 permits only one writer. Owner is Hana.',
                   'Version 5 now permits four concurrent writers. This is not a completed migration.', None, None),
    'coexist': ('Under config A, latency is 120ms. Owner is Hana.',
                'Under config B, latency is 90ms. Config A has not been retested.', None, None),
    'conflict': ('On build 7 under config A, latency is 120ms. Owner is Hana.',
                 'On build 7 under config A, latency is 90ms. Neither report has been corrected.', None, None),
}
SEQUENCES = [[], ['approve'], ['reject'], ['approve','reject'], ['reject','approve']]


def build():
    cases=[]
    for kind,(old,new,old_assert,new_assert) in STORIES.items():
        for form in ('plain','unicode_multiline'):
            prefix,suffix=('', '') if form=='plain' else ('  실험 기록 🧪\n조건을 임의로 넓히지 않는다.\n','\n\t')
            for votes in SEQUENCES:
                case_id=f'{kind}-{form}-'+('-'.join(votes) or 'pending')
                def source(name,text,owner,date):
                    return dict(id=name,owner=owner,speaker=owner,observed_at=date,
                                location=f'synthetic-records://{case_id}/{name}',text=prefix+text+suffix)
                sources=[source('old',old,'hana','2026-10-01T09:00:00+09:00'),
                         source('new',new,'jun','2026-10-02T00:00:00Z')]
                def span(s,text):
                    start=s['text'].index(text)
                    return dict(source_id=s['id'],start=start,end=start+len(text),quote=text)
                candidate=dict(kind=kind,previous=span(sources[0],old),incoming=span(sources[1],new),
                               reason='Oracle relation supplied to isolate record state handling.',
                               previous_assertion=span(sources[0],old_assert) if old_assert else None,
                               incoming_assertion=span(sources[1],new_assert) if new_assert else None)
                status=('informational' if kind=='coexist' else 'pending' if not votes else
                        'approved' if votes[0]=='approve' else 'rejected')
                effect=({'correction':'replace_assertion','reconsider':'authorize_reconsideration'}.get(kind,'none')
                        if status=='approved' else 'none')
                cases.append(dict(id=case_id,scenario_group=kind,split='diagnostic',sources=sources,
                                  candidate=candidate,votes=votes,mode='sequential',
                                  expected=dict(status=status,effect=effect,reviewer='hana',
                                                accepted_votes=0 if kind=='coexist' or not votes else 1)))
    # A closed review cannot be reversed by a sequential command. Conflicting
    # votes can instead exist in a pre-existing v2 Git store imported at genesis.
    from copy import deepcopy
    for row in list(cases):
        if row['candidate']['kind']!='coexist' and row['votes']==['approve','reject']:
            imported=deepcopy(row)
            imported.update(id=row['id']+'-legacy-import',mode='legacy_vote_conflict')
            imported['expected'].update(status='review_conflict',effect='none',accepted_votes=0)
            cases.append(imported)
    return dict(version='records-diagnostic-v1.1',synthetic=True,relation_labels_are_inputs=True,
                independent_story_templates=len(STORIES),cases=cases)


if __name__=='__main__':
    Path('evaluation/records/cases.json').write_text(json.dumps(build(),ensure_ascii=False,indent=2)+'\n')
