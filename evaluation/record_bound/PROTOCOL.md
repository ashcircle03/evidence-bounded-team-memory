# Bound records candidate, fixed full-gold comparison

Records only. Gold and scorer are EXACTLY the frozen `evaluation/record_full/{gold.json,evaluate.py,gold.py}` v3 files. Do not tune their anchors, labels or metric rules. Compare68 new Qwen3-8B non-thinking calls with the previous same68 inputs/136 simple and grouped outputs from122970. Same model revision b968826d9c46dd6066d109eabc6255188de91218, temperature0, seed42, max output2048. Candidate gets the SAME source/author metadata, split into original sentence segments with IDs. The additional structural prompt and two new-domain examples are part of the intervention; record token/time cost. No QA generation, training, paid API, gold in inference packet or reference-model substitution.

## Intervention and reference implementation intent

1. LangExtract1.7.2 Resolver exact alignment is actually called. Restrict alignment to the model-selected source segment and translate its character interval back to original offsets. Distinct repeated times in distinct segments are no longer globally ambiguous. Wrong segment or changed meaning is rejected, not repaired by nearest/fuzzy text.
2. LlamaIndex0.14.25 SchemaLLMPathExtractor creates a nested typed triplet schema, validates each item and skips invalid items; `_prune_invalid_triplets` removes invalid types/relations without discarding every valid item. Adapt this implementation pattern to nested root+context records and per-span quarantine. We are not claiming to execute its KG extraction or ontology. Whole-source text and rejection diagnostics stay available.
3. LangExtract Extraction stores attributes per extraction. Preserve stance per assertion (and method/qualification kind) in records.graph/v3 instead of forcing a proposal and an approval-status observation into one group stance. Root stance remains for backward compatibility; consumers receive assertion attributes too.
4. Explicit `ignored` source spans separate salutations/acknowledgements/formatting from reusable records. No benchmark-name/ID-specific filters or phrase replacement rules. A mistaken omission still loses recall. Original text is always retained.

Installed source files and hashes are captured in references.json. Primary upstream locations:
- https://github.com/google/langextract/blob/main/langextract/resolver.py
- https://github.com/google/langextract/blob/main/langextract/core/data.py
- https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/indices/property_graph/transformations/schema_llm.py

## Compatibility and frozen metric adapter

V1/V2 graph validation and constructors remain available. V3 adds per-assertion attributes, original-source excluded spans, partial status and item-level diagnostics. RecordsAdapter must append/reload it and reader_bridge must preserve every visible assertion attribute and provenance. Gateway exposes partial extraction as an issue; it does not promote it to complete.

The frozen scorer consumes rows. `rows.py` only flattens new nested output and per-assertion stored attributes into the SAME role/text/group/stance rows. It never reads gold. V1/V2 rows must exactly equal the old representation adapter for all136 outputs. This is an input-format adapter, not a changed evaluation rule. Ignored spans are explicitly classified non-records, not counted as generated record rows; their correctness is checked through missing substantive gold and preserved raw source.

## Diagnosis and adoption gates fixed before new outputs

Report content/root/typed-edge scores, wrong/extra rows, boilerplate, overmerged pairs, per-assertion stance, raw→compiled loss, exact source preservation and actual persistence/reader transport; keep synthetic and natural separate and all9 primary strata unchanged.

For each old grouped output, define protected required nodes and required edges as the gold items it correctly retained AFTER compilation. Also protect each of its complete documents. Compare exact item sets, not merely total recall or a higher average hiding damage. Default adoption requires all protected nodes/edges/complete documents preserved, no transport/source integrity failure, no lower typed-edge F1 in either panel and an improvement in at least one panel's typed-edge F1. A failed gate means opt-in experimental implementation only; no automatic default switch. Do not choose a per-case output using gold or merge gold-correct pieces of two arms.

One68-call candidate run, with old simple/grouped cached controls. No semantic prompt iterations or extra modules based on these outputs. Runtime compatibility fixes, if needed, require a new immutable packet with failures preserved. Same data were previously observed, so this remains development evidence, not held-out generalization.

## Execution

Aurora batch_ugrad/ugrad, g8 for existing NLTK reuse, GPU1/CPU8/RAM48G, fixed12h, --no-requeue, conda. Check queue+dispatch lock before sbatch --parsable and immediately preserve actual ID. No login-node computation or dataset duplication. Verify COMPLETED/0:0, program completion, all68 calls, exact input/code hashes, frozen scoring hashes and packet transport before reporting success.
