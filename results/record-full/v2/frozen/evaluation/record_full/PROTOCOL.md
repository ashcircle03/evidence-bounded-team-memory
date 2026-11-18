# Whole-document records evaluation v1

## Scope and exposure

Only records: automatic construction of source-grounded claim/context structures. No QA, retrieval, reconsideration or approval-model evaluation. Production extractor/schema/prompts remain unchanged.

The original68 sources, their source IDs, and all3x3 balanced synthetic strata are unchanged.54 synthetic variants come from18 base stories (six semantic templates across three construction difficulties);14 natural messages belong to5 failure-selected EverMem cases. Keep all variants/messages of one story together in future splits. Availability names refer to the original two focal qualifiers, NOT all information in the document: even a `none` document may contain complete distractor facts, which are now gold and scored too. The natural n06 legacy stratum is retained for traceability, but its full-document gold correctly includes the in-source file-storage subject. Natural scores stay separate from the balanced distribution.

This is retrospective developer-set evaluation. Prior model outputs and failures were already observed. New gold/scorer is frozen before this re-scoring, but that is NOT a blind pre-inference or held-out test. No independent human annotator has adjudicated the gold. Reuse the exact136 real Qwen3-8B calls from Aurora122970 (same model/inputs/prompts); there is no scientific reason to repeat identical inference solely to replace a scoring key. Verify cached evidence hashes, completion, settings and prompt reconstruction. Fresh model calls0. No paid API or server computation this round; scoring runs locally.

## Annotation policy

`gold.py` reads sources and source specifications only, never model output. `gold.json` inventories every substantive record root and its claim text, applicability conditions, explicit reasons, dates, needed antecedent/subject, addressed recipient, qualification/caveat and method/example. Greetings and purely conversational acknowledgements are not record roots. A confirmation of a missing proposition (n11) is retained with an unresolved-reference note; do not invent its antecedent. Repeated identical observations are one semantic record with all original occurrence spans. Scope scaffolding is a modifier, not a new independent result. A premise can be preserved as a basis or a supplemental assertion, but the typed reason link is still required to make it usable as a rationale.

Every node has exact source offsets/quotes and material-token anchors. Negation, modal verbs and numbers remain material; articles/pronouns/prepositions and auxiliaries alone do not determine identity. This fixes the prior `on Thursday`/`Thursday` scoring artifact. Anchor matching is ordered subsequence matching; it is a source-compatible diagnostic, NOT unrestricted semantic entailment or paraphrase judging. Full record roots may contain several coordinated objects of one predicate; named lists and units must remain. Caveats and methods are separate gold nodes even if the current schema carries them as additional claim spans.

Claim stance is per assertion, not automatically shared with its caveat: proposal+unapproved observation is legal. Store graph collapse to unknown is separately visible. Reason links that the author does not explicitly establish but that are plausible are optional inferred links; absence is not penalized. No link from mere proximity is required. Required bases are source-stated; qualification labels (stated/inferred/unspecified) are reported separately because current source-graph schema can leave them unspecified.

Source provenance consists of source ID, owner, speaker, observed_at, location, source hash and original intervals. Author metadata is not an @recipient or authenticated approval. `unresolved` gold notes are not fabricated resolved subjects. The current output schema has no explicit unresolved-reference flag: this benchmark can detect invented fills but cannot claim to measure that unsupported flag's recovery.

## Metrics and failure accounting

Report raw and compiled records separately, and balanced synthetic versus natural separately. Report9-cell strata and document-macro recall alongside micro counts; do not allow many noise facts in hard documents to silently dominate one pooled score.

- Required information-node recall: claim/context content appears somewhere in extraction, independent of correct binding. This is a location diagnostic, not correctness of a record.
- Record-root recall and precision proxy: source-compatible roots recovered; unsupported/non-root claim rows count as surplus predictions. Supplemental grounded reason/caveat/method assertions are not automatically extra roots. The matcher can flag legitimate split fragments; preserve per-row errors for adjudication rather than silently promoting this proxy to semantic precision.
- Typed edge P/R/F1: `(record, role, context-node)` triples. Condition-as-reason, method-as-condition, a right quote attached to the wrong record, and context without a target produce FP/FN. Same role/quote under two real targets is allowed only when both are gold. Inline caveat/method/recipient links may be encoded in claim text; condition/basis/time/anaphoric subject require their contracted roles.
- Extra unmatched rows, boilerplate mixed into valid rows, exact repeated output rows and overmerged independent-record pairs. Overmerging is scored even if a giant group preserves every source word. Correct text alone must not grant perfect quality.
- Assertion stance accuracy/missing count without raw group collapse; compiled-group unknown can lose assertion distinctions.
- Exact quote fidelity separately from semantic anchors; source metadata equality, graph validation and previously measured actual store/reader transport. Exact quote validity does not prove correct semantic attachment. Raw repeated quotes without offsets remain provenance-ambiguous; compiled graphs expose actual intervals.
- Document complete requires all required nodes/edges, no incorrect edge, no extra root/row/boilerplate/duplicate/overmerge, valid per-assertion stance and exact output quotations. It is strict and not the only reported score. Unspecified basis qualification and unsupported unresolved flags are reported as separate coverage limitations, not hidden as fully solved.

All scores retain missed nodes, extra rows and wrong triples for review. No model judge trained on this gold. Gold/schema/scorer changes after scoring require a new version, not an improved number in place.

## Verification before scoring

68 complete gold-oracle records must pass. Deliberate mutations must detect omission; a flat full-sentence copy with no typed links; unsupported new assertion; condition/reason swap; correct quote under wrong target; unrelated records merged; valid per-assertion stances collapsed; method mislabeled condition; removed negation; and harmless temporal preposition variation. These are evaluator checks, not model benchmark results. Validate all gold spans and unchanged input strata.

## Reporting boundaries

The entire supplied document is annotated under this policy, including distractors and nonfocal facts. This broadens beyond the old focal probes but is not a claim of universal/service-level records quality. Single-agent annotation, source-anchor matching, synthetic templates and prior exposure remain limitations. Do not choose a new production design from one total score, and do not relabel failures to favor either arm.

## Evaluator v2 correction

The first scorer incorrectly counted source-valid fragments of one same-group assertion as extra claims, even when their concatenation preserved the complete assertion. Example: `The proposal is approved` + `can be finalized`. This is an evaluator defect, not a proposed model improvement. v1 gold/scorer snapshot and scores remain under `results/record-full/v1/frozen/` and its evaluation.json. v2 uses contributing source-compatible fragments for content, stance and inline links.68 source-derived split-span invariance tests now pass, alongside68 whole-oracle cases and10 deliberate mutations. Gold and inputs are unchanged. Freeze v2 before rescoring; explicitly retain prior-output exposure status.
