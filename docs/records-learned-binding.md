# Conditions and reasons: learned binding reference audit

2026-11-15. Scope is records only. This is an opt-in candidate under evaluation,
not a new default and not a claim that QA has improved.

## What actually makes the reference bind fields

Pinned implementation: [GLiNER2 c379245](https://github.com/fastino-ai/GLiNER2/tree/c379245ce9fe0fee03a530a320ddb1885847c4d6).
Pinned checkpoint: [GLiNER2.5-base 07d99c0](https://huggingface.co/fastino/gliner2.5-base-v1/tree/07d99c0ba5d15cb3b24e0a236fa99bdd4ef87a5c).
The paper commonly cited as GLiNER2 describes the earlier family; the specific
instance-assignment implementation inspected here is the boundary/2.5 path.
Do not attribute all this newer code to the earlier paper's experiments.

1. The schema and original document condition an encoder. A learned boundary
   proposer supplies candidate spans and their representations. Schema strings
   alone are not a parser that recovers arbitrary source relations.
2. [RecordHead](https://github.com/fastino-ai/GLiNER2/blob/c379245ce9fe0fee03a530a320ddb1885847c4d6/gliner2/models/boundary/records.py)
   creates one natural-mode instance per anchor and scores each field candidate
   **against that instance**, using trained parameters. Latent/anchorless modes
   use different instance formation; we do not silently switch between them.
3. Scalar fields can choose an explicit ABSENT column. Multi-value fields use
   independent sigmoid assignments, so an empty set represents no selected
   field. Non-exclusive fields can attach to several instances; exclusive
   fields impose an ownership constraint. Our reasons/conditions are optional,
   non-exclusive lists because shared evidence is allowed.
4. The decoder consumes those scores and cardinality constraints. We use the
   checkpoint's 0.5 threshold without selecting a threshold on the 68 cases.
   Returning a source span establishes where it came from, not whether the
   selected condition/reason is semantically correct.
5. [Training losses](https://github.com/fastino-ai/GLiNER2/blob/c379245ce9fe0fee03a530a320ddb1885847c4d6/gliner2/models/boundary/model.py)
   combine candidate/span objectives with record existence and field-assignment
   supervision. In `compute_dense_batch_loss`, scalar assignments use a
   normalized choice loss and list assignments use binary cross-entropy.
   Natural anchors match gold anchor instances; latent sets require instance
   matching. Copying `RecordSpec` without these trained parameters is not reuse
   of the learned capability.

The selected checkpoint config has `enable_records=true`, a shared candidate
pool of 192 and `max_len=4096`. Its card states that records were trained; it
does not establish that our complete-proposition anchors and distinction
between applicability and stated rationale were covered by training data.
This is therefore a task-transfer experiment, not a verified same-task model.
The first stage measures this transfer without fine-tuning. Its failure is
preserved separately from the supervised adaptation described below.

## Why not transplant other references

- UIE's [SEL parser](https://github.com/universal-ie/UIE/blob/main/uie/extraction/predict_parser/spotasoc_predict_parser.py)
  reconstructs predicted spot/association structure. The association is learned
  during the upstream structured extraction training; the parser cannot decide
  which of our existing claims a reason belongs to. Its trained checkpoint,
  schema and task representation would need separate compatibility validation.
- LangExtract's exact aligner is retained for source grounding. It does not
  classify a rationale as a condition or resolve which instance it explains.
- LlamaIndex item validation checks shape and allowed relation types. It does
  not supply a trained claim-to-context assignment model.

## Adapter boundary

`team_memory.records.learned_binding.predict` calls the native pretrained model
on the full original document. It receives no existing annotations or gold.
`bind` joins native anchors to **exact existing Qwen assertion offsets**. This
join handles identity only; it makes no semantic or nearest-neighbour choice.
A shorter entity/predicate anchor is skipped instead of being stretched to a
proposition. Multiple native instances mapping to one existing group are also
skipped. These skips are measured because preserving old answers by never
applying a candidate is not evidence of a successful fix.

For an unambiguous match, only condition/basis fields are replaced. Assertions,
their stances, time and subject remain fixed. A native empty field is evaluated
as deletion, not concealed by falling back to old correct links. Structural
failure retains the original graph and records the reason; semantic failure
is scored normally. Explicit model inference does not authorize approval or
team-state mutation. The adapter is not automatically enabled in the service.

## Fixed acceptance and diagnostic boundaries

Same 68 sources, same cached Qwen outputs, same v3 gold/scorer and difficulty /
evidence-availability distribution. Compare to the previously accepted
per-assertion storage path, including prior correct content, links, stances and
whole documents. Require no losses and no increase in false links or extra
extractions in either panel, plus at least one correct new target link.

Report upstream native extraction, anchor-join coverage and stored graph quality
separately. RecordHead execution is instrumented; strict checkpoint loading and
actual trained head keys are recorded. All model work is on a Slurm compute
node using the existing conda base and an isolated dependency environment.
The new checkpoint stays in the project's `checkpoints/`; no existing datasets
are replicated. Runtime packet excludes gold and scoring code.

[Frozen protocol](../evaluation/record_binding/PROTOCOL.md)
and [results directory](../results/record-binding/v1/).

## Supervised adaptation and two implementation traps

The unadapted checkpoint executed its actual record head 68 times, but produced
only five condition fields and four basis fields across 65 native records.
Only 14 anchors exactly joined existing Qwen assertions. Replacing their fields
lost three previously correct links without gaining a correct new link. The
native candidate was rejected before adaptation; its results remain intact.

One additional run uses the upstream trainer and losses, not an imitation head.
240 synthetic training documents and 80 development documents use disjoint
domain families. Both sets are separate from the fixed 68 evaluation sources;
their generation uses no benchmark gold. The evaluation source comparison
found no exact-document or seven-token overlap. Because templates are shared
between training and development, the development score measures learning the
limited attachment grammar; it is not natural-language generalization evidence.

Two details of the inspected implementation affect this use:

- `DataLoader_Factory._validate_records` validates through a sanitizing
  `InputExample.from_dict(...).to_dict()` round trip. That round trip does not
  retain the explicit per-field `record_metadata.fields`. We validate every
  example without mutation and use the upstream raw `ExtractorDataset` with
  sanitization disabled. The processed natural anchor and list cardinalities
  are asserted before training. This preserves supervision rather than
  bypassing validation of invalid data.
- `_record_loss` is added only while `model.training` is true. Consequently the
  default validation `eval_loss` is not a direct measure of instance binding.
  The upstream trainer's `compute_metrics` callback runs real extraction on the
  separate development documents and selects by exact anchor/typed-field F1.
  Actual field loss, nonzero record-head gradients and changed weights are
  recorded. Six epochs and one configuration were fixed before the run.

The upstream single-task structure-drop augmentation is set to zero, so it
cannot remove the only supervised task. Its field-order shuffling remains.
Encoder LR 1e-5 and task LR 5e-4 follow upstream defaults; this run uses FP32,
batch eight, seed42 and the default candidate injection schedule.

Separately, the positive-only adapter treats absence as lack of a new proposal,
not evidence that an old binding is false. It adds explicit source-grounded
links and retypes only the same interval for the same assertion when the model
positively assigns another role. Shared reasons are not deleted from another
assertion. Native/adapted predictions are each compared under both integration
policies, without selecting an arm per document. The acceptance gate is unchanged.
