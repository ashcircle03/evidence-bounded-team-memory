"""Rebuild the frozen evaluation from PEP Git objects and replay the saved responses."""

import argparse
import hashlib
import json
import zlib
from pathlib import Path

from assess import evaluate
from build import build
from retrieve import prepare_all

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def pilot_gzip(raw):
    # The pilot hashes the archive, including the platform-specific gzip OS byte.
    # zlib (level 9) made the original deflate stream on macOS (OS byte 19).
    archive = bytearray(zlib.compress(raw, level=9, wbits=31))
    archive[9] = 19
    return bytes(archive)


def verified_archive(name, rows, expected):
    compressed = pilot_gzip(
        json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()
    )
    if hashlib.sha256(compressed).hexdigest() != expected:
        raise ValueError(f"cannot reproduce the recorded SHA-256 of {name}")
    (HERE / name).write_bytes(compressed)


def replay(repo):
    freeze = json.loads((HERE / "freeze.json").read_text())
    events = json.loads((HERE / "events.json").read_text())
    run = json.loads((ROOT / "results/cpython/outputs.json").read_text())

    snapshots = build(repo, events)
    verified_archive("inputs.json.gz", snapshots, freeze["sha256"]["inputs.json.gz"])
    # The frozen retrieval script reads the sorted snapshot from disk.
    rows = json.loads(json.dumps(snapshots, sort_keys=True))
    packets, ranks = prepare_all(rows)
    verified_archive("packets.json.gz", packets, run["packets_sha256"])

    scores = evaluate(ranks, run)
    cache = ROOT / ".cache"
    cache.mkdir(exist_ok=True)
    (cache / "ranks.json").write_text(json.dumps(ranks, indent=2) + "\n")
    (cache / "score.json").write_text(
        json.dumps(scores, ensure_ascii=False, indent=2) + "\n"
    )
    print(f"Verified {scores['gpu']['verified_calls']} recorded model calls.")
    print("Combined action and target hits:", scores["joint_hits"])
    print(
        "Grounded QA:",
        sum(row["model_ok"] for row in scores["qa"]),
        "/",
        len(scores["qa"]),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bare_repo", type=Path)
    replay(parser.parse_args().bare_repo)
