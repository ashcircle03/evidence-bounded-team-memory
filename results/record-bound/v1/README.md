# Records bound extraction: fixed-gold comparison

Job `122986`. Default adoption: **False**.

[한국어 원인 분석과 채택 판단](ANALYSIS.md)

Gold, scorer, input source bytes, Qwen3-8B revision and decode settings were held fixed. The nested extraction contract, examples, source segment IDs and compiler are the intervention. Controls are 136 cached actual calls; the candidate has 68 new calls. This is records-only development evidence, not QA accuracy or held-out generalization.

## Full-document quality

| Panel | Arm | Stage | Content recall | Root recall | Link P / R / F1 | Complete | Extra rows | Boilerplate | Overmerged pairs | Wrong stance |
|---|---|---|---:|---:|---|---:|---:|---:|---:|---:|
| balanced_synthetic | simple | raw | 225/243 (92.6%) | 94.4% | 76.9% / 12.3% / 21.3% | 11/54 | 0 | 0 | 35 | 17 |
| balanced_synthetic | simple | compiled | 222/243 (91.4%) | 93.8% | 83.3% / 12.3% / 21.5% | 11/54 | 0 | 0 | 35 | 29 |
| balanced_synthetic | ours | raw | 243/243 (100.0%) | 99.4% | 61.2% / 50.6% / 55.4% | 28/54 | 10 | 0 | 0 | 2 |
| balanced_synthetic | ours | compiled | 207/243 (85.2%) | 85.8% | 64.2% / 42.0% / 50.7% | 23/54 | 10 | 0 | 0 | 16 |
| balanced_synthetic | bound | raw | 243/243 (100.0%) | 100.0% | 75.0% / 55.6% / 63.8% | 20/54 | 1 | 0 | 0 | 3 |
| balanced_synthetic | bound | compiled | 243/243 (100.0%) | 100.0% | 75.0% / 55.6% / 63.8% | 21/54 | 1 | 0 | 0 | 3 |
| natural_audit | simple | raw | 73/93 (78.5%) | 84.4% | 42.1% / 16.7% / 23.9% | 0/14 | 1 | 0 | 27 | 10 |
| natural_audit | simple | compiled | 54/93 (58.1%) | 62.2% | 50.0% / 8.3% / 14.3% | 0/14 | 1 | 0 | 17 | 18 |
| natural_audit | ours | raw | 90/93 (96.8%) | 97.8% | 58.3% / 29.2% / 38.9% | 0/14 | 11 | 10 | 10 | 3 |
| natural_audit | ours | compiled | 76/93 (81.7%) | 82.2% | 58.8% / 20.8% / 30.8% | 0/14 | 10 | 8 | 4 | 7 |
| natural_audit | bound | raw | 91/93 (97.8%) | 97.8% | 93.3% / 29.2% / 44.4% | 0/14 | 6 | 8 | 5 | 4 |
| natural_audit | bound | compiled | 91/93 (97.8%) | 97.8% | 93.3% / 29.2% / 44.4% | 0/14 | 6 | 8 | 5 | 4 |

`simple`: previous simple extraction; `ours`: previous grouped extraction; `bound`: new parent-bound extraction. `raw`: actual model JSON before compilation; `compiled`: stored graph. Extra rows count unmatched output rows, not every semantic error. Typed-edge FP, wrong stance and overmerging are separate. Content recall only establishes that required words/meaning-bearing anchors are present somewhere; it does not establish correct attachment.

## Item preservation and adoption

- balanced_synthetic: retained nodes 207/207; retained edges 22/34; old complete documents retained 17/23; newly recovered nodes 36, edges 23.
- natural_audit: retained nodes 74/76; retained edges 8/10; old complete documents retained 0/0; newly recovered nodes 17, edges 6.

```json
{
  "protected_nodes_preserved": false,
  "protected_edges_preserved": false,
  "complete_documents_preserved": false,
  "source_integrity": true,
  "transport": true,
  "nondecreasing_relation_f1": true,
  "improved_relation_f1": true
}
```

The gate was specified before inspecting candidate output. No per-case selection or gold-guided merging of two methods is used. If any gate fails, the new extractor stays opt-in and the existing default is retained.

## Compilation and persistence

- simple: raw→stored lost required nodes 22; lost required links 4.
- ours: raw→stored lost required nodes 50; lost required links 11.
- bound: raw→stored lost required nodes 0; lost required links 0.
- Candidate extraction status: {'annotated': 68}.
- Candidate append/restart/reader transport: 68/68; full source and metadata exactly retained.
- All 136 previous case/arm scores reproduced exactly with the new representation adapter.
- A passing transport check means that stored information reaches the reader; it does not mean the LLM extracted all correct information.

## Cost and limits

- Candidate token usage: {"prompt_tokens": 99363, "total_tokens": 122552, "completion_tokens": 23189}.
- Candidate program time including client setup/transport: 788.23 seconds. Slurm total including preparation is in `slurm.txt` and `verification.json`.
- 54 synthetic documents = 18 story families × three focal-evidence variants; nine predefined difficulty/availability cells remain six documents each. The 18 families also share six semantic templates. These are not 54 independent real-world situations.
- 14 natural messages come from five failure-selected EverMem cases, so they are an audit panel rather than a representative benchmark estimate.
- Availability describes two focal qualifiers, not whether the entire document has any extractable facts. All substantive original facts remain in the fixed gold.
- Single-agent gold with finite anchors/spans; no independent human adjudication or unrestricted semantic entailment. Stated/inferred basis labels are retained, but their full semantic correctness is not comprehensively scored.
- No new QA calls, training, paid API or dataset replication. No claim that existing QA answer accuracy was remeasured here.

## Artifacts

- [Design and integration](../../../docs/records-bound-extraction.md)
- [Fixed protocol](../../../evaluation/record_bound/PROTOCOL.md)
- [Per-document sources, outputs and error sets](cases.md)
- [Difficulty and availability cells](strata.md)
- [Machine-readable scores and preservation](evaluation.json)
- [References](references.json), [source/input freeze](freeze.json), [comparison freeze](comparison-freeze.json)
