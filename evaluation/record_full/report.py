"""Readable gold and side-by-side error audit; does not change scores."""
import json
from pathlib import Path

def main():
    out=Path('results/record-full/v3');ev=json.loads((out/'evaluation.json').read_text());gold=json.loads(Path('evaluation/record_full/gold.json').read_text())['documents'];inputs={x['id']:x for x in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']}
    raw=json.loads(Path('results/record-strata/v1/record-strata-122970.json').read_text())['rows'];original={(r['id'],r['arm']):r for r in raw}
    g=['# 문서 전체 정답과 원문','','기존54개 합성/14개 자연 원문 유지. 원문 기반 단일 작성자 정답이며 독립 검수 전 개발용이다. 원문의 모든 의미를 자연어 일반 추론으로 판정하는 정답은 아니다.','']
    cases=['# 문서 전체 records 비교','','실제 Qwen3-8B job122970의136개 원출력을 재평가했다. 신규 추론0회. 매 사례의 원문, 전체 정답, 원출력, 누락/오추출/잘못된 연결을 함께 읽는다.','']
    for d in gold:
        item=inputs[d['id']];header=[f"## {d['id']} · {d['difficulty']} · {d['availability']}",'',f"source_id: `{d['source']['id']}`",'',item['source']['text'],'','| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |','|---|---|---|---|---|']
        for n in d['nodes']:
            text=n['text'].replace('|','\\|');ranges=', '.join(f"{s['start']}:{s['end']}" for s in n['spans']);header.append(f"|{n['id']}|{n['role']}|{text}|{ranges}|{n['required']}|")
        header += ['','연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.','']
        for r in d['records']:
            if r['unresolved']:header += [f"미해결 참조 {r['id']}: {'; '.join(r['unresolved'])}",'']
        g+=header;cases+=header
        for arm in ('simple','ours'):
            row=original[(d['id'],arm)];c=next(c for c in ev['cases'] if c['id']==d['id'] and c['arm']==arm)
            cases += [f'### {arm}','','```json',row['raw'],'```','',f"컴파일 오류: {row['compile_error']}",'']
            for stage in ('raw','compiled'):
                r=c[stage];detail={k:r[k] for k in ('complete','content_recall','claim_recall','typed_edges','missing_nodes','missing_edges','incorrect_edges','extra_rows','extra_claim_rows','overmerged_record_pairs','boilerplate_rows','stance_wrong')}
                cases += [f'**{stage}**','```json',json.dumps(detail,ensure_ascii=False,indent=2),'```','']
    (out/'gold-cases.md').write_text('\n'.join(g)+'\n');(out/'cases.md').write_text('\n'.join(cases)+'\n')
    lines=['# 난이도·가용성별 전체 records 점수','','합성54입력의9셀을 유지했다. 완전 통과는 전체 주장을 포함하며, 내용/연결/상태/출처/불필요 추출을 함께 요구한다. none도 다른 대상의 기록은 남아 있으므로 문서 전체가 비어 있는 것이 아니다.','', '| 난이도 | 가용성 | n | 단순 완전 통과 raw→compiled | 기존 완전 통과 raw→compiled | 단순 관계F1 raw→compiled | 기존 관계F1 raw→compiled |','|---|---|---:|---:|---:|---:|---:|']
    def pct(v):return '—' if v is None else f'{100*v:.1f}%'
    for diff in ('easy','medium','hard'):
        for av in ('full','partial','none'):
            rows={(r['arm'],r['stage']):r for r in ev['summary'] if r['panel']=='balanced_synthetic' and r['difficulty']==diff and r['availability']==av}
            s0,s1,o0,o1=[rows[t] for t in [('simple','raw'),('simple','compiled'),('ours','raw'),('ours','compiled')]]
            lines += [f"|{diff}|{av}|6|{s0['complete']}→{s1['complete']}|{o0['complete']}→{o1['complete']}|{pct(s0['metrics']['typed_edges']['f1'])}→{pct(s1['metrics']['typed_edges']['f1'])}|{pct(o0['metrics']['typed_edges']['f1'])}→{pct(o1['metrics']['typed_edges']['f1'])}|"]
    (out/'strata.md').write_text('\n'.join(lines)+'\n')
    print('gold-cases.md, cases.md, strata.md written')
if __name__=='__main__':main()
