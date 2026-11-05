# CUPMem team service v1: implementation contract

Status: implementation contract fixed before the integrated development run.
This is a development API, not a benchmark result or a replacement-baseline decision.

## Purpose and reuse

Accept unannotated team reports, propose evidence-linked review of prior decisions,
and answer questions with original citations while preserving conditional observations.
The caller supplies an existing `CupMemEngine`, its physical-call recorder, and a
`generate(system, content)` function. No UI, MCP server, new memory engine, or paid
provider is introduced.

| Component | Purpose | Reused implementation / reason |
|---|---|---|
| Memory writer/query | Update and retrieve potentially invalidated beliefs | Official CUPMem revision `ea7d391103a151927cd29d2f01d87597a782bdcb`, unchanged. [Paper section 5](https://arxiv.org/html/2605.06527v1#S5). |
| Original records | Preserve observations independently of derived memory status | Existing `Store`, `source_envelope`, `capture`, content IDs. A changed deployment constraint does not erase a past measurement. |
| Original-source retrieval | Recover details omitted from summaries | Reuse CUPMem's already loaded `engine.embedding.rank` on original sentence passages, top 4; no new embedding model or custom ranking algorithm. A bounded union with native provenance replaces no native state. This is a design hypothesis, not measured superiority. |
| Native provenance | Recover selected memory origins and status-change causes | Existing `resolve_grounding` / `source_packet`; validated against the captured originals. [Multi-vector retrieval pattern](https://www.langchain.com/blog/semi-structured-multi-modal-rag). |
| Structured review | Make recommendations consumable by another module | Read only selected earlier sources plus the explicit incoming record; reuse passage IDs, exact-span resolution, `timeline_proposals` and owner review. |
| QA | Preserve conditions, history, and unresolved reports | Existing original-source reader; pass explicit temporal scope and actual review links. |
| Approval | Keep AI memory distinct from approved team changes | Existing `timeline.review` and append-only votes. Only an approved correction supersedes its precise old assertion; reconsideration never invalidates an observation. |

ATMS supplies a rationale for recording a conclusion's supporting assumptions,
not a claim that natural-language condition extraction is solved or that an ATMS
engine has been implemented: [de Kleer 1986](https://www.dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf).

## Ownership of state

1. `sources`: immutable original reports, owner, observed time, location and text.
   Source IDs deduplicate repeated intake. Source content is not an instruction.
2. CUPMem state: derived candidate memory; can change before a human review.
   It does not approve, delete, or rewrite the original source or team votes.
3. `timeline_proposals` / `timeline_votes`: team review state, reused unchanged.
   A proposal records `previous` / `incoming` assertions and additional exact
   `old_condition`, `new_condition`, and `old_reason` witnesses. For reconsideration,
   `previous` must be the earlier decision and all three support roles are required.
   These role assignments remain model interpretations, not proved entailments.
4. Source order and successful intake receipts are stored separately. One service
   owns one engine and serializes its calls. Multiple processes must not share an
   engine or service directory concurrently. Separate Git checkouts have separate
   derived engines. New shared records are passed through `ingest` by the caller.

## Operations and return contract

`CUPMemService(memory, generate, store)` exposes:

- `ingest(source)`: capture first, native write, native review query, original-source
  retrieval, structured review, then save pending proposals. The first record has
  no earlier target. A repeated source returns its receipt with no extra inference.
- `ask(question, temporal_scope="current" | "historical")`: native query + original
  retrieval + linked originals + relevant team review records -> ONE canonical
  `answers` list. The native answer is diagnostic, never an implicit fallback.
- `review(proposal_id, actor, choice)`: original-owner review of an exact proposal.
  Actor authentication is the caller's responsibility; the engine cannot approve.
- `rebuild()`: explicitly replay captured arrivals through the native writer after
  restart or a failed write. This performs model calls and preserves team proposals
  and votes. It does not silently retry failed writes or regenerate proposals.
- `handle(request)`: JSON dispatcher for these four operations. No transport/UI.

All responses use `schema_version`, `operation`, `status`, `answers`, `proposals`,
`warnings`, `errors`, and operation-specific metadata. Status is one of `ok`,
`partial`, `insufficient`, `invalid`, `error`, `needs_rebuild`. `ok` means the
operation met the mechanical contract, not that an answer is semantically correct.
Each accepted citation names a source ID, literal quote, character offsets, owner,
speaker and location. An answer can cite several passages.

For historical QA, old observations retain their recorded conditions and correction
annotations. For current QA, approved corrections apply only to their exact old
assertions. Pending/disputed corrections remain visibly unresolved. Review links
touching selected evidence pull in their counterpart original records so that one
side cannot be hidden merely by retrieval. Rejected proposals do not alter QA state.
The prompt enforces question relevance; citations carry actual overlapping review
states. Current answers supported only by fully superseded quoted assertions are
flagged partial, not silently rewritten or dropped.

Malformed output or bad evidence is isolated at the individual answer/proposal;
valid siblings survive as partial. A source retrieval hit is not semantic support.
No candidates -> insufficient. Missing provenance or native query failure can use
the independently retrieved original sources, explicitly reported as degraded.
No source is invented from the native answer. A failed native write preserves the
original, blocks further model operations until explicit rebuild, and is not retried.
Native query mutation of persistent memory is an error. A constructor with saved
sources and an empty engine requires rebuild before model operations.

The raw search scans at most 2048 original sentence passages. Beyond this bound it
reports the limit and uses native candidates; it does not truncate source documents
or claim scalable indexed search. Top 4 is a development resource bound, not a tuned
optimum. Historical scope is not an arbitrary point-in-time snapshot API.

## Completion checks for this implementation

Before any model result is inspected:

- Unit/integration checks: duplicate intake, malformed input/output, unknown or
  swapped evidence IDs, missing reconsideration roles, owner approval, persistence,
  failed native writes, explicit rebuild, current/historical policy, no-candidate
  behavior, raw retrieval when native provenance misses, and unrelated review scope.
- One live, fully connected Qwen3-8B run: the existing two-record Cedar development
  stream followed by an unrelated report. No human claim/condition labels enter
  the model. Verify a supported reconsideration, conditional measurements and
  folder QA, no proposal caused by the unrelated report, and QA after owner review.
- Separately record engineering execution success and each semantic outcome. Do
  not revise the expected output or retry prompts after seeing this run.
- Preserve raw requests/responses, source/config/input hashes and Slurm accounting.
  GPU1 / CPU8 / 48G / 25 minutes, conda, no node pinning; one initial submission
  within the existing 200 CUPMem / 500 campaign GPU-minute caps.

The small run is development evidence. General retrieval recall, false-positive
rates, existing 20-QA preservation, and benchmark improvement remain unmeasured.
