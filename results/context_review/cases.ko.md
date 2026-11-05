# 새 Git 보고의 근거와 최종 판단

단순 검색, 직전 참조 방식, 역할 검증 방식, 문맥 확장 방식의 최종 출력을 같은 보고에서 비교했다.

## patch-search

[과거 결정](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9) · [새 보고](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4) · [주제가 비슷한 대조 결정](https://github.com/git/git/commit/d85d7ecb80ebc93f7380b4196c303756ee051668)

The search-key change inserted a captureless regex, making $1 undef. Initial /regex search now warns and asks for the expression again. Identify either this actual failed search behavior or the capture overwrite and its triggering inserted regex.

### simple

retest · 올바른 대상 True · 근거 쌍 True · 조건과 동작 False · 대조 결정 구별 False

previous · [0, 58]

add -p: only bind search key if there's more than one hunk

incoming · [53, 206]

Fix a regression in 88f6ffc1c2 ("add -p: only bind search key if
there's more than one hunk", 2018-02-13) which is present in
2.17.0-rc*, but not 2.16.0.

### referenced-review

reassess · 올바른 대상 True · 근거 쌍 True · 조건과 동작 False · 대조 결정 구별 False

previous · [60, 296]

If there is only a single hunk then disable searching as there is
nothing to search for. Also print a specific error message if the user
tries to search with '/' when there's only a single hunk rather than
just listing the key bindings.

incoming · [615, 975]

$ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many

alternative · [43, 329]

Since c9d961647 (i18n: add--interactive: mark
edit_hunk_manually message for translation, 2016-12-14),
when the user asks to edit a hunk manually, we respect
core.commentChar in generating the edit instructions.
However, when we then strip out comment lines, we use a
simple regex like:

rationale

The regression occurred because attempting to search for "Many" failed due to an uninitialized value, which specifically went wrong when trying to search with "/" after splitting into four hunks, despite there being only one hunk available for search.

distinction

The other decision addresses editing a hunk manually, differing from the specific operation in the incoming report which involves searching for a regex pattern "/Many" after splitting into multiple hunks.

### role-review

keep · 올바른 대상 False · 근거 쌍 False · 조건과 동작 False · 대조 결정 구별 False

incomplete role evidence for the reported change

### context-review

reassess · 올바른 대상 True · 근거 쌍 True · 조건과 동작 True · 대조 결정 구별 True

previous · [60, 296]

If there is only a single hunk then disable searching as there is
nothing to search for. Also print a specific error message if the user
tries to search with '/' when there's only a single hunk rather than
just listing the key bindings.

report_anchor · [615, 975]

$ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many

incoming · [510, 975]

As a result the "/" feature to search for a string in a hunk by regex
completely broke, on git.git:

    $ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many

alternative · [43, 329]

Since c9d961647 (i18n: add--interactive: mark
edit_hunk_manually message for translation, 2016-12-14),
when the user asks to edit a hunk manually, we respect
core.commentChar in generating the edit instructions.
However, when we then strip out comment lines, we use a
simple regex like:

rationale

Reconsider the earlier decision “If there is only a single hunk then disable searching as there is
nothing to search for. Also print a specific error message if the user
tries to search with '/' when there's only a single hunk rather than
just listing the key bindings.”. The new report gives the following behavior and its conditions. “As a result the "/" feature to search for a string in a hunk by regex
completely broke, on git.git:

    $ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many”

distinction

The alternative addresses “Since c9d961647 (i18n: add--interactive: mark
edit_hunk_manually message for translation, 2016-12-14),
when the user asks to edit a hunk manually, we respect
core.commentChar in generating the edit instructions.
However, when we then strip out comment lines, we use a
simple regex like:”. The reported observation is “As a result the "/" feature to search for a string in a hunk by regex
completely broke, on git.git:

    $ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many”.

## asan-preload

[과거 결정](https://github.com/git/git/commit/131b94a10a77e40eb3b3ba276d07fb663e220cd1) · [새 보고](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6) · [주제가 비슷한 대조 결정](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

The glibc malloc-check preload change causes ASan test startup failure because ASan runtime is not first in the library list, specifically SANITIZE=address on glibc >=2.34. Include the failure and both sanitizer and version constraints. Leak/undefined are unaffected.

### simple

retest · 올바른 대상 True · 근거 쌍 True · 조건과 동작 False · 대조 결정 구별 False

previous · [0, 73]

test-lib.sh: Use GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34

incoming · [299, 489]

This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message

### referenced-review

reassess · 올바른 대상 True · 근거 쌍 True · 조건과 동작 False · 대조 결정 구별 False

previous · [75, 292]

In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment
variables have been replaced by GLIBC_TUNABLES.  Also the new
glibc requires that you preload a library called libc_malloc_debug.so
to get these features.

incoming · [57, 297]

As the address sanitizer checks for a superset of the issues detected
by setting MALLOC_CHECK_ (which tries to detect things like double
frees and off-by-one errors) there is no need to set the latter when
compiling with -fsanitize=address.

alternative · [57, 253]

Add "fast_unwind_on_malloc=0" to LSAN_OPTIONS to get more meaningful
stack traces from LSAN. This isn't required under ASAN which will emit
traces such as this one for a leak in "t/t0006-date.sh":

rationale

Setting MALLOC_CHECK_ when compiling with -fsanitize=address went wrong because it conflicts with the requirement in glibc >= 2.34 to use GLIBC_TUNABLES instead, leading to undefined behavior and potential false negatives in address sanitization.

distinction

The other decision addresses disabling MALLOC_CHECK_ for ASAN compatibility, differing from the incoming report's recommendation to use GLIBC_TUNABLES for glibc >= 2.34.

### role-review

reassess · 올바른 대상 True · 근거 쌍 True · 조건과 동작 False · 대조 결정 구별 False

previous · [75, 292]

In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment
variables have been replaced by GLIBC_TUNABLES.  Also the new
glibc requires that you preload a library called libc_malloc_debug.so
to get these features.

incoming · [57, 297]

As the address sanitizer checks for a superset of the issues detected
by setting MALLOC_CHECK_ (which tries to detect things like double
frees and off-by-one errors) there is no need to set the latter when
compiling with -fsanitize=address.

alternative · [57, 253]

Add "fast_unwind_on_malloc=0" to LSAN_OPTIONS to get more meaningful
stack traces from LSAN. This isn't required under ASAN which will emit
traces such as this one for a leak in "t/t0006-date.sh":

rationale

Revisit the earlier decision reported as “In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment variables have been replaced by GLIBC_TUNABLES. Also the new glibc requires that you preload a library called libc_malloc_debug.so to get these features.”. The incoming evidence gives the reason. As the address sanitizer checks for a superset of the issues detected
by setting MALLOC_CHECK_ (which tries to detect things like double
frees and off-by-one errors) there is no need to set the latter when
compiling with -fsanitize=address.

distinction

The alternative addresses “Add "fast_unwind_on_malloc=0" to LSAN_OPTIONS to get more meaningful stack traces from LSAN. This isn't required under ASAN which will emit traces such as this one for a leak in "t/t0006-date.sh":”, while the new report concerns “As the address sanitizer checks for a superset of the issues detected by setting MALLOC_CHECK_ (which tries to detect things like double frees and off-by-one errors) there is no need to set the latter when compiling with -fsanitize=address.”.

### context-review

reassess · 올바른 대상 True · 근거 쌍 True · 조건과 동작 False · 대조 결정 구별 False

previous · [75, 292]

In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment
variables have been replaced by GLIBC_TUNABLES.  Also the new
glibc requires that you preload a library called libc_malloc_debug.so
to get these features.

report_anchor · [57, 297]

As the address sanitizer checks for a superset of the issues detected
by setting MALLOC_CHECK_ (which tries to detect things like double
frees and off-by-one errors) there is no need to set the latter when
compiling with -fsanitize=address.

incoming · [299, 651]

This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message

    ASan runtime does not come first in initial library list;
    you should either link runtime to your application or
    manually preload it with LD_PRELOAD.

alternative · [57, 253]

Add "fast_unwind_on_malloc=0" to LSAN_OPTIONS to get more meaningful
stack traces from LSAN. This isn't required under ASAN which will emit
traces such as this one for a leak in "t/t0006-date.sh":

rationale

Reconsider the earlier decision “In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment
variables have been replaced by GLIBC_TUNABLES.  Also the new
glibc requires that you preload a library called libc_malloc_debug.so
to get these features.”. The new report gives the following behavior and its conditions. “This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message

    ASan runtime does not come first in initial library list;
    you should either link runtime to your application or
    manually preload it with LD_PRELOAD.”

distinction

The alternative addresses “Add "fast_unwind_on_malloc=0" to LSAN_OPTIONS to get more meaningful
stack traces from LSAN. This isn't required under ASAN which will emit
traces such as this one for a leak in "t/t0006-date.sh":”. The reported observation is “This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message

    ASan runtime does not come first in initial library list;
    you should either link runtime to your application or
    manually preload it with LD_PRELOAD.”.

## email-priority

[과거 결정](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb) · [새 보고](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23) · [주제가 비슷한 대조 결정](https://github.com/git/git/commit/c8243933c74e0bebcc617f750ae3990ecca47759)

The Perl config reader takes the first rather than the last scalar key when repeated across config scopes, preferring global over local values. Preserve this direction and the conflicting/multiple-key condition.

### simple

retest · 올바른 대상 True · 근거 쌍 True · 조건과 동작 False · 대조 결정 구별 False

previous · [1488, 1624]

We now run just one "git config"
invocation on startup instead of 8, the exact number will differ based
on the local sendemail.* config.

incoming · [65, 306]

Fix a regression in my c95e3a3f0b8 (send-email: move trivial config
handling to Perl, 2021-05-28) where we'd pick the first config key out
of multiple defined ones, instead of using the normal "last key wins"
semantics of "git config --get".

### referenced-review

reassess · 올바른 대상 True · 근거 쌍 True · 조건과 동작 False · 대조 결정 구별 False

previous · [880, 1388]

However, that means we can end up with "undef" in the middle of a
list. E.g. for sendemail.smtpserveroption in conjuction with
sendemail.smtpserver as a path this would have produce a warning. For
most of the other keys we'd behave the same despite the subtle change
in the value, e.g. sendemail.to would behave the same because
Mail::Address->parse() happens to return an empty list if fed
"undef". For the boolean values we were already prepared to handle
these variables being initialized as undef anyway.

incoming · [308, 551]

This broke e.g. cases where a .git/config would have a different
sendemail.smtpServer than ~/.gitconfig. We'd pick the ~/.gitconfig
over .git/config, instead of preferring the repository-local
version. The same would go for /etc/gitconfig etc.

alternative · [163, 333]

Since the introduction of 'core.hooksPath' configuration option in
867ad08a261 (hooks: allow customizing where the hook directory is,
2016-05-04), this is no longer true.

rationale

The regression occurred when the decision to initialize boolean values as undef was applied, leading to misinterpretation of repository-specific configurations over system-wide defaults, such as differing smtpServer settings between .git/config and ~/.gitconfig files.

distinction

The other decision addresses the change in `core.hooksPath` which affects how configuration options like `sendemail.smtpserver` are loaded, differing from the specific issue with `undef` values in `sendemail.smtpserveroption`.

### role-review

keep · 올바른 대상 False · 근거 쌍 False · 조건과 동작 False · 대조 결정 구별 False

incomplete role evidence for the reported change

### context-review

keep · 올바른 대상 False · 근거 쌍 False · 조건과 동작 False · 대조 결정 구별 False

no supported observation with its condition in the report window

## commit-permissions

[과거 결정](https://github.com/git/git/commit/9c4d6c0297b7d6167bf330853139b0515b351b89) · [새 보고](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a) · [주제가 비슷한 대조 결정](https://github.com/git/git/commit/3491047e14532f4c01e3459d59d914d9598721c5)

Updating/writing the cache tree during commit leads to duplicate insufficient-permission errors when .git/objects cannot be written. prepare_index should be quiet; prepare_to_commit should report the error. State the duplication and unwritable condition without swapping which call should be silent.

### simple

retest · 올바른 대상 True · 근거 쌍 True · 조건과 동작 False · 대조 결정 구별 False

previous · [51, 100]

During the commit process, update the cache-tree.

incoming · [306, 457]

The cause is rather straightforward, we've got WRITE_TREE_SILENT for
the use-case of wanting to prepare an index silently, quieting any
permission etc.

### referenced-review

keep · 올바른 대상 False · 근거 쌍 False · 조건과 동작 False · 대조 결정 구별 False

no unique decision in the document comparison

### role-review

keep · 올바른 대상 False · 근거 쌍 False · 조건과 동작 False · 대조 결정 구별 False

no unique decision in the document comparison

### context-review

keep · 올바른 대상 False · 근거 쌍 False · 조건과 동작 False · 대조 결정 구별 False

no unique decision in the document comparison

## help-spacing

[과거 결정](https://github.com/git/git/commit/1b81d8cb19d8da6d865b7fca5a095dd5fec8d209) · [새 보고](https://github.com/git/git/commit/93de1b6999898079f521afd73d6a4ae9d5f9aaea) · [주제가 비슷한 대조 결정](https://github.com/git/git/commit/968b1fe263f9dfec65be4598e4f0dd76f1692551)

Moving guide output to section-printing code adds an unintended leading newline for git help --guides or other single-section output. Describe the newline and single-section condition; not missing or duplicated guide text.

### simple

retest · 올바른 대상 False · 근거 쌍 False · 조건과 동작 False · 대조 결정 구별 False

previous · [629, 654]

This commit cleans it up.

incoming · [693, 881]

With 1b81d8cb19d we started using the "print_cmd_by_category()"
function added earlier in the same series, or in cfb22a02ab5 (help:
use command-list.h for common command list, 2018-05-10).

### referenced-review

reassess · 올바른 대상 True · 근거 쌍 True · 조건과 동작 True · 대조 결정 구별 True

previous · [53, 322]

The help command currently hard codes the list of guides and their
summary in C. Let's move this list to command-list.txt. This lets us
extract summary lines from Documentation/git*.txt. This also
potentially lets us list guides in git.txt, but I'll leave that for
now.

incoming · [53, 320]

Fix a formatting regression in 1b81d8cb19d (help: use command-list.txt
for the source of guides, 2018-05-20). Adjust the output of "git help
--guides" and any other future single-section commands so that a
newline isn't inserted before the only section being printed.

alternative · [580, 730]

The continuation message's phrasing is awkward.  This commit cleans it up.
As a bonus, we now use full-sentence strings which make translation easier.

rationale

The regression occurred because adjusting the output of "git help --guides" led to an unintended newline being inserted before the only section when there are no sections to separate, contrary to the expectation of a single guide section without additional whitespace.

distinction

The other decision addresses improving the phrasing of continuation messages, which differs from the incoming report's focus on adjusting newline insertion in help command outputs.

### role-review

keep · 올바른 대상 False · 근거 쌍 False · 조건과 동작 False · 대조 결정 구별 False

incomplete role evidence for the reported change

### context-review

keep · 올바른 대상 False · 근거 쌍 False · 조건과 동작 False · 대조 결정 구별 False

no supported observation with its condition in the report window
