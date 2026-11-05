"""Render the audited paired observations without changing the scoring decisions."""
import json
from .build import ROOT,HERE
OUT=ROOT/'results/design_review'
GROUPS=['3b/raw/direct-full','3b/raw/module','14b/raw/direct-full','14b/raw/module',
        '3b/hidden/direct-full','3b/hidden/module','3b/hidden/direct-oracle',
        '14b/hidden/direct-full','14b/hidden/module','14b/hidden/direct-oracle']
def read(name):return json.loads((OUT/name).read_text())
def esc(s):return str(s).replace('|','\\|').replace('\n',' ')

def report():
 rows=read('rows.json');counts=read('counts.json');ratings=read('ratings.json');checks=read('checks.json');runs=read('runs.json')
 keys=json.loads((HERE/'key.json').read_text())
 lines=['# 고정 사례에서의 설계 유지 판단','',
  '2026-11-05. 기존 Git 보고 15개를 고정한 진단 비교이다. 독립된 새 테스트셋 성과가 아니다. 원문 참조 유무와 양성·음성 변형을 독립 사례로 더해 표본 수를 부풀리지 않는다.',
  '', '현재 모듈을 일반 재검토 방식으로 그대로 채택하지 않는다. 출처·인용 검증과 승인 상태 분리·기존 QA는 유지하고, 일반 의미 판단은 더 강한 단순 읽기 방식을 기준으로 다시 설계한다. 명시적 원인 참조를 이용하는 경로는 별도 비교 대상으로 남긴다. [구성요소별 판단과 근거](decision.ko.md)',
  '', '## 동일 입력에서의 결과','',
  '성공은 올바른 이전 결정에 대해 실제 실패 동작·조건을 설명하고 인용으로 뒷받침한 제안이다. 잘못된 인용 형식은 정답이나 올바른 보류로 세지 않는다. raw는 원인의 커밋 참조를 포함한 원문, hidden은 그 참조를 가린 입력이다. 오탐은 실제 대상이 없는 음성 15개에서 제안한 횟수이며, 양성의 잘못된 대상·설명도 재검토 성공에서 제외한다.', '',
  '| 모델·입력·방법 | 근거 있는 재검토 /15 | 음성 오탐 /15 | 음성의 올바른 보류 /15 | 형식·실행 오류 /30 | 호출 수 | 입력 토큰 |',
  '|---|---:|---:|---:|---:|---:|---:|']
 for k in GROUPS:
  c=counts[k];lines.append(f"| {k} | {c['grounded']} | {c['false_positive']} | {c['correct_keep']} | {c['invalid']} | {c['calls']} | {c['input_tokens']:,} |")
 lines+=['','원문 전체 단순 방식은 1회 생성, 모듈은 여러 번의 선택·생성을 수행한다. 공통 상한 안에서 실제 소비량이 달라 동일 비용 비교는 아니다. 3B와 14B의 원문/정답 근거 대조 90개는 시스템·사용자 프롬프트가 바이트 단위로 동일하다. 실제 모델은 Qwen2.5-3B-Instruct와 Qwen2.5-14B-Instruct이며, 공식 SpeakerMem-R1 학습 체크포인트 재현 결과가 아니다.',
         '', '## QA와 실행 검증','',
         f"기존 회귀 검사 {checks['historical_qa_n']}개 항목 중 {checks['historical_qa_same']}개에서 실제 3B 재생성 후 원래 파서를 통과한 답·상태·인용·출처가 동일했다. 136프롬프트의 원래 배치·순서를 사용했다. 단일 답 16개, 미해결 양쪽 답 3개, 조건별 답 1개이며 EverMemBench-Dynamic 항목은 이 중 3개다. QA 전체 정확도나 개선, 14B QA 성능으로 해석하지 않는다.",
         '',f"실제 Git pull 검사: {json.dumps({k:{'same':v['same'],'pending':v['pending']} for k,v in checks['pulls'].items()},ensure_ascii=False)}.",
         '',f"이 goal의 실제 GPU 사용 {runs['gpu_seconds']} GPU초 ({runs['gpu_seconds']/60:.2f} GPU분); 다운로드 CPU 작업의 walltime 합 {runs['cpu_only_seconds']}초. 실패도 포함했다. 전체 캠페인 누적 GPU {runs['cumulative_gpu_seconds']/60:.2f}/{runs['budget']['single_gpu_minutes']} GPU분, CPU 전용 walltime 합 {runs['cumulative_cpu_only_seconds']/60:.2f}/{runs['budget']['cpu_only_minutes']}분. 주 작업 행의 빈 MaxRSS는 미측정으로 두고 batch 행 기록을 보존했다.",
         '', '7개의 형식 오류는 모두 3B의 대상·문단 ID 불일치였다. 300개 유효 비교 행에서 실행 오류와 생성 길이 상한 도달은 0개였다. [단계별 실패·대조·예산 검사](diagnostics.json) · [잘못된 원출력](invalid-outputs.json)',
         '', '## 범위와 한계','',
         '- 15개 보고 모두 과거 실험에 노출된 진단 사례다. 이번에는 평가 중 생산 모듈·추론 프롬프트·의미 기준을 수정하지 않았다.',
         '- 모델과 설계의 상호작용을 확인하기 위해 14B 모듈 비교를 추가했다. 전체 14B 원출력 회수·의미 채점 전이지만 실행 로그에서 일부 행동 라벨은 노출됐으므로 초기 계획에 포함된 비교라고 주장하지 않는다. [추가 요인 비교 기록](../../evaluation/design_review/FACTORIAL_AMENDMENT.md)',
         '- 노드마다 다른 로컬 모델 경로로 첫 14B 추론 작업이 실패했다. 검증된 공유 모델로 경로를 고치고 관측된 I/O 시간을 반영해 재시도 wall 한도를 20분에서 40분으로 변경했다. 추론 예산과 입력은 동일하다. [운영 변경](../../evaluation/design_review/RUNTIME_AMENDMENT.md)',
         '- 첫 제출 직후, 결과를 읽기 전 입력 검사로 제목만 있는 음성 기록 두 개의 빈 축약 오류를 발견했다. 그 두 oracle 입력만 별도 작업으로 교체했다. 나머지 원문·모듈 결과와 28개 oracle 입력은 유지했다. [수정 기록](../../evaluation/design_review/INPUT_CORRECTION.md)',
         '- 의미 채점은 방법 이름을 제거한 카드에 대해 한 AI 평가자가 수행했다. 형식으로 방법을 추정할 수 있어 완전한 맹검이나 독립 평가자 합의를 주장하지 않는다. 핵심 근거를 인용했어도 설명이 실제 실패·조건을 생략하면 엄격한 성공에서 제외한다. 원문을 설명에 직접 넣는 모듈의 출력도 같은 기준으로 읽었으므로 설명 형식의 영향과 경계 판정은 독립 평가가 필요하다. [판정 근거](ratings.json)',
         '- 정확한 근거 창은 Codex가 원문을 읽고 실행 전에 선정한 것으로, 사람의 독립 검증이나 실제 시스템의 자동 검색 성과가 아니다. 14B 결과도 이 모델·프롬프트·패널에 한정한다.',
         '- hidden 조건의 인용 검증 대상은 참조를 가린 입력이다. 링크된 실제 Git 원문에는 가림 기호가 없으며, 이 조건은 통제된 입력 변형이다. 단순 프롬프트의 date 필드는 null이고 earlier/incoming 역할로 선후관계를 제공했다. 이 패널은 날짜 추론 평가가 아니다.',
         '- 실제 팀의 장기 지식 공유 전체를 평가한 결과가 아니다. 원문 검증과 승인 상태 보존의 기능적 가치와 재검토 선택기의 성능을 구분한다.',
         '', '[판단과 비용 비교](decision.ko.md) · [문항별 비교](cases.ko.md) · [QA 답·인용](qa.ko.md) · [실행과 자원](runs.json) · [검증 결과](checks.json) · [프로토콜](../../evaluation/design_review/PROTOCOL.md)',
         '', '## 저장된 결과 재검증', '', '```sh',
         'python3 -m evaluation.design_review.verify',
         'python3 -m evaluation.design_review.score',
         'python3 -m evaluation.design_review.diagnostics',
         'python3 -m evaluation.design_review.report', '```', '',
         'verify는 로컬 캠페인의 회수 결과·source와 기존 QA 자료가 필요하다. 위 명령은 GPU 작업을 재제출하지 않는다. 공개용 결과 파일만으로 집계를 다시 만들려면 verify를 제외하고 나머지 세 명령을 실행한다.']
 (OUT/'README.md').write_text('\n'.join(lines)+'\n')
 lines=['# 15개 Git 보고의 문항별 판단','', '형식 오류와 무관한 결정 선택은 별도 실패로 남긴다. 성공/실패는 고정 의미 기준과 인용을 함께 판정한 결과다.','']
 for topic in sorted({r['topic'] for r in rows.values()}):
  key=next(k for k in keys.values() if k['topic']==topic and k['scenario']=='mixed' and k['view']=='raw')
  lines += [f'## {topic}','',f"[새 보고]({key['report']}) · [실제 이전 결정]({key['earlier']}) · [유사 결정]({key['alternative']})",'',key['rubric'],'',
            '| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |','|---|---|---|---|']
  for group in GROUPS:
   model,view,method=group.split('/')
   pos=next(r for r in rows.values() if (r['model'],r['view'],r['method'],r['topic'],r['scenario'])==(model,view,method,topic,'mixed'))
   neg=next(r for r in rows.values() if (r['model'],r['view'],r['method'],r['topic'],r['scenario'])==(model,view,method,topic,'no-match'))
   detail=ratings[pos['card_id']]['reason'] if pos['card_id'] else '보류' if pos['action']=='keep' else '형식 오류' if pos['action']=='invalid_output' else '대상 또는 인용 불일치'
   lines.append(f"| {group} | {pos['action']} | {'성공: ' if pos['grounded'] else '실패: '}{esc(detail)} | {neg['action']} |")
  for uid,r in rows.items():
   if r['topic']!=topic or r['scenario']!='mixed':continue
   lines += ['',f"### {r['model']}/{r['view']}/{r['method']}",'',r['result'].get('rationale',r['result'].get('basis',r['action']))]
   for part in ('previous','incoming'):
    evidence=r['result'].get(part,[])
    if isinstance(evidence,dict):evidence=[evidence]
    for w in evidence:
     lines+=['',f"{part}: [{w.get('paragraph_id','원문 구간')}]({w['location']})",'', '```text',w['quote'],'```']
 (OUT/'cases.ko.md').write_text('\n'.join(lines)+'\n')
 qa=read('qa-historical.json');lines=['# 기존 QA 답·상태·인용 보존','', '| 항목 | 질문 | 재생성 답 | 동일 |','|---|---|---|---|']
 for key,v in qa.items():
  after=v['after'];answers=after.get('answers',[after]);answer=' / '.join(str(a.get('answer','')) for a in answers)
  lines.append(f"| {esc(key)} | {esc(v['question'])} | {esc(answer)} | {v['identical']} |")
 for key,v in qa.items():
  lines+=['',f'## {key}','',v['question'],'']
  for a in v['after'].get('answers',[v['after']]):
   lines += [f"답: {a.get('answer','')} · [{a.get('speaker','source')}]({a.get('location','')})",'','```text',a.get('quote',''),'```','']
 (OUT/'qa.ko.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':report()
