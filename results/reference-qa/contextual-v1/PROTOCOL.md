# Feedback retrieval and contextual attribution, development v1

Freeze implementation, inputs and scoring before new model outputs. Test the same ten EverMem questions and twenty historical QA cases. This is exposed development, not a blind benchmark or paper reproduction. Native gold answers and R labels stay local to scoring and never enter query generation, retrieval or reader inputs. Do not tune prompts on this run's outputs.

## Design

Reuse LlamaIndex0.14.25 BM25Retriever and QueryFusionRetriever (reciprocal rank fusion). Initial retrieval is the original whole-topic BM25 top8 with chunks512/64. One query-generation call receives the question and those eight original records, with author/time metadata. Generate three additional queries grounded in their known people/events/conditions. Search the original query and three generated queries against the same corpus with author/time included in the search key. Fuse to eight passages. This is one bounded relevance-feedback adaptation, not full IRCoT or LongMemEval reproduction. No gold-driven filters or per-question rules.

Reuse Attribute First content selection, then restore enclosing records for fusion-in-context. Use the existing LangChain QuotedAnswer schema and source/quote binder for final source-specific answers. Source metadata remains outside source text. Final citations can refer only to records actually shown at fusion. Unlocated selection quotes remain diagnostics; their source IDs can still identify original records for reading. Final quote validity and semantic entailment are separate checks.

The compact search/reader path is an optional contextual profile. Existing attributed QA remains the selected path until the new candidate passes the preservation gate.

## Fixed arms

| Scope | Arms |
|---|---|
| Ever10 | saved format-recovery claims baseline; reader_only (old8 + contextual reader); retrieval_only (new8 + unchanged claims reader); combined (new8 + contextual reader) |
| Existing20 | new contextual reader on the identical historical retrieved records; compare saved attributed20 and format-recovery claims17 |
| Selected attributed path | exact replay of the existing20 physical responses, separately labelled; retrieval is not rerun in this check |

All three new Ever arms share the question. The two new-retrieval arms share exactly the same eight passages. Retrieval receives Q only; multiple-choice options are provided only to readers. Verify original top8 reproduction. Topic01/02 full dialogue corpus, fixed revision a6b210a32248e841967b7b64a64281d2ff3f669d. Keep topics03–05 untouched. Existing20 uses fixed reader inputs, so preservation there is not evidence of end-to-end search preservation.

Qwen3-8B revision b968826d9c46dd6066d109eabc6255188de91218, BF16, nonthinking, temperature0, output1024, context32768. Expected at most110 calls, cap125, client1800seconds. GPU1/CPU8/RAM48G/wall40minutes, conda, no node pin or requeue, no paid API. The reservation fits the unchanged caps150/520/820 GPUminutes, including earlier failures. Stop on execution failure without enlarging resources automatically.

## Metrics and adoption

Use the unchanged historical keys and Ever A/options. Grade each output for answer correctness, required facts, all required supporting original passages, unsupported extras, retained author/date/condition, and valid literal citation spans. Main success requires the entire required answer and supporting evidence without unsupported additions. Keep full-passage support and narrowed quote support separate. Record reasons and exact evidence. The implementing AI reviews semantics; independent human adjudication is absent.

Also report Ever R-location recall and source sufficiency (enough/partial/absent, allowing clearly described metadata or date inference) separately from QA. Compare against the prior ten-question audit. Report lost as well as recovered successes, parser/partial status, calls/tokens and actual GPU elapsed including preparation.

Do not replace attributed unless all20 historical required answers and evidence are retained, combined Ever success exceeds the prior best supported2/10 without losing those prior successes, and the new answers do not invent conditions or authorship. If the gate fails, retain the baseline and report which component helps. No new adaptive experiment after scoring this run.
