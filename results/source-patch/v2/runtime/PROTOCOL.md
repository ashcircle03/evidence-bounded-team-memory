# Decision patch v2 — fixed before inference

One run, same Qwen3-8B revision, nonthinking/temp0, same37 QA inputs and original
keys as completion v3b. Existing20 core answers+required evidence must remain20/20;
the eight previously passing state/value+review citation cases must remain8/8.
Rate strict direct-source coverage separately (the older release/pending output
already lacked its direct incoming citation). Judge the original writer/cache
positive relations for reconsideration+correct changed premise and the two
negative relations for no unnecessary proposal. Empty extraction, failed receipt,
missing update or parse failure cannot count as a correct negative. Inspect actual
source sentences and before/after delta, not keyword labels. Preserve any failure.

Implementation: the v1 flat value schema let actions occupy premise fields
and caused format failures, losing earlier fact corrections. v1 is preserved and
not adopted. Keep the v3b factual comparison input/prompt/output unchanged. Extract
only reasoned decisions from old sources through vLLM guided_json; decision and
basis are different immutable source references. Existing factual proposals that
overlap those decision/basis spans are suppressed and retained in the audit. A
scoped RFC6902 patch can replace only the basis reference with incoming evidence;
it cannot change action or choose kind. A changed basis yields reconsideration;
unchanged/not-addressed gives no proposal. Unknown remains an explicit abstention,
not a correct negative. Explanations render original quotes, not invented values.
No extra QA stage or prompt. jsonpatch1.33/jsonpointer3.0.0 unmodified. Two comparison
calls for pure fact inputs, three when decisions need updates. Source/owner
approval and evidence contracts are unchanged. Guided schema reaches HTTP while
retaining nonthinking and the original QA model configuration.

GPU1, conda, Slurm12h, no node pin, max800 calls, no paid API. Temporary stores
on node-local /local_datasets; exported full source/proposal/vote/snapshot records
on Ceph. No semantic revision after outputs; do not add prompt variants this run.
This repeated authored development set is not a natural or independent benchmark.
