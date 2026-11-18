# Causal records repair, v1

Freeze existing full-record v3 gold/scorer and 68 source documents. Never relabel
failures. Keep synthetic 54 and natural audit 14 separate. No QA generation.

## Sequential storage fixes on exactly the same actual Qwen outputs

Control: old grouped outputs from job122970, not the rejected bound prompt.
These are the 68 original Qwen3-8B outputs, with no model re-generation or gold
inference. Compare three storage paths on each exact raw response:

1. Original compiled graph (cached and reproduced).
2. Same grouped compiler with per-extraction assertion attributes retained.
   All failures still fail the document as before. No prompt/schema change.
3. Step2 plus item-level rejection. Invalid context is quarantined; other exact
   spans survive; a group without an accepted claim is not reparented. Repeated
   context stays unresolved; do not select its occurrence with gold or proximity.

Both fixes must preserve every previously correct required node, typed edge,
stance and complete document, relative to the old path and the preceding step.
Report FP/extras and both panel F1, not just retained recall. Adding valid raw
rows to previously empty graphs can expose pre-existing wrong relations: report
that explicitly, not as a successful semantic repair. No per-case choice between
outputs. Store/read/reader transport is checked for every document and step.

## Input-boundary diagnosis

Bound job122986 is a rejected alternative, not a replacement control. Audit its
actual prompt/schema/output and stored graph separately. A sentence ID is a
location hint, not proof of a semantic boundary. If a fresh generation comparison
is needed, change only the source-window granularity (one full original document
versus sentence segments), keeping the existing instruction/examples, model,
decode settings and output schema structure. Freeze that packet before running;
do not simultaneously change exclusions, ontology, examples or postprocessing.

## Interpretation

Cached actual model-output replay is the strongest isolation for storage bugs;
it is not a fresh Qwen run. No claim that semantic attachment/omission is fixed
by a storage repair. Review original-source-preserved versus annotation-complete
separately. Reference code support must name its operating assumptions and what
it cannot establish for our task. Do not add a checker or semantic heuristic.
