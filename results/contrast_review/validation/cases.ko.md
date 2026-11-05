# 보고별 재검토와 구별 근거

원문 혼합과 같은 보고의 음성 대조를 함께 표시했다. 표시가 가려진 자료, 단일 후보, 역순의 결과까지 포함한 전체 원출력은 [cases.json](cases.json)에 있다.

## hook

The invoked_hook flag/output is not forwarded from run_commit_hook to run_hooks_opt; later code therefore cannot reliably tell if the hook ran.

The alternative migrates the pre-commit and prepare-commit-msg hooks to hook.h; library migration is distinct from passing back the invoked flag.

[과거 결정](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede) · [비슷한 결정](https://github.com/git/git/commit/f443246b9f29b815f0b98a07bb2d425628ae6522) · [새 보고](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

**simple** · 과거 대상 선택 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — ran the "pre-commit" hook and it modified the index, but hook_exists() returns false later on (e.g., because the hook itself went away, the directory became unreadable, etc.).
- 새 보고 — ==31275== Conditional jump or move depends on uninitialised value(s) ==31275== at 0x43C63F: prepare_to_commit (commit.c:1058) ==31275== by 0x4396A5: cmd_commit (commit.c:1722) ==31275== by 0x407C8A: run_builtin (git.c:465) ==31275== by 0x406741: handle_builtin (git.c:718) ==31275== by 0x407665: run_argv (git.c:785) ==31275== by 0x406500: cmd_main (git.c:916) ==31275== by 0x510839: main (common-main.c:56) ==31275== Uninitialised value was created by a stack allocation ==31275== at

**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — Fix a Time-of-check to time-of-use (TOCTOU) race in code added in 680ee550d72 (commit: skip discarding the index if there is no pre-commit hook, 2017-08-14).
- 새 보고 — Fix a regression in a8cc5943338 (hooks: fix an obscure TOCTOU "did we just run a hook?" race, 2022-03-07): The "invoked_hook" variable passed to run_commit_hook() wasn't passed forward to run_hooks_opt(), as push_to_checkout() in that commit correctly did.

The report reveals a failure in the fix where the "invoked_hook" variable was incorrectly not passed forward from run_commit_hook() to run_hooks_opt() despite push_to_checkout() correctly doing so in the original commit a8cc5943338 (hooks: fix an obscure TOCTOU "did we just run a hook?" race, 2022-03-07), necessitating a recheck of this specific implementation detail.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**referenced-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 keep

- 과거 결정 — Let's also change this for the push-to-checkout hook. Now instead of checking if the hook exists and either doing a push to checkout or a push to deploy we'll always attempt a push to checkout. If the hook doesn't exist we'll fall back on push to deploy. The same behavior as before, without the TOCTOU race. See 0855331941b (receive-pack: support push-to-checkout hook, 2014-12-01) for the introduction of the previous behavior.
- 새 보고 — Fix a regression in a8cc5943338 (hooks: fix an obscure TOCTOU "did we just run a hook?" race, 2022-03-07): The "invoked_hook" variable passed to run_commit_hook() wasn't passed forward to run_hooks_opt(), as push_to_checkout() in that commit correctly did.
- 비슷한 결정 — Move these hooks hook away from run-command.h to and over to the new hook.h library.
- 귀속 표현 — hooks: fix "invoked hook" regression in a8cc5943338

The regression occurred because the "invoked_hook" variable, which was correctly passed to run_commit_hook() in push_to_checkout() in the earlier commit, was omitted when calling run_hooks_opt(), leading to potential incorrect hook execution.

판정 — run_hooks_opt로 전달하지 않은 점은 맞지만 push_to_checkout가 run_commit_hook에 전달했다고 서술해 올바른 병렬 경로를 잘못 연결했다.

The other decision addresses moving hooks to a new hook.h library, which differs from the specific operation in the incoming report about fixing a regression in handling the "invoked_hook" variable.

판정 — 훅 라이브러리 이동과 invoked_hook 값 전달 문제를 다른 작업으로 정확하게 구별했다.

## header

The enum error from unpacking is mishandled: fsck/caller tries to parse an uninitialized header or reports a parse failure instead of an unpack failure.

The alternative distinguishes the oversized-header result (and the allow-unknown-type fallback); it is not the handling of generic unpack failure before parsing.

[과거 결정](https://github.com/git/git/commit/3b6a8db3b03adb118bfafb90bbc710068dbd6d14) · [비슷한 결정](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71) · [새 보고](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

**simple** · 과거 대상 누락 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — Split up the return code for "header too long" from the generic negative return value unpack_loose_header() returns, and report via error() if we exceed MAX_HEADER_LEN.
- 새 보고 — Fix a regression in my 3b6a8db3b03 (object-file.c: use "enum" return type for unpack_loose_header(), 2021-10-01) revealed both by running the test suite with --valgrind, and with the amended "git fsck" test.

**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — In a preceding commit we changed and documented unpack_loose_header() from its previous behavior of returning any negative value or zero, to only -1 or 0.
- 새 보고 — Fix a regression in my 3b6a8db3b03 (object-file.c: use "enum" return type for unpack_loose_header(), 2021-10-01) revealed both by running the test suite with --valgrind, and with the amended "git fsck" test.

The reported failure reveals that the change in the return type from an enum to any negative value or zero in the function unpack_loose_header() in object-file.c (commit 3b6a8db3b03, 2021-10-01) may have introduced a regression, necessitating a recheck of the rationale behind this decision.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**referenced-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 keep

- 과거 결정 — In a preceding commit we changed and documented unpack_loose_header() from its previous behavior of returning any negative value or zero, to only -1 or 0.
- 새 보고 — Fix a regression in my 3b6a8db3b03 (object-file.c: use "enum" return type for unpack_loose_header(), 2021-10-01) revealed both by running the test suite with --valgrind, and with the amended "git fsck" test.
- 비슷한 결정 — As a test added earlier in this series in t1006-cat-file.sh shows we'll correctly emit zlib errors from zlib.c already in this case, so we have no need to carry those return codes further down the stack. Let's instead just return ULHR_TOO_LONG saying we ran into the MAX_HEADER_LEN limit, or other negative values for "unable to unpack <OID> header".
- 귀속 표현 — object-file: fix a unpack_loose_header() regression in 3b6a8db3b03

The regression occurred because the function unpack_loose_header() was incorrectly allowed to return any negative value or zero after being previously restricted to only return -1 or 0, leading to inconsistent behavior that was not caught by the test suite.

The other decision addresses returning negative values or zero, differing from the specific operation in the incoming report which now returns ULHR_TOO_LONG or other negative values.

판정 — 너무 긴 헤더의 특수 반환값을 들어오는 보고의 새 동작이라고 설명해 대안과 보고의 역할을 뒤집었다.

## reflog

The switch to lookup_commit makes null_oid yield non-NULL for an empty reflog, leading to an erroneous parse/error; preserve empty reflog handling.

The alternative tolerates missing referenced objects in --stale-fix mode, distinct from handling a null OID while expiring an empty reflog.

[과거 결정](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed) · [비슷한 결정](https://github.com/git/git/commit/c809798b2acf1afdeeea02a9175677590ad8d689) · [새 보고](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

**simple** · 과거 대상 선택 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — None of our tests cover the case where "commit" is NULL after this lookup.
- 새 보고 — Fix a regression in my daf1d8285ee (reflog expire: don't use lookup_commit_reference_gently(), 2021-12-22), in changing from lookup_commit_reference_gently() to lookup_commit() we stopped trying to call deref_tag() and parse_object() on the provided OID, but we also started returning non-NULL for the null_oid().

**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — I don't think we've ever found tags that we need to recursively dereference in reflogs, so this should at least be changed to a "lookup commit" as I'm doing here, although I can't think of a way where it mattered in practice.
- 새 보고 — Fix a regression in my daf1d8285ee (reflog expire: don't use lookup_commit_reference_gently(), 2021-12-22), in changing from lookup_commit_reference_gently() to lookup_commit() we stopped trying to call deref_tag() and parse_object() on the provided OID, but we also started returning non-NULL for the null_oid().

The report reveals a change from using `lookup_commit_reference_gently()` to `lookup_commit()` where stopping attempts to call `deref_tag()` and `parse_object()` on the provided OID led to returning a non-NULL value for `null_oid()`, indicating a potential failure in dereferencing tags in reflogs that needs reevaluation.

판정 — null_oid 반환 변화는 언급하지만 문제를 빈 로그가 아니라 태그 역참조의 실패로 돌렸다.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**referenced-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 keep

- 과거 결정 — In the initial implementation of "git reflog" in 4264dc15e19 (git reflog expire, 2006-12-19) we had this lookup_commit_reference_gently().
- 새 보고 — Fix a regression in my daf1d8285ee (reflog expire: don't use lookup_commit_reference_gently(), 2021-12-22), in changing from lookup_commit_reference_gently() to lookup_commit() we stopped trying to call deref_tag() and parse_object() on the provided OID, but we also started returning non-NULL for the null_oid().
- 비슷한 결정 — Whenever a user runs `git reflog expire --stale-fix`, the most likely reason is that their repository is at least _somewhat_ corrupt. Which means that it is more than just possible that some objects are missing.
- 귀속 표현 — Fix a regression in my daf1d8285ee (reflog expire: don't use lookup_commit_reference_gently(), 2021-12-22), in changing from lookup_commit_reference_gently() to lookup_commit() we stopped trying to call deref_tag() and parse_object() on the provided OID, but we also started returning non-NULL for the null_oid().

The regression occurred because returning non-NULL for the null_oid() after removing the calls to deref_tag() and parse_object() led to incorrect handling of NULL OIDs in reflog expiration, potentially leading to dereferencing invalid objects.

판정 — null_oid에서 non-NULL을 반환하는 문제는 짚었지만 실제 빈 reflog의 파싱 오류 대신 유효하지 않은 객체 역참조 가능성을 근거 없이 추가했다.

The other decision addresses fixing a regression by switching from `lookup_commit_reference_gently()` to `lookup_commit()`, which differs from the specific operation in the incoming report by also stopping attempts to call `deref_tag()` and `parse_object()` on the provided OID.

판정 — 대안의 --stale-fix와 누락 객체 허용을 언급하지 않고 양쪽을 동일한 lookup 함수 변경으로 설명했다.

## prompt

The protected branch-name indirection assumes the shell expands PS1, but default zsh does not and shows the literal variable; condition the indirection on expansion.

The alternative displays an optional upstream branch name rather than changing whether the shell expands PS1.

[과거 결정](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f) · [비슷한 결정](https://github.com/git/git/commit/1f6806cf2da84e30d162ca3aee15d16db4f1daef) · [새 보고](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

**simple** · 과거 대상 선택 · 혼합 retest · 무관한 두 후보 invalid_output

- 과거 결정 — git-prompt.sh: don't put unsanitized branch names in $PS1
- 새 보고 — This fixes a regression introduced in commit 8976500 ("git-prompt.sh: don't put unsanitized branch names in $PS1"): zsh does not expand PS1 by default, but that commit assumed it did.

**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — Both bash and zsh subject the value of PS1 to parameter expansion, command substitution, and arithmetic expansion. Rather than include the raw, unescaped branch name in PS1 when running in two- or three-argument mode, construct PS1 to reference a variable that holds the branch name. Because the shells do not recursively expand, this avoids arbitrary code execution by specially-crafted branch names such as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.
- 새 보고 — Not all shells subject the prompt string to parameter expansion. Test whether the shell will expand the value of PS1, and use the result to control whether raw ref names are included directly in PS1.

The report reveals that not all shells expand the value of PS1, which was previously assumed, necessitating a recheck of how PS1 is handled across different shells to ensure raw ref names are not directly included, avoiding potential security risks.

판정 — 셸마다 확장이 다르다는 점은 찾았지만 어떤 셸에서 변수 간접 참조가 그대로 보이는지와 그 조건에서 필요한 변경을 누락했다.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**referenced-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 keep

- 과거 결정 — Both bash and zsh subject the value of PS1 to parameter expansion, command substitution, and arithmetic expansion. Rather than include the raw, unescaped branch name in PS1 when running in two- or three-argument mode, construct PS1 to reference a variable that holds the branch name. Because the shells do not recursively expand, this avoids arbitrary code execution by specially-crafted branch names such as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.
- 새 보고 — This fixes a regression introduced in commit 8976500 ("git-prompt.sh: don't put unsanitized branch names in $PS1"): zsh does not expand PS1 by default, but that commit assumed it did. The bug resulted in prompts containing the literal string '${__git_ps1_branch_name}' instead of the actual branch name.
- 비슷한 결정 — When working with multiple remotes, it is common to switch the upstream from a remote to another. Doing so, the prompt may not be the expected one. Providing an option to display tracking information sounds useful.
- 귀속 표현 — This fixes a regression introduced in commit 8976500 ("git-prompt.sh: don't put unsanitized branch names in $PS1"): zsh does not expand PS1 by default, but that commit assumed it did. The bug resulted in prompts containing the literal string '${__git_ps1_branch_name}' instead of the actual branch name.

The regression occurred because the fix assumed zsh would expand PS1 by default, whereas it actually requires the `set -o prompt` option enabled to do so, leading to prompts displaying the literal placeholder instead of the actual branch name.

판정 — 기본 zsh와 리터럴 변수 표시는 맞지만 두 근거 어디에도 없는 'set -o prompt'가 필요하다고 덧붙였다.

The other decision addresses displaying tracking information for branches across multiple remotes, which differs from the specific issue of fixing the default behavior of `zsh` expanding `PS1` without parameter expansion enabled in the incoming report.

판정 — 대안의 tracking 표시는 맞지만 기본 zsh가 확장을 하지 않는 문제를 확장 비활성 상태에서 zsh가 확장한다고 표현해 방향이 뒤집혔다.

## range

Moving diff configuration into range-diff stopped forwarding flags such as --no-patch or --stat; propagate caller options again.

The alternative sends output to diff_option.file instead of always stdout; output destination is distinct from option propagation.

[과거 결정](https://github.com/git/git/commit/73a834e9e27906a76940f1ced5c132bce205d3f8) · [비슷한 결정](https://github.com/git/git/commit/87f1b2d45ca7987cc6cc1a74eb66a77fa11fab94) · [새 보고](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

**simple** · 과거 대상 선택 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — range-diff: relieve callers of low-level configuration burden
- 새 보고 — In 73a834e9e2 ("range-diff: relieve callers of low-level configuration burden", 2018-07-22) we broke passing down options like --no-patch, --stat etc.

**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — There are a number of very low-level configuration details which need to be managed precisely to generate a proper range-diff. In particular, 'diff_options' output format, header suppression, indentation, and dual-color mode must all be set appropriately to ensure proper behavior.
- 새 보고 — As noted in a change leading up to this ("range-diff doc: add a section about output stability", 2018-11-07) the output is not meant to be stable. So this regression test will likely need to be tweaked once we get a "proper" --stat option.

The earlier behavior indicated that the output was not meant to be stable, as noted in a change adding a section on output stability (2018-11-07), revealing a circumstance where the regression test may need to be adjusted given the new evidence suggesting the output is inherently unstable.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**referenced-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


