# Reference composition audit v1 — frozen before submission

Date: 2026-11-14. This is a **development diagnosis**, not a new benchmark or
paper reproduction. Production code, storage and retrieval are not modified.

## Questions

1. Does whole-response judgment hide erroneous subclaims under partial support?
2. Does placing the existing AQA prompt before any contradiction/source-coverage
   gate preserve answer/source alternatives better, at lower cost?
3. Do changes preserve ordinary answers, exact evidence, condition distinctions
   and review authority? Does claim decomposition itself lose qualifications?

## Inputs and isolation

- All 37 QA packets from module-boundary/v1, plus all 8 supplied-correct-relation
  packets from comparator-choice/oracle-v1: 45 packets, no outcome-based subset.
- Legacy20, observed-state17, supplied-correct-relation8 are separate strata.
  Several questions share a story; they are not 45 independent observations.
- Reuse exact witness text, source IDs/order, author/date, review snapshots and
  recorded review_context. Hash the full evidence/context object per packet.
- Wrong upstream relations in the observed-state stratum stay wrong. The oracle
  stratum isolates downstream QA with a supplied correct relation. Neither is a
  new retrieval, ingestion, approval-authentication or end-to-end benchmark.
- Produce one fresh ordinary draft per packet with the existing citation QA
  template and state template. All post-draft arms consume that exact draft.
  Frozen packets bypass CitationQueryEngine retrieval and CompactAndRefine;
  do not claim this is an exact replay of their original generation requests.
- Qwen3-8B revision b968826d9c46dd6066d109eabc6255188de91218, BF16, TP1,
  temperature0, seed42, thinking disabled, 32768 context, answer/decomposition
  budget1024. Document judge retains the upstream4096 completion budget.
- No gold or previous model answer is included in model packets. Gold stays
  local. No provider fallback, training, new model or semantic special cases.

## Four conditions

| Arm | Changed component | Preserved components |
|---|---|---|
| direct | No document judge/rewrite/AQA | Shared draft; current quote attribution |
| current | Current production review and conditional AQA | Shared draft, state masking, original judge, revision prompt, citation |
| aqa_first | Existing AQA prompt generates directly from the same evidence, without draft gate | Same existing one-shot example, state policy, answer budget, citation |
| claim_review | ConflictScore Table10 claim decomposition before existing per-document judgment | Shared draft, judge prompt, state policy/masking, any-contradiction revision trigger, revision prompt, conditional AQA, citation |

The AQA condition isolates placement, not author demonstration selection or
fine-tuned weights. The claim condition isolates granularity, not the original
TruthfulQA multiple-choice R-RAG setup. CS-C/counts are diagnostics, not the
adoption objective. Do not strengthen partial support, change thresholds, or add
another verifier after looking at these outputs.

Every arm uses the same existing exact-quote citation adapter. Pre-attribution
answers and final answers are both retained. An already cited sentence is not
rechecked by that adapter; measure this limitation, do not call it entailment.

Rotate arm order by packet index. Log every physical HTTP request/response,
finish_reason, usage, full prompt and per-arm time. Record shared-draft hashes.
Repeated identical requests still count as real calls; no hidden cache replay.

## Scoring and decisions

Existing answer/evidence keys and manual ratings are copied with hashes into
the local result folder before submission. Use their semantic requirements,
not just answer keyword presence. Case provenance maps each new ID to its key.

For each arm/case record: answer correctness; every required answer/source pair;
original-report citation correctness/completeness; state citation correctness;
conditions preserved; correction vs reconsideration semantics; unsupported
added claims; unwarranted abstention; protocol/parse/truncation failure. Inspect
claim decomposition for lost author/condition/negation and judge rationale
against the actual source. Missing ratings stay null, never count as success.

Blind shuffled cards omit arm names. Read question, input evidence and output,
then compare with the frozen key. One reviewer is not inter-rater validation.

Retain production unless a candidate:
1. preserves every legacy answer/evidence success of the historical baseline
   AND the fresh current arm;
2. preserves existing state-answer/citation successes and introduces no new
   approval/fact-change authority violation;
3. improves at least one failed complete answer/source case, without worsening
   that stratum's complete success count;
4. costs no more than 2x current physical calls and reported generated tokens.

Report paired changed cases and all strata, not just a pooled score. An arm
that improves detection but corrupts answers is not adopted. Failure of all
arms does not authorize a new module or further experiments in this protocol.
Keep source retrieval/state storage and exact-provenance boundaries; identify
which existing boundary requires a separately justified change.

## Execution

GPU1 CPU8 RAM48G, Slurm batch_ugrad/ugrad, account QOS, no-requeue,12h wall.
Bound client3h, startup15min, at most2000 physical calls; no automatic extension.
Use the existing shared project checkpoint directly; no model/dataset copying
to other nodes. Packets are small explicit experimental inputs. NLTK tokenizer
runtime resources are reused from the already prepared g8 cache; no download.
Use g8 solely to reuse that existing runtime resource. If it is absent, fail
with an explicit error; do not silently recreate it on a different node.
Activate the existing conda environment. All remote Python/hash/inference run
inside the Slurm allocation. User's unrelated4-GPU job is not touched. Pending
GPU quota is not a failure or permission to bypass the account limit.

Completion requires Slurm COMPLETED/0:0, server/client completion,45 drafts,
180 successful arm outputs, unchanged packet/code hashes and trace verification.
An incomplete comparison cannot select a winner. Preserve all failed artifacts.
