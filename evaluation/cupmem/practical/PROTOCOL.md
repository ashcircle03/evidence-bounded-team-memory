# Paired acceptance protocol

This protocol is written before inspecting the practical development model
results. Code and final data get additional hash freezes before final inference.
The user objective remains authoritative; this file defines how its gates will
be measured, without asserting that they will pass.

## Arms and inputs

Use the same pinned Qwen3-8B, local vLLM settings, input source collection,
original embedding model, top4 sentence hits expanded to original documents,
context/output bounds and single GPU allocation conditions in both arms.
Alternate arm order across streams. Both share `core.answer_question` plus the
same temporal/approval policy. No completed-answer cache, no human claim labels,
no private gold snippets in actor input, and no native intermediate answer in QA.

- Simple: retain original sources, retrieve, use existing `compare_records` for
  new-record proposals, and the shared cited reader for QA. It performs no CUPMem
  writes; report that lower ingestion cost explicitly.
- Candidate: official CUPMem writes; add native profile candidate origins and
  status-cause sources for review, then structured source-role review of each
  retrieved old-source/current-incoming pair (at most8). Store
  original records and owner votes separately. Factual QA uses original retrieval
  and actual team review links, not the native premise adjudicator.

Native retrieval/write implementation remains pinned, but this is a changed
query orchestration. Do not label it unchanged CUPMem or a SpeakerMem-R1 result.

## Panels and scoring

1. Existing development stream: all five Cedar QA checkpoints, the unrelated
   report and source/approval state. This panel may guide development and is not
   independent generalization evidence. All answers and citations must remain.
2. Legacy regression: exact historical20 questions, seven full source collections
   in original order, including original question/as_of values. The evaluator
   retains original aliases, evidence-source groups and source provenance, never
   passes them to actors. Report corpus-specific counts: Git, PEP, controlled,
   natural EverMemBench. An answer succeeds only when the required content and
   conditions are present AND the cited original passages support them. Correct
   content retained with a formatting warning can succeed; malformed/unsupported
   extra substantive answers cannot. Inspect original passages, not aliases alone.
   Lost successes are cases where simple succeeds and candidate does not. Target0;
   report absolute scores as well so a weak shared baseline cannot hide behind0.
3. New transfer:20 source-grounded streams,10 needing reconsideration and10 not.
   Exclude previously used source events using original locations/commit IDs and
   content hashes. Retain the original source text. Identify controlled pairings
   and number of independent follow-up reports; do not claim20 independent natural
   histories if inputs are paired constructions. Freeze actual targets, premise
   changes, witness spans and unrelated-topic distinctions before final inference.
   Positive success requires a reconsider proposal with the correct old decision,
   changed relevant condition, source evidence and supported explanation. Source
   presence alone is insufficient. Required reconsiderations target>=8/10.
   Any consequential proposal on a negative counts as unnecessary: target0/10.
   Report additional wrong-target/wrong-kind proposals on positives separately.

All semantic ratings include a reason and actual quotes. Rating uncertainty is
reported and does not silently become success. No new source-specific aliases,
semantic exceptions or input repairs after seeing final outputs. Ambiguous cases
are resolved or excluded with reasons before the final data freeze, not afterward.

## Mechanical and cost gates

Verify Slurm COMPLETED/0:0, program completion, exact code/input hashes, physical
call logs, required case/arm/event coverage, original source preservation, query
scope, actual generated output binding, and source IDs/offsets in actual inputs.
AI proposals stay pending; only an explicitly simulated original-owner review
may approve. A new operating condition is not a retrospective correction.

Count physical model requests, including native writes and repair calls. Separate
ingestion and QA cost. For first-time questions in each state, candidate mean QA
calls must be<=4.5 (half of service-v1's9) while quality gates hold. Report token
counts, per-operation warm latency and total allocated GPU time; startup and
embedding work are not free or silently attributed to other arms. Repeated
checkpoints are also reported, not substituted for first-time questions.

## Decision and deliverables

Run the frozen final comparison once. Choose the supported implementation and
mark unmet gates explicitly. Do not declare general benchmark success from this
small panel. Deliver the callable module, API/state/failure specification, usage
example, exact outputs with citations, per-case ratings and actual resources.
No automatic extension to more final experiments, new models or UI work.
