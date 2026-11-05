"""Create the per-case explanation and QA audit from the scored current run."""
from .verify import HERE,OUT
from evaluation.decision_records.build import read,save


def flat(text):return ' '.join(text.split())

def render():
    key=read(HERE/'key.json');data=read(OUT/'cases.json');raw=read(OUT/'comparison.json')
    costs={}
    lines=['# 새 Git 보고의 근거와 최종 판단','', '단순 검색, 직전 참조 방식, 역할 검증 방식, 문맥 확장 방식의 최종 출력을 같은 보고에서 비교했다.']
    for cid,k in key.items():
        if (k['scenario'],k['view'])!=('mixed','raw'):continue
        lines+=['','## '+k['topic'],'',f"[과거 결정]({k['earlier']}) · [새 보고]({k['report']}) · [주제가 비슷한 대조 결정]({k['alternative']})",'',k['rubric']]
        for method in ('simple','referenced-review','role-review','context-review'):
            v=data[cid+'/'+method];r=v['result'];calls=raw['results'][cid][method]['used']
            costs[cid+'/'+method]=dict(calls=len(calls),input_characters=sum(len(raw['calls'][c]['system'])+len(raw['calls'][c]['content']) for c in calls))
            lines+=['','### '+method,'',f"{r['action']} · 올바른 대상 {v['target']} · 근거 쌍 {v['pair']} · 조건과 동작 {v['grounded']} · 대조 결정 구별 {v['contrast']}"]
            if r.get('basis'):lines+=['',r['basis']]
            for field in ('previous','report_anchor','incoming','alternative'):
                if field in r:lines+=['',field+' · '+str([r[field]['start'],r[field]['end']]),'',r[field]['quote']]
            for field in ('rationale','distinction'):
                if field in r:lines+=['',field,'',r[field]]
    (OUT/'cases.ko.md').write_text('\n'.join(lines)+'\n');save(OUT/'inference-costs.json',costs)
    lines=['# 기존 QA 및 실제 pull에서의 답·인용 비교','']
    for uid,r in read(OUT/'qa-historical.json').items():
        lines+=['','## '+uid,'',r['question'],'',f"원래 답·상태·출처·인용문과 일치 · {r['identical']}"]
        for a in r['after'].get('answers',[r['after']]):
            lines+=['','- '+a.get('answer',a.get('status',''))+' · '+a.get('location',''),'  > '+flat(a.get('quote',''))]
    for cid,r in raw['qa'].items():
        lines+=['','## 실제 pull · '+key[cid]['topic'],'',r['question']]
        for label,a in zip(('원문 복제본','pull 복제본'),r['answers']):
            lines+=['',label+' · '+a['out'].get('status','')]
            for ans in a['out'].get('answers',[]):
                lines+=['','- '+ans['answer']+' · '+ans['location'],'  > '+flat(ans['quote'])]
        lines+=['','관련 재검토 제안 상태 · '+', '.join(p['status'] for p in r['context'])]
    (OUT/'qa.ko.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':render()
