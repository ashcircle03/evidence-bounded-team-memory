"""Build using pinned GitBugs Thunderbird + QMSum ALL/test and a Bugzilla audit."""
import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN = re.compile(r'\w+', re.UNICODE)
ISSUE_HINT = re.compile(r'https?://|www\.|\b(?:bug|issue|ticket)\s*[:#-]?\s*\d+|#\s*\d{3,}|\b\d{6,8}\b|\b(?:dupe|duplicate)\s+(?:of|bug|ticket|issue|#)|\b[\w.+-]+@[\w.-]+\.\w+', re.I)
ANNOTATION = re.compile(r'relevant_text_span|specific_query_list|answer\s*[:=]|(?:turn|utterance)\s*#?\d+\s*(?:to|[-–])\s*\d+', re.I)


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def norm(text):
    return ' '.join(TOKEN.findall(text.casefold()))


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def prepare(raw):
    issues = {r['Issue id']: r for r in read_csv(raw/'bugs.csv')}
    links = defaultdict(set)
    for row in read_csv(raw/'pairs.csv'):
        links[row['Issue id']].update(re.findall(r'\d+', row['Duplicate id']))
    audit = Counter()
    # Sample one pool before looking at retrieval output. Add fixed background negatives/unjudged records.
    safe = {i for i,r in issues.items() if len(norm(r['Summary']).split()) >= 4 and not ISSUE_HINT.search(r['Summary'])}
    candidates = []
    for i, targets in links.items():
        if i not in safe or not targets <= safe:
            audit['missing_or_filtered_title'] += 1
        elif any(datetime.fromisoformat(issues[t]['Created']) >= datetime.fromisoformat(issues[i]['Created']) for t in targets):
            audit['target_not_strictly_earlier'] += 1
        elif any(norm(issues[t]['Summary']) == norm(issues[i]['Summary']) for t in targets):
            audit['verbatim_pair'] += 1
        else:
            candidates.append(i)
    candidates = sorted(candidates, key=digest)[:600]
    background = sorted(safe, key=lambda i:digest('background'+i))[:650]
    ids = set(background) | set(candidates) | {t for i in candidates for t in links[i]}
    return issues, links, candidates, ids, audit


def bugs(raw):
    issues, links, proposed, ids, counts = prepare(raw)
    attest = json.loads((raw/'audit.json').read_text())
    usable = {i for i in ids if attest.get(i) == 'unchanged'}
    counts['issues_unverified_or_title_changed'] = len(ids - usable)
    def sid(i): return 'b-'+digest('tb:'+i)
    docs = {i:dict(id=sid(i), text=issues[i]['Summary'].strip(), created=issues[i]['Created']) for i in usable}
    cases, labels = [], []
    seen = set()
    for i in proposed:
        if i not in usable or not links[i] <= usable:
            counts['pair_failed_history_check'] += 1
            continue
        cutoff = datetime.fromisoformat(docs[i]['created'])
        past = [j for j,d in docs.items() if datetime.fromisoformat(d['created']) < cutoff]
        if len(past) < 100 or any(norm(docs[j]['text']) == norm(docs[i]['text']) for j in past):
            counts['small_pool_or_title_copy'] += 1
            continue
        if norm(docs[i]['text']) in seen:
            counts['repeated_query'] += 1
            continue
        seen.add(norm(docs[i]['text']))
        cid = 'f02-'+digest(i)
        cases.append(dict(id=cid,task='F02',pool='thunderbird',query=docs[i]['text'],before=docs[i]['created']))
        labels.append(dict(id=cid,groups=[[sid(t)] for t in sorted(links[i])],upstream_id=i))
    return sorted(docs.values(),key=lambda d:d['id']), cases, labels, counts


def meetings(raw):
    pools, cases, labels, counts = {}, [], [], Counter()
    seen = set()
    for lineno,line in enumerate((raw/'meetings.jsonl').read_text().splitlines(),1):
        m = json.loads(line)
        mid = 'meeting-'+str(lineno)
        turns = m['meeting_transcripts']
        docs = [dict(id=f'{mid}-{n}', text=t['speaker']+' — '+t['content']) for n,t in enumerate(turns)]
        pools[mid] = docs
        for n,row in enumerate(m['specific_query_list']):
            q, a = row['query'].strip(), norm(row['answer'])
            if not q or not a or norm(q) in seen or ANNOTATION.search(q) or a in norm(q):
                counts['empty_repeated_or_answer_hint'] += 1
                continue
            groups = []
            for s,e in row.get('relevant_text_span',[]):
                if not str(s).isdigit() or not str(e).isdigit() or not 0 <= int(s) <= int(e) < len(docs):
                    break
                group = [d['id'] for d in docs[int(s):int(e)+1]]
                if group not in groups: groups.append(group)
            else:
                if groups:
                    cid = f'f05-{lineno}-{n}'
                    cases.append(dict(id=cid,task='F05',pool=mid,query=q))
                    labels.append(dict(id=cid,groups=groups,source_row=lineno,question_index=n))
                    seen.add(norm(q))
                    continue
            counts['missing_or_invalid_annotation'] += 1
    return pools,cases,labels,counts


def write(folder,name,rows):
    (folder/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))


def main():
    p=argparse.ArgumentParser();p.add_argument('raw',type=Path);p.add_argument('--output',type=Path,default=ROOT/'data')
    opts=p.parse_args()
    for line in (ROOT/"SOURCES.sha256").read_text().splitlines():
        expected,name=line.split()
        if hashlib.sha256((opts.raw/name).read_bytes()).hexdigest()!=expected:
            raise ValueError("Source checksum mismatch: "+name)
    docs,bc,bg,ba=bugs(opts.raw);pools,qc,qg,qa=meetings(opts.raw)
    assert min(len(bc),len(qc))>=100
    pools['thunderbird']=docs
    dest=opts.output;dest.mkdir(exist_ok=True,parents=True)
    write(dest,'pools.jsonl',[dict(pool=k,documents=v) for k,v in pools.items()])
    write(dest,'cases.jsonl',bc+qc);write(dest,'gold.jsonl',bg+qg)
    print(json.dumps(dict(F02=len(bc),F05=len(qc),issues=len(docs),meetings=len(pools)-1,bugs_excluded=ba,qmsum_excluded=qa),indent=2))

if __name__=='__main__':
    main()
