# Git 사례별 재검토 판정

고정 조건의 설명은 보류한 경우에도 별도 호출해 채점했다. 실사용 조건에서 보류한 행에는 전달한 설명이나 인용이 없다.

## git-alias-pos

When resolving CamelCased aliases in early config, names must match config keys case-insensitively; -h output is independent.

[과거 원문](https://github.com/git/git/commit/a9bcf6586d1a4888aea91553d73cda20494b8335) · [새 보고](https://github.com/git/git/commit/643df7e234dda47a4748311361a82df5415b7bc1)

### 고정한 근거

**original · earlier-first** · 재검토 누락

The earlier decision relied on the method of finding .git/ directories and resetting global state based on matching aliases; the report introduces concrete new evidence showing that alias names can be in CamelCase, thus changing the applicability of the earlier result, provided that alias names are consistently written in either all lowercase or all uppercase for the earlier method to remain valid.

설명 채점 — 대소문자 혼합을 언급하지만 모두 대문자나 소문자로 쓰면 과거 방법이 유효하다는 조건을 상상했다.

- 과거 — Instead of discovering the .git/ directory, reading the config and then trying to painstakingly reset all the global state if we did not find a matching alias, let's use the early config machinery instead.
- 신규 — It is totally legitimate to add CamelCased aliases, but due to the way config keys are compared, the case does not matter.

**revised · earlier-first** · 설명 오류

The report reveals that allowing CamelCased aliases is acceptable despite previous decisions based on the assumption that config keys are case-sensitive, thus requiring reevaluation of those prior project decisions.

설명 채점 — 대소문자 조합은 언급하지만 과거가 대소문자 구분을 전제했다고 단정하고 설정 키와의 비교 변경을 놓쳤다.

**original · report-first** · 재검토 누락

The earlier decision relied on the fact that the case of config keys did not matter for adding aliases; however, the new evidence shows that with concrete new data indicating the importance of preserving the original casing when comparing config keys, this earlier result may no longer apply, unless there is a specific configuration or context where the casing comparison is irrelevant.

설명 채점 — 원문이 요구한 대소문자 무시와 반대로 원래 대소문자를 보존해야 한다고 했다.

**revised · report-first** · 설명 오류

The report reveals that allowing CamelCased aliases is acceptable despite previous decisions based on the assumption that config keys are case-sensitive, thus requiring reevaluation of those prior project decisions.

설명 채점 — 대소문자 조합은 언급하지만 과거가 대소문자 구분을 전제했다고 단정하고 설정 키와의 비교 변경을 놓쳤다.

### 원문 전체에서 출발

**pairwise** · 재검토 누락

**fixed-review** · 문단 오류

The report reveals a prior decision to use the early config machinery to expand aliases, introduced by commit a9bcf6586d1 on 2017-06-14, which may need reevaluation given the earlier behavior of discovering the .git/ directory and resetting global state.

설명 채점 — 커밋과 초기 설정 로딩을 언급했지만 대소문자가 섞인 별칭이 실패하는 조건을 설명하지 않았다.

- 과거 — Instead of discovering the .git/ directory, reading the config and then trying to painstakingly reset all the global state if we did not find a matching alias, let's use the early config machinery instead.
- 신규 — This fixes a regression introduced by a9bcf6586d1 (alias: use the early config machinery to expand aliases, 2017-06-14).

## cross-alias

Distinct historical decision. When resolving CamelCased aliases in early config, names must match config keys case-insensitively; -h output is independent.

[과거 원문](https://github.com/git/git/commit/0989fe9623dc8d98033f6acdcc0c84ec28571b19) · [새 보고](https://github.com/git/git/commit/643df7e234dda47a4748311361a82df5415b7bc1)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision relied on the potential future use of `split_cmdline()` for non-alias functionalities, but the report indicates that the current case-insensitive comparison of config keys means that adding CamelCased aliases does not pose a problem, thus changing the applicability of the earlier decision. The earlier result remains true if the case sensitivity of config keys is maintained or if there are no plans to change the comparison method.

- 과거 — split_cmdline() is currently used for aliases only, but later it can be useful for other builtins as well. Move it to alias.c for now, indicating that originally it's for aliases, but we'll have it in libgit this way.
- 신규 — It is totally legitimate to add CamelCased aliases, but due to the way config keys are compared, the case does not matter.

**revised · earlier-first** · 오탐

The report reveals that config keys comparison ignores case sensitivity for CamelCased aliases, indicating a prior decision to allow such cases might need revisiting in light of this new evidence.

**original · report-first** · 보류

The earlier decision was based on the assumption that split_cmdline() is specifically for aliases, but the new evidence shows that config keys comparison indicates case does not affect functionality, thus changing its applicability to consider it useful for other builtins without needing to move it to alias.c unless there are specific cases where case sensitivity matters.

**revised · report-first** · 오탐

The report reveals that config keys comparison ignores case sensitivity for CamelCased aliases, indicating a prior decision to allow such cases might need revisiting in light of this new evidence.

## git-alias-neg

When resolving CamelCased aliases in early config, names must match config keys case-insensitively; -h output is independent.

[과거 원문](https://github.com/git/git/commit/a9bcf6586d1a4888aea91553d73cda20494b8335) · [새 보고](https://github.com/git/git/commit/a9a60b94ccda5ff25faf51f39faeac11cac68346)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision relied on the observation that most Git commands provide helpful usage information when invoked with `-h`. The report introduces new evidence suggesting that aliases could benefit from additional context indicating they are aliases and for what command, thus changing the applicability of the earlier decision to consider providing such context for aliases specifically. The earlier result remains valid for other Git commands where `-h` is used.

- 과거 — Instead of discovering the .git/ directory, reading the config and then trying to painstakingly reset all the global state if we did not find a matching alias, let's use the early config machinery instead.
- 신규 — Most git commands respond to -h anywhere in the command line, or at least as a first and lone argument, by printing the usage information. For aliases, we can provide a little more information that might be useful in interpreting/understanding the following output by prepending a line telling that the command is an alias, and for what.

**revised · earlier-first** · 보류

The earlier behavior of most git commands responding to -h by printing usage information may no longer align with the need to provide additional context for aliases, revealing a circumstance where rechecking the rationale behind this decision is necessary.

**original · report-first** · 보류

The earlier decision relied on the assumption that finding the .git/ directory was necessary before attempting to interpret aliases, but the new evidence shows that git commands now provide alias-specific usage information even when invoked without specifying the full command name, thus changing the applicability of this assumption. The earlier result remains true if the command does not include an alias or if alias interpretation is not required.

**revised · report-first** · 보류

The earlier behavior of most git commands responding to -h by printing usage information may no longer align with the need to provide additional context for aliases, revealing a circumstance where rechecking the rationale behind this decision is necessary.

### 원문 전체에서 출발

**pairwise** · 보류

**fixed-review** · 오탐

Review the decision to initially limit split_cmdline() usage to aliases only, given the reported exception where 'somecommand' fails with an invalid option '-h' when invoked via git sc -h.

- 과거 — split_cmdline() is currently used for aliases only, but later it can be useful for other builtins as well. Move it to alias.c for now, indicating that originally it's for aliases, but we'll have it in libgit this way.
- 신규 — $ git sc -h 'sc' is aliased to '!somecommand' somecommand: invalid option '-h'

## git-cvs-pos

When neither CLI nor .cvspass supplies a password, initialize the scrambled empty value to A; object IDs do not change password handling.

[과거 원문](https://github.com/git/git/commit/3fb9d58235ce4985689840b901aecacc6e3bd094) · [새 보고](https://github.com/git/git/commit/e481b1d8db9947681a5c124545ef06951f42155d)

### 고정한 근거

**original · earlier-first** · 재검토 누락

The earlier decision was based on the rationale that passwords stored in .cvspass are already scrambled and thus need not be scrambled again; however, the report introduces new evidence suggesting that if no passwords are found in .cvspass and none are read from the command line, the initialization process must use "A" as the password, thereby changing the applicability of the earlier decision when neither .cvspass nor command-line input contains passwords.

설명 채점 — 기존 저장 파일 암호 처리와 두 입력이 모두 비면 A로 초기화해야 한다는 예외를 정확히 연결했다.

- 과거 — Passwords stored in .cvspass are already scrambled, we do not want to scramble them twice. Only passwords read from the command line are scrambled.
- 신규 — If we do not read a password from the command line, and there are no passwords stored in .cvspass, we have to initialize the password with just "A".

**revised · earlier-first** · 적중

The report reveals a scenario where initializing the password with just "A" is necessary if neither command-line input nor .cvspass passwords are present, indicating a potential oversight in previous project decisions regarding password initialization logic.

설명 채점 — CLI와 저장 파일 모두 비었을 때 A로 초기화하는 누락 분기를 정확하게 특정했다.

**original · report-first** · 재검토 누락

The earlier decision relied on the assumption that passwords read from the command line were unscrambled before being stored in .cvspass, whereas the new evidence shows that these passwords are also scrambled, thus changing the applicability of the earlier result and necessitating a reassessment of whether passwords from the command line need to be initialized with "A".

설명 채점 — 입력이 모두 없는 경우를 놓치고 CLI 암호 자체에 A가 필요한 것으로 바꿨다.

**revised · report-first** · 적중

The report reveals a scenario where initializing the password with just "A" is necessary if neither command-line input nor .cvspass passwords are present, indicating a potential oversight in previous project decisions regarding password initialization logic.

설명 채점 — CLI와 저장 파일 모두 비었을 때 A로 초기화하는 누락 분기를 정확하게 특정했다.

### 원문 전체에서 출발

**pairwise** · 재검토 누락

**fixed-review** · 문단 오류

The report reveals a decision to avoid scrambling passwords stored in .cvspass, which may need reevaluation given the fix addressing the unintended scrambling of command-line passwords introduced by 3fb9d582.

설명 채점 — 두 암호 입력이 모두 없는 상황을 CLI 암호를 잘못 섞은 상황으로 바꿨다.

- 과거 — Passwords stored in .cvspass are already scrambled, we do not want to scramble them twice. Only passwords read from the command line are scrambled.
- 신규 — This fixes a regression introduced by 3fb9d582 (Do not scramble password read from .cvspass).

## cross-cvs

Distinct historical decision. When neither CLI nor .cvspass supplies a password, initialize the scrambled empty value to A; object IDs do not change password handling.

[과거 원문](https://github.com/git/git/commit/8c372fb01dcd9da5e0e538943cc173941c03ef2d) · [새 보고](https://github.com/git/git/commit/e481b1d8db9947681a5c124545ef06951f42155d)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision relied on the necessity of reading a password from the command line or having passwords stored in .cvspass for git-cvsimport to succeed in CVS repositories with unusual CVSROOT. The new evidence that changes its applicability is the finding that initializing the password with just "A" is sufficient, provided that either a password is read from the command line or stored in .cvspass. This condition preserves the earlier result as long as these alternative methods are available.

- 과거 — For CVS repositories with unusual CVSROOT, git-cvsimport would fail:
- 신규 — If we do not read a password from the command line, and there are no passwords stored in .cvspass, we have to initialize the password with just "A".

**revised · earlier-first** · 오탐

The report reveals a decision to initialize a password with just "A" if reading from the command line is disabled and no passwords are stored, which may need revisiting given new evidence; use the full report to verify this specific recommendation's necessity.

**original · report-first** · 보류

The earlier decision regarding CVSROOT initialization for unusual configurations is based on the assumption that if no passwords are set and not stored, "A" must be used; however, this rationale may no longer hold if the new evidence shows that git-cvsimport can now succeed without explicitly setting a password. The earlier result remains valid for standard CVSROOT setups where no default password handling exists.

**revised · report-first** · 오탐

The report reveals a decision to initialize a password with just "A" if reading from the command line is disabled and no passwords are stored, which may need revisiting given new evidence; use the full report to verify this specific recommendation's necessity.

## git-cvs-neg

When neither CLI nor .cvspass supplies a password, initialize the scrambled empty value to A; object IDs do not change password handling.

[과거 원문](https://github.com/git/git/commit/3fb9d58235ce4985689840b901aecacc6e3bd094) · [새 보고](https://github.com/git/git/commit/f3eaa09261c25813c84a0e47ce8a4dd1b9f5b717)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision relied on the principle that passwords stored in .cvspass are already scrambled and thus do not need to be scrambled again, whereas the report introduces new evidence suggesting that all command-line inputs for object IDs should now be checked using is_oid regardless of their cryptographic hash type, thereby changing the applicability of the earlier decision. The earlier result remains true if passwords in .cvspass continue to be scrambled as per the original policy.

- 과거 — Passwords stored in .cvspass are already scrambled, we do not want to scramble them twice. Only passwords read from the command line are scrambled.
- 신규 — Instead of calling the function is_sha1, call it is_oid and update it to match either a SHA-1 or a SHA-256 hex object ID.

**revised · earlier-first** · 오탐

The report suggests changing the function name from `is_sha1` to `is_oid` and updating its logic to recognize both SHA-1 and SHA-256 hex object IDs, indicating a potential change in password handling strategy that needs reevaluation.

**original · report-first** · 보류

The earlier decision relied on the principle that passwords stored in .cvspass are already scrambled and thus do not need further scrambling, but the new evidence shows that the updated function now accepts both SHA-1 and SHA-256 object IDs, potentially reintroducing a risk of password exposure if these IDs are derived from unscrambled inputs. This changes the applicability because the function's new functionality could lead to a situation where previously unscrambled inputs are now processed

**revised · report-first** · 오탐

The report suggests changing the function name from `is_sha1` to `is_oid` and updating its logic to recognize both SHA-1 and SHA-256 hex object IDs, indicating a potential change in password handling strategy that needs reevaluation.

### 원문 전체에서 출발

**pairwise** · 보류

**fixed-review** · 오탐

The report suggests changing the function from `is_sha1` to `is_oid` to match either a SHA-1 or SHA-256 hex object ID, indicating a potential change in cryptographic standards that should be reevaluated in existing project decisions.

- 과거 — This fixes a regression introduced by b2139db (git-cvsimport: add support for cvs pserver password scrambling., 2009-08-14).
- 신규 — Instead of calling the function is_sha1, call it is_oid and update it to match either a SHA-1 or a SHA-256 hex object ID.

## git-svn-pos

Dropping the Perl/shared library also lost the svn availability check; svnadmin tests need to skip or check when svn is absent. Empty-file test helpers do not restore it.

[과거 원문](https://github.com/git/git/commit/b0ad24be8ca9acd86393ce099d3217872d838915) · [새 보고](https://github.com/git/git/commit/8e9d453ce77b7942dd35c23e145981dc472fb8c8)

### 고정한 근거

**original · earlier-first** · 재검토 누락

The earlier decision relied on eliminating the dependency on SVN perl bindings to simplify and improve readability of the tests. However, the new evidence shows that this change introduced a regression by removing the safety check for svn availability, thus changing its applicability. The earlier result remains true if the safety check for svn is reinstated.

설명 채점 — Perl 의존 제거 과정에서 svn 가용성 확인이 사라졌고 이 검사를 복원해야 한다는 점을 특정했다.

- 과거 — Running test t9010 without the SVN:: perl modules currently errors out, for no good reason. We can make these tests easier to read and run by not using the perl libsvn bindings and instead duplicating only the relevant code from lib-git-svn.sh.
- 신규 — The test uses "svnadmin" without checking if svn is available. This was a regression introduced by b0ad24b (t9010 (svn-fe): Eliminate dependency on svn perl bindings, 2010-10-10) when it stopped including ./lib-git-svn.sh that had the safety.

**revised · earlier-first** · 설명 오류

The earlier decision to eliminate dependency on SVN perl bindings in commit b0ad24b (2010-10-10) may have introduced a regression due to the removal of lib-git-svn.sh, which contained safety checks; thus, the rationale for this decision should be revisited.

설명 채점 — 라이브러리의 일반 안전 검사를 언급했지만 svn 실행 파일이 없을 때 svnadmin을 호출하는 조건을 밝히지 않았다.

**original · report-first** · 재검토 누락

The earlier decision relied on the absence of SVN::perl modules causing test failures; however, the new evidence shows that this failure is due to a regression introduced by a commit that inadvertently removed a safety mechanism, thus changing the applicability of the earlier result under conditions where the safety mechanism was still present.

설명 채점 — Perl 바인딩 부재와 svn 실행 파일 부재를 구별하지 않고 일반적인 안전장치 문제로 설명했다.

**revised · report-first** · 설명 오류

The earlier decision to eliminate dependency on SVN perl bindings in commit b0ad24b (2010-10-10) may have introduced a regression due to the removal of lib-git-svn.sh, which contained safety checks; thus, the rationale for this decision should be revisited.

설명 채점 — 라이브러리의 일반 안전 검사를 언급했지만 svn 실행 파일이 없을 때 svnadmin을 호출하는 조건을 밝히지 않았다.

### 원문 전체에서 출발

**pairwise** · 문단 오류

The earlier decision relied on ensuring that calls to git would gracefully fail, but the new evidence shows that this change causes tests to erroneously fail when using svn, thus changing its applicability unless explicitly allowed for svn interactions.

설명 채점 — 기존 실패 단언이 svn 사용 시 실패를 유발했다는 근거 없는 인과를 만들었다.

- 과거 — This patch changes every occurrence of "! git" -- with the meaning that a git call has to gracefully fail -- into "test_must_fail git".
- 신규 — Running test t9010 without svn currently errors out for no good reason.

**fixed-review** · 문단 오류

The report reveals that running test t9010 without svn currently errors out for no good reason, indicating a failure in the current project decision to treat git calls as mandatory and requiring their graceful failure, necessitating a reevaluation of this prior project decision.

설명 채점 — svn 실행 파일의 부재를 별개 결정인 실패 단언 도우미의 문제로 돌렸다.

- 과거 — This patch changes every occurrence of "! git" -- with the meaning that a git call has to gracefully fail -- into "test_must_fail git".
- 신규 — Running test t9010 without svn currently errors out for no good reason.

## cross-svn

Distinct historical decision. Dropping the Perl/shared library also lost the svn availability check; svnadmin tests need to skip or check when svn is absent. Empty-file test helpers do not restore it.

[과거 원문](https://github.com/git/git/commit/d492b31cafe9aa5ce001b1d48815f4c0bb40d01a) · [새 보고](https://github.com/git/git/commit/8e9d453ce77b7942dd35c23e145981dc472fb8c8)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision relied on ensuring that calls to git failed gracefully; however, the new evidence shows that this change inadvertently removed a safety mechanism for svnadmin usage, which now requires explicit testing for svn availability, thus changing its applicability.

- 과거 — This patch changes every occurrence of "! git" -- with the meaning that a git call has to gracefully fail -- into "test_must_fail git".
- 신규 — The test uses "svnadmin" without checking if svn is available. This was a regression introduced by b0ad24b (t9010 (svn-fe): Eliminate dependency on svn perl bindings, 2010-10-10) when it stopped including ./lib-git-svn.sh that had the safety.

**revised · earlier-first** · 오탐

The report reveals a prior decision to eliminate dependency on svn perl bindings, introduced by b0ad24b (t9010 (svn-fe): Eliminate dependency on svn perl bindings, 2010-10-10), which may need revisiting due to the current test's reliance on svnadmin without verifying its availability.

**original · report-first** · 보류

The earlier decision relied on the assumption that using "! git" would ensure graceful failure for git calls, but the new evidence shows that this is no longer true due to the removal of "./lib-git-svn.sh", thus changing the applicability of the earlier result under conditions where the script provided fallbacks for git calls.

**revised · report-first** · 오탐

The report reveals a prior decision to eliminate dependency on svn perl bindings, introduced by b0ad24b (t9010 (svn-fe): Eliminate dependency on svn perl bindings, 2010-10-10), which may need revisiting due to the current test's reliance on svnadmin without verifying its availability.

## git-svn-neg

Dropping the Perl/shared library also lost the svn availability check; svnadmin tests need to skip or check when svn is absent. Empty-file test helpers do not restore it.

[과거 원문](https://github.com/git/git/commit/b0ad24be8ca9acd86393ce099d3217872d838915) · [새 보고](https://github.com/git/git/commit/ed254710eee0a5fcde1057593d181d40b02922e1)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision to avoid using SVN:: perl modules in test t9010 was based on the absence of a clear reason for errors; however, the introduction of use of test_must_be_empty, which is more efficient and provides better debugging information, makes the reliance on the original rationale less applicable, provided that the new test does not introduce significant performance overhead or loss of critical error detection capabilities.

- 과거 — Running test t9010 without the SVN:: perl modules currently errors out, for no good reason. We can make these tests easier to read and run by not using the perl libsvn bindings and instead duplicating only the relevant code from lib-git-svn.sh.
- 신규 — Use test_must_be_empty instead of comparing it to an empty file. That's more efficient, as the function only needs built-in meta-data only check in the usual case, and provides nicer debug output otherwise.

**revised · earlier-first** · 보류

The report suggests revisiting the decision to use test_must_be_empty, revealing inefficiency and suggesting better debug output, indicating prior project decisions on testing methods may need reevaluation.

**original · report-first** · 보류

The earlier decision relied on the inefficiency and verbosity of using SVN::perl modules for running specific tests, but the introduction of a more efficient alternative test_must_be_empty that avoids these issues makes the applicability of the earlier result conditional on the necessity of maintaining compatibility with SVN::perl or the desire to simplify and improve test readability and execution.

**revised · report-first** · 보류

The report suggests revisiting the decision to use test_must_be_empty, revealing inefficiency and suggesting better debug output, indicating prior project decisions on testing methods may need reevaluation.

### 원문 전체에서 출발

**pairwise** · 보류

**fixed-review** · 오탐

The report suggests changing the test from "test_must_fail" to "test_must_be_empty", indicating a potential inefficiency and improved debugging; thus, the rationale behind advertising "test_must_fail" for new tests must be rechecked.

- 과거 — - advertise the use of "test_must_fail" for new tests.
- 신규 — Use test_must_be_empty instead of comparing it to an empty file. That's more efficient, as the function only needs built-in meta-data only check in the usual case, and provides nicer debug output otherwise.

## git-trash-pos

The output directory inherited/defaulted by the subtests puts their scratch outside t0000; set TEST_OUTPUT_DIRECTORY for the sub-tests. Indentation does not affect it.

[과거 원문](https://github.com/git/git/commit/38b074de80759c95fec20b0dbc30614caccdfd24) · [새 보고](https://github.com/git/git/commit/68830470712b370d5ea231f76babd60a8859c105)

### 고정한 근거

**original · earlier-first** · 재검토 누락

The earlier decision relied on the default behavior of $TEST_OUTPUT_DIRECTORY being equal to $TEST_DIRECTORY, leading to sub-test trash directories being created under the top-level t/ directory. The new evidence shows that when $TEST_OUTPUT_DIRECTORY is not "." and an absolute --root is not specified, the $test variable uses $TRASH_DIRECTORY, thus changing the condition under which sub-test trash directories are retained; this concrete new evidence makes the earlier result applicable only if $TEST_OUTPUT_DIRECTORY

설명 채점 — 어느 문서가 새 관측인지 뒤바꾸고 조건절 중간에서 끊겼다.

- 과거 — After the location of $TRASH_DIRECTORY is adjusted by $TEST_OUTPUT_DIRECTORY, we go on to use the $test variable to make the trash directory and cd into it. This means that when $TEST_OUTPUT_DIRECTORY is not "." and an absolute --root has not been specified, we do not remove the trash directory once the tests are complete (remove_trash is set to $TRASH_DIRECTORY).
- 신규 — These scratch areas for sub-tests should be under the t0000 trash directory, but because TEST_OUTPUT_DIRECTORY defaults to TEST_DIRECTORY, which is exported to help sub-tests find test-lib.sh, the sub-test trash directories are created under the toplevel t/ directory instead. Because some of the sub-tests simulate failures, their trash directories are kept around.

**revised · earlier-first** · 적중

The earlier behavior where sub-test trash directories were incorrectly placed under the top-level t/ directory instead of the intended t0000 trash directory due to TEST_OUTPUT_DIRECTORY defaulting to TEST_DIRECTORY should be rechecked given the new evidence.

설명 채점 — 하위 테스트가 물려받는 출력 경로의 기본값 때문에 임시 디렉터리가 t0000 밖에 생기는 조건과 증상을 특정했다.

**original · report-first** · 재검토 누락

The earlier decision held that the trash directory was retained unless explicitly removed due to the default behavior of $TEST_OUTPUT_DIRECTORY overriding $TRASH_DIRECTORY; however, the new evidence shows that this retention only occurs if $TEST_OUTPUT_DIRECTORY does not default to ".", indicating a need to reconsider the applicability of the earlier decision when $TEST_OUTPUT_DIRECTORY is ".".

설명 채점 — 하위 테스트의 출력 위치 문제를 점 경로에서만 달라지는 보존 조건이라고 잘못 해석했다.

**revised · report-first** · 적중

The earlier behavior where sub-test trash directories were incorrectly placed under the top-level t/ directory instead of the intended t0000 trash directory due to TEST_OUTPUT_DIRECTORY defaulting to TEST_DIRECTORY should be rechecked given the new evidence.

설명 채점 — 하위 테스트가 물려받는 출력 경로의 기본값 때문에 임시 디렉터리가 t0000 밖에 생기는 조건과 증상을 특정했다.

### 원문 전체에서 출발

**pairwise** · 재검토 누락

**fixed-review** · 문단 오류

The report reveals that prior to commit 38b074d, tests used a \"trash\" directory within their current directory rather than the specified TEST_OUTPUT_DIRECTORY, suggesting a prior decision to use the current directory's trash for test outputs should be revisited.

설명 채점 — 수정 전의 테스트 위치를 다시 설명했고 하위 테스트가 물려받은 기본값 문제를 놓쳤다.

- 과거 — Fix this by always referring to the trash directory as $TRASH_DIRECTORY.
- 신규 — This fixes a regression introduced by 38b074d (t/test-lib.sh: fix TRASH_DIRECTORY handling, 2013-04-14). Before that commit, the TEST_OUTPUT_DIRECTORY setting was not respected consistently so most tests did their work in a "trash" subdirectory of the current directory instead of the output dir.

## cross-trash

Distinct historical decision. The output directory inherited/defaulted by the subtests puts their scratch outside t0000; set TEST_OUTPUT_DIRECTORY for the sub-tests. Indentation does not affect it.

[과거 원문](https://github.com/git/git/commit/f69e836fab2b634281d92a0d304de4d768e479cc) · [새 보고](https://github.com/git/git/commit/68830470712b370d5ea231f76babd60a8859c105)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision was based on ensuring that test scripts did not fail due to whitespace or shell metacharacters in git checkout paths; however, the new evidence shows that this does not apply when sub-tests' expected failure scenarios leave behind persistent trash directories under the top-level t/ directory, thus changing its applicability.

- 과거 — This fixes the remainder of the issues where the test script itself is at fault for failing when the git checkout path contains whitespace or other shell metacharacters.
- 신규 — These scratch areas for sub-tests should be under the t0000 trash directory, but because TEST_OUTPUT_DIRECTORY defaults to TEST_DIRECTORY, which is exported to help sub-tests find test-lib.sh, the sub-test trash directories are created under the toplevel t/ directory instead. Because some of the sub-tests simulate failures, their trash directories are kept around.

**revised · earlier-first** · 오탐

The earlier behavior of defaulting TEST_OUTPUT_DIRECTORY to TEST_DIRECTORY led to sub-test trash directories being created under the top-level t/ directory instead of the intended t0000 directory, revealing a discrepancy that must be rechecked in the TEST_OUTPUT_DIRECTORY setting's default logic.

**original · report-first** · 보류

The earlier decision was based on issues with the test script failing due to whitespace or shell metacharacters in the git checkout path; however, the new evidence indicates that sub-test trash directories are now being created in the top-level directory, changing the applicability of the earlier result as it does not pertain to sub-tests' failure scenarios.

**revised · report-first** · 오탐

The earlier behavior of defaulting TEST_OUTPUT_DIRECTORY to TEST_DIRECTORY led to sub-test trash directories being created under the top-level t/ directory instead of the intended t0000 directory, revealing a discrepancy that must be rechecked in the TEST_OUTPUT_DIRECTORY setting's default logic.

## git-trash-neg

The output directory inherited/defaulted by the subtests puts their scratch outside t0000; set TEST_OUTPUT_DIRECTORY for the sub-tests. Indentation does not affect it.

[과거 원문](https://github.com/git/git/commit/38b074de80759c95fec20b0dbc30614caccdfd24) · [새 보고](https://github.com/git/git/commit/2f68c99a3beefa5556eca76811deb443599e214a)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision relied on the specific formatting of test scripts in t0000-basic.sh using four-space indentation; the report introduces new evidence indicating some tests now use tab indentation, thus changing the applicability of the earlier result for those tests. The earlier decision remains valid for tests still using the four-space indentation format.

- 과거 — After the location of $TRASH_DIRECTORY is adjusted by $TEST_OUTPUT_DIRECTORY, we go on to use the $test variable to make the trash directory and cd into it. This means that when $TEST_OUTPUT_DIRECTORY is not "." and an absolute --root has not been specified, we do not remove the trash directory once the tests are complete (remove_trash is set to $TRASH_DIRECTORY).
- 신규 — Some tests in t0000-basic.sh used the older four space indent format. Update these to use tabs.

**revised · earlier-first** · 보류

The report sentence "Update these to use tabs" highlights an earlier project decision whose rationale should be revisited in light of new evidence, as indicated by the earlier behavior where the location of $TRASH_DIRECTORY was incorrectly adjusted based on $TEST_OUTPUT_DIRECTORY, revealing a potential oversight in handling the trash directory cleanup process.

**original · report-first** · 보류

The earlier decision relied on the necessity of maintaining a trash directory for test cleanup after adjusting $TEST_OUTPUT_DIRECTORY; however, the new evidence indicates that since some scripts now use tab indentation instead of four spaces, the specific need to preserve the $TRASH_DIRECTORY for cleanup may no longer apply universally, as the exact script being referred to might have changed formatting requirements. The earlier result remains valid if the script still uses the four-space indentation format.

**revised · report-first** · 보류

The report sentence "Update these to use tabs" highlights an earlier project decision whose rationale should be revisited in light of new evidence, as indicated by the earlier behavior where the location of $TRASH_DIRECTORY was incorrectly adjusted based on $TEST_OUTPUT_DIRECTORY, revealing a potential oversight in handling the trash directory cleanup process.

### 원문 전체에서 출발

**pairwise** · 보류

**fixed-review** · 보류

## git-symlink-pos

Canonicalizing an absolute worktree symlink dereferences the link, making Git act on the target instead of the link. Local clone object-store symlinks are a different operation.

[과거 원문](https://github.com/git/git/commit/18e051a3981f38db08521bb61ccf7e4571335353) · [새 보고](https://github.com/git/git/commit/f02033f1d02a55b32815a4702389e4d492f38bcc)

### 고정한 근거

**original · earlier-first** · 재검토 누락

The earlier decision allowed for dereferencing symlinks in filenames when using absolute paths, but this decision may now need reconsideration given that concrete new evidence shows that such dereferencing can lead to unintended modifications of files other than the symlinked ones, thus changing its applicability.

설명 채점 — 절대 경로를 따라가면 링크 대신 다른 파일을 수정할 수 있다는 반례를 포착했다.

- 과거 — setup: translate symlinks in filename when using absolute paths
- 신규 — When symlinks in the working tree are manipulated using the absolute path, git dereferences them, and tries to manipulate the link target instead.

**revised · earlier-first** · 적중

The report reveals that manipulating symlinks with absolute paths causes git to dereference them and target manipulation, indicating a need to revisit the setup: translate symlinks in filename when using absolute paths.

설명 채점 — 절대 경로의 링크를 해석해 링크 자체 대신 대상에 작용하는 문제를 기존 변환에 연결했다.

**original · report-first** · 재검토 누락

The earlier decision relied on the behavior that symlinks in the working tree are dereferenced and manipulated based on their absolute path. However, the introduction of concrete new evidence showing that git instead attempts to manipulate the actual target of the symlink when an absolute path is used changes its applicability under certain conditions where relative paths are employed.

설명 채점 — 문제는 절대 경로로 링크를 조작할 때인데 새로운 적용 조건으로 상대 경로를 도입했다.

**revised · report-first** · 적중

The report reveals that manipulating symlinks with absolute paths causes git to dereference them and target manipulation, indicating a need to revisit the setup: translate symlinks in filename when using absolute paths.

설명 채점 — 절대 경로의 링크를 해석해 링크 자체 대신 대상에 작용하는 문제를 기존 변환에 연결했다.

### 원문 전체에서 출발

**pairwise** · 재검토 누락

**fixed-review** · 문단 오류

The original author's decision to translate symlinks in filenames when using absolute paths (introduced by 18e051a) likely overlooked symlinks within the work tree, which should now be rechecked given this new evidence revealing a regression.

설명 채점 — 작업 트리 내부 링크의 누락은 찾았으나 대상을 따라가 링크 대신 대상 파일에 작용하는 결과를 밝히지 않았다.

- 과거 — otherwise, comparison to validate against work tree will fail when the path includes a symlink and the name passed is not canonical.
- 신규 — This is a regression introduced by 18e051a: setup: translate symlinks in filename when using absolute paths (which did not take symlinks inside the work tree into consideration).

## cross-symlink

Distinct historical decision. Canonicalizing an absolute worktree symlink dereferences the link, making Git act on the target instead of the link. Local clone object-store symlinks are a different operation.

[과거 원문](https://github.com/git/git/commit/f66bc5f928194366ee5eb78ef18a3562fb1bb7cf) · [새 보고](https://github.com/git/git/commit/f02033f1d02a55b32815a4702389e4d492f38bcc)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision that git dereferences symlinks when manipulating them with an absolute path is now applicable only if the path provided does not contain a relative component; otherwise, the concrete new evidence indicates that git may misinterpret the path and fail to dereference as previously assumed.

- 과거 — Unify all
- 신규 — When symlinks in the working tree are manipulated using the absolute path, git dereferences them, and tries to manipulate the link target instead.

**revised · earlier-first** · 보류

The report reveals that manipulating symlinks with absolute paths causes git to dereference them and target manipulation, which may have been an unintended consequence; this behavior must be rechecked for potential risks or issues.

**original · report-first** · 보류

The earlier decision to unify all manipulations involving symlinks was based on the assumption that dereferencing symlinks using an absolute path results in manipulation of the link target; however, the new evidence indicates that manipulating symlinks with absolute paths may not always result in the intended target modification due to potential differences in working directory contexts, thus changing its applicability. The earlier result remains true when the manipulation is performed within a consistent working directory context where dereferencing does indeed

**revised · report-first** · 보류

The report reveals that manipulating symlinks with absolute paths causes git to dereference them and target manipulation, which may have been an unintended consequence; this behavior must be rechecked for potential risks or issues.

## git-symlink-neg

Canonicalizing an absolute worktree symlink dereferences the link, making Git act on the target instead of the link. Local clone object-store symlinks are a different operation.

[과거 원문](https://github.com/git/git/commit/18e051a3981f38db08521bb61ccf7e4571335353) · [새 보고](https://github.com/git/git/commit/150e6b0aedf57d224c3c49038c306477fa159886)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision to translate symlinks in filenames for absolute paths was based on the potential security risk of cloning from a malicious repository, as evidenced by CVE-2022-39253. However, the introduction of 6f054f9fb3 (refusing symlinks in the source repository for `--local` clones) makes the necessity of translating symlinks obsolete under certain conditions, specifically when avoiding `--local` clones

- 과거 — setup: translate symlinks in filename when using absolute paths
- 신규 — Eventually though, we figured out that following symlinks like this can cause havoc when performing a local clone of a malicious repository, which resulted in CVE-2022-39253. This issue was fixed via 6f054f9fb3 (builtin/clone.c: disallow `--local` clones with symlinks, 2022-07-28), by refusing symlinks in the source repository.

**revised · earlier-first** · 오탐

The report reveals that allowing symlink translation in local repository clones could lead to security vulnerabilities, as evidenced by CVE-2022-39253, necessitating a reevaluation of the initial setup decision to translate symlinks in filenames when using absolute paths.

**original · report-first** · 보류

The earlier decision to translate symlinks in filenames for absolute paths was based on preventing potential security issues related to symbolic links; however, the introduction of CVE-2022-39253 demonstrates that allowing such translations can lead to vulnerabilities, thus making the earlier result applicable only in contexts where symlinks are not used in malicious repositories, specifically after the fix at 6f054f9fb3.

**revised · report-first** · 오탐

The report reveals that allowing symlink translation in local repository clones could lead to security vulnerabilities, as evidenced by CVE-2022-39253, necessitating a reevaluation of the initial setup decision to translate symlinks in filenames when using absolute paths.

### 원문 전체에서 출발

**pairwise** · 보류

**fixed-review** · 오탐

The original author should revisit prior project decisions regarding symlink handling, as the code that resolves symlinks persists despite the current policy against linking symlinks, potentially exposing vulnerabilities like CVE-2022-39253.

- 과거 — otherwise, comparison to validate against work tree will fail when the path includes a symlink and the name passed is not canonical.
- 신규 — But even though we now shouldn't ever link symlinks anymore, the code that resolves symlinks still exists. In the best case the code does not end up doing anything because there are no symlinks anymore. In the worst case though this can be abused by an adversary that rewrites the source file after it has been checked not to be a symlink such that it actually is a symlink when we call link(3P). Thus, it is still possible to recreate CVE-2022-39253 due to this time-of-check-time-of-use bug.

## git-am-pos

Patch-format detection must ignore leading whitespace that webmail prepends to saved mail. Resuming a failed patch without a tty is independent.

[과거 원문](https://github.com/git/git/commit/15ced753ac091314941abb28302f7109a9e86b81) · [새 보고](https://github.com/git/git/commit/0e8341f29d6541f661cc52f27f96877c0fd469c2)

### 고정한 근거

**original · earlier-first** · 재검토 누락

The earlier decision to default to mbox format based solely on input source was informed by the assumption that most email clients do not prepend whitespace; however, new evidence indicates that some clients do add leading whitespace, thus changing the applicability of this decision and requiring the patch format detection logic to account for this additional whitespace.

설명 채점 — 공백은 포착했으나 stdin 기본값이 이메일 클라이언트가 공백을 넣지 않는다는 가정에 근거한다고 잘못 단정했다.

- 과거 — Default to mbox format if input is from stdin. Otherwise, look at the first few lines of the first patch to try to guess its format.
- 신규 — Some web-based email clients prepend whitespace to raw message transcripts to workaround content-sniffing in some browsers. Adjust the patch format detection logic to ignore leading whitespace.

**revised · earlier-first** · 설명 오류

The earlier decision to default to mbox format if input is from stdin should be revisited given the new evidence that some web-based email clients prepend whitespace to raw message transcripts, as indicated by the report's recommendation to adjust the patch format detection logic to ignore leading whitespace.

설명 채점 — 메일 공백과 탐지를 짚었으나 다시 볼 이전 분기를 파일의 첫 줄 탐지 대신 stdin의 mbox 기본값으로 지목했다.

**original · report-first** · 재검토 누락

The earlier decision relied on initial observations about stdin inputs and patch format sniffing in browser content rendering. The new evidence shows that prepending whitespace to raw message transcripts can interfere with format detection logic, thus changing the applicability of the earlier result when dealing with such inputs. The earlier result remains valid for inputs without such whitespace interference.

설명 채점 — 공백이 형식 탐지를 방해한다는 점은 맞지만 브라우저의 콘텐츠 스니핑을 과거 Git 탐지 결정의 근거로 잘못 돌렸다.

**revised · report-first** · 설명 오류

The earlier decision to default to mbox format if input is from stdin should be revisited given the new evidence that some web-based email clients prepend whitespace to raw message transcripts, as indicated by the report's recommendation to adjust the patch format detection logic to ignore leading whitespace.

설명 채점 — 메일 공백과 탐지를 짚었으나 다시 볼 이전 분기를 파일의 첫 줄 탐지 대신 stdin의 mbox 기본값으로 지목했다.

### 원문 전체에서 출발

**pairwise** · 재검토 누락

**fixed-review** · 문단 오류

Adjust the patch format detection logic to ignore leading whitespace reveals a new evidence suggesting previous web-based email client practices may have influenced patch handling decisions; these prior decisions should be revisited.

설명 채점 — 공백 무시는 언급했지만 새 메일 환경이 과거 결정에 영향을 줬을 것이라고 추측하고 어떤 입력의 탐지가 깨지는지 연결하지 못했다.

- 과거 — Include checks for mailboxes, stgit patch series, stgit single patches and hg patches.
- 신규 — Some web-based email clients prepend whitespace to raw message transcripts to workaround content-sniffing in some browsers. Adjust the patch format detection logic to ignore leading whitespace.

## cross-am

Distinct historical decision. Patch-format detection must ignore leading whitespace that webmail prepends to saved mail. Resuming a failed patch without a tty is independent.

[과거 원문](https://github.com/git/git/commit/9b9f5a2258e6df611d2903d84fd8d41806ce0e00) · [새 보고](https://github.com/git/git/commit/0e8341f29d6541f661cc52f27f96877c0fd469c2)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision relied on the consistent naming convention across all state files using dashes instead of underscores, and the absence of a need for an "extra" step. The report introduces new evidence showing that web-based email clients prepend whitespace to raw message transcripts, which changes the applicability of the earlier decision regarding file naming conventions but does not affect the necessity of the "extra" step.

- 과거 — All other state files use dash in their names, not underscores. Also, there is no reason to call this "extra". Drop it.
- 신규 — Some web-based email clients prepend whitespace to raw message transcripts to workaround content-sniffing in some browsers. Adjust the patch format detection logic to ignore leading whitespace.

**revised · earlier-first** · 오탐

The report suggests adjusting patch format detection logic to ignore leading whitespace, revealing inconsistent handling of whitespace across different email clients; this must be rechecked to ensure uniformity in patch formats.

**original · report-first** · 보류

The earlier decision relied on naming conventions and formatting practices specific to state files, but the new evidence indicates that web-based email clients now prepend whitespace to raw message transcripts, thus changing the applicability of the earlier result and requiring a reevaluation of patch format detection logic to account for leading whitespace. The earlier result remains true for state files using dashes in their names.

**revised · report-first** · 오탐

The report suggests adjusting patch format detection logic to ignore leading whitespace, revealing inconsistent handling of whitespace across different email clients; this must be rechecked to ensure uniformity in patch formats.

## git-am-neg

Patch-format detection must ignore leading whitespace that webmail prepends to saved mail. Resuming a failed patch without a tty is independent.

[과거 원문](https://github.com/git/git/commit/15ced753ac091314941abb28302f7109a9e86b81) · [새 보고](https://github.com/git/git/commit/53ce2e3f0abf356fb0d2638783fe06711c5337d6)

### 고정한 근거

**original · earlier-first** · 보류

The earlier decision defaulted to mbox format when input was from stdin, assuming it would always come from a terminal. However, with the introduction of concrete new evidence showing that stdin can sometimes be non-interactive, this assumption may no longer hold, thus changing its applicability. The earlier result remains valid if stdin is indeed always provided through a terminal.

- 과거 — Default to mbox format if input is from stdin. Otherwise, look at the first few lines of the first patch to try to guess its format.
- 신규 — So if no resume command is given, then we require that stdin be a tty, and otherwise complain about (potentially) receiving an mbox on stdin. But of course you might not actually have a terminal available! And sadly there is no explicit way to hit this same code path; this is the only place that sets RESUME_APPLY. So you're stuck, and scripts like our test suite have to bend over backwards to create a pseudo-tty.

**revised · earlier-first** · 오탐

The earlier decision to require stdin to be a tty when no resume command is given, and to complain about receiving an mbox on stdin otherwise, must be rechecked in light of the new evidence suggesting this can lead to script limitations without a terminal available.

**original · report-first** · 보류

The earlier decision defaulted to mbox format for stdin inputs without checking for a tty, but this reliance is now invalid due to the introduction of concrete new evidence showing that stdin may not always be associated with a tty, thus changing the applicability of the earlier result. The earlier decision remains valid when stdin is indeed a tty.

**revised · report-first** · 오탐

The earlier decision to require stdin to be a tty when no resume command is given, and to complain about receiving an mbox on stdin otherwise, must be rechecked in light of the new evidence suggesting this can lead to script limitations without a terminal available.

### 원문 전체에서 출발

**pairwise** · 보류

**fixed-review** · 오탐

The reported failure with `git am <patch` followed by `git am --3way` after an initial failure indicates prior project decisions to include checks for mailboxes, stgit patch series, stgit single patches, and hg patches should be reevaluated in light of this new evidence.

- 과거 — Include checks for mailboxes, stgit patch series, stgit single patches and hg patches.
- 신규 — git am <patch # oops, it failed; let's try again git am --3way

## development-checkout

Initial checkout requires updating the worktree and index; cheap test ordering is incidental.

[과거 원문](https://github.com/git/git/commit/fa655d8411cc2d7ffcf898e53a1493c737d7de68) · [새 보고](https://github.com/git/git/commit/8424bfd45b291a56594f0289dc6af22e900a1d88)

### 고정한 근거

**original · earlier-first** · 설명 오류

The earlier decision relied on the specific context of creating a new branch via "git checkout -b <new_branch>" without affecting the working tree, but the new evidence indicates that filesystem access may occur during such checkouts, thus changing the applicability of the earlier result; the earlier decision remains valid for other checkout scenarios where no filesystem access is expected.

설명 채점 — 최초 checkout에서 작업 트리 갱신이 필요하다는 조건을 파일시스템 접근 여부로 치환했다.

- 과거 — Skip merging the commit, updating the index and working directory if and only if we are creating a new branch via "git checkout -b <new_branch>." Any other checkout options will still go through the former code path.
- 신규 — When doing a 'checkout -b' do a full checkout including updating the working tree when doing the initial checkout. As the new test involves an filesystem access, do it later in the sequence to give chance to other cheaper tests to leave early. This fixes the regression in behavior caused by fa655d8411 (checkout: optimize "git checkout -b <new_branch>", 2018-08-16).

**revised · earlier-first** · 설명 오류

The earlier decision to skip a full checkout for 'checkout -b' might need revisiting given the new evidence that it causes a regression fixed by fa655d8411 (checkout: optimize "git checkout -b <new_branch>", 2018-08-16).

설명 채점 — 최초 checkout 예외를 누락하고 회귀를 도입한 커밋을 수정한 커밋으로 설명했다.

**original · report-first** · 재검토 누락

The earlier decision relied on skipping updates for branch creation to avoid unnecessary overhead; however, the new evidence shows that filesystem access during branch creation can now impact performance, thus changing its applicability to scenarios involving filesystem access. The earlier result remains valid for other checkout options that do not involve filesystem access.

설명 채점 — 최초 checkout 대신 파일 접근 여부나 성능을 변경된 조건이라고 했다.

**revised · report-first** · 설명 오류

The earlier decision to skip a full checkout for 'checkout -b' might need revisiting given the new evidence that it causes a regression fixed by fa655d8411 (checkout: optimize "git checkout -b <new_branch>", 2018-08-16).

설명 채점 — 최초 checkout 예외를 누락하고 회귀를 도입한 커밋을 수정한 커밋으로 설명했다.

### 원문 전체에서 출발

**pairwise** · 설명 오류

The earlier decision relied on the specific context of creating a new branch via "git checkout -b <new_branch>" without affecting the working tree, but the new evidence indicates that filesystem access may occur during such checkouts, thus changing the applicability of the earlier result; the earlier decision remains valid for other checkout scenarios where no filesystem access is expected.

설명 채점 — 최초 checkout에서 작업 트리 갱신이 필요하다는 조건을 파일시스템 접근 여부로 치환했다.

- 과거 — Skip merging the commit, updating the index and working directory if and only if we are creating a new branch via "git checkout -b <new_branch>." Any other checkout options will still go through the former code path.
- 신규 — When doing a 'checkout -b' do a full checkout including updating the working tree when doing the initial checkout. As the new test involves an filesystem access, do it later in the sequence to give chance to other cheaper tests to leave early. This fixes the regression in behavior caused by fa655d8411 (checkout: optimize "git checkout -b <new_branch>", 2018-08-16).

**fixed-review** · 설명 오류

The earlier decision to skip a full checkout for 'checkout -b' might need revisiting given the new evidence that it causes a regression fixed by fa655d8411 (checkout: optimize "git checkout -b <new_branch>", 2018-08-16).

설명 채점 — 최초 checkout 예외를 누락하고 회귀를 도입한 커밋을 수정한 커밋으로 설명했다.

- 과거 — Skip merging the commit, updating the index and working directory if and only if we are creating a new branch via "git checkout -b <new_branch>." Any other checkout options will still go through the former code path.
- 신규 — When doing a 'checkout -b' do a full checkout including updating the working tree when doing the initial checkout. As the new test involves an filesystem access, do it later in the sequence to give chance to other cheaper tests to leave early. This fixes the regression in behavior caused by fa655d8411 (checkout: optimize "git checkout -b <new_branch>", 2018-08-16).
