"""Score only complete paired predictions, against any human-approved span."""
import json
import re
import string
import sys
from collections import Counter
from pathlib import Path


def norm(s):
    s=re.sub(r'&\s*SPEAKER_\d+:',' ',s,flags=re.I).lower()
    s=s.translate(str.maketrans(dict.fromkeys(string.punctuation,' ')))
    return re.sub(r'\b(a|an|the)\b',' ',s).split()


def token_f1(a,b):
    a,b=norm(a),norm(b)
    hits=sum((Counter(a)&Counter(b)).values())
    return 2*hits/(len(a)+len(b)) if hits else 0.


def score(inputs,key,result):
    docs={i['id']:i for i in inputs}
    assert result['status']=='complete' and set(docs)==set(key)
    jobs={(r['id'],r['arm']):r for r in result['answers']}
    assert len(jobs)==len(result['answers'])==2*len(key)
    rows=[]
    for qid,g in key.items():
        row={'id':qid,'question':docs[qid]['question'],'unanswerable':g['unanswerable'],'gold':g['answers']}
        for arm in ('raw','records'):
            choice=jobs[qid,arm]['response']['choices'][0]
            p=json.loads(choice['message']['content'])
            outcome,answer,q=p['outcome'],p['answer'],p['quote']
            abstained=outcome=='abstain' and not answer.strip() and not q.strip()
            text=docs[qid]['context'];start=text.find(q) if q else -1
            unique=start>=0 and text.find(q,start+1)<0
            output=dict(prediction=p,correct_outcome=abstained if g['unanswerable'] else outcome=='answer' and bool(answer.strip()))
            if not g['unanswerable']:
                refs=g['reference_sets']
                def evidence_f1(spans):
                    gold_positions={pos for a,t in spans for pos in range(a,a+len(t))}
                    hit=sum(start<=pos<start+len(q) for pos in gold_positions) if unique else 0
                    return 2*hit/(len(q)+len(gold_positions))
                variants=[' '.join(t for _,t in spans) for spans in refs]
                output.update(answer_token_f1=max(token_f1(answer,t) for t in variants) if outcome=='answer' else 0,
                              exact_answer=outcome=='answer' and any(norm(answer)==norm(t) for t in variants),
                              exact_evidence=outcome=='answer' and unique and any(spans==[[start,q]] for spans in refs),
                              evidence_char_f1=max(evidence_f1(spans) for spans in refs) if outcome=='answer' else 0)
            row[arm]=output
        rows.append(row)
    return rows

if __name__=='__main__':
    inputs,key,result,output=map(Path,sys.argv[1:])
    import hashlib
    report=json.loads(result.read_text())
    assert report['input_sha256']==hashlib.sha256(inputs.read_bytes()).hexdigest()
    output.write_text(json.dumps(score(*[json.loads(p.read_text()) for p in (inputs,key)],report),ensure_ascii=False,indent=2))
