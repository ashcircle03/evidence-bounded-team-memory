"""Rank complete source turns and claim text separately; retain conversational context."""
import math
import re
from collections import Counter

def words(s):
    stop=set("the which were this that about from they our after with what who for and when how was did does are has have been their its during would will should could into some please you them those any just something can based".split())
    ws=re.findall(r"[^\W_]+", s.casefold())
    def stem(w):
        if len(w)>5 and w.endswith("ies"):return w[:-3]+"y"
        if len(w)>6 and w.endswith("ing"):return w[:-3].rstrip('e')
        if len(w)>5 and w.endswith("ed"):return w[:-2].rstrip('e')
        if len(w)>4 and w.endswith("s"):return w[:-1]
        return w.rstrip('e') if len(w)>5 else w
    return [stem(w) for w in ws if len(w)>1 and w not in stop]

def rank(query, documents):
    q=set(words(re.split(r'\n\s*Options:',query,flags=re.I)[0]))
    bags={k:Counter(words(s)) for k,s in documents.items()}
    df=Counter(w for b in bags.values() for w in b)
    avg=sum(map(lambda b:sum(b.values()),bags.values()))/max(1,len(bags))
    scores={}
    for k,bag in bags.items():
        score=sum(math.log1p((len(bags)-df[w]+.5)/(df[w]+.5))*bag[w]*2.2 /
                  (bag[w]+1.2*(.5+.5*sum(bag.values())/max(1,avg))) for w in sorted(q & bag.keys()))
        if score: scores[k]=score
    return sorted(scores,key=lambda k:(-scores[k],k))

def retrieve(sources, rows, question, issue=None):
    src={k:v['source'] for k,v in sources.items()}
    loc={(s['location'],s['text']):k for k,s in src.items()}
    def key(r):
        s=r['record']['source'];return loc.get((s['location'],s['text']))
    live=[r for r in rows if r['status'] not in ('superseded','rejected')]
    if issue:
        chosen=[r for r in live if r['record']['issue']==issue]
        return [],chosen
    excluded={key(r) for r in rows if r['status'] in ('superseded','rejected')}-{key(r) for r in live}
    raw=rank(question,{k:s['speaker']+' '+s['text'] for k,s in src.items() if k not in excluded})
    by_id={r['id']:r for r in live}
    ranked=rank(question,{k:' '.join([r['record']['issue'],r['record']['quote'],r['record']['value'],*r['record']['scope'].values()]) for k,r in by_id.items()})
    raw_ids=raw[:7]
    # Duration questions need endpoints, which seldom repeat all the phrasing of the question.
    if re.search(r'how (?:many|long)|duration|elapsed',question,re.I) and re.search(r'spent|took|elapsed|duration',question,re.I):
        for pattern in (r"\b(?:i.m starting|i am starting|started|began|kicked off)\b",r"\b(?:complete[d]?|finished|marked .* complete)\b"):
            pool={k:s['speaker']+' '+s['text'] for k,s in src.items() if k not in excluded and re.search(pattern,s['text'],re.I)}
            for k in rank(question,pool)[:1]:
                if k not in raw_ids:raw_ids.append(k)
    chosen=[by_id[k] for k in ranked[:3]]
    # Adjacency is meaningful only within the exact same conversation and day.
    # Recover the reply to a highly-ranked query/request, even if it uses pronouns.
    sibling={s['location']:k for k,s in src.items() if k not in excluded}
    for k in raw[:3]:
        s=src[k];base,_,pos=s['location'].rpartition('/')
        if pos.isdigit() and '?' in s['text']:
            neighbor=sibling.get(base+'/'+str(int(pos)+1))
            if neighbor and neighbor not in raw_ids:raw_ids.append(neighbor)
    return raw_ids,chosen
