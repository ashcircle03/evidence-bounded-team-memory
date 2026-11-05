# Local Qwen3 compatibility review

Checked 2026-11-05 against official documentation, pinned source, and package metadata. This is a compatibility recommendation, **not an executed installation or performance result**. Qwen3-8B is a replacement actor for a new paired experiment; it is not established as equivalent to the paper's GPT-4o-mini. Previous BAZE results must remain separate.

## Candidate environment

Use a separate conda environment with Python 3.11, `vllm==0.8.5.post1`, and `transformers==4.51.3`. Do not upgrade the existing CUPMem environment in place. The pinned vLLM requirements specify `torch==2.6.0`, `torchaudio==2.6.0`, `torchvision==0.21.0`, `xformers==0.0.29.post2`, and `transformers>=4.51.1`; let the environment resolve that matching stack, then preserve the actual resolved package list. [CUDA requirements](https://github.com/vllm-project/vllm/blob/v0.8.5.post1/requirements/cuda.txt), [common requirements](https://github.com/vllm-project/vllm/blob/v0.8.5.post1/requirements/common.txt).

PyPI declares Python `>=3.9,<3.13`. The Linux x86-64 wheel is `vllm-0.8.5.post1-cp38-abi3-manylinux1_x86_64.whl` (326,421,557 bytes), SHA256 `b7f0dbd46f82aac6b2e7489c2bbf1c90fdc2e56d3f1fff44549951db40814d5a`. This is wheel metadata, not a local download verification. [PyPI release metadata](https://pypi.org/pypi/vllm/0.8.5.post1/json).

The pinned build's default CUDA version is 12.4. CUDA 12.x minor compatibility has Linux driver minimum 525.60.13; the driver shipped with CUDA 12.4 GA is 550.54.14, or 550.54.15 for Update 1. These are different thresholds, so do not infer runtime success from the lower number alone. Aurora's allocated GPU driver and actual imports/kernels still need checking. [Pinned build configuration](https://github.com/vllm-project/vllm/blob/v0.8.5.post1/setup.py), [NVIDIA compatibility table](https://docs.nvidia.com/cuda/archive/12.4.1/cuda-toolkit-release-notes/index.html).

RTX 3090 has compute capability 8.6, exceeding vLLM 0.8.5's minimum 7.0. Use the original BF16 checkpoint for this candidate. This establishes architecture eligibility, not available memory or working inter-GPU communication. [NVIDIA GPU table](https://developer.nvidia.com/cuda/gpus), [vLLM 0.8.5 GPU installation](https://docs.vllm.ai/en/v0.8.5/getting_started/installation/gpu.html).

## Candidate server and request settings

Qwen's versioned deployment guide supports vLLM >=0.8.5 and documents non-thinking requests. In 0.8.5, **omit both reasoning parser flags** when sending `enable_thinking=False`. The guide documents YaRN factor 4 for 131,072 tokens and warns that static YaRN may affect short-context performance. Keep the same model/runtime in both paired arms and disclose this extension. Avoid the FP8 checkpoint on this version/3090 combination. [Qwen v3 deployment guide](https://qwen.readthedocs.io/en/v3.0/deployment/vllm.html).

Run the following only inside the authorized two-GPU Slurm allocation, after activating the separate environment. `QWEN_MODEL_PATH` must be the downloaded, revision-recorded original checkpoint under `/local_datasets`.

```sh
VLLM_USE_V1=1 vllm serve "$QWEN_MODEL_PATH" \
  --served-model-name Qwen/Qwen3-8B \
  --host 127.0.0.1 --port 8000 \
  --dtype bfloat16 \
  --tensor-parallel-size 2 \
  --distributed-executor-backend mp \
  --max-model-len 131072 \
  --rope-scaling '{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}' \
  --gpu-memory-utilization 0.90 \
  --max-num-seqs 1 \
  --enable-chunked-prefill \
  --max-num-batched-tokens 4096 \
  --enforce-eager \
  --guided-decoding-backend xgrammar \
  --generation-config vllm
```

The small prefill batch and eager execution are proposed memory controls, not measured optimal settings. `--generation-config vllm` prevents loading checkpoint-specific generation defaults; send the experiment's explicit sampling and output limits on each request. The flags above are present in the pinned implementation, and xgrammar is a supported V1 backend. [Pinned argument definitions](https://github.com/vllm-project/vllm/blob/v0.8.5.post1/vllm/engine/arg_utils.py), [backend configuration](https://github.com/vllm-project/vllm/blob/v0.8.5.post1/vllm/config.py).

Every HTTP chat request must contain `"chat_template_kwargs":{"enable_thinking":false}`. With the OpenAI Python client, put that field in `extra_body`. Route only to the local server; no BAZE/OpenAI hosted inference is part of this setup.

## JSON compatibility and original behavior

The pinned OpenAI chat protocol accepts both `response_format.type="json_object"` and `"json_schema"`. The latter accepts `name`, `schema`, and `strict`; the code passes the schema to guided decoding. The `strict` boolean is accepted but is not separately used in that conversion, so this is not proof of complete OpenAI strict-schema equivalence. [Pinned chat protocol](https://github.com/vllm-project/vllm/blob/v0.8.5.post1/vllm/entrypoints/openai/protocol.py).

The pinned xgrammar validator rejects some schema features, including array `minItems`/`maxItems`, `uniqueItems`, string `format`, and object `patternProperties`. Compile/check the actual schemas used before a scored run. A valid JSON object does not establish semantic correctness. [Pinned xgrammar validator](https://github.com/vllm-project/vllm/blob/v0.8.5.post1/vllm/v1/structured_output/backend_xgrammar.py).

Local inspection of CUPMem revision `ea7d391103a151927cd29d2f01d87597a782bdcb` found `call_json_with_schema` defined in `cup_mem/llm_layer/client.py:485` and `responses_adapter.py:416`, with **no call sites elsewhere in the pinned upstream Python tree**. The chat implementation uses standard `response_format` with `strict=True` when invoked, but catches errors and falls back to prompt-only JSON. Ordinary `call_json` also has its original repair/retry behavior. STALE's evaluator explicitly uses `json_object`. Preserve these original behaviors and log the actual path; do not label all native CUPMem calls schema-constrained or silently add constraints to every call.

## Checks needed before execution claims

1. Record allocated GPUs, driver, `torch.version.cuda`, package versions, checkpoint revision, and server launch options. Confirm BF16 loading and TP2 communication on the actual node.
2. Exercise non-thinking text, JSON object, and the actual schema path; preserve raw bodies, responses, errors, fallback attempts, and finish reasons. Confirm no reasoning parser is enabled.
3. Count each exact chat-template input with the pinned Qwen tokenizer and enforce `prompt_tokens + requested_max_tokens <= 131072`. The local STALE wrapper retains an upstream 125,440-token input limit based on a different tokenizer; it is not a Qwen-context guarantee. A hypothetical 8,192-token output allowance already makes 125,440 + 8,192 exceed 131,072. Do not silently drop source turns or rewrite the experiment to fit.
4. Check the server's reported KV capacity and one representative long input before the scored run. From the official model's 36 layers, 8 KV heads, and head dimension 128, BF16 KV storage for one 131,072-token sequence is approximately 18 GiB total, or 9 GiB/GPU under TP2, excluding weights, activations, allocator, and communication overhead. This calculation suggests feasibility on two 24 GiB cards but does not establish it. [Official model configuration](https://huggingface.co/Qwen/Qwen3-8B/blob/main/config.json).
5. If the fixed configuration fails, retain failure evidence and distinguish runtime compatibility from CUPMem or QA quality. Do not silently enlarge resources, shorten the histories, substitute quantization, or combine the new actor's scores with the old BAZE pilot.
