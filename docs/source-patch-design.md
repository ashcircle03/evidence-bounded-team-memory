# Source-bound updates before proposal classification

Status: both v1 and v2 rejected after fresh Qwen regression. Default service
restored to v3b. Historical results remain immutable. The QA reader is unchanged.
See [results and case-level evidence](../results/source-patch/README.md).

## Actual implementation references

| Reference inspected | Actual mechanism | Reuse here |
|---|---|---|
| [Trustcall `_ExtractUpdates`, `PatchDoc`, `_apply_patch`](https://github.com/hinthornw/trustcall/blob/8c7312b591542cf9349ce00d2811e890ea6eef91/trustcall/_base.py) | Updates an existing document through JSON Patch, applies the patch and validates the result; insertion/deletion are separately enabled | Adapt the existing-document update contract. Run the same upstream `python-json-patch` library, pinned1.33, with jsonpointer3.0.0. Do not import Trustcall's LangGraph orchestration or claim to run Trustcall. |
| [Graphiti `enforce_edge_type_signatures`, `_same_pair_edges`, temporal invalidation](https://github.com/getzep/graphiti/blob/747b480ec6b12ecb718f1e2bc588b20ee36ea9c2/graphiti_core/utils/maintenance/edge_operations.py) | Restricts candidate relations to resolved endpoints and allowed types; validity intervals limit invalidation | Adapt typed-target and scope checks. A decision-premise endpoint can only yield reconsideration; a different fact scope yields coexistence, not correction. No Graphiti graph database dependency or copied graph implementation. |
| [Zep paper](https://arxiv.org/abs/2501.13956) | Retains temporal provenance instead of treating every later fact as deletion of earlier history | Preserve original source, condition and owner vote. A changed premise proposes another review; it does not erase the original decision or establish approval. |

These projects do **not** supply a verified scientific-decision reconsideration
classifier. Our typed adapter is an adaptation, and its semantic accuracy must be
measured. Library correctness cannot certify model-extracted values or relevance.

## Failure and change

The previous model directly emitted `kind=correction/reconsider/...`. Literal
sentence validation could establish that the quotation existed but could not stop
a new-version result being labelled a correction or an irrelevant improvement
being stored as a proposal. v3b produced two wrong positive kinds and two unnecessary
negative proposals; the QA sometimes disagreed with the stored proposal.

The rejected first candidate in `team_memory/source_patch.py` had two model calls:

1. Extract facts or explicitly reasoned decision premises from earlier records.
   This call receives no new report, QA question or key. Subject, attribute, type
   and original-sentence bindings are fixed in the result.
2. Give the new report and existing records to a JSON Patch updater. It can replace
   only `value` and `conditions`, never identity, evidence, type, or approval.

The code applies RFC6902 and computes the actual delta. Empty/identity patches
produce no proposal. A changed decision premise becomes `reconsider`. Facts with
different conditions coexist informationally; explicit same-condition corrections
are proposed to the owner, and independent same-condition disagreement remains a
conflict. The model cannot directly choose the resulting relation kind. Missing
record updates, malformed patches, and out-of-range source IDs remain visible
failed receipts, not successful negative cases. Every valid or rejected update
retains its before/after evidence in `comparison_audit`.

Actual v1 execution120393 preserved legacy20 but lost4 of the state8. Three
comparisons failed from malformed JSON or omitted fields. The model also put
actions into the `value` field intended for decision premises: changing policy
then appeared to change only scope and was incorrectly ignored. A writer proposal
had the right relation label but the wrong version-specific delta. This candidate
is **not** adopted. Its complete packet, output and ratings are in
`results/source-patch/v1/`.

## V2: preserve the established fact path; patch original basis references

The rejected v2 adapter is `team_memory/decision_patch.py` (not the default path):

1. Use [vLLM0.8.5 guided JSON](https://docs.vllm.ai/en/v0.8.5/features/structured_outputs.html)
   to extract only explicit decision and basis **sentence references** from old
   records. The extractor receives no incoming report or QA question. There is no
   generic normalized `value` slot in which an action can replace a premise.
2. Run the established `source_comparison.py` factual comparator with the same
   input and prompt as v3b. Preserve its unrelated fact corrections/conflicts and
   informational coexistence. Candidate assertions overlapping a recognized
   decision/basis endpoint are retained in the audit but routed to the decision
   path; they cannot be stored as corrections of that historical decision.
3. For those decisions, guided JSON proposes at most one RFC6902 replacement of
   `/basis`, referencing incoming source sentences. It cannot edit `/decision`,
   choose a relation kind, or approve anything. A changed basis yields
   reconsideration. Unchanged/not-addressed yields no proposal; uncertain remains
   visible abstention. Exact repeated basis text is a no-op even with a new source
   ID. The explanation renders the old and new original evidence, instead of
   repeating an unsupported model assertion that a new version falsifies an old one.

The `jsonpatch` and `jsonpointer` packages are used directly, unmodified, including
their licenses in the offline execution packet. Graphiti/Trustcall's full services
are not imported. The source/type gate and update orchestration are our adapters.
An HTTP-boundary test caught that LlamaIndex's `additional_kwargs` overrode a
per-call `extra_body`; a shallow configuration copy now sends `guided_json` while
preserving the shared trace client and `enable_thinking=False`. QA receives no
guided schema or changed configuration. This is an implementation detail that
prompt wording alone would not fix.

Facts cost two comparison calls (old-only decision scan + existing comparison);
decision inputs cost three. No new answer writer, judge loop, keyword rule,
case-ID route, or automatic approval is added. The old normalized-value adapter
is retained for v1 replay only. No persistent extraction cache is claimed.

V2 execution120394 recovered two grounded reconsideration proposals, but extracted
ordinary schedule/temperature/retention/interval facts and a measurement as reasoned
decisions. Four correct fact corrections became reconsideration; JPEG/PNG
coexistence became an unnecessary proposal. One negative failed with a placeholder
source ID. All20 legacy answers/evidence survived; state8 core answers were7/8,
but only2/8 retained the intended correction relation and its review evidence.
The clear value regression was40C after approval instead of45C. Correct JSON and
valid source offsets do not establish correct endpoint semantics. Neither this run
nor v1 isolates an intrinsic Qwen model limit from extraction-contract limitations.

`service.py` has been restored byte-for-byte to the prior v3b version. The default
comparison is `source_comparison.py`; the new adapters are experimental artifacts.
The generic receipt audit fields remain optional and do not affect the default
comparator. Restoration is verified by11 recorded comparison calls and16 exact
review-source snapshots; that is deterministic replay, not additional fresh QA.

## Limits and fixed validation

Old-only extraction prevents incoming text from changing the **input** to the old
extraction; it does not prove the extractor chose the correct premise. Semantic
equivalence, attribution and relevance still require model judgment. Identical
text is the only automatic equivalence fast path; paraphrases are not guaranteed.
Multiple changed attributes in one source can hit the existing
four-proposal/duplicate-target contract and must report an error, not silently drop
an update. A premise-free decision cannot generate grounded reconsideration here.

Use the unchanged full-source20 plus17 known synthetic QA states (including the
specified state8). Same Qwen3-8B revision/nonthinking/temp0 and same QA reader.
Rate positive kind+premise evidence, unnecessary negative proposals, core answers,
original supporting evidence, and actual owner-state citations separately. The
same repeated cases are regression diagnostics, not a held-out benchmark. One
bounded v2 execution after the recorded v1 failure; preserve failures instead of
editing the answer key or spinning through prompt variants. Transient stores move to node-local disk; complete result
objects and exact requests/responses remain exported to Ceph and frozen locally.
