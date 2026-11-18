# Parent-bound records extraction

This candidate changes records extraction and serialization, not QA or review authority. It is opt-in until the fixed evaluation passes the preservation gates in [the protocol](../evaluation/record_bound/PROTOCOL.md). Do not replace `grouped.construct_aligned` with it merely because an aggregate score increases. Evaluation results live in [record-bound/v1](../results/record-bound/v1/).

## Problem and reference implementation

The prior full-document audit found three different failures: context assigned to the wrong assertion, non-substantive text emitted as records, and valid model output lost during graph compilation. Keeping the original text does not by itself make these annotations usable by downstream modules.

| Failure | Implementation change | Reference and boundary |
|---|---|---|
| Free context groups can attach a reason to the wrong assertion | A nested record has one root, its details, and its own condition/basis/time/subject lists | Adapt the nested typed schema and per-item validation used by LlamaIndex `SchemaLLMPathExtractor`. We do not execute that class's KG extraction or reproduce its full ontology. The LLM still decides the semantic attachment; the schema cannot prove it correct. |
| Identical time phrases in different sentences make whole-source alignment ambiguous | Every quote carries its original segment ID; align inside that segment and translate to original offsets | Actually call LangExtract's `Resolver.align` with fuzzy and lesser matching disabled. Segment IDs disambiguate location without rewriting the quote. |
| One invalid span discards unrelated valid content | Reject the invalid span with a path and reason; retain other aligned content; reject a record whose root is invalid without reparenting its context | Adapt LlamaIndex's individual validation/pruning pattern. Mark incomplete output `partial`; never silently report complete extraction. |
| A proposal and its lack-of-approval observation collapse into one stance | Preserve `stance` and `kind` on each assertion, alongside the backward-compatible root stance | LangExtract's extraction-level attributes motivate preserving metadata at the same unit as the extracted assertion. This records what the source says; it is not an approval event. |
| Greetings become reusable facts | Separate exact `ignored` spans from records | Explicit extraction contract, not a keyword filter. Full source remains immutable. Ignoring a substantive claim still loses recall in the fixed gold. |

Primary implementation sources:

- [LangExtract Resolver](https://github.com/google/langextract/blob/main/langextract/resolver.py)
- [LangExtract extraction attributes](https://github.com/google/langextract/blob/main/langextract/core/data.py)
- [LlamaIndex typed extraction and pruning](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/indices/property_graph/transformations/schema_llm.py)

Exact installed versions and implementation hashes are recorded in [references.json](../results/record-bound/v1/references.json). The reference patterns do not establish that this adaptation improves the benchmark; that requires the measured comparison.

## Input, output and ownership

Input is a complete immutable source: ID, owner, speaker, observation time, location and original text. `bound.segments(source)` supplies sentence IDs and original offsets. No question, gold label or target answer selects which sentences to process.

The model emits `records` and `ignored`. Each record has one `root` plus `details`, `condition`, `basis`, `time` and `subject`. Every item has an exact quote and segment ID. Root/details carry their own stance; details distinguish qualification, method and continuation. Basis distinguishes a source-stated link from an inferred link. A procedural detail is not automatically a condition or a reason.

`records.graph/v3` retains all source units and produces typed claim-to-context links. It adds per-assertion attributes, excluded spans and rejection diagnostics to the existing graph contract. V1/V2 remain supported. This is an attributed graph representation inside the existing records store; it does not require a graph database or a new central service.

All extracted assertions remain `model_extracted_unverified`. Records may preserve explicit approval wording, but only the existing review/state authority may apply an approval event. QA is not allowed to promote these annotations to accepted state.

`graph.describe` delivers assertion attributes with source spans. RecordsAdapter append/reload and the reader bridge must preserve them. Gateway reports partial extraction as an issue while making original source and accepted annotations available. Downstream consumers must inspect extraction status and must not treat a missing annotation as proof that the original source lacks that fact.

## Opt-in integration

Use the same existing record-builder injection point. For each source, configure the provider's structured-output constraint with `bound.schema(len(bound.segments(source)))`, then invoke:

```python
from team_memory.records import bound

def build_records(source):
    output_schema = bound.schema(len(bound.segments(source)))

    def generate(system, prompt):
        # Existing provider returns the raw JSON string using output_schema.
        return provider.generate(system, prompt, schema=output_schema)

    return bound.construct(source, generate, model=model_revision)
```

`provider` above is a placeholder for the caller's existing client, not a new provider API shipped by this patch. The runnable local-Qwen integration is [evaluation/record_bound/run.py](../evaluation/record_bound/run.py). Its inference packet contains source inputs and code, not gold or scorer files.

## Failure and compatibility contract

- Invalid envelope: failed annotation, preserved source, diagnostic.
- Invalid item shape: reject that record/item and record the path.
- Invalid root alignment: reject its record; never attach its context elsewhere.
- Invalid context alignment: preserve the valid root and other valid context, mark partial.
- Exact repeated quote in different segments: resolve by declared segment. Repetition inside one segment still requires a longer quotation.
- Changed wording or wrong segment: no fuzzy repair, invented quote or guessed location.
- Invalid/missing JSON after token truncation: reported as failure, not a hidden extra call.
- Exact duplicate removal is allowed; semantic deduplication and merging are not added here.
- Original source and source metadata never change; excluded spans also point back to original text.

## What the fixed evaluation establishes

The comparison uses the same 68 sources and Qwen3-8B revision as the previous simple/grouped controls. Only the candidate has new calls; controls are cached actual outputs. Report synthetic and natural panels separately, and retain all difficulty/evidence-availability cells. Compare raw output with stored representation to distinguish model extraction errors from compilation losses.

The frozen scorer measures required content, assertion roots, typed links, extra rows, boilerplate, merging errors, stance errors and strict complete documents. It does not certify unrestricted semantic equivalence or downstream QA correctness. Protected items are the individual required nodes and edges retained by the old grouped method, plus its complete documents. An improved average cannot compensate for losing those items in the adoption gate.

The data have already been inspected during development. This is a controlled regression/quality diagnosis, not a held-out generalization claim. No QA inference is included in this records-only task.
