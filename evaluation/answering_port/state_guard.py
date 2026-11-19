"""Pass eight frozen post-attribution answers through the public port's output conversion."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Lock
from unittest.mock import patch

from team_memory.adapters.answering import AnsweringAdapter
from team_memory.adapters.base import request
from team_memory.adapters.legacy import state_witness
from team_memory.adapters.reader_bridge import evidence_from
from team_memory.adapters.records import RecordsAdapter
from team_memory.contracts.ports import CallContext
from team_memory.readers.state_citations import render_snapshot
from team_memory.storage.sources import SourceStore

CASES = ('release-correction/pending', 'release-correction/approved', 'rejected-calendar/rejected',
         'new-temperature/pending', 'new-temperature/approved', 'new-retention/current',
         'new-retention/proposal', 'new-vote-conflict/current')


def run(folder):
    base = Path('results/module-boundary/v1')
    saved = json.loads((base/'result.json').read_text())
    ratings = json.loads((base/'ratings.json').read_text())
    selected = {r['case_id']+'/'+r['label']:r for r in saved['rows'] if r['request']['operation']=='ask'}
    rows = []
    for key in CASES:
        row = selected[key]
        old = row['result']
        originals = old['citation_sources']
        review, = [w for w in originals if w.get('evidence_type') == 'review_state']
        frozen = review['record_snapshot']
        assert render_snapshot(frozen)[review['start']:review['end']] == review['quote']
        objects = saved['stores'][row['case_id']]
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = SourceStore(root)
            for sid in frozen['source_ids']:
                assert store.put('sources', objects['sources'][sid]) == sid
            pid = review['proposal_id']
            assert store.put('timeline_proposals', objects['timeline_proposals'][pid]) == pid
            for vid, vote in frozen['votes'].items():
                assert store.put('timeline_votes', vote) == vid
            snapshot = RecordsAdapter(root,'guard').snapshot()
            proposal, = snapshot['proposals']
            assert proposal['status'] == frozen['proposal']['status'] and proposal['id'] == pid
            evidence = [evidence_from(state_witness(snapshot,proposal) if w is review else w,snapshot,i)
                        for i,w in enumerate(originals,1)]
            bundle = dict(snapshot=snapshot,query=dict(text=row['request']['question'],time_scope='current',
                          as_of=None,conditions=[]), evidence=evidence,coverage='hits',
                          unresolved_proposal_ids=[pid] if proposal['status'] in ('pending','review_conflict') else [])
            class FinalDraft:
                lock = Lock()
                def generate_evidence(self, question, witnesses, context):
                    return dict(raw=old['raw'],citation_sources=witnesses,status=old['status'])
            port = AnsweringAdapter('guard',lambda _:FinalDraft(),root/'diag',snapshot_loader=lambda _:snapshot)
            req = request('answer.generate',dict(bundle=bundle),workspace_id='guard',request_id=key)
            # Start where the frozen result was recorded, after citation repair.
            with patch('team_memory.adapters.answering.attach_citations', side_effect=lambda _,q,r:r):
                res=port.handle(req,context=CallContext('guard','tester',frozenset(['answer:generate'])))
            assert res['data'] is not None,res
            answer=res['data']
            owned={eid for c in answer['claims'] for eid in c['evidence_ids']}
            def identity(w):
                if w.get('evidence_type')=='review_state':
                    return ('review',w['proposal_id'],w['record_snapshot']['proposal']['status'])
                return (w['source_id'],w['start'],w['end'],w['quote'])
            expected={identity(w) for a in old['answers'] for w in a['evidence']}
            actual={identity(w) for e,w in zip(evidence,originals) if e['id'] in owned}
            rows.append(dict(case=key,answer_equal=answer['original_text']==old['raw'],
                evidence_equal=actual==expected,state_cited=('review',pid,proposal['status']) in actual,
                historical_rating=ratings[key],status=res['status']))
    folder.mkdir(exist_ok=True,parents=True)
    (folder/'state8.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    assert all(r['answer_equal'] and r['evidence_equal'] and r['state_cited'] for r in rows),rows


if __name__=='__main__':
    run(Path('results/answering-port/outcome-contract'))
