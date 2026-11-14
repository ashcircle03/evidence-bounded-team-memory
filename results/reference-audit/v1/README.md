# Reference composition audit — pending GPU

2026-11-14. [원형 대조와 판단](../../../docs/reference-composition-audit.md).

- Job122740: PENDING / QOSMaxGRESPerUser. No new inference results yet.
- Unrelated121613 holds the account's4 GPU allocation. It was not modified.
- Frozen45 QA,4 conditions,180 planned outputs. All are development diagnostics.
- Local contract tests16 passed; source packet79 files verified. Not model accuracy.
- `historical-stage-analysis.json`: actual saved draft/judge outputs verified
  against their HTTP traces. Oracle8:24 judgments,0 contradictions,0 revisions,
  6 prior answer-rating failures. This is historical evidence, not fresh scores.
- Production files are unchanged by this audit. No new model module or prompts
  were put into the production path. New variants only exist under evaluation/.

## Resume without duplicate submission

1. Read `dispatch.json` and canonical campaign ledger. Query122740 via squeue/sacct.
2. Do not submit another job or change121613. If pending for quota, keep it pending.
3. On completion require COMPLETED/0:0 and retrieve these exact small artifacts:
   `/ceph_data/pjw031003/capstone-shared-knowledge/results/reference-audit-122740.json`
   and `.calls.jsonl`, plus `sm-122740.json` and `logs/sm-122740.log`.
   Save locally as result.json/calls.jsonl/server.json/run.log, preserving originals.
4. Check server/client complete, then run locally:
   `.venv/bin/python -m evaluation.reference_audit.analyze fresh`.
   This validates hashes,45 drafts,180 outputs and traces, then creates blind cards.
5. Score every answer/source/state against frozen local keys and actual source text.
   No keyword-only semantic pass; no blank rating counted as success. Report all
   changed cases, source/condition errors, decomposition loss, truncations and cost.
6. Apply PROTOCOL.md adoption gates. Do not change the frozen code/key or start
   new variants after viewing outputs. Update decision and report measured limits.

Known upstream relation mistakes remain in observed17; supplied-correct oracle8
is separate. Existing20 answer/evidence preservation is separate from sentence-level
citation quality. Compare fresh current with other arms, not new scores against
an unqualified historical total. No automated semantic judge selects a winner.

## Artifacts

- `freeze.json`: source/packet and local gold hashes, frozen before submission.
- `runtime/`: exact7 uploaded files; no evaluation keys or prior answers.
- `case-provenance.json`: source jobs and old result hashes per question.
- `gold-*`, `*-historical-ratings.json`: existing criteria and previous judgments.
- `historical-outputs.json`: old responses, not inference inputs.
- `dispatch.json`: actual job ID and latest state; canonical ledger is
  `../../../../campaigns/speakermem-dev/campaign-dispatch.json`.
- `reference-source-manifest.json`: upstream code URLs and hashes inspected.

Two local packaging failures (missing key path, absent optional namespace init)
were corrected before freezing or submission; no GPU jobs were started for them.
Their partial files were preserved in `v1-prepare-incomplete*` and matching local
campaign source directories. They are not completed runs.
