# Records diagnostic evaluation

Run the key-free Qwen runner through the frozen Aurora packet. Production code is unchanged.

- `build.py`: deterministic synthetic strata and natural focal annotations.
- `arms.py`: concise extraction versus existing grouped prompt; shared schema/compiler.
- `run.py`: actual Qwen traces, compiler output, RecordsAdapter/restarted-adapter/reader transport.
- `score.py`: frozen focal-claim scoring; raw and compiled stages separately.
- `preflight.py`: gold-minimal-spans and deliberate metric failure checks.
- `PROTOCOL.md`: sampling, interpretation, stop conditions and limitations.
- `report.py`: rendering only, does not change frozen scores.

Results: `results/record-strata/v1/`. One natural annotation error (`n06`) was identified before reading model output and is preserved in `pre-output-label-audit.json`; exclude it from the interpretable natural aggregate. Keep original fixed scores for auditability. Do not silently replace the original key or pool natural and synthetic results.

Local checks: `NLTK_DATA="$PWD/.cache/reference-nltk" .venv/bin/python -m evaluation.record_strata.preflight`. Scoring/reports require the retrieved job results and frozen hashes.
