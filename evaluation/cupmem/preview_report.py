"""A self-contained viewer of actual inference, including failures and raw output."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build(fresh=None):
    from evaluation.timeline.score import grade_qa
    groups = []
    inputs = json.loads((ROOT/'evaluation/timeline/final.json').read_text())
    records = json.loads((ROOT/'results/timeline/final-generations.json').read_text())
    scores = json.loads((ROOT/'results/timeline/final/rows.json').read_text())
    groups.append(dict(id='previous', label='기존 14B 실행 · 20개 흐름', model='Qwen2.5-14B-Instruct',
        note='이미 측정된 응답 재생. 자연 대화 QA + 합성 팀 기록. 새 추론이 아닙니다.',
        cases=inputs, records=records['streams'], scores=scores))
    if fresh:
        result = json.loads(fresh.read_text())
        assert result['status']=='complete', 'Never present partial inference as a completed preview'
        inputs_path=ROOT.parent/'campaigns/speakermem-dev/source/cup-fast-preview-v1/inputs.json'
        assert sha256(inputs_path.read_bytes()).hexdigest()==result['input_sha256']
        inputs=json.loads(inputs_path.read_text())
        keys=json.loads((ROOT/'evaluation/timeline/development-key.json').read_text())
        scores={}
        for uid, record in result['streams'].items():
            key=keys[record['id']]
            qa={s['id']:grade_qa(s['result'],key['qa'][s['id']])
                for s in record['steps'] if s['op']=='ask'}
            scores[uid]=dict(type=key['kind'],qa=qa,qa_correct=sum(q['correct'] for q in qa.values()),qa_total=len(qa))
        groups.insert(0,dict(id='fresh',label='새 8B 실행 · 3개 개발 흐름',model=result['model'],
            note=f"새 실제 추론 · Slurm {result['job_id']} · 합성 개발 사례, 성능 입증용 평가가 아닙니다. 작성자 승인은 모의 동작입니다.",
            cases=inputs,records=result['streams'],scores=scores))
    for group in groups:
        for record in group['records'].values():
            cursor=0
            record['step_calls']=[]
            for step in record['steps']:
                r=step['result']
                n=(1 if step['op']=='ask' else
                   (int(record['mode']=='indexed')+int(bool(r['history'])))
                   if step['op']=='ingest' and not r.get('replayed') else 0)
                record['step_calls'].append(record['calls'][cursor:cursor+n])
                cursor+=n
            assert cursor==len(record['calls']), (record['id'], 'call mapping mismatch')
    data=json.dumps(groups,ensure_ascii=False).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    out=ROOT/'results/preview';out.mkdir(exist_ok=True)
    (out/'index.html').write_text(HTML.replace('__DATA__',data))
    (out/'summary.json').write_text(json.dumps({g['id']:dict(model=g['model'],note=g['note'],
        cases=len(g['cases']),scores=g['scores']) for g in groups},ensure_ascii=False,indent=2)+'\n')
    print(out/'index.html')


HTML=r'''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Team Memory · 실제 실행 보기</title>
<style>
:root{font-family:system-ui,-apple-system,sans-serif;color:#182a32;background:#f3f5f3;font-size:15px}*{box-sizing:border-box}body{margin:0}header{padding:34px max(24px,5vw) 24px;background:#133c3b;color:#fff}header small{letter-spacing:2px;color:#b8dbd1}h1{font-size:32px;margin:12px 0}header p{color:#d3e4dd;max-width:900px;line-height:1.7}main{max-width:1450px;margin:auto;padding:24px}select,button{font:inherit;border:1px solid #bbc9c3;border-radius:7px;background:white;padding:10px;color:#163b34}button{cursor:pointer}button:disabled{opacity:.4;cursor:default}.controls{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}.note{color:#51645c;line-height:1.6}.grid{display:grid;grid-template-columns:270px 1fr 1fr;gap:18px;margin-top:20px}.panel{background:white;border:1px solid #dce5df;border-radius:12px;padding:20px;min-width:0}h2{font-size:18px;margin:0 0 16px}h3{font-size:16px;margin:18px 0 9px}p{line-height:1.65}.event{display:block;width:100%;text-align:left;margin-bottom:8px;border-color:#e1e8e3;font-size:13px}.event.active{background:#dcefe6;border-color:#54957a}.badge{font-size:12px;border-radius:5px;background:#e8eee9;padding:4px 7px;display:inline-block;margin:3px}.bad{background:#fce3df;color:#8e3426}.good{background:#d9efdf;color:#226942}.source,.answer,.relation{border-top:1px solid #e3eae5;padding:14px 0;overflow-wrap:anywhere}.meta{font-size:12px;color:#64776c}blockquote{margin:10px 0;padding:10px 14px;border-left:3px solid #75a18c;background:#f6f8f5;line-height:1.6;white-space:pre-wrap}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;line-height:1.6;background:#f6f7f5;padding:12px;max-height:440px;overflow:auto}details{margin-top:14px}summary{cursor:pointer;color:#286551}a{color:#226b52}footer{padding:22px;color:#617466;text-align:center;font-size:12px}@media(max-width:1050px){.grid{grid-template-columns:220px 1fr}.result-panel{grid-column:2}}@media(max-width:700px){.grid{display:block}.panel{margin-bottom:14px}h1{font-size:25px}.controls select{width:100%}}
</style>
<header><small>TEAM MEMORY / RESEARCH PROTOTYPE</small><h1>기록이 들어온 뒤, AI는 무엇을 바꿨을까?</h1>
<p>원문 → 재검토 제안 → 작성자 검토 → 근거 있는 답변. 단계별 실제 모델 출력과 검증 결과를 함께 확인합니다. 자동 판단의 오류도 그대로 표시합니다.</p></header>
<main><div class="controls"><select id="group" aria-label="실행 선택"></select><select id="case" aria-label="사례 선택"></select><select id="mode" aria-label="방식 선택"><option value="direct">direct · 원문 읽기</option><option value="indexed">indexed · 색인 추가</option></select><button id="prev">← 이전</button><button id="next">다음 →</button></div>
<div id="note" class="note"></div><div id="metrics"></div><div class="grid"><nav class="panel"><h2>시간순 진행</h2><div id="events"></div></nav><section class="panel"><h2>이 시점까지의 원문</h2><div id="sources"></div></section><section class="panel result-panel"><h2 id="result-title">실제 처리 결과</h2><div id="result"></div><details><summary>정확한 모델 입력 · 원출력</summary><div id="raw"></div></details></section></div></main>
<footer>저장된 실행을 살펴보는 화면입니다. 새 질문을 보내거나 원작성자의 승인을 생성하지 않습니다. 과거 평가의 코드·점수는 변경하지 않았습니다.</footer>
<script type="application/json" id="data">__DATA__</script><script>
const DATA=JSON.parse(document.getElementById('data').textContent);let pos=0;
const $=id=>document.getElementById(id),kind={reconsider:'과거 결정 재검토',coexist:'다른 조건의 공존',conflict:'같은 조건의 충돌',correction:'명시적 정정',irrelevant:'무관한 새 보고'};
function el(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e}
function badge(parent,text,cls=''){parent.append(el('span',text,'badge '+cls))}
function section(parent,title,text){parent.append(el('h3',title),el('p',text))}
function obj(parent,value){parent.append(el('pre',JSON.stringify(value,null,2)))}
function current(){const g=DATA[+$('group').value];const row=g.cases.find(x=>x.id===$('case').value);const mode=$('mode').value;return {g,row,rec:g.records[row.id+'/'+mode],score:g.scores[row.id+'/'+mode]}}
function groups(){DATA.forEach((g,i)=>{let o=el('option',g.label);o.value=i;$('group').append(o)});cases()}
function cases(){const g=DATA[+$('group').value];$('case').replaceChildren();for(const r of g.cases){let s=g.scores[r.id+'/direct'];let o=el('option',r.id+' · '+(kind[s.type]||s.type));o.value=r.id;$('case').append(o)}$('mode').options[1].disabled=g.id==='fresh';if(g.id==='fresh')$('mode').value='direct';pos=0;render()}
function render(){const {g,row,rec,score}=current();pos=Math.min(pos,row.steps.length-1);$('note').textContent=g.model+' — '+g.note;$('metrics').replaceChildren();badge($('metrics'),'흐름 전체 QA '+score.qa_correct+'/'+score.qa_total);badge($('metrics'),'실제 호출 '+rec.calls.length+'회');badge($('metrics'),'입력 '+rec.input_tokens.toLocaleString()+' 토큰');badge($('metrics'),'호출 경과 '+rec.seconds.toFixed(1)+'초');badge($('metrics'),'승인은 모의 사용자 동작');
 $('events').replaceChildren();row.steps.forEach((s,i)=>{const label=s.op==='ingest'?'원문 도착':s.op==='review'?'작성자 검토 (모의)':'QA · '+s.id;const b=el('button',(i+1)+'. '+label,'event'+(i===pos?' active':''));b.onclick=()=>{pos=i;render()};$('events').append(b)});$('prev').disabled=pos===0;$('next').disabled=pos===row.steps.length-1;
 $('sources').replaceChildren();for(const s of row.steps.slice(0,pos+1)){if(s.op!=='ingest')continue;const d=el('div',undefined,'source');d.append(el('b',s.source.owner),el('div',s.source.source.location,'meta'),el('blockquote',s.source.source.text));$('sources').append(d)}
 const spec=row.steps[pos],step=rec.steps[pos],result=step.result;const p=$('result');p.replaceChildren();$('raw').replaceChildren();$('result-title').textContent=spec.op==='ask'?'질문과 실제 답':spec.op==='review'?'작성자 검토 결과':'새 기록에 대한 제안';
 if(spec.op==='ask'){p.append(el('h3',spec.question));const grade=score.qa[spec.id];if(grade)badge(p,grade.correct?'고정 기준 통과':'고정 기준 실패: '+grade.errors.join(', '),grade.correct?'good':'bad');badge(p,result.kind);if(result.error)section(p,'검증 오류',result.error);for(const a of result.answers){const d=el('div',undefined,'answer');d.append(el('b',a.answer));badge(d,a.status);d.append(el('blockquote',a.quote),el('div',a.location,'meta'));if(a.condition)d.append(el('p','조건: '+a.condition.quote));p.append(d)}if(!result.answers.length)p.append(el('p','최종 전달된 답이 없습니다. 원출력에서 원인을 확인할 수 있습니다.'))}
 else if(spec.op==='ingest'){const relations=result.relations||[];p.append(el('p',relations.length?'생성된 제안 '+relations.length+'개':'생성된 제안이 없습니다.'));for(const r of relations){const d=el('div',undefined,'relation');badge(d,kind[r.kind]||r.kind);badge(d,r.status);section(d,'판단 이유',r.reason);d.append(el('h3','과거 근거'),el('blockquote',r.previous.quote),el('h3','새 근거'),el('blockquote',r.incoming.quote));p.append(d)}for(const e of result.errors||[])p.append(el('p',typeof e==='string'?e:JSON.stringify(e),'bad'))}
 else{p.append(el('p','고정된 모의 검토 시나리오와 일치한 제안: '+result.matched+'개. 실제 GitHub 사용자의 승인이 아닙니다.'));obj(p,result)}
 const call=rec.step_calls[pos];if(call.length){for(const c of call){$('raw').append(el('h3','시스템 지시'),el('pre',c.system),el('h3','실제 입력'),el('pre',c.content),el('h3','수정하지 않은 원출력'),el('pre',c.raw))}}else $('raw').append(el('p','이 단계에는 모델 호출이 없습니다.'));
}
$('group').onchange=cases;$('case').onchange=()=>{pos=0;render()};$('mode').onchange=()=>{pos=0;render()};$('prev').onclick=()=>{pos--;render()};$('next').onclick=()=>{pos++;render()};groups();
</script></html>'''

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--fresh',type=Path)
    args=p.parse_args();build(args.fresh)
