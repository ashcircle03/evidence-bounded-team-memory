# Exact final execution packet

Byte-for-byte copies of the files submitted for job120370 (`cup-state-final-v1`).
Every payload hash is recorded in [freeze-final.json](../../../results/service-v3/freeze-final.json).
`code.tar.gz` contains the frozen actor/evaluator source, not current working-tree code.
`nltk-data.tar.gz` is the small prepared NLTK data bundle used by that run.

These are **historical execution files**, not a portable one-command installer.
The sbatch, conda paths, model/cache paths, account and client environment refer to Aurora.
Do not submit unchanged on a different machine. Model weights and full dataset caches are
not included. Use the [evaluation guide](../../../docs/evaluation-guide.md) to inspect stored
results without a model, or prepare a separate configuration for a fresh run.
Archive contents are limited to the explicitly frozen code/data. No credentials are required
for result verification. Copying this packet does not launch or resubmit a job.
