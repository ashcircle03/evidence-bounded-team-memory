"""Replay exact measured prompts through real Git transport and owner review."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import tempfile
from team_memory.store import Store, capture
from team_memory import timeline as t
from team_memory.timeline_cli import pull


def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args],text=True,stderr=subprocess.STDOUT).strip()


def replay(row,recorded):
    calls=iter(recorded['calls']);used=[]
    def generate(system,content):
        r=next(calls)
        assert (system,content)==(r['system'],r['content']), (row['id'],len(used),'prompt mismatch')
        used.append(sha256((system+'\n'+content).encode()).hexdigest())
        return r['raw']
    with tempfile.TemporaryDirectory(prefix='timeline-git-') as tmp:
        root=Path(tmp);origin=root/'origin.git';a=root/'author';b=root/'reader'
        subprocess.run(['git','init','--bare',str(origin)],check=True,capture_output=True)
        subprocess.run(['git','clone',str(origin),str(a)],check=True,capture_output=True)
        git(a,'config','user.name','Timeline fixture');git(a,'config','user.email','fixture@example.invalid')
        git(a,'checkout','-b','main');(a/'README').write_text('Simulated local collaboration; no external remote.\n')
        git(a,'add','.');git(a,'commit','-m','Initialize');git(a,'push','-u','origin','main')
        git(origin,'symbolic-ref','HEAD','refs/heads/main')
        subprocess.run(['git','clone',str(origin),str(b)],check=True,capture_output=True)
        git(b,'config','user.name','Timeline fixture');git(b,'config','user.email','fixture@example.invalid')
        sa,sb=Store(a/'records'),Store(b/'records');outputs=[]
        for step in row['steps']:
            if step['op']=='ingest':
                git(a,'pull','--ff-only');capture(sa,step['source'])
                git(a,'add','records');git(a,'commit','-m','Publish source');git(a,'push')
                result=pull(sb,generate,recorded['mode'])
                git(b,'add','records')
                if git(b,'diff','--cached','--name-only'):
                    git(b,'commit','-m','Record local assessment');git(b,'push')
                outputs.append(dict(op='ingest',receipt=result))
            elif step['op']=='ask':
                answer=t.ask(sb,step['question'],generate,recorded['mode'])
                expected=next(x['result'] for x in recorded['steps'] if x['op']=='ask' and x['id']==step['id'])
                assert answer==expected,(row['id'],step['id'],'answer changed')
                outputs.append(dict(op='ask',id=step['id'],answer=answer))
            else:
                git(a,'pull','--ff-only')
                found=[p for p in t.proposals(sa) if p['kind']==step['kind']
                       and p['previous']['source_id']==step['previous'] and p['incoming']['source_id']==step['incoming']
                       and step['old_contains'] in p['previous']['quote'] and step['new_contains'] in p['incoming']['quote']]
                for p in found:t.review(sa,p['id'],step['actor'],step['choice'])
                if found:
                    git(a,'add','records');git(a,'commit','-m','Original owner reviews exact proposal');git(a,'push')
                assert pull(sb,generate,recorded['mode'])==[]
                outputs.append(dict(op='review',matched=len(found)))
        try:next(calls);raise AssertionError('unused model call')
        except StopIteration:pass
        git(a,'pull','--ff-only')
        assert t.view(sa)==t.view(sb)==recorded['final_state']
        assert sb.load('sources')==recorded['objects']['sources']
        return dict(status='passed',id=row['id'],mode=recorded['mode'],calls_replayed=len(used),
                    prompt_hashes=used,steps=outputs,clones_converged=True,raw_sources_unchanged=True)


if __name__=='__main__':
    import sys
    rows=json.loads(Path(sys.argv[1]).read_text());data=json.loads(Path(sys.argv[2]).read_text())
    result={uid:replay(next(r for r in rows if r['id']==s['id']),s) for uid,s in data['streams'].items()}
    Path(sys.argv[3]).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
