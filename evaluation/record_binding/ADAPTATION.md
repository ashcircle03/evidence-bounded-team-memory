# One supervised adaptation, frozen before training

The native pretrained candidate failed: only 14 exact anchors were joinable,
no correct new target link was obtained, and field replacement deleted three
previously correct links. It is rejected. This motivates one task adaptation,
not a threshold search or repeated evaluation-driven prompt revisions.

Use the SAME pinned native code/checkpoint/schema and complete learned pipeline.
240 generated training sources cover 12 domains; 80 development sources cover
four disjoint domains. Ten explicit discourse patterns include missing fields,
scope before a claim, rationale before/after a claim, shared reasons and adjacent
unrelated claims. Modality has two variants. This synthetic grammar is limited;
the benchmark remains a development audit, not a new held-out claim.

No benchmark source, gold record or previous model output is used as a training
example. Audit exact texts and 7-token overlaps before submission. Training data
is versioned separately from the immutable 68-document evaluation. Store it on
g8 in `/local_datasets/pjw031003/capstone-shared-knowledge/record-binding-adapt-v1/`.

Use upstream ExtractorTrainer with encoder_lr=1e-5, task_lr=5e-4 (upstream
defaults), six epochs, batch eight, FP32, seed42. Select one best checkpoint on
independent development **actual anchor/typed-field span F1**, through the
upstream compute_metrics callback. Default eval_loss excludes the record
auxiliary loss in eval mode, so it is not the selection metric here. No second
training configuration is allowed after seeing the 68 evaluation predictions.

Before training, validate source spans without mutation. Avoid the upstream
sanitizing InputExample round trip that discards per-field record metadata;
verify processed natural anchor and list cardinalities. Require actual nonzero
record-head gradients, finite record-field losses, and changed record weights.
Use native candidate injection schedule/losses/decoder, not a hand-written loss.

Independently compare replacement vs positive-only integration on BOTH native
and adapted predictions. Empty predictions are missing information, not evidence
that an existing binding is false. Positive-only adds predicted links; a role
can change only when the exact same interval and assertion have an explicit
other-role prediction. It never deletes links to another assertion (shared
reasons are legal). No per-case choice between these arms.

The prior zero-regression/no-added-errors adoption gate remains unchanged.
Separate gains from supervised adaptation and integration policy. Do not adopt
a net-improving arm that loses protected content/links/states/documents. Preserve
all trial outputs; no new modules or further tuning after this comparison.
