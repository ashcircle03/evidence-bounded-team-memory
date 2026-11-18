# Fixed source-to-assertion binding comparison (2026-11-16)

Scope: records, not QA. No new training, model selection, label edits, threshold
search, per-document arm selection, or benchmark-derived demonstrations.

First instrument the original GLiNER2.5 checkpoint and the previous adapted
checkpoint without changing predictions. Read native candidate probabilities,
instance scores and field-assignment scores. Apply frozen gold only afterwards
to local diagnostics. Complete source coverage in a candidate is not the same
as a good, minimal candidate; report exact spans as well as material coverage.
Do not claim that these observations prove an architectural capacity ceiling.

Compare the accepted storage-preserving baseline (same 68 cached original Qwen
outputs) with one Qwen3-8B relation pass over those *fixed* existing assertions
and the complete original source. Use the same model revision, temperature0,
seed42, thinking disabled and max2048 output tokens. All documents receive the
same prompt, with no task examples; the additional call cost is reported.

The candidate adapts known-endpoint, typed relation extraction from Graphiti:
claim IDs cannot be generated again, only selected. Unlike its current dangling
endpoint materialization, reject unknown claim IDs. Unlike its paraphrased edge
facts, require exact context and evidence quotations using the existing real
LangExtract aligner. Evidence must contain the context and a target assertion.
This is a structural check, not proof of correct semantic attachment.

Use only positive additions. An empty list is not a deletion. A longer source
span can replace a contained span only for the same role and target. Different
roles, assertions, stances, approvals and original source bytes remain untouched.
Old semantic mistakes are not silently corrected by a gold-aware policy.

Freeze gold, scorer, input sources and this implementation before inference.
Score all68 and append/restart/read each stored result. Adopt only if all prior
correct required content, typed links, stances and whole documents survive,
neither natural nor synthetic panel increases false links or extra rows, and
at least one correct condition/basis link is gained. Otherwise retain the
baseline and report the concrete failure. Natural14 are selected development
failures; these are not unseen generalization results.

References inspected at pinned commits:
- GLiNER2 `c379245ce9fe0fee03a530a320ddb1885847c4d6` boundary records/engine/model.
- Graphiti `3a8a78c997a07cceeb3411ede533b0f342d71c64` extract_edges prompt and
  edge_operations endpoint/type handling. This is an adapter of its boundary,
  not execution of its entire graph service or an equivalent capability claim.
- PAIE `1917c46db1498e6115aa40897790d6b36a9b83e2` models/paie.py: marked-trigger
  argument spans require trained start/end selectors, supervised task schemas
  and matching loss. Its event checkpoint is not a ready rationale binder.

No extra evaluator pass is fed into model inference or used to choose outputs.
