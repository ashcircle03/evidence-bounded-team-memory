# Records construction

Question-independent, unverified annotations over immutable original text.

- `graph.py`: LlamaIndex sentence windows, legacy sentence-ID writer, common graph
  contract, exact-span validation and packet descriptions.
- `grouped.py`: LangExtract1.7.2 prompt/example formatter + resolver/alignment;
  attaches exact condition/reason/time/subject spans using claim groups and compiles
  into the SAME graph contract. `construct_aligned` preserves canonical original
  spans and keeps mixed group stance unknown; strict `construct` reproduces v1. Explicit opt-in, not QA default.

See [design and usage](../../docs/modules/records-grouped.md) and
[measured results](../../results/record-groups/README.md). `annotated` means the
extraction completed, not that its semantics or completeness are verified.
`failed` preserves the full source; no guessed state or authenticated review event
is emitted. These modules do not mutate existing source records.
