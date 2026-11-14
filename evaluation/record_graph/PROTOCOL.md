# Record graph diagnosis v1 — freeze before new Qwen output

## Question
Does an explicitly linked, source-grounded record representation preserve the
claim/subject/conditions/reasons/time and epistemic distinctions required by
known downstream failures, without promoting extraction into authenticated state?

## Design and limits

- Five EverMem development failure families (14 previously recovered decisive
  messages), plus four synthetic contrasts (8 messages): 9 cases, 22 sources.
- The writer receives source text and metadata ONLY. No question, answer, gold
  role link, future source or hand-authored relation is provided to it.
- Source selection is oracle coverage from earlier diagnosis, not a retrieval
  benchmark. Existing examples are not unseen evaluation data.
- Same Qwen3-8B revision/nonthinking/temperature0 for construction and QA. The QA
  model and output budget are identical between raw and linked conditions.
- Both QA arms receive identical complete original sources and their metadata.
  Linked adds tentative ID-bound annotations. Thus QA differences diagnose
  representation, not successful recovery of previously missing source records.
- Writer output limit2048, QA output limit1024, context32768, physical request
  cap300, client3600s, startup900s. Additional annotation token/call costs are
  reported separately. No paid API, no retry or automatic resource expansion.
- Actual AnsweringAdapter and AttributedQA stages execute. Embeddings are a
  MockEmbedding because evidence is fixed and no retrieval runs in this test.
- The raw response/calls, source graphs, bundle, exact reader witnesses and final
  answer are saved. Existing QA20 is separately replayed with exact requests.

## Scores and attribution

1. Source/metadata/spans/links surviving records, restart, comparison input,
   retrieval packet and actual QA request: mechanical transmission, not semantics.
2. Provisional claim/role requirements in key.json: diagnose missing scope and
   wrong association. They are implementation-agent annotations, not independent
   gold and not exhaustive coverage of every source assertion. Never report full
   claim precision from this partial key. Human review is still required.
3. Inspect all extracted claims for unsupported role assignment, missed negation,
   author-vs-mention confusion, time invention and epistemic promotion. Correct
   substring IDs alone do not establish semantic correctness.
4. QA: compare answer, source-specific evidence, missing alternatives and state
   violations. Gold answers/requirements are never loaded by run.py. Do not count
   exact-request legacy replay as fresh QA accuracy.
5. Window-only expansion and model-linked expansion must be separated. The
   reference window is a context-recovery mechanism, not an automatic condition
   classifier. Full original fallback is retained for failed/empty extraction.

Do not change inputs, prompts, key or the first-run score after inspecting model
output. Describe ambiguous provisional requirements and report sensitivity
separately. Do not adopt linked as default if it introduces unsupported semantic
links/state promotion or loses previously correct answers. If original sources
work as well at lower cost, retain the simpler representation for that use.

## Graph/reference boundary

LlamaIndex0.14.25 SentenceWindowNodeParser executes directly; its joined window
text is mapped back to exact original offsets. The fact/evidence coupling of
LangChain's pinned FactWithEvidence is adapted to IDs, not fuzzy matching or a
claim that its full QA method is reproduced. Graphiti's episode provenance and
separate temporal semantics inform the schema; its database, entity resolution,
edge invalidation and retrieval do NOT execute. No latest-wins policy is added.
