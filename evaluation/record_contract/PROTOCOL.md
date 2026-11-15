# Frozen input-contract comparison

Same30 sources as record-groups-v1b; no questions/gold at construction time.
Each source receives two fresh calls on same local Qwen3-8B b968826d, temperature0,
seed42, nonthinking,2048 output budget. Source order fixed; arm order alternates.
Total60 model calls; no retries. No new models, retrieval, QA checker or training.

Control: prior DESCRIPTION+two examples+a/b/c identifiers.
Revised: clarified extraction contract+three neutral examples+source-anchored group keys.
Common to BOTH: system instruction, JSON output schema (optional basis_kind on basis
rows), canonical alignment, ambiguity handling, graph/v2 compiler, source/metadata,
model and generation settings. Only input description/examples/group-key guidance
changes. This tests an input package, not independent contributions of each sentence.
Original historical output is not silently treated as the new control.

Graph/v2 attaches a stated/inferred/unspecified qualification to EVERY basis unit.
Missing old-prompt mode remains unspecified, never inferred automatically from words.
Both stated and inferred links are unverified model annotations; neither authorizes
review state. Original graph/v1 remains supported; existing records stay immutable.

Primary diagnostic: same frozen15 typed-role probes from prior run, with7 historical
correct probes protected as a fixed regression set. Report new control/revised and
historical preservation separately; do not replace old key or cherry-pick arms.
Version4's implicit reason remains an ambiguous gold requirement in this OLD score.
Separately measure whether unspoken reasons get promoted to stated. For version4 an
inferred relation OR abstention is allowed under the revised contract; abstention is
NOT counted as recovered reason coverage. Polling's inferred reason can support
coverage while remaining explicitly an inference. Compare stated/inferred types only
for matching target claims and actual required premise spans.

Review all newly extracted claims and all regressions against source. Count failures,
wrong-target links, spurious reasons, missing qualifiers, token usage and finish_reason.
Retain raw outputs and failure logs; do not tune after inspecting results. Test actual
storage/restart/reader packets with basis types, and existing QA20 exact-request replay
as compatibility only. No fresh QA accuracy claim.

LangExtract per-row exact preflight uses same independent overlap alignment as runtime.
Report upstream sequential warnings as well: repeated spans across targets/roles are
intentional and unique in the source. Every example row must independently align exactly.
This is a documented extension of the medication-group pattern, not a full reproduction
of upstream Gemini extraction or an established causal reason extractor.

Decision: do not promote a candidate that loses any protected7 connections. Even if
those are preserved, semantic failures/false stated reasons block default adoption.
Small development outcomes cannot establish broad semantic precision or generalization.
