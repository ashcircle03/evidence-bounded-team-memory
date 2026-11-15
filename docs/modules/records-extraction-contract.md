# Records extraction: qualified, reusable links

This is an opt-in revision of `records/grouped.py`, not another pipeline stage.
It changes the extraction contract and examples while retaining LangExtract1.7.2's
prompt formatter, output resolver and exact token alignment. The controlled experiment
uses the same graph/v2 compiler and output schema in both fresh arms.

## Reference intent and adaptation

LangExtract's [medication-group example](https://github.com/google/langextract/blob/0e441bf77ddc3119dd0aa413322959234dd84ee5/docs/examples/medication_examples.md)
uses a shared, meaningful medication key to connect related dosage/frequency spans.
We use a short source quotation naming the target assertion as the group key.
The upstream resolver aligns extraction spans; it does not prove a causal relationship.
`condition`, `basis` and their semantics are our explicitly evaluated adaptation.
Upstream Gemini examples are not evidence that Qwen3-8B has equivalent capability.

| Contract | Why downstream needs it | Representation |
|---|---|---|
| Applicability is a distinct role even if already in the assertion/subject | A comparator should not have to rediscover a restriction hidden inside prose | Same original unit may be `claim`, `subject` and `condition` |
| Stated and inferred reasons are distinct | A plausible explanation must not become an author-confirmed justification | Per-basis-unit `stated`, `inferred` or legacy `unspecified` |
| A premise can support several assertions | One-to-one attachment can silently lose an explanation | Repeat the extraction row with another target group; compiled units are shared |
| One premise can constrain one assertion and explain another | Applicability and justification depend on the target | Roles belong to claim-to-unit links, not globally to the text unit |
| Original wording, negation, time, caveats and attribution survive | Later modules need to verify interpretation against the record | Original offsets/quotes and immutable source metadata; no normalized model text replaces the source |

## Reason boundary

`stated` requires an explicit explanatory connection to this target: “because”,
“therefore”, “for that reason”, purpose language or an equivalent explicit statement.
The supporting premise must still be present in the source. `inferred` denotes a
plausible relationship between a source premise and this assertion that the author did
not explicitly assert. If ambiguous, omit the relation. Omission does not count as
recovering a reason. `unspecified` preserves legacy output without guessing its type.

Both `stated` and `inferred` are **unverified model annotations**. “Stated” describes
what the extractor thinks the author said, not a verified fact. Neither updates the
review state or proves the proposition. Records never authorizes an approval, rejection,
correction or supersession. Original-source evidence and explicit review events remain
available to subsequent modules. QA output is not automatically written back as truth.

## Examples and alignment

The three examples in `contract_examples()` cover:

1. Battery-operated tablets: the restricted subject is also an applicability condition;
   the same explicitly cited wet-inlet premise supports two actions.
2. A closed canyon route followed by a postponed survey: the reason is marked inferred;
   an unrelated chair-color observation does not become a reason.
3. Station Z on solar power: section scope reaches later actions across an unrelated
   clock statement; an explicit broken-lamp reason and a future “Once…” condition
   attach to their own actions.

Examples contain no evaluation source text. Each of the17 extraction rows is checked
with upstream `validate_prompt_alignment` using no fuzzy/lesser matches. Runtime aligns
rows independently because shared/overlapping output spans are intentional. Upstream's
sequential whole-example check reports4 issues for repeated spans; these are retained
in `example-preflight.json`, not called a clean sequential preflight. Every example
source occurrence is unique. This difference from the sequential reference is deliberate.

## Contract version and transport

`records.graph/v2` adds a mandatory `basis_annotations` list to every claim:

```json
{"basis": ["u:..."],
 "basis_annotations": [{"unit_id": "u:...", "kind": "inferred"}]}
```

Every basis unit has exactly one annotation, in the basis-list order. No other units
may be annotated. These annotations participate in the immutable claim identity.
V1 graphs remain valid and unchanged; they are never silently upgraded or relabeled.
The module envelope remains `team-memory.modules/v1.2`; its source schema explicitly
accepts either nested graph version. A client that only understands graph/v1 must be
upgraded before consuming v2. This is not transparent compatibility for old clients.

The actual `record.append` → store restart → snapshot → evidence → reader witness
path preserves the graph, author/time metadata and basis qualifiers. `record_context`
includes the qualifiers. Packet transport is not proof that an LLM interprets them
correctly; the records experiment does not claim new QA accuracy.

## Failure and rollout

Missing/nonexact spans, ambiguous repeated context or orphaned context groups fail
construction; the full original text remains stored with `status=failed`. Unsupported
interpretations are not synthesized by a repair model. Canonical alignment stores the
original exact-token interval; mixed stance labels remain `unknown`. No source-specific
rules or new inference stages are used.

`construct_contract(source, generate, model=..., revised_input=True)` is explicit opt-in.
The default QA path stays unchanged. Adoption depends on the frozen comparison in
[evaluation/record_contract/PROTOCOL.md](../../evaluation/record_contract/PROTOCOL.md):
same30 sources/model/settings, fresh60 calls, same compiler/schema,15 existing probes,
all7 previously correct connections protected, and full output review. A protected
regression or false semantic link blocks default adoption. Small diagnostic results
cannot establish general precision, recall or benchmark superiority.
