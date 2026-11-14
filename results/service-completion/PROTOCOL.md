# Service completion boundary check — fixed before new inference

Version cup-completion-v1. Qwen3-8B at the prior pinned revision, nonthinking,
temperature0. One local GPU, conda, Slurm12h, no node pin, no paid API. Maximum800
physical requests; fail rather than silently retry or increase resources.

Changes: rejected-state transport; explicit correction effect separate from proposal;
context quote separate from changed assertion; provenance retained through all active
QA stages; upstream ConflictScore completion limit4096 (bounded by actual remaining
context) replaces the local384 override. No new judge stage. This is a bundle,
not an ablation identifying each change's causal contribution.

20 legacy questions use FULL original record collections and fresh hybrid retrieval.
8 known diagnostic streams have11QA states.3 new authored streams have6QA states,
including restart, pending/approved/rejected, unchanged assertion and conflicting
owner votes. Total37QA outputs. New synthetic inputs and keys are fixed before
outputs; they are not a natural Git generalization benchmark. No expected labels
or key file is sent to actor/model. Fixture approvals are not real human actions.

Primary requirement: each core answer and its required source evidence is correct;
state claims require a stored review-state citation. Literal span validity is a
separate structural check. Rate against full original records, not keyword match.
Legacy20 must all preserve required answers/evidence. Changed assertions must not
invalidate unrelated owner facts. Negative reconsideration cases must not produce
unnecessary proposals of any kind. Count failed/partial responses and unused or
invalid source citations separately. Report calls, token counts, finish reasons,
walltime and actual allocated GPU duration including failures/preparation.

Use stored prior service-v3 output as historical diagnostic comparison only: its
legacy20 used fixed passages, while this run uses full retrieval. Do not claim a
paired causal gain from unlike inputs. The new6 are held out only from this edit's
known cases, not independently curated or human graded.

Stopping rule: inspect each failure against actual input/output. Do not relabel keys
or claim completion because existing code tests pass. This run decides whether the
headless module meets these boundaries; broad EverMem retrieval/natural QA and
production authentication remain separate capabilities. If a requirement fails,
preserve the result and report the specific remaining blocker.
