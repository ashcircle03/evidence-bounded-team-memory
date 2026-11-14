"""Freeze diagnostic source inputs separately from the provisional scoring key.

Existing failure cases are development data. Selecting decisive messages isolates
record construction at oracle-source coverage, not end-to-end retrieval quality.
"""
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path
from team_memory.adapters.legacy import public_source

ROOT=Path(__file__).resolve().parents[2]


def prepare():
    path=ROOT/'results/reference-qa/format-recovery-v1/retrieval-audit.json'
    audit=json.loads(path.read_text())
    identifiers=['F_SH_Top01_026','F_SH_Top02_014','F_TP_Top01_002','MA_U_Top01_005','MA_P_Top02_083']
    cases=[]
    for cid in identifiers:
        row=audit[cid];sources=[]
        for m in row['decisive_native_messages']:
            # Upstream timestamps have no timezone. UTC is an explicit adapter
            # convention for stable storage, not a claim about the original zone.
            sources.append(public_source(dict(owner=m['speaker'],observed_at=m['time'].replace(' ','T')+'Z',
                                              source=dict(speaker=m['speaker'],location=m['location'],text=m['dialogue']))))
        cases.append(dict(id=cid,origin='EverMem existing development failure diagnosis',sources=sources,question=row['question']))
    # New synthetic contrasts isolate conditions, scope, and reported approval.
    stories=[('version-defer','Version 4 permits one writer only. We defer the throughput experiment for version 4. Archive is Orion.',
              'Version 5 permits four writers. This report does not replace the version 4 observation.',
              'What was deferred, why, and does the version 5 report invalidate the version 4 observation?'),
             ('hypothesis','Under profile A, latency is 120ms. Owner is Hana.',
              'I suspect profile B may reach 90ms. This is an untested proposal; no measurement is available.',
              'What was measured and what is only an untested proposal?'),
             ('reported-approval','The retry limit is 3. The maintainer is Hana.',
              'Jun says: "Hana approved changing the retry limit to 4." No authenticated review event is supplied here.',
              'What does this record report, and can it establish an authenticated approval?'),
             ('far-condition','This experiment concerns version 4 on CPU only. '+'The archive reference remains unchanged. '*8+'We defer the throughput experiment because only one writer is available.',
              'Version 5 on GPU allows four writers; this has not been tested on version 4.',
              'Under what conditions was the experiment deferred?')]
    for cid,a,b,q in stories:
        sources=[public_source(dict(owner=who,observed_at=f'2026-11-0{i}T00:00:00Z',source=dict(speaker=who,location=f'synthetic-record-graph://{cid}/{i}',text=text)))
                 for i,(who,text) in enumerate([('Hana',a),('Jun',b)],1)]
        cases.append(dict(id=cid,origin='synthetic diagnostic contrast',sources=sources,question=q))
    inputs=dict(version='record-graph-dev-v1',cases=cases)
    # Provisional requirements: independent of generated graph/output, but
    # implementation-agent annotated, not a human-adjudicated benchmark gold.
    requirements={
        'F_SH_Top01_026':[dict(claim='The final test report has been uploaded to Confluence.',subject=['Verify the accuracy of alarm rule creation and trigger logic'])],
        'F_SH_Top02_014':[dict(claim='your medication check-in module and family member invitation interface are due today',subject=['@Hanqiang Liang and @Huihong Tian'],time=['Today is Thursday.'])],
        'F_TP_Top01_002':[dict(claim='I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday',time=['last Friday'],subject=['file storage solution'])],
        'MA_U_Top01_005':[dict(claim='must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy',condition=['ACCOUNT_STATUS_LOCKED'])],
        'MA_P_Top02_083':[dict(claim='This task can be implemented using polling for now',basis=["our message push service isn't fully ready yet"],condition=["our message push service isn't fully ready yet"]),
                               dict(claim='we can upgrade it uniformly',condition=['Once the WebSocket service is stable later'])],
        'version-defer':[dict(claim='We defer the throughput experiment for version 4.',condition=['version 4'],basis=['Version 4 permits one writer only.'],stance=['decision'])],
        'hypothesis':[dict(claim='I suspect profile B may reach 90ms.',condition=['profile B'],basis=['no measurement is available'],stance=['proposal','uncertainty'])],
        'reported-approval':[dict(claim='Hana approved changing the retry limit to 4.',basis=['No authenticated review event is supplied here.'])],
        'far-condition':[dict(claim='We defer the throughput experiment because only one writer is available.',condition=['version 4 on CPU only'],basis=['only one writer is available'],stance=['decision'])],
    }
    for case in cases:
        for requirement in requirements[case['id']]:
            assert any(requirement['claim'] in s['text'] for s in case['sources']),case['id']
            for role,anchors in requirement.items():
                if role in ('claim','stance'):continue
                for a in anchors:assert any(a in s['text'] for s in case['sources']),(case['id'],a)
    key=dict(annotation='implementation-agent provisional diagnostic requirements, not exhaustive or independent gold',
             requirements=requirements,qa_gold={cid:audit[cid]['gold_answer'] for cid in identifiers})
    folder=ROOT/'evaluation/record_graph'
    (folder/'inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
    (folder/'key.json').write_text(json.dumps(key,ensure_ascii=False,indent=2)+'\n')
    manifest=dict(created_at=datetime.now(timezone.utc).isoformat(),upstream_archive_sha256=sha256(path.read_bytes()).hexdigest(),
                  cases=len(cases),sources=sum(len(c['sources']) for c in cases),
                  source_selection='Existing decisive messages; oracle source coverage; not retrieval or unseen generalization',
                  timestamp_convention='Unzoned upstream times assigned UTC for adapter only; no elapsed-time semantics validated',
                  files={n:sha256((folder/n).read_bytes()).hexdigest() for n in ('inputs.json','key.json')})
    (folder/'data-freeze.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))


if __name__=='__main__':prepare()
