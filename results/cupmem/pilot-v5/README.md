# CUPMem stopped pilot: verified scope and next decision

This is one completed STALE T1 case and a partial T2 case, using BAZE
`gpt-5.4-mini` and `gemini-3.1-flash-lite`. It is **not** the original-model paper
score reproduction, a completed two-case pilot, or a benchmark-wide result.
The native code, prompts, schema and original judgments have not been changed.

## Execution and integrity

Aurora job 119626 ended `FAILED / 1:0` after 32m15s because the program enforced
the 1000 physical-request limit (`BudgetStop`). It was not a Slurm timeout or OOM.
One case completed all 50 sessions and three probes; the next case saved six
completed sessions and stopped during the seventh. Every sent attempt counts,
including work after the last session checkpoint and an SDK retry.

The [artifact audit](artifact-audit.json) independently checks the frozen source
archive and config, all physical request hashes and model roles, the actual
writer inputs, raw composer answers and rationales, raw judge inputs/outputs,
and six query-boundary memory hashes. The dataset hash was checked by the
executed compute-node runner; the dataset was not copied or rehashed locally.
This verifies artifact linkage, not semantic correctness.

| Measured component, completed T1 | Physical requests | Known input tokens | Known output tokens |
|---|---:|---:|---:|
| CUPMem writes across 50 sessions | 902 | 2,628,738 | 128,400 |
| CUPMem reads across 3 probes | 20 | 139,466 | 5,944 |
| Direct reads across 3 probes | 3 | 372,104 | 643 |
| Official judges, both arms | 2 | 2,580 | 368 |

Compatibility probes and 71 T2 attempts bring the run total to 1000 requests,
3,301,189 known input tokens and 146,887 known output tokens. Request 69 timed
out at the transport layer: its unknown bill retains a reservation of 9000 input
and 8192 output tokens. It is not treated as free. No output was length-censored.
BAZE currency/credit debits are unavailable, so these counts are not a cash bill.
The direct baseline used the official privileged gold-preserving truncation;
it kept 40/41/41 of 50 sessions for the three probes. CUPMem ingested all 50.

## Scientific interpretation

The unmodified official judge reports CUPMem 2/3 and direct 1/3. One case cannot
establish a performance difference. More importantly, the
[raw-source audit](source-audit.md) finds:

1. An unsupported inferred prior preference produced `UNKNOWN_CURRENT` in
   session 0. Unrelated meditation/productivity evidence weakened gift-reciprocity
   memory in session 1.
2. The actual change in session 38 **was detected**. Because the item was already
   weak, `WEAK_CHALLENGE_IDEMPOTENT` left its old reason in the persistent item
   revision history. The valid later reason remains in the session trace only.
3. The new conversation contains a default behavior and an exception. CUPMem's
   IPA response has source support for the exception, but omits the default and
   broadens the exception. The official judge receives the short gold summary,
   not all those turns. Neither a complete success nor a wholly invented answer
   is an adequate description.

No counterfactual intervention has been run, so the two passing answers are not
claimed to have been caused exclusively by the earlier memory errors. No native
semantic rules have been patched based on this observation.

The [provenance audit](provenance-audit.json) prepares a later citation adapter:
it resolves only native-selected records to literal original turns and binds
the selection to the actual composer request and query-time state. Missing
links never trigger a full-history fallback. This is source expansion, **not**
a completed cited reader or a measured citation-preservation result. Native
status annotations and their source support need an explicit common-reader
presentation policy before a fair adapter comparison.

## Offline preparation validation

The incremental native-QA core now preserves each original event and a separate
query-time snapshot. Its fake-engine tests cover all80 exported cases,
280 source arrivals and146 existing QA checkpoints. This does not constitute
an executed CUPMem transfer evaluation. Common cited-reader prompts, review
assessment, provider integration and Slurm execution remain to be wired.

[Offline validation](../offline-validation.json):60 tests passed and1 SDK test
was skipped in the local environment; no model calls. Independent code review
identified and corrected model-role/answer linkage gaps in the partial verifier,
and serialization/event-attribution/query-time hash gaps in the new core.

## Remaining scope

The second official case, full benchmark inference, the 60 Git/20 timeline
transfer comparison, and new-actor legacy 20 QA/citation preservation remain
unmeasured. Their original inputs have been exported separately from answer
keys; the legacy corpus was recovered from actual historical input hashes and
outputs, without shortening it to gold passages. That reconstruction is not a
new QA result.

Additional inference awaits the pending capacity/provider decision. The
1000-request authorization is exhausted; no new API call or Slurm allocation
was made during this offline audit. The proposed 4000-request continuation does
not authorize the 400-case benchmark and does not guarantee that all team/legacy
evaluation will fit. All future allocations require GPU>=1 and explicit conda.
The goal remains active and incomplete; CUPMem adoption or a justified design
addition must follow the remaining measured comparisons.

## Reproduce the offline checks

From the repository root:

```sh
python3 -m evaluation.cupmem.partial_verify \
  ../campaigns/speakermem-dev/results/sm-119626.json \
  ../campaigns/speakermem-dev/source/cup-pilot-v5 \
  results/cupmem/pilot-v5 \
  ../campaigns/speakermem-dev/campaign-dispatch.json \
  results/cupmem/pilot-v5/artifact-audit.json
python3 -m evaluation.cupmem.source_audit
python3 -m unittest tests.test_cupmem_partial_verify tests.test_cupmem_transfer_inputs tests.test_cupmem_legacy_inputs tests.test_cupmem_provenance
```
