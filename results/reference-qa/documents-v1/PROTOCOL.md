# Frozen document-reader development comparison

Same inputs as demonstrated-v1: legacy20 and Ever10, SHA256 040bf0a0b514a9534ddb0585d0319ae4c3125fd94b46f0c94094e55056f340ab.
Actor receives no answer, gold R, oracle, prior result, or question ID in prompts.
Legacy: fixed sources x direct/con. Ever: exact original BM25 top8 versus Contriever top8 on identical original chunks x direct/con. 80 one-call Qwen3-8B generations, temperature0, max1024, same32768 context; no silent truncation.
Contriever pinned2bd46a25019aeea091fd42d1f0fd4801675cf699, masked mean / unnormalized dot product from LongMemEval. Corpus embedding once before Qwen starts; GPU1, conda,12h. No optional retrieval gate.
All arms share metadata, chronological display and ALCE document-ID binding. Reading con adds brief extraction/reasoning inside the same request; direct does not. No fact expansion, reranking, query generation or online judge.
Primary: correct complete answer AND returned evidence supports every claim AND required evidence complete AND every citation relevant AND no unsupported extra AND structurally valid cited output. Quote-span accuracy is not applicable: source paragraph is returned deterministically. Report answer accuracy separately. Input evidence sufficiency is manual source review, not inferred from R recall.
Separate wrong author/group/time, unresolved alternatives, unnecessary citations and missing evidence in review reasons. Each claim reviewed with original source. Working notes are diagnostic, not final answer claims. Implementing-agent review is not independent human evaluation.
Adoption per reading: legacy20 all preserved, connected-v1 prior Ever successes preserved, Ever>3/10, dense beats same-reader BM25, no format/ID errors. If both qualify choose more Ever successes, tie direct. If neither qualifies keep selected attributed and record causes without changing this run or adding posthoc retries. Historical attributed score is not a fresh control.
Stop after this frozen80-call comparison and source-based decision; no claim of full benchmark or merge solution.
