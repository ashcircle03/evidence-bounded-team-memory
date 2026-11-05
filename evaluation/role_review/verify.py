"""Replay raw answers, validate links and reconcile every requested Slurm job."""
from hashlib import sha256
from pathlib import Path
import zipfile

from evaluation.contrast_review.score import run
from evaluation.decision_records.build import ROOT, WORK, read, save
from evaluation.pair_selection.qa import packets
from evaluation.pair_selection.qa_replay import historical
from team_memory.role_review import valid_ledger

HERE=Path(__file__).resolve().parent
OUT=ROOT/"results/role_review"
ATTEMPTS={
    "records-read-v23":"development.json", "records-read-v26":"development-v2.json",
    "records-read-v25":"qa-generations.json", "records-read-v27":"development-v3.json",
    "records-read-v24":"comparison-v3.json",
    "records-read-v28":"development-final.json", "records-read-v29":"comparison.json",
}

def verify():
    campaign=WORK/"campaigns/speakermem-dev"
    ledger=read(campaign/"campaign-dispatch.json")
    attempts=[]
    for stage,name in ATTEMPTS.items():
        job=ledger["jobs"][stage]
        result=read(OUT/name)
        assert job["verified"] and (job["state"],job["exit_code"])==("COMPLETED","0:0")
        assert result["status"]=="complete" and str(result["job_id"])==job["job_id"]
        assert result["input_sha256"]==job["source_sha256"]["packets.json"]
        src=campaign/"source"/stage
        for filename,h in job["source_sha256"].items():
            assert sha256((src/filename).read_bytes()).hexdigest()==h
        if stage in ("records-read-v28","records-read-v29"):
            with zipfile.ZipFile(src/"infer.py") as z:
                for path in (ROOT/"team_memory").glob("*.py"):
                    assert z.read(f"team_memory/{path.name}")==path.read_bytes()
        if stage in ("records-read-v24","records-read-v29"):
            assert (src/"packets.json").read_bytes()==(HERE/"inputs.json").read_bytes()
        attempts.append(dict(stage=stage,job=job["job_id"],state=job["state"],exit_code=job["exit_code"],
                             elapsed_seconds=job["elapsed_seconds"],gpu=job["gpus"],wall_minutes=job["wall_minutes"],
                             max_rss=[r["MaxRSS"] for r in job["usage"] if r["JobID"].endswith(".batch")],
                             source_sha256=job["source_sha256"],output=name,
                             result_sha256=sha256((OUT/name).read_bytes()).hexdigest()))
    save(OUT/"runs.json",dict(attempts=attempts,elapsed_gpu_seconds=sum(r["elapsed_seconds"] for r in attempts),
                              campaign_gpu_seconds=sum(v["elapsed_seconds"] for v in ledger["jobs"].values() if v["gpus"]),
                              cap_gpu_minutes=ledger["budget"]["single_gpu_minutes"]))
    shots=read(OUT/"qa-generations.json")["calls"]
    qa=historical(packets()[1],{r["id"]:r for r in shots})
    save(OUT/"qa-historical.json",qa)
    result=read(OUT/"comparison.json")
    changes = {}
    for cid, methods in result["results"].items():
        if "role-reversed" in methods:
            changes[cid] = methods["role-reversed"]["result"] == methods["role-review"]["result"]
        out=methods["role-review"]["result"]
        if out["action"] in ("reassess","retest"):assert valid_ledger(out)
    key = read(HERE/"key.json")
    checks = {}
    for cid, fixture in result["qa"].items():
        before, after = [a["out"] for a in fixture["answers"]]
        checks[key[cid]["topic"]] = dict(identical=before == after,
            before=[a["answer"] for a in before.get("answers", [])],
            after=[a["answer"] for a in after.get("answers", [])],
            context_status=[item["status"] for item in fixture["context"]])
    save(OUT/"checks.json", dict(order=changes, pull_qa=checks,
         historical_qa=sum(q["identical"] for q in qa.values()), historical_n=len(qa),
         matched_batch_prompts=len(shots)))
    run(HERE,OUT)

if __name__=="__main__":verify()
