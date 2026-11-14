# Source patch v1 — fixed before inference

One run, same Qwen3-8B revision, nonthinking/temp0, same37 QA inputs and original
keys as completion v3b. Existing20 core answers+required evidence must remain20/20;
the eight previously passing state/value+review citation cases must remain8/8.
Rate strict direct-source coverage separately (the older release/pending output
already lacked its direct incoming citation). Judge the original writer/cache
positive relations for reconsideration+correct changed premise and the two
negative relations for no unnecessary proposal. Empty extraction, failed receipt,
missing update or parse failure cannot count as a correct negative. Inspect actual
source sentences and before/after delta, not keyword labels. Preserve any failure.

Implementation: old-only typed extraction, bounded RFC6902 update of value/scope,
deterministic kind gate, unchanged original sources and owner approval. Full raw
requests/outputs retained. No answer key in actor. No new answer prompts or QA
models. One extra comparison call per incoming source. jsonpatch1.33 and
jsonpointer3.0.0 are unmodified offline pure-Python dependencies with licenses.

GPU1, conda, Slurm12h, no node pin, max800 calls, no paid API. Temporary stores
on node-local /local_datasets; exported full source/proposal/vote/snapshot records
on Ceph. No semantic revision after outputs; do not add prompt variants this run.
This repeated authored development set is not a natural or independent benchmark.
