# Records-only grouped extraction v1 — frozen before inference

Purpose: repair condition/reason binding upstream, without conflating availability
of the source with downstream QA correctness. No QA prompt or score changes.

30 sources: the previous 22 decisive source messages (14 EverMem development + 8
synthetic), plus 8 new implementation-authored synthetic controls. These are not
unseen natural benchmark data. Questions and keys never go to the writer.

38 new physical calls: grouped on all30, previous sentence-ID baseline on the8 new
controls. The prior22 baseline outputs are cached from122843 (same source, model,
seed42, temperature0, nonthinking,2048 output budget). Distinguish cached from new
runs and do not claim statistically reliable superiority or an isolated effect of
one mechanism. Grouped prompt/examples cost extra tokens, reported separately.
No retries or output-conditioned prompt edits. Failed sources retain original text
and all source spans; never count fallback raw text as successful role extraction.

15 predeclared partial probes, 5 on old failures and10 on new controls, measure:
- action anchor retained in a claim;
- specified exact text covered by that SAME claim's condition/basis links;
- absent role stays empty, unrelated target's context not attached;
- source/metadata/qualifications preserved through storage restart and actual
  reader evidence/witness construction (no new QA inference).
Coverage uses original character intervals, not normalized string matches.
All requirements must hold in one claim. The old10 diagnostic requirements stay
unchanged and are supplementary only. These partial keys do NOT establish overall
claim recall or semantic precision. Review ALL extracted claims against sources;
report incomplete caveats, wrong groups, stance errors and unresolved references.

Reference implementation: LangExtract1.7.2 real PromptTemplateStructured,
QAPromptGenerator, Resolver.resolve and Resolver.align. Adapt medication_group
example to claim_group. Align overlapping rows independently. Require exact
original bytes/character spans; reject fuzzy/normalized matches and repeated
ambiguous condition/basis spans. This is a core-component adaptation, NOT a
reproduction of its entire provider/chunking/multiple-pass pipeline. Keep source
complete and model annotations unverified; no authority/state events manufactured.

Existing QA20 /130request replay is a compatibility check, not fresh accuracy.
Previous exact-input QA failures (locked-account D→B; Friday→Monday; ConflictScore
IRRELEVANT despite halt=true) stay on a separate downstream-error list. No claim of
fixing them here. Existing8 questions/11 uncited spans are not erased.

Adoption: keep raw default. A grouped constructor can remain explicit opt-in if
contract/storage/trace checks pass. Do not promote it to authoritative knowledge or
QA default based on a partial diagnostic score. If new negative controls gain false
links, document and withhold default adoption even if positive coverage rises.
