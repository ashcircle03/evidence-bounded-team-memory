# 15개 Git 보고의 문항별 판단

형식 오류와 무관한 결정 선택은 별도 실패로 남긴다. 성공/실패는 고정 의미 기준과 인용을 함께 판정한 결과다.

## asan-preload

[새 보고](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6) · [실제 이전 결정](https://github.com/git/git/commit/131b94a10a77e40eb3b3ba276d07fb663e220cd1) · [유사 결정](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

The glibc malloc-check preload change causes ASan test startup failure because ASan runtime is not first in the library list, specifically SANITIZE=address on glibc >=2.34. Include the failure and both sanitizer and version constraints. Leak/undefined are unaffected.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | keep |
| 3b/raw/module | reassess | 실패: ASan 오류와 glibc 버전은 있으나 SANITIZE=address 발동 조건이 인용과 설명에 없다. | keep |
| 14b/raw/direct-full | reassess | 실패: 라이브러리 preload 순서 문제를 MALLOC_CHECK_ 제거 때문이라고 설명하며 SANITIZE=address 조건을 뒷받침하는 구절도 선택하지 않았다. | keep |
| 14b/raw/module | reassess | 실패: ASan 오류와 glibc 버전은 있으나 SANITIZE=address 발동 조건이 인용과 설명에 없다. | keep |
| 3b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | keep |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | keep | 실패: 보류 | keep |
| 14b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | keep |
| 14b/hidden/module | keep | 실패: 보류 | reassess |
| 14b/hidden/direct-oracle | reassess | 실패: 대상 또는 인용 불일치 | keep |

### 3b/raw/direct-full

The new evidence indicates that the change in test-lib.sh (P1) has caused a regression where tests fail with an error related to the ASan runtime not being the first in the initial library list. This failure is due to the address sanitizer (SANITIZE=address) being used with glibc versions >= 2.34, which now require the ASan runtime to be preloaded. The earlier decision (P0) did not consider this specific issue with glibc versions >= 2.34.

previous: [P0:0](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
test-lib: add "fast_unwind_on_malloc=0" to LSAN_OPTIONS
```

previous: [P0:1](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
Add "fast_unwind_on_malloc=0" to LSAN_OPTIONS to get more meaningful
stack traces from LSAN. This isn't required under ASAN which will emit
traces such as this one for a leak in "t/t0006-date.sh":
```

previous: [P0:2](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    $ ASAN_OPTIONS=detect_leaks=1 ./t0006-date.sh -vixd
    [...]
    Direct leak of 3 byte(s) in 1 object(s) allocated from:
        #0 0x488b94 in strdup (t/helper/test-tool+0x488b94)
        #1 0x9444a4 in xstrdup wrapper.c:29:14
        #2 0x5995fa in parse_date_format date.c:991:24
        #3 0x4d2056 in show_dates t/helper/test-date.c:39:2
        #4 0x4d174a in cmd__date t/helper/test-date.c:116:3
        #5 0x4cce89 in cmd_main t/helper/test-tool.c:127:11
        #6 0x4cd1e3 in main common-main.c:52:11
        #7 0x7fef3c695e49 in __libc_start_main csu/../csu/libc-start.c:314:16
        #8 0x422b09 in _start (t/helper/test-tool+0x422b09)
```

previous: [P0:3](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    SUMMARY: AddressSanitizer: 3 byte(s) leaked in 1 allocation(s).
    Aborted
```

previous: [P0:4](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
Whereas LSAN would emit this instead:
```

previous: [P0:5](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    $ ./t0006-date.sh -vixd
    [...]
    Direct leak of 3 byte(s) in 1 object(s) allocated from:
        #0 0x4323b8 in malloc (t/helper/test-tool+0x4323b8)
        #1 0x7f2be1d614aa in strdup string/strdup.c:42:15
```

previous: [P0:6](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    SUMMARY: LeakSanitizer: 3 byte(s) leaked in 1 allocation(s).
    Aborted
```

previous: [P0:7](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
Now we'll instead git this sensible stack trace under
LSAN. I.e. almost the same one (but starting with "malloc", as is
usual for LSAN) as under ASAN:
```

previous: [P0:8](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    Direct leak of 3 byte(s) in 1 object(s) allocated from:
        #0 0x4323b8 in malloc (t/helper/test-tool+0x4323b8)
        #1 0x7f012af5c4aa in strdup string/strdup.c:42:15
        #2 0x5cb164 in xstrdup wrapper.c:29:14
        #3 0x495ee9 in parse_date_format date.c:991:24
        #4 0x453aac in show_dates t/helper/test-date.c:39:2
        #5 0x453782 in cmd__date t/helper/test-date.c:116:3
        #6 0x451d95 in cmd_main t/helper/test-tool.c:127:11
        #7 0x451f1e in main common-main.c:52:11
        #8 0x7f012aef5e49 in __libc_start_main csu/../csu/libc-start.c:314:16
        #9 0x42e0a9 in _start (t/helper/test-tool+0x42e0a9)
```

previous: [P0:9](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    SUMMARY: LeakSanitizer: 3 byte(s) leaked in 1 allocation(s).
    Aborted
```

previous: [P0:10](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
As the option name suggests this does make things slower, e.g. for
t0001-init.sh we're around 10% slower:
```

previous: [P0:11](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    $ hyperfine -L v 0,1 'LSAN_OPTIONS=fast_unwind_on_malloc={v} make T=t0001-init.sh' -r 3
    Benchmark 1: LSAN_OPTIONS=fast_unwind_on_malloc=0 make T=t0001-init.sh
      Time (mean ± σ):      2.135 s ±  0.015 s    [User: 1.951 s, System: 0.554 s]
      Range (min … max):    2.122 s …  2.152 s    3 runs
```

previous: [P0:12](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    Benchmark 2: LSAN_OPTIONS=fast_unwind_on_malloc=1 make T=t0001-init.sh
      Time (mean ± σ):      1.981 s ±  0.055 s    [User: 1.769 s, System: 0.488 s]
      Range (min … max):    1.941 s …  2.044 s    3 runs
```

previous: [P0:13](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    Summary
      'LSAN_OPTIONS=fast_unwind_on_malloc=1 make T=t0001-init.sh' ran
        1.08 ± 0.03 times faster than 'LSAN_OPTIONS=fast_unwind_on_malloc=0 make T=t0001-init.sh'
```

previous: [P0:14](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
I think that's more than worth it to get the more meaningful stack
traces, we can always provide LSAN_OPTIONS=fast_unwind_on_malloc=0 for
one-off "fast" runs.
```

incoming: [N:2](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message
```

### 3b/raw/module

Reconsider the earlier decision “In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment
variables have been replaced by GLIBC_TUNABLES.  Also the new
glibc requires that you preload a library called libc_malloc_debug.so
to get these features.”. The new report gives the following behavior and its conditions. “This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message

    ASan runtime does not come first in initial library list;
    you should either link runtime to your application or
    manually preload it with LD_PRELOAD.”

previous: [원문 구간](https://github.com/git/git/commit/131b94a10a77e40eb3b3ba276d07fb663e220cd1)

```text
In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment
variables have been replaced by GLIBC_TUNABLES.  Also the new
glibc requires that you preload a library called libc_malloc_debug.so
to get these features.
```

incoming: [원문 구간](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message

    ASan runtime does not come first in initial library list;
    you should either link runtime to your application or
    manually preload it with LD_PRELOAD.
```

### 3b/hidden/direct-full

The new evidence indicates a regression where tests fail with the message 'ASan runtime does not come first in initial library list; you should either link runtime to your application or manually preload it with LD_PRELOAD.' This message suggests that the change in P1 has led to an issue that was not present before, undermining the original decision to use GLIBC_TUNABLES and the new library.

previous: [P0:0](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
test-lib: add "fast_unwind_on_malloc=0" to LSAN_OPTIONS
```

previous: [P0:1](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
Add "fast_unwind_on_malloc=0" to LSAN_OPTIONS to get more meaningful
stack traces from LSAN. This isn't required under ASAN which will emit
traces such as this one for a leak in "t/t0006-date.sh":
```

previous: [P0:2](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    $ ASAN_OPTIONS=detect_leaks=1 ./t0006-date.sh -vixd
    [...]
    Direct leak of 3 byte(s) in 1 object(s) allocated from:
        #0 0x488b94 in strdup (t/helper/test-tool+0x488b94)
        #1 0x9444a4 in xstrdup wrapper.c:29:14
        #2 0x5995fa in parse_date_format date.c:991:24
        #3 0x4d2056 in show_dates t/helper/test-date.c:39:2
        #4 0x4d174a in cmd__date t/helper/test-date.c:116:3
        #5 0x4cce89 in cmd_main t/helper/test-tool.c:127:11
        #6 0x4cd1e3 in main common-main.c:52:11
        #7 0x7fef3c695e49 in __libc_start_main csu/../csu/libc-start.c:314:16
        #8 0x422b09 in _start (t/helper/test-tool+0x422b09)
```

previous: [P0:3](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    SUMMARY: AddressSanitizer: 3 byte(s) leaked in 1 allocation(s).
    Aborted
```

previous: [P0:4](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
Whereas LSAN would emit this instead:
```

previous: [P0:5](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    $ ./t0006-date.sh -vixd
    [...]
    Direct leak of 3 byte(s) in 1 object(s) allocated from:
        #0 0x4323b8 in malloc (t/helper/test-tool+0x4323b8)
        #1 0x7f2be1d614aa in strdup string/strdup.c:42:15
```

previous: [P0:6](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    SUMMARY: LeakSanitizer: 3 byte(s) leaked in 1 allocation(s).
    Aborted
```

previous: [P0:7](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
Now we'll instead git this sensible stack trace under
LSAN. I.e. almost the same one (but starting with "malloc", as is
usual for LSAN) as under ASAN:
```

previous: [P0:8](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    Direct leak of 3 byte(s) in 1 object(s) allocated from:
        #0 0x4323b8 in malloc (t/helper/test-tool+0x4323b8)
        #1 0x7f012af5c4aa in strdup string/strdup.c:42:15
        #2 0x5cb164 in xstrdup wrapper.c:29:14
        #3 0x495ee9 in parse_date_format date.c:991:24
        #4 0x453aac in show_dates t/helper/test-date.c:39:2
        #5 0x453782 in cmd__date t/helper/test-date.c:116:3
        #6 0x451d95 in cmd_main t/helper/test-tool.c:127:11
        #7 0x451f1e in main common-main.c:52:11
        #8 0x7f012aef5e49 in __libc_start_main csu/../csu/libc-start.c:314:16
        #9 0x42e0a9 in _start (t/helper/test-tool+0x42e0a9)
```

previous: [P0:9](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    SUMMARY: LeakSanitizer: 3 byte(s) leaked in 1 allocation(s).
    Aborted
```

previous: [P0:10](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
As the option name suggests this does make things slower, e.g. for
t0001-init.sh we're around 10% slower:
```

previous: [P0:11](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    $ hyperfine -L v 0,1 'LSAN_OPTIONS=fast_unwind_on_malloc={v} make T=t0001-init.sh' -r 3
    Benchmark 1: LSAN_OPTIONS=fast_unwind_on_malloc=0 make T=t0001-init.sh
      Time (mean ± σ):      2.135 s ±  0.015 s    [User: 1.951 s, System: 0.554 s]
      Range (min … max):    2.122 s …  2.152 s    3 runs
```

previous: [P0:12](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    Benchmark 2: LSAN_OPTIONS=fast_unwind_on_malloc=1 make T=t0001-init.sh
      Time (mean ± σ):      1.981 s ±  0.055 s    [User: 1.769 s, System: 0.488 s]
      Range (min … max):    1.941 s …  2.044 s    3 runs
```

previous: [P0:13](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    Summary
      'LSAN_OPTIONS=fast_unwind_on_malloc=1 make T=t0001-init.sh' ran
        1.08 ± 0.03 times faster than 'LSAN_OPTIONS=fast_unwind_on_malloc=0 make T=t0001-init.sh'
```

previous: [P0:14](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
I think that's more than worth it to get the more meaningful stack
traces, we can always provide LSAN_OPTIONS=fast_unwind_on_malloc=0 for
one-off "fast" runs.
```

incoming: [N:2](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
This fixes a regression introduced by [ref] ("[referenced subject]", 2022-03-04)
which causes all the tests to fail with the message
```

### 3b/hidden/direct-oracle

The incoming report mentions a regression introduced by a previous commit ([ref] ("[referenced subject]", 2022-03-04)) that causes tests to fail with specific messages related to the order of initial libraries. The old evidence discusses adding an option to enable more meaningful stack traces under LSAN, which is unrelated to the new evidence about a regression in sanitizers. There is no direct connection between the old and new evidence.

### 3b/hidden/module

no unique decision in the document comparison

### 14b/hidden/direct-full

The addition of the fast_unwind_on_malloc option in P0 may cause issues when compiling with -fsanitize=address, as noted in the incoming report. The incoming report indicates that setting MALLOC_CHECK_ is unnecessary and can lead to test failures when using the address sanitizer.

previous: [P0:0](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
test-lib: add "fast_unwind_on_malloc=0" to LSAN_OPTIONS
```

previous: [P0:1](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
Add "fast_unwind_on_malloc=0" to LSAN_OPTIONS to get more meaningful
stack traces from LSAN. This isn't required under ASAN which will emit
traces such as this one for a leak in "t/t0006-date.sh":
```

previous: [P0:10](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
As the option name suggests this does make things slower, e.g. for
t0001-init.sh we're around 10% slower:
```

previous: [P0:11](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    $ hyperfine -L v 0,1 'LSAN_OPTIONS=fast_unwind_on_malloc={v} make T=t0001-init.sh' -r 3
    Benchmark 1: LSAN_OPTIONS=fast_unwind_on_malloc=0 make T=t0001-init.sh
      Time (mean ± σ):      2.135 s ±  0.015 s    [User: 1.951 s, System: 0.554 s]
      Range (min … max):    2.122 s …  2.152 s    3 runs
```

previous: [P0:12](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    Benchmark 2: LSAN_OPTIONS=fast_unwind_on_malloc=1 make T=t0001-init.sh
      Time (mean ± σ):      1.981 s ±  0.055 s    [User: 1.769 s, System: 0.488 s]
      Range (min … max):    1.941 s …  2.044 s    3 runs
```

previous: [P0:13](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
    Summary
      'LSAN_OPTIONS=fast_unwind_on_malloc=1 make T=t0001-init.sh' ran
        1.08 ± 0.03 times faster than 'LSAN_OPTIONS=fast_unwind_on_malloc=0 make T=t0001-init.sh'
```

incoming: [N:0](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
tests: make SANITIZE=address imply TEST_NO_MALLOC_CHECK
```

incoming: [N:2](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
This fixes a regression introduced by [ref] ("[referenced subject]", 2022-03-04)
which causes all the tests to fail with the message
```

incoming: [N:3](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
    ASan runtime does not come first in initial library list;
    you should either link runtime to your application or
    manually preload it with LD_PRELOAD.
```

### 14b/hidden/direct-oracle

The earlier decision to add 'fast_unwind_on_malloc=0' to LSAN_OPTIONS was based on the assumption that it would provide more meaningful stack traces similar to those under ASAN. However, the incoming report indicates that ASAN already covers a superset of the issues detected by MALLOC_CHECK_, making the specific configuration for LSAN less necessary. Additionally, the new evidence shows a regression introduced by the previous decision, causing tests to fail on systems with glibc >= 2.34 when compiled with SANITIZE=address.

previous: [P0:1](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
Add "fast_unwind_on_malloc=0" to LSAN_OPTIONS to get more meaningful
stack traces from LSAN. This isn't required under ASAN which will emit
traces such as this one for a leak in "t/t0006-date.sh":
```

previous: [P0:7](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
Now we'll instead git this sensible stack trace under
LSAN. I.e. almost the same one (but starting with "malloc", as is
usual for LSAN) as under ASAN:
```

previous: [P0:10](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
As the option name suggests this does make things slower, e.g. for
t0001-init.sh we're around 10% slower:
```

previous: [P0:14](https://github.com/git/git/commit/71f26798f24b69b5c7dc29fd169ebcc2a730b5e5)

```text
I think that's more than worth it to get the more meaningful stack
traces, we can always provide LSAN_OPTIONS=fast_unwind_on_malloc=0 for
one-off "fast" runs.
```

incoming: [N:1](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
As the address sanitizer checks for a superset of the issues detected
by setting MALLOC_CHECK_ (which tries to detect things like double
frees and off-by-one errors) there is no need to set the latter when
compiling with -fsanitize=address.
```

incoming: [N:2](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
This fixes a regression introduced by [ref] ("[referenced subject]", 2022-03-04)
which causes all the tests to fail with the message
```

incoming: [N:4](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
when git is compiled with SANITIZE=address on systems with glibc >=
2.34. I have tested SANITIZE=leak and SANITIZE=undefined and they do
not suffer from this regression so the fix in this patch should be
sufficient.
```

### 14b/raw/direct-full

The change introduced by P1 to use GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34 has caused a regression when compiling with SANITIZE=address. The new evidence shows that tests now fail with an ASan runtime error message, indicating that the address sanitizer no longer works correctly due to the removal of MALLOC_CHECK_.

previous: [P1:0](https://github.com/git/git/commit/131b94a10a77e40eb3b3ba276d07fb663e220cd1)

```text
test-lib.sh: Use GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34
```

previous: [P1:1](https://github.com/git/git/commit/131b94a10a77e40eb3b3ba276d07fb663e220cd1)

```text
In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment
variables have been replaced by GLIBC_TUNABLES.  Also the new
glibc requires that you preload a library called libc_malloc_debug.so
to get these features.
```

previous: [P1:2](https://github.com/git/git/commit/131b94a10a77e40eb3b3ba276d07fb663e220cd1)

```text
Using the ordinary glibc system variable detect if this is glibc >= 2.34 and
use GLIBC_TUNABLES and the new library.
```

previous: [P1:3](https://github.com/git/git/commit/131b94a10a77e40eb3b3ba276d07fb663e220cd1)

```text
This patch was inspired by a Richard W.M. Jones ndbkit patch
```

incoming: [N:2](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message
```

incoming: [N:3](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
    ASan runtime does not come first in initial library list;
    you should either link runtime to your application or
    manually preload it with LD_PRELOAD.
```

### 14b/raw/module

Reconsider the earlier decision “In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment
variables have been replaced by GLIBC_TUNABLES.  Also the new
glibc requires that you preload a library called libc_malloc_debug.so
to get these features.”. The new report gives the following behavior and its conditions. “This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message

    ASan runtime does not come first in initial library list;
    you should either link runtime to your application or
    manually preload it with LD_PRELOAD.”

previous: [원문 구간](https://github.com/git/git/commit/131b94a10a77e40eb3b3ba276d07fb663e220cd1)

```text
In glibc >= 2.34 MALLOC_CHECK_ and MALLOC_PERTURB_ environment
variables have been replaced by GLIBC_TUNABLES.  Also the new
glibc requires that you preload a library called libc_malloc_debug.so
to get these features.
```

incoming: [원문 구간](https://github.com/git/git/commit/067109a5e7db3fdffc25240bfc3b350962cd6bd6)

```text
This fixes a regression introduced by 131b94a10a ("test-lib.sh: Use
GLIBC_TUNABLES instead of MALLOC_CHECK_ on glibc >= 2.34", 2022-03-04)
which causes all the tests to fail with the message

    ASan runtime does not come first in initial library list;
    you should either link runtime to your application or
    manually preload it with LD_PRELOAD.
```

### 14b/hidden/module

the exact passages did not reproduce the document judgment
## commit-permissions

[새 보고](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a) · [실제 이전 결정](https://github.com/git/git/commit/9c4d6c0297b7d6167bf330853139b0515b351b89) · [유사 결정](https://github.com/git/git/commit/3491047e14532f4c01e3459d59d914d9598721c5)

Updating/writing the cache tree during commit leads to duplicate insufficient-permission errors when .git/objects cannot be written. prepare_index should be quiet; prepare_to_commit should report the error. State the duplication and unwritable condition without swapping which call should be silent.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: .git/objects 쓰기 불가 조건을 설명에서 누락하고 WRITE_TREE_SILENT 추가를 원인으로 단정한다. | invalid_output |
| 3b/raw/module | keep | 실패: 보류 | keep |
| 14b/raw/direct-full | reassess | 실패: cache-tree 쓰기와 권한 오류 중복 원인은 맞지만 .git/objects를 쓸 수 없을 때라는 발동 조건을 설명에서 생략한다. 선택 근거는 충분하나 설명은 부분 성공이다. | keep |
| 14b/raw/module | reassess | 성공: commit의 cache-tree 쓰기와 .git/objects 쓰기 불가 시 같은 권한 오류가 반복되는 동작을 설명에 인용하여 보존한다. | keep |
| 3b/hidden/direct-full | invalid_output | 실패: 형식 오류 | invalid_output |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | keep | 실패: 보류 | keep |
| 14b/hidden/direct-full | keep | 실패: 보류 | keep |
| 14b/hidden/module | reassess | 성공: cache-tree 쓰기와 .git/objects 쓰기 불가 시 중복 권한 오류를 인용한 설명에 함께 보존한다. | keep |
| 14b/hidden/direct-oracle | keep | 실패: 보류 | keep |

### 3b/hidden/direct-full

invalid_output

### 3b/hidden/direct-oracle

The incoming report mentions a regression in error output related to writing objects to .git/objects. This issue is triggered by the difference in how `write_object_file()` is called before and after the commit process. The earlier decisions focus on updating the path variable and committing the cache-tree, neither of which directly address the specific error output issue described in the incoming report. Therefore, there is no need to reconsider the earlier decisions based on the new evidence.

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The incoming report indicates that the regression in error output was introduced by the change in P0, specifically the addition of WRITE_TREE_SILENT flag without corresponding silent handling in the update_one() function of cache-tree.c. This change led to the emission of multiple 'insufficient permission' errors, contrary to the intended behavior of preparing the index silently.

previous: [P0:0](https://github.com/git/git/commit/9c4d6c0297b7d6167bf330853139b0515b351b89)

```text
cache-tree: Write updated cache-tree after commit
```

previous: [P0:1](https://github.com/git/git/commit/9c4d6c0297b7d6167bf330853139b0515b351b89)

```text
During the commit process, update the cache-tree. Write this updated
cache-tree so that it's ready for subsequent commands.
```

incoming: [N:0](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
commit: fix duplication regression in permission error output
```

incoming: [N:1](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
Fix a regression in the error output emitted when .git/objects can't
be written to. Before 9c4d6c0297b (cache-tree: Write updated
cache-tree after commit, 2014-07-13) we'd emit only one "insufficient
permission" error, now we'll do so again.
```

incoming: [N:2](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
The cause is rather straightforward, we've got WRITE_TREE_SILENT for
the use-case of wanting to prepare an index silently, quieting any
permission etc. error output. Then when we attempt to update to
that (possibly broken) index we'll run into the same errors again.
```

incoming: [N:3](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
But with 9c4d6c0297b the gap between the cache-tree API and the object
store wasn't closed in terms of asking write_object_file() to be
silent. I.e. post-9c4d6c0297b the first call is to prepare_index(),
and after that we'll call prepare_to_commit(). We only want verbose
error output from the latter.
```

incoming: [N:4](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
So let's add and use that facility with a corresponding HASH_SILENT
flag, its only user is cache-tree.c's update_one(), which will set it
if its "WRITE_TREE_SILENT" flag is set.
```

### 3b/raw/module

no unique decision in the document comparison

### 14b/hidden/direct-full

The incoming report addresses a regression in error output related to permission issues during commit operations. It does not provide new evidence that undermines or changes the conditions on which the earlier decisions depend. The earlier decisions focus on updating the cache tree and handling slashes in paths, while the new report deals with silent error handling during write operations.

### 14b/hidden/direct-oracle

The incoming report addresses a specific issue related to error handling during the commit process, particularly concerning the silent writing of objects to the repository. Neither of the provided earlier decisions directly relate to this issue. P0 discusses iterating through paths during a process, while P1 focuses on updating the cache-tree during commits. The new evidence does not provide information that would necessitate reconsideration of these earlier decisions.

### 14b/hidden/module

Reconsider the earlier decision “During the commit process, update the cache-tree. Write this updated
cache-tree so that it's ready for subsequent commands.”. The new report gives the following behavior and its conditions. “Fix a regression in the error output emitted when .git/objects can't
be written to. Before [ref] ([referenced subject], 2014-07-13) we'd emit only one "insufficient
permission" error, now we'll do so again.

The cause is rather straightforward, we've got WRITE_TREE_SILENT for
the use-case of wanting to prepare an index silently, quieting any
permission etc. error output. Then when we attempt to update to
that (possibly broken) index we'll run into the same errors again.”

previous: [원문 구간](https://github.com/git/git/commit/9c4d6c0297b7d6167bf330853139b0515b351b89)

```text
During the commit process, update the cache-tree. Write this updated
cache-tree so that it's ready for subsequent commands.
```

incoming: [원문 구간](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
Fix a regression in the error output emitted when .git/objects can't
be written to. Before [ref] ([referenced subject], 2014-07-13) we'd emit only one "insufficient
permission" error, now we'll do so again.

The cause is rather straightforward, we've got WRITE_TREE_SILENT for
the use-case of wanting to prepare an index silently, quieting any
permission etc. error output. Then when we attempt to update to
that (possibly broken) index we'll run into the same errors again.
```

### 14b/raw/direct-full

The earlier decision P0 introduced a change to write the updated cache-tree during the commit process, which inadvertently led to duplicated permission error outputs due to the unclosed gap between the cache-tree API and the object store in terms of handling silent writes.

previous: [P0:0](https://github.com/git/git/commit/9c4d6c0297b7d6167bf330853139b0515b351b89)

```text
cache-tree: Write updated cache-tree after commit
```

previous: [P0:1](https://github.com/git/git/commit/9c4d6c0297b7d6167bf330853139b0515b351b89)

```text
During the commit process, update the cache-tree. Write this updated
cache-tree so that it's ready for subsequent commands.
```

incoming: [N:1](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
Fix a regression in the error output emitted when .git/objects can't
be written to. Before 9c4d6c0297b (cache-tree: Write updated
cache-tree after commit, 2014-07-13) we'd emit only one "insufficient
permission" error, now we'll do so again.
```

incoming: [N:2](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
The cause is rather straightforward, we've got WRITE_TREE_SILENT for
the use-case of wanting to prepare an index silently, quieting any
permission etc. error output. Then when we attempt to update to
that (possibly broken) index we'll run into the same errors again.
```

incoming: [N:3](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
But with 9c4d6c0297b the gap between the cache-tree API and the object
store wasn't closed in terms of asking write_object_file() to be
silent. I.e. post-9c4d6c0297b the first call is to prepare_index(),
and after that we'll call prepare_to_commit(). We only want verbose
error output from the latter.
```

incoming: [N:4](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
So let's add and use that facility with a corresponding HASH_SILENT
flag, its only user is cache-tree.c's update_one(), which will set it
if its "WRITE_TREE_SILENT" flag is set.
```

### 14b/raw/module

Reconsider the earlier decision “During the commit process, update the cache-tree. Write this updated
cache-tree so that it's ready for subsequent commands.”. The new report gives the following behavior and its conditions. “Fix a regression in the error output emitted when .git/objects can't
be written to. Before 9c4d6c0297b (cache-tree: Write updated
cache-tree after commit, 2014-07-13) we'd emit only one "insufficient
permission" error, now we'll do so again.

The cause is rather straightforward, we've got WRITE_TREE_SILENT for
the use-case of wanting to prepare an index silently, quieting any
permission etc. error output. Then when we attempt to update to
that (possibly broken) index we'll run into the same errors again.”

previous: [원문 구간](https://github.com/git/git/commit/9c4d6c0297b7d6167bf330853139b0515b351b89)

```text
During the commit process, update the cache-tree. Write this updated
cache-tree so that it's ready for subsequent commands.
```

incoming: [원문 구간](https://github.com/git/git/commit/4ef91a2d795c424eda2bec1bfbbd0c813bcc978a)

```text
Fix a regression in the error output emitted when .git/objects can't
be written to. Before 9c4d6c0297b (cache-tree: Write updated
cache-tree after commit, 2014-07-13) we'd emit only one "insufficient
permission" error, now we'll do so again.

The cause is rather straightforward, we've got WRITE_TREE_SILENT for
the use-case of wanting to prepare an index silently, quieting any
permission etc. error output. Then when we attempt to update to
that (possibly broken) index we'll run into the same errors again.
```
## dir-diff

[새 보고](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a) · [실제 이전 결정](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007) · [유사 결정](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

Constructing the temporary left index from a subdirectory fails to add top-level-relative paths after the subdirectory argument change; distinguish the changed working directory from unmerged duplicate entries.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/raw/module | keep | 실패: 보류 | keep |
| 14b/raw/direct-full | reassess | 실패: 하위 디렉터리와 left index 문맥은 맞지만 실제 최상위 기준 경로의 인덱스 추가 누락을 설명하지 않고 경로 관련 이슈라고만 요약한다. 부분 성공이다. | keep |
| 14b/raw/module | reassess | 성공: 현재 하위 디렉터리 기준 경로 처리와 임시 left index에 최상위 기준 경로가 추가되지 않는 동작을 인용하여 연결한다. | keep |
| 3b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 14b/hidden/direct-full | reassess | 성공: 하위 디렉터리 경로 처리 변경과 left diff에서 최상위 기준 경로가 누락되는 실제 결과를 연결한다. | keep |
| 14b/hidden/module | reassess | 성공: 현재 하위 디렉터리 기준 경로 처리와 임시 left index에 최상위 기준 경로가 추가되지 않는 동작을 인용하여 연결한다. | keep |
| 14b/hidden/direct-oracle | reassess | 성공: 하위 디렉터리에서 임시 인덱스를 구성해 최상위 기준 경로가 추가되지 않는 조건과 동작을 보존한다. | reassess |

### 3b/hidden/direct-full

The new evidence indicates that the previous decision (P0) fixed an issue where unmerged files caused duplicate paths in the output of `git diff --raw`, leading to failures in `git difftool --dir-diff`. However, the new evidence shows that this fix introduced a regression where entries outside of the subdirectory are not properly handled by `git difftool --dir-diff`. The original problem was related to unmerged files, while the new issue pertains to the handling of paths outside the subdirectory.

previous: [P0:0](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

```text
difftool: handle unmerged files in dir-diff mode
```

previous: [P0:1](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

```text
When files are unmerged they can show up as both unmerged and
modified in the output of `git diff --raw`.  This causes
difftool's dir-diff to create filesystem entries for the same
path twice, which fails when it encounters a duplicate path.
```

previous: [P0:2](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

```text
Ensure that each worktree path is only processed once.
Add a test to demonstrate the breakage.
```

incoming: [N:0](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
difftool: fix dir-diff index creation when in a subdirectory
```

incoming: [N:1](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
[ref] ([referenced subject], 2016-07-18)
corrected how path arguments are handled in a subdirectory, but
it introduced a regression in how entries outside of the
subdirectory are handled by dir-diff.
```

incoming: [N:2](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
When preparing the right-side of the diff we only include the
changed paths in the temporary area.
```

incoming: [N:3](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.
```

incoming: [N:4](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
Teach difftool to chdir to the toplevel of the repository before
preparing its temporary indexes.  This ensures that all of the
toplevel-relative paths are valid.
```

incoming: [N:5](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
Add test cases to more thoroughly exercise this scenario.
```

### 3b/hidden/direct-oracle

The new evidence indicates that the correction made in P1 to handle path arguments relative to the current directory introduced a regression where entries outside the subdirectory are not being added to the index, causing the issue described in P0.

previous: [P0:1](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

```text
When files are unmerged they can show up as both unmerged and
modified in the output of `git diff --raw`.  This causes
difftool's dir-diff to create filesystem entries for the same
path twice, which fails when it encounters a duplicate path.
```

previous: [P0:2](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

```text
Ensure that each worktree path is only processed once.
Add a test to demonstrate the breakage.
```

incoming: [N:1](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
[ref] ([referenced subject], 2016-07-18)
corrected how path arguments are handled in a subdirectory, but
it introduced a regression in how entries outside of the
subdirectory are handled by dir-diff.
```

incoming: [N:3](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.
```

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The new evidence shows that the previous decision (P0) fixed an issue where unmerged files caused duplicate paths in the diff, but it introduced a new regression where paths outside the subdirectory were not included in the diff. The incoming report explains that the new commit (N) addresses this regression by ensuring that the temporary index is built from the toplevel of the repository, thus fixing the issue.

previous: [P0:0](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

```text
difftool: handle unmerged files in dir-diff mode
```

previous: [P0:1](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

```text
When files are unmerged they can show up as both unmerged and
modified in the output of `git diff --raw`.  This causes
difftool's dir-diff to create filesystem entries for the same
path twice, which fails when it encounters a duplicate path.
```

previous: [P0:2](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

```text
Ensure that each worktree path is only processed once.
Add a test to demonstrate the breakage.
```

incoming: [N:0](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
difftool: fix dir-diff index creation when in a subdirectory
```

incoming: [N:1](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
9ec26e7977 (difftool: fix argument handling in subdirs, 2016-07-18)
corrected how path arguments are handled in a subdirectory, but
it introduced a regression in how entries outside of the
subdirectory are handled by dir-diff.
```

incoming: [N:2](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
When preparing the right-side of the diff we only include the
changed paths in the temporary area.
```

incoming: [N:3](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.
```

incoming: [N:4](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
Teach difftool to chdir to the toplevel of the repository before
preparing its temporary indexes.  This ensures that all of the
toplevel-relative paths are valid.
```

incoming: [N:5](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
Add test cases to more thoroughly exercise this scenario.
```

### 3b/raw/module

no unique decision in the document comparison

### 14b/hidden/direct-full

The earlier decision (P1) corrected how path arguments are handled in a subdirectory, but it introduced a regression where entries outside of the subdirectory were not properly included in the left side of the diff due to incorrect handling of toplevel-relative paths.

previous: [P1:0](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
difftool: fix argument handling in subdirs
```

previous: [P1:1](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
When in a subdirectory of a repository, path arguments should be
interpreted relative to the current directory not the root of the
working tree.
```

previous: [P1:2](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
The Git::repository object passed into setup_dir_diff() is configured to
handle this correctly but we create a new Git::repository here without
setting the WorkingSubdir argument.  By simply using the existing
repository, path arguments are handled relative to the current
directory.
```

incoming: [N:1](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
[ref] ([referenced subject], 2016-07-18)
corrected how path arguments are handled in a subdirectory, but
it introduced a regression in how entries outside of the
subdirectory are handled by dir-diff.
```

incoming: [N:3](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.
```

incoming: [N:4](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
Teach difftool to chdir to the toplevel of the repository before
preparing its temporary indexes.  This ensures that all of the
toplevel-relative paths are valid.
```

### 14b/hidden/direct-oracle

The change made in P1 to handle path arguments relative to the current directory introduced a regression where entries outside of the subdirectory are not properly handled by dir-diff. Specifically, the indexed paths are toplevel-relative and thus not added to the index when constructed from within the subdirectory.

previous: [P1:1](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
When in a subdirectory of a repository, path arguments should be
interpreted relative to the current directory not the root of the
working tree.
```

previous: [P1:2](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
The Git::repository object passed into setup_dir_diff() is configured to
handle this correctly but we create a new Git::repository here without
setting the WorkingSubdir argument.  By simply using the existing
repository, path arguments are handled relative to the current
directory.
```

incoming: [N:1](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
[ref] ([referenced subject], 2016-07-18)
corrected how path arguments are handled in a subdirectory, but
it introduced a regression in how entries outside of the
subdirectory are handled by dir-diff.
```

incoming: [N:3](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.
```

### 14b/hidden/module

Reconsider the earlier decision “When in a subdirectory of a repository, path arguments should be
interpreted relative to the current directory not the root of the
working tree.”. The new report gives the following behavior and its conditions. “The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.”

previous: [원문 구간](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
When in a subdirectory of a repository, path arguments should be
interpreted relative to the current directory not the root of the
working tree.
```

incoming: [원문 구간](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.
```

### 14b/raw/direct-full

The earlier decision P1 corrected how path arguments are handled in a subdirectory, but it introduced a regression where entries outside of the subdirectory were not properly handled by dir-diff. Specifically, the left side of the diff was constructed incorrectly due to the context of the subdirectory, leading to issues with toplevel-relative paths.

previous: [P1:0](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
difftool: fix argument handling in subdirs
```

previous: [P1:1](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
When in a subdirectory of a repository, path arguments should be
interpreted relative to the current directory not the root of the
working tree.
```

previous: [P1:2](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
The Git::repository object passed into setup_dir_diff() is configured to
handle this correctly but we create a new Git::repository here without
setting the WorkingSubdir argument.  By simply using the existing
repository, path arguments are handled relative to the current
directory.
```

incoming: [N:1](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
9ec26e7977 (difftool: fix argument handling in subdirs, 2016-07-18)
corrected how path arguments are handled in a subdirectory, but
it introduced a regression in how entries outside of the
subdirectory are handled by dir-diff.
```

incoming: [N:2](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
When preparing the right-side of the diff we only include the
changed paths in the temporary area.
```

incoming: [N:3](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.
```

incoming: [N:4](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
Teach difftool to chdir to the toplevel of the repository before
preparing its temporary indexes.  This ensures that all of the
toplevel-relative paths are valid.
```

### 14b/raw/module

Reconsider the earlier decision “When in a subdirectory of a repository, path arguments should be
interpreted relative to the current directory not the root of the
working tree.”. The new report gives the following behavior and its conditions. “The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.”

previous: [원문 구간](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007)

```text
When in a subdirectory of a repository, path arguments should be
interpreted relative to the current directory not the root of the
working tree.
```

incoming: [원문 구간](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a)

```text
The left side of the diff is constructed from a temporary
index that is built from the same set of changed files, but it
was being constructed from within the subdirectory.  This is a
problem because the indexed paths are toplevel-relative, and
thus they were not getting added to the index.
```
## email-priority

[새 보고](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23) · [실제 이전 결정](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb) · [유사 결정](https://github.com/git/git/commit/c8243933c74e0bebcc617f750ae3990ecca47759)

The Perl config reader takes the first rather than the last scalar key when repeated across config scopes, preferring global over local values. Preserve this direction and the conflicting/multiple-key condition.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/raw/module | keep | 실패: 보류 | keep |
| 14b/raw/direct-full | reassess | 성공: 동일 키가 여러 번 정의됐을 때 first-key-wins가 되어 global이 local보다 우선하는 방향을 보존한다. | reassess |
| 14b/raw/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-full | reassess | 성공: first/last 우선순위 역전과 global/local 중복 설정 조건을 올바르게 설명하고 인용한다. | invalid_output |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | reassess | 성공: 복수 설정값에서 global이 local보다 우선하는 잘못된 방향을 이전 설정 처리 최적화와 연결한다. | keep |
| 14b/hidden/direct-full | reassess | 성공: 설정 처리 최적화 이후 first/last 우선순위가 역전된 실제 동작을 설명하고 global/local 중복 조건을 인용한다. | keep |
| 14b/hidden/module | keep | 실패: 보류 | keep |
| 14b/hidden/direct-oracle | reassess | 성공: last-key-wins 위반과 global이 local보다 우선하는 방향을 이전 설정 처리 변경과 연결하며 인용에 중복 키 조건이 있다. | keep |

### 3b/raw/direct-full

The incoming report identifies a regression introduced in version 2.33.0 where the 'git-send-email' script prefers global configuration settings over local repository settings for certain configuration keys. This contradicts the earlier decision in P0, which aimed to respect the 'core.hooksPath' setting and avoid making assumptions about the location of hooks. The new evidence shows that the regression affects multiple configuration keys, including those related to SMTP server settings, which were previously handled correctly according to the earlier decision.

previous: [P0:0](https://github.com/git/git/commit/c8243933c74e0bebcc617f750ae3990ecca47759)

```text
git-send-email: Respect core.hooksPath setting
```

previous: [P0:1](https://github.com/git/git/commit/c8243933c74e0bebcc617f750ae3990ecca47759)

```text
get-send-email currently makes the assumption that the
'sendemail-validate' hook exists inside of the repository.
```

previous: [P0:2](https://github.com/git/git/commit/c8243933c74e0bebcc617f750ae3990ecca47759)

```text
Since the introduction of 'core.hooksPath' configuration option in
867ad08a261 (hooks: allow customizing where the hook directory is,
2016-05-04), this is no longer true.
```

previous: [P0:3](https://github.com/git/git/commit/c8243933c74e0bebcc617f750ae3990ecca47759)

```text
Instead of assuming a hardcoded repo relative path, query
git for the actual path of the hooks directory.
```

incoming: [N:0](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
send-email: fix a "first config key wins" regression in v2.33.0
```

incoming: [N:1](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
Fix a regression in my c95e3a3f0b8 (send-email: move trivial config
handling to Perl, 2021-05-28) where we'd pick the first config key out
of multiple defined ones, instead of using the normal "last key wins"
semantics of "git config --get".
```

incoming: [N:2](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
This broke e.g. cases where a .git/config would have a different
sendemail.smtpServer than ~/.gitconfig. We'd pick the ~/.gitconfig
over .git/config, instead of preferring the repository-local
version. The same would go for /etc/gitconfig etc.
```

incoming: [N:3](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
The full list of impacted config keys (the %config_settings values
which are references to scalars, not arrays) is:
```

incoming: [N:4](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
    sendemail.smtpencryption
    sendemail.smtpserver
    sendemail.smtpserverport
    sendemail.smtpuser
    sendemail.smtppass
    sendemail.smtpdomain
    sendemail.smtpauth
    sendemail.smtpbatchsize
    sendemail.smtprelogindelay
    sendemail.tocmd
    sendemail.cccmd
    sendemail.aliasfiletype
    sendemail.envelopesender
    sendemail.confirm
    sendemail.from
    sendemail.assume8bitencoding
    sendemail.composeencoding
    sendemail.transferencoding
    sendemail.sendmailcmd
```

incoming: [N:5](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
I.e. having any of these set in say ~/.gitconfig and in-repo
.git/config regressed in v2.33.0 to prefer the --global one over the
--local.
```

incoming: [N:6](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
To test this add a test of config priority to one of these config
variables, most don't have tests at all, but there was an existing one
for sendemail.8bitEncoding.
```

incoming: [N:7](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
The "git config" (instead of "test_config") is somewhat of an
anti-pattern, but follows established conventions in
t9001-send-email.sh, likewise with any other pattern or idiom in this
test.
```

incoming: [N:8](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
The populating of home/.gitconfig and setting of HOME= is copied from
a test in t0017-env-helper.sh added in 1ff750b128e (tests: make
GIT_TEST_GETTEXT_POISON a boolean, 2019-06-21). This test fails
without this bugfix, but now it works.
```

### 3b/raw/module

no supported observation with its condition in the report window

### 3b/hidden/direct-full

The incoming report introduces a regression where the first config key now takes precedence over subsequent ones, contrary to the intended last-key-wins behavior. This change affects multiple config keys listed in N:4, including sendemail.smtpserver, which could lead to misconfiguration if ~/.gitconfig overrides the repository-local settings. The earlier decision in P0 focused on optimizing the startup time and handling specific config types, but the new evidence shows a deviation from this intent.

previous: [P0:0](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
send-email: move trivial config handling to Perl
```

previous: [P0:1](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
Optimize the startup time of git-send-email by using an amended
config_regexp() function to retrieve the list of config keys and
values we're interested in.
```

previous: [P0:2](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
For boolean keys we can handle the [true|false] case ourselves, and
the "--get" case didn't need any parsing. Let's leave "--path" and
other "--bool" cases to "git config". I'm not bothering with the
"undef" or "" case (true and false, respectively), let's just punt on
those and others and have "git config --type=bool" handle it.
```

previous: [P0:3](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
The "grep { defined } @values" here covers a rather subtle case. For
list values such as sendemail.to it is possible as with any other
config key to provide a plain "-c sendemail.to", i.e. to set the key
as a boolean true. In that case the Git::config() API will return an
empty string, but this new parser will correctly return "undef".
```

previous: [P0:4](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
However, that means we can end up with "undef" in the middle of a
list. E.g. for sendemail.smtpserveroption in conjuction with
sendemail.smtpserver as a path this would have produce a warning. For
most of the other keys we'd behave the same despite the subtle change
in the value, e.g. sendemail.to would behave the same because
Mail::Address->parse() happens to return an empty list if fed
"undef". For the boolean values we were already prepared to handle
these variables being initialized as undef anyway.
```

previous: [P0:5](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
This brings the runtime of "git send-email" from ~60-~70ms to a very
steady ~40ms on my test box. We now run just one "git config"
invocation on startup instead of 8, the exact number will differ based
on the local sendemail.* config. I happen to have 8 of those set.
```

previous: [P0:6](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
This brings the runtime of t9001-send-email.sh from ~13s down to ~12s
for me. The change there is less impressive as many of those tests set
various config values, and we're also getting to the point of
diminishing returns for optimizing "git send-email" itself.
```

incoming: [N:0](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
send-email: fix a "first config key wins" regression in v2.33.0
```

incoming: [N:1](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
Fix a regression in my [ref] ([referenced subject], 2021-05-28) where we'd pick the first config key out
of multiple defined ones, instead of using the normal "last key wins"
semantics of "git config --get".
```

incoming: [N:2](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
This broke e.g. cases where a .git/config would have a different
sendemail.smtpServer than ~/.gitconfig. We'd pick the ~/.gitconfig
over .git/config, instead of preferring the repository-local
version. The same would go for /etc/gitconfig etc.
```

incoming: [N:3](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
The full list of impacted config keys (the %config_settings values
which are references to scalars, not arrays) is:
```

incoming: [N:4](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
    sendemail.smtpencryption
    sendemail.smtpserver
    sendemail.smtpserverport
    sendemail.smtpuser
    sendemail.smtppass
    sendemail.smtpdomain
    sendemail.smtpauth
    sendemail.smtpbatchsize
    sendemail.smtprelogindelay
    sendemail.tocmd
    sendemail.cccmd
    sendemail.aliasfiletype
    sendemail.envelopesender
    sendemail.confirm
    sendemail.from
    sendemail.assume8bitencoding
    sendemail.composeencoding
    sendemail.transferencoding
    sendemail.sendmailcmd
```

incoming: [N:5](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
I.e. having any of these set in say ~/.gitconfig and in-repo
.git/config regressed in v2.33.0 to prefer the --global one over the
--local.
```

incoming: [N:6](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
To test this add a test of config priority to one of these config
variables, most don't have tests at all, but there was an existing one
for sendemail.8bitEncoding.
```

incoming: [N:7](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
The "git config" (instead of "test_config") is somewhat of an
anti-pattern, but follows established conventions in
t9001-send-email.sh, likewise with any other pattern or idiom in this
test.
```

incoming: [N:8](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
The populating of home/.gitconfig and setting of HOME= is copied from
a test in t0017-env-helper.sh added in [ref] (tests: make
GIT_TEST_GETTEXT_POISON a boolean, 2019-06-21). This test fails
without this bugfix, but now it works.
```

### 3b/hidden/direct-oracle

The new evidence indicates a regression in the handling of multiple config keys, specifically mentioning that the behavior changed in version 2.33.0 to prefer the global configuration over the local one. This contradicts the original decision in P0, which aimed to optimize the startup time by retrieving specific config keys and values without affecting the default behavior of 'last key wins'.

previous: [P0:1](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
Optimize the startup time of git-send-email by using an amended
config_regexp() function to retrieve the list of config keys and
values we're interested in.
```

previous: [P0:2](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
For boolean keys we can handle the [true|false] case ourselves, and
the "--get" case didn't need any parsing. Let's leave "--path" and
other "--bool" cases to "git config". I'm not bothering with the
"undef" or "" case (true and false, respectively), let's just punt on
those and others and have "git config --type=bool" handle it.
```

incoming: [N:1](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
Fix a regression in my [ref] ([referenced subject], 2021-05-28) where we'd pick the first config key out
of multiple defined ones, instead of using the normal "last key wins"
semantics of "git config --get".
```

incoming: [N:2](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
This broke e.g. cases where a .git/config would have a different
sendemail.smtpServer than ~/.gitconfig. We'd pick the ~/.gitconfig
over .git/config, instead of preferring the repository-local
version. The same would go for /etc/gitconfig etc.
```

incoming: [N:5](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
I.e. having any of these set in say ~/.gitconfig and in-repo
.git/config regressed in v2.33.0 to prefer the --global one over the
--local.
```

### 3b/hidden/module

no unique decision in the document comparison

### 14b/hidden/direct-full

The new evidence indicates a regression introduced in v2.33.0 where the first config key was incorrectly chosen instead of the last one, which affects the behavior of certain sendemail settings. This contradicts the expected behavior described in the earlier decision P0, which aimed to optimize the retrieval of config keys and values without altering their precedence rules.

previous: [P0:0](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
send-email: move trivial config handling to Perl
```

previous: [P0:1](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
Optimize the startup time of git-send-email by using an amended
config_regexp() function to retrieve the list of config keys and
values we're interested in.
```

previous: [P0:2](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
For boolean keys we can handle the [true|false] case ourselves, and
the "--get" case didn't need any parsing. Let's leave "--path" and
other "--bool" cases to "git config". I'm not bothering with the
"undef" or "" case (true and false, respectively), let's just punt on
those and others and have "git config --type=bool" handle it.
```

previous: [P0:3](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
The "grep { defined } @values" here covers a rather subtle case. For
list values such as sendemail.to it is possible as with any other
config key to provide a plain "-c sendemail.to", i.e. to set the key
as a boolean true. In that case the Git::config() API will return an
empty string, but this new parser will correctly return "undef".
```

previous: [P0:4](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
However, that means we can end up with "undef" in the middle of a
list. E.g. for sendemail.smtpserveroption in conjuction with
sendemail.smtpserver as a path this would have produce a warning. For
most of the other keys we'd behave the same despite the subtle change
in the value, e.g. sendemail.to would behave the same because
Mail::Address->parse() happens to return an empty list if fed
"undef". For the boolean values we were already prepared to handle
these variables being initialized as undef anyway.
```

previous: [P0:5](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
This brings the runtime of "git send-email" from ~60-~70ms to a very
steady ~40ms on my test box. We now run just one "git config"
invocation on startup instead of 8, the exact number will differ based
on the local sendemail.* config. I happen to have 8 of those set.
```

previous: [P0:6](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
This brings the runtime of t9001-send-email.sh from ~13s down to ~12s
for me. The change there is less impressive as many of those tests set
various config values, and we're also getting to the point of
diminishing returns for optimizing "git send-email" itself.
```

incoming: [N:0](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
send-email: fix a "first config key wins" regression in v2.33.0
```

incoming: [N:1](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
Fix a regression in my [ref] ([referenced subject], 2021-05-28) where we'd pick the first config key out
of multiple defined ones, instead of using the normal "last key wins"
semantics of "git config --get".
```

incoming: [N:2](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
This broke e.g. cases where a .git/config would have a different
sendemail.smtpServer than ~/.gitconfig. We'd pick the ~/.gitconfig
over .git/config, instead of preferring the repository-local
version. The same would go for /etc/gitconfig etc.
```

incoming: [N:5](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
I.e. having any of these set in say ~/.gitconfig and in-repo
.git/config regressed in v2.33.0 to prefer the --global one over the
--local.
```

### 14b/hidden/direct-oracle

The earlier optimization in P0:2 led to a regression where the last key wins semantics were not preserved, causing preference for global configurations over local ones.

previous: [P0:2](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
For boolean keys we can handle the [true|false] case ourselves, and
the "--get" case didn't need any parsing. Let's leave "--path" and
other "--bool" cases to "git config". I'm not bothering with the
"undef" or "" case (true and false, respectively), let's just punt on
those and others and have "git config --type=bool" handle it.
```

incoming: [N:1](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
Fix a regression in my [ref] ([referenced subject], 2021-05-28) where we'd pick the first config key out
of multiple defined ones, instead of using the normal "last key wins"
semantics of "git config --get".
```

incoming: [N:2](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
This broke e.g. cases where a .git/config would have a different
sendemail.smtpServer than ~/.gitconfig. We'd pick the ~/.gitconfig
over .git/config, instead of preferring the repository-local
version. The same would go for /etc/gitconfig etc.
```

incoming: [N:5](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
I.e. having any of these set in say ~/.gitconfig and in-repo
.git/config regressed in v2.33.0 to prefer the --global one over the
--local.
```

### 14b/raw/direct-full

The new evidence indicates that the changes made in P1 introduced a regression where the first config key out of multiple defined ones was picked instead of using the normal 'last key wins' semantics of 'git config --get'. This affected several sendemail.* configuration keys, leading to incorrect preference of global configurations over local ones.

previous: [P1:0](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
send-email: move trivial config handling to Perl
```

previous: [P1:1](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
Optimize the startup time of git-send-email by using an amended
config_regexp() function to retrieve the list of config keys and
values we're interested in.
```

previous: [P1:2](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
For boolean keys we can handle the [true|false] case ourselves, and
the "--get" case didn't need any parsing. Let's leave "--path" and
other "--bool" cases to "git config". I'm not bothering with the
"undef" or "" case (true and false, respectively), let's just punt on
those and others and have "git config --type=bool" handle it.
```

previous: [P1:3](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
The "grep { defined } @values" here covers a rather subtle case. For
list values such as sendemail.to it is possible as with any other
config key to provide a plain "-c sendemail.to", i.e. to set the key
as a boolean true. In that case the Git::config() API will return an
empty string, but this new parser will correctly return "undef".
```

previous: [P1:4](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
However, that means we can end up with "undef" in the middle of a
list. E.g. for sendemail.smtpserveroption in conjuction with
sendemail.smtpserver as a path this would have produce a warning. For
most of the other keys we'd behave the same despite the subtle change
in the value, e.g. sendemail.to would behave the same because
Mail::Address->parse() happens to return an empty list if fed
"undef". For the boolean values we were already prepared to handle
these variables being initialized as undef anyway.
```

previous: [P1:5](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
This brings the runtime of "git send-email" from ~60-~70ms to a very
steady ~40ms on my test box. We now run just one "git config"
invocation on startup instead of 8, the exact number will differ based
on the local sendemail.* config. I happen to have 8 of those set.
```

previous: [P1:6](https://github.com/git/git/commit/c95e3a3f0b8107b5dc7eac9dfdb9e5238280c9fb)

```text
This brings the runtime of t9001-send-email.sh from ~13s down to ~12s
for me. The change there is less impressive as many of those tests set
various config values, and we're also getting to the point of
diminishing returns for optimizing "git send-email" itself.
```

incoming: [N:0](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
send-email: fix a "first config key wins" regression in v2.33.0
```

incoming: [N:1](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
Fix a regression in my c95e3a3f0b8 (send-email: move trivial config
handling to Perl, 2021-05-28) where we'd pick the first config key out
of multiple defined ones, instead of using the normal "last key wins"
semantics of "git config --get".
```

incoming: [N:2](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
This broke e.g. cases where a .git/config would have a different
sendemail.smtpServer than ~/.gitconfig. We'd pick the ~/.gitconfig
over .git/config, instead of preferring the repository-local
version. The same would go for /etc/gitconfig etc.
```

incoming: [N:3](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
The full list of impacted config keys (the %config_settings values
which are references to scalars, not arrays) is:
```

incoming: [N:4](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
    sendemail.smtpencryption
    sendemail.smtpserver
    sendemail.smtpserverport
    sendemail.smtpuser
    sendemail.smtppass
    sendemail.smtpdomain
    sendemail.smtpauth
    sendemail.smtpbatchsize
    sendemail.smtprelogindelay
    sendemail.tocmd
    sendemail.cccmd
    sendemail.aliasfiletype
    sendemail.envelopesender
    sendemail.confirm
    sendemail.from
    sendemail.assume8bitencoding
    sendemail.composeencoding
    sendemail.transferencoding
    sendemail.sendmailcmd
```

incoming: [N:5](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
I.e. having any of these set in say ~/.gitconfig and in-repo
.git/config regressed in v2.33.0 to prefer the --global one over the
--local.
```

incoming: [N:6](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
To test this add a test of config priority to one of these config
variables, most don't have tests at all, but there was an existing one
for sendemail.8bitEncoding.
```

incoming: [N:7](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
The "git config" (instead of "test_config") is somewhat of an
anti-pattern, but follows established conventions in
t9001-send-email.sh, likewise with any other pattern or idiom in this
test.
```

incoming: [N:8](https://github.com/git/git/commit/b996f84989f78c8f6d2429b5f0b9785e13f7af23)

```text
The populating of home/.gitconfig and setting of HOME= is copied from
a test in t0017-env-helper.sh added in 1ff750b128e (tests: make
GIT_TEST_GETTEXT_POISON a boolean, 2019-06-21). This test fails
without this bugfix, but now it works.
```

### 14b/raw/module

no supported observation with its condition in the report window

### 14b/hidden/module

no unique decision in the document comparison
## freebsd-cwd

[새 보고](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac) · [실제 이전 결정](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f) · [유사 결정](https://github.com/git/git/commit/f4c21e89d7c6b578140e90c02b40eccb51ab8428)

Changing the old cwd buffer to strbuf causes failure on long, permission-restricted FreeBSD paths; a smaller buffer can hit EACCES even though a larger one succeeds. Link the buffer change, condition and result.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/raw/module | reassess | 실패: 재시도 수정과 경로 조건은 있지만 작은 버퍼로 EACCES가 발생하는 실제 실패 설명을 선택하지 못했다. | keep |
| 14b/raw/direct-full | reassess | 실패: 긴 경로·권한 조건은 언급하나 strbuf가 경로 길이 제한을 도입했다고 부정확하게 요약하고 실제 getcwd/EACCES 실패를 설명하지 않는다. | keep |
| 14b/raw/module | reassess | 성공: strbuf 변경과 FreeBSD에서 작은 버퍼·권한 부족 때문에 EACCES가 나고 더 큰 버퍼는 성공할 수 있다는 동작을 설명에 인용하여 보존한다. | keep |
| 3b/hidden/direct-full | reassess | 실패: 긴 경로에서 작은 버퍼가 EACCES를 유발한다는 동작 연결을 설명하지 않고 FreeBSD 고려 부족으로 일반화한다. | keep |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | reassess | 실패: 이전 결정이 PATH_MAX 버퍼를 충분하다고 가정했다며 실제 strbuf 전환 방향을 뒤집는다. | reassess |
| 14b/hidden/direct-full | reassess | 실패: 긴 경로·권한 조건과 strbuf 변경은 맞지만 실제 getcwd 실패나 EACCES 동작을 설명하지 않고 새 이슈라고만 표현한다. 부분 성공이다. | keep |
| 14b/hidden/module | keep | 실패: 보류 | keep |
| 14b/hidden/direct-oracle | reassess | 실패: strbuf 전환과 긴 경로·권한 조건은 맞지만 결과를 regression이라고만 부르며 getcwd의 EACCES/작은 버퍼 실패 동작을 설명하지 않는다. 부분 성공이다. | keep |

### 3b/hidden/direct-full

The incoming report introduces a new issue related to FreeBSD's implementation of getcwd(3), where FreeBSD uses a fallback method based on readdir(3) that requires read and execute permissions on path components. This contradicts the original decision in P0, which focused on converting functions to use strbuf without considering the specific behavior of FreeBSD's getcwd(3). The new evidence suggests that the original decision might not fully address the FreeBSD-specific issue.

previous: [P0:0](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
setup: convert setup_git_directory_gently_1 et al. to strbuf
```

previous: [P0:1](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
Convert setup_git_directory_gently_1() and its helper functions
setup_explicit_git_dir(), setup_discovered_git_dir() and
setup_bare_git_dir() to use a struct strbuf to hold the current working
directory.  Replacing the PATH_MAX-sized buffer used before removes a
path length limition on some file systems.  The functions are converted
all in one go because they all read and write the variable cwd.
```

incoming: [N:0](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
strbuf: support long paths w/o read rights in strbuf_getcwd() on FreeBSD
```

incoming: [N:1](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
FreeBSD implements getcwd(3) as a syscall, but falls back to a version
based on readdir(3) if it fails for some reason.  The latter requires
permissions to read and execute path components, while the former does
not.  That means that if our buffer is too small and we're missing
rights we could get EACCES, but we may succeed with a bigger buffer.
```

incoming: [N:2](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.
```

incoming: [N:3](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
This fixes a regression introduced with [ref] ([referenced subject], 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.
```

### 3b/hidden/direct-oracle

The new evidence indicates that FreeBSD's implementation of getcwd(3) can fail due to insufficient permissions, leading to EACCES errors for long paths. This contradicts the assumption made in P0 that PATH_MAX-sized buffers are sufficient without considering permission issues.

previous: [P0:1](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
Convert setup_git_directory_gently_1() and its helper functions
setup_explicit_git_dir(), setup_discovered_git_dir() and
setup_bare_git_dir() to use a struct strbuf to hold the current working
directory.  Replacing the PATH_MAX-sized buffer used before removes a
path length limition on some file systems.  The functions are converted
all in one go because they all read and write the variable cwd.
```

incoming: [N:1](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
FreeBSD implements getcwd(3) as a syscall, but falls back to a version
based on readdir(3) if it fails for some reason.  The latter requires
permissions to read and execute path components, while the former does
not.  That means that if our buffer is too small and we're missing
rights we could get EACCES, but we may succeed with a bigger buffer.
```

incoming: [N:3](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
This fixes a regression introduced with [ref] ([referenced subject], 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.
```

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The new evidence suggests that the change in handling nonexistent top-level paths might lead to issues with long paths longer than 127 bytes on FreeBSD due to permission issues. This contradicts the original decision to avoid stripping leading slashes and removing slashes from groups of multiple slashes, which could result in incorrect behavior for such paths.

previous: [P0:0](https://github.com/git/git/commit/f4c21e89d7c6b578140e90c02b40eccb51ab8428)

```text
real_path(): properly handle nonexistent top-level paths
```

previous: [P0:2](https://github.com/git/git/commit/f4c21e89d7c6b578140e90c02b40eccb51ab8428)

```text
1. Do not strip off a leading slash, because that erroneously turns an
   absolute path into a relative path.
```

incoming: [N:0](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
strbuf: support long paths w/o read rights in strbuf_getcwd() on FreeBSD
```

incoming: [N:1](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
FreeBSD implements getcwd(3) as a syscall, but falls back to a version
based on readdir(3) if it fails for some reason.  The latter requires
permissions to read and execute path components, while the former does
not.  That means that if our buffer is too small and we're missing
rights we could get EACCES, but we may succeed with a bigger buffer.
```

incoming: [N:2](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.
```

incoming: [N:3](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
This fixes a regression introduced with 7333ed17 (setup: convert
setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.
```

### 3b/raw/module

Reconsider the earlier decision “Convert setup_git_directory_gently_1() and its helper functions
setup_explicit_git_dir(), setup_discovered_git_dir() and
setup_bare_git_dir() to use a struct strbuf to hold the current working
directory.  Replacing the PATH_MAX-sized buffer used before removes a
path length limition on some file systems.  The functions are converted
all in one go because they all read and write the variable cwd.”. The new report gives the following behavior and its conditions. “Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.

This fixes a regression introduced with 7333ed17 (setup: convert
setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.”

previous: [원문 구간](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
Convert setup_git_directory_gently_1() and its helper functions
setup_explicit_git_dir(), setup_discovered_git_dir() and
setup_bare_git_dir() to use a struct strbuf to hold the current working
directory.  Replacing the PATH_MAX-sized buffer used before removes a
path length limition on some file systems.  The functions are converted
all in one go because they all read and write the variable cwd.
```

incoming: [원문 구간](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.

This fixes a regression introduced with 7333ed17 (setup: convert
setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.
```

### 14b/hidden/direct-full

The conversion of setup_git_directory_gently_1 and related functions to use strbuf (P0) aimed to remove a path length limitation. However, the new evidence shows that this change introduced a regression for paths longer than 127 bytes with restricted permissions, indicating that the original path length limitation was circumvented but new issues arose due to permission handling.

previous: [P0:0](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
setup: convert setup_git_directory_gently_1 et al. to strbuf
```

previous: [P0:1](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
Convert setup_git_directory_gently_1() and its helper functions
setup_explicit_git_dir(), setup_discovered_git_dir() and
setup_bare_git_dir() to use a struct strbuf to hold the current working
directory.  Replacing the PATH_MAX-sized buffer used before removes a
path length limition on some file systems.  The functions are converted
all in one go because they all read and write the variable cwd.
```

incoming: [N:0](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
strbuf: support long paths w/o read rights in strbuf_getcwd() on FreeBSD
```

incoming: [N:1](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
FreeBSD implements getcwd(3) as a syscall, but falls back to a version
based on readdir(3) if it fails for some reason.  The latter requires
permissions to read and execute path components, while the former does
not.  That means that if our buffer is too small and we're missing
rights we could get EACCES, but we may succeed with a bigger buffer.
```

incoming: [N:2](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.
```

incoming: [N:3](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
This fixes a regression introduced with [ref] ([referenced subject], 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.
```

### 14b/hidden/direct-oracle

The conversion to use a struct strbuf in P0 removed a path length limitation, but introduced a regression for paths longer than 127 bytes with missing read or execute permissions, as noted in N.

previous: [P0:1](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
Convert setup_git_directory_gently_1() and its helper functions
setup_explicit_git_dir(), setup_discovered_git_dir() and
setup_bare_git_dir() to use a struct strbuf to hold the current working
directory.  Replacing the PATH_MAX-sized buffer used before removes a
path length limition on some file systems.  The functions are converted
all in one go because they all read and write the variable cwd.
```

incoming: [N:1](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
FreeBSD implements getcwd(3) as a syscall, but falls back to a version
based on readdir(3) if it fails for some reason.  The latter requires
permissions to read and execute path components, while the former does
not.  That means that if our buffer is too small and we're missing
rights we could get EACCES, but we may succeed with a bigger buffer.
```

incoming: [N:3](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
This fixes a regression introduced with [ref] ([referenced subject], 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.
```

### 14b/hidden/module

no supported observation with its condition in the report window

### 14b/raw/direct-full

The conversion to strbuf in P1 introduced a limitation on path lengths and permissions, causing issues for paths longer than 127 bytes with restricted permissions.

previous: [P1:0](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
setup: convert setup_git_directory_gently_1 et al. to strbuf
```

previous: [P1:1](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
Convert setup_git_directory_gently_1() and its helper functions
setup_explicit_git_dir(), setup_discovered_git_dir() and
setup_bare_git_dir() to use a struct strbuf to hold the current working
directory.  Replacing the PATH_MAX-sized buffer used before removes a
path length limition on some file systems.  The functions are converted
all in one go because they all read and write the variable cwd.
```

incoming: [N:0](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
strbuf: support long paths w/o read rights in strbuf_getcwd() on FreeBSD
```

incoming: [N:1](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
FreeBSD implements getcwd(3) as a syscall, but falls back to a version
based on readdir(3) if it fails for some reason.  The latter requires
permissions to read and execute path components, while the former does
not.  That means that if our buffer is too small and we're missing
rights we could get EACCES, but we may succeed with a bigger buffer.
```

incoming: [N:2](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.
```

incoming: [N:3](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
This fixes a regression introduced with 7333ed17 (setup: convert
setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.
```

### 14b/raw/module

Reconsider the earlier decision “Convert setup_git_directory_gently_1() and its helper functions
setup_explicit_git_dir(), setup_discovered_git_dir() and
setup_bare_git_dir() to use a struct strbuf to hold the current working
directory.  Replacing the PATH_MAX-sized buffer used before removes a
path length limition on some file systems.  The functions are converted
all in one go because they all read and write the variable cwd.”. The new report gives the following behavior and its conditions. “FreeBSD implements getcwd(3) as a syscall, but falls back to a version
based on readdir(3) if it fails for some reason.  The latter requires
permissions to read and execute path components, while the former does
not.  That means that if our buffer is too small and we're missing
rights we could get EACCES, but we may succeed with a bigger buffer.

Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.”

previous: [원문 구간](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f)

```text
Convert setup_git_directory_gently_1() and its helper functions
setup_explicit_git_dir(), setup_discovered_git_dir() and
setup_bare_git_dir() to use a struct strbuf to hold the current working
directory.  Replacing the PATH_MAX-sized buffer used before removes a
path length limition on some file systems.  The functions are converted
all in one go because they all read and write the variable cwd.
```

incoming: [원문 구간](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac)

```text
FreeBSD implements getcwd(3) as a syscall, but falls back to a version
based on readdir(3) if it fails for some reason.  The latter requires
permissions to read and execute path components, while the former does
not.  That means that if our buffer is too small and we're missing
rights we could get EACCES, but we may succeed with a bigger buffer.

Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.
```
## fsck-empty

[새 보고](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d) · [실제 이전 결정](https://github.com/git/git/commit/3ba7a065527a27f45659398e882feaa1165cbb4c) · [유사 결정](https://github.com/git/git/commit/eb726f2d760dd78915e4a24f014ab411a165daa3)

Changing read-error/corruption classification leads fsck to misreport empty loose object files as a read/invalid argument error. Empty loose file, reporting behavior, and connection to the earlier decision are required.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 빈 파일의 잘못된 read 오류를 설명하지 않고 EMFILE 판단과 새 오류 메시지가 모순이라고 잘못 설명한다. | reassess |
| 3b/raw/module | reassess | 성공: 기존 EMFILE 분류 변경과 빈 loose 파일에서 Invalid argument를 내는 동작을 함께 보존한다. | keep |
| 14b/raw/direct-full | reassess | 실패: 빈 loose 객체 파일을 corrupt로 표시해서는 안 된다고 덧붙여 원문의 오류 분류 방향을 뒤집는다. 실제 회귀는 Invalid argument 읽기 오류로 잘못 표시한 것이다. | reassess |
| 14b/raw/module | reassess | 성공: 기존 EMFILE 분류 변경과 빈 loose 파일에서 Invalid argument를 내는 동작을 함께 보존한다. | keep |
| 3b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | keep | 실패: 보류 | keep |
| 14b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 14b/hidden/module | keep | 실패: 보류 | keep |
| 14b/hidden/direct-oracle | reassess | 실패: 빈 파일 read 오류를 찾았지만 여전히 잘못된 corruption 보고가 문제라고 설명하여 현재 회귀의 오류 분류 방향을 뒤집는다. | reassess |

### 3b/raw/direct-full

The incoming report introduces a new error message for empty loose object files, contradicting the original decision that such objects are not corrupt if they cannot be read due to EMFILE. This change affects the error handling and reporting mechanism, which was previously correct.

previous: [P0:0](https://github.com/git/git/commit/3ba7a065527a27f45659398e882feaa1165cbb4c)

```text
A loose object is not corrupt if it cannot be read due to EMFILE
```

incoming: [N:0](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
fsck: give accurate error message on empty loose object files
```

incoming: [N:1](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message
```

incoming: [N:2](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
  fatal: failed to read object <sha1>: Invalid argument
```

incoming: [N:3](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
This comes from a failure of mmap on this empty file, which sets errno to
EINVAL. Instead of calling xmmap on empty file, we display a clean error
message ourselves, and return a NULL pointer. The new message is
```

incoming: [N:4](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
  error: object file .git/objects/09/<rest-of-sha1> is empty
  fatal: loose object <sha1> (stored in .git/objects/09/<rest-of-sha1>) is corrupt
```

incoming: [N:5](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
The second line was already there before the regression in 3ba7a065527a,
and the first is an additional message, that should help diagnosing the
problem for the user.
```

### 3b/raw/module

Reconsider the earlier decision “"git fsck" bails out with a claim that a loose object that cannot be
read but exists on the filesystem to be corrupt, which is wrong when
read_object() failed due to e.g. EMFILE.”. The new report gives the following behavior and its conditions. “Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message

  fatal: failed to read object <sha1>: Invalid argument”

previous: [원문 구간](https://github.com/git/git/commit/3ba7a065527a27f45659398e882feaa1165cbb4c)

```text
"git fsck" bails out with a claim that a loose object that cannot be
read but exists on the filesystem to be corrupt, which is wrong when
read_object() failed due to e.g. EMFILE.
```

incoming: [원문 구간](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message

  fatal: failed to read object <sha1>: Invalid argument
```

### 3b/hidden/direct-full

The incoming report introduces a new error message for empty loose object files, contradicting the previous decision that fsck should not abort upon finding an empty blob. This change affects the error handling and reporting mechanism, which was previously set to avoid aborting fsck on empty blobs.

previous: [P0:0](https://github.com/git/git/commit/eb726f2d760dd78915e4a24f014ab411a165daa3)

```text
fsck: do not abort upon finding an empty blob
```

previous: [P0:1](https://github.com/git/git/commit/eb726f2d760dd78915e4a24f014ab411a165daa3)

```text
Asking fwrite() to write one item of size bytes results in fwrite()
reporting "I wrote zero item", when size is zero. Instead, we could
ask it to write "size" items of 1 byte and expect it to report that
"I wrote size items" when it succeeds, with any value of size,
including zero.
```

previous: [P0:2](https://github.com/git/git/commit/eb726f2d760dd78915e4a24f014ab411a165daa3)

```text
Noticed and reported by BJ Hargrave.
```

incoming: [N:0](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
fsck: give accurate error message on empty loose object files
```

incoming: [N:1](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
Since [ref] ([referenced subject]), "git fsck" on a repository with an empty
loose object file complains with the error message
```

incoming: [N:2](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
  fatal: failed to read object <sha1>: Invalid argument
```

incoming: [N:3](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
This comes from a failure of mmap on this empty file, which sets errno to
EINVAL. Instead of calling xmmap on empty file, we display a clean error
message ourselves, and return a NULL pointer. The new message is
```

incoming: [N:4](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
  error: object file .git/objects/09/<rest-of-sha1> is empty
  fatal: loose object <sha1> (stored in .git/objects/09/<rest-of-sha1>) is corrupt
```

incoming: [N:5](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
The second line was already there before the regression in [ref],
and the first is an additional message, that should help diagnosing the
problem for the user.
```

### 3b/hidden/direct-oracle

The incoming report mentions a new error message from 'git fsck' when encountering an empty loose object file, which differs from the previous decision where 'git fsck' was reported as bailing out with a claim of corruption. This change suggests a different underlying issue, not related to the original advice about fwrite().

### 3b/hidden/module

no unique decision in the document comparison

### 14b/hidden/direct-full

The earlier decision P0 aimed to prevent 'fwrite()' from aborting upon encountering an empty blob, but the new evidence shows that 'git fsck' still encounters issues with empty loose object files, leading to misleading error messages. This indicates that the condition of handling empty blobs needs further refinement.

previous: [P0:0](https://github.com/git/git/commit/eb726f2d760dd78915e4a24f014ab411a165daa3)

```text
fsck: do not abort upon finding an empty blob
```

incoming: [N:0](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
fsck: give accurate error message on empty loose object files
```

incoming: [N:1](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
Since [ref] ([referenced subject]), "git fsck" on a repository with an empty
loose object file complains with the error message
```

incoming: [N:2](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
  fatal: failed to read object <sha1>: Invalid argument
```

incoming: [N:3](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
This comes from a failure of mmap on this empty file, which sets errno to
EINVAL. Instead of calling xmmap on empty file, we display a clean error
message ourselves, and return a NULL pointer. The new message is
```

incoming: [N:4](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
  error: object file .git/objects/09/<rest-of-sha1> is empty
  fatal: loose object <sha1> (stored in .git/objects/09/<rest-of-sha1>) is corrupt
```

incoming: [N:5](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
The second line was already there before the regression in [ref],
and the first is an additional message, that should help diagnosing the
problem for the user.
```

### 14b/hidden/direct-oracle

The new evidence shows that 'git fsck' fails with a specific error message related to reading an empty loose object file, which was not addressed by the previous decision P1. This indicates that the condition under which 'git fsck' incorrectly reports corruption needs further consideration.

previous: [P1:1](https://github.com/git/git/commit/3ba7a065527a27f45659398e882feaa1165cbb4c)

```text
"git fsck" bails out with a claim that a loose object that cannot be
read but exists on the filesystem to be corrupt, which is wrong when
read_object() failed due to e.g. EMFILE.
```

incoming: [N:1](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
Since [ref] ([referenced subject]), "git fsck" on a repository with an empty
loose object file complains with the error message
```

incoming: [N:2](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
  fatal: failed to read object <sha1>: Invalid argument
```

incoming: [N:3](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
This comes from a failure of mmap on this empty file, which sets errno to
EINVAL. Instead of calling xmmap on empty file, we display a clean error
message ourselves, and return a NULL pointer. The new message is
```

### 14b/raw/direct-full

The earlier decision in P0 aimed to prevent 'git fsck' from marking objects as corrupt when they cannot be read due to EMFILE. However, the new evidence shows that the change introduced in P0 has led to a different issue where 'git fsck' now gives an incorrect error message for empty loose object files, which should not be marked as corrupt. This indicates that the condition under which the earlier decision was made may need to be refined to avoid such unintended consequences.

previous: [P0:0](https://github.com/git/git/commit/3ba7a065527a27f45659398e882feaa1165cbb4c)

```text
A loose object is not corrupt if it cannot be read due to EMFILE
```

previous: [P0:1](https://github.com/git/git/commit/3ba7a065527a27f45659398e882feaa1165cbb4c)

```text
"git fsck" bails out with a claim that a loose object that cannot be
read but exists on the filesystem to be corrupt, which is wrong when
read_object() failed due to e.g. EMFILE.
```

incoming: [N:1](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message
```

incoming: [N:2](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
  fatal: failed to read object <sha1>: Invalid argument
```

incoming: [N:4](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
  error: object file .git/objects/09/<rest-of-sha1> is empty
  fatal: loose object <sha1> (stored in .git/objects/09/<rest-of-sha1>) is corrupt
```

incoming: [N:5](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
The second line was already there before the regression in 3ba7a065527a,
and the first is an additional message, that should help diagnosing the
problem for the user.
```

### 14b/raw/module

Reconsider the earlier decision “"git fsck" bails out with a claim that a loose object that cannot be
read but exists on the filesystem to be corrupt, which is wrong when
read_object() failed due to e.g. EMFILE.”. The new report gives the following behavior and its conditions. “Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message

  fatal: failed to read object <sha1>: Invalid argument”

previous: [원문 구간](https://github.com/git/git/commit/3ba7a065527a27f45659398e882feaa1165cbb4c)

```text
"git fsck" bails out with a claim that a loose object that cannot be
read but exists on the filesystem to be corrupt, which is wrong when
read_object() failed due to e.g. EMFILE.
```

incoming: [원문 구간](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d)

```text
Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message

  fatal: failed to read object <sha1>: Invalid argument
```

### 14b/hidden/module

the exact passages did not reproduce the document judgment
## header

[새 보고](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99) · [실제 이전 결정](https://github.com/git/git/commit/3b6a8db3b03adb118bfafb90bbc710068dbd6d14) · [유사 결정](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

The enum error from unpacking is mishandled: fsck/caller tries to parse an uninitialized header or reports a parse failure instead of an unpack failure.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/raw/module | reassess | 실패: 선택한 이전 문단은 enum 도입 자체가 아니라 선행 반환값 변경이다. enum 처리 오류의 연결 근거가 빠진다. | keep |
| 14b/raw/direct-full | reassess | 실패: enum 처리 누락은 짚지만 실패를 헤더가 제대로 파싱되지 않는 문제로 요약한다. 미초기화 헤더를 파싱하거나 unpack 실패를 parse 실패로 오보한다는 실제 동작을 설명하지 않는다. 부분 성공이다. | reassess |
| 14b/raw/module | reassess | 실패: 선택한 이전 문단은 enum 도입 자체가 아니라 선행 반환값 변경이다. enum 처리 오류의 연결 근거가 빠진다. | keep |
| 3b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | invalid_output |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 14b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 14b/hidden/module | reassess | 실패: 선택한 과거 구절은 앞선 -1/0 반환 정리이고 이번 enum 반환 변경이 아니다. 새 오류 문구만으로 올바른 과거 근거가 되지 않는다. | reassess |
| 14b/hidden/direct-oracle | reassess | 실패: 대상 또는 인용 불일치 | reassess |

### 3b/hidden/direct-full

The incoming report reveals a regression where `unpack_loose_header()` now incorrectly claims that it cannot parse the header, whereas before it could still unpack it but failed to initialize the header structure properly. This contradicts the earlier decision to return specific error codes (`ULHR_TOO_LONG`) for header length issues, indicating that the current implementation might be failing to handle the header initialization correctly.

previous: [P0:0](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
object-file.c: return ULHR_TOO_LONG on "header too long"
```

previous: [P0:1](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
Split up the return code for "header too long" from the generic
negative return value unpack_loose_header() returns, and report via
error() if we exceed MAX_HEADER_LEN.
```

previous: [P0:2](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
As a test added earlier in this series in t1006-cat-file.sh shows
we'll correctly emit zlib errors from zlib.c already in this case, so
we have no need to carry those return codes further down the
stack. Let's instead just return ULHR_TOO_LONG saying we ran into the
MAX_HEADER_LEN limit, or other negative values for "unable to unpack
<OID> header".
```

incoming: [N:0](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
object-file: fix a unpack_loose_header() regression in [ref]
```

incoming: [N:1](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
Fix a regression in my [ref] ([referenced subject], 2021-10-01) revealed both by running
the test suite with --valgrind, and with the amended "git fsck" test.
```

incoming: [N:2](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:
```

incoming: [N:3](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
	-error: unable to unpack header of ./objects/e6/[ref]
	+error: unable to parse header of ./objects/e6/[ref]
```

incoming: [N:4](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
I.e. we'd proceed to call parse_loose_header() on the uninitialized
"hdr" value, and it would have been very unlikely for that
uninitialized memory to be a valid git object.
```

incoming: [N:5](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
The other callers of unpack_loose_header() were already checking the
enum values exhaustively. See [ref] and
[ref] ([referenced subject],
2021-10-01).
```

### 3b/hidden/direct-oracle

The new evidence indicates a regression where the error message changed from 'unable to unpack header' to 'unable to parse header', suggesting that the change in P1 allowed the uninitialized 'hdr' value to be misinterpreted as a valid git object, leading to the reported issue.

previous: [P0:1](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
Split up the return code for "header too long" from the generic
negative return value unpack_loose_header() returns, and report via
error() if we exceed MAX_HEADER_LEN.
```

previous: [P0:2](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
As a test added earlier in this series in t1006-cat-file.sh shows
we'll correctly emit zlib errors from zlib.c already in this case, so
we have no need to carry those return codes further down the
stack. Let's instead just return ULHR_TOO_LONG saying we ran into the
MAX_HEADER_LEN limit, or other negative values for "unable to unpack
<OID> header".
```

incoming: [N:1](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
Fix a regression in my [ref] ([referenced subject], 2021-10-01) revealed both by running
the test suite with --valgrind, and with the amended "git fsck" test.
```

incoming: [N:2](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:
```

incoming: [N:3](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
	-error: unable to unpack header of ./objects/e6/[ref]
	+error: unable to parse header of ./objects/e6/[ref]
```

incoming: [N:4](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
I.e. we'd proceed to call parse_loose_header() on the uninitialized
"hdr" value, and it would have been very unlikely for that
uninitialized memory to be a valid git object.
```

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The incoming report reveals a regression where the function now incorrectly claims it cannot parse the header, whereas before it would have reported a 'header too long' error. This change affects the handling of uninitialized memory in parse_loose_header(), leading to potential issues.

previous: [P0:0](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
object-file.c: return ULHR_TOO_LONG on "header too long"
```

previous: [P0:1](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
Split up the return code for "header too long" from the generic
negative return value unpack_loose_header() returns, and report via
error() if we exceed MAX_HEADER_LEN.
```

previous: [P0:2](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
As a test added earlier in this series in t1006-cat-file.sh shows
we'll correctly emit zlib errors from zlib.c already in this case, so
we have no need to carry those return codes further down the
stack. Let's instead just return ULHR_TOO_LONG saying we ran into the
MAX_HEADER_LEN limit, or other negative values for "unable to unpack
<OID> header".
```

incoming: [N:0](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
object-file: fix a unpack_loose_header() regression in 3b6a8db3b03
```

incoming: [N:1](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
Fix a regression in my 3b6a8db3b03 (object-file.c: use "enum" return
type for unpack_loose_header(), 2021-10-01) revealed both by running
the test suite with --valgrind, and with the amended "git fsck" test.
```

incoming: [N:2](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:
```

incoming: [N:3](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
	-error: unable to unpack header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
	+error: unable to parse header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
```

incoming: [N:4](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
I.e. we'd proceed to call parse_loose_header() on the uninitialized
"hdr" value, and it would have been very unlikely for that
uninitialized memory to be a valid git object.
```

incoming: [N:5](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
The other callers of unpack_loose_header() were already checking the
enum values exhaustively. See 3b6a8db3b03 and
5848fb11acd (object-file.c: return ULHR_TOO_LONG on "header too long",
2021-10-01).
```

### 3b/raw/module

Reconsider the earlier decision “In a preceding commit we changed and documented unpack_loose_header()
from its previous behavior of returning any negative value or zero, to
only -1 or 0.”. The new report gives the following behavior and its conditions. “In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:

	-error: unable to unpack header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
	+error: unable to parse header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391”

previous: [원문 구간](https://github.com/git/git/commit/3b6a8db3b03adb118bfafb90bbc710068dbd6d14)

```text
In a preceding commit we changed and documented unpack_loose_header()
from its previous behavior of returning any negative value or zero, to
only -1 or 0.
```

incoming: [원문 구간](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:

	-error: unable to unpack header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
	+error: unable to parse header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
```

### 14b/hidden/direct-full

The earlier decision in P0 introduced a specific error message for 'header too long' scenarios, but it inadvertently led to a regression where the system incorrectly claims it cannot parse the header instead of unpacking it. This failure is directly tied to the changes made in P0.

previous: [P0:0](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
object-file.c: return ULHR_TOO_LONG on "header too long"
```

previous: [P0:1](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
Split up the return code for "header too long" from the generic
negative return value unpack_loose_header() returns, and report via
error() if we exceed MAX_HEADER_LEN.
```

previous: [P0:2](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
As a test added earlier in this series in t1006-cat-file.sh shows
we'll correctly emit zlib errors from zlib.c already in this case, so
we have no need to carry those return codes further down the
stack. Let's instead just return ULHR_TOO_LONG saying we ran into the
MAX_HEADER_LEN limit, or other negative values for "unable to unpack
<OID> header".
```

incoming: [N:0](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
object-file: fix a unpack_loose_header() regression in [ref]
```

incoming: [N:1](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
Fix a regression in my [ref] ([referenced subject], 2021-10-01) revealed both by running
the test suite with --valgrind, and with the amended "git fsck" test.
```

incoming: [N:3](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
	-error: unable to unpack header of ./objects/e6/[ref]
	+error: unable to parse header of ./objects/e6/[ref]
```

incoming: [N:4](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
I.e. we'd proceed to call parse_loose_header() on the uninitialized
"hdr" value, and it would have been very unlikely for that
uninitialized memory to be a valid git object.
```

### 14b/hidden/direct-oracle

The new evidence indicates a regression introduced by P0 where the error message incorrectly states 'unable to unpack header' instead of 'unable to parse header'. This suggests that the condition under which the error is reported has led to an incorrect handling of the header parsing process.

previous: [P0:1](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
Split up the return code for "header too long" from the generic
negative return value unpack_loose_header() returns, and report via
error() if we exceed MAX_HEADER_LEN.
```

previous: [P0:2](https://github.com/git/git/commit/5848fb11acd0b6aad6ba9e3e71bd91485e0d4c71)

```text
As a test added earlier in this series in t1006-cat-file.sh shows
we'll correctly emit zlib errors from zlib.c already in this case, so
we have no need to carry those return codes further down the
stack. Let's instead just return ULHR_TOO_LONG saying we ran into the
MAX_HEADER_LEN limit, or other negative values for "unable to unpack
<OID> header".
```

incoming: [N:1](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
Fix a regression in my [ref] ([referenced subject], 2021-10-01) revealed both by running
the test suite with --valgrind, and with the amended "git fsck" test.
```

incoming: [N:2](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:
```

incoming: [N:3](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
	-error: unable to unpack header of ./objects/e6/[ref]
	+error: unable to parse header of ./objects/e6/[ref]
```

incoming: [N:4](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
I.e. we'd proceed to call parse_loose_header() on the uninitialized
"hdr" value, and it would have been very unlikely for that
uninitialized memory to be a valid git object.
```

### 14b/hidden/module

Reconsider the earlier decision “In a preceding commit we changed and documented unpack_loose_header()
from its previous behavior of returning any negative value or zero, to
only -1 or 0.”. The new report gives the following behavior and its conditions. “In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:

	-error: unable to unpack header of ./objects/e6/[ref]
	+error: unable to parse header of ./objects/e6/[ref]”

previous: [원문 구간](https://github.com/git/git/commit/3b6a8db3b03adb118bfafb90bbc710068dbd6d14)

```text
In a preceding commit we changed and documented unpack_loose_header()
from its previous behavior of returning any negative value or zero, to
only -1 or 0.
```

incoming: [원문 구간](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:

	-error: unable to unpack header of ./objects/e6/[ref]
	+error: unable to parse header of ./objects/e6/[ref]
```

### 14b/raw/direct-full

The change introduced in P1 altered the return type of unpack_loose_header() to an enum, but did not ensure all callers handled the new enum values correctly, leading to a regression where the header could not be parsed properly.

previous: [P1:0](https://github.com/git/git/commit/3b6a8db3b03adb118bfafb90bbc710068dbd6d14)

```text
object-file.c: use "enum" return type for unpack_loose_header()
```

previous: [P1:1](https://github.com/git/git/commit/3b6a8db3b03adb118bfafb90bbc710068dbd6d14)

```text
In a preceding commit we changed and documented unpack_loose_header()
from its previous behavior of returning any negative value or zero, to
only -1 or 0.
```

previous: [P1:2](https://github.com/git/git/commit/3b6a8db3b03adb118bfafb90bbc710068dbd6d14)

```text
Let's add an "enum unpack_loose_header_result" type and use it for
these return values, and have the compiler assert that we're
exhaustively covering all of them.
```

incoming: [N:0](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
object-file: fix a unpack_loose_header() regression in 3b6a8db3b03
```

incoming: [N:1](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
Fix a regression in my 3b6a8db3b03 (object-file.c: use "enum" return
type for unpack_loose_header(), 2021-10-01) revealed both by running
the test suite with --valgrind, and with the amended "git fsck" test.
```

incoming: [N:2](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:
```

incoming: [N:3](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
	-error: unable to unpack header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
	+error: unable to parse header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
```

incoming: [N:4](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
I.e. we'd proceed to call parse_loose_header() on the uninitialized
"hdr" value, and it would have been very unlikely for that
uninitialized memory to be a valid git object.
```

incoming: [N:5](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
The other callers of unpack_loose_header() were already checking the
enum values exhaustively. See 3b6a8db3b03 and
5848fb11acd (object-file.c: return ULHR_TOO_LONG on "header too long",
2021-10-01).
```

### 14b/raw/module

Reconsider the earlier decision “In a preceding commit we changed and documented unpack_loose_header()
from its previous behavior of returning any negative value or zero, to
only -1 or 0.”. The new report gives the following behavior and its conditions. “In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:

	-error: unable to unpack header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
	+error: unable to parse header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391”

previous: [원문 구간](https://github.com/git/git/commit/3b6a8db3b03adb118bfafb90bbc710068dbd6d14)

```text
In a preceding commit we changed and documented unpack_loose_header()
from its previous behavior of returning any negative value or zero, to
only -1 or 0.
```

incoming: [원문 구간](https://github.com/git/git/commit/4627c67fa68d5669be511962a6437a11c0db3c99)

```text
In practice this regression in v2.34.0 caused us to claim that we
couldn't parse the header, as opposed to not being able to unpack
it. Before the change in the C code the test_cmp added here would emit:

	-error: unable to unpack header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
	+error: unable to parse header of ./objects/e6/9de29bb2d1d6434b8b29ae775ad8c2e48c5391
```
## help-spacing

[새 보고](https://github.com/git/git/commit/93de1b6999898079f521afd73d6a4ae9d5f9aaea) · [실제 이전 결정](https://github.com/git/git/commit/1b81d8cb19d8da6d865b7fca5a095dd5fec8d209) · [유사 결정](https://github.com/git/git/commit/968b1fe263f9dfec65be4598e4f0dd76f1692551)

Moving guide output to section-printing code adds an unintended leading newline for git help --guides or other single-section output. Describe the newline and single-section condition; not missing or duplicated guide text.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | keep | 실패: 보류 | keep |
| 3b/raw/module | keep | 실패: 보류 | keep |
| 14b/raw/direct-full | reassess | 성공: 단일 섹션인 git help --guides 출력 앞에 의도하지 않은 개행이 붙는 동작과 이전 변경을 정확히 연결한다. | keep |
| 14b/raw/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-full | keep | 실패: 보류 | keep |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | keep | 실패: 보류 | keep |
| 14b/hidden/direct-full | keep | 실패: 보류 | keep |
| 14b/hidden/module | keep | 실패: 보류 | keep |
| 14b/hidden/direct-oracle | keep | 실패: 보류 | keep |

### 3b/hidden/direct-full

The incoming report proposes a change to the formatting of the help output, specifically removing an extra newline character before single-section outputs. This change does not directly relate to the earlier decisions regarding the phrasing of warning messages for invalid commands, which were made in P0. The issue described in N pertains to a different aspect of the help command's output formatting and does not undermine or change the conditions on which the earlier decisions depended.

### 3b/hidden/direct-oracle

The incoming report mentions a formatting regression in the help command, specifically about inserting an extra newline before the only section being printed. This issue is related to the change made in P0:8 and P0:10, where the continuation messages were cleaned up and changed to use full-sentence strings. The new evidence suggests that the extra newline was unintentional and resulted from a change in how the help command's output was handled, which aligns with the changes in P0. However, the specific issue described in the incoming report (extra newline) is not directly addressed by the changes in P0, as those changes focused on the wording of the warning messages rather than the formatting of the output itself.

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The incoming report proposes a change to the formatting of the help output, specifically removing an extra newline character before single-section outputs. This change does not directly relate to the earlier decisions regarding the phrasing of warning messages for invalid commands, which were made in P0. The new evidence does not undermine or change the conditions on which P0's decision depended.

### 3b/raw/module

no supported observation with its condition in the report window

### 14b/hidden/direct-full

The incoming report does not warrant reconsideration of either provided earlier decision. It addresses a different issue related to the formatting of 'git help --guides' output, which is unrelated to the auto-correction feature discussed in P0 or the command list management discussed in P1.

### 14b/hidden/direct-oracle

The incoming report does not provide evidence that warrants reconsideration of either P0 or P1. The report focuses on fixing a formatting issue in the output of 'git help --guides' and does not relate to the decisions made in P0 or P1.

### 14b/hidden/module

the exact passages did not reproduce the document judgment

### 14b/raw/direct-full

The change introduced in P1 led to a formatting regression where an extra newline was inserted before the output of single-section commands like 'git help --guides'. This issue was identified and corrected in the incoming report.

previous: [P1:0](https://github.com/git/git/commit/1b81d8cb19d8da6d865b7fca5a095dd5fec8d209)

```text
help: use command-list.txt for the source of guides
```

previous: [P1:1](https://github.com/git/git/commit/1b81d8cb19d8da6d865b7fca5a095dd5fec8d209)

```text
The help command currently hard codes the list of guides and their
summary in C. Let's move this list to command-list.txt. This lets us
extract summary lines from Documentation/git*.txt. This also
potentially lets us list guides in git.txt, but I'll leave that for
now.
```

incoming: [N:0](https://github.com/git/git/commit/93de1b6999898079f521afd73d6a4ae9d5f9aaea)

```text
help: don't print "\n" before single-section output
```

incoming: [N:1](https://github.com/git/git/commit/93de1b6999898079f521afd73d6a4ae9d5f9aaea)

```text
Fix a formatting regression in 1b81d8cb19d (help: use command-list.txt
for the source of guides, 2018-05-20). Adjust the output of "git help
--guides" and any other future single-section commands so that a
newline isn't inserted before the only section being printed.
```

incoming: [N:7](https://github.com/git/git/commit/93de1b6999898079f521afd73d6a4ae9d5f9aaea)

```text
That we started printing an extra "\n" in 1b81d8cb19d wasn't intended,
but an emergent effect of moving all of the printing of "git help"
output to code that was ready to handle printing N sections.
```

incoming: [N:8](https://github.com/git/git/commit/93de1b6999898079f521afd73d6a4ae9d5f9aaea)

```text
With 1b81d8cb19d we started using the "print_cmd_by_category()"
function added earlier in the same series, or in cfb22a02ab5 (help:
use command-list.h for common command list, 2018-05-10).
```

### 14b/raw/module

no supported observation with its condition in the report window
## hook

[새 보고](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20) · [실제 이전 결정](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede) · [유사 결정](https://github.com/git/git/commit/f443246b9f29b815f0b98a07bb2d425628ae6522)

The invoked_hook flag/output is not forwarded from run_commit_hook to run_hooks_opt; later code therefore cannot reliably tell if the hook ran.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/raw/module | reassess | 실패: 이전 근거는 정상인 push_to_checkout 경로이고 새 근거에는 run_commit_hook에서 run_hooks_opt로의 누락이 없다. | keep |
| 14b/raw/direct-full | reassess | 성공: invoked_hook을 run_hooks_opt로 전달하지 않은 변경과 미초기화 값에 따른 분기를 정확히 설명하며 호출 경로도 인용으로 확인된다. | keep |
| 14b/raw/module | reassess | 실패: 과거의 가독성 설명과 새 미초기화 분기 현상만 남겨 invoked_hook을 run_commit_hook에서 run_hooks_opt로 전달하지 않은 핵심 경로를 설명·인용하지 못한다. | keep |
| 3b/hidden/direct-full | reassess | 실패: 정상 전달한 push_to_checkout를 회귀 발생 경로로 잘못 지목한다. | reassess |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | reassess | 실패: 전달 누락은 맞지만 기존 TOCTOU 경합이 다시 발생한다는 원문에 없는 결과를 덧붙인다. | reassess |
| 14b/hidden/direct-full | reassess | 성공: TOCTOU 수정의 invoked_hook가 run_hooks_opt에 전달되지 않아 후속 동작이 불명확한 회귀를 정확히 설명한다. | keep |
| 14b/hidden/module | reassess | 실패: 과거 근거가 TOCTOU 제목뿐이고 새 근거는 Valgrind 추적이다. 누락된 invoked_hook 전달 경로와 이전 결정의 구체적 변경을 복구하지 못한다. | keep |
| 14b/hidden/direct-oracle | reassess | 성공: invoked_hook 전달 누락으로 후속 분기 실행 여부가 불명확해진다는 동작을 잘못된 경로를 덧붙이지 않고 설명한다. | keep |

### 3b/hidden/direct-full

The new evidence reveals a regression in the 'invoked hook' mechanism introduced in P1, specifically in the 'push-to-checkout' hook. This regression causes undefined behavior regarding whether the hook was executed based on the presence of the hook, leading to potential issues such as uninitialized values detected by Valgrind. The original decision in P0 aimed to improve readability and clarity of the code, but the new evidence shows that this change has unintended consequences.

previous: [P0:0](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
hooks: fix an obscure TOCTOU "did we just run a hook?" race
```

previous: [P0:1](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
Fix a Time-of-check to time-of-use (TOCTOU) race in code added in
680ee550d72 (commit: skip discarding the index if there is no
pre-commit hook, 2017-08-14).
```

previous: [P0:2](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This obscure race condition can occur if we e.g. ran the "pre-commit"
hook and it modified the index, but hook_exists() returns false later
on (e.g., because the hook itself went away, the directory became
unreadable, etc.). Then we won't call discard_cache() when we should
have.
```

previous: [P0:3](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
The race condition itself probably doesn't matter, and users would
have been unlikely to run into it in practice. This problem has been
noted on-list when 680ee550d72 was discussed[1], but had not been
fixed.
```

previous: [P0:4](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This change is mainly intended to improve the readability of the code
involved, and to make reasoning about it more straightforward. It
wasn't as obvious what we were trying to do here, but by having an
"invoked_hook" it's clearer that e.g. our discard_cache() is happening
because of the earlier hook execution.
```

previous: [P0:5](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
Let's also change this for the push-to-checkout hook. Now instead of
checking if the hook exists and either doing a push to checkout or a
push to deploy we'll always attempt a push to checkout. If the hook
doesn't exist we'll fall back on push to deploy. The same behavior as
before, without the TOCTOU race. See 0855331941b (receive-pack:
support push-to-checkout hook, 2014-12-01) for the introduction of the
previous behavior.
```

previous: [P0:6](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This leaves uses of hook_exists() in two places that matter. The
"reference-transaction" check in refs.c, see 67541597670 (refs:
implement reference transaction hook, 2020-06-19), and the
"prepare-commit-msg" hook, see 66618a50f9c (sequencer: run
'prepare-commit-msg' hook, 2018-01-24).
```

previous: [P0:7](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
In both of those cases we're saving ourselves CPU time by not
preparing data for the hook that we'll then do nothing with if we
don't have the hook. So using this "invoked_hook" pattern doesn't make
sense in those cases.
```

previous: [P0:8](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
The "reference-transaction" and "prepare-commit-msg" hook also aren't
racy. In those cases we'll skip the hook runs if we race with a new
hook being added, whereas in the TOCTOU races being fixed here we were
incorrectly skipping the required post-hook logic.
```

previous: [P0:9](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
1. https://lore.kernel.org/git/20170810191613.kpmhzg4seyxy3cpq@sigill.intra.peff.net/
```

incoming: [N:0](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
hooks: fix "invoked hook" regression in [ref]
```

incoming: [N:1](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Fix a regression in [ref] ([referenced subject], 2022-03-07): The "invoked_hook" variable
passed to run_commit_hook() wasn't passed forward to run_hooks_opt(),
as push_to_checkout() in that commit correctly did.
```

incoming: [N:2](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".
```

incoming: [N:3](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
This bug was revealed by running e.g. "t5537-fetch-shallow.sh" with
the --valgrind option. Unfortunately running the whole test suite with
--valgrind is really slow, so we didn't have a CI job that spotted
this. The --valgrind output was:
```

incoming: [N:4](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
    ==31275== Conditional jump or move depends on uninitialised value(s)
    ==31275==    at 0x43C63F: prepare_to_commit (commit.c:1058)
    ==31275==    by 0x4396A5: cmd_commit (commit.c:1722)
    ==31275==    by 0x407C8A: run_builtin (git.c:465)
    ==31275==    by 0x406741: handle_builtin (git.c:718)
    ==31275==    by 0x407665: run_argv (git.c:785)
    ==31275==    by 0x406500: cmd_main (git.c:916)
    ==31275==    by 0x510839: main (common-main.c:56)
    ==31275==  Uninitialised value was created by a stack allocation
    ==31275==    at 0x43B344: prepare_to_commit (commit.c:719)
```

### 3b/hidden/direct-oracle

The new evidence indicates a regression where the 'invoked_hook' variable was not passed forward to run_hooks_opt(), leading to undefined behavior regarding whether the code was contingent on running the hook. This could result in the race condition described in P0:2, where the index might be modified by a pre-commit hook without calling discard_cache().

previous: [P0:2](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This obscure race condition can occur if we e.g. ran the "pre-commit"
hook and it modified the index, but hook_exists() returns false later
on (e.g., because the hook itself went away, the directory became
unreadable, etc.). Then we won't call discard_cache() when we should
have.
```

previous: [P0:4](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This change is mainly intended to improve the readability of the code
involved, and to make reasoning about it more straightforward. It
wasn't as obvious what we were trying to do here, but by having an
"invoked_hook" it's clearer that e.g. our discard_cache() is happening
because of the earlier hook execution.
```

incoming: [N:1](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Fix a regression in [ref] ([referenced subject], 2022-03-07): The "invoked_hook" variable
passed to run_commit_hook() wasn't passed forward to run_hooks_opt(),
as push_to_checkout() in that commit correctly did.
```

incoming: [N:2](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".
```

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The new evidence reveals a regression in the 'hooks: fix an obscure TOCTOU "did we just run a hook?" race' commit (P1). Specifically, it shows that the 'invoked_hook' variable passed to `run_commit_hook()` was not passed forward to `run_hooks_opt()`, leading to undefined behavior. This regression was detected by running the test suite with valgrind, indicating a potential memory safety issue.

previous: [P0:0](https://github.com/git/git/commit/f443246b9f29b815f0b98a07bb2d425628ae6522)

```text
commit: convert {pre-commit,prepare-commit-msg} hook to hook.h
```

previous: [P0:1](https://github.com/git/git/commit/f443246b9f29b815f0b98a07bb2d425628ae6522)

```text
Move these hooks hook away from run-command.h to and over to the new
hook.h library.
```

incoming: [N:0](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
hooks: fix "invoked hook" regression in a8cc5943338
```

incoming: [N:1](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Fix a regression in a8cc5943338 (hooks: fix an obscure TOCTOU "did we
just run a hook?" race, 2022-03-07): The "invoked_hook" variable
passed to run_commit_hook() wasn't passed forward to run_hooks_opt(),
as push_to_checkout() in that commit correctly did.
```

incoming: [N:2](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".
```

incoming: [N:3](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
This bug was revealed by running e.g. "t5537-fetch-shallow.sh" with
the --valgrind option. Unfortunately running the whole test suite with
--valgrind is really slow, so we didn't have a CI job that spotted
this. The --valgrind output was:
```

incoming: [N:4](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
    ==31275== Conditional jump or move depends on uninitialised value(s)
    ==31275==    at 0x43C63F: prepare_to_commit (commit.c:1058)
    ==31275==    by 0x4396A5: cmd_commit (commit.c:1722)
    ==31275==    by 0x407C8A: run_builtin (git.c:465)
    ==31275==    by 0x406741: handle_builtin (git.c:718)
    ==31275==    by 0x407665: run_argv (git.c:785)
    ==31275==    by 0x406500: cmd_main (git.c:916)
    ==31275==    by 0x510839: main (common-main.c:56)
    ==31275==  Uninitialised value was created by a stack allocation
    ==31275==    at 0x43B344: prepare_to_commit (commit.c:719)
```

### 3b/raw/module

Reconsider the earlier decision “Let's also change this for the push-to-checkout hook. Now instead of
checking if the hook exists and either doing a push to checkout or a
push to deploy we'll always attempt a push to checkout. If the hook
doesn't exist we'll fall back on push to deploy. The same behavior as
before, without the TOCTOU race. See 0855331941b (receive-pack:
support push-to-checkout hook, 2014-12-01) for the introduction of the
previous behavior.”. The new report gives the following behavior and its conditions. “Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".

This bug was revealed by running e.g. "t5537-fetch-shallow.sh" with
the --valgrind option. Unfortunately running the whole test suite with
--valgrind is really slow, so we didn't have a CI job that spotted
this. The --valgrind output was:”

previous: [원문 구간](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
Let's also change this for the push-to-checkout hook. Now instead of
checking if the hook exists and either doing a push to checkout or a
push to deploy we'll always attempt a push to checkout. If the hook
doesn't exist we'll fall back on push to deploy. The same behavior as
before, without the TOCTOU race. See 0855331941b (receive-pack:
support push-to-checkout hook, 2014-12-01) for the introduction of the
previous behavior.
```

incoming: [원문 구간](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".

This bug was revealed by running e.g. "t5537-fetch-shallow.sh" with
the --valgrind option. Unfortunately running the whole test suite with
--valgrind is really slow, so we didn't have a CI job that spotted
this. The --valgrind output was:
```

### 14b/hidden/direct-full

The regression introduced in [ref] ([referenced subject], 2022-03-07) affects the 'invoked_hook' variable handling, which was part of the changes made in P0 to address TOCTOU race conditions. The failure to pass 'invoked_hook' forward to run_hooks_opt() leads to undefined behavior, indicating that the fix in P0 may have inadvertently introduced a new issue.

previous: [P0:0](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
hooks: fix an obscure TOCTOU "did we just run a hook?" race
```

previous: [P0:1](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
Fix a Time-of-check to time-of-use (TOCTOU) race in code added in
680ee550d72 (commit: skip discarding the index if there is no
pre-commit hook, 2017-08-14).
```

previous: [P0:2](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This obscure race condition can occur if we e.g. ran the "pre-commit"
hook and it modified the index, but hook_exists() returns false later
on (e.g., because the hook itself went away, the directory became
unreadable, etc.). Then we won't call discard_cache() when we should
have.
```

previous: [P0:5](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
Let's also change this for the push-to-checkout hook. Now instead of
checking if the hook exists and either doing a push to checkout or a
push to deploy we'll always attempt a push to checkout. If the hook
doesn't exist we'll fall back on push to deploy. The same behavior as
before, without the TOCTOU race. See 0855331941b (receive-pack:
support push-to-checkout hook, 2014-12-01) for the introduction of the
previous behavior.
```

incoming: [N:0](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
hooks: fix "invoked hook" regression in [ref]
```

incoming: [N:1](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Fix a regression in [ref] ([referenced subject], 2022-03-07): The "invoked_hook" variable
passed to run_commit_hook() wasn't passed forward to run_hooks_opt(),
as push_to_checkout() in that commit correctly did.
```

incoming: [N:2](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".
```

### 14b/hidden/direct-oracle

The regression introduced by the change in P0 causes the 'invoked_hook' variable to not be properly passed forward, leading to undefined behavior whether the code contingent on running the hook executes or not. This undermines the clarity and reliability improvements aimed for in P0.

previous: [P0:2](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This obscure race condition can occur if we e.g. ran the "pre-commit"
hook and it modified the index, but hook_exists() returns false later
on (e.g., because the hook itself went away, the directory became
unreadable, etc.). Then we won't call discard_cache() when we should
have.
```

previous: [P0:4](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This change is mainly intended to improve the readability of the code
involved, and to make reasoning about it more straightforward. It
wasn't as obvious what we were trying to do here, but by having an
"invoked_hook" it's clearer that e.g. our discard_cache() is happening
because of the earlier hook execution.
```

incoming: [N:1](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Fix a regression in [ref] ([referenced subject], 2022-03-07): The "invoked_hook" variable
passed to run_commit_hook() wasn't passed forward to run_hooks_opt(),
as push_to_checkout() in that commit correctly did.
```

incoming: [N:2](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".
```

### 14b/hidden/module

Reconsider the earlier decision “hooks: fix an obscure TOCTOU "did we just run a hook?" race”. The new report gives the following behavior and its conditions. “This bug was revealed by running e.g. "t5537-fetch-shallow.sh" with
the --valgrind option. Unfortunately running the whole test suite with
--valgrind is really slow, so we didn't have a CI job that spotted
this. The --valgrind output was:

    ==31275== Conditional jump or move depends on uninitialised value(s)
    ==31275==    at 0x43C63F: prepare_to_commit (commit.c:1058)
    ==31275==    by 0x4396A5: cmd_commit (commit.c:1722)
    ==31275==    by 0x407C8A: run_builtin (git.c:465)
    ==31275==    by 0x406741: handle_builtin (git.c:718)
    ==31275==    by 0x407665: run_argv (git.c:785)
    ==31275==    by 0x406500: cmd_main (git.c:916)
    ==31275==    by 0x510839: main (common-main.c:56)
    ==31275==  Uninitialised value was created by a stack allocation
    ==31275==    at 0x43B344: prepare_to_commit (commit.c:719)”

previous: [원문 구간](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
hooks: fix an obscure TOCTOU "did we just run a hook?" race
```

incoming: [원문 구간](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
This bug was revealed by running e.g. "t5537-fetch-shallow.sh" with
the --valgrind option. Unfortunately running the whole test suite with
--valgrind is really slow, so we didn't have a CI job that spotted
this. The --valgrind output was:

    ==31275== Conditional jump or move depends on uninitialised value(s)
    ==31275==    at 0x43C63F: prepare_to_commit (commit.c:1058)
    ==31275==    by 0x4396A5: cmd_commit (commit.c:1722)
    ==31275==    by 0x407C8A: run_builtin (git.c:465)
    ==31275==    by 0x406741: handle_builtin (git.c:718)
    ==31275==    by 0x407665: run_argv (git.c:785)
    ==31275==    by 0x406500: cmd_main (git.c:916)
    ==31275==    by 0x510839: main (common-main.c:56)
    ==31275==  Uninitialised value was created by a stack allocation
    ==31275==    at 0x43B344: prepare_to_commit (commit.c:719)
```

### 14b/raw/direct-full

The new evidence indicates a regression introduced by P1 where the 'invoked_hook' variable was not properly passed forward to run_hooks_opt(). This oversight led to undefined behavior, causing conditional jumps or moves to depend on uninitialized values, as revealed by valgrind testing.

previous: [P1:0](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
hooks: fix an obscure TOCTOU "did we just run a hook?" race
```

previous: [P1:1](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
Fix a Time-of-check to time-of-use (TOCTOU) race in code added in
680ee550d72 (commit: skip discarding the index if there is no
pre-commit hook, 2017-08-14).
```

previous: [P1:2](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This obscure race condition can occur if we e.g. ran the "pre-commit"
hook and it modified the index, but hook_exists() returns false later
on (e.g., because the hook itself went away, the directory became
unreadable, etc.). Then we won't call discard_cache() when we should
have.
```

previous: [P1:5](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
Let's also change this for the push-to-checkout hook. Now instead of
checking if the hook exists and either doing a push to checkout or a
push to deploy we'll always attempt a push to checkout. If the hook
doesn't exist we'll fall back on push to deploy. The same behavior as
before, without the TOCTOU race. See 0855331941b (receive-pack:
support push-to-checkout hook, 2014-12-01) for the introduction of the
previous behavior.
```

incoming: [N:0](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
hooks: fix "invoked hook" regression in a8cc5943338
```

incoming: [N:1](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Fix a regression in a8cc5943338 (hooks: fix an obscure TOCTOU "did we
just run a hook?" race, 2022-03-07): The "invoked_hook" variable
passed to run_commit_hook() wasn't passed forward to run_hooks_opt(),
as push_to_checkout() in that commit correctly did.
```

incoming: [N:2](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".
```

incoming: [N:3](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
This bug was revealed by running e.g. "t5537-fetch-shallow.sh" with
the --valgrind option. Unfortunately running the whole test suite with
--valgrind is really slow, so we didn't have a CI job that spotted
this. The --valgrind output was:
```

incoming: [N:4](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
    ==31275== Conditional jump or move depends on uninitialised value(s)
    ==31275==    at 0x43C63F: prepare_to_commit (commit.c:1058)
    ==31275==    by 0x4396A5: cmd_commit (commit.c:1722)
    ==31275==    by 0x407C8A: run_builtin (git.c:465)
    ==31275==    by 0x406741: handle_builtin (git.c:718)
    ==31275==    by 0x407665: run_argv (git.c:785)
    ==31275==    by 0x406500: cmd_main (git.c:916)
    ==31275==    by 0x510839: main (common-main.c:56)
    ==31275==  Uninitialised value was created by a stack allocation
    ==31275==    at 0x43B344: prepare_to_commit (commit.c:719)
```

### 14b/raw/module

Reconsider the earlier decision “This change is mainly intended to improve the readability of the code
involved, and to make reasoning about it more straightforward. It
wasn't as obvious what we were trying to do here, but by having an
"invoked_hook" it's clearer that e.g. our discard_cache() is happening
because of the earlier hook execution.”. The new report gives the following behavior and its conditions. “Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".

This bug was revealed by running e.g. "t5537-fetch-shallow.sh" with
the --valgrind option. Unfortunately running the whole test suite with
--valgrind is really slow, so we didn't have a CI job that spotted
this. The --valgrind output was:”

previous: [원문 구간](https://github.com/git/git/commit/a8cc594333848713b8e772cccf8159196ea85ede)

```text
This change is mainly intended to improve the readability of the code
involved, and to make reasoning about it more straightforward. It
wasn't as obvious what we were trying to do here, but by having an
"invoked_hook" it's clearer that e.g. our discard_cache() is happening
because of the earlier hook execution.
```

incoming: [원문 구간](https://github.com/git/git/commit/4369e3a1a39895ab51c2bef2985255ad05957a20)

```text
Whether we ran the code contingent on having run the hook or not was
thus undefined, but in practice on most (all?) modern platforms we'd
have run it (almost?) all the time, since stack variables will get
initialized to some random value, which most of the time isn't "0".

This bug was revealed by running e.g. "t5537-fetch-shallow.sh" with
the --valgrind option. Unfortunately running the whole test suite with
--valgrind is really slow, so we didn't have a CI job that spotted
this. The --valgrind output was:
```
## http-index

[새 보고](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc) · [실제 이전 결정](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93) · [유사 결정](https://github.com/git/git/commit/7655b4119d49844e6ebc62da571e5f18528dbde8)

A dumb HTTP fetch with a remote v1 pack index fails after collision checks; the local index can conflict with the downloaded one. At minimum connect the failure/condition and prior collision check.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/raw/module | reassess | 실패: v1/v2 충돌 결과는 맞지만 이전 근거가 충돌 검사 도입 결정이 아니라 그 이전의 무검사 동작 설명이다. | keep |
| 14b/raw/direct-full | reassess | 성공: 기존 충돌 검사와 dumb HTTP의 원격 v1 idx/로컬 재생성 idx 충돌로 fetch가 실패하는 조건·동작을 정확히 연결한다. | keep |
| 14b/raw/module | reassess | 실패: v1/v2 충돌 결과는 맞지만 이전 근거가 충돌 검사 도입 결정이 아니라 그 이전의 무검사 동작 설명이다. | keep |
| 3b/hidden/direct-full | keep | 실패: 보류 | reassess |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | keep | 실패: 보류 | reassess |
| 14b/hidden/direct-full | reassess | 성공: 충돌 검사 도입이 dumb HTTP의 다운로드/로컬 인덱스 충돌과 fetch 실패를 만든다고 설명한다. v1/v2 조건은 선택한 관측 문단에 명시되어 있다. | reassess |
| 14b/hidden/module | keep | 실패: 보류 | keep |
| 14b/hidden/direct-oracle | reassess | 실패: 새 충돌 검사 도입 결정이 동일한 디스크 내용만을 가정했다고 설명하여, 도입 전의 가정을 새 결정의 가정으로 뒤집는다. | reassess |

### 3b/hidden/direct-full

The incoming report introduces a new issue with dumb-http fetching where a collision between downloaded pack index files and local files can occur. This is unrelated to the collision check discussed in P0, which pertains to loose objects and pack checksums. The new evidence does not undermine or change the conditions under which the collision check was decided upon.

### 3b/hidden/direct-oracle

The incoming report discusses a regression related to fetching v1 pack idx files over the dumb-http protocol, which is unrelated to the collision check described in the earlier decision (P0). The collision check in P0 is about writing files with the same name, not about fetching different versions of the same index file. Therefore, the new evidence does not undermine or change the condition on which P0 depends.

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The incoming report introduces a new scenario where fetching a v1 pack index file over dumb HTTP causes a collision check failure, leading to a fetch failure. This is triggered by the co-mingling of downloaded idx files in the local objects directory, which can lead to unexpected behavior such as deleting or retaining unnecessary files. The earlier decision to show progress for fetches over dumb HTTP did not anticipate this specific issue.

previous: [P0:0](https://github.com/git/git/commit/7655b4119d49844e6ebc62da571e5f18528dbde8)

```text
remote-curl: show progress for fetches over dumb HTTP
```

previous: [P0:1](https://github.com/git/git/commit/7655b4119d49844e6ebc62da571e5f18528dbde8)

```text
Fetching over dumb HTTP transport doesn't show any progress, even with
the option --progress.  If the connection is slow or there is a lot of
data to get then this can take a long time while the user is left to
wonder if git got stuck.
```

previous: [P0:2](https://github.com/git/git/commit/7655b4119d49844e6ebc62da571e5f18528dbde8)

```text
We don't know the number of objects to fetch at the outset, but we can
count the ones we got.  Show an open-ended progress indicator based on
that number if the user asked for it.
```

incoming: [N:0](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
dumb-http: store downloaded pack idx as tempfile
```

incoming: [N:1](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
This patch fixes a regression in b1b8dfde69 (finalize_object_file():
implement collision check, 2024-09-26) where fetching a v1 pack idx file
over the dumb-http protocol would cause the fetch to fail.
```

incoming: [N:2](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
The core of the issue is that dumb-http stores the idx we fetch from the
remote at the same path that will eventually hold the idx we generate
from "index-pack --stdin". The sequence is something like this:
```

incoming: [N:3](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  0. We realize we need some object X, which we don't have locally, and
     nor does the other side have it as a loose object.
```

incoming: [N:4](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  1. We download the list of remote packs from objects/info/packs.
```

incoming: [N:5](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  2. For each entry in that file, we download each pack index and store
     it locally in .git/objects/pack/pack-$hash.idx (the $hash is not
     something we can verify yet and is given to us by the remote).
```

incoming: [N:6](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  3. We check each pack index we got to see if it has object X. When we
     find a match, we download the matching .pack file from the remote
     to a tempfile. We feed that to "index-pack --stdin", which
     reindexes the pack, rather than trusting that it has what the other
     side claims it does. In most cases, this will end up generating the
     exact same (byte-for-byte) pack index which we'll store at the same
     pack-$hash.idx path, because the index generation and $hash id are
     computed based on what's in the packfile. But:
```

incoming: [N:7](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
       a. The other side might have used other options to generate the
          index. For instance we use index v2 by default, but long ago
          it was v1 (and you can still ask for v1 explicitly).
```

incoming: [N:8](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
       b. The other side might even use a different mechanism to
          determine $hash. E.g., long ago it was based on the sorted
          list of objects in the packfile, but we switched to using the
          pack checksum in 1190a1acf8 (pack-objects: name pack files
          after trailer hash, 2013-12-05).
```

incoming: [N:9](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
The regression we saw in the real world was (3a). A recent client
fetching from a server with a v1 index downloaded that index, then
complained about trying to overwrite it with its own v2 index. This
collision is otherwise harmless; we know we want to replace the remote
version with our local one, but the collision check doesn't realize
that.
```

incoming: [N:10](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
There are a few options to fix it:
```

incoming: [N:11](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - we could teach index-pack a command-line option to ignore only pack
    idx collisions, and use it when the dumb-http code invokes
    index-pack. This would be an awkward thing to expose users to and
    would involve a lot of boilerplate to get the option down to the
    collision code.
```

incoming: [N:12](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - we could delete the remote .idx file right before running
    index-pack. It should be redundant at that point (since we've just
    downloaded the matching pack). But it feels risky to delete
    something from our own .git/objects based on what the other side has
    said. I'm not entirely positive that a malicious server couldn't lie
    about which pack-$hash.idx it has and get us to delete something
    precious.
```

incoming: [N:13](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - we can stop co-mingling the downloaded idx files in our local
    objects directory. This is a slightly bigger change but I think
    fixes the root of the problem more directly.
```

incoming: [N:14](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
This patch implements the third option. The big design questions are:
where do we store the downloaded files, and how do we manage their
lifetimes?
```

incoming: [N:15](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
There are some additional quirks to the dumb-http system we should
consider. Remember that in step 2 we downloaded every pack index, but in
step 3 we may only download some of the matching packs. What happens to
those other idx files now? They sit in the .git/objects/pack directory,
possibly waiting to be used at a later date. That may save bandwidth for
a subsequent fetch, but it also creates a lot of weird corner cases:
```

incoming: [N:16](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - our local object directory now has semi-untrusted .idx files sitting
    around, without their matching .pack
```

incoming: [N:17](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - in case 3b, we noted that we might not generate the same hash as the
    other side. In that case even if we download the matching pack,
    our index-pack invocation will store it in a different
    pack-$hash.idx file. And the unmatched .idx will sit there forever.
```

incoming: [N:18](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - if the server repacks, it may delete the old packs. Now we have
    these orphaned .idx files sitting around locally that will never be
    used (nor deleted).
```

incoming: [N:19](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - if we repack locally we may delete our local version of the server's
    pack index and not realize we have it. So we'll download it again,
    even though we have all of the objects it mentions.
```

incoming: [N:20](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
I think the right solution here is probably some more complex cache
management system: download the remote .idx files to their own storage
directory, mark them as "seen" when we get their matching pack (to avoid
re-downloading even if we repack), and then delete them when the
server's objects/info/refs no longer mentions them.
```

incoming: [N:21](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
But since the dumb http protocol is so ancient and so inferior to the
smart http protocol, I don't think it's worth spending a lot of time
creating such a system. For this patch I'm just downloading the idx
files to .git/objects/tmp_pack_*, and marking them as tempfiles to be
deleted when we exit (and due to the name, any we miss due to a crash,
etc, should eventually be removed by "git gc" runs based on timestamps).
```

incoming: [N:22](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
That is slightly worse for one case: if we download an idx but not the
matching pack, we won't retain that idx for subsequent runs. But the
flip side is that we're making other cases better (we never hold on to
useless idx files forever). I suspect that worse case does not even come
up often, since it implies that the packs are generated to match
distinct parts of history (i.e., in practice even in a repo with many
packs you're going to end up grabbing all of those packs to do a clone).
If somebody really cares about that, I think the right path forward is a
managed cache directory as above, and this patch is providing the first
step in that direction anyway (by moving things out of the objects/pack/
directory).
```

incoming: [N:23](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
There are two test changes. One demonstrates the broken v1 index case
(it double-checks the resulting clone with fsck to be careful, but prior
to this patch it actually fails at the clone step). The other tweaks the
expectation for a test that covers the "slightly worse" case to
accommodate the extra index download.
```

incoming: [N:24](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
The code changes are fairly simple. We stop using finalize_object_file()
to copy the remote's index file into place, and leave it as a tempfile.
We give the tempfile a real ".idx" name, since the packfile code expects
that, and thus we make sure it is out of the usual packs/ directory (so
we'd never mistake it for a real local .idx).
```

incoming: [N:25](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
We also have to change parse_pack_index(), which creates a temporary
packed_git to access our index (we need this because all of the pack idx
code assumes we have that struct). It reads the index data from the
tempfile, but prior to this patch would speculatively write the
finalized name into the packed_git struct using the pack-$hash we expect
to use.
```

incoming: [N:26](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
I was mildly surprised that this worked at all, since we call
verify_pack_index() on the packed_git which mentions the final name
before moving the file into place! But it works because
parse_pack_index() leaves the mmap-ed data in the struct, so the
lazy-open in verify_pack_index() never triggers, and we read from the
tempfile, ignoring the filename in the struct completely. Hacky, but it
works.
```

incoming: [N:27](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
After this patch, parse_pack_index() now uses the index filename we pass
in to derive a matching .pack name. This is OK to change because there
are only two callers, both in the dumb http code (and the other passes
in an existing pack-$hash.idx name, so the derived name is going to be
pack-$hash.pack, which is what we were using anyway).
```

incoming: [N:28](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
I'll follow up with some more cleanups in that area, but this patch is
sufficient to fix the regression.
```

### 3b/raw/module

Reconsider the earlier decision “We've had "FIXME!!! Collision check here ?" in finalize_object_file()
since aac1794132 (Improve sha1 object file writing., 2005-05-03). That
is, when we try to write a file with the same name, we assume the
on-disk contents are the same and blindly throw away the new copy.”. The new report gives the following behavior and its conditions. “b. The other side might even use a different mechanism to
          determine $hash. E.g., long ago it was based on the sorted
          list of objects in the packfile, but we switched to using the
          pack checksum in 1190a1acf8 (pack-objects: name pack files
          after trailer hash, 2013-12-05).

The regression we saw in the real world was (3a). A recent client
fetching from a server with a v1 index downloaded that index, then
complained about trying to overwrite it with its own v2 index. This
collision is otherwise harmless; we know we want to replace the remote
version with our local one, but the collision check doesn't realize
that.”

previous: [원문 구간](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
We've had "FIXME!!! Collision check here ?" in finalize_object_file()
since aac1794132 (Improve sha1 object file writing., 2005-05-03). That
is, when we try to write a file with the same name, we assume the
on-disk contents are the same and blindly throw away the new copy.
```

incoming: [원문 구간](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
b. The other side might even use a different mechanism to
          determine $hash. E.g., long ago it was based on the sorted
          list of objects in the packfile, but we switched to using the
          pack checksum in 1190a1acf8 (pack-objects: name pack files
          after trailer hash, 2013-12-05).

The regression we saw in the real world was (3a). A recent client
fetching from a server with a v1 index downloaded that index, then
complained about trying to overwrite it with its own v2 index. This
collision is otherwise harmless; we know we want to replace the remote
version with our local one, but the collision check doesn't realize
that.
```

### 14b/hidden/direct-full

The collision check introduced in P0 causes issues during the dumb HTTP fetch process, as described in N. Specifically, the downloaded pack index file collides with the locally generated index file, leading to a failure in the fetch operation. This scenario highlights a condition not fully considered in P0, where the hash-based naming assumption does not hold for intermediate files during the fetch process.

previous: [P0:0](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
finalize_object_file(): implement collision check
```

previous: [P0:3](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
So while it's a theoretical concern now, it hasn't been a priority.
However, if we start using weaker hashes for pack checksums and names,
this will become a practical concern. So in preparation, let's actually
implement a byte-for-byte collision check.
```

previous: [P0:11](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
    There is a collision check in index-pack via its `check_collision()`
    function, but there isn't an analogous function in unpack-objects,
    which just feeds the result to write_object_file().
```

previous: [P0:12](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
    So skipping the collision check here does not change for better or
    worse the hardness of loose object writes.
```

incoming: [N:9](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
The regression we saw in the real world was (3a). A recent client
fetching from a server with a v1 index downloaded that index, then
complained about trying to overwrite it with its own v2 index. This
collision is otherwise harmless; we know we want to replace the remote
version with our local one, but the collision check doesn't realize
that.
```

incoming: [N:13](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - we can stop co-mingling the downloaded idx files in our local
    objects directory. This is a slightly bigger change but I think
    fixes the root of the problem more directly.
```

incoming: [N:24](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
The code changes are fairly simple. We stop using finalize_object_file()
to copy the remote's index file into place, and leave it as a tempfile.
We give the tempfile a real ".idx" name, since the packfile code expects
that, and thus we make sure it is out of the usual packs/ directory (so
we'd never mistake it for a real local .idx).
```

incoming: [N:25](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
We also have to change parse_pack_index(), which creates a temporary
packed_git to access our index (we need this because all of the pack idx
code assumes we have that struct). It reads the index data from the
tempfile, but prior to this patch would speculatively write the
finalized name into the packed_git struct using the pack-$hash we expect
to use.
```

### 14b/hidden/direct-oracle

The new evidence indicates a specific scenario where the collision check in finalize_object_file() causes a harmless but disruptive failure during fetching operations involving different versions of index files. This situation was not anticipated in the original decision, which assumed that collisions would always indicate identical on-disk contents.

previous: [P0:1](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
We've had "FIXME!!! Collision check here ?" in finalize_object_file()
since aac1794132 (Improve sha1 object file writing., 2005-05-03). That
is, when we try to write a file with the same name, we assume the
on-disk contents are the same and blindly throw away the new copy.
```

previous: [P0:4](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
The new check will cause the write of new differing content to be a
failure, rather than a silent noop, and we'll retain the temporary file
on disk. If there's no collision present, we'll clean up the temporary
file as usual after either rename()-ing or link()-ing it into place.
```

incoming: [N:1](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
This patch fixes a regression in [ref] ([referenced subject], 2024-09-26) where fetching a v1 pack idx file
over the dumb-http protocol would cause the fetch to fail.
```

incoming: [N:7](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
       a. The other side might have used other options to generate the
          index. For instance we use index v2 by default, but long ago
          it was v1 (and you can still ask for v1 explicitly).
```

incoming: [N:9](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
The regression we saw in the real world was (3a). A recent client
fetching from a server with a v1 index downloaded that index, then
complained about trying to overwrite it with its own v2 index. This
collision is otherwise harmless; we know we want to replace the remote
version with our local one, but the collision check doesn't realize
that.
```

### 14b/hidden/module

no unique decision in the document comparison

### 14b/raw/direct-full

The new evidence shows that the implementation of the collision check in finalize_object_file() introduced a regression in fetching v1 pack idx files over dumb HTTP. Specifically, the downloaded idx file conflicts with the locally generated idx file, causing the fetch to fail due to the collision check. This issue arises because the downloaded idx file is stored at the same path as the final idx file, leading to a false collision detection.

previous: [P1:0](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
finalize_object_file(): implement collision check
```

previous: [P1:1](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
We've had "FIXME!!! Collision check here ?" in finalize_object_file()
since aac1794132 (Improve sha1 object file writing., 2005-05-03). That
is, when we try to write a file with the same name, we assume the
on-disk contents are the same and blindly throw away the new copy.
```

previous: [P1:2](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
One of the reasons we never implemented this is because the files it
moves are all named after the cryptographic hash of their contents
(either loose objects, or packs which have their hash in the name these
days). So we are unlikely to see such a collision by accident. And even
though there are weaknesses in sha1, we assume they are mitigated by our
use of sha1dc.
```

previous: [P1:3](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
So while it's a theoretical concern now, it hasn't been a priority.
However, if we start using weaker hashes for pack checksums and names,
this will become a practical concern. So in preparation, let's actually
implement a byte-for-byte collision check.
```

previous: [P1:4](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
The new check will cause the write of new differing content to be a
failure, rather than a silent noop, and we'll retain the temporary file
on disk. If there's no collision present, we'll clean up the temporary
file as usual after either rename()-ing or link()-ing it into place.
```

previous: [P1:5](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
Note that this may cause some extra computation when the files are in
fact identical, but this should happen rarely.
```

previous: [P1:6](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
Loose objects are exempt from this check, and the collision check may be
skipped by calling the _flags variant of this function with the
FOF_SKIP_COLLISION_CHECK bit set. This is done for a couple of reasons:
```

previous: [P1:7](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
  - We don't treat the hash of the loose object file's contents as a
    checksum, since the same loose object can be stored using different
    bytes on disk (e.g., when adjusting core.compression, using a
    different version of zlib, etc.).
```

previous: [P1:8](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
    This is fundamentally different from cases where
    finalize_object_file() is operating over a file which uses the hash
    value as a checksum of the contents. In other words, a pair of
    identical loose objects can be stored using different bytes on disk,
    and that should not be treated as a collision.
```

previous: [P1:9](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
  - We already use the path of the loose object as its hash value /
    object name, so checking for collisions at the content level doesn't
    add anything.
```

previous: [P1:10](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
    Adding a content-level collision check would have to happen at a
    higher level than in finalize_object_file(), since (avoiding race
    conditions) writing an object loose which already exists in the
    repository will prevent us from even reaching finalize_object_file()
    via the object freshening code.
```

previous: [P1:11](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
    There is a collision check in index-pack via its `check_collision()`
    function, but there isn't an analogous function in unpack-objects,
    which just feeds the result to write_object_file().
```

previous: [P1:12](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
    So skipping the collision check here does not change for better or
    worse the hardness of loose object writes.
```

previous: [P1:13](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
As a small note related to the latter bullet point above, we must teach
the tmp-objdir routines to similarly skip the content-level collision
checks when calling migrate_one() on a loose object file, which we do by
setting the FOF_SKIP_COLLISION_CHECK bit when we are inside of a loose
object shard.
```

incoming: [N:1](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
This patch fixes a regression in b1b8dfde69 (finalize_object_file():
implement collision check, 2024-09-26) where fetching a v1 pack idx file
over the dumb-http protocol would cause the fetch to fail.
```

incoming: [N:3](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  0. We realize we need some object X, which we don't have locally, and
     nor does the other side have it as a loose object.
```

incoming: [N:4](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  1. We download the list of remote packs from objects/info/packs.
```

incoming: [N:5](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  2. For each entry in that file, we download each pack index and store
     it locally in .git/objects/pack/pack-$hash.idx (the $hash is not
     something we can verify yet and is given to us by the remote).
```

incoming: [N:6](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  3. We check each pack index we got to see if it has object X. When we
     find a match, we download the matching .pack file from the remote
     to a tempfile. We feed that to "index-pack --stdin", which
     reindexes the pack, rather than trusting that it has what the other
     side claims it does. In most cases, this will end up generating the
     exact same (byte-for-byte) pack index which we'll store at the same
     pack-$hash.idx path, because the index generation and $hash id are
     computed based on what's in the packfile. But:
```

incoming: [N:7](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
       a. The other side might have used other options to generate the
          index. For instance we use index v2 by default, but long ago
          it was v1 (and you can still ask for v1 explicitly).
```

incoming: [N:8](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
       b. The other side might even use a different mechanism to
          determine $hash. E.g., long ago it was based on the sorted
          list of objects in the packfile, but we switched to using the
          pack checksum in 1190a1acf8 (pack-objects: name pack files
          after trailer hash, 2013-12-05).
```

incoming: [N:9](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
The regression we saw in the real world was (3a). A recent client
fetching from a server with a v1 index downloaded that index, then
complained about trying to overwrite it with its own v2 index. This
collision is otherwise harmless; we know we want to replace the remote
version with our local one, but the collision check doesn't realize
that.
```

incoming: [N:10](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
There are a few options to fix it:
```

incoming: [N:11](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - we could teach index-pack a command-line option to ignore only pack
    idx collisions, and use it when the dumb-http code invokes
    index-pack. This would be an awkward thing to expose users to and
    would involve a lot of boilerplate to get the option down to the
    collision code.
```

incoming: [N:12](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - we could delete the remote .idx file right before running
    index-pack. It should be redundant at that point (since we've just
    downloaded the matching pack). But it feels risky to delete
    something from our own .git/objects based on what the other side has
    said. I'm not entirely positive that a malicious server couldn't lie
    about which pack-$hash.idx it has and get us to delete something
    precious.
```

incoming: [N:13](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - we can stop co-mingling the downloaded idx files in our local
    objects directory. This is a slightly bigger change but I think
    fixes the root of the problem more directly.
```

incoming: [N:14](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
This patch implements the third option. The big design questions are:
where do we store the downloaded files, and how do we manage their
lifetimes?
```

incoming: [N:15](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
There are some additional quirks to the dumb-http system we should
consider. Remember that in step 2 we downloaded every pack index, but in
step 3 we may only download some of the matching packs. What happens to
those other idx files now? They sit in the .git/objects/pack directory,
possibly waiting to be used at a later date. That may save bandwidth for
a subsequent fetch, but it also creates a lot of weird corner cases:
```

incoming: [N:16](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - our local object directory now has semi-untrusted .idx files sitting
    around, without their matching .pack
```

incoming: [N:17](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - in case 3b, we noted that we might not generate the same hash as the
    other side. In that case even if we download the matching pack,
    our index-pack invocation will store it in a different
    pack-$hash.idx file. And the unmatched .idx will sit there forever.
```

incoming: [N:18](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - if the server repacks, it may delete the old packs. Now we have
    these orphaned .idx files sitting around locally that will never be
    used (nor deleted).
```

incoming: [N:19](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
  - if we repack locally we may delete our local version of the server's
    pack index and not realize we have it. So we'll download it again,
    even though we have all of the objects it mentions.
```

incoming: [N:20](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
I think the right solution here is probably some more complex cache
management system: download the remote .idx files to their own storage
directory, mark them as "seen" when we get their matching pack (to avoid
re-downloading even if we repack), and then delete them when the
server's objects/info/refs no longer mentions them.
```

incoming: [N:21](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
But since the dumb http protocol is so ancient and so inferior to the
smart http protocol, I don't think it's worth spending a lot of time
creating such a system. For this patch I'm just downloading the idx
files to .git/objects/tmp_pack_*, and marking them as tempfiles to be
deleted when we exit (and due to the name, any we miss due to a crash,
etc, should eventually be removed by "git gc" runs based on timestamps).
```

incoming: [N:22](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
That is slightly worse for one case: if we download an idx but not the
matching pack, we won't retain that idx for subsequent runs. But the
flip side is that we're making other cases better (we never hold on to
useless idx files forever). I suspect that worse case does not even come
up often, since it implies that the packs are generated to match
distinct parts of history (i.e., in practice even in a repo with many
packs you're going to end up grabbing all of those packs to do a clone).
If somebody really cares about that, I think the right path forward is a
managed cache directory as above, and this patch is providing the first
step in that direction anyway (by moving things out of the objects/pack/
directory).
```

incoming: [N:23](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
There are two test changes. One demonstrates the broken v1 index case
(it double-checks the resulting clone with fsck to be careful, but prior
to this patch it actually fails at the clone step). The other tweaks the
expectation for a test that covers the "slightly worse" case to
accommodate the extra index download.
```

incoming: [N:24](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
The code changes are fairly simple. We stop using finalize_object_file()
to copy the remote's index file into place, and leave it as a tempfile.
We give the tempfile a real ".idx" name, since the packfile code expects
that, and thus we make sure it is out of the usual packs/ directory (so
we'd never mistake it for a real local .idx).
```

incoming: [N:25](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
We also have to change parse_pack_index(), which creates a temporary
packed_git to access our index (we need this because all of the pack idx
code assumes we have that struct). It reads the index data from the
tempfile, but prior to this patch would speculatively write the
finalized name into the packed_git struct using the pack-$hash we expect
to use.
```

incoming: [N:26](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
I was mildly surprised that this worked at all, since we call
verify_pack_index() on the packed_git which mentions the final name
before moving the file into place! But it works because
parse_pack_index() leaves the mmap-ed data in the struct, so the
lazy-open in verify_pack_index() never triggers, and we read from the
tempfile, ignoring the filename in the struct completely. Hacky, but it
works.
```

incoming: [N:27](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
After this patch, parse_pack_index() now uses the index filename we pass
in to derive a matching .pack name. This is OK to change because there
are only two callers, both in the dumb http code (and the other passes
in an existing pack-$hash.idx name, so the derived name is going to be
pack-$hash.pack, which is what we were using anyway).
```

incoming: [N:28](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
I'll follow up with some more cleanups in that area, but this patch is
sufficient to fix the regression.
```

### 14b/raw/module

Reconsider the earlier decision “We've had "FIXME!!! Collision check here ?" in finalize_object_file()
since aac1794132 (Improve sha1 object file writing., 2005-05-03). That
is, when we try to write a file with the same name, we assume the
on-disk contents are the same and blindly throw away the new copy.”. The new report gives the following behavior and its conditions. “b. The other side might even use a different mechanism to
          determine $hash. E.g., long ago it was based on the sorted
          list of objects in the packfile, but we switched to using the
          pack checksum in 1190a1acf8 (pack-objects: name pack files
          after trailer hash, 2013-12-05).

The regression we saw in the real world was (3a). A recent client
fetching from a server with a v1 index downloaded that index, then
complained about trying to overwrite it with its own v2 index. This
collision is otherwise harmless; we know we want to replace the remote
version with our local one, but the collision check doesn't realize
that.”

previous: [원문 구간](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93)

```text
We've had "FIXME!!! Collision check here ?" in finalize_object_file()
since aac1794132 (Improve sha1 object file writing., 2005-05-03). That
is, when we try to write a file with the same name, we assume the
on-disk contents are the same and blindly throw away the new copy.
```

incoming: [원문 구간](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc)

```text
b. The other side might even use a different mechanism to
          determine $hash. E.g., long ago it was based on the sorted
          list of objects in the packfile, but we switched to using the
          pack checksum in 1190a1acf8 (pack-objects: name pack files
          after trailer hash, 2013-12-05).

The regression we saw in the real world was (3a). A recent client
fetching from a server with a v1 index downloaded that index, then
complained about trying to overwrite it with its own v2 index. This
collision is otherwise harmless; we know we want to replace the remote
version with our local one, but the collision check doesn't realize
that.
```
## make-info

[새 보고](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac) · [실제 이전 결정](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4) · [유사 결정](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

Sharing the cleared suffix list breaks make info's explicit rule because its use of $* depended on a recognized suffix. Must identify that dependency, not merely show a Makefile regression.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | keep |
| 3b/raw/module | keep | 실패: 보류 | keep |
| 14b/raw/direct-full | reassess | 실패: 공유 Makefile에 빈 suffix 목록을 적용한 일을 주 Makefile에서 제거한 일로 설명한다. 명시적 규칙의 $*가 인식된 suffix에 의존한다는 핵심도 설명하지 않는다. | keep |
| 14b/raw/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | keep |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | keep | 실패: 보류 | keep |
| 14b/hidden/direct-full | keep | 실패: 보류 | keep |
| 14b/hidden/module | keep | 실패: 보류 | keep |
| 14b/hidden/direct-oracle | reassess | 실패: 명시 규칙의 .texi suffix 의존성은 찾았지만 $*가 인식된 suffix에 의존해 비게 되는 실제 실패 동작을 설명하지 않는다. 엄격 기준의 부분 성공이다. | keep |

### 3b/hidden/direct-full

The incoming report introduces a new issue where the 'make info' command fails due to a regression introduced in the commit referenced in the incoming report. This failure is related to the use of the '$*' variable in an explicit rule, which is resolved by using the $< variable. The earlier decision in P0 focused on fixing a dependency issue in the 'make lint-docs' command, unrelated to the 'make info' command.

previous: [P0:0](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
Documentation/Makefile: fix lint-docs mkdir dependency
```

previous: [P0:1](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
Since 8650c6298c (doc lint: make "lint-docs" non-.PHONY, 2021-10-15), we
put the output for gitlink linter into .build/lint-docs/gitlink. There
are order-only dependencies to create the sequence of subdirs like:
```

previous: [P0:2](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
  .build/lint-docs: | .build
          $(QUIET)mkdir $@
  .build/lint-docs/gitlink: | .build/lint-docs
          $(QUIET)mkdir $@
```

previous: [P0:3](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
where each level has to depend on the prior one (since the parent
directory must exist for us to create something inside it). But the
"howto" and "config" subdirectories of gitlink have the wrong
dependency; they depend on "lint-docs", not "lint-docs/gitlink".
```

previous: [P0:4](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
This usually works out, because the LINT_DOCS_GITLINK targets which
depend on "gitlink/howto" also depend on just "gitlink", so the
directory gets created anyway. But since we haven't given make an
explicit ordering, things can racily happen out of order.
```

previous: [P0:5](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
If you stick a "sleep 1" in the rule to build "gitlink" like this:
```

previous: [P0:6](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
   ## Lint: gitlink
   .build/lint-docs/gitlink: | .build/lint-docs
  -	$(QUIET)mkdir $@
  +	$(QUIET)sleep 1 && mkdir $@
```

previous: [P0:7](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
then "make clean; make lint-docs" will fail reliably. Or you can see it
as-is just by building the directory in isolation:
```

previous: [P0:8](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
  $ make clean
  [...]
  $ make .build/lint-docs/gitlink/howto
      GEN mergetools-list.made
      GEN cmd-list.made
      GEN doc.dep
      SUBDIR ../
  make[1]: 'GIT-VERSION-FILE' is up to date.
      SUBDIR ../
  make[1]: 'GIT-VERSION-FILE' is up to date.
  mkdir: cannot create directory ‘.build/lint-docs/gitlink/howto’: No such file or directory
  make: *** [Makefile:476: .build/lint-docs/gitlink/howto] Error 1
```

previous: [P0:9](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
The fix is easy: we just need to depend on the correct parent directory.
```

incoming: [N:0](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
Documentation/Makefile: fix "make info" regression in [ref]
```

incoming: [N:1](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
Fix a regression in my [ref] ([referenced subject], 2022-03-03). As explained in the GNU make documentation
for the $* variable, available at:
```

incoming: [N:2](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	info make --index-search='$*'
```

incoming: [N:3](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
This rule relied on ".texi" being in the default list of suffixes, as
seen at:
```

incoming: [N:4](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	make -f/dev/null -p | grep -v -e ^# -e ^$|grep -F .SUFFIXES
```

incoming: [N:5](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
The documentation explains what was going on here:
```

incoming: [N:6](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	In an explicit rule, there is no stem; so '$*' cannot be determined
	in that way.  Instead, if the target name ends with a recognized
	suffix (*note Old-Fashioned Suffix Rules: Suffix Rules.), '$*' is
	set to the target name minus the suffix.  For example, if the
	target name is 'foo.c', then '$*' is set to 'foo', since '.c' is a
	suffix.  GNU 'make' does this bizarre thing only for compatibility
	with other implementations of 'make'.  You should generally avoid
	using '$*' except in implicit rules or static pattern rules.
```

incoming: [N:7](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	If the target name in an explicit rule does not end with a
	recognized suffix, '$*' is set to the empty string for that rule.
```

incoming: [N:8](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
I.e. this rule added back in [ref] (Documentation: add
gitman.info target, 2007-12-10) was resolving gitman.texi from
gitman.info. We can instead just use the more obvious $< variable
referring to the prerequisite.
```

incoming: [N:9](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
This was the only use of $* in our Makefiles in an explicit rule, the
three remaining ones are all implicit rules, and therefore didn't
depend on the ".SUFFIXES" list.
```

### 3b/hidden/direct-oracle

The incoming report discusses changes related to the $* variable in Makefiles, specifically how it resolves suffixes. This does not directly relate to the issue described in P0, where the dependency structure for gitlink subdirectories was incorrect. The new evidence does not undermine any specific earlier decision or change a condition on which an earlier decision depended.

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The incoming report introduces a regression where the 'make info' command fails due to a missing dependency on the correct parent directory. This contradicts the earlier decision to fix the 'make lint-docs' command's dependency issues, as the new evidence shows that the 'make info' command now requires the same corrected dependency structure.

previous: [P0:3](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
where each level has to depend on the prior one (since the parent
directory must exist for us to create something inside it). But the
"howto" and "config" subdirectories of gitlink have the wrong
dependency; they depend on "lint-docs", not "lint-docs/gitlink".
```

previous: [P0:4](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
This usually works out, because the LINT_DOCS_GITLINK targets which
depend on "gitlink/howto" also depend on just "gitlink", so the
directory gets created anyway. But since we haven't given make an
explicit ordering, things can racily happen out of order.
```

previous: [P0:5](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
If you stick a "sleep 1" in the rule to build "gitlink" like this:
```

previous: [P0:6](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
   ## Lint: gitlink
   .build/lint-docs/gitlink: | .build/lint-docs
  -	$(QUIET)mkdir $@
  +	$(QUIET)sleep 1 && mkdir $@
```

previous: [P0:7](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
then "make clean; make lint-docs" will fail reliably. Or you can see it
as-is just by building the directory in isolation:
```

previous: [P0:8](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
  $ make clean
  [...]
  $ make .build/lint-docs/gitlink/howto
      GEN mergetools-list.made
      GEN cmd-list.made
      GEN doc.dep
      SUBDIR ../
  make[1]: 'GIT-VERSION-FILE' is up to date.
      SUBDIR ../
  make[1]: 'GIT-VERSION-FILE' is up to date.
  mkdir: cannot create directory ‘.build/lint-docs/gitlink/howto’: No such file or directory
  make: *** [Makefile:476: .build/lint-docs/gitlink/howto] Error 1
```

previous: [P0:9](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

```text
The fix is easy: we just need to depend on the correct parent directory.
```

incoming: [N:0](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
Documentation/Makefile: fix "make info" regression in dad9cd7d518
```

incoming: [N:1](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
Fix a regression in my dad9cd7d518 (Makefile: move ".SUFFIXES" rule to
shared.mak, 2022-03-03). As explained in the GNU make documentation
for the $* variable, available at:
```

incoming: [N:2](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	info make --index-search='$*'
```

incoming: [N:3](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
This rule relied on ".texi" being in the default list of suffixes, as
seen at:
```

incoming: [N:4](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	make -f/dev/null -p | grep -v -e ^# -e ^$|grep -F .SUFFIXES
```

incoming: [N:5](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
The documentation explains what was going on here:
```

incoming: [N:6](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	In an explicit rule, there is no stem; so '$*' cannot be determined
	in that way.  Instead, if the target name ends with a recognized
	suffix (*note Old-Fashioned Suffix Rules: Suffix Rules.), '$*' is
	set to the target name minus the suffix.  For example, if the
	target name is 'foo.c', then '$*' is set to 'foo', since '.c' is a
	suffix.  GNU 'make' does this bizarre thing only for compatibility
	with other implementations of 'make'.  You should generally avoid
	using '$*' except in implicit rules or static pattern rules.
```

incoming: [N:7](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	If the target name in an explicit rule does not end with a
	recognized suffix, '$*' is set to the empty string for that rule.
```

incoming: [N:8](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
I.e. this rule added back in 5cefc33bffd (Documentation: add
gitman.info target, 2007-12-10) was resolving gitman.texi from
gitman.info. We can instead just use the more obvious $< variable
referring to the prerequisite.
```

incoming: [N:9](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
This was the only use of $* in our Makefiles in an explicit rule, the
three remaining ones are all implicit rules, and therefore didn't
depend on the ".SUFFIXES" list.
```

### 3b/raw/module

no supported observation with its condition in the report window

### 14b/hidden/direct-full

The incoming report addresses a specific issue related to the use of the $* variable in an explicit rule within the Makefile, which is distinct from the issues addressed in P0 and P1. The new evidence does not undermine or change the conditions of the earlier decisions.

### 14b/hidden/direct-oracle

The earlier decision in P1 modified the Makefile to disable default implicit rules, which inadvertently caused a regression in the handling of explicit rules. The new evidence shows that an explicit rule relying on the default suffixes for ".texi" files no longer works as expected after the change, necessitating a fix.

previous: [P1:1](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
This was added in 30248886ce8 (Makefile: disable default implicit
rules, 2010-01-26), let's move it to the top of "shared.mak" so it'll
apply to all our Makefiles.
```

previous: [P1:2](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
This doesn't benefit the main Makefile at all, since it already had
the rule, but since we're including shared.mak in other Makefiles
starts to benefit them. E.g. running the 'man" target is now faster:
```

previous: [P1:6](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
The reason for that can be seen when comparing that run with
"--debug=a". Without this change making a target like "git-status.1"
will cause "make" to consider not only "git-status.txt", but
"git-status.txt.o", as well as numerous other implicit suffixes such
as ".c", ".cc", ".cpp" etc. See [1] for a more detailed before/after
example.
```

incoming: [N:1](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
Fix a regression in my [ref] ([referenced subject], 2022-03-03). As explained in the GNU make documentation
for the $* variable, available at:
```

incoming: [N:3](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
This rule relied on ".texi" being in the default list of suffixes, as
seen at:
```

incoming: [N:6](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	In an explicit rule, there is no stem; so '$*' cannot be determined
	in that way.  Instead, if the target name ends with a recognized
	suffix (*note Old-Fashioned Suffix Rules: Suffix Rules.), '$*' is
	set to the target name minus the suffix.  For example, if the
	target name is 'foo.c', then '$*' is set to 'foo', since '.c' is a
	suffix.  GNU 'make' does this bizarre thing only for compatibility
	with other implementations of 'make'.  You should generally avoid
	using '$*' except in implicit rules or static pattern rules.
```

incoming: [N:7](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	If the target name in an explicit rule does not end with a
	recognized suffix, '$*' is set to the empty string for that rule.
```

incoming: [N:8](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
I.e. this rule added back in [ref] (Documentation: add
gitman.info target, 2007-12-10) was resolving gitman.texi from
gitman.info. We can instead just use the more obvious $< variable
referring to the prerequisite.
```

incoming: [N:9](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
This was the only use of $* in our Makefiles in an explicit rule, the
three remaining ones are all implicit rules, and therefore didn't
depend on the ".SUFFIXES" list.
```

### 14b/hidden/module

no supported observation with its condition in the report window

### 14b/raw/direct-full

The incoming report indicates that the change made in P1 introduced a regression in the 'make info' command, specifically due to the removal of ".SUFFIXES" from the main Makefile. This change affected the resolution of prerequisites in explicit rules, leading to issues with the 'gitman.info' target.

previous: [P1:0](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
Makefile: move ".SUFFIXES" rule to shared.mak
```

previous: [P1:1](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
This was added in 30248886ce8 (Makefile: disable default implicit
rules, 2010-01-26), let's move it to the top of "shared.mak" so it'll
apply to all our Makefiles.
```

previous: [P1:2](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
This doesn't benefit the main Makefile at all, since it already had
the rule, but since we're including shared.mak in other Makefiles
starts to benefit them. E.g. running the 'man" target is now faster:
```

previous: [P1:3](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
    $ git -c hyperfine.hook.setup= hyperfine -L rev HEAD~1,HEAD~0 -s 'make -C Documentation man' 'make -C Documentation -j1 man'
    Benchmark 1: make -C Documentation -j1 man' in 'HEAD~1
      Time (mean ± σ):     121.7 ms ±   8.8 ms    [User: 105.8 ms, System: 18.6 ms]
      Range (min … max):   112.8 ms … 148.4 ms    26 runs
```

previous: [P1:4](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
    Benchmark 2: make -C Documentation -j1 man' in 'HEAD~0
      Time (mean ± σ):      97.5 ms ±   8.0 ms    [User: 80.1 ms, System: 20.1 ms]
      Range (min … max):    89.8 ms … 111.8 ms    32 runs
```

previous: [P1:5](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
    Summary
      'make -C Documentation -j1 man' in 'HEAD~0' ran
        1.25 ± 0.14 times faster than 'make -C Documentation -j1 man' in 'HEAD~1'
```

previous: [P1:6](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
The reason for that can be seen when comparing that run with
"--debug=a". Without this change making a target like "git-status.1"
will cause "make" to consider not only "git-status.txt", but
"git-status.txt.o", as well as numerous other implicit suffixes such
as ".c", ".cc", ".cpp" etc. See [1] for a more detailed before/after
example.
```

previous: [P1:7](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
So this is causing us to omit a bunch of work we didn't need to
do. For making "git-status.1" the "--debug=a" output is reduced from
~140k lines to ~6k.
```

previous: [P1:8](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4)

```text
1. https://lore.kernel.org/git/220222.86bkyz875k.gmgdl@evledraar.gmail.com/
```

incoming: [N:0](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
Documentation/Makefile: fix "make info" regression in dad9cd7d518
```

incoming: [N:1](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
Fix a regression in my dad9cd7d518 (Makefile: move ".SUFFIXES" rule to
shared.mak, 2022-03-03). As explained in the GNU make documentation
for the $* variable, available at:
```

incoming: [N:2](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	info make --index-search='$*'
```

incoming: [N:3](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
This rule relied on ".texi" being in the default list of suffixes, as
seen at:
```

incoming: [N:4](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	make -f/dev/null -p | grep -v -e ^# -e ^$|grep -F .SUFFIXES
```

incoming: [N:5](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
The documentation explains what was going on here:
```

incoming: [N:6](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	In an explicit rule, there is no stem; so '$*' cannot be determined
	in that way.  Instead, if the target name ends with a recognized
	suffix (*note Old-Fashioned Suffix Rules: Suffix Rules.), '$*' is
	set to the target name minus the suffix.  For example, if the
	target name is 'foo.c', then '$*' is set to 'foo', since '.c' is a
	suffix.  GNU 'make' does this bizarre thing only for compatibility
	with other implementations of 'make'.  You should generally avoid
	using '$*' except in implicit rules or static pattern rules.
```

incoming: [N:7](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
	If the target name in an explicit rule does not end with a
	recognized suffix, '$*' is set to the empty string for that rule.
```

incoming: [N:8](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac)

```text
I.e. this rule added back in 5cefc33bffd (Documentation: add
gitman.info target, 2007-12-10) was resolving gitman.texi from
gitman.info. We can instead just use the more obvious $< variable
referring to the prerequisite.
```

### 14b/raw/module

no supported observation with its condition in the report window
## patch-search

[새 보고](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4) · [실제 이전 결정](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9) · [유사 결정](https://github.com/git/git/commit/d85d7ecb80ebc93f7380b4196c303756ee051668)

The search-key change inserted a captureless regex, making $1 undef. Initial /regex search now warns and asks for the expression again. Identify either this actual failed search behavior or the capture overwrite and its triggering inserted regex.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/raw/module | reassess | 성공: 검색 변경과 네 hunk에서 /Many가 경고 후 다시 정규식을 묻는 실제 동작을 함께 인용한다. | keep |
| 14b/raw/direct-full | reassess | 실패: / 기능 실패라는 요약은 있지만 초기 검색의 경고·재질문 또는 새 무캡처 정규식에 의한 $1 손실을 설명하지 않는다. 인용은 충분하나 설명은 부분 성공이다. | keep |
| 14b/raw/module | reassess | 성공: 검색 변경과 네 hunk에서 /Many가 경고 후 다시 정규식을 묻는 실제 동작을 함께 인용한다. | keep |
| 3b/hidden/direct-full | reassess | 성공: 새 정규식 삽입이 $1을 undef로 만들고 /regex 검색을 망가뜨리는 인과를 원문으로 뒷받침한다. | reassess |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | invalid_output | 실패: 형식 오류 | reassess |
| 14b/hidden/direct-full | reassess | 실패: 올바른 regex 근거를 인용했지만 설명은 원인을 코드베이스의 다른 곳으로 돌리며 실제 $1 덮어쓰기나 재질문 동작을 짚지 않는다. | reassess |
| 14b/hidden/module | keep | 실패: 보류 | keep |
| 14b/hidden/direct-oracle | reassess | 실패: 다중 hunk의 검색 실패는 찾았으나 단일 hunk 검색 제한 정책이 무의미해졌다고 해석하고 모든 경우로 일반화한다. | reassess |

### 3b/raw/direct-full

The new evidence shows that the issue arises because the addition of a new regex match between the old match and the corresponding code that was expecting $1 made the $1 variable always undef. This breakage is directly related to the change in P1, which introduced the condition for disabling search functionality when there's only a single hunk.

previous: [P0:0](https://github.com/git/git/commit/d85d7ecb80ebc93f7380b4196c303756ee051668)

```text
add--interactive: quote commentChar regex
```

previous: [P0:2](https://github.com/git/git/commit/d85d7ecb80ebc93f7380b4196c303756ee051668)

```text
  /^$commentChar/
```

previous: [P0:3](https://github.com/git/git/commit/d85d7ecb80ebc93f7380b4196c303756ee051668)

```text
If your chosen comment character is a regex metacharacter,
then that will behave in a confusing manner ("$", for
instance, would only eliminate blank lines, not actual
comment lines).
```

incoming: [N:0](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
add -p: fix 2.17.0-rc* regression due to moved code
```

incoming: [N:1](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
Fix a regression in 88f6ffc1c2 ("add -p: only bind search key if
there's more than one hunk", 2018-02-13) which is present in
2.17.0-rc*, but not 2.16.0.
```

incoming: [N:2](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
In Perl, regex variables like $1 always refer to the last regex
match. When the aforementioned change added a new regex match between
the old match and the corresponding code that was expecting $1, the $1
variable would always be undef, since the newly inserted regex match
doesn't have any captures.
```

incoming: [N:3](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
As a result the "/" feature to search for a string in a hunk by regex
completely broke, on git.git:
```

incoming: [N:4](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
    $ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many
```

incoming: [N:5](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
I.e. the initial "/regex" command wouldn't work, and would always emit
a warning and ask again for a regex, now it works as intended again.
```

### 3b/raw/module

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

previous: [원문 구간](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9)

```text
If there is only a single hunk then disable searching as there is
nothing to search for. Also print a specific error message if the user
tries to search with '/' when there's only a single hunk rather than
just listing the key bindings.
```

incoming: [원문 구간](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
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
```

### 3b/hidden/direct-full

The new evidence shows that the regression introduced in the commit referenced in P1 caused the issue described in N:2, N:3, and N:4. Specifically, the addition of a new regex match between the old match and the corresponding code that was expecting $1 made $1 always undefined, leading to the warning and the broken functionality of the '/regex' command.

previous: [P0:0](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9)

```text
add -p: only bind search key if there's more than one hunk
```

previous: [P0:1](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9)

```text
If there is only a single hunk then disable searching as there is
nothing to search for. Also print a specific error message if the user
tries to search with '/' when there's only a single hunk rather than
just listing the key bindings.
```

incoming: [N:2](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
In Perl, regex variables like $1 always refer to the last regex
match. When the aforementioned change added a new regex match between
the old match and the corresponding code that was expecting $1, the $1
variable would always be undef, since the newly inserted regex match
doesn't have any captures.
```

incoming: [N:3](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
As a result the "/" feature to search for a string in a hunk by regex
completely broke, on git.git:
```

incoming: [N:4](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
    $ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many
```

### 3b/hidden/direct-oracle

invalid_output

### 3b/hidden/module

no unique decision in the document comparison

### 14b/hidden/direct-full

The earlier decision in P0 introduced a feature to disable searching in single-hunk scenarios and to provide an error message if the user attempts to search. However, the new evidence shows that the '/regex' feature has broken due to a regression unrelated to the number of hunks, indicating that the issue lies elsewhere in the codebase. This suggests that the condition on which the earlier decision depended (the presence of multiple hunks for enabling search) is not the root cause of the current failure.

previous: [P0:0](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9)

```text
add -p: only bind search key if there's more than one hunk
```

previous: [P0:1](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9)

```text
If there is only a single hunk then disable searching as there is
nothing to search for. Also print a specific error message if the user
tries to search with '/' when there's only a single hunk rather than
just listing the key bindings.
```

incoming: [N:2](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
In Perl, regex variables like $1 always refer to the last regex
match. When the aforementioned change added a new regex match between
the old match and the corresponding code that was expecting $1, the $1
variable would always be undef, since the newly inserted regex match
doesn't have any captures.
```

incoming: [N:4](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
    $ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many
```

### 14b/hidden/direct-oracle

The earlier decision to disable searching when there is only a single hunk may no longer be relevant due to the reported issue where the '/regex' command fails and emits a warning even when multiple hunks are present. The new evidence shows that the '/regex' feature completely breaks, indicating a more fundamental issue with the implementation that affects all cases, not just single hunks.

previous: [P0:1](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9)

```text
If there is only a single hunk then disable searching as there is
nothing to search for. Also print a specific error message if the user
tries to search with '/' when there's only a single hunk rather than
just listing the key bindings.
```

incoming: [N:3](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
As a result the "/" feature to search for a string in a hunk by regex
completely broke, on git.git:
```

incoming: [N:4](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
    $ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many
```

incoming: [N:5](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
I.e. the initial "/regex" command wouldn't work, and would always emit
a warning and ask again for a regex, now it works as intended again.
```

### 14b/raw/direct-full

The regression introduced in P1 due to the modification of the code flow has caused the "/" feature to fail, as evidenced by the error messages and behavior described in N.

previous: [P1:0](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9)

```text
add -p: only bind search key if there's more than one hunk
```

previous: [P1:1](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9)

```text
If there is only a single hunk then disable searching as there is
nothing to search for. Also print a specific error message if the user
tries to search with '/' when there's only a single hunk rather than
just listing the key bindings.
```

incoming: [N:1](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
Fix a regression in 88f6ffc1c2 ("add -p: only bind search key if
there's more than one hunk", 2018-02-13) which is present in
2.17.0-rc*, but not 2.16.0.
```

incoming: [N:2](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
In Perl, regex variables like $1 always refer to the last regex
match. When the aforementioned change added a new regex match between
the old match and the corresponding code that was expecting $1, the $1
variable would always be undef, since the newly inserted regex match
doesn't have any captures.
```

incoming: [N:4](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
    $ perl -pi -e 's/Git/Tig/g' README.md
    $ ./git --exec-path=$PWD add -p
    [..]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? s
    Split into 4 hunks.
    [...]
    Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? /Many
    Use of uninitialized value $1 in string eq at /home/avar/g/git/git-add--interactive line 1568, <STDIN> line 1.
    search for regex? Many
```

incoming: [N:5](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
I.e. the initial "/regex" command wouldn't work, and would always emit
a warning and ask again for a regex, now it works as intended again.
```

### 14b/raw/module

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

previous: [원문 구간](https://github.com/git/git/commit/88f6ffc1c256ef241cbed33dabbdd23c1a7ac6a9)

```text
If there is only a single hunk then disable searching as there is
nothing to search for. Also print a specific error message if the user
tries to search with '/' when there's only a single hunk rather than
just listing the key bindings.
```

incoming: [원문 구간](https://github.com/git/git/commit/fd2fb4aa0cc2a25a8e4ddf3f3c48880f317edcf4)

```text
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
```

### 14b/hidden/module

no unique decision in the document comparison
## prompt

[새 보고](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c) · [실제 이전 결정](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f) · [유사 결정](https://github.com/git/git/commit/1f6806cf2da84e30d162ca3aee15d16db4f1daef)

The protected branch-name indirection assumes the shell expands PS1, but default zsh does not and shows the literal variable; condition the indirection on expansion.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 성공: PS1 확장 가정, 기본 zsh 비확장과 리터럴 변수 표시를 정확히 연결한다. | keep |
| 3b/raw/module | keep | 실패: 보류 | keep |
| 14b/raw/direct-full | reassess | 성공: 기존 PS1 간접 참조 가정과 기본 zsh의 비확장으로 변수 문자열이 출력되는 실패를 정확히 설명한다. | keep |
| 14b/raw/module | reassess | 성공: PS1 간접 참조 결정과 기본 zsh 비확장 때문에 변수 문자열이 그대로 출력되는 실패를 함께 보존한다. | keep |
| 3b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | keep |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | invalid_output | 실패: 형식 오류 | keep |
| 14b/hidden/direct-full | reassess | 성공: 변수 간접 참조로 보호한 PS1이 확장하지 않는 셸에서 리터럴을 표시하는 문제를 정확히 설명하고 zsh 조건을 인용한다. | keep |
| 14b/hidden/module | reassess | 성공: PS1 확장 가정, 기본 zsh 비확장, 리터럴 변수 표시와 조건 검사 방향이 인용을 포함한 설명에 모두 남는다. | keep |
| 14b/hidden/direct-oracle | reassess | 성공: PS1 확장 가정과 zsh의 리터럴 표시 오류를 연결하고 조건부 처리가 필요함을 원문으로 뒷받침한다. | keep |

### 3b/hidden/direct-full

The new evidence suggests that not all shells expand the value of PS1 by default, contrary to the assumption made in P0. This change could lead to prompts containing literal strings instead of the actual branch names, as observed in the regression reported in N.

previous: [P0:0](https://github.com/git/git/commit/1f6806cf2da84e30d162ca3aee15d16db4f1daef)

```text
git-prompt.sh: optionally show upstream branch name
```

previous: [P0:1](https://github.com/git/git/commit/1f6806cf2da84e30d162ca3aee15d16db4f1daef)

```text
When working with multiple remotes, it is common to switch the upstream
from a remote to another. Doing so, the prompt may not be the expected
one. Providing an option to display tracking information sounds useful.
```

previous: [P0:2](https://github.com/git/git/commit/1f6806cf2da84e30d162ca3aee15d16db4f1daef)

```text
Add a "name" option to GIT_PS1_SHOWUPSTREAM which will show the upstream
abbrev name. This option is ignored if "verbose" is false.
```

incoming: [N:0](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
git-prompt.sh: don't assume the shell expands the value of PS1
```

incoming: [N:1](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
Not all shells subject the prompt string to parameter expansion.  Test
whether the shell will expand the value of PS1, and use the result to
control whether raw ref names are included directly in PS1.
```

incoming: [N:2](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
This fixes a regression introduced in commit [ref] ("[referenced subject]"):  zsh does not expand PS1
by default, but that commit assumed it did.  The bug resulted in
prompts containing the literal string '${__git_ps1_branch_name}'
instead of the actual branch name.
```

### 3b/hidden/direct-oracle

invalid_output

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The new evidence indicates that not all shells expand the value of PS1 by default, contrary to the assumption made in P0. This change affects zsh, leading to prompts containing the literal string '${__git_ps1_branch_name}' instead of the actual branch name.

previous: [P0:0](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f)

```text
git-prompt.sh: don't put unsanitized branch names in $PS1
```

previous: [P0:1](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f)

```text
Both bash and zsh subject the value of PS1 to parameter expansion,
command substitution, and arithmetic expansion.  Rather than include
the raw, unescaped branch name in PS1 when running in two- or
three-argument mode, construct PS1 to reference a variable that holds
the branch name.  Because the shells do not recursively expand, this
avoids arbitrary code execution by specially-crafted branch names such
as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.
```

incoming: [N:0](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
git-prompt.sh: don't assume the shell expands the value of PS1
```

incoming: [N:1](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
Not all shells subject the prompt string to parameter expansion.  Test
whether the shell will expand the value of PS1, and use the result to
control whether raw ref names are included directly in PS1.
```

incoming: [N:2](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
This fixes a regression introduced in commit 8976500 ("git-prompt.sh:
don't put unsanitized branch names in $PS1"):  zsh does not expand PS1
by default, but that commit assumed it did.  The bug resulted in
prompts containing the literal string '${__git_ps1_branch_name}'
instead of the actual branch name.
```

### 3b/raw/module

no supported observation with its condition in the report window

### 14b/hidden/direct-full

The earlier decision in P1 aimed to prevent arbitrary code execution by ensuring branch names were not directly included in PS1. However, the new evidence indicates that not all shells expand PS1 values, leading to prompts displaying literal strings instead of actual branch names. This suggests that the approach taken in P1 needs to be reconsidered to account for different shell behaviors.

previous: [P1:0](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f)

```text
git-prompt.sh: don't put unsanitized branch names in $PS1
```

previous: [P1:1](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f)

```text
Both bash and zsh subject the value of PS1 to parameter expansion,
command substitution, and arithmetic expansion.  Rather than include
the raw, unescaped branch name in PS1 when running in two- or
three-argument mode, construct PS1 to reference a variable that holds
the branch name.  Because the shells do not recursively expand, this
avoids arbitrary code execution by specially-crafted branch names such
as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.
```

incoming: [N:0](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
git-prompt.sh: don't assume the shell expands the value of PS1
```

incoming: [N:1](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
Not all shells subject the prompt string to parameter expansion.  Test
whether the shell will expand the value of PS1, and use the result to
control whether raw ref names are included directly in PS1.
```

incoming: [N:2](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
This fixes a regression introduced in commit [ref] ("[referenced subject]"):  zsh does not expand PS1
by default, but that commit assumed it did.  The bug resulted in
prompts containing the literal string '${__git_ps1_branch_name}'
instead of the actual branch name.
```

### 14b/hidden/direct-oracle

The earlier decision assumed that all shells perform parameter expansion on PS1, which led to a regression in zsh where prompts contained literal strings instead of expanded values. The new evidence shows that not all shells expand PS1, necessitating a conditional check.

previous: [P1:1](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f)

```text
Both bash and zsh subject the value of PS1 to parameter expansion,
command substitution, and arithmetic expansion.  Rather than include
the raw, unescaped branch name in PS1 when running in two- or
three-argument mode, construct PS1 to reference a variable that holds
the branch name.  Because the shells do not recursively expand, this
avoids arbitrary code execution by specially-crafted branch names such
as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.
```

incoming: [N:1](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
Not all shells subject the prompt string to parameter expansion.  Test
whether the shell will expand the value of PS1, and use the result to
control whether raw ref names are included directly in PS1.
```

incoming: [N:2](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
This fixes a regression introduced in commit [ref] ("[referenced subject]"):  zsh does not expand PS1
by default, but that commit assumed it did.  The bug resulted in
prompts containing the literal string '${__git_ps1_branch_name}'
instead of the actual branch name.
```

### 14b/hidden/module

Reconsider the earlier decision “Both bash and zsh subject the value of PS1 to parameter expansion,
command substitution, and arithmetic expansion.  Rather than include
the raw, unescaped branch name in PS1 when running in two- or
three-argument mode, construct PS1 to reference a variable that holds
the branch name.  Because the shells do not recursively expand, this
avoids arbitrary code execution by specially-crafted branch names such
as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.”. The new report gives the following behavior and its conditions. “Not all shells subject the prompt string to parameter expansion.  Test
whether the shell will expand the value of PS1, and use the result to
control whether raw ref names are included directly in PS1.

This fixes a regression introduced in commit [ref] ("[referenced subject]"):  zsh does not expand PS1
by default, but that commit assumed it did.  The bug resulted in
prompts containing the literal string '${__git_ps1_branch_name}'
instead of the actual branch name.”

previous: [원문 구간](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f)

```text
Both bash and zsh subject the value of PS1 to parameter expansion,
command substitution, and arithmetic expansion.  Rather than include
the raw, unescaped branch name in PS1 when running in two- or
three-argument mode, construct PS1 to reference a variable that holds
the branch name.  Because the shells do not recursively expand, this
avoids arbitrary code execution by specially-crafted branch names such
as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.
```

incoming: [원문 구간](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
Not all shells subject the prompt string to parameter expansion.  Test
whether the shell will expand the value of PS1, and use the result to
control whether raw ref names are included directly in PS1.

This fixes a regression introduced in commit [ref] ("[referenced subject]"):  zsh does not expand PS1
by default, but that commit assumed it did.  The bug resulted in
prompts containing the literal string '${__git_ps1_branch_name}'
instead of the actual branch name.
```

### 14b/raw/direct-full

The original decision in P0 aimed to prevent unsanitized branch names from being included in PS1 due to potential security risks. However, the new evidence indicates that this change introduced a regression in zsh where PS1 is not expanded by default, leading to prompts displaying the literal string '${__git_ps1_branch_name}' instead of the actual branch name. This suggests that the condition under which the original decision was made (that all shells expand PS1) does not hold universally.

previous: [P0:0](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f)

```text
git-prompt.sh: don't put unsanitized branch names in $PS1
```

previous: [P0:1](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f)

```text
Both bash and zsh subject the value of PS1 to parameter expansion,
command substitution, and arithmetic expansion.  Rather than include
the raw, unescaped branch name in PS1 when running in two- or
three-argument mode, construct PS1 to reference a variable that holds
the branch name.  Because the shells do not recursively expand, this
avoids arbitrary code execution by specially-crafted branch names such
as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.
```

incoming: [N:0](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
git-prompt.sh: don't assume the shell expands the value of PS1
```

incoming: [N:1](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
Not all shells subject the prompt string to parameter expansion.  Test
whether the shell will expand the value of PS1, and use the result to
control whether raw ref names are included directly in PS1.
```

incoming: [N:2](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
This fixes a regression introduced in commit 8976500 ("git-prompt.sh:
don't put unsanitized branch names in $PS1"):  zsh does not expand PS1
by default, but that commit assumed it did.  The bug resulted in
prompts containing the literal string '${__git_ps1_branch_name}'
instead of the actual branch name.
```

### 14b/raw/module

Reconsider the earlier decision “Both bash and zsh subject the value of PS1 to parameter expansion,
command substitution, and arithmetic expansion.  Rather than include
the raw, unescaped branch name in PS1 when running in two- or
three-argument mode, construct PS1 to reference a variable that holds
the branch name.  Because the shells do not recursively expand, this
avoids arbitrary code execution by specially-crafted branch names such
as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.”. The new report gives the following behavior and its conditions. “This fixes a regression introduced in commit 8976500 ("git-prompt.sh:
don't put unsanitized branch names in $PS1"):  zsh does not expand PS1
by default, but that commit assumed it did.  The bug resulted in
prompts containing the literal string '${__git_ps1_branch_name}'
instead of the actual branch name.”

previous: [원문 구간](https://github.com/git/git/commit/8976500cbbb13270398d3b3e07a17b8cc7bff43f)

```text
Both bash and zsh subject the value of PS1 to parameter expansion,
command substitution, and arithmetic expansion.  Rather than include
the raw, unescaped branch name in PS1 when running in two- or
three-argument mode, construct PS1 to reference a variable that holds
the branch name.  Because the shells do not recursively expand, this
avoids arbitrary code execution by specially-crafted branch names such
as '$(IFS=_;cmd=sudo_rm_-rf_/;$cmd)'.
```

incoming: [원문 구간](https://github.com/git/git/commit/1e4119c81b3e203e1729e03be6e4a53eb9207f5c)

```text
This fixes a regression introduced in commit 8976500 ("git-prompt.sh:
don't put unsanitized branch names in $PS1"):  zsh does not expand PS1
by default, but that commit assumed it did.  The bug resulted in
prompts containing the literal string '${__git_ps1_branch_name}'
instead of the actual branch name.
```
## range

[새 보고](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83) · [실제 이전 결정](https://github.com/git/git/commit/73a834e9e27906a76940f1ced5c132bce205d3f8) · [유사 결정](https://github.com/git/git/commit/87f1b2d45ca7987cc6cc1a74eb66a77fa11fab94)

Moving diff configuration into range-diff stopped forwarding flags such as --no-patch or --stat; propagate caller options again.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/raw/module | keep | 실패: 보류 | keep |
| 14b/raw/direct-full | reassess | 성공: 설정을 range-diff 내부로 옮긴 결정과 --no-patch/--stat 전달 중단을 정확히 연결한다. | reassess |
| 14b/raw/module | reassess | 성공: 호출자 설정을 내부로 옮긴 결정과 --no-patch/--stat 전달 실패가 설명에 인용되어 있다. | reassess |
| 3b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | reassess |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | keep | 실패: 보류 | keep |
| 14b/hidden/direct-full | reassess | 실패: 대상 또는 인용 불일치 | keep |
| 14b/hidden/module | keep | 실패: 보류 | keep |
| 14b/hidden/direct-oracle | reassess | 실패: 대상 또는 인용 불일치 | keep |

### 3b/raw/direct-full

The incoming report indicates a regression in passing down diff options, specifically --no-patch and --stat, which was introduced in P1. However, the issue described in N:0 and N:1 suggests that the previous fix in P0 did not properly handle these options, leading to a regression. This implies that the original decision in P0 may no longer be sufficient to address the current issue.

previous: [P0:0](https://github.com/git/git/commit/87f1b2d45ca7987cc6cc1a74eb66a77fa11fab94)

```text
range-diff: respect diff_option.file rather than assuming 'stdout'
```

previous: [P0:1](https://github.com/git/git/commit/87f1b2d45ca7987cc6cc1a74eb66a77fa11fab94)

```text
The actual diffs output by range-diff respect diff_option.file, which
range-diff passes down the call-chain, thus are destination-agnostic.
However, output_pair_header() is hard-coded to emit to 'stdout'. Fix
this by making output_pair_header() respect diff_option.file, as well.
```

incoming: [N:0](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
range-diff: fix regression in passing along diff options
```

incoming: [N:1](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
In 73a834e9e2 ("range-diff: relieve callers of low-level configuration
burden", 2018-07-22) we broke passing down options like --no-patch,
--stat etc.
```

incoming: [N:2](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
Fix that regression, and add a test asserting the pre-73a834e9e2
behavior for some of these diff options.
```

incoming: [N:3](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
As noted in a change leading up to this ("range-diff doc: add a
section about output stability", 2018-11-07) the output is not meant
to be stable. So this regression test will likely need to be tweaked
once we get a "proper" --stat option.
```

incoming: [N:4](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
See
https://public-inbox.org/git/nycvar.QRO.7.76.6.1811071202480.39@tvgsbejvaqbjf.bet/
for a further explanation of the regression. The fix here is not the
same as in Johannes's on-list patch, for reasons that'll be explained
in a follow-up commit.
```

### 3b/raw/module

no unique decision in the document comparison

### 3b/hidden/direct-full

The incoming report mentions a regression in passing down diff options, specifically --no-patch and --stat, which was fixed in the earlier decision P0. However, the new evidence indicates that the output is not meant to be stable, suggesting that the current implementation may still be problematic despite the fix.

previous: [P0:0](https://github.com/git/git/commit/87f1b2d45ca7987cc6cc1a74eb66a77fa11fab94)

```text
range-diff: respect diff_option.file rather than assuming 'stdout'
```

previous: [P0:1](https://github.com/git/git/commit/87f1b2d45ca7987cc6cc1a74eb66a77fa11fab94)

```text
The actual diffs output by range-diff respect diff_option.file, which
range-diff passes down the call-chain, thus are destination-agnostic.
However, output_pair_header() is hard-coded to emit to 'stdout'. Fix
this by making output_pair_header() respect diff_option.file, as well.
```

incoming: [N:0](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
range-diff: fix regression in passing along diff options
```

incoming: [N:1](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
In [ref] ("[referenced subject]", 2018-07-22) we broke passing down options like --no-patch,
--stat etc.
```

incoming: [N:2](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
Fix that regression, and add a test asserting the pre-[ref]
behavior for some of these diff options.
```

incoming: [N:3](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
As noted in a change leading up to this ("range-diff doc: add a
section about output stability", 2018-11-07) the output is not meant
to be stable. So this regression test will likely need to be tweaked
once we get a "proper" --stat option.
```

incoming: [N:4](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
See
https://public-inbox.org/git/nycvar.QRO.7.76.6.[ref].39@tvgsbejvaqbjf.bet/
for a further explanation of the regression. The fix here is not the
same as in Johannes's on-list patch, for reasons that'll be explained
in a follow-up commit.
```

### 3b/hidden/direct-oracle

The incoming report mentions breaking the passing down of options like --no-patch, --stat, etc., which is unrelated to the earlier decisions about handling specific configuration details and localizing tweaks for range-diff generation. The earlier decisions did not address the issue of passing down options, hence no reconsideration is warranted.

### 3b/hidden/module

no unique decision in the document comparison

### 14b/hidden/direct-full

The earlier decision in P0 aimed to make the range-diff output destination-agnostic by respecting diff_option.file. However, the incoming report indicates a regression where certain diff options like --no-patch and --stat are not being passed down correctly, undermining the intended stability and flexibility of the range-diff output.

previous: [P0:0](https://github.com/git/git/commit/87f1b2d45ca7987cc6cc1a74eb66a77fa11fab94)

```text
range-diff: respect diff_option.file rather than assuming 'stdout'
```

previous: [P0:1](https://github.com/git/git/commit/87f1b2d45ca7987cc6cc1a74eb66a77fa11fab94)

```text
The actual diffs output by range-diff respect diff_option.file, which
range-diff passes down the call-chain, thus are destination-agnostic.
However, output_pair_header() is hard-coded to emit to 'stdout'. Fix
this by making output_pair_header() respect diff_option.file, as well.
```

incoming: [N:1](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
In [ref] ("[referenced subject]", 2018-07-22) we broke passing down options like --no-patch,
--stat etc.
```

incoming: [N:2](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
Fix that regression, and add a test asserting the pre-[ref]
behavior for some of these diff options.
```

### 14b/hidden/direct-oracle

The earlier decision in P0 aimed to make the output of range-diff destination-agnostic by respecting diff_option.file. However, the incoming report indicates a regression where passing down options like --no-patch and --stat was broken, suggesting that the fix in P0 did not fully address the issue of maintaining compatibility with various diff options.

previous: [P0:1](https://github.com/git/git/commit/87f1b2d45ca7987cc6cc1a74eb66a77fa11fab94)

```text
The actual diffs output by range-diff respect diff_option.file, which
range-diff passes down the call-chain, thus are destination-agnostic.
However, output_pair_header() is hard-coded to emit to 'stdout'. Fix
this by making output_pair_header() respect diff_option.file, as well.
```

incoming: [N:1](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
In [ref] ("[referenced subject]", 2018-07-22) we broke passing down options like --no-patch,
--stat etc.
```

incoming: [N:2](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
Fix that regression, and add a test asserting the pre-[ref]
behavior for some of these diff options.
```

### 14b/raw/direct-full

The earlier decision P1 introduced changes to manage low-level configuration details within the range-diff backend, which inadvertently broke the passing of certain diff options like --no-patch and --stat. This regression necessitates a reevaluation of how these options are handled to restore their intended functionality.

previous: [P1:0](https://github.com/git/git/commit/73a834e9e27906a76940f1ced5c132bce205d3f8)

```text
range-diff: relieve callers of low-level configuration burden
```

previous: [P1:1](https://github.com/git/git/commit/73a834e9e27906a76940f1ced5c132bce205d3f8)

```text
There are a number of very low-level configuration details which need to
be managed precisely to generate a proper range-diff. In particular,
'diff_options' output format, header suppression, indentation, and
dual-color mode must all be set appropriately to ensure proper behavior.
```

previous: [P1:2](https://github.com/git/git/commit/73a834e9e27906a76940f1ced5c132bce205d3f8)

```text
Handle these details locally in the libified range-diff back-end rather
than forcing each caller to have specialized knowledge of these
implementation details, and to avoid duplication as new callers are
added.
```

incoming: [N:1](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
In 73a834e9e2 ("range-diff: relieve callers of low-level configuration
burden", 2018-07-22) we broke passing down options like --no-patch,
--stat etc.
```

incoming: [N:2](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
Fix that regression, and add a test asserting the pre-73a834e9e2
behavior for some of these diff options.
```

### 14b/raw/module

Reconsider the earlier decision “Handle these details locally in the libified range-diff back-end rather
than forcing each caller to have specialized knowledge of these
implementation details, and to avoid duplication as new callers are
added.”. The new report gives the following behavior and its conditions. “In 73a834e9e2 ("range-diff: relieve callers of low-level configuration
burden", 2018-07-22) we broke passing down options like --no-patch,
--stat etc.

Fix that regression, and add a test asserting the pre-73a834e9e2
behavior for some of these diff options.”

previous: [원문 구간](https://github.com/git/git/commit/73a834e9e27906a76940f1ced5c132bce205d3f8)

```text
Handle these details locally in the libified range-diff back-end rather
than forcing each caller to have specialized knowledge of these
implementation details, and to avoid duplication as new callers are
added.
```

incoming: [원문 구간](https://github.com/git/git/commit/4624185a67aa17104762a4bbff2b05727ef4cd83)

```text
In 73a834e9e2 ("range-diff: relieve callers of low-level configuration
burden", 2018-07-22) we broke passing down options like --no-patch,
--stat etc.

Fix that regression, and add a test asserting the pre-73a834e9e2
behavior for some of these diff options.
```

### 14b/hidden/module

the exact passages did not reproduce the document judgment
## reflog

[새 보고](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c) · [실제 이전 결정](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed) · [유사 결정](https://github.com/git/git/commit/c809798b2acf1afdeeea02a9175677590ad8d689)

The switch to lookup_commit makes null_oid yield non-NULL for an empty reflog, leading to an erroneous parse/error; preserve empty reflog handling.

| 조건 | 양성 판단 | 근거 판정 | 음성 판단 |
|---|---|---|---|
| 3b/raw/direct-full | keep | 실패: 보류 | keep |
| 3b/raw/module | reassess | 실패: lookup_commit 전환과 null_oid 또는 빈 reflog 조건이 빠져 있다. | keep |
| 14b/raw/direct-full | reassess | 성공: lookup_commit 전환이 null_oid에 non-NULL을 반환해 후속 오류를 일으키는 구체적 조건과 동작을 설명하고 parse_commit 원문으로 뒷받침한다. | keep |
| 14b/raw/module | reassess | 실패: 과거 근거가 최초 lookup_commit_reference_gently 사용 이력뿐이다. 재검토 대상인 lookup_commit으로의 전환 결정을 잘못 고른다. | keep |
| 3b/hidden/direct-full | keep | 실패: 보류 | keep |
| 3b/hidden/module | keep | 실패: 보류 | keep |
| 3b/hidden/direct-oracle | reassess | 실패: null_oid의 non-NULL 반환은 찾지만 없는 객체의 역참조 오류로 원인을 바꾸고 빈 reflog 조건도 설명하지 않는다. | keep |
| 14b/hidden/direct-full | reassess | 성공: lookup_commit 변경, null_oid에서 non-NULL 반환, parse_commit 오류의 인과를 정확히 연결한다. 실제 입력 조건 null_oid를 명시한다. | keep |
| 14b/hidden/module | reassess | 실패: 새 null_oid 회귀 구절은 맞지만 과거에는 최초 구현 이력만 골라 lookup_commit 전환 결정의 근거를 잃었다. | keep |
| 14b/hidden/direct-oracle | reassess | 실패: null_oid의 parse 오류는 찾았으나 NULL 객체를 오류 표시 후 계속 처리하는 정책의 가정이 깨졌다고 해석한다. 실제 원인은 null_oid가 non-NULL 객체로 바뀐 것이다. | keep |

### 3b/hidden/direct-full

The incoming report proposes to remove the error message for empty reflogs. This change does not directly relate to the earlier decisions regarding reflog expiration or handling missing objects. The earlier decisions were focused on improving robustness and handling corrupted repositories, while the incoming report addresses a specific issue related to error messages in reflogs. There is no direct connection between the incoming report and the conditions or failures mentioned in the earlier decisions.

### 3b/hidden/direct-oracle

The incoming report suggests that dereferencing commits in reflogs might lead to errors due to missing objects, which contradicts the original decision to change to a 'lookup commit' approach. The new evidence indicates that the current implementation returns non-NULL for null_oid(), leading to potential errors in the `mark_reachable` function.

previous: [P0:2](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
I don't think we've ever found tags that we need to recursively
dereference in reflogs, so this should at least be changed to a
"lookup commit" as I'm doing here, although I can't think of a way
where it mattered in practice.
```

previous: [P0:3](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
I also think we'd probably like to just die here if we have a NULL
object, but as this code needs to handle potentially broken
repositories let's just show an "error" but continue, the non-quiet
lookup_commit() will do for us. None of our tests cover the case where
"commit" is NULL after this lookup.
```

incoming: [N:1](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
Fix a regression in my [ref] ([referenced subject], 2021-12-22), in changing from
lookup_commit_reference_gently() to lookup_commit() we stopped trying
to call deref_tag() and parse_object() on the provided OID, but we
also started returning non-NULL for the null_oid().
```

incoming: [N:2](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.
```

### 3b/hidden/module

no unique decision in the document comparison

### 3b/raw/direct-full

The incoming report proposes changes to the behavior of `git reflog expire` to avoid emitting errors on empty reflogs. This change does not directly address the issues mentioned in the earlier decisions (`P0` and `P1`). The earlier decisions focused on handling missing objects and ensuring robustness in corrupt repositories, while the incoming report aims to fix a regression related to dereferencing tags in empty reflogs. There is no direct connection between the incoming report and the specific conditions addressed in the earlier decisions.

### 3b/raw/module

Reconsider the earlier decision “In the initial implementation of "git reflog" in 4264dc15e19 (git
reflog expire, 2006-12-19) we had this
lookup_commit_reference_gently().”. The new report gives the following behavior and its conditions. “As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.”

previous: [원문 구간](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
In the initial implementation of "git reflog" in 4264dc15e19 (git
reflog expire, 2006-12-19) we had this
lookup_commit_reference_gently().
```

incoming: [원문 구간](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.
```

### 14b/hidden/direct-full

The change from using lookup_commit_reference_gently() to lookup_commit() introduced a regression where non-NULL values were returned for null_oid(), leading to errors when attempting to parse_commit(). This issue was not anticipated in the original decision.

previous: [P0:2](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
I don't think we've ever found tags that we need to recursively
dereference in reflogs, so this should at least be changed to a
"lookup commit" as I'm doing here, although I can't think of a way
where it mattered in practice.
```

previous: [P0:3](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
I also think we'd probably like to just die here if we have a NULL
object, but as this code needs to handle potentially broken
repositories let's just show an "error" but continue, the non-quiet
lookup_commit() will do for us. None of our tests cover the case where
"commit" is NULL after this lookup.
```

incoming: [N:1](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
Fix a regression in my [ref] ([referenced subject], 2021-12-22), in changing from
lookup_commit_reference_gently() to lookup_commit() we stopped trying
to call deref_tag() and parse_object() on the provided OID, but we
also started returning non-NULL for the null_oid().
```

incoming: [N:2](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.
```

### 14b/hidden/direct-oracle

The change from using lookup_commit_reference_gently() to lookup_commit() introduced a regression where an error was emitted due to attempting to parse a null_oid(). This contradicts the assumption that handling NULL objects by showing an 'error' but continuing would not cause practical issues.

previous: [P0:2](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
I don't think we've ever found tags that we need to recursively
dereference in reflogs, so this should at least be changed to a
"lookup commit" as I'm doing here, although I can't think of a way
where it mattered in practice.
```

previous: [P0:3](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
I also think we'd probably like to just die here if we have a NULL
object, but as this code needs to handle potentially broken
repositories let's just show an "error" but continue, the non-quiet
lookup_commit() will do for us. None of our tests cover the case where
"commit" is NULL after this lookup.
```

incoming: [N:1](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
Fix a regression in my [ref] ([referenced subject], 2021-12-22), in changing from
lookup_commit_reference_gently() to lookup_commit() we stopped trying
to call deref_tag() and parse_object() on the provided OID, but we
also started returning non-NULL for the null_oid().
```

incoming: [N:2](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.
```

### 14b/hidden/module

Reconsider the earlier decision “In the initial implementation of "git reflog" in 4264dc15e19 (git
reflog expire, 2006-12-19) we had this
lookup_commit_reference_gently().”. The new report gives the following behavior and its conditions. “Fix a regression in my [ref] ([referenced subject], 2021-12-22), in changing from
lookup_commit_reference_gently() to lookup_commit() we stopped trying
to call deref_tag() and parse_object() on the provided OID, but we
also started returning non-NULL for the null_oid().

As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.”

previous: [원문 구간](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
In the initial implementation of "git reflog" in 4264dc15e19 (git
reflog expire, 2006-12-19) we had this
lookup_commit_reference_gently().
```

incoming: [원문 구간](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
Fix a regression in my [ref] ([referenced subject], 2021-12-22), in changing from
lookup_commit_reference_gently() to lookup_commit() we stopped trying
to call deref_tag() and parse_object() on the provided OID, but we
also started returning non-NULL for the null_oid().

As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.
```

### 14b/raw/direct-full

The change from using `lookup_commit_reference_gently()` to `lookup_commit()` introduced a regression where non-NULL values were returned for `null_oid()`, leading to errors during subsequent operations.

previous: [P1:2](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
I don't think we've ever found tags that we need to recursively
dereference in reflogs, so this should at least be changed to a
"lookup commit" as I'm doing here, although I can't think of a way
where it mattered in practice.
```

previous: [P1:3](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
I also think we'd probably like to just die here if we have a NULL
object, but as this code needs to handle potentially broken
repositories let's just show an "error" but continue, the non-quiet
lookup_commit() will do for us. None of our tests cover the case where
"commit" is NULL after this lookup.
```

incoming: [N:1](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
Fix a regression in my daf1d8285ee (reflog expire: don't use
lookup_commit_reference_gently(), 2021-12-22), in changing from
lookup_commit_reference_gently() to lookup_commit() we stopped trying
to call deref_tag() and parse_object() on the provided OID, but we
also started returning non-NULL for the null_oid().
```

incoming: [N:2](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.
```

### 14b/raw/module

Reconsider the earlier decision “In the initial implementation of "git reflog" in 4264dc15e19 (git
reflog expire, 2006-12-19) we had this
lookup_commit_reference_gently().”. The new report gives the following behavior and its conditions. “Fix a regression in my daf1d8285ee (reflog expire: don't use
lookup_commit_reference_gently(), 2021-12-22), in changing from
lookup_commit_reference_gently() to lookup_commit() we stopped trying
to call deref_tag() and parse_object() on the provided OID, but we
also started returning non-NULL for the null_oid().

As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.”

previous: [원문 구간](https://github.com/git/git/commit/daf1d8285eeb44eeb8be92b7b01706e887f718ed)

```text
In the initial implementation of "git reflog" in 4264dc15e19 (git
reflog expire, 2006-12-19) we had this
lookup_commit_reference_gently().
```

incoming: [원문 구간](https://github.com/git/git/commit/57be9c6deeb1be7c3ce6270df52473eddc09a86c)

```text
Fix a regression in my daf1d8285ee (reflog expire: don't use
lookup_commit_reference_gently(), 2021-12-22), in changing from
lookup_commit_reference_gently() to lookup_commit() we stopped trying
to call deref_tag() and parse_object() on the provided OID, but we
also started returning non-NULL for the null_oid().

As a result we'd emit an error() via mark_reachable() later in this
function as we tried to invoke parse_commit() on it.
```
