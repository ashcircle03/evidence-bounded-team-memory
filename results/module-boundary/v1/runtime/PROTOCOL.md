# Module boundary v1 — fixed before inference

Same Qwen3-8B revision, nonthinking/temp0, same37 inputs and original keys as
cup-completion-v3b. No classifier prompt, QA prompt, model, retrieval configuration
or training change. No new LLM stage. Compare requests and outputs as well as scores.

Changes: sentence selector retains exact original offsets; malformed candidates
are rejected independently (all duplicate kind/targets rejected); comparator call
failure is a recorded failed receipt and cannot block reading captured sources.
Reconsideration effects are explicit derived state, never factual corrections.
New reconsideration snapshots are versioned; existing v1 renderings stay stable.
Only contexts containing reconsideration receive the new effect field/text.

Acceptance: preserve all previously correct legacy20 answers and required source
citations, all eight prior state/value plus review-citation successes, exact scope
of factual corrections, immutable original sources, original-owner review.
Inspect writer/cache positives and near-miss negatives separately. Plumbing tests
with supplied correct labels do NOT establish improved model classification.
Failure/empty extraction is not a correct negative. No semantic tuning after run.
Report strict full source coverage separately from the historical core-value gate.

Use existing QA keys; do not put keys in actor inputs. Raw calls, output, sources,
proposals, votes and snapshots retained. This is repeated authored development
data, not held-out or a full EverMemBench/STALE benchmark. Only three legacy QA
questions are natural EverMem-derived questions.

GPU1, CPU8, RAM48G, Slurm12h, conda, no node pin, --no-requeue, max800 calls.
No paid API. Node-local stores; export results to Ceph. No automatic retry.
