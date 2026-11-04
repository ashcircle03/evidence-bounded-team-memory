"""Build as-of PEP snapshots using only immutable local git objects."""
import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUBLIC = "https://github.com/python/peps/blob/"
def git(repo, *args, data=None):
    return subprocess.check_output(["git", "--git-dir", str(repo), *args], input=data)

def past_text(raw):
    header, sep, body = raw.partition("\n\n")
    fields = [l for l in header.splitlines() if l.startswith(("PEP:", "Title:", "Status:"))]
    if not sep or not fields:
        raise ValueError("unrecognized PEP")
    return "\n".join(fields) + "\n\n" + body.lstrip()[:1800].rstrip()

def envelope(n, commit, time, text):
    return {"owner":f"PEP {n} contributors", "observed_at":time,
            "source":{"speaker":f"PEP {n} contributors", "location":f"{PUBLIC}{commit}/peps/pep-{n:04}.rst","text":text}}

def build(repo, events):
    cases = []
    for event in events:
        commit = event["commit"]
        parent = git(repo,"rev-parse",commit+"^1").decode().strip()
        old_date, new_date = [git(repo,"show","-s","--format=%cI",r).decode().strip() for r in (parent,commit)]
        entries = {}
        for line in git(repo,"ls-tree","-r",parent,"--","peps").decode().splitlines():
            meta,path = line.split("\t",1)
            match = re.fullmatch(r"peps/pep-(\d{4})\.rst",path)
            if match:
                entries[int(match[1])] = meta.split()[2]
        assert event["pep"] not in entries
        stream = io.BytesIO(git(repo,"cat-file","--batch",data=("\n".join(entries.values())+"\n").encode()))
        past = {}
        for n, oid in entries.items():
            sha, kind, length = stream.readline().split()
            assert sha.decode()==oid and kind==b"blob"
            raw = stream.read(int(length)).decode()
            assert stream.read(1)==b"\n"
            past[str(n)] = envelope(n,parent,old_date,past_text(raw))
        path = f"peps/pep-{event['pep']:04}.rst"
        raw = git(repo,"show",commit+":"+path).decode()
        new = "\n".join(raw.splitlines()[:160])
        cases.append({**event,"parent":parent,"history":past,"incoming":envelope(event["pep"],commit,new_date,new)})
    return cases

if __name__ == "__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("bare_repo",type=Path)
    ap.add_argument("output",type=Path)
    args=ap.parse_args()
    rows=build(args.bare_repo,json.loads((HERE/"events.json").read_text()))
    raw=json.dumps(rows,ensure_ascii=False,sort_keys=True).encode()
    args.output.write_bytes(gzip.compress(raw,mtime=0))
    print([(r["id"],len(r["history"])) for r in rows])
    print(hashlib.sha256(args.output.read_bytes()).hexdigest())
