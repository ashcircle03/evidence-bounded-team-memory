"""Replay recorded comparisons through restored service; NOT fresh model QA."""
import json,tempfile
from pathlib import Path
from hashlib import sha256
from team_memory.service import TeamMemoryService
from team_memory.source_store import SourceStore
from team_memory import timeline
from team_memory.review_citations import review_sources


def main():
    repo=Path(__file__).resolve().parents[2]
    base=repo/'results/service-completion/v3b'
    cfg=json.loads((base/'freeze.json').read_text())['config']
    unchanged=[n for n in cfg['code_sha256'] if n=='team_memory/service.py' or n=='team_memory/source_comparison.py'
               or n.startswith('team_memory/reference_') or n.startswith('team_memory/review_')]
    for name in unchanged:assert sha256((repo/name).read_bytes()).hexdigest()==cfg['code_sha256'][name],name
    inputs=json.loads((base/'runtime/inputs.json').read_text())
    prior=json.loads((base/'result.json').read_text())
    asks={(r['case_id'],r['label']):r for r in prior['rows'] if r['request']['operation']=='ask'}
    comparisons={c['context']['case_id']:c for c in map(json.loads,(base/'calls.jsonl').read_text().splitlines()) if c['context']['label']=='ingest'}
    class ImportOnlyReader:
        def __init__(self,path):self.store=SourceStore(path)
        def import_history(self,records):return dict(status='ok',source_ids=[self.store.capture_source(e) for e in records])
    checks=0;calls=0;cases=[]
    with tempfile.TemporaryDirectory() as temp:
        for c in inputs['streams']+inputs['transfer']:
            cid=c['id'];recorded=comparisons[cid]
            def generate(system,content):
                nonlocal calls
                assert [dict(role='system',content=system),dict(role='user',content=content)]==recorded['request']['messages'],cid
                calls+=1
                return recorded['response']['choices'][0]['message']['content']
            root=Path(temp)/cid
            service=TeamMemoryService(root,reader=ImportOnlyReader(root),generate=generate)
            service.import_history(c['initial']);ingested=service.ingest(c['incoming'])
            assert ingested['status']=='ok',cid
            for step in c['steps']:
                if step['operation']=='restart':
                    service=TeamMemoryService(root,reader=ImportOnlyReader(root),generate=generate);service.sync()
                elif step['operation']=='review_fixture':
                    for p in timeline.proposals(service.store):service.review(p['id'],p['reviewer'],step['choice'])
                elif step['operation']=='conflicting_votes_fixture':
                    for p in timeline.proposals(service.store):
                        for choice in ('approve','reject'):service.store.put('timeline_votes',dict(proposal=p['id'],actor=p['reviewer'],choice=choice))
                elif step['operation']=='ask':
                    row=asks[(cid,step['label'])]['result'];ctx=row.get('review_context')
                    if not ctx:continue
                    current={p['id']:p for p in timeline.proposals(service.store)}
                    for p in ctx['relations']:assert current[p['id']]==p
                    rendered={w['source_id']:w for w in review_sources(service.store,ctx)}
                    for w in row.get('citation_sources',[]):
                        if w.get('evidence_type')=='review_state':
                            now=rendered[w['source_id']]
                            assert now['quote'][w['start']:w['end']]==w['quote']
                            assert now['record_snapshot']==w['record_snapshot']
                            checks+=1
            cases.append(cid)
    report=dict(status='passed',scope='Exact recorded-comparison/state replay, not new QA inference',
        comparisons=calls,streams=len(cases),review_source_checks=checks,
        unchanged_service_and_qa_files=unchanged,
        semantic_limit='The old two reconsideration misclassifications and two unnecessary proposals remain unresolved.')
    dest=repo/'results/source-patch/restoration.json';dest.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='unchanged_service_and_qa_files'},indent=2))


if __name__=='__main__':main()
