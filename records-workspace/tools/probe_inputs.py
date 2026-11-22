"""형식이 제각각인 입력 6종으로 preserving.construct()를 가짜 모델과 실행한다. 레포 루트에서: python ../records-workspace/tools/probe_inputs.py"""
import json, sys
sys.path.insert(0, '.')
from team_memory.records import preserving
from team_memory.records.segments import blocks
def row(role, text, g='a', stance='unknown'):
    return {role: text, role + '_attributes': {'claim_group': g, 'stance': stance}}
def run(title, text, rows, **kw):
    src = dict(id='s', owner='o', speaker='민수', observed_at='2026-11-20T09:00:00Z', location='회의록.md', text=text)
    calls = []
    def gen(system, prompt): calls.append(prompt); return json.dumps({'extractions': rows})
    g = preserving.construct(src, gen, model='fake', **kw)['record_graph']
    q = {u['id']: u['quote'] for u in g['units']}
    print(f"\n### {title}\n blocks={len(list(blocks(text)))} calls={len(calls)} status={g['status']}")
    for c in g['claims']:
        print('  claim', {r: [q[i] for i in c[r]] for r in ('claim','condition','basis','time','subject') if c[r]})
    for d in g['diagnostics']: print('  diag', d['path'], d['reason'][:70])
    if g.get('layout'): print('  layout', [(r['kind'], r.get('label', {}) and r['label']['quote'], [c['quote'] for c in r['cells']]) for r in g['layout']])
    return calls

# A. 불릿 목록 → 블록/호출 수, 대명사
run('A. bullets', "- 배포는 금요일로 정했다\n- 그건 QA 통과 후에 한다\n- 민수: 문서 정리, 슬라이드 수정\n",
    [row('claim','배포는 금요일로 정했다','a','decision')])
# B. 한국어 정렬 (명세 A 사례)
run('B. korean', "dataset v1에서는 Petr가 초안을 승인했다.",
    [row('claim','Petr가 초안을 승인했다','a','decision'), row('condition','dataset v1에서는'), row('subject','초안')])
# C. 줄바꿈 중간 문장, 모델이 줄을 합쳐서 반환
run('C. line-wrapped', "Petr approved\nthe draft yesterday.",
    [row('claim','Petr approved the draft','a','decision'), row('time','yesterday')])
# D. 문맥 구절 반복 (흔한 단어)
run('D. repeated context', "If QA passes, ship v2. QA owns the checklist.",
    [row('condition','QA passes'), row('claim','ship v2','a','decision'), row('claim','QA owns the checklist','b','observation'), row('subject','QA','b')])
# E. 한 행만 살짝 바꿔 쓴 경우 (기본 isolate_invalid=False)
run('E. one paraphrased row (default)', "Ship v2 on Friday because tests passed. Mina will update the docs.",
    [row('claim','Ship v2','a','decision'), row('time','on Friday'), row('basis','the tests passed'),
     row('claim','Mina will update the docs','b','proposal')])
# F. 같은 주장 문장이 두 번
run('F. duplicated claim text', "Ship it. Later Mina said: ship it.",
    [row('claim','ship it','a','decision')])
