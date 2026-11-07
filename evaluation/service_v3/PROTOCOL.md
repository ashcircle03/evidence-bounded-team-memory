# Frozen source/state citation and reader comparison

2026-11-08 KST. Freeze before any new model output is observed. No semantic code,
prompt, key or score rule changes after freeze. Execute once, retain all failures,
and make an engineering decision; do not extend experiments to obtain a win.

## Question and arms

Does the existing document judge + bounded rewrite + AQA repair earn its extra
cost once source/state citation infrastructure is shared?

- direct: existing dense/BM25 RRF retrieval (team streams), the SAME initial
  CitationQueryEngine prompt as attributed, and the SAME LangChain exact-quote
  attribution. No document judge/rewrite/AQA repair.
- attributed: current service with those three optional stages.
- same Qwen3-8B pinned revision, nonthinking/temperature0/context32768/output1024;
  judge output384; same source packets, initial generation prompt, review states.
- timeline direct reconsideration is shared, run once per incoming record and
  given identically to both arms. Thus no claim of relative reconsideration gain:
  measure absolute supported proposals, wrong relations and unnecessary alerts.
- Natural QA uses whole-topic BM25 top8/512/64 for Ever and supplied context pairs
  for Wiki. Identical retrieved packets are given to both reader arms. This tests
  the reader, not end-to-end deployed hybrid search or official full benchmarks.

## Inputs and separation

1. Known development: two recorded pending/current responses from120359. Preserve
   their exact answer bytes and existing original citations; only add quote
   citations backed by persisted proposal/vote snapshots. 2 new attribution calls.
2. Existing legacy20: exact physical-response replay, plus fresh same-passage
   direct/attributed inference on all20 (reader regression; not full new retrieval).
3. New natural QA: Ever topics03/04, one each F_SH/F_MH/F_TP (6). Select min SHA256
   of `service-state-v1:`+ID per type/topic. Wiki6 min hashes excluding every ID
   in the prior claims-v3 keys, paired contexts only. Preserve official answer/
   source keys outside model messages. Never use keys for retrieval or selection.
4. New synthetic streams in streams.json:8 distinct sequences. Same-condition
   pending/approved/rejected corrections, history, different-condition coexistence,
   unresolved conflict, two changed-decision-rationale positives, two topical
   near-miss negatives. They are authored controlled tests, not natural Git cases
   or independent random samples. Approval actions are scripted fixture-owner acts.
5. Compute selected IDs, original data hashes and exact retrieval packets BEFORE
   model evaluation. Model runner never reads evaluator-only expected answer fields.

## Scores (kept separate)

- QA answer correctness: all required values/actors/conditions/temporal status,
  and no materially unsupported added assertion. Missing a required side fails.
- QA source support: each required factual answer has a citation whose actual
  quoted original supports it; literal/offset validity alone is not entailment.
- State citation: approval/pending/rejection claims linked to the matching exact
  proposal snapshot and valid owner votes (pending is a snapshot, not an event).
  Report absence and incorrect binding separately, including already-numbered
  sentences that still cite the wrong evidence type. `ok` is not a gold score.
- Existing20: exact replay retention separate from fresh semantic support and
  regressions against the old expected answers; no fresh20/20 claim from replay.
- Reconsideration: correct target+kind+old decision/reason+changed incoming condition
  with literal original evidence; unnecessary alerts on negative streams separately.
- Costs: physical calls/tokens, QA and shared update separately, paired latency,
  full Slurm GPU minutes including preparation/failures. No speed inference across
  hardware, no inference-cost benefit from shared cached evaluation drafts.
- Implementation-agent source review with per-case reasons; not independent human
  evaluation. Blind labels used for review, identity revealed only after ratings.

## Precommitted adoption gate

Keep the optional attributed stages only if on NEW QA:
(a) at least2 more answer+source-supported successes than direct,
(b) no case correct/supported in direct is lost,
(c) no added incorrect review-status/approval assertions,
(d) attributed total QA physical calls <=2x direct total.
All four are engineering gates, not statistical significance. Otherwise select
simple direct as the provisional deployment profile. Report remaining failures
and do not claim task completion/generalization. If direct has fresh legacy
regressions, retain attributed as compatibility profile for those existing uses,
without case-ID routing. Unresolved evidence means no global replacement claim.

## Reference intent

Reuse LangChain FactWithEvidence/substring_quote schema already vendored. Extend
its candidate evidence pool to typed, deterministic views of existing timeline
proposal/vote records, not model-created status labels. W3C PROV-DM's distinction
between entities, activities and responsible agents informs source vs review
provenance (https://www.w3.org/TR/prov-dm/); this is not a PROV implementation or
claim that PROV solves semantic QA. No new judge or learned status classifier.

## Execution correction before final freeze

Development120369 was Slurm COMPLETED/0:0 but not an attribution success:2
request attempts,0 model responses. The new harness used httpcore's reserved
`trace` extension name. Replace it with the project-specific key already used
by prior runners, and test through real localhost transport. No semantic actor
change. Run the two known attribution cases first in the same allocation as
final evaluation to avoid repeated model loading; if either remains incomplete,
abort BEFORE any new case generation. Final cases and actor are already frozen.
