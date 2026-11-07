# LongMemEval reuse

Upstream: xiaowu0162/LongMemEval, commit 9e0b455f4ef0e2ab8f2e582289761153549043fc.
MIT copyright 2024 Di Wu; original LICENSE retained.
Original retrieval and generation files retained for audit, not executed as scripts.

contriever.py extracts the flat-contriever computation: original masked mean pooling,
unnormalized inner product, descending ranking. Changes: explicit local snapshot,
batch16 instead of128, corpus embeddings cached once rather than per query,
explicit eval(), truncation counts, and original witness objects returned.
Same original Qwen-tokenized 512/64 chunks as our BM25 comparison, rather than
LongMemEval's native user-only session/turn dataset transformation. All team speakers
are retained. Retrieval keys are original text, not generated facts.

reference_documents.py adapts the direct/con instructions and chronological
presentation to multi-person records and ALCE document IDs. This is a task adapter,
not an exact reproduction of LongMemEval's published scores or generation template.
