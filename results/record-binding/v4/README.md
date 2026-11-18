# Fixed-span binding: reject the new classifier; retain the endpoint contract

**Decision: do not enable this classifier.** It retains old correct records but
adds many incorrect relations. The assumption that loss of target identity was
the main cause of the recent errors is not supported by this experiment.
`preserving.py` remains the accepted evaluation baseline. No gateway/service
default was changed; the gateway still accepts an explicitly supplied builder.

## What changed and why

The earlier learned adapter converted an exact anchor span into `claim_group`.
A group may contain multiple assertions. That representation cannot preserve
which assertion was selected. The earlier Qwen alternative also regenerated
the context quote while selecting the group, sometimes returning the entire
assertion as its own context.

This candidate fixes both endpoints before classification. The same Qwen3-8B
receives the full original source and metadata; for each context passage it
assigns `none`, `condition`, or `basis` to each candidate target. A context request
contains multiple targets; this is **not** 1,192 independent model calls.
There are 263 calls containing 1,192 directed pair decisions. No training,
larger model, new semantic validator, or new evaluation examples were used.

New `records.graph/v4.context_bindings` retains the exact target and context
offsets. Original groups, assertions, stances, units and legacy edges stay intact.
The graph is an immutable JSON representation, not a new graph database.
The atomic endpoint contract and reader support are implemented and tested;
the automatic relation producer remains experimental and disabled by default.
The historical `learned_binding` path is kept for reproducing earlier results,
not presented as repaired or adopted.

See [the implementation audit](../../../docs/records-pair-binding-audit.md)
for pinned GLiNER2, Graphiti and PAIE code and their actual learning assumptions.

## Fixed results

Same 68 documents: 54 balanced synthetic and 14 previously seen natural audit
documents. Gold, matching/scoring rules, difficulty and evidence-availability
distribution are unchanged. Seven original storage failures remain failures;
the candidate ran on the other 61 documents.

| Representation / decision | Correct typed links | Incorrect typed links | Fully correct documents |
|---|---:|---:|---:|
| Accepted baseline | 44 | 26 | 27/68 |
| Fixed-pair predictions, exact target persistence | 52 | 380 | 13/68 |
| **Same predictions**, group-wide persistence control | 54 | 317 | 13/68 |

These are the unchanged scorer's **typed relation counts**, including wrong
types and unbound targets. They are not counts of independent false model
decisions: a quoted span can match multiple semantic units. The group-based
scorer requires each atomic edge to be rendered as a target/context view;
coarse group merging can also collapse several wrong predictions. Therefore
380 vs 317 is not a pure estimate of how many errors group broadening creates.
It does show that exact identity preservation did not cure relation selection.
Raw output examples below independently establish real semantic errors.

| Panel | Baseline TP / FP | Exact target TP / FP | Group control TP / FP |
|---|---:|---:|---:|
| Synthetic 54 | 34 / 19 | 40 / 206 | 41 / 165 |
| Natural audit 14 | 10 / 7 | 12 / 174 | 13 / 152 |

All 283 previously matched required content units, 44 previously correct typed
links and 187 correct stance units remain correct. However, new errors spoil
**14 previously complete documents**. Thus preservation of isolated old answers
is insufficient: neither arm passes the fixed adoption gate.

The physical baseline representation remains 192 groups, 231 assertion entries
and 657 source units in both baseline and atomic candidate. No physical assertion
was newly extracted or deleted. The scorer's extra-row increase includes repeated
target views of incomplete/irrelevant extracted spans; do not call these newly
stored assertions. They still expose unsuitable target candidates and do not
make the new wrong relations acceptable.

## Where errors originate, using actual model output

- **e01-partial:** `For chilled parcels, use liner K6.` The existing condition
  was correct; the new model additionally labelled `For chilled parcels` a
  **basis** for `use liner K6`. Both endpoints are present, short and correct.
  This is role misclassification before storage, not a retrieval or offset error.
- **e03-full:** `the seal failed inspection` was additionally called a
  **condition** for the shipping prohibition, although it is the stated reason.
  The correct old reason remains, but the extra relation spoils the document.
- **n03:** the future document-storage need correctly supports comparing Blob
  and S3. The model also attached it to starting the task, evaluation dimensions,
  and the next-week report. The new correct reason is accompanied by unsupported
  target generalization already present in the raw JSON.
- **n12:** `to ensure the charts render correctly` was labelled **condition**
  for the static-integration plan and **basis** for unrelated dynamic-refresh /
  WebSocket plans. It also treated `Received, thanks a lot!` as a reason for the
  data-structure observation. Exact quotes and IDs cannot fix these choices.
- **n13:** the reduced-pressure reason was recovered for polling, but the
  document still contains other wrong new relations. This is not a solved case.

The model returned 320 positive pair labels (120 condition, 200 basis) and 872
NONE labels. Twenty-seven positives duplicate existing relations; 293 new edges
were persisted and all 293 retained their exact endpoints in reader packets.
The raw-output failure is therefore not an output-format or silent-binding loss.

Eight new required condition/reason links were recovered across six documents:
m03-full, h02-partial, h03-full, h03-partial, n03 and n13. There was no casewise
selection or selective deployment of these successes.

## Candidate quality is a separate limitation

Using the unchanged token matcher, both selectable endpoints exist for 38/54
required synthetic condition/reason links and 5/13 natural links. This is a
diagnostic of this **frozen extracted-span catalog**, not an oracle recall claim
about raw documents. In natural records:

- n07 has failed original storage (four required links unavailable).
- n09 lacks a single complete selectable target matching the fixed target.
- n04, n10 and n12's conditional WebSocket plan have the qualifier only inside
  the whole target span, without a separate selectable qualifier.

Using every earlier extraction as a possible endpoint also introduces greetings,
fragments and other non-assertions. References relying on suitable entity/trigger
instances or supervised field assignment do not justify that substitution.
Our failed zero-shot enum classifier does not acquire their learned assignment
ability just by using endpoint IDs.

## What to retain

1. Retain explicit assertion/context identity, source offsets and unverified
   qualification as an opt-in storage contract. Do not broadcast a selected
   target to its group. Existing v1/v2/v3 behavior remains compatible.
2. Reject this all-span Qwen classification path. Do not add filters for the
   observed phrases or adopt only its correct rows.
3. Treat instance construction and typed/no-relation assignment as distinct
   prerequisites for the next design. A suitable learned reference must supply
   both appropriate targets and negative/role supervision; its input schema
   alone is not enough. This result does not prove that Qwen universally cannot
   solve the task, or that larger models/training automatically will.

## Verification and cost

- Slurm job **123016**, aurora-g8, **COMPLETED / 0:0**; program complete, 68 rows.
- Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`;
  GPU1 / CPU8 / 48G / conda, 12h walltime limit, no requeue.
- Actual allocation **773 seconds = 12.88 GPU-minutes**, including setup;
  inference driver **180.81 seconds**. Preparation includes checkpoint integrity
  verification and model startup. No dataset/model copies, paid API or training.
- 263 actual request bodies and raw responses verified against frozen inputs;
  192,251 prompt tokens and 14,648 completion tokens.
- All 68 baseline scores reproduced; 204 append/restart/reader transports passed.
  All 293 newly persisted bindings retain their selected endpoint quotes.
- 114 local contract/regression tests passed. The 68-document no-new-edge
  preflight exactly reproduces baseline scores; all 1,192 permitted endpoint
  combinations pass structural validation and group-control projection.
- One **pre-scoring, pre-output-inspection** compatibility amendment repaired
  the group control: its initial code used an unsupported `evidence_quote`
  attribute. The control now applies the identical offsets to existing group
  units directly, without a second extraction/alignment. The original freeze
  and amendment hashes are preserved. Runtime, primary arm, gold, scorer and
  acceptance criteria did not change.

This is records evaluation. No new end-to-end QA accuracy claim is made.

Artifacts: [fixed protocol](../../../evaluation/record_binding/PAIR_PROTOCOL.md),
[freeze](pair-freeze.json), [scores and protection](pair-evaluation.json),
[all cases and selected quotes](cases.md), [raw model calls](record-pair-123016.calls.jsonl),
[candidate availability](candidate-coverage.json), [execution](execution.json).

Replay from repository root:

```bash
NLTK_DATA="$PWD/.cache/reference-nltk" .venv/bin/python -m evaluation.record_binding.evaluate_pair 123016
NLTK_DATA="$PWD/.cache/reference-nltk" .venv/bin/python -m evaluation.record_binding.pair_diagnostics
```
