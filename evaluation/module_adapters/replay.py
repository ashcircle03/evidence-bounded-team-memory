"""Replay measured Qwen outputs only when complete model requests match exactly.

This fixes the previously retrieved evidence. It is not fresh inference or a
retrieval benchmark. No reference answer is supplied to the runtime adapter.
"""
import argparse
from collections import defaultdict,deque
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
from threading import Lock


def key(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))


def run(base,output):
    import httpx,nltk
    from transformers import AutoTokenizer
    from llama_index.core.embeddings import MockEmbedding
    from llama_index.llms.openai_like import OpenAILike
    from team_memory.adapters.records import RecordsAdapter
    from team_memory.adapters.answering import AnsweringAdapter
    from team_memory.adapters.reader_bridge import evidence_from
    from team_memory.adapters.base import request
    from team_memory.contracts.ports import CallContext
    from team_memory.readers.attribution import AttributedQA
    from team_memory.storage.sources import SourceStore

    root=Path(__file__).resolve().parents[2]
    nltk.data.path.insert(0,str(root/'.cache/reference-nltk'))
    tokenizer=AutoTokenizer.from_pretrained(str(root/'.cache/qwen-tokenizer'),local_files_only=True)
    original=json.loads((base/'result.json').read_text())
    traces=[json.loads(line) for line in (base/'calls.jsonl').read_text().splitlines()]
    rows=[r for r in original['rows'] if r['split']=='legacy' and r['request']['operation']=='ask']
    report=dict(mode='exact-request recorded-response replay with fixed retrieved evidence',
                fresh_inference=False,retrieval_reevaluated=False,source_job_id=original['job_id'],
                input_sha256={name:sha256((base/name).read_bytes()).hexdigest() for name in ('result.json','calls.jsonl')},rows=[])
    context=CallContext('replay','reader',frozenset(['answer:generate']))
    with tempfile.TemporaryDirectory(prefix='module-qa-replay-') as temp:
        temp=Path(temp)
        for row in rows:
            cid,label=row['case_id'],row['label'];folder=temp/(cid+'-'+label)
            legacy=SourceStore(folder)
            for env in original['stores'][cid]['sources'].values():legacy.put('sources',env)
            snapshot=RecordsAdapter(folder,'replay').snapshot()
            selected=[t for t in traces if t['context']==dict(case_id=cid,split='legacy',label=label)]
            queue=defaultdict(deque)
            for t in selected:queue[key(t['request'])].append(t)
            matched=[];missed=[];lock=Lock()
            def transport(req):
                body=json.loads(req.content)
                with lock:
                    entries=queue[key(body)]
                    if not entries:
                        missed.append(body)
                        raise RuntimeError('No exact recorded request: replay refused')
                    recorded=entries.popleft();matched.append(recorded['id'])
                return httpx.Response(200,json=deepcopy(recorded['response']))
            with httpx.Client(transport=httpx.MockTransport(transport),trust_env=False) as client:
                llm=OpenAILike(model='Qwen3-8B',api_base='http://127.0.0.1:9999/v1',api_key='local-no-secret',
                    is_chat_model=True,is_function_calling_model=False,context_window=32768,max_tokens=1024,
                    tokenizer=tokenizer,temperature=0,timeout=90,max_retries=0,http_client=client,
                    additional_kwargs={'extra_body':{'chat_template_kwargs':{'enable_thinking':False}}})
                factory=lambda store:AttributedQA(store,llm=llm,embed_model=MockEmbedding(embed_dim=8),tokenizer=tokenizer,
                    context_window=32768,num_output=1024)
                adapter=AnsweringAdapter('replay',factory,folder/'private',snapshot_loader=lambda sid: snapshot if sid==snapshot['id'] else None)
                old=row['result'];bundle=dict(snapshot=snapshot,
                    query=dict(text=row['request']['question'],time_scope='current',as_of=None,conditions=[]),
                    evidence=[evidence_from(w,snapshot,i) for i,w in enumerate(old['citation_sources'],1)],
                    coverage='hits',unresolved_proposal_ids=[])
                result=adapter.handle(request('answer.generate',dict(bundle=bundle),workspace_id='replay',request_id=cid+label),context=context)
                diagnostics=list(adapter.diagnostics.load('answer_diagnostics').values())
                native=diagnostics[-1]['result'] if diagnostics else {}
                claims=(result.get('data') or {}).get('claims',[])
                evidence_by_id={e['id']:e for e in bundle['evidence']}
                mapped={(evidence_by_id[eid]['source_id'],evidence_by_id[eid]['start'],evidence_by_id[eid]['end'],evidence_by_id[eid]['quote'])
                        for c in claims for eid in c['evidence_ids']}
                old_cites={(w['source_id'],w['start'],w['end'],w['quote']) for a in old['answers'] for w in a['evidence']}
                comparison=dict(case_id=cid,label=label,status=result['status'],exact_requests_matched=len(matched),
                    expected_calls=len(selected),unmatched_requests=len(missed),unused_recordings=sum(len(q) for q in queue.values()),
                    native_answer_equal=native.get('raw')==old['raw'],native_evidence_equal=native.get('answers')==old['answers'],
                    public_answer_equal=(result.get('data') or {}).get('original_text')==old['raw'],
                    prior_revision_preserved=(not old.get('aqa_candidate_accepted') or
                        (result.get('data') or {}).get('unverified_revision',{}).get('original_text')==old['pre_aqa_raw']),
                    unattributed_segments=len((result.get('data') or {}).get('unattributed',[])),
                    claim_evidence_equal=mapped==old_cites)
                report['rows'].append(comparison)
                # Keep diagnostics for mismatches, not a fallback response.
                if missed:
                    output.mkdir(parents=True,exist_ok=True)
                    (output/(cid+'-'+label+'-unmatched.json')).write_text(json.dumps(missed,ensure_ascii=False,indent=2))
    report['passed']=sum(all(r[k] for k in ('native_answer_equal','native_evidence_equal','public_answer_equal','claim_evidence_equal','prior_revision_preserved'))
                         and r['unmatched_requests']==0 and r['unused_recordings']==0 for r in report['rows'])
    report['total']=len(rows)
    output.mkdir(parents=True,exist_ok=True)
    (output/'replay.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('mode','passed','total')},ensure_ascii=False))
    return 0 if report['passed']==report['total']==20 else 1


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base',type=Path,default=Path('results/module-boundary/v1'))
    parser.add_argument('--output',type=Path,default=Path('results/module-adapters/v1'))
    args=parser.parse_args();raise SystemExit(run(args.base,args.output))
