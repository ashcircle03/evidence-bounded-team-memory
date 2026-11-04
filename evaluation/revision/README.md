# Replaying the second trial

Production was frozen at `3f0dc09` after the Aimers and EverMem development runs. The second commit `e1c3cd4` fixes the held-out casebook, scoring code, answer keys and every request hash. Each public historical review uses actual ancestors of the incoming commit. Incoming bug reports that name an older commit preserve that natural cross-reference. The reviewer receives the history, new source and generic project goal. The keys never enter a model call.

From the repository root, run these commands with Python 3.10+ (3.12 used in CI) and Git. The source archive is regenerated from upstream Git objects. The first fetch downloads Git history because three reported regressions revisit decisions several years old.

```sh
export PYTHONPATH=.
mkdir -p .cache/revision
git clone --bare --single-branch --branch v2.49.0 https://github.com/git/git.git .cache/revision/git.git
git init --bare .cache/revision/peps.git
git --git-dir=.cache/revision/peps.git fetch --depth=1 https://github.com/python/peps.git 16991a9ce7b223b38f0b473f51a8a7d94c8b9249
curl -fL 'https://huggingface.co/datasets/EverMind-AI/EverMemBench-Dynamic/resolve/a6b210a32248e841967b7b64a64281d2ff3f669d/01/dialogue.json' -o .cache/revision/dialogue.json
python3 evaluation/revision/build_final.py .cache/revision/git.git .cache/revision/source.json .cache/revision/key.json
cmp .cache/revision/key.json evaluation/revision/final-key.json
python3 evaluation/revision/regression.py .cache/revision/peps.git .cache/revision/dialogue.json .cache/revision/regression.json
python3 evaluation/revision/replay.py .cache/revision/source.json .cache/revision/regression.json results/revision/outputs.json .cache/revision
python3 evaluation/revision/score.py .cache/revision/key.json .cache/revision/final-outcomes.json .cache/revision/scored.json --overrides results/revision/adjudication.json
cmp .cache/revision/scored.json results/revision/scored.json
```

Add `--show r15/premise` to the replay command to inspect the prior decisions, complete incoming report as retrieved, raw model response and the proposal an owner would see. Use `--show q01-ordinary/legacy` for the existing reader or `--show d06/premise` to see every source-isolated QA read. Historical source times are Git committer times. Configuration QA is as of release commit `683c54c`. The documentation is segmented at headings for every option in 22 configuration files. Each source can be checked against the linked line range. An original and its unrelated-calendar repeat count as one event.

To use ordinary Git notes in two clones, run `python3 -m team_memory --store shared-records pull --model /path/to/Qwen --strategy premise --notes-dir notes` in the receiving clone after another member shares a note. On first use it imports prior versions of notes from the local pre-pull history and reviews the incoming commits in order. The input directory is repository-relative. Source records refer to the original Git object, file and line numbers. To share pending proposals with another member, track the chosen store in the team repository, commit and push it. `inbox` and relevant `ask` responses expose pending status and both citations. The `review` command binds the proposal to its original owner's recorded identity. Identity verification relies on the team's Git permissions. An approved review opens follow-up work. Replacing an accepted claim goes through the separate existing record-review workflow.


The integration recording from job 119276 also runs locally without Qwen weights. It recreates two disposable clones with deterministic commits, replays only matching prompt hashes, and checks the complete outcome including the pending view, owner vote, and retained sources.

```sh
PYTHONPATH=. python3 evaluation/revision/integration.py evaluation/revision/development .cache/revision/git-replay.json --recording results/revision/git-integration.json
```

For a GPU reproduction, use `evaluation/revision/run.py` on each generated casebook to produce the final and regression packet arrays. Concatenate them in that order, serializing with `json.dumps(packets, ensure_ascii=False, indent=2) + "\n"`; verify the file SHA against `freeze.json`. Run `python3 evaluation/team_pilot/infer.py packets.json /path/to/pinned/Qwen output.json JOB_ID --count 286 --max-new-tokens 192` on a Slurm GPU allocation. Use `integration.py --model /path/to/pinned/Qwen` instead of `--recording` for the complete Git interaction. The model revision and budget amendment are in `freeze.json` and `PROTOCOL.md`.
