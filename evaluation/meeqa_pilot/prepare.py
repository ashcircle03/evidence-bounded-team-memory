"""Pin a small meeting-disjoint, answerability-balanced MeeQA validation panel."""
import csv
import hashlib
import json
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def prepare(archive, meeting_list, destination):
    with zipfile.ZipFile(archive) as z:
        data = json.loads(z.read('validation_data.json'))['data']
    with open(meeting_list) as stream:
        names = sorted((r['meeting_name'] for r in csv.DictReader(stream)), key=len, reverse=True)
    groups = defaultdict(list)
    for row in data:
        groups[row['id'].rsplit('_',1)[0]].append(row)
    eligible = []
    for qid, rows in groups.items():
        q = rows[0]
        meeting = next((n for n in names if qid.startswith(n)),None)
        if not meeting or len({r['id'] for r in rows})<2 or len({r['is_impossible'] for r in rows})!=1:
            continue
        if not all(r[k] for r in rows for k in ('isQuestionComprehensible','isQuestionRelavent','isQuestionSelfContained')):
            continue
        if not all((r['question'],r['context'])==(q['question'],q['context']) for r in rows):continue
        refs = set()
        for r in rows:
            for start,answer in zip(r['answers']['answer_start'],r['answers']['text']):
                if start>=0 and answer:
                    if q['context'][start:start+len(answer)]!=answer:break
                    refs.add((start,answer))
                elif not q['is_impossible']:break
            else:continue
            break
        else:
            if bool(refs)!=q['is_impossible']:
                eligible.append((sha(('v021-meeqa-1/'+qid).encode()),meeting,qid,q,sorted(refs),rows))
    used=set();counts={True:0,False:0};inputs=[];key={}
    for _,meeting,qid,q,refs,votes in sorted(eligible):
        flag=q['is_impossible']
        if meeting in used or counts[flag]>=4:continue
        used.add(meeting);counts[flag]+=1
        inputs.append(dict(id=qid,meeting=meeting,question=q['question'],context=q['context']))
        key[qid]=dict(unanswerable=flag,annotators=len(votes),answers=refs,
                      reference_sets=[[(a,t) for a,t in zip(v['answers']['answer_start'],v['answers']['text']) if a>=0 and t] for v in votes])
    assert counts=={True:4,False:4}
    dest=Path(destination);dest.mkdir(exist_ok=True,parents=True)
    for name,obj in [('inputs',inputs),('key',key)]:
        (dest/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    (dest/'manifest.json').write_text(json.dumps(dict(revision='7b9a6c43eef4e0830336862ffc19b48ff52615a6',
        archive_sha256=sha(Path(archive).read_bytes()),meeting_list_sha256=sha(Path(meeting_list).read_bytes()),
        input_sha256=sha((dest/'inputs.json').read_bytes()),key_sha256=sha((dest/'key.json').read_bytes()),
        ids=[i['id'] for i in inputs],eligible=len(eligible)),indent=2)+'\n')

if __name__=='__main__':prepare(*sys.argv[1:])
