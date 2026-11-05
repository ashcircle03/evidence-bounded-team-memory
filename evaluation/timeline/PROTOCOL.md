# Accumulating evidence: minimal system comparison

Approved goal 2026-11-05. Do not preserve a complex module merely to justify earlier work.

Compare two runnable paths with the same Qwen2.5-14B-Instruct revision cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8, bf16 greedy:

- `direct`: append raw sources, then compare each arrival once against all earlier visible raw sources. Answer from those same sources and the actual proposal/review state.
- `indexed`: same raw history, comparator, QA reader, and approval engine; additionally extract and persist up to three verbatim decision/rationale/scope cards at arrival. These may help later reading but cannot replace raw evidence or authorize changes.

Both modes retain raw evidence and source-bound, owner-reviewed relations. A correction applies to its cited assertion, never every fact in a file. Approving reconsideration does not refute an old observation. Unreviewed reports remain usable as provisional evidence. An exact proposal ID and original source owner are needed to approve. All sources, proposals and votes are immutable objects suitable for Git exchange. Transported but unprocessed later sources must not enter an earlier inference.

This tests whether a persistent decision index adds value to a simple complete-source reader. It does not assert that structured records are beneficial, or that the former multi-stage gates should be retained. Existing QA defaults remain available and unchanged.

## Data and sequence

Five constructed development streams cover changed-decision conditions, condition-dependent coexistence, unresolved same-condition conflict, explicit correction, and unrelated arrivals. After development, freeze production code/prompts before constructing/selecting the final 20 streams (four per type). Do not tune on final predictions.

Final streams combine untouched, source-checked question/evidence records from a new EverMemBench-Dynamic topic 02 with explicitly synthetic worklog sequences. Natural QA checks factual retention; the synthetic extensions provide unambiguous review and approval semantics not labeled by the original benchmark. They are not genuine historical team decisions. Publish source IDs, version, selection reasons and transformations. Distinct worklog stories are controlled test events, not 20 independent organizations or official benchmark review labels. The original QA subset is support-selected and short-context; it does not estimate full-corpus retrieval performance.

Each stream arrives sequentially: a natural source, an earlier scoped worklog, a related distractor, new evidence, and simulated owner review. Test QA before new evidence, after it arrives, and after review. Each model sees only already-ingested raw sources, generated cards, and reviews that have happened. It receives no gold issue/scope labels, correct prior source marker, future question during indexing, or future result. The simulated owner approves only a supplied proposal that matches the declared review event; missing proposals remain missing. This conditional approval is a workflow fixture, not a learned human policy, and is reported separately from automatic proposal quality.

## Outcomes and stopping rule

Count review success only if the correct old assertion/decision is connected to the incoming evidence with the right conditions, source quotations, and action. Distinguish reconsideration from coexistence, conflict and correction. Reconsider/conflict/correction are owner-review requests; coexistence alone is not an alert. Report all unsupported alerts, including wrong explanations on positive streams. Wrong relations remain visible for inspection and are never counted as correct just because their quotes are literal.

Measure: grounded required-review hits; unnecessary review requests on no-review streams and unrelated arrivals; correct relation kinds/targets; QA answer plus actual supporting source, conditions, unresolved sides and review status at each checkpoint; stale answers after accepted correction; lost valid unrelated assertions; unapproved promotion and raw-source overwrites. Approval invariants are engine guarantees and do not count as model reasoning gains. Report parser failures and context/output caps separately.

Preserve the existing 20 QA regression results with their real 3B reader as a separate legacy check. New 14B timeline QA is the meaningful test of the changed history path, not a claim based on replaying an unchanged reader.

Each stream/arm has a common total cap of 120000 input and 7000 generated tokens, including indexing, comparisons and QA. No silent truncation or retries. Per-call generation caps: comparison 512, index 384, QA 320. Report actual calls, tokens, elapsed time and allocation GPU time; common ceilings are not equal realized cost. Complete histories are deliberately small enough to fit, so a weak retrieval baseline cannot explain the difference.

Candidate adoption requires more grounded required reviews without more unnecessary review requests, no lost correct QA relative to direct on the same checkpoints, and zero unapproved promotion/raw loss. No arbitrary winner is required: if indexing fails this criterion, select the simpler direct design, retaining the shared provenance/approval engine. Partial functionality may be retained with its limits; do not launch a sequence of repairs on the final set. At most one development revision based on observed development results, then one frozen final comparison. Infrastructure failures may be repaired separately with all attempts preserved.

Semantic grading uses source-based criteria fixed before final inference. The implementing agent's evaluation alone is not independent agreement; publish every contested/partial case and avoid statistical/generalization claims. The official natural QA answer is not sufficient when its cited message fails to support the requested fact.

## Compute

Aurora compute nodes only for server Python, data access, hashing and inference. Existing downloaded models; topic 02 data are verified/downloaded under /local_datasets from a CPU allocation. CPU extraction job wall 5 minutes. Development GPU2 wall 25 minutes; final comparison planned as two GPU2 jobs with 45-minute walls. Existing legacy QA GPU1 wall 10 minutes if needed. Goal cap 240 GPU-minutes including failures; cumulative campaign ceiling 500 GPU-minutes, CPU-only ceiling 100 minutes. At most 4 running, 8 queued+running, 4 GPUs; no node pinning, no requeue, no automatic increases after timeout/OOM. Persist actual IDs before mirroring, reconcile ambiguous submissions, and verify completed output against Slurm and frozen inputs.
