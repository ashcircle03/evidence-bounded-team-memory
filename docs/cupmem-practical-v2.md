# Practical service: responsibilities and operating contract

This is the implementation under the active practical-service goal. Acceptance
is pending the frozen final comparison; consult `results/cupmem/practical` for
actual measured status. Service-v1 and its result remain separate and unchanged.

## Intended behavior and reuse

| Responsibility | Implementation | Reason and limit |
|---|---|---|
| Native memory writes | `CUPMemCandidateMemory`, official `write_session` | Reuse extraction, update and invalidation rather than reimplementing a memory engine. Its derived state never approves team changes. |
| Candidate discovery | Official `_retrieve_query_topk` plus existing provenance resolver | Reuse active/stale/unknown candidates and literal source lineage without generating a native answer only to discard it. Retrieved candidates are not verified conclusions. |
| Original search | CUPMem encoder and cosine ranking, batched/cached text vectors | Recover details omitted in memory. Same implementation and top4 hits in the simple control; no answer cache. Maximum16,384 source sentence candidates is explicit. |
| Pair review | Existing `review_sources` on each old-source/current-incoming pair | Prevent a prior update from being mistaken for the current report. At most8 candidate sources; report incomplete coverage. This follows CUPMem's individual candidate judgment pattern. |
| QA | Existing `core.answer_question` and service-v1 temporal/approval handling | One source-grounded generation; historical observations survive changed premises. With no team links, simple and candidate use the same reader input. |
| Authority and storage | Existing immutable `Store`, `timeline.review`, append-only votes | The original owner reviews the exact proposal. Caller authenticates identity and transports files; the library does not implement Git hosting or MCP. |

[Pinned CUPMem code](https://github.com/icedreamc/STALE/tree/ea7d391103a151927cd29d2f01d87597a782bdcb/cup_mem)
and [paper](https://arxiv.org/html/2605.06527v1#S5) supply the memory implementation.
The query orchestration here is an adaptation, not a claim to reproduce native
CUPMem scores. The shared retrieved-original reader is the simple comparison
path, not a new retrieval research contribution.

## Interface

Construct `PracticalCUPMemService(memory, generate, store, strategy='cupmem')`.
`memory` is `CUPMemCandidateMemory(engine, recorded_calls)`, where `engine` is the
pinned `CupMemEngine`. `generate(system, content)` returns model JSON text.
The evaluation runtime records every physical request/response and serves as a
complete real-model wiring example: [run.py](../evaluation/cupmem/practical/run.py).
Use `SourceOnlyMemory` and `strategy='simple'` for the control.

The common response envelope retains `schema_version='team-memory-service/v1'`
and `operation`, `status`, `answers`, `proposals`, `warnings`, `errors`.
`ok` is mechanical completion, never a guarantee of semantic correctness.

| Request operation | Required fields | Behavior |
|---|---|---|
| `ingest` | `source` | Capture original, native write, retrieve earlier candidates, propose review. Duplicate input reuses its receipt and refreshes actual vote status without inference. |
| `ask` | `question`; optional `temporal_scope` | `current` or `historical`, default `current`; return exact original citations and actual overlapping review state. |
| `review` | `proposal_id`, `actor`, `choice` | Existing owner-bound vote handling. No model inference or implicit approval. |
| `import_history` | `records` | Empty-store initialization of a full source collection. Native writes in batches, without generating speculative review proposals during import. |
| `rebuild` | none | Explicit native writer replay with the saved batch boundaries; retain original sources and votes. Performs inference. |

An original source contains `owner`, timezone-bearing `observed_at`, and
`source: {speaker, location, text}`. Supply original reports, not gold claim labels.

```python
service.handle({"operation": "ingest", "source": {
    "owner": "jaewon", "observed_at": "2026-11-06T10:00:00+09:00",
    "source": {"speaker": "jaewon", "location": "git://project/report/1",
               "text": "We stopped batch trials because only one worker was available."}
}})
received = service.handle({"operation": "ingest", "source": {
    "owner": "teammate", "observed_at": "2026-11-06T11:00:00+09:00",
    "source": {"speaker": "teammate", "location": "git://project/report/2",
               "text": "The batch runner now supports four workers."}
}})
answer = service.handle({"operation": "ask",
    "question": "Why did we stop the trials, and what changed?",
    "temporal_scope": "historical"})
# Pass received['proposals'] to the original author. Their explicit choice,
# authenticated by the caller, can then be submitted using operation='review'.
```

This illustrative snippet does not assert an unmeasured answer for those strings.
The measured executable example is the packaged Cedar development stream.

## Import, persistence and failures

`import_history` validates the whole input before capture, rejects duplicate
source IDs and nonempty stores, and preserves every original envelope and order.
Default native batches contain at most16 records and12,000 JSON characters;
an oversized single record is rejected rather than silently truncated. Native
session time is the latest observation in its batch, while each turn retains its
original timestamp. This is a source-collection adapter, not native chronological
STALE semantics. New `ingest` records are independent subsequent native sessions.

`cup_intakes` stores original arrival order; `cup_batches` stores exact native
import/arrival boundaries. On failed writing, originals remain and further model
operations require explicit `rebuild`. After restart, an empty derived engine
likewise requires rebuild. A corrupt batch/order manifest is an error, not an
excuse to invent a replacement history. One process owns each service directory.

QA uses original retrieval and exact team review links; it does not treat an
AI-assigned STALE label as deletion of the whole source. Pair review records
`review_traces` for each actual old/new input. Invalid evidence is rejected and
reported; an invalid attempt with no saved proposal is not a successful abstention.
When native candidate retrieval fails, raw source candidates remain available
with an explicit warning. Query-time native state mutation requires rebuild.

The library still relies on model reasoning for semantic relevance, conditions
and explanations. Citation offsets, schema validation and owner votes do not
prove entailment. Resource bounds, candidate omissions, errors and partial
results must remain visible to the caller.
