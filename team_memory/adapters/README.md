# Concrete module adapters

Use [`runtime.connect_v2`](runtime.py) with the existing local model components,
an `AttributedQA` or `CitedSourceQA` factory, and a trusted caller context.

| Owner | File | Reused implementation |
|---|---|---|
| records | [records.py](records.py) | immutable Store, SourceStore validation, timeline reducer |
| relations | [relations.py](relations.py) | sentence selection and exact-span relation binding |
| retrieval | [retrieval.py](retrieval.py) | v2 RRF retrieval and review-context expansion |
| answering | [answering.py](answering.py) | v2 synthesis, checking, AQA, quote attribution |
| gateway | [gateway.py](gateway.py) | explicit ingest/review/ask orchestration |

[Runtime integration and migration limits](../../docs/modules/runtime.md) ·
[Versioned contracts](../../docs/modules/README.md) ·
[Measured verification scope](../../results/module-adapters/README.md).

The `legacy`/`reader_bridge` files contain shared representation conversion, not
another model. `base` owns envelope/error handling. Do not copy a second schema
or state reducer into an adapter. The old service v2 remains a separate entrypoint.
