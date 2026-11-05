# 개발 사례별 설명 검사

각 원문 조각의 문자 범위는 개발 결과 JSON에 저장했다. 대조 문장의 순서는 기존 설명, 정확한 의역, 반대로 바꾼 의역, 사실인 원문 발췌다.

## hook

> Fix a regression in a8cc5943338 (hooks: fix an obscure TOCTOU "did we just run a hook?" race, 2022-03-07): The "invoked_hook" variable passed to run_commit_hook() wasn't passed forward to run_hooks_opt(), as push_to_checkout() in that commit correctly did.

- 보류 · The regression occurred because the "invoked_hook" variable, which was correctly passed to run_commit_hook() in push_to_checkout() in the earlier commit, was omitted when calling run_hooks_opt(), leading to potential incorrect hook execution.
  - unsupported nesting: run_commit_hook() in push_to_checkout()
- 보류 · The invoked_hook variable did not reach run_hooks_opt() from run_commit_hook(), while push_to_checkout() correctly forwarded it.
- 보류 · The invoked_hook variable did not reach run_commit_hook() from run_hooks_opt(), while push_to_checkout() correctly forwarded it.
- 허용 · The "invoked_hook" variable passed to run_commit_hook() wasn't passed forward to run_hooks_opt(), as push_to_checkout() in that commit correctly did.

수리 후 reassess
- subject · The "invoked_hook" variable · [160, 187)
- action · wasn't passed forward to run_hooks_opt() · [216, 256)
- condition · passed to run_commit_hook() · [188, 215)

## reflog

> Fix a regression in my daf1d8285ee (reflog expire: don't use lookup_commit_reference_gently(), 2021-12-22), in changing from lookup_commit_reference_gently() to lookup_commit() we stopped trying to call deref_tag() and parse_object() on the provided OID, but we also started returning non-NULL for the null_oid().

- 보류 · The regression occurred because returning non-NULL for the null_oid() after removing the calls to deref_tag() and parse_object() led to incorrect handling of NULL OIDs in reflog expiration, potentially leading to dereferencing invalid objects.
- 보류 · After switching to lookup_commit(), lookup of null_oid() started returning non-NULL.
- 보류 · After switching to lookup_commit(), lookup of null_oid() started returning NULL.
- 허용 · we also started returning non-NULL for the null_oid().

수리 후 reassess
- subject · lookup_commit() · [202, 217)
- action · started returning non-NULL · [308, 334)
- condition · for the null_oid() · [335, 353)

## prompt

> This fixes a regression introduced in commit 8976500 ("git-prompt.sh: don't put unsanitized branch names in $PS1"): zsh does not expand PS1 by default, but that commit assumed it did. The bug resulted in prompts containing the literal string '${__git_ps1_branch_name}' instead of the actual branch name.

- 보류 · The regression occurred because the fix assumed zsh would expand PS1 by default, whereas it actually requires the `set -o prompt` option enabled to do so, leading to prompts displaying the literal placeholder instead of the actual branch name.
  - option absent from evidence: -o
- 보류 · In default zsh, PS1 is not expanded, so the branch-name variable is shown literally.
- 보류 · In default zsh, PS1 is expanded, so the actual branch name is shown normally.
- 허용 · zsh does not expand PS1 by default, but that commit assumed it did.

수리 후 reassess
- subject · zsh · [383, 386)
- action · does not expand PS1 · [387, 406)
- condition · by default · [407, 417)
