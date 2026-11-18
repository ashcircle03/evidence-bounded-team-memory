"""Create blind scorecards from the completed reader responses and summarize signed ratings."""
import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

from evaluation.team_record_pilot.pilot import SOURCES,rows


def blind(questions, outputs, directory):
    qs={r['qid']:r for r in rows(questions)}
    answers=json.loads(Path(outputs).read_text())
    expected={(q,a) for q in qs for a in ('raw','automatic','human')}
    if not expected or {(a['qid'],a['arm']) for a in answers}!=expected or len(answers)!=len(expected):
        raise ValueError('Missing or duplicate reader responses')
    random.SystemRandom().shuffle(answers)
    dest=Path(directory);dest.mkdir(exist_ok=False)
    key=[]
    with (dest/'scorecard.csv').open('w',newline='') as stream:
        w=csv.writer(stream);w.writerow(['code','qid','thread','question','response','answer_ok','citations_ok','outcome_ok','reason'])
        for i,a in enumerate(answers,1):
            q=qs[a['qid']];code=f'B{i:03}'
            key.append(dict(code=code,qid=q['qid'],thread=q['thread'],arm=a['arm']))
            w.writerow([code,q['qid'],q['thread'],q['question'],a['response']['choices'][0]['message']['content'],'','','',''])
    (dest/'coordinator-only-key.json').write_text(json.dumps(key))


def summarize(key_path,ratings):
    key={r['code']:r for r in json.loads(Path(key_path).read_text())}
    data=rows(ratings)
    if {r['code'] for r in data}!=set(key) or len(data)!=len(key):raise ValueError('Incomplete grades')
    byq=defaultdict(dict)
    for r in data:
        k=key[r['code']]
        if r['qid']!=k['qid'] or r['thread']!=k['thread'] or not r['reason'].strip():raise ValueError(r['code'])
        scores=[r[x] for x in ('answer_ok','citations_ok','outcome_ok')]
        if not set(scores)<={'0','1','NA'}:raise ValueError(scores)
        byq[(r['thread'],r['qid'])][k['arm']]=scores
    for (thread,qid),scores in sorted(byq.items()):
        print(json.dumps(dict(thread=thread,qid=qid,arms=scores)))
if __name__=='__main__':
    {'blind':blind,'summarize':summarize}[sys.argv[1]](*sys.argv[2:])
