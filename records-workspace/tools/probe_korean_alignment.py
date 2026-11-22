"""한국어 구절별 정렬 성공/실패 확인. 레포 루트에서: python ../records-workspace/tools/probe_korean_alignment.py"""
import sys
sys.path.insert(0, '.')
from team_memory.records.preserving import _aligned_span
def row(role, text, stance='unknown'):
    return {role: text, role + '_attributes': {'claim_group': 'a', 'stance': stance}}
text = "dataset v1에서는 Petr가 초안을 승인했다. 회의는 오늘 3시에 열린다."
src = dict(id='s', text=text)
for r in [row('claim','Petr가 초안을 승인했다','decision'), row('condition','dataset v1에서는'), row('subject','초안'),
          row('claim','승인했다','decision'), row('claim','회의는 오늘 3시에 열린다','observation'), row('time','오늘 3시에'),
          row('claim','Petr','decision'), row('claim','dataset v1','decision')]:
    try: s = _aligned_span(src, r); print('OK  ', repr(text[s['start']:s['end']]), '<-', list(r.values())[0])
    except Exception as e: print('FAIL', list(r.values())[0], '|', e)
from langextract.core import tokenizer
print([text[t.char_interval.start_pos:t.char_interval.end_pos] for t in tokenizer.tokenize(text).tokens][:14])
