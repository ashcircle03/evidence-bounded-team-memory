"""Local-only courier. Send an authorized BAZE env credential via SSH stdin.

The receiver and helper run inside a recorded Slurm allocation with conda active.
Never pass the credential as a shell argument or Slurm environment export.
"""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys


def deliver(version):
    # Check BEFORE consuming the allocation's credential-receiver window.
    # Codex's per-directory shell environments differ; run this courier from
    # the workspace root where the user-authorized BAZE variable is configured.
    key = os.environ.get("BAZE_API_KEY")
    if not key:
        raise RuntimeError("BAZE_API_KEY is absent in this shell environment; do not submit a new job")
    work = Path(__file__).resolve().parents[3]
    campaign = work / "campaigns/speakermem-dev"
    ledger = json.loads((campaign / "campaign-dispatch.json").read_text())
    job = ledger["jobs"][version]
    assert job["submission_intent"] == "submitted" and str(job["job_id"]).isdigit()
    cfg = json.loads((campaign / "source" / version / "config.json").read_text())
    assert cfg["execution_authorized"] is True
    assert cfg["policy"]["base_url"] == "https://factchat-cloud.mindlogic.ai/v1/gateway"
    helper = job["source_path"] + "/unpacked/evaluation/cupmem/credential.py"
    script = "source /ceph_data/pjw031003/anaconda3/etc/profile.d/conda.sh\n"
    script += "conda activate " + shlex.quote(cfg["conda_prefix"]) + "\n"
    script += "exec python " + shlex.quote(helper) + " " + job["job_id"]
    command = ["srun", "--jobid=" + job["job_id"], "--overlap", "--nodes=1", "--ntasks=1",
               "--cpus-per-task=1", "--mem=256M", "/bin/bash", "--noprofile", "--norc", "-e", "-c", script]
    ssh = ["ssh", "-p", "30080", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15",
           "-o", "ControlPath=/private/tmp/team-memory-30080.sock", "pjw031003@aurora.khu.ac.kr"]
    # Authoritative live status before sending; a ledger is not a liveness check.
    state = subprocess.check_output(ssh + ["squeue -h -j " + job["job_id"] + " -o %T"], text=True).strip()
    assert state == "RUNNING", "Allocation is not RUNNING"
    result = subprocess.run(ssh + [shlex.join(command)], input=json.dumps({"api_key": key}),
                            text=True, capture_output=True, timeout=60)
    # Never echo raw stdout/stderr if the remote helper behaves unexpectedly.
    if result.returncode or ("credential_delivered " + job["job_id"]) not in result.stdout:
        raise RuntimeError("Credential courier failed; key not logged, inspect allocation state")
    print("credential_delivered", job["job_id"])


if __name__ == "__main__":
    deliver(sys.argv[1])
