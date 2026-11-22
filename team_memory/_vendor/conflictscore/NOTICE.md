Source: microsoft/ConflictScore@a8868e5cd98bff81935a1766b54a02ad3eab9e8f, eval_all_calibration.py. See LICENSE.

Local modification: exception diagnostics use Python logging (stderr) with the exception class instead of printing the error into stdout. This protects the JSONL interface and avoids logging request content. The original support-judgment prompt and label parser are retained. The adapter's output-token limit is configured outside this vendor file.
