# Practical CUPMem service goal

Status: active development, before new inference and final data selection.

The authoritative objective is the user-approved goal of 2026-11-06. This plan
does not turn its performance targets into presumed results. Existing service-v1
code, inputs, criteria and output archives remain unchanged.

## Required evidence

| Requirement | Evidence to produce |
|---|---|
| Existing Cedar flow | Fresh connected local Qwen run: five QA checkpoints, unrelated intake, exact sources and approval events |
| Legacy QA preservation | All original20 cases and full original corpora; same actor/retriever/reader for simple and module; casewise content AND citation scoring and lost-baseline-success count |
| New review transfer |20 source-grounded streams,10 positive and10 negative, excluded from prior experiment inputs; original evidence and rubric frozen before final inference |
| Citations and state | Literal offsets plus actual physical input/output linkage; separate manual semantic assessment; no AI-generated approvals |
| Cost | First-time questions, physical calls, input/output tokens and warm inference latency; target at least50% reduction from9 QA calls |
| Deliverable | Headless implementation, clear API/state ownership, working examples, evidence archives, final acceptance/rejection decision |

## Initial design direction

Service-v1 invokes CUPMem's full query chain (eight model calls in each observed
QA) and then a second source reader. Four intermediate answers reject unrelated
facts as outdated; source readout recovers them. We will preserve the upstream
writer and provenance representation, while separating factual QA from native
premise adjudication. QA and the simple control share one source retrieval and
cited readout; team review state adds exact assertion-scoped relationships.

The upstream code exposes `_retrieve_query_topk`, `_build_topk_status_context`,
and explicit chunk/delta/source lineage without generation. Reuse this for
candidate discovery during review, rather than generate and discard a native
answer. Candidate state remains unapproved; a proposed reconsideration cannot
invalidate an old observation. This is an engineering adaptation, not unchanged
CUPMem query evaluation or a baseline replacement.

Development119825 found that multi-source review treated an old follow-up as the
incoming report on unrelated Birch intake. The source-role validator rejected
the output, so this is an invalid review rather than a successful abstention.
The revision compares each retrieved prior source with the actual incoming source
separately using the same existing reviewer. This follows the upstream writer's
candidate-by-candidate judgment pattern. At most8 source candidates are judged;
coverage limitations are explicit. Native status annotations guide candidate
discovery, not semantic conclusions in the pair's original-source review.

Legacy20 consists of Git, PEP, controlled cases and three natural EverMemBench
questions over seven source collections. Preserve every original source and
question. Do not turn786 unique source documents into gold-filtered packets.
Choose and document a bounded import mechanism before inference; bulk source
collection import is not a native STALE chronological-session reproduction.

## Evaluation discipline

Use service-v1 and explicit development fixtures for implementation. Lock code
and prompts before inspecting/selecting new final outcomes; data/rubrics are
fixed before execution. Report real versus synthetic/controlled data separately.
Do not interpret small-panel success as a population false-positive rate.
After final evaluation, report unmet gates and choose the supported path; no
output-specific rules or repeated final-set tuning.

## Resources

The user authorized240 additional GPU minutes. Campaign cap:500→740;
CUPMem cap:200→440; new `cup-practical-` jobs also have their own240-minute cap.
Current queue was empty; no open dispatch intents or locks. Every server
computation uses GPU>=1 in Slurm with explicit conda, no node pinning, no requeue.
Keep user-wide limits of4 running jobs,8 queued/running tasks,4 GPUs. Count failed
attempts and reservations. No external model API. Freeze resources before each
submission, record actual job IDs immediately, verify accounting and program
completion. Do not resize a failed allocation automatically.

## Reused sources

- [CUPMem paper section5 and appendixF](https://arxiv.org/html/2605.06527v1#S5)
- [Official pinned code](https://github.com/icedreamc/STALE/tree/ea7d391103a151927cd29d2f01d87597a782bdcb/cup_mem)
- Existing `Store`, `timeline.review`, `core.answer_question`, provenance resolver
  and service-v1 tests. Source retrieval uses CUPMem's existing embedding model.

No UI, MCP, Notion write, paid provider, or primary-baseline replacement.
