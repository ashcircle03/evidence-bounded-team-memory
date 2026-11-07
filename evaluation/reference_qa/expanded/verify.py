"""Verify physical inputs and output binding; export separate semantic ratings.

No automatic semantic judge or inferred approval/merge labels.
"""
from collections import Counter
from hashlib import sha256
import json,sys
from pathlib import Path
from types import SimpleNamespace


def main():
    from team_memory.reference_joint import joint_template,format_joint
    from team_memory.reference_claims import answer_from_sources
    root=Path(__file__).resolve().parents[3];folder=Path(sys.argv[1])
    read=lambda p:json.loads(p.read_text())
    def write(n,x):(folder/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    cfg=read(folder/'config.json');freeze=read(folder/'freeze.json');result=read(folder/'result.json');keys=read(folder/'keys.json')
    assert result['status']=='complete' and len(result['rows'])==cfg['expected_output_rows']
    assert result['code_sha256']==cfg['code_sha256'] and result['data_sha256']==cfg['data_sha256']
    for n,h in {**cfg['code_sha256'],**freeze['evaluation_sha256'],**freeze['prior_sha256']}.items():assert sha256((root/n).read_bytes()).hexdigest()==h,n
    calls=[json.loads(l) for l in (folder/'calls.jsonl').read_text().splitlines()]
    assert len(calls)==result['calls']<=cfg['max_calls']
    assert [c['id'] for c in calls]==list(range(len(calls)))
    assert all(c['http_status']==200 and c['rendered_prompt_tokens']+c['request']['max_tokens']<=32768 for c in calls)
    oldkeys=read(root/'evaluation/cupmem/practical/legacy-key.json')['cases'];transferkeys=read(root/'evaluation/reference_qa/simplify/key.json')['cases']
    cards={};blind={};mapping={};rating_template={};groups={}
    for row in result['rows']:
        identity={k:row[k] for k in ['split','case_id','arm']};cid='/'.join(identity.values());assert cid not in cards
        actual=[c for c in calls if c['context']==identity];assert len(actual)==row['calls']
        q=row['question'];witnesses=row['retrieval_sources'];output=row['result']
        if row['arm']=='claims':
            consumed=[]
            class Replay:
                def chat(self,messages):
                    c=actual[len(consumed)];body=[dict(role=m.role.value,content=m.content) for m in messages]
                    assert body==c['request']['messages'],cid
                    consumed.append(c['id']);return SimpleNamespace(message=SimpleNamespace(content=c['response']['choices'][0]['message']['content']))
            rebuilt=answer_from_sources(q,witnesses,Replay());assert len(consumed)==len(actual)
        else:
            assert len(actual)==1
            ctx='\n\n'.join(f"Source {i}:\nrecord_author: {w['speaker']}\nrecorded_at: {w.get('observed_at','unknown')}\n{w['quote']}" for i,w in enumerate(witnesses,1))
            assert actual[0]['request']['messages']==[dict(role='user',content=joint_template().format(context_str=ctx,query_str=q))]
            rebuilt=format_joint(q,actual[0]['response']['choices'][0]['message']['content'],witnesses)
        assert rebuilt==output,cid
        def valid(w):
            return any(p['source_id']==w['source_id'] and w['start']>=p['start'] and w['end']<=p['end'] and
                p['quote'][w['start']-p['start']:w['end']-p['start']]==w['quote'] for p in witnesses)
        selected=[w for a in output['answers'] for w in a['evidence']]
        spans=[w for c in output['claims'] for w in c.get('quoted_spans',c.get('evidence',[]))]
        assert all(valid(w) for w in selected+spans),cid
        # Selected quotes must be in an actual evidence-bearing prompt, not only
        # in the model's answer. First prompt contains the retrieved records.
        assert all(w['quote'] in actual[0]['request']['messages'][0]['content'] for w in selected+spans)
        if row['split']=='legacy':
            parent,label=row['case_id'].rsplit('/',1);gold=oldkeys[parent]['questions'][label]
        elif row['split']=='transfer':gold=transferkeys[row['case_id']]
        elif row['split']=='order':gold=transferkeys['new-conflict-one-source']
        else:gold=keys['keys'][row['case_id'].split('/')[0]]
        bid=sha256(('blinded-claims-v1:'+cid).encode()).hexdigest()[:12];mapping[bid]=cid
        claims=[dict(text=c['text'],returned_evidence=a['evidence'],located_quotes=c.get('quoted_spans',c.get('evidence',[]))) for c,a in zip(output['claims'],output['answers'])]
        blind[bid]=dict(question=q,condition=row['case_id'].split('/')[-1] if row['split']=='wiki' else None,
            answer=output['raw'],claims=claims,available_sources=witnesses,reference=gold)
        rating_template[bid]=dict(answer_correct=None,returned_evidence_supports_all_claims=None,required_evidence_complete=None,
            narrow_quotes_support_all_claims=None,unsupported_extra=None,reason='',claim_reviews=[])
        cards[cid]=dict(**row,blind_id=bid)
        group=row['split']+'/'+row['arm'];groups.setdefault(group,[]).append(row)
    for split in ['order','ever','wiki']:
        ids={r['case_id'] for r in result['rows'] if r['split']==split}
        for cid in ids:
            rows=[r for r in result['rows'] if r['split']==split and r['case_id']==cid]
            assert len(rows)==2 and rows[0]['retrieval_sources']==rows[1]['retrieval_sources']
    metrics={}
    for group,rows in groups.items():
        traces=[c for c in calls if c['context']['split']+'/'+c['context']['arm']==group]
        metrics[group]=dict(outputs=len(rows),calls=len(traces),seconds=sum(r['seconds'] for r in rows),
            input_tokens=sum(c['response']['usage']['prompt_tokens'] for c in traces),output_tokens=sum(c['response']['usage']['completion_tokens'] for c in traces),
            statuses=dict(Counter(r['result']['status'] for r in rows)))
    retrieval=[]
    for r in keys['retrieval']:
        gold=set(r['gold_reference_locations']);found=set(r['retrieved_locations'])
        retrieval.append(dict(id=r['id'],matched=len(gold&found),total=len(gold),recall=len(gold&found)/len(gold) if gold else None))
    verification=dict(physical_calls=len(calls),output_records=len(cards),all_actual_prompts_replayed=True,all_returned_quotes_bound_to_input=True,
        paired_witnesses_equal=True,code_inputs_and_prior_results_unchanged=True,
        truncated_outputs=sum(c['response']['choices'][0]['finish_reason']=='length' for c in calls),
        metrics=metrics,ever_reference_location_recall=retrieval,semantic_evaluation='Separate ratings required')
    write('cards.json',cards);write('blind-cards.json',dict(sorted(blind.items())));write('blind-mapping.json',mapping);write('verification.json',verification)
    if not (folder/'ratings.json').exists():write('ratings-template.json',dict(reviewer='',independent_human=False,ratings=rating_template))
    print(json.dumps(verification,indent=2))


if __name__=='__main__':main()
