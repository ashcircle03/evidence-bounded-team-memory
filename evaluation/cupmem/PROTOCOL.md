# CUPMem / STALE reproduction and team transfer

This protocol is fixed before this campaign's model outputs. No previous frozen
evaluation, score, or source snapshot is changed. The objective is a design
decision based on faithful implementation, not a sequence of local rescues.

## Native benchmark

- Upstream: icedreamc/STALE, commit ea7d391103a151927cd29d2f01d87597a782bdcb.
- Dataset: STALEproj/STALE revision 617c51dc200b5ab09970834144c7e51c77959af0,
  T1_T2_400_FULL.json SHA256 5f3ec375179e20e2e94469e018189188f34e2e7e5f21cbecbd99fcfa648c1876.
- 400 cases, 50 chronological sessions each, three probes. Verify actual type counts.
- CUPMem ingests every session (`full`, never CLI default `relevant_only`).
  Preserve original prompts, schema, thresholds, writer, retrieval, and reader.
- Strip M_old, M_new, explanation, and relevant_session_index from the object
  passed to CUPMem. Questions are consumed only after writing. Hash persistent
  memory before/after each probe and require the same memory for all three.
- Original actor: GPT-4o-mini. Original judge code: gemini-3.1-flash-lite-preview.
  BAZE lists neither the actor nor that exact judge ID. The user chose BAZE to
  avoid an additional OpenAI payment. Pilot uses gpt-5.4-mini and
  gemini-3.1-flash-lite. This is an **alternate-model protocol reproduction**,
  not reproduction of the paper's reported score with the original models.
- Match the direct baseline to the actor and official prompt functions. Keep
  the original 125440 input-token budget and original gold-preserving noise
  truncation. This baseline has privileged truncation; disclose every removal.
  Do not describe it as unassisted retrieval. Three questions are independent.
- Use the exact official all-in-one judge prompt/function, with explicit client
  injection. Gold fields go only to the judge. Technical failures, incomplete
  cases, and capped outputs are reported separately from semantic failures.
- Pilot: one UID-hash-selected case per type (`cupmem-pilot-v1:` salt), chosen
  before inference. It measures compatibility, latency, usage, and trace
  validity; two cases cannot establish performance. Full 400-case inference
  remains required for a benchmark-wide conclusion and needs measured sizing.

## Pilot execution and accounting

Authorized scope: two full cases, CUPMem plus direct plus official judge;
maximum 1000 physical requests, 5000000 input tokens, 200000 output tokens.
CPU8/RAM16G/GPU0, walltime45min for the activated-conda pilot; failures and compatibility probes count.
No automatic resource increase or repeated submission after a timeout.

Environment amendment before any paid call: the user requires an activated
conda environment for all server computation. Create the isolated prefix
`runtime/cupmem-conda-v1` on a Slurm compute node, activate it explicitly, and
assert both CONDA_PREFIX and sys.executable. v1 stopped before inference because
the prior uv-managed environment had no pip. v2 passed eight offline tests and
verified the data but received no key after the user's conda requirement; it
expired at the credential wait. Preserve both failures and include their actual
CPU allocation time. They produced zero API model calls. Before conda pilot
inference, plan the new CUPMem goal at CPU120 minutes and the cumulative campaign
at CPU200 minutes (previous cap100), including all earlier usage; no usage reset.
The API request/token limits are unchanged. The prior 25-minute requests failed
in setup/credential waiting, not at the Slurm walltime or memory limit. The
45-minute request provides API latency headroom for the newly required conda
execution. No walltime/OOM-triggered automatic expansion is authorized.

Resource-policy amendment while job119626 was running: the user now requires
at least one GPU for every newly submitted compute allocation, even for
preprocessing or external-API inference. All new submissions request GPU1 or
more and explicitly activate conda. Already running119626 remains unchanged
under the prior instruction against unsolicited cancellation/reallocation.
Plan CUPMem at200 GPU minutes within the existing campaign500 GPU-minute cap;
all failures remain included. GPU allocation alone does not change the frozen
embedding device or model inputs of the running comparison.

The transport logs every physical request and raw response, reported model ID,
usage, error, elapsed time and input hash; SDK and original CUPMem retries count.
Headers and credentials are never logged. Unknown usage retains a conservative
reservation, not zero cost. Concurrent calls reserve capacity before sending.
The pilot adds an 8192-token output cap per request (actor
max_completion_tokens; judge max_tokens). This runtime difference is explicit.
Any length termination stops the pilot and makes the affected sample censored.
No reasoning-effort or temperature substitutions are applied silently. First
test the actual nondefault temperature and JSON settings used by the source.

Credentials are delivered through SSH stdin to a same-UID private Unix socket
inside the already-recorded allocation. No key is embedded in source, config,
sbatch, exported Slurm environment, or credential files. Data and embedding
calculations stay on Slurm compute nodes; datasets remain under /local_datasets.

## Team transfer (separate from STALE)

Use the previously frozen 20 timeline streams and the 15 Git topics, with both
mixed and no-match cases and both raw and masked views (60 Git inputs). These
are previously exposed diagnostic cases, not a new held-out benchmark. Natural
EverMemBench questions embedded in the timeline remain distinct from synthetic
condition/review scenarios. Preserve source text, author, date, and location.
Represent team reports as attributed user messages without inserting gold
relations, normalized conditions, expected answers, or human decision summaries.

Compare the same actor with raw records versus unchanged CUPMem. Record both
write-time memory updates and query-time judgments. A query that prompts review
does not count as proactive detection. CUPMem has no native pull-request/author
approval interface; any later adapter must be labeled separately. Do not feed
scripted gold approval events into memory as if CUPMem earned a correct proposal.

Score separately: retained observations under each condition; correct old/new
target and exact evidence; explanation's actors/actions/conditions; warranted
review recall; irrelevant-decision false positives; repeated-arrival alerts;
unresolved evidence retention; and reviewer-controlled approval behavior.
Newer evidence under another condition must not erase an older valid result.

CUPMem's native final output has answer and brief_rationale, not formal citation
IDs. Measure native answer correctness and trace provenance separately. A common
cited reader may consume CUPMem-selected original passages and raw-baseline
passages, but is an explicit adapter with its own result table; it must not use
gold evidence or bypass memory with the complete history. Exact quote validity,
source correctness and entailment are distinct checks. Preserve the original
20-case legacy QA regression and separately test paired QA with the new actor;
an unchanged old-Qwen replay alone cannot establish CUPMem QA preservation.

## Stop / design decision

Do not change semantic prompts, schema, thresholds, or evaluation keys based on
these results. Version compatibility fixes, preserve failures, and disclose all
differences. Once the native benchmark and transfer comparisons are measured,
choose unchanged CUPMem, the simpler raw approach, or a narrowly justified
missing capability. Do not claim system completion from imports, unit tests,
one successful API call, or a two-case pilot.

## Local-model amendment, 2026-11-05

The user subsequently chose local inference and delegated model selection.
The current run uses public Qwen/Qwen3-8B revision
`b968826d9c46dd6066d109eabc6255188de91218`, BF16, non-thinking mode,
static YaRN factor 4, and a 131072-token context. It is a fresh paired run on the
same preselected two UIDs, not a continuation of the BAZE answers. No hosted
model API calls are authorized for this local run. The old BAZE limits and
partial results above are historical and remain preserved.

Preparation 119672 completed with Slurm COMPLETED/0:0, verified model bytes,
all 72 upstream files, the pinned 400-case dataset, and actual Qwen chat-template
counts. Earlier preparation 119669 timed out during download with zero model
calls. Actual allocated GPU time was 30:04 for 119669 and 10:30 for 119672,
combined 40:34. No failed allocation is discarded.

All six original-tiktoken direct packets exceeded 131072 when reserving 8192
output tokens: their actual Qwen input counts were 124788–127990. Before any
Qwen inference, select the explicitly labeled `qwen_token_budget` variant:
retain the original gold-preserving session-removal algorithm but use actual
Qwen counts and 122880 input tokens. Its frozen packets contain 118924–122095
input tokens and 39–42 sessions. Original gold-related sessions remain protected;
CUPMem still ingests all 50 sessions. This tokenizer/budget change and the
privileged direct truncation are deviations, not an exact original-model score
reproduction. Exact packets and both variants are retained in
`cup-context-119672.json`, SHA256
`a2bbf02da8c35d7ae47f30459d6bba3a8923445cbd2617e182b936518a2df7aa`.

Pilot 119684 uses GPU 2 / CPU 16 / RAM 96G / 75min under conda, without node pinning or
requeue. Both arms share the same runtime and native temperatures/prompts.
Three small compatibility probes and all six direct answers precede CUP writes.
Each response must report exactly the expected Qwen prompt-token count; context
or serving mismatches stop as technical failures. No silent truncation, variant
fallback, or partial-run inheritance is permitted. Local guardrails are 8000
physical requests, 50M input and 2M output tokens; these are not external API
spending authorizations. Slurm and the existing cumulative GPU limits remain
hard limits.

The official judge prompt/parser uses the same local Qwen model provisionally.
It is explicitly non-independent self-judging. Its scores require separate
source audit and cannot establish either paper-score reproduction or general
performance. Team/legacy inference remains separate and unmeasured until run.
