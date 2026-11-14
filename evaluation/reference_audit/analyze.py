"""Local artifact analysis. Historical replay never masquerades as new inference."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

from evaluation.reference_audit.run import digest

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'results/reference-audit/v1'


def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def history():
    rows=[]; counts={}
    for group, name in [('observed','module-boundary/v1'),('oracle','comparator-choice/oracle-v1')]:
        folder=ROOT/'results'/name
        data=json.loads((folder/'result.json').read_text())
        ratings=json.loads((folder/'ratings.json').read_text())
        calls=[json.loads(line) for line in (folder/'calls.jsonl').read_text().splitlines()]
        for row in data['rows']:
            if row.get('request',{}).get('operation')!='ask':continue
            key=row['case_id']+'/'+row['label']; answer=row['result']
            trace=[c for c in calls if c['context'].get('case_id')==row['case_id'] and c['context'].get('label')==row['label']]
            response_texts=[c['response']['choices'][0]['message']['content'] for c in trace]
            # Check recorded draft and judge responses are actual saved outputs.
            assert answer['draft_raw'] in response_texts,key
            judgments=answer.get('document_judgments',[])
            for j in judgments:assert j['raw'] in response_texts,key
            before_citation=answer.get('pre_citation_raw',answer['raw'])
            rows.append(dict(id=group+'/'+key,group=group,legacy=row['case_id'].startswith('legacy-'),
                source_job=data['job_id'],judgments=dict(Counter(j['label'] for j in judgments)),
                revised=answer['revised'],text_changed_before_citation=answer['draft_raw']!=before_citation,
                aqa_called='aqa_candidate_raw' in answer,aqa_accepted=answer.get('aqa_candidate_accepted',False),
                original_rating=ratings.get(key),trace_ids=[c['id'] for c in trace],
                initial_prompt_contains_correct_reconsideration_effect=(
                    'changes_established_facts' in json.dumps(trace[0]['request']) and
                    'reconsider' in json.dumps(trace[0]['request'])) if group=='oracle' else None,
                draft_raw=answer['draft_raw'],before_citation=before_citation,final_raw=answer['raw']))
        group_rows=[r for r in rows if r['group']==group]
        counts[group]=dict(cases=len(group_rows),judgment_calls=sum(sum(r['judgments'].values()) for r in group_rows),
            cases_with_contradiction=sum(r['judgments'].get('CONTRADICTS',0)>0 for r in group_rows),
            rewritten=sum(r['revised'] for r in group_rows),
            changed_text=sum(r['text_changed_before_citation'] for r in group_rows),
            aqa_calls=sum(r['aqa_called'] for r in group_rows),
            aqa_accepted=sum(r['aqa_accepted'] for r in group_rows),
            failed_existing_answer_rating=sum(r['original_rating'] is not None and not r['original_rating']['answer_correct'] for r in group_rows))
    result=dict(kind='Verified historical request/output analysis; zero new model calls',counts=counts,rows=rows)
    write(REPORT/'historical-stage-analysis.json',result)
    print(json.dumps(counts,indent=2))


def fresh():
    cfg=json.loads((REPORT/'runtime/config.json').read_text())
    inputs=REPORT/'runtime/inputs.json'
    data=json.loads((REPORT/'result.json').read_text())
    packets={p['id']:p for p in json.loads(inputs.read_text())['packets']}
    assert data['status']=='complete',data['status']
    assert data['input_sha256']==sha256(inputs.read_bytes()).hexdigest()
    assert data['code_sha256']==cfg['code_sha256']
    drafts={r['case_id']:r for r in data['shared_drafts']}
    assert len(drafts)==len(packets)==45 and len(data['rows'])==180
    traces=[json.loads(line) for line in (REPORT/'calls.jsonl').read_text().splitlines()]
    assert len(traces)==data['calls']
    assert {t['id'] for t in traces}==set(range(1,data['calls']+1))
    counts=Counter((r['case_id'],r['arm']) for r in data['rows'])
    assert len(counts)==180 and set(counts.values())=={1}
    cards=[]; mapping={}; cost={}
    for t in traces:
        request=t['request']; arm=t['context']['arm']; cid=t['context']['case_id']
        assert request['model']=='Qwen3-8B' and request['temperature']==0
        assert t['context']['evidence_sha256']==packets[cid]['evidence_sha256']
        entry=cost.setdefault(arm,dict(calls=0,prompt_tokens=0,completion_tokens=0,length_finishes=0))
        entry['calls']+=1
        for k in ('prompt_tokens','completion_tokens'):entry[k]+=t['response']['usage'][k]
        entry['length_finishes']+=sum(c['finish_reason']=='length' for c in t['response']['choices'])
    for r in data['rows']:
        cid=r['case_id'];p=packets[cid]
        assert 'error' not in r and r['evidence_sha256']==p['evidence_sha256']
        assert r['shared_draft_sha256']==drafts[cid]['sha256']==digest(drafts[cid]['raw'])
        assert digest(dict(witnesses=p['witnesses'],review_context=p['review_context']))==p['evidence_sha256']
        key=digest(dict(case_id=cid,arm=r['arm'],salt='reference-audit-v1-blind'))[:16]
        mapping[key]=dict(case_id=cid,arm=r['arm'])
        cards.append(dict(id=key,question=p['question'],witnesses=p['witnesses'],review_context=p['review_context'],
                          answer=r['result']['raw'],before_citation=r['before_citation']['raw']))
    write(REPORT/'verification.json',dict(complete=True,cases=45,outputs=180,calls=data['calls'],cost=cost,
        semantic_correctness_verified=False,slurm_must_be_checked_separately=True))
    write(REPORT/'blind-cards.json',sorted(cards,key=lambda x:x['id']))
    write(REPORT/'arm-map.json',mapping)
    write(REPORT/'ratings-template.json',{c['id']:dict(answer_correct=None,required_answer_source_pairs=None,
        original_citations_complete=None,state_citations_correct=None,conditions_preserved=None,
        review_semantics_correct=None,unsupported_added_claims=None,reason=None) for c in cards})
    print('Verified180 outputs; semantic/source review still required. No automatic adoption.')


if __name__=='__main__':
    {'history':history,'fresh':fresh}[sys.argv[1]]()
