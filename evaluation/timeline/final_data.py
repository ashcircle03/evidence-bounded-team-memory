"""Held-out controlled workflows, authored after code freeze and before inference.

Worklogs are synthetic. Natural messages/questions are untouched support-selected
EverMemBench-Dynamic topic 02 records. Keys never enter comparison/index/QA calls.
"""
from datetime import datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path
from team_memory.store import digest
from .build import HERE, ROOT, envelope, make_stream, write

REVISION = 'a6b210a32248e841967b7b64a64281d2ff3f669d'
NATURAL = [0,2,4,5,6,8,9,10,11,12,14,16,17,18,19,20,22,23,25,26]

# A gold reason names the changed premise, not just a newer or better number.
STORIES = [
 dict(name='Harbor',kind='reconsider',
      old='With the CPU-only worker, Harbor thumbnail rendering took 18 minutes per album. We shelved Harbor GPU trials because production workers have no GPU.',
      new='Production workers now include a supported GPU. With the GPU-enabled worker, Harbor thumbnail rendering took 3 minutes per album. This does not revise the CPU-only measurement.',
      ov='18 minutes',nv='3 minutes',oc='CPU-only worker',nc='GPU-enabled worker',metric='thumbnail rendering times per album',
      reason='The no-GPU production constraint that justified shelving GPU trials has changed; the new GPU result warrants reconsidering those trials, while the CPU result remains scoped.'),
 dict(name='Lumen',kind='reconsider',
      old='On the English-only validation set, Lumen multilingual routing had 72% accuracy. We stopped evaluating that routing because the release supported English only.',
      new='The release now supports Korean as well as English. On the bilingual validation set, Lumen multilingual routing had 88% accuracy. The English-only result is unchanged.',
      ov='72%',nv='88%',oc='English-only validation set',nc='bilingual validation set',metric='multilingual routing accuracies',
      reason='The English-only release scope underlying the stopped evaluation changed to bilingual support. The two accuracies are not a controlled same-set improvement.'),
 dict(name='Granite',kind='reconsider',
      old='At the 256 MB memory cap, Granite compressed lookup took 9 seconds per request. We deferred the large-dictionary variant because its dictionary could not fit within that cap.',
      new='Deployment now provides a 2 GB memory cap. At the 2 GB memory cap, Granite large-dictionary compressed lookup took 2 seconds per request and the dictionary fit in memory. The 256 MB observation remains valid.',
      ov='9 seconds',nv='2 seconds',oc='256 MB memory cap',nc='2 GB memory cap',metric='compressed lookup times per request',
      reason='The memory-cap reason for deferring the large dictionary no longer holds in the new deployment; preserve the old constrained measurement.'),
 dict(name='Kite',kind='reconsider',
      old='Using the serial-loader release, Kite import took 27 minutes per archive. We ruled out the parallel loader for production because the vendor had not released a supported build.',
      new='The vendor has released a supported parallel-loader build for production. Using the parallel-loader release, Kite import took 11 minutes per archive. The serial-loader result has not been retracted.',
      ov='27 minutes',nv='11 minutes',oc='serial-loader release',nc='parallel-loader release',metric='import times per archive',
      reason='A supported build now exists, removing the specific availability reason for ruling out the parallel loader; neither result is erased.'),
 dict(name='Delta',kind='coexist',
      old='Under the wired-LAN profile, Delta request latency was 8 milliseconds.',
      new='Under the mobile-WAN profile, Delta request latency was 130 milliseconds. No wired-LAN measurement is being corrected.',
      ov='8 milliseconds',nv='130 milliseconds',oc='wired-LAN profile',nc='mobile-WAN profile',metric='request latencies',
      reason='Different network profiles support coexisting latency observations, with no earlier decision or same-condition contradiction.'),
 dict(name='Meadow',kind='coexist',
      old='On the indoor-camera set, Meadow object detection reached 94% recall.',
      new='On the outdoor-camera set, Meadow object detection reached 81% recall. The indoor set was not rerun.',
      ov='94%',nv='81%',oc='indoor-camera set',nc='outdoor-camera set',metric='object detection recalls',
      reason='Indoor and outdoor sets differ; retain both scoped results and do not infer a regression or request decision reversal.'),
 dict(name='Fjord',kind='coexist',
      old='For the 10-file fixture, Fjord indexing peaked at 120 MB of memory.',
      new='For the 1000-file fixture, Fjord indexing peaked at 940 MB of memory. This report covers only the larger fixture.',
      ov='120 MB',nv='940 MB',oc='10-file fixture',nc='1000-file fixture',metric='indexing peak memory measurements',
      reason='The fixture sizes differ; neither peak contradicts or supersedes the other.'),
 dict(name='Mosaic',kind='coexist',
      old='With weekly retention, Mosaic archive storage cost was 14 dollars per month.',
      new='With annual retention, Mosaic archive storage cost was 86 dollars per month. Both retention plans remain available.',
      ov='14 dollars',nv='86 dollars',oc='weekly retention',nc='annual retention',metric='monthly archive storage costs',
      reason='Different retention scopes legitimately have different monthly costs; no recorded decision needs reopening.'),
 dict(name='Anchor',kind='conflict',
      old='Under build A8 defaults, the Anchor connection limit is 64 connections.',
      new='My independent reading under the same build A8 defaults gives the Anchor connection limit as 96 connections. Neither report has been withdrawn and the mismatch is unresolved.',
      ov='64 connections',nv='96 connections',oc='build A8 defaults',nc='build A8 defaults',metric='connection limit',
      reason='Two unwithdrawn limits describe the same build and defaults, so preserve both and request resolution rather than selecting the later one.'),
 dict(name='Beacon',kind='conflict',
      old='On the frozen B2 evaluation set, Beacon classification accuracy is 83%.',
      new='An independent calculation on the same frozen B2 evaluation set reports Beacon classification accuracy as 87%. We have not reconciled the two calculations or established that either is an error.',
      ov='83%',nv='87%',oc='frozen B2 evaluation set',nc='frozen B2 evaluation set',metric='classification accuracy',
      reason='The same frozen evaluation set has two unresolved accuracy calculations; a higher later number is not evidence of an accepted correction.'),
 dict(name='Cobalt',kind='conflict',
      old='For snapshot C5 after the agreed filters, the Cobalt row count is 4200 rows.',
      new='My separate count for the same snapshot C5 after the agreed filters is 4170 rows. We have not determined the cause of disagreement and neither count is retracted.',
      ov='4200 rows',nv='4170 rows',oc='snapshot C5 after the agreed filters',nc='snapshot C5 after the agreed filters',metric='row count',
      reason='Snapshot and filters match, but counts differ with no resolution. Both sources must remain available.'),
 dict(name='Drift',kind='conflict',
      old='In the staging D4 configuration, the Drift callback port is 8082.',
      new='My independent inspection of the same staging D4 configuration reports the Drift callback port as 8092. No configuration change is recorded and the disagreement remains open.',
      ov='8082',nv='8092',oc='staging D4 configuration',nc='staging D4 configuration',metric='callback port',
      reason='The inspections concern the same configuration without a recorded change; request resolution and do not infer a new configuration or correction.'),
 dict(name='Elm',kind='correction',
      old='For release E6, the Elm export batch size is 150 records.',
      new='I correct my earlier Elm export batch-size note: I transcribed the count incorrectly. For the same release E6, the batch size is 105 records. No other assertion in my earlier note is retracted.',
      ov='150 records',nv='105 records',oc='release E6',nc='release E6',metric='export batch size',
      reason='The original author explicitly corrects the transcribed batch size under the same release. Only that assertion changes after owner approval.'),
 dict(name='Flint',kind='correction',
      old='For the F3 review round, the Flint submission deadline is 17:00 UTC.',
      new='I retract the deadline in my earlier Flint note because I copied the wrong hour. For the same F3 review round, the submission deadline is 15:00 UTC. The rest of the earlier note still applies.',
      ov='17:00 UTC',nv='15:00 UTC',oc='F3 review round',nc='F3 review round',metric='submission deadline',
      reason='An explicit same-round author correction changes the deadline assertion after review, without changing other facts in the old note.'),
 dict(name='Grove',kind='correction',
      old='In the G9 timing run, Grove startup took 46 seconds.',
      new='I correct my earlier Grove startup duration because I reversed two digits in the log summary. In the same G9 timing run, startup took 64 seconds. This is a transcription correction, not a new timing run.',
      ov='46 seconds',nv='64 seconds',oc='G9 timing run',nc='G9 timing run',metric='startup duration',
      reason='The author retracts a transcribed value for the identical timing run; it is a pending correction before review, not a new condition or performance regression.'),
 dict(name='Haven',kind='correction',
      old='Under policy H2, the Haven alert threshold is 0.75.',
      new='I correct the threshold in my earlier Haven policy note: the decimal value was mistyped. Under the same policy H2, the alert threshold is 0.57. The policy itself did not change.',
      ov='0.75',nv='0.57',oc='policy H2',nc='policy H2',metric='alert threshold',
      reason='Explicit same-policy author correction changes only the mistyped threshold, pending owner approval; the policy did not evolve.'),
 dict(name='Islet',kind='irrelevant',
      old='The Islet retry limit is 6 attempts. We deferred the transport rollout because failover testing is incomplete.',
      new='The Islet troubleshooting guide now has 22 pages after copyediting. No failover test or transport run was performed.',
      ov='6 attempts',nv='22 pages',oc='',nc='',metric='retry limit',
      reason='Guide length gives no new evidence about retry behavior or the missing failover validation; do not reopen the rollout decision.'),
 dict(name='Juniper',kind='irrelevant',
      old='The Juniper query timeout is 25 seconds. We postponed the database index migration until lock contention is measured.',
      new='The Juniper dashboard font size is now 16 pixels. This visual change includes no database benchmark or lock measurement.',
      ov='25 seconds',nv='16 pixels',oc='',nc='',metric='query timeout',
      reason='A dashboard font change is unrelated to timeout or the missing lock-contention evidence.'),
 dict(name='Knoll',kind='irrelevant',
      old='Knoll validation precision is 91%. We rejected deployment because the offline bias audit is unfinished.',
      new='The Knoll planning agenda now has 7 topics. The meeting covered scheduling only, and no model evaluation or bias audit was run.',
      ov='91%',nv='7 topics',oc='',nc='',metric='validation precision',
      reason='An agenda edit does not resolve the missing bias audit or change measured precision.'),
 dict(name='Lagoon',kind='irrelevant',
      old='Lagoon build startup takes 32 seconds. We suspended the compiler switch because the target ABI has not been validated.',
      new='Lagoon shipping labels now use 10-point text. This packaging change has no compiler build or ABI validation results.',
      ov='32 seconds',nv='10-point text',oc='',nc='',metric='build startup duration',
      reason='A packaging typography update provides no evidence about startup or the unvalidated target ABI.'),
]


def build():
    freeze=json.loads((HERE/'freeze.json').read_text())
    for path,h in freeze['files'].items():assert sha256((ROOT/path).read_bytes()).hexdigest()==h,path
    candidates=json.loads((HERE/'natural-candidates.json').read_text())
    rows=[];keys={};selection=[]
    for i,(story,ni) in enumerate(zip(STORIES,NATURAL),1):
        uid=f'final-{i:02d}';s=story;c=candidates[ni];m=c['message'];date,group,index=c['key']
        # Dataset timestamps have no explicit timezone. UTC is an ordering convention,
        # not a claim about the actual location/timezone of the original conversation.
        at=datetime.fromisoformat(m['time']).replace(tzinfo=__import__('datetime').timezone.utc).isoformat()
        location=f'EverMemBench-Dynamic@{REVISION}/02/{date}/{group}/{index}'
        natural=dict(id=c['id'],question=c['question'],answer=c['answer'],
                     envelope=envelope(m['dialogue'],location,m['speaker'],at))
        extra=f" The evidence archive is {s['name']}-evidence."
        before=f"What {s['metric']} was reported for {s['name']}"+(f" under {s['oc']}?" if s['oc'] else '?')
        question=(f"What {s['metric']} were recorded for {s['name']} under each reported condition?"
                  if s['kind'] in ('reconsider','coexist') else
                  f"What is currently supported about the {s['name']} {s['metric']}, including any unresolved or pending report?"
                  if s['kind'] in ('conflict','correction') else before)
        row,key=make_stream(uid,s['kind'],natural,s['old']+extra,s['new'],s['ov'],s['nv'],s['oc'],s['nc'],
                            question,before,f"Where is the evidence archive for {s['name']}?",s['name']+'-evidence',
                            f"The {s['name']} status page now uses sentence case in headings. This note only records a typography edit.")
        incoming=next(x['source'] for x in reversed(row['steps']) if x['op']=='ingest')
        repeat=envelope('Unchanged follow-up: '+s['new']+' No additional observation or condition change is reported here.',
                        f'scenario://timeline/{uid}/repeat',incoming['owner'],
                        (datetime.fromisoformat(incoming['observed_at'])+timedelta(hours=1)).isoformat())
        row['steps'] += [dict(op='ingest',source=repeat),dict(op='ask',id='natural_after_repeat',question=c['question'])]
        key['qa']['natural_after_repeat']=key['qa']['natural_before']
        key.update(reason_criterion=s['reason'],repeat_source=digest(repeat),repeat_expected_alerts=0)
        rows.append(row);keys[uid]=key
        selection.append(dict(stream=uid,natural_id=c['id'],source_id=digest(natural['envelope']),location=location,
                              question=c['question'],answer=c['answer'],speaker=m['speaker'],original_text=m['dialogue'],
                              selection_reason='Manually checked that this original message supports the official short answer to this question.'))
    # Mix event types across both jobs, while keeping a whole stream/arm indivisible.
    ordered=[rows[j] for k in range(4) for j in range(k,20,4)]
    write(HERE/'final.json',ordered);write(HERE/'final-key.json',keys)
    write(HERE/'final-a.json',ordered[::2]);write(HERE/'final-b.json',ordered[1::2])
    write(HERE/'natural-selection.json',dict(revision=REVISION,topic='02',items=selection,
         timestamp_convention='Naive original timestamps interpreted as UTC only to provide deterministic ordering.',
         scope='20 source-checked short-answer items; original messages/questions unchanged; support-selected, not full-corpus retrieval. Synthetic worklogs and repeated arrivals are not official labels.'))
    files=['final_data.py','final.json','final-key.json','final-a.json','final-b.json','natural-selection.json']
    write(HERE/'data-freeze.json',dict(phase='before final inference; no development model output inspected',
          code_freeze_sha256=sha256((HERE/'freeze.json').read_bytes()).hexdigest(),
          files={name:sha256((HERE/name).read_bytes()).hexdigest() for name in files},
          cases=len(rows),natural_questions=len(selection),qa_checkpoints_per_arm=sum(len(k['qa']) for k in keys.values()),
          review_required_per_arm=sum(k['expected_review'] for k in keys.values()),
          grading='Grounded requires exact old/new target, correct relation kind, and explanation satisfying the source-based reason criterion. Reject invented conditions, reversed actors, unsupported causal claims, or loss of the actual old decision rationale. Coexistence is not a review alert. Repeated arrivals require zero new alerts.'))
    print('frozen',len(rows),'streams, 20 natural questions,',sum(len(k['qa']) for k in keys.values()),'QA checkpoints per arm')


if __name__=='__main__':build()
