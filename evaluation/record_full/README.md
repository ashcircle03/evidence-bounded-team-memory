# Whole-document records gold and evaluation

Current report: [results/record-full/v3](../../results/record-full/v3/README.md).

- `gold.py` / `gold.json`: source-authored whole-document records, typed context, exact spans, optional inferred links and unresolved references. No model-output imports.
- `evaluate.py`: frozen v3 whole-source scoring of existing real Qwen outputs; no generation or production changes.
- `test_contract.py`: 147 gold-oracle, split-span and failure-mode checks.
- `verify.py`: original9-cell distribution, source intervals, frozen model requests/settings, compiler replay and provenance checks.
- `report.py`: human-readable full gold, raw outputs, error comparisons and stratum tables.
- `PROTOCOL.md`: annotation policy, exposure, scoring and version corrections.

```bash
.venv/bin/python -m evaluation.record_full.test_contract
.venv/bin/python -m evaluation.record_full.evaluate
NLTK_DATA="$PWD/.cache/reference-nltk" .venv/bin/python -m evaluation.record_full.verify
.venv/bin/python -m evaluation.record_full.report
```

The source documents remain `evaluation/record_strata/inputs.json`. Do not regenerate or overwrite the prior experiment. The current evaluator is frozen in `results/record-full/v3/freeze.json`. Prior versions and scores are kept for evaluator audit; make a new version before changing gold or primary scoring. This is retrospective development-set re-evaluation, not a held-out result. No fresh GPU inference is needed while inputs and extractors are unchanged.
