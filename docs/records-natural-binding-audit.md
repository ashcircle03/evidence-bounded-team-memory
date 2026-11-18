# Natural-record binding: coverage, model and integration audit

2026-11-16. Records only. Fixed gold/scorer. No additional training.

## What the instrumented model actually did

Job123008 ran the original and previously adapted GLiNER2.5 checkpoints on all
68 unchanged documents, recording native pool, anchor and assignment scores.
The public extracted spans/roles/edges reproduce all136 previous predictions.
Confidence floats differ in67 adapted outputs; these are semantic reproduction,
not bitwise-equal numeric execution. Raw predictions and scores are retained.
The source-only inference packet contained neither gold nor the scorer.

All13 required natural condition/reason nodes have a material-covering candidate
in the adapted pool; 11 have an exact gold span candidate. Covering spans can
be oversized, so 13/13 is not exact candidate quality. Only4 have a covering
candidate scoring at least0.5 and only4 have a selected matching target anchor.

Examples of separate failure mechanisms:

| Case | Native evidence after adaptation | Conclusion |
|---|---|---|
| n03 storage comparison | Exact reason exists; basis probability0.68073. Correct selected anchor exists. Its assignment probability to that exact reason is0.0000047. | Clear instance-to-field binding failure before integration. |
| n12 chart integration | Exact purpose exists, basis probability0.18052; selected integration anchor assignment0.0000055. | Both span role scoring and binding fail; a formatter cannot recover it. |
| n10 downstream notifications | Exact condition probability0.79172, selected target assignment0.02377. | Another assignment failure, despite a good source candidate. |
| m06 estimate scope | `reduced load` scores0.99461; assigned to procurement0.99312 and estimate0.86833. Full `under reduced load` scores0.11293 and estimate assignment0.00045. | Wrong target and incomplete boundary are separate errors. High confidence does not validate the relation. |

No confidence threshold was tuned. Simply lowering one threshold would not
repair the two failing gates or distinguish the wrong procurement target.
The instrumentation's default `truncated=false` marker is not used as measured
evidence of truncation; the diagnosis relies on observed source candidates.

## What is known about training coverage

Our prior training240/dev80 documents use exactly the same10 sentence templates,
with disjoint domain families. Character lengths: training median97.5/max161;
dev median103/max173; natural14 median299.5/max497. This is evidence of a
restricted transfer setup, not proof that length alone causes the failures.
Templates cover short when/if/for/because/therefore relations and explicit shared
reasons; they do not sample the open-ended discourse of natural team records.
Several condition targets omit their introductory words. That annotation
convention is not a guarantee of complete applicability clauses at deployment.
The m06 boundary error is consistent with this mismatch, not a demonstrated
causal effect of a particular training example.

The prior95.08% dev edge F1 therefore measures learning this limited grammar.
It does not establish natural-language generalization. We have inspected the
base checkpoint's public config/card, but its exact pretraining corpus coverage
of our task is not established. Do not invent an upstream training-data account.

The evidence supports **transfer failure in the current checkpoint/training
combination**, not a proven194M architecture ceiling. Establishing that ceiling
would require matched, independently sourced natural supervision and a model
comparison. No evaluation example or paraphrase was added to training here.

## What the references really provide

- [GLiNER2 RecordHead](https://github.com/fastino-ai/GLiNER2/blob/c379245ce9fe0fee03a530a320ddb1885847c4d6/gliner2/models/boundary/records.py)
  uses trained instance+field queries to score candidate representations.
  Nonexclusive list fields use independent sigmoid assignments; they permit
  shared evidence but cannot prevent wrong ownership without learned scores.
  The [decoder](https://github.com/fastino-ai/GLiNER2/blob/c379245ce9fe0fee03a530a320ddb1885847c4d6/gliner2/models/boundary/engine.py)
  also applies optional-field candidate probability gates. We ran both genuine
  components and inspected both gates rather than copying schema formatting.
- [PAIE](https://github.com/mayubo2333/PAIE/blob/1917c46db1498e6115aa40897790d6b36a9b83e2/models/paie.py)
  predicts argument boundaries with learned role-specific start/end selectors,
  trained against task argument spans with cross-entropy and optional Hungarian
  matching. Trigger/role prompts alone are not the trained capability. Its
  event-role ontology is not our proposition-condition-reason ontology, so its
  pretrained event checkpoint is not transplanted as a zero-shot rationale fix.
- [Graphiti edge extraction](https://github.com/getzep/graphiti/blob/3a8a78c997a07cceeb3411ede533b0f342d71c64/graphiti_core/prompts/extract_edges.py)
  supplies existing nodes, source episodes and typed relation definitions to
  the LLM. This avoids needing a second free-form extractor to regenerate
  identical anchors. Its current [edge operations](https://github.com/getzep/graphiti/blob/3a8a78c997a07cceeb3411ede533b0f342d71c64/graphiti_core/utils/maintenance/edge_operations.py)
  can materialize dangling endpoints; our adapter deliberately disallows that
  authority. This is a documented adaptation, not a claim that Graphiti itself
  guarantees endpoint rejection or semantic correctness.
- Existing LangExtract exact alignment remains the executed source grounding
  implementation. It verifies quotations, not the correctness of a relation.

## Candidate change and its limits

Replace the optional learned-binding candidate with one Qwen context-edge pass
over fixed existing claim IDs and the entire source. This does not stack both
GLiNER and Qwen binders. It reuses the original assertion extraction, source
store, exact aligner and v3 graph compiler. No new claim/approval/state authority.
Required context/evidence quotes must align and include the target assertion.
Absent proposed links do not delete old fields. Same-role contained fragments
can be replaced by a longer exact source span, without changing another field.

This directly tests whether the same8B backbone can read the missing relation
when anchor identity is supplied, at an additional inference cost. It is not a
controlled experiment proving which training distribution caused GLiNER's
failure. Its output is scored without semantic fallback or gold-based selection.

## First candidate result and explicit counterexample

The 8B pass (123009) passed source/schema/storage checks but failed semantic
acceptance: correct typed links44→52, false typed links26→128. Old283 content
nodes,44 links and187 stances survived, yet fully correct documents27→13.
The counts are fixed-scorer typed edges, not counts of raw proposed links.
Broad context quotations can create several wrong typed edges from one row.

In n03 the model recovered the source-stated rationale for comparing storage
services, but also linked it to the evaluation-dimensions assertion and treated
whole assertions as their own conditions. In n12 it returned the entire
integration-and-purpose sentence as a basis. A material-token scorer credits
the contained purpose link; this is not evidence of clean minimal extraction.
In m06 it again attached the estimate scope to procurement and called lack of
measurement a supporting basis. These are actual raw-output semantic failures,
not storage loss or a citation-format rejection.

Known target IDs therefore solve identity transfer, not semantic ownership or
source-endpoint typing. Our adaptation is incomplete relative to Graphiti's
two-distinct-typed-endpoint intention: the free context span can cover the
whole target assertion. Merely adding exact quotations is not a semantic gate.
This candidate is not installed as the default. Do not cherry-pick n03/n12.

A separately frozen follow-up changes only the relation-generation model to
existing Qwen2.5-14B-Instruct; messages, source, claim IDs, JSON schema, decoding
budget and scorer stay the same. Qwen2.5 versus Qwen3 also changes model family,
so this compares available models, not a pure parameter-count scaling law.

The completed14B run123011 produced55 correct/103 false typed links and13
complete documents. It correctly isolated the purpose and conditional clause
in n12, but misclassified n03's reason as a condition and m06's lack-of-evidence
caveat as a basis. The model switch alone did not meet acceptance. All68 actual
request bodies were compared: only the served model name changed.

## Fix for the missing endpoint contract

`context_contract.bind` now rejects a newly generated context interval containing
its entire target root assertion. The root is the existing preserving-v3 first
assertion; a proper inline qualifier remains allowed, as does a reason that is
a separate assertion elsewhere. This adapts the distinct-endpoint principle to
our span-based representation. It uses no words, case IDs or evaluation labels.
No additional model call or deletion of old records is introduced.

With the same saved raw outputs and fixed scorer, this reduces false edges
128→54 for8B and103→67 for14B. It also removes4 and2 newly credited links whose
quotations violate the stricter endpoint boundary. All original283 content
nodes,44 correct links and187 stances remain. However fully correct documents
are21/68 and18/68, below the baseline27/68, so neither candidate is adopted.

This fixes an identifiable contract omission; it does not solve semantic
ownership, role confusion or the missing reasons. Existing malformed roots can
also limit the relation pass. In seven baseline-rejected documents, including
n01/n07, the adapter retains the baseline failure instead of concealing it.
The production default remains unchanged. Do not present the improved
candidate-to-candidate figures as a win over the accepted baseline.

## Tokenizer warning audit

The adapted checkpoint emits a Mistral-regex warning. The actual encoder config
is DeBERTa-v3-base, not Mistral. Transformers4.57.6's
[warning path](https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/tokenization_utils_base.py)
checks large vocabularies and local saved version metadata; with an intermediate
saved version it can reach the warning branch without a Mistral model type.
The warning-only branch does not patch the tokenizer. We did not force a
Mistral regex onto this encoder or attribute the missing reasons to this
warning. The base config advertises5.8.0 while our adaptation runtime is4.57.6;
that compatibility difference remains documented, not silently equated with
the author's training environment.

Protocol: [ANCHORED.md](../evaluation/record_binding/ANCHORED.md).
Results and adoption decision: [v2 report](../results/record-binding/v2/README.md).
