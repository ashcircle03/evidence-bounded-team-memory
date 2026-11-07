# Review-state citations

The existing LangChain FactWithEvidence adapter accepts a second evidence type:
`review_state`. Original report evidence keeps its existing source IDs and byte
spans. A review citation refers to a deterministic rendering of an immutable
`review_snapshots/<id>.json` object, not a fabricated passage in a report.

The snapshot stores the validated timeline proposal, its reduced status, valid
owner vote objects and IDs, the visible original-source IDs and temporal scope.
`pending` is a state at this snapshot with no accepted vote, not an approval
activity. Approval is traceable to the exact stored owner vote. No event time is
invented because the existing vote format has no timestamp. A later vote produces
a different snapshot; earlier answer citations remain addressable.

The quote adapter adds numbered citations without rewriting the answer or old
citations. Ambiguous phrases that occur in several review snapshots are rejected.
Wrong/missing quotes remain `partial`; literal binding is not semantic proof.
Already numbered mixed factual/status sentences still need semantic evaluation:
a document citation alone does not substantiate approval. Snapshot creation does
not approve proposals and does not establish authentication of the actor.

This reuses the vendored [LangChain citation schema](reference-attribution.md).
The separation of source entities, review activities and responsible actors is
informed by [W3C PROV-DM](https://www.w3.org/TR/prov-dm/). We do not claim PROV
compliance, an upstream implementation of our voting policy, or a new verifier.

`python -m team_memory.service --reader direct ...` selects the same retrieved
sources, initial prompt, review context and citation adapter without the optional
document judge, answer rewrite and AQA repair. `--reader attributed` preserves the
previous checked path. The fixed comparison in `evaluation/service_v3/PROTOCOL.md`
decides which profile to recommend; profile selection is not case-ID routing.
