"""Render frozen scorer outputs; does not define or alter scores."""
import json
from pathlib import Path

def main(folder,job):
    result=json.loads((folder/f'record-strata-{job}.json').read_text());ev=json.loads((folder/'evaluation.json').read_text())
    inputs={x['id']:x for x in json.loads(Path('evaluation/record_strata/inputs.json').read_text())['items']}
    keys={x['id']:x for x in json.loads(Path('evaluation/record_strata/keys.json').read_text())['items']}
    rows={(x['id'],x['arm']):x for x in result['rows']}
    lines=['# Records 층화 진단: 원문과 단계별 결과','',f'Job {job}. 정답과 채점기는 실행 전 고정. 원출력·부분 역할 판정이며 전체 QA 정확도가 아님.','']
    for item in inputs.values():
        key=keys[item['id']]
        lines += [f"## {item['id']} — {item['panel']} / {item['difficulty']} / {item['availability']}",'',f"Source: `{item['source']['id']}`",'',item['source']['text'],'','고정한 요구사항:','', '```json',json.dumps(key,ensure_ascii=False,indent=2),'```','']
        for arm in ('simple','ours'):
            row=rows[(item['id'],arm)];case=next(c for c in ev['cases'] if c['id']==item['id'] and c['arm']==arm)
            lines += [f'### {arm}','',f"원출력 통과: {case['raw']['passed']}; 컴파일 후 통과: {case['compiled']['passed']}; 컴파일 오류: {row['compile_error']}; 저장 전달: {case['transport']}",'','원출력:','```json',row['raw'],'```','','고정 채점:','```json',json.dumps(dict(raw=case['raw'],compiled=case['compiled']),ensure_ascii=False,indent=2),'```','']
    (folder/'cases.md').write_text('\n'.join(lines)+'\n')
    lines=['# Records 난이도 × 근거 가용성 비교','',f'실제 Qwen3-8B 작업: {job}. 상세 원문·원출력·채점은 [cases.md](cases.md), 고정 기준은 [PROTOCOL](../../../evaluation/record_strata/PROTOCOL.md).','',
      '54개 합성 입력은18개 이야기의 근거 제거 변형이다. 독립54사례나 서비스 분포를 대표하는 벤치마크가 아니다. 자연14개 메시지는5개 과거 실패 사례의 별도 부분 진단이다. 자연 n06은 모델 출력 열람 전에 라벨 오류를 발견했으며 아래14개 원점수는 감사용이다. 해석 가능한13개 집계와 사례 분석은 FINDINGS.md를 보라.','',
      '| 난이도 | 근거 가용성 | n/방식 | 단순 원출력 | 기존 원출력 | 단순 컴파일 후 | 기존 컴파일 후 |','|---|---|---:|---:|---:|---:|---:|']
    for d in ('easy','medium','hard'):
        for a in ('full','partial','none'):
            ss=[next(r for r in ev['summary'] if r['panel']=='balanced_synthetic' and r['arm']==arm and r['difficulty']==d and r['availability']==a) for arm in ('simple','ours')]
            lines += [f"|{d}|{a}|6|{ss[0]['raw_passed']}|{ss[1]['raw_passed']}|{ss[0]['compiled_passed']}|{ss[1]['compiled_passed']}|"]
    lines += ['','통과는 초점 주장·보이는 필수 역할·태도·잘못된 대상 연결·제거한 정보의 추측을 함께 검사한다. none은 문서가 비었다는 뜻이 아니라 초점의 두 조건/이유가 입력에 없다는 뜻이다.','','## 단계별 총계','','| 패널 | 방식 | n | 내용 회수(원출력) | 역할 완비(원출력) | 결합 통과(원출력) | 결합 통과(컴파일) | 컴파일 거절 | 저장/전달 실패 |','|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in ev['summary']:
        if r['difficulty']=='all':lines += [f"|{r['panel']}|{r['arm']}|{r['n']}|{r['raw_visible_recovered']}|{r['raw_typed_complete']}|{r['raw_passed']}|{r['compiled_passed']}|{r['compile_rejections']}|{r['transport_failures']}|"]
    lines += ['','## 비용','','```json',json.dumps(ev['cost'],indent=2),'```','','## 해석 한계','','- 자연 원문은 실패를 보고 고른 사례이고 정답도 초점 부분만 지정했다. 전체 추출 정밀도/재현율이나 EverMem 공식 점수가 아니다.','- 같은8B의 두 프롬프트가 모두 틀려도 모델의 본질적 능력 한계로 확정할 수 없다. 공통 출력 계약의 영향이 남는다.','- 내용 회수는 조건이 claim에 포함된 경우도 센다. 역할 완비는 뒤 모듈이 별도 조건·이유 필드로 접근 가능한지를 센다.','- 저장 전달은 새 adapter 인스턴스와 reader packet을 검사한다. 새 OS 프로세스 재시작이나 최종 QA 추론은 이번 실행 범위가 아니다.','- 생산 코드는 변경하지 않았다. 기존QA20 결과를 이번에 새로 실행한 것처럼 합산하지 않는다.']
    (folder/'README.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':
    import sys
    main(Path(sys.argv[1]),sys.argv[2])
