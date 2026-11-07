Prompt excerpts from lovodkin93/attribute-first-then-generate, commit cc7b995dfb288da7982ae388994f182bef030b75, few_shot_experiments/prompts/LFQA.json (Apache-2.0).

Reference: Attribute First, then Generate: Locally-attributable Grounded Text Generation, ACL 2024, https://aclanthology.org/2024.acl-long.182/.

Our adapter uses the published content_selection -> fusion_in_context two-stage path. It changes the textual output to typed evidence/claim lists, permits short answers, retains source metadata, and preserves conflicting source claims. It does not reproduce the original model, demonstrations, training, or benchmark results.
