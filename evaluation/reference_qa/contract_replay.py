"""Replay old physical model responses; verify state fixes preserve answers.

No fresh inference. Historical judge responses came from max_tokens1024;
the corrected384 setting is checked separately at the HTTP boundary in tests.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from threading import Lock,RLock
from types import SimpleNamespace
from unittest.mock import patch


def main(output=None):
    from team_memory.reference_qa import ReferenceQA,format_response
    from team_memory.reference_attributed import AttributedQA
    root=Path(__file__).resolve().parents[2];base=root/'results/reference-qa/quote-normalized-v1'
    cards=json.loads((base/'cards.json').read_text())
    calls=[json.loads(l) for l in (base/'calls.jsonl').read_text().splitlines()]
    used=[];drafts=[];rows=[];lock=Lock()
    for cid,card in cards.items():
        physical=[c for c in calls if c['context']==dict(case_id=card['case_id'],label=card['label'])]
        first=min(physical,key=lambda c:c['id']);expected=card['result']
        assert first['response']['choices'][0]['message']['content']==expected['draft_raw'];drafts.append(first['id'])
        class Replay:
            def chat(self,messages,**kwargs):
                actual=[dict(role=m.role.value,content=m.content) for m in messages]
                matches=[c for c in physical if c['request']['messages']==actual];assert len(matches)==1,(cid,len(matches))
                call=matches[0]
                with lock:assert call['id'] not in used;used.append(call['id'])
                return SimpleNamespace(message=SimpleNamespace(content=call['response']['choices'][0]['message']['content']))
        q=expected['alce']['question'];draft=format_response(q,expected['draft_raw'],expected['citation_sources'],allow_source_labels=True)
        service=object.__new__(AttributedQA);service.lock=RLock();service.llm=Replay()
        with patch.object(ReferenceQA,'ask',return_value=deepcopy(draft)):result=service.ask(q)
        assert result['raw']==expected['raw'],cid
        assert result['answers']==expected['answers'],cid
        rows.append(dict(id=cid,answer_and_evidence_unchanged=True,old_status=expected['status'],status=result['status'],
                         stage_failures=result.get('stage_failures',[])))
    assert set(used+drafts)=={c['id'] for c in calls}
    out=dict(cases=len(rows),post_retrieval_calls_replayed=len(used),draft_calls_verified=len(drafts),
        fresh_model_calls=0,gpu_minutes=0,rows=rows,
        source_sha256={str(p.relative_to(root)):sha256(p.read_bytes()).hexdigest() for p in [root/'team_memory'/n for n in ['reference_checked.py','reference_quotes.py','reference_attributed.py','reference_fallback.py']]},
        preserved_files_sha256={n:sha256((base/n).read_bytes()).hexdigest() for n in ['cards.json','ratings.json','calls.jsonl']},
        limitation='Historical responses replayed, not new inference with the corrected384 judge limit. Retrieval not re-executed.')
    path=Path(output) if output else root/'results/reference-qa/contract-v1/replay.json';path.parent.mkdir(exist_ok=True,parents=True);path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(cases=len(rows),calls=len(used),unchanged=len(rows),status_changes=sum(r['old_status']!=r['status'] for r in rows))))


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Write a new replay artifact without replacing historical results')
    main(parser.parse_args().output)
