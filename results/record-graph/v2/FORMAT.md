# Format-only recovery v2

The first frozen run emitted text values where sentence IDs were required.
v2 passes the SAME Pydantic extraction schema to vLLM 0.8.5 guided_json.
No prompt, source, question, role criteria, gold, model, token budget or QA arm
changes. No retry, coercion, string-to-ID guessing or semantic repair.
This is a development recovery after inspecting v1, not an independent test.
The first run remains reportable; failure rates are not erased.
Structured syntax does not establish semantic correctness. The same stop and
adoption criteria apply. No further semantic tuning is part of this run.
Reference: https://docs.vllm.ai/en/v0.8.5/features/structured_outputs.html
