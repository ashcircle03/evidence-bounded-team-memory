# Records difficulty and evidence availability diagnosis v1

Frozen before model outputs. Production records/retrieval/QA code remains unchanged.

## Question and contrasts

Determine whether required information is missing in the submitted source, lost in model extraction/role linkage, rejected during alignment/compilation, or lost in persistent storage/reader transport. Same Qwen3-8B revision, non-thinking, temperature0, seed42, max2048 output tokens, shared guided JSON schema and canonical LangExtract1.7.2 compiler in both arms. Alternate arm order per input. No retries selected by quality.

- `simple`: concise role/stance definitions, explicit format, no demonstrations.
- `ours`: existing grouped DESCRIPTION and its two demonstrations. NOT the previously rejected revised contract/examples.
- Both use graph/v2's optional basis_kind compatibility field and identical persistence. This controlled contrast measures input specification, not native end-to-end paper baselines. Different prompt lengths are recorded as cost; output budget is equal.
- Neither prompt receives gold, difficulty, evidence-availability labels, downstream questions or answers.

## Data and sampling

Primary panel:18 synthetic base stories,6 per preassigned difficulty, each with full/partial/none availability of TWO focal context requirements =54 inputs,6 per 3x3 cell. Difficulty denotes construction features, not measured item difficulty: easy local statements; medium cross-sentence scope plus distractors; hard distant scope, competing target and repeated short phrases. Stance/negation/caveats occur across tiers. These are related variants and share six semantic template types;54 is not the independent sample size. They are development diagnostic inputs, not a held-out generalization benchmark.

Availability refers to the focal condition/reason/time/caveat fields, not the whole document. The focal claim remains in all variants. Partial variants alternate which qualifier is omitted. None means neither focal qualifier is supported; some competing records retain the same literal date but it must not be attached to the focal claim. Omission of unavailable content is correct. The counterfactual variant is the input truth; knowledge of other variants cannot fill missing fields.

Secondary panel:14 original EverMem messages from5 prior failure-selected cases. Preannotated focal claims/roles only, not exhaustive source gold; never pooled into the balanced scores. These preserve the current ONE-message interface, so absent antecedents are explicitly unavailable. Ambiguous future plans accept decision/proposal, reported approval accepts observation/decision, and the implicit polling reason is optional. No new original-benchmark QA score is claimed.

No train/test split or training this round. Any later split must keep every variant of a base story and all messages from the same natural case together. Independent annotation and broader natural data are needed before a service-quality/generalization claim.

## Frozen scoring

`keys.json` and `score.py` are hashed before submission. Focal anchor coverage, all visible content recovered in the same group, all visible roles correct, stance, unsupported withheld-value completion, wrong-target qualifier attachment and combined pass are separate. Normalized word-sequence coverage permits capitalization/punctuation differences; exact verbatim grounding is separately reported. Multiple linked spans may cover the focal phrase. Group labels themselves never count as extracted content. Optional fields do not penalize omission. A correct group cannot cancel another wrong group for the same focal claim.

These checks are partial semantic probes: wrong content outside the focal group and unstated hallucinations not matching the withheld/foil spans require manual audit. Exact source grounding is not proof of correct linkage. Report case-level raw output, compiler errors, graph and transport receipts; do not relabel after observing output. Explain any label ambiguity in a separate audit without changing primary scores.

Stages:
1. Raw generated groups (including truncation, verbatim and field/link failures).
2. Same raw output through unchanged compiler. Count correct raw information lost through document-wide rejection separately.
3. Actual RecordsAdapter append, new adapter instance snapshot, source equality, every claim's reader witness record_context equality and role span enclosure. This is storage/reader-packet transport, not semantic QA or a second operating-system process restart.

Preflight gold minimal exact quotes passes the scorer and exercises the same compiler/storage without LLM. Repeated short quotes may fail even with correct gold; this diagnoses a representation/compiler mismatch, not proof no longer unique span can work. Preserve these cases rather than tuning the compiler away before measuring. Preflight also tests wrong-role versus content presence, missing-input invention, and duplicated target false links.

## Interpretation and stopping

Run136 fresh calls once; no prompt tuning/new modules based on outcomes. Full/partial/none matched pairs show input availability sensitivity. Differences between prompts show a prompt/extraction effect under this backbone. Both arms failing does NOT prove intrinsic model incapacity: output contract and shared compiler remain confounds. Use raw output and gold preflight to localize them. Persistence equality can hold even when extraction was already wrong.

Report9-cell counts and separate natural panel; no aggregate model-versus-system superiority based on success-selected QA20. Existing QA20 is unchanged production regression evidence from prior run, not freshly executed here. No product adoption based only on total score. Prefer repairing demonstrated upstream loss before adding a checker or changing models.

## Execution and references

Aurora GPU1/CPU8/RAM48G, fixed12h, no-requeue, conda, g8 for existing NLTK dataset reuse. No data/model replication, paid APIs or master-node computation. Explicit inputs/code archive, dispatch intent/lock, actual sbatch ID and result hashes. Validate Slurm COMPLETED/0:0, server/client completion and136 exact requests before conclusions.

The capability/test-type separation follows the behavioral testing rationale of CheckList (https://aclanthology.org/2020.acl-main.442/); this dataset/metric is our diagnostic adaptation, not its benchmark. Existing extraction reuses upstream LangExtract structured examples, Resolver and exact alignment, with our graph compiler unchanged. No new retrieval/QA modules.
