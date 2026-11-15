"""Freeze query-free source inputs and predeclared binding probes before inference."""
import json
from pathlib import Path
from team_memory.adapters.legacy import public_source


def main():
    old=json.loads(Path('evaluation/record_graph/inputs.json').read_text())
    sources=[]
    for c in old['cases']:
        sources.extend(dict(source=s,origin=c['origin'],case_id=c['id'],arms=['grouped']) for s in c['sources'])
    probes=[]
    def probe(s,anchor,condition=(),basis=(),absent=(),forbidden=()):
        for t in [anchor,*condition,*basis,*forbidden]:assert t in s['text'],t
        probes.append(dict(source_id=s['id'],anchor=anchor,condition=list(condition),basis=list(basis),absent=list(absent),forbidden=list(forbidden)))
    # Existing failures: minimal action anchors replace sentence boundaries in this
    # NEW diagnostic only. Old 10 requirements are left untouched and reported separately.
    for item in sources:
        s=item['source'];t=s['text']
        if 'This task can be implemented using polling for now' in t:
            probe(s,'implemented using polling',basis=["our message push service isn't fully ready yet"])
            probe(s,'we can upgrade it uniformly',condition=['Once the WebSocket service is stable later'])
        if 'must be forcibly routed' in t:probe(s,'must be forcibly routed',condition=['ACCOUNT_STATUS_LOCKED'])
        if 'We defer the throughput experiment for version 4.' in t:
            probe(s,'We defer the throughput experiment',condition=['version 4'],basis=['one writer only'])
        if 'We defer the throughput experiment because' in t:
            probe(s,'We defer the throughput experiment',condition=['version 4 on CPU only'],basis=['only one writer is available'])
    controls=[
      ('causal','Because the sensor is overheating, suspend acquisition until it cools. The backup log is green.',
       [('suspend acquisition',['until it cools'],['the sensor is overheating'],[],['backup log'])]),
      ('conditional','If the sample is saline, use tray R. If the sample is dry, use tray S.',
       [('use tray R',['sample is saline'],[],['basis'],['sample is dry']),('use tray S',['sample is dry'],[],['basis'],['sample is saline'])]),
      ('adjacent','The printer is offline. We retain the budget unchanged. The roof was repaired.',
       [('retain the budget unchanged',[],[],['condition','basis'],['printer','roof'])]),
      ('negation','For contaminated batches, do not release the lot because the assay failed. Clean batches remain eligible.',
       [('do not release the lot',['contaminated batches'],['the assay failed'],[],['Clean batches'])]),
      ('interleaved','At pressures above 8 bar, stop pump X because its casing is cracked. The spare badge is orange. At pressures below 2 bar, start pump Y because the reservoir needs refill.',
       [('stop pump X',['pressures above 8 bar'],['its casing is cracked'],[],['pressures below 2 bar','reservoir needs refill']),('start pump Y',['pressures below 2 bar'],['reservoir needs refill'],[],['pressures above 8 bar','casing is cracked'])]),
      ('proposal','For coastal sites, we might trial coating N next quarter; no durability measurement exists. This is not approval to deploy it.',
       [('might trial coating N',['coastal sites'],[],['basis'],[])]),
      ('far','The following cancellation concerns turbine T9 in winter. '+'The inventory shelf remains unchanged. '*8+'Cancel the vibration trial because the mount is broken.',
       [('Cancel the vibration trial',['turbine T9 in winter'],['the mount is broken'],[],[])]),
      ('coincidence','Rain began at 14:00. The valve closed at 14:00. The record does not establish a cause for the closure.',
       [('valve closed',[],[],['condition','basis'],[])])]
    for i,(name,text,reqs) in enumerate(controls):
        s=public_source(dict(owner='Mira',observed_at='2026-11-15T00:00:00Z',source=dict(speaker='Mira',location='synthetic-record-groups://'+name,text=text)))
        sources.append(dict(source=s,origin='new implementation-authored synthetic contrast',case_id=name,arms=['baseline','grouped'] if i%2==0 else ['grouped','baseline']))
        for anchor,cond,basis,absent,forbidden in reqs:probe(s,anchor,cond,basis,absent,forbidden)
    p=Path('evaluation/record_groups')
    (p/'inputs.json').write_text(json.dumps(dict(version='record-groups-v1',sources=sources),ensure_ascii=False,indent=2)+'\n')
    (p/'key.json').write_text(json.dumps(dict(annotation='Partial implementation-authored diagnostic probes; not independent semantic gold. Existing probes are development data. New contrasts are also authored by implementer.',probes=probes),ensure_ascii=False,indent=2)+'\n')
    print('sources',len(sources),'calls',sum(len(s['arms']) for s in sources),'probes',len(probes))

if __name__=='__main__':main()
