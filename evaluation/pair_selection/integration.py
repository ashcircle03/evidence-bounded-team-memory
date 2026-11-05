"""Replay the CLI's pull and ask entry points around a real pending proposal."""
import contextlib
import io
import json
import sys
import tempfile
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

from team_memory.__main__ import main
from team_memory.evidence import active_sources,ask
from team_memory.store import Store,capture,digest
from evaluation.revision.integration import git
from evaluation.decision_records.build import read,save
from evaluation.pair_selection.trial import HERE,RESULT,streams

QUESTIONS={"unseen-2p":"Which configuration key opts sparse-checkout users into the earlier optimized branch-creation behavior?",
           "prior_git-03":"Which containing buffer did the earlier diff_words_flush() change free in addition to its members?"}

def qa_inputs(data):
    requests=[]
    for c,order,old,new in streams(data):
        if c["id"] not in QUESTIONS or order!="forward":continue
        with tempfile.TemporaryDirectory() as tmp:
            store=Store(Path(tmp))
            for env,_ in old.values():capture(store,env)
            capture(store,new)
            for phase in ("control","with-review"):
                def record(s,x):
                    requests.append(dict(id="live/"+c["id"]+"/"+phase,system=s,content=x,
                                         sha256=sha256((s+"\n"+x).encode()).hexdigest(),max_output_tokens=64))
                    return "NONE"
                ask(active_sources(store),QUESTIONS[c["id"]],record,"simple")
    return requests

def cli(store,args,generator):
    buffer=io.StringIO()
    with patch("team_memory.writer.local_generator",return_value=generator),patch.object(sys,"argv",["team_memory","--store",str(store.root),*args]),contextlib.redirect_stdout(buffer):
        main()
    return json.loads(buffer.getvalue())

def run(data):
    m=read(RESULT/"margins.json");g=read(RESULT/"generations.json")
    calls={r["id"]:r for r in g["calls"]}
    margins={r["sha256"]:r["margin"] for r in m["calls"]}
    outcomes={}
    for c,order,old,new in streams(data):
        cid=c["id"]
        if cid not in QUESTIONS or order!="forward":continue
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); upstream=root/"remote.git";upstream.mkdir()
            git(upstream,"init","--bare","--initial-branch=main")
            git(root,"clone",str(upstream),"member")
            member=root/"member"; origin_store=Store(member/"records")
            for env,_ in old.values():capture(origin_store,env)
            git(member,"add",".");git(member,"commit","-qm","Earlier decisions");git(member,"push","-u","origin","main")
            git(root,"clone",str(upstream),"client");store=Store(root/"client/records")
            capture(origin_store,new);git(member,"add",".");git(member,"commit","-qm","Incoming counterevidence");git(member,"push")
            def lookup(key,s,x):
                row=calls[key];assert row["sha256"]==sha256((s+"\n"+x).encode()).hexdigest()
                return row["raw"]
            def explain(s,x):return lookup(cid+"/forward/reason",s,x)
            explain.evidence_margin=lambda s,x:margins[sha256((s+"\n"+x).encode()).hexdigest()]
            result=cli(store,["pull","--strategy","pairwise","--model","replay"],explain)
            before=cli(origin_store,["ask",QUESTIONS[cid],"--strategy","simple","--model","replay"],lambda s,x:lookup("live/"+cid+"/control",s,x))
            after=cli(store,["ask",QUESTIONS[cid],"--strategy","simple","--model","replay"],lambda s,x:lookup("live/"+cid+"/with-review",s,x))
            context=after.pop("review_context",[])
            outcomes[cid]=dict(pull=result["arrivals"],qa_control=before,qa_with_review=after,
                               same=before==after,review_context=context,
                               same_sources=origin_store.load("sources")==store.load("sources"))
    return outcomes

if __name__=="__main__":save(RESULT/"integration.json",run(read(HERE/"corpus.json")))
