# Claim evidence development comparison, v1

Freeze code, prompts, selection and criteria before any new Qwen outputs. No new answer-specific rule or retry after scoring. This is a development pilot, not a blind benchmark result or full paper reproduction.

## Question and arms

Does selecting evidence before generating claims recover distinct answers within one original source, while preserving existing answers and reducing the repeated review/rewrite/attribution path?

`joint`: unchanged one-pass AQA-intent/LangChain-schema reader. `claims`: published Attribute First content_selection -> fusion_in_context path adapted to typed evidence units and short source-attributed claims. Same Qwen3-8B revision, nonthinking, temperature0, output1024, context32768. The new candidate uses at most two calls for these fixed inputs. A valid quote proves source binding, not entailment or completeness.

## Frozen sample and comparison boundaries

| Set | Sample | Comparison |
|---|---|---|
| Historical QA | Existing20 | Fresh claims vs saved attributed20 and joint20; identical retrieved passages, metadata restored from original envelopes. Historical comparison, not a new paired end-to-end retrieval run. |
| Prior transfer | Existing12 | Fresh claims vs saved joint/attributed; same retrieved passages. Previously inspected diagnostic cases, not unseen data. |
| Pure order control | Two permutations | Identical complete manual/report blocks, headings, question, author and timestamp; only block order changes. Both readers. The earlier confounded order pair stays in historical12 only. |
| EverMemBench-Dynamic |10, one of each F_SH/F_MH/F_TP/MA_U/MA_P per topic01/02 | Both readers on the same whole-topic BM25 top8 witnesses. SentenceSplitter512/64, Qwen tokenizer. Query Q only, no gold references or answer options in retrieval. |
| WikiContradict |8 unique questions × single1/single2/both | Both readers, dataset-provided passages. This tests generation with supplied evidence, not retrieval. |

104 output records, at most172 ordinary model requests; hard cap220 and client2200seconds. The extra cap is an operational guard, not an authorization for adaptive experiments. Order-pair variants and three Wiki conditions are correlated, not independent questions. Alternate arm order. No paid API. GPU1/CPU8/RAM48G/wall45minutes; conda; no node pin or requeue.

Native selection: ascending SHA256(`claim-evidence-v1:` + question id), stratified by the five Ever types and topic; Wiki hashes `wiki:` + question_ID. Exclude Ever IDs already present in earlier pilot selection files. Existing samples may already have been inspected for format; no claim of blind heldout evaluation. Keep topics03–05 untouched for tuning. Preserve the pinned15-file manifest; original CSV has253 Wiki rows, not506 concatenated viewer rows.

## Metrics, scored separately

1. Answer correctness: frozen historical keys; native Ever A/options, Wiki answer1/answer2. Free-form answers require source-based semantic review; exact match/token F1 are proxies only. Report per type, not only pooled counts.
2. Claim support: does the exact attached evidence entail the whole claim, including subject, action, author and condition? Review every produced claim; unsupported extras are errors even when a required answer appears. Keep literal span validity separate.
3. Coverage: all required facts/conditions and (Wiki both) both source-specific answers with their own evidence. Also report unused selected spans. Selected-span coverage is not recall of all relevant corpus facts.
4. Retrieval: Ever native R location recall within the top8, separately from answer accuracy. R may include contextual lines, so this is not an entailment label. Wiki has no retrieval metric in this run.
5. Robustness: order-invariant source-specific answers; authorship vs mentions; no-answer abstention; unrelated records and different conditions must not be manufactured into conflicts. Relevant historical diagnostics remain separate from native dataset scores.
6. Interface: schema failures, incomplete/partial stages, stdout JSON validity, unknown citation IDs and quote matching. `ok` means structural success only, never certified semantic truth.
7. Cost: actual call counts, input/output tokens, elapsed time and allocated GPU elapsed including preparation/failures. Compare old saved cost with the fixed-context scope limitation.

Create a blinded review sheet from outputs and reference passages. Record reviewer identity and reasons. If only the implementing assistant reviews it, say so; independent human agreement has not been established. Do not call such scores official benchmark results.

## Decision and original evaluation commitments

Do not promote claims over the selected historical attributed path unless all20 prior required answers/evidence are preserved, the previously failing same-source answers are covered without false alternatives on negative controls, and the new native comparison does not lose joint's correctly supported answers. A pilot passing these gates only justifies a larger development run. Failure stops promotion; report the failure, do not extend tuning on these outputs.

Original dataset agreement (2026-11-04 memo): Ever581 development /876 final QA, Wiki253 rows, and a separately annotated chronological derivative (target20 development/60 test) for reconsideration/merge. This pilot implements both native readers and compatible scoring inputs. It does not silently substitute native MA_U QA for update accuracy, manufacture native merge labels, or claim the chronological annotations already exist. Existing Git/approval replay and Aimers reconstruction remain separate system-level checks. SpeakerMem-R1 remains the planned research comparator; joint is an engineering control, not a replacement reproduction.
