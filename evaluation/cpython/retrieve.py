"""Build label-free model inputs and record retrieval ranks, before any reader is invoked."""
import argparse
import gzip
import json
import re
import tempfile
from pathlib import Path
from team_memory.reconsider import prepare, witness
from team_memory.retrieval import rank
from team_memory.store import Store, capture, digest, source_envelope
from team_memory.qa import answer

def stripped(text):
    return re.sub(r"https?://[^\s>]+|:pep:`\d+`|\bPEP(?:\s*:\s*|[ -]*)\d+\b", " ",text,flags=re.I)

def evaluate(event, masked=False):
    envs={n:source_envelope(env) for n,env in event["history"].items()}
    sources={digest(env):env for env in envs.values()}
    incoming=source_envelope(event["incoming"])
    if masked:
        incoming["source"]["text"]=stripped(incoming["source"]["text"])
    new=incoming["source"]["text"]
    raw={k:v["source"]["text"] for k,v in sources.items()}
    pep={digest(env):n for n,env in envs.items()}
    target_list=rank(new,raw)
    index=target_list[0]
    others={k:doc for k,doc in raw.items() if k!=index}
    aux=rank(new+" "+raw[index],others)[:3]
    sid=digest(incoming)
    sources[sid]=incoming
    inc=witness(sid,incoming,0,new)
    direct={"section":witness(index,sources[index],0,raw[index]),"context":[witness(k,sources[k],0,raw[k]) for k in aux],"incoming":inc}
    batch=prepare(sources,sid,event["goals"][0][1],limit=1)
    scoped=next(iter(batch["cases"]),None)
    return ({"plain_rank": [pep[k] for k in target_list],"module_top1":pep[scoped["decision"]["source_id"]] if scoped else None},
            direct,scoped)

def prepare_all(rows):
    packets=[]
    ranks={}
    for event in rows:
        ranking,direct,scoped=evaluate(event)
        redacted,_,_=evaluate(event,True)
        id_=event["id"]
        ranks[id_]={"raw":ranking,"masked":redacted,"documents":len(event["history"]),"parent":event["parent"]}
        packet={"id":id_,"goals":event["goals"],"direct":direct,"module":scoped,"qa":[]}
        for key,q in event["qa"]:
            for phase in (("before","after") if key=="historic" else ("after",)):
                docs=dict(event["history"])
                if phase=="after":
                    docs[str(event["pep"])]=event["incoming"]
                ordered=rank(q,{k:v["source"]["text"] for k,v in docs.items()})[:3]
                with tempfile.TemporaryDirectory() as tmp:
                    store=Store(tmp)
                    for k in ordered:
                        capture(store,docs[k])
                    result=answer(store,q)
                packet["qa"].append({"kind":key,"phase":phase,"question":q,"selected":ordered,
                                     "evidence":result})
        packets.append(packet)
    return packets,ranks

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs",type=Path);ap.add_argument("packets",type=Path);ap.add_argument("ranks",type=Path)
    a=ap.parse_args()
    rows=json.loads(gzip.decompress(a.inputs.read_bytes()))
    packets,ranks=prepare_all(rows)
    a.packets.write_bytes(gzip.compress(json.dumps(packets,ensure_ascii=False,sort_keys=True).encode(),mtime=0))
    a.ranks.write_text(json.dumps(ranks,indent=2)+"\n")
