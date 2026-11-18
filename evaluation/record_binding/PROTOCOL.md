# Learned binding v1 — freeze before inference

Scope: records condition/reason attachment only. Gold, scorer, all 68 source
documents and the previous Qwen3-8B outputs remain unchanged. No QA, test-set
training, per-case model selection, threshold tuning or semantic postfilter.

The complete pretrained GLiNER2.5-base-v1 boundary pipeline (pinned source and
checkpoint) extracts natural-anchor statement instances plus optional,
non-exclusive condition/basis fields from the original source. Encoder,
candidate generator, trained instance assignment, ABSENT and global decoder
must all run. Weights load strictly; random missing heads invalidate the run.
Schema field descriptions are task adaptation, not a claim of task training.

Primary comparator: accepted per-assertion storage path on the same 68 Qwen
outputs. Candidate: change only condition/basis fields for native anchors
exactly equal to one existing assertion span. No fuzzy/nearest-anchor join.
Unmatched or multiply matched groups stay unchanged, with diagnostics. An
empty native field removes that group's old field: do not selectively retain
old edges based on gold. Structural errors return the original graph with a
trace. Source, assertions, stances, time and subject are not rewritten.

Run original-source inference for every document, not only prior failures.
Report native anchor availability, native matches, skipped predictions and
storage effects separately from semantic scores. Hash actual model inputs and
outputs, preserve checkpoint config/weights and source revision. No score files
or gold are placed in the inference packet.

Adoption requires zero loss of prior correct required content, typed links,
assertion stances and complete documents, no increase in typed false links or
unnecessary extraction in either panel, and at least one gained correct
condition/basis link. Otherwise retain the accepted storage path and report
the causal limitation; do not weaken the gate or expand trials indefinitely.

Synthetic 54 documents (18 story families) and natural 14 audit documents are
diagnostic/development cases. Preserve their difficulty/evidence strata and
report separately. This is not held-out or representative benchmark evidence.
