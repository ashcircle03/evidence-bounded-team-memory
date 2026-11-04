"""Exercise ordinary Markdown arrivals, Qwen review, pending QA, and the original owner's vote."""
import argparse
import gc
import json
import os
from pathlib import Path
import subprocess
import tempfile

from evaluation.team_pilot.pilot import call_hash, write
from team_memory.evidence import active_sources, ask
from team_memory.store import Store
from team_memory.sync import followups, pull, relevant_followups, vote


def git(repo, *args, who="Fixture", day=1):
    stamp=f"2026-09-{day:02}T12:00:00+0000"
    env=dict(os.environ,GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM="1",
             GIT_AUTHOR_NAME=who,GIT_COMMITTER_NAME=who,GIT_AUTHOR_EMAIL="fixture@example.invalid",
             GIT_COMMITTER_EMAIL="fixture@example.invalid",GIT_AUTHOR_DATE=stamp,GIT_COMMITTER_DATE=stamp)
    return subprocess.check_output(["git","-c","commit.gpgSign=false","-C",str(repo),*args],env=env,stderr=subprocess.PIPE,text=True)


def exercise(folder, notes, reader_factory):
    writer, teammate=folder/"author",folder/"teammate"
    git(folder,"init","--bare","origin.git")
    git(folder/"origin.git","symbolic-ref","HEAD","refs/heads/main")
    git(folder,"clone","origin.git",str(writer))
    a,b=(Store(root/"shared") for root in (writer,teammate))
    (writer/"notes").mkdir()
    def raw(name):
        return json.loads((notes/(name+".json")).read_text())["source"]["text"]
    (writer/"notes"/"models.md").write_text(raw("jaewon")+"\n")
    (writer/"notes"/"tracking.md").write_text("We deferred parcel tracking because the courier does not supply scan identifiers.\n")
    git(writer,"add","notes")
    git(writer,"commit","-m","Record the original team decisions",who="jaewon")
    git(writer,"branch","-M","main")
    git(writer,"push","-u","origin","main")
    git(folder,"clone","origin.git",str(teammate))
    (teammate/"notes"/"benchmark.md").write_text(raw("seonghun")+"\n")
    (teammate/"notes"/"courier.md").write_text("Perhaps courier tracking will improve if scan identifiers arrive next year. There is no signed change or tested interface.\n")
    git(teammate,"add","notes")
    git(teammate,"commit","-m","Share the benchmark and courier notes",who="seonghun",day=2)
    git(teammate,"push","origin","HEAD:main")
    reader=reader_factory(192)
    arrival=pull(a,"대회 모델의 검증 성능을 높일 다음 비교를 고른다.",reader,"premise","notes")
    del reader
    gc.collect()
    git(writer,"add","shared")
    git(writer,"commit","-m","Share source records and pending review",who="jaewon",day=3)
    git(writer,"push","origin","HEAD:main")
    git(teammate,"pull","--ff-only")
    question="TabM 블렌드에 대해 어떤 검토가 열려 있고, 그 근거는 무엇인가?"
    pending=relevant_followups(b,question)
    reader=reader_factory(64)
    qa=ask(active_sources(b),question,reader,"premise")
    qa["review_context"]=pending
    old_ids=set(b.load("sources"))
    wrong_rejected=False
    desired=next((r for r in followups(a) if "benchmark.md#" in r["incoming"]["location"]
                  and "models.md#" in r["previous"]["location"] and r["reviewer"]=="jaewon"),None)
    if desired:
        pid=desired["id"]
        try:
            vote(b,pid,pid,"seonghun","approve")
        except ValueError:
            wrong_rejected=True
        vote(a,pid,pid,"jaewon","approve")
        git(writer,"add","shared")
        git(writer,"commit","-m","Owner approves a follow-up",who="jaewon",day=4)
        git(writer,"push","origin","HEAD:main")
        git(teammate,"pull","--ff-only")
    return dict(arrivals=arrival["arrivals"],pending_in_second_checkout=pending,qa=qa,
                nonowner_vote_rejected=wrong_rejected,after_owner_vote=followups(b),
                source_ids_before=sorted(old_ids),source_ids_after=sorted(b.load("sources")))


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("notes",type=Path)
    ap.add_argument("output",type=Path)
    mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--model");mode.add_argument("--recording",type=Path)
    a=ap.parse_args()
    calls=[]
    if a.recording:
        log=json.loads(a.recording.read_text())
    def factory(cap):
        if a.model:
            from team_memory.writer import local_generator
            model=local_generator(a.model,max_new_tokens=cap)
        def run(system,content):
            sha=call_hash(system,content)
            if a.model:
                raw=model(system,content)
                item=dict(sha256=sha,raw=raw,**model.last_usage)
            else:
                item=log["calls"][len(calls)]
                if sha!=item["sha256"]: raise ValueError("Git replay prompt mismatch")
                raw=item["raw"]
            calls.append(item)
            return raw
        return run
    with tempfile.TemporaryDirectory() as temp:
        out=exercise(Path(temp),a.notes,factory)
    if a.recording and (len(calls)!=len(log["calls"]) or out!=log["outcome"]):
        raise ValueError("Git replay outcome mismatch")
    write(a.output,dict(status="complete",job_id=os.environ.get("SLURM_JOB_ID","replay"),
                        calls=calls,outcome=out))
