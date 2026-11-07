# Demonstrated QA 固定 development protocol

Frozen before execution; same byte-identical connected-v1 inputs.json: legacy20 and EverMem10.
No question, answer, reference location or grading criterion changes. Exposed development only.

Candidate: original Attribute First first2 LFQA examples with all text, spans and sentence links;
AQA paper Figure1 paraphrase1 (NOT unavailable author 3-shot). No test-derived demonstrations.
Remove free-text purpose. Select literal spans, generate answers with explicit highlight IDs.
No new judge, training, posthoc answer rewriting or semantic rules.

- legacy20: candidate on exactly the prior fixed supplied sources. No end-to-end retrieval claim.
- Ever10 direct: same demonstrations, original top8, direct answer+citations in one call.
- Ever10 reader_only: select+aligned generate from original top8.
- Ever10 combined: same initial selection, up to2 retrieval rounds and reselect after new records,
  then aligned generate; retain original8, append at most16. Stop on no/new duplicate query or no new records.
- 50 final outputs, 80 to100 Qwen calls. Fresh direct control has same examples but no selector.
- Same pinned Qwen3-8B BF16, nonthinking, temperature0, max output1024, context32768.
  Record all model messages and original output; fail explicitly on context overflow.

Answer/evidence grading fields unchanged from connected-v1: answer_correct,
returned_evidence_supports_all_claims, required_evidence_complete,
narrow_quotes_support_all_claims, unsupported_extra. Success = first3 and no unsupported_extra.
Review every returned claim against original records. Literal citation match is not semantic support.
Use existing frozen keys. No new evaluator model. Implementing AI review, not independent human.

Adopt only if legacy20/20, combined>3/10 and >fresh direct, all prior successes retained,
and no new format/source contract errors. Otherwise keep current selected attributed profile.
Show source selection versus reader error and direct costs; do not claim same-token comparison.
Historical attributed20/20 is prior response replay, not a fresh call in this job.

No prompt changes, new examples, repair or extra experiment after seeing outputs.
Verify SLURM COMPLETED/0:0, program complete, all hashes and exact request/output replay.
Review all50 once. Synthetic legacy and natural EverMem remain separated; no merge benchmark claim.

GPU1 CPU8 RAM48G explicit conda, no node pin, no-requeue, walltime12:00:00 per latest user policy.
No locally invented cumulative GPU caps. Global user limits remain4 running/8 active+pending/4GPU.
All remote compute, cache preparation, dataset traversal, hashing and inference on Slurm nodes.
