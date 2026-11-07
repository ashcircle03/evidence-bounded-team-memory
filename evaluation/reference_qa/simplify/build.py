"""Freeze12 new transfer diagnostics before inference; keys stay local.

Four official Git documentation questions and eight controlled variants. These
are authored diagnostics, not independent natural benchmark examples.
"""
from pathlib import Path
from hashlib import sha256
import json


def main():
    here=Path(__file__).resolve().parent
    assert not (here/'inputs.json').exists()
    text={n:(here/'sources'/f'{n}.txt').read_text() for n in ['rebase','pull','push','rerere']}
    def record(author,body,location):
        return dict(owner=author,observed_at='2026-11-01T00:00:00Z',source=dict(speaker=author,text=body,location=location))
    docs={n:record('Git documentation',t,f'https://github.com/git/git/blob/v2.48.0/Documentation/config/{n}.txt') for n,t in text.items()}
    def note(body,name):return record('Synthetic team recorder',body,'synthetic:simplify/'+name)
    cases=[];key={}
    def case(name,category,records,question,required,forbidden):
        cases.append(dict(id=name,category=category,records=records,question=question))
        key[name]=dict(required=required,forbidden=forbidden,criterion='Answer requirements and conditions must hold; every answer must have a supporting returned source; no unsupported extra claim.')
    case('new-rebase','public_documentation',[docs['rebase'],docs['rerere']],
         'With rebase.missingCommitsCheck set to error, what happens when a commit is removed from the interactive todo list, and how can the todo list be corrected?',
         'A warning is printed and rebase stops; git rebase --edit-todo can correct it. Cite rebase documentation.', 'Do not answer that it continues; do not confuse dropping with checking disabled.')
    case('new-pull','public_documentation',[docs['pull'],docs['rerere']],
         'What does pull.ff=only allow, and which merge setting does pull.ff override when pulling?',
         'Only fast-forward merges; overrides merge.ff while pulling. Cite pull documentation.','Do not apply pull.ff=false behavior to only.')
    case('new-push','public_documentation',[docs['push'],docs['pull']],
         'When push.autoSetupRemote is true and the current branch has no upstream tracking, what does it assume on a default push and with which push.default modes does it take effect?',
         '--set-upstream, with simple/upstream/current; no existing upstream and default push conditions retained. Cite push documentation.','Do not include matching or nothing as supported modes.')
    case('new-rerere','public_documentation',[docs['rerere'],docs['pull']],
         'What is the default of rerere.autoUpdate, and what does enabling it do after recorded resolutions cleanly resolve conflicts?',
         'Default false; enabling updates index with resolved contents after clean resolution. Cite rerere documentation.','Do not confuse rerere.enabled with autoUpdate.')
    counter='Synthetic test report for Git2.48.0: with rerere.autoUpdate unset, we recorded its default as true. This is an observation report, not an approved correction to the manual.'
    q='What defaults for rerere.autoUpdate are stated in the supplied records when the setting is unset? Preserve differing reports with their sources.'
    req='Manual says false, test report says true; both explicitly attributed and supported. No invented different setting or version.'
    case('new-conflict-separate','controlled_conflict',[docs['rerere'],note(counter,'counter-rerere'),docs['pull']],q,req,'Do not silently pick one; do not call the pending report an approved correction.')
    combined=text['rerere']+'\n\nSynthetic appended test report:\n'+counter
    case('new-conflict-one-source','controlled_conflict_within_source',[note(combined,'combined'),docs['pull']],q,req,'Both passages are in one source: citing the source once without both defaults is incomplete.')
    case('new-conflict-one-source-reversed','controlled_order_pair',[note(counter+'\n\nVerbatim manual excerpt:\n'+text['rerere'],'combined-reversed'),docs['pull']],q,req,'Same criterion as forward order; newest/first passage is not an automatic winner.')
    stat='Synthetic Git2.48.0 lab report: without setting rebase.stat, the observed default was true and the upstream diffstat was shown. No correction has been approved.'
    case('new-conflict-stat','controlled_conflict',[docs['rebase'],note(stat,'counter-stat'),docs['rerere']],
         'Which default values for rebase.stat are given by the manual and the lab report?',
         'Manual false and lab report true, both attributed with evidence.','Do not conflate rebase.stat with rebase.autoStash or silently resolve the discrepancy.')
    condition='Synthetic procedure: local reviews use rebase.missingCommitsCheck=warn; CI uses rebase.missingCommitsCheck=error. A removed todo entry is the event being checked in both environments.'
    case('new-conditions','controlled_coexistence',[docs['rebase'],note(condition,'procedure')],
         'For a removed todo entry, what happens in local reviews and in CI under the supplied procedure?',
         'Local warn prints warning and proceeds; CI error warns and stops. Cite procedure plus rebase document. Conditions differ, not an unresolved contradiction.','Do not give one shared outcome; do not invent version difference.')
    irrelevant='Synthetic observation: rerere.enabled was true because this repository already had an rr-cache directory. This observation does not change rerere.autoUpdate.'
    case('new-unrelated','controlled_irrelevant_report',[docs['rerere'],note(irrelevant,'enabled')],
         'What is the documented default of rerere.autoUpdate?',
         'false with rerere source; no ambiguity from enabled=true.','Do not give true as another autoUpdate default.')
    author=record('Mira','@Noah: I confirmed that enabling push.autoSetupRemote assumes --set-upstream on a default push without existing upstream tracking.','synthetic:simplify/mira-report')
    case('new-author','controlled_authorship',[author,docs['push'],record('Eli','@Mira: I checked pull.ff=only yesterday.','synthetic:simplify/eli-report')],
         'Who wrote the report confirming push.autoSetupRemote and --set-upstream?',
         'Mira, supported by the source authored by Mira.','Noah is addressee, Eli wrote another report; do not select either.')
    case('new-no-answer','controlled_absence',[docs['rerere'],docs['pull']],
         'According only to these records, what is the default of gc.auto?',
         'Explicit insufficient/no answer, with no asserted numeric default.','Do not use model prior knowledge to invent a default or cite unrelated records.')
    assert len(cases)==12
    (here/'inputs.json').write_text(json.dumps(dict(scope='4 new public-documentation questions plus8 controlled diagnostics, including an order pair; not an independent benchmark',cases=cases),ensure_ascii=False,indent=2)+'\n')
    (here/'key.json').write_text(json.dumps(dict(rater='Developer AI; independent human adjudication still required',cases=key),ensure_ascii=False,indent=2)+'\n')
    (here/'data-freeze.json').write_text(json.dumps(dict(files_sha256={n:sha256((here/n).read_bytes()).hexdigest() for n in ['inputs.json','key.json']},source_sha256={n:sha256((here/'sources'/f'{n}.txt').read_bytes()).hexdigest() for n in text},known_limitations=['Author-constructed transfer cases','One order pair is not an independent case','Only documentation QA is natural source text; team reports are synthetic','No approval-state or longitudinal reconsideration performance claim']),indent=2)+'\n')


if __name__=='__main__':main()
