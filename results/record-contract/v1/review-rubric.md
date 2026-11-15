# Manual review rubric fixed before reading new outputs

Reviewer: implementation agent; no independent human gold or inter-rater agreement.
Review each of30 sources, both arms, all accepted claims AND failed raw outputs.
Mechanical source alignment is not semantic correctness. The15 probes remain unchanged.

Record source text, generated role spans, basis qualifications, stance, and failure.
Check source-backedness, scope omission/wrong-target attachment, reasons falsely labeled
stated, unsupported inferred reasons, polarity/modality/attribution loss, unrelated
premises, and substantive omissions. Distinguish source-preserved-but-unlinked from
source text absent. A parsed but malformed source is not counted as correct extraction.
A valid inferred premise is not author-confirmed even if it plausibly supports a decision.

Trace every protected-probe regression to actual raw output, not only the final graph.
For hard5, say separately whether claim, applicability, reason and reason kind are present.
For version4 without an explicit causal connective, omit/inferred are permissible in
our new contract but do not silently alter the historical score or count abstention as
reason recovery. Polling premise and action are adjacent: qualify any reason as inferred.

All30-source review is qualitative. Report any new failures versus both fresh control
and historical extraction; do not convert a list of detected issues into full precision.
No prompt/runtime changes after inspection, no new model retries, no rescue arms.
