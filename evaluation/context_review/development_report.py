"""Compare all diagnostic attempts and expose what text was actually supplied."""
from .verify import HERE,OUT
from evaluation.decision_records.build import read,save
from team_memory.context_review import valid_evidence


def run():
    keys=read(HERE/'dev-key.json');data=read(OUT/'development-v3.json')['results']
    scores={};lines=['# 문맥 확장 개발 결과','','단위는 원문 보고 두 개다. 순서 반전은 같은 사례의 반복 관측이다. 최종판은 같은 문서의 구절을 원래 순서로 정렬한다. 따라서 앞뒤 문단 순서를 뒤집어도 동일해지는 부분은 구현상의 성질이다.','']
    for cid,row in data.items():
        k=keys[cid];r=row['result']['revised'];opened=r['action'] in ('reassess','retest')
        if opened:assert valid_evidence(r)
        success=k['topic']=='fsck-empty' and k['variant']=='neighbors2'
        reason=('빈 파일 조건과 실제 failed to read / Invalid argument 메시지를 함께 인용했다.' if success else
                '오류 메시지를 찾았지만 빈 파일 조건까지 포함하지 않았다.' if opened and k['topic']=='fsck-empty' else
                '권한 오류 시 재시도하라는 수리 방법과 회귀 귀속을 골랐다. 작은 버퍼의 EACCES와 큰 버퍼의 성공을 설명하는 원문을 선택하지 못했다.' if opened else '실패 동작과 조건을 함께 뒷받침할 구절을 선택하지 못해 보류했다.')
        scores[cid]=dict(topic=k['topic'],variant=k['variant'],reverse=k['reverse'],opened=opened,success=success,reason=reason)
        if k['reverse']:continue
        lines += ['','## '+k['topic']+' · '+k['variant'],'',f"{r['action']} · 근거 있는 복구 {success}",'',reason]
        for p in next(x for x in read(HERE/'dev-inputs.json') if x['id']==cid)['passages']:
            lines+=['','입력 구절 · '+p['location']+' · '+str([p['start'],p['end']]),'',p['quote']]
        if opened:lines+=['','최종 선택 구절','',r['incoming']['quote']]
    save(OUT/'development-scores.json',scores)
    (OUT/'development.ko.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':run()
