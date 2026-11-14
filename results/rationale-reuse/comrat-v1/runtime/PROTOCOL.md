# Original CoMRAT pilot (frozen before model outputs)

Execute the released pages/commit.py:user_commit_page, helpers.preprocess,
helpers.load_models, Tokenizer fitting on released data, padding and >0.5
threshold unchanged. Only Streamlit input/output is replaced by headless calls;
weights are cached between documents. All token IDs/probabilities and output rows
are retained. No QA/review/service code import or modification. No new training,
threshold sweep, or Qwen prompt. Published example labels stay local for scoring.

1. Replay all 12 published predictions in the user-study CSV. Match the first
   row (the original already-preprocessed sentence is presented as a title).
   Retain any additional empty-body rows; report them as preprocessing artifacts.
   This is execution fidelity, NOT held-out accuracy. Compare human-vote labels
   separately and do not call the author's predicted labels ground truth.
2. Run the 22 complete raw old/new documents from our 11 known scenarios with
   upstream preprocessing. For the 11 old documents, assess whether both
   Decision and Rationale are detected (possibly in separate nonempty rows):
   4 reasoned decision records, 7 factual measurement/configuration records.
   Empty strings cannot provide evidence. Errors are failures, not negatives.
   This narrow authored diagnostic is NOT a natural benchmark; writer/cache
   source texts repeat across positive/negative reports.
3. Keep every source string and inspect whether preprocessing strips source
   context. A sentence label does not pair decisions with reasons or establish
   changed conditions, conflict, approval or reconsideration.

Candidate routing gate: published labels 24/24 reproduced, all 4 reasoned old
records detected, zero of 7 fact-only old records routed as reasoned decisions.
Even passing is only permission for a separate pair-level experiment, not adoption
in default service. If failed, do not prompt-tune the gate or rerun full QA.

GPU1 reserved; conda Python3.11; Slurm12h. Original TensorFlow2.13 dependencies.
Record whether TensorFlow actually uses GPU or CPU; allocation is not evidence of
GPU inference. Original requirements installed in an isolated environment only.
No paid API or GitHub credentials. Download/extract dataset/models on compute-node
/local_datasets and verify archive SHA256; no login-node computation.
