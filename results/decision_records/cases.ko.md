# 사건별 판단과 원문 인용

각 원문의 발췌 번호는 해당 입력 안에서 고정했다. 아래는 실제 인용 구절의 시작 부분이며, 전체 구절과 모델 원출력은 [outcomes.json](outcomes.json)에 있다. A는 원문, B는 AI 메모 추가, C는 당시 유지보수자 메모 추가다.

## historical-01 · historical

The small-field design drops or repeatedly reads large deltas, hurting pack size or time for that workload.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | review or keep | The incoming record introduces changes to the behavior of handling small files and large deltas in the context of pack-objects. While the old records discuss general practices and optimizations, the new record specifically addresses performance improvements and fixes related to large deltas. These changes suggest a need to reassess the handling of large deltas, which might affect the reliability and efficiency of previous decisions regarding small files. Therefore, the incoming record warrants a review to ensure compatibility and correctness. |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record introduces a new approach to handling large deltas during the packing process, which could lead to improved performance and reduced memory usage compared to the previous method. However, the change involves a significant adjustment in how large deltas are managed, which might affect the reliability and consistency of the system. Therefore, further review is necessary to ensure that the new approach does not introduce unforeseen issues. | [O1.1.1](https://github.com/git/git/commit/ba41a8b600871b68680ff33de08012f4887133a2) “packed_ref_cache: don't use mmap() for small files”<br>[N.1.1](https://github.com/git/git/commit/9ac3f0e5b3e4cebe5bc9a24e3adef8b8e64fe692) “pack-objects: fix performance issues on packing large deltas” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record introduces a new approach to handling small packed-refs files by using read() instead of mmap(), addressing the issue mentioned in the old record. However, the old record suggests avoiding mmap() for small files, which is still relevant and necessary to ensure that munmap() operations do not fail. Therefore, the old record remains true, warranting a review of the new approach. | [O1.1.1](https://github.com/git/git/commit/ba41a8b600871b68680ff33de08012f4887133a2) “packed_ref_cache: don't use mmap() for small files”<br>[N.1.1](https://github.com/git/git/commit/9ac3f0e5b3e4cebe5bc9a24e3adef8b8e64fe692) “pack-objects: fix performance issues on packing large deltas” | 출력·인용 형식 오류 |

## historical-02 · historical

The corrected multi-pack-index offset encoding is separate from the in-memory delta-size choice.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | keep | The incoming changes pertain to a different aspect of Git operations (multi-pack-index description correction) and do not contradict or necessitate a review of the previous decisions regarding packed-ref cache handling or struct object_entry optimizations. The old passages focus on improving memory efficiency and performance, while the new ones address a minor bug in the multi-pack-index description. These changes do not overlap significantly enough to warrant a review of the older decisions. |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record introduces a new issue regarding the multi-pack-index description, which is different from the previous records focused on file handling and struct optimization. While the context of file handling might have some overlap, the specific problem described in N.1.1 pertains to a different aspect of Git operations. | [O1.1.1](https://github.com/git/git/commit/ba41a8b600871b68680ff33de08012f4887133a2) “packed_ref_cache: don't use mmap() for small files”<br>[N.1.1](https://github.com/git/git/commit/eb31044ff793de9a8a093f567f5eb262ac196c24) “pack-format: correct multi-pack-index description” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record introduces a new issue regarding the multi-pack-index description, which is different from the previous records focused on packed-ref handling. However, the context suggests that both sets of changes aim to improve git operations' efficiency and correctness. The new record introduces a bug fix that affects the multi-pack-index description, which could indirectly impact the performance and correctness of git operations, especially when dealing with large repositories. Therefore, it warrants further investigation to ensure that the fix does not introduce unintended side effects. | [O1.1.1](https://github.com/git/git/commit/ba41a8b600871b68680ff33de08012f4887133a2) “packed_ref_cache: don't use mmap() for small files”<br>[N.1.1](https://github.com/git/git/commit/eb31044ff793de9a8a093f567f5eb262ac196c24) “pack-format: correct multi-pack-index description” | 출력·인용 형식 오류 |

## historical-03 · historical

Generation-first ordering can increase walk count or time on certain topologies, contrary to the old claim.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record introduces a significant change in the order of commits processed by paint_down_to_common(), which affects the number of commits walked. This change impacts the performance and correctness of the function, especially in certain topological scenarios. The old passage (O1.1.4) incorrectly states that the change does not affect the number of commits walked, which is contradicted by the new record (N.1.5) showing a substantial increase in the number of iterations due to the altered order. Therefore, the incoming record warrants reviewing the impact of this change. | [O1.1.4](https://github.com/git/git/commit/3afc679b3c13d99e4f02bceb686f11d51576d3ae) “This change does not affect the number of commits that are walked during the execution of paint_down_to_common(), only the or”<br>[N.1.5](https://github.com/git/git/commit/091f4cf3586957c3fd99d4c4c59c569d009137ad) “The commit message for 3afc679b includes the following sentence:” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record introduces a significant change in the order of commits being inspected by paint_down_to_common(). This change affects the number of commits that are walked during the execution of the function, contrary to the original commit message. The new commit suggests avoiding the use of generation numbers if not needed, which directly impacts the performance and correctness of the function. | [O1.1.1](https://github.com/git/git/commit/3afc679b3c13d99e4f02bceb686f11d51576d3ae) “commit: use generations in paint_down_to_common()”<br>[N.1.1](https://github.com/git/git/commit/091f4cf3586957c3fd99d4c4c59c569d009137ad) “commit: don't use generation numbers if not needed” | 출력·인용 형식 오류 |

## historical-04 · historical

Hyphenation of the file name does not affect ordering or the walk.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | keep | The incoming changes are about documentation and do not affect the functionality or performance improvements described in the older passages. The references to the 'commit-graph file' are being corrected while maintaining the existing behavior regarding the commit graph. |  | 출력·인용 형식 오류 |
| B | ✓ | keep | The incoming record does not introduce any changes that necessitate reviewing or altering the existing decisions. Martin Ågren's changes are purely about documentation, specifically fixing references to the 'commit-graph file' to include the dash. This does not impact the functionality or performance improvements discussed in the older records. | [O1.2.5](https://github.com/git/git/commit/d7c1ec3efd0092ee665085cba4e8a2bcef95143b) “For a copy of the Linux repository, where HEAD is checked out at v4.13~100, we get the following performance improvement for ”<br>[N.1.2](https://github.com/git/git/commit/4c399442f781f70a00273746ca6a0de9fef9b0d3) “The file processed by `git commit-graph` is referred to as the "commit-graph file", also with a dash. We have a few reference” | 기존 성능 변경과 문서 표기 수정이 별개임을 두 원문에서 확인. |
| C | ✓ | keep | The incoming record does not introduce any changes that would necessitate reviewing or altering the existing decisions regarding the use of generations in paint_down_to_common(). The proposed change in the incoming record is about documentation, specifically fixing references to the 'commit-graph file' with a dash, which does not conflict with or require revisiting the existing code changes. | [O1.1.1](https://github.com/git/git/commit/3afc679b3c13d99e4f02bceb686f11d51576d3ae) “commit: use generations in paint_down_to_common()”<br>[N.1.1](https://github.com/git/git/commit/4c399442f781f70a00273746ca6a0de9fef9b0d3) “Doc: refer to the "commit-graph file" with dash” | generation 사용과 문서 하이픈을 서로 다른 수정으로 구분. |

## historical-05 · historical

safecrlf=false should suppress round-trip errors but the flag conversion can emit a warning.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record introduces a regression that affects the behavior of the 'safecrlf' setting, specifically causing a warning message to be produced despite it being set to 'false'. This suggests a change in behavior that may require further investigation or adjustment of the previous decision regarding 'safecrlf'. | [O1.1.1](https://github.com/git/git/commit/8462ff43e42ab67cecd16fdfb59451a53cc8a945) “convert_to_git(): safe_crlf/checksafe becomes int conv_flags”<br>[N.1.1](https://github.com/git/git/commit/6cb09125bea69d9bdb461b8ecacd5c50c9e6a4f5) “config.c: fix regression for core.safecrlf false” | 출력·인용 형식 오류 |

## historical-06 · historical

Grammar or style in userdiff leaves the line-ending flags and behavior untouched.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | keep | The incoming record 'N.1.1' discusses fixing grammar and style issues in userdiff, which is unrelated to the previous decisions made about test automation and EOL handling in the Makefile. These changes do not necessitate reviewing or altering the existing decisions regarding test re-running and EOL handling practices. | [O1.1.1](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “t/Makefile: add a rule to re-run previously-failed tests”<br>[N.1.1](https://github.com/git/git/commit/2731a7840a462a97b8afb5beadaf36c1db992ac7) “userdiff: fix grammar and style issues” | 조치 또는 인용 대상이 정답과 다름 |
| B | ✗ | keep | The incoming record 'userdiff: fix grammar and style issues' does not introduce any changes related to test re-running or conditions testing. It focuses on improving the grammar and style of the userdiff function, which is unrelated to the context of re-running previously failed tests discussed in the old records. | [O1.1.1](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “t/Makefile: add a rule to re-run previously-failed tests”<br>[N.1.1](https://github.com/git/git/commit/2731a7840a462a97b8afb5beadaf36c1db992ac7) “userdiff: fix grammar and style issues” | 조치 또는 인용 대상이 정답과 다름 |
| C | ✗ | keep | The incoming record 'userdiff: fix grammar and style issues' by Boxuan Li does not introduce any changes related to test re-running or conditions. It focuses on improving the userdiff script's grammar and style. The previous records discuss how 'make -C t failed' runs only the tests that failed in the previous run, which is unrelated to the incoming record. | [O1.1.1](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “t/Makefile: add a rule to re-run previously-failed tests”<br>[N.1.1](https://github.com/git/git/commit/2731a7840a462a97b8afb5beadaf36c1db992ac7) “userdiff: fix grammar and style issues” | 조치 또는 인용 대상이 정답과 다름 |

## historical-07 · historical

Moving fixup/squash counting away from localized text caused an off-by-one in displayed message numbers.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | review or keep | The incoming record introduces a regression in the labeling of commit messages when squashing commits together, which was fixed by the patch. This change impacts the functionality of the rebase -i command, warranting a review to ensure the fix does not introduce new issues. |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record introduces a new feature ('current-fixups' file) that improves the handling of rebase operations, specifically addressing a regression in commit message numbering and cleanup. This change is significant enough to warrant reviewing the previous decision to adopt Johannes Schindelin's patch for re-running previously failed tests, as the new feature impacts the overall rebase process and commit message management. The old passage supports the initial decision to adopt the patch for test re-execution, while the new passage highlights the necessity of reviewing the rebase-related changes due to their impact on commit message handling. |  | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record introduces a fix for a regression in commit messages when squashing commits, which aligns with the previous record indicating improvements in handling test failures. The new record specifically addresses a regression introduced by the previous patch, suggesting a need to review the impact of this change on the overall functionality. | [O1.1.1](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “t/Makefile: add a rule to re-run previously-failed tests”<br>[N.1.1](https://github.com/git/git/commit/dd2e36ebaccd6dc2ca4d37759248ce9bbdf9113e) “rebase -i: fix numbering in squash message” | 출력·인용 형식 오류 |

## historical-08 · historical

Wording about rebase-merges preserves its meaning and has no bearing on squash-message numbering.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | keep | The incoming record does not introduce a change related to the functionality described in the old passages. The new record pertains to improving documentation, which is unrelated to the automated test re-running and rebase handling functionalities mentioned in the old passages. | [N.1.1](https://github.com/git/git/commit/d3a8caebf38b42d8d8ca80cb1856ee2e54fb4c4d) “doc: improve readability of --rebase-merges in git-rebase” | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record does not directly relate to the functionality of re-running previously failed tests or handling rebase issues. The proposed change in Naveen Nathan's record aims to improve the documentation and clarity around the usage of `--rebase-merges` and `--preserve-merges`. These changes do not warrant reopening or testing the previous decisions regarding test re-running and rebase handling. |  | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record does not introduce a change related to re-running previously failed tests or managing test results. The old record mentions adding a rule to re-run previously-failed tests, which is different from improving the documentation of the `--rebase-merges` option in the `git-rebase` command. Therefore, the incoming record does not warrant reopening the past decision or testing it under a changed condition. | [O1.1.1](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “t/Makefile: add a rule to re-run previously-failed tests”<br>[N.1.1](https://github.com/git/git/commit/d3a8caebf38b42d8d8ca80cb1856ee2e54fb4c4d) “doc: improve readability of --rebase-merges in git-rebase” | 출력·인용 형식 오류 |

## prior_git-01 · prior_git

The candidate limit still gives incorrect distance with disjoint roots.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record introduces a new scenario where the current stopping condition might prematurely abort the search, leading to incorrect results. This is highlighted by Jeff King's example in N.1.3, where the test fails due to early termination. Therefore, the old decision to modify the stopping condition to ensure accuracy in multi-branch scenarios needs to be reviewed to account for the new edge case introduced. | [O1.1.7](https://github.com/git/git/commit/30b1c7ad9d64695a65c23f922e6ffd2fd35660da) “Thus, this commit modifies the stopping condition to only abort the search when only one branch is left to search *and* all c”<br>[N.1.5](https://github.com/git/git/commit/d0e52c1728bdab27f7ca61ee0d4ff91055646bae) “So I'm punting on that for now, but I'd like to adjust the tests to be more resilient, and to document the findings. So this ” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record mentions a weakness in the disjoint-root handling of git-describe, specifically that it might stop too early when searching for the best tag to describe a commit. This suggests a potential issue that needs further investigation, hence warranting a review. | [O1.1.1](https://github.com/git/git/commit/30b1c7ad9d64695a65c23f922e6ffd2fd35660da) “describe: don't abort too early when searching tags”<br>[N.1.1](https://github.com/git/git/commit/d0e52c1728bdab27f7ca61ee0d4ff91055646bae) “t6120: demonstrate weakness in disjoint-root handling” | 출력·인용 형식 오류 |

## prior_git-02 · prior_git

A nonlocal transport can be mistaken for a local clone despite the URL test.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record introduces a new scenario where Git might incorrectly identify a local URL due to a symbolic link in a submodule. This could lead to unintended local cloning, which contradicts the original intention of identifying local URLs. Therefore, the old decision to avoid parsing .gitmodules during merge conflicts may need reconsideration in light of the new vulnerability introduced by the symbolic link in the submodule. | [O1.1.1](https://github.com/git/git/commit/d4e98b581b5b3b70ca58cb6677ec02bee4ae7007) “Submodules: Don't parse .gitmodules when it contains, merge conflicts”<br>[N.1.1](https://github.com/git/git/commit/58325b93c5b6212697b088371809e9948fee8052) “t5619: demonstrate clone_local() with ambiguous transport” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record introduces a new scenario regarding the handling of URLs in cloning operations, which could potentially lead to misinterpretation of local vs. remote repositories. This new information suggests a need to reassess the conditions under which the `clone_local()` optimization is applied, especially in cases where URLs might be misleading. The old passage focuses on parsing conflicts in `.gitmodules`, which is unrelated to the new issue of URL manipulation during cloning. | [O1.1.1](https://github.com/git/git/commit/d4e98b581b5b3b70ca58cb6677ec02bee4ae7007) “Submodules: Don't parse .gitmodules when it contains, merge conflicts”<br>[N.1.1](https://github.com/git/git/commit/58325b93c5b6212697b088371809e9948fee8052) “t5619: demonstrate clone_local() with ambiguous transport” | 출력·인용 형식 오류 |

## prior_git-03 · prior_git

Freeing the containing buffer can double-free it with word-diff and color-moved together.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record introduces a new issue related to the `git-describe` command's stopping condition, specifically mentioning a regression in the `show --word-diff --color-moved` functionality. This suggests that the previous decision to modify the stopping condition might not fully address all edge cases, particularly those involving multi-branch scenarios where tags are found across independent branches. Therefore, further investigation is warranted to ensure the accuracy and reliability of tag identification. | [O1.1.7](https://github.com/git/git/commit/30b1c7ad9d64695a65c23f922e6ffd2fd35660da) “Thus, this commit modifies the stopping condition to only abort the search when only one branch is left to search *and* all c”<br>[N.1.2](https://github.com/git/git/commit/b59ec03cb5f69d6a87dce8fc3ccbfd22d8de3c16) “Add a failing test which demonstrates a regression in a18d66cefb ("diff.c: free "buf" in diff_words_flush()", 2022-03-04), th” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record introduces a new issue with the `git-describe` command where it may prematurely terminate the search for tag candidates, leading to incorrect tag descriptions. This issue is demonstrated through a test case showing a memory leak regression introduced in a previous commit. The old passage does not address this specific problem, hence the need to review the behavior of `git-describe` in multi-root commit scenarios. | [O1.1.6](https://github.com/git/git/commit/30b1c7ad9d64695a65c23f922e6ffd2fd35660da) “The help text of `git-describe` states pretty clearly that when describing a commit D, the number appended to the emitted tag”<br>[N.1.2](https://github.com/git/git/commit/b59ec03cb5f69d6a87dce8fc3ccbfd22d8de3c16) “Add a failing test which demonstrates a regression in a18d66cefb ("diff.c: free "buf" in diff_words_flush()", 2022-03-04), th” | 출력·인용 형식 오류 |

## scope-01 · controlled

Re-test prove on the newly stable Windows Perl configuration. The old MSYS2 crashes remain valid.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record suggests a successful implementation of the previous decision to avoid parsing .gitmodules during merge conflicts, leading to improved usability and reduced crash frequency on Windows builds. This indicates that while the initial decision was correct, its implementation may need further refinement based on new performance data. | [O1.1.1](https://github.com/git/git/commit/d4e98b581b5b3b70ca58cb6677ec02bee4ae7007) “Submodules: Don't parse .gitmodules when it contains, merge conflicts”<br>N.1.1 “Our Windows build with a native Perl and the required Subversion bindings completed 200 massively parallel prove runs with no” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record suggests that the Windows build with a native Perl and Subversion bindings completed 200 massively parallel prove runs without crashes, indicating that the previous issue with crashes due to the use of `prove` tool may have been resolved. However, the old record mentions that `prove` tool requires Perl, which could lead to crashes under stress conditions, especially when running massively-parallel tests. Therefore, while the crash issue seems to be resolved, the context of the new information is still relevant to ensure that the changes made do not introduce other unforeseen issues. | [O1.1.1](https://github.com/git/git/commit/d4e98b581b5b3b70ca58cb6677ec02bee4ae7007) “Submodules: Don't parse .gitmodules when it contains, merge conflicts”<br>N.1.1 “Our Windows build with a native Perl and the required Subversion bindings completed 200 massively parallel prove runs with no” | 출력·인용 형식 오류 |

## scope-02 · controlled

Linux success does not remove the Windows compatibility and crash reason.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record mentions successful completion of 200 massively parallel prove runs with no crashes on Linux native Perl workers, but unexplained crashes on Windows MSYS2. This suggests that the current decision to avoid parsing .gitmodules during merge conflicts may need reconsideration due to the recurring crashes on Windows. The old passage supports the initial decision to improve usability by avoiding command failures, while the new passage indicates potential issues with the current approach. | [O1.1.1](https://github.com/git/git/commit/d4e98b581b5b3b70ca58cb6677ec02bee4ae7007) “Submodules: Don't parse .gitmodules when it contains, merge conflicts”<br>N.1.1 “The Linux native Perl workers completed 200 massively parallel prove runs with no crashes. On the Windows MSYS2 pool the same” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record mentions successful completion of 200 massively parallel prove runs with no crashes on the Linux native Perl workers, but unexplained crashes continued on the Windows MSYS2 pool. This suggests that the issue may have been resolved on Linux but remains unresolved on Windows, warranting further investigation. | [O1.1.1](https://github.com/git/git/commit/d4e98b581b5b3b70ca58cb6677ec02bee4ae7007) “Submodules: Don't parse .gitmodules when it contains, merge conflicts”<br>N.1.1 “The Linux native Perl workers completed 200 massively parallel prove runs with no crashes. On the Windows MSYS2 pool the same” | 출력·인용 형식 오류 |

## scope-03 · controlled

Re-test mmap for small nonempty files on the new kernel while keeping the empty-file exception.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record introduces a scenario where zero-length packed-refs files cause issues with `mmap()`, contrary to the previous evidence that `mmap()` was faster than `read()` for non-empty files. This suggests a need to revisit the decision to automate the re-running of previously failed tests, as the current approach may not be reliable for all cases, including zero-length files. | [O1.1.5](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “It is the most convenient way to determine which tests failed after running the entire test suite, in parallel, to look for l”<br>N.1.1 “On the new kernel we benchmarked nonempty 2 KiB packed-refs files. mmap was faster than read in all ten runs. Zero-length fil” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record introduces a scenario where zero-length files cause issues with `mmap`. This suggests that the previous approach of running only the tests that failed in the previous run might not be sufficient for handling all edge cases, including zero-length files. Therefore, it may warrant reviewing the decision to ensure that such cases are properly handled. | [O1.1.1](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “t/Makefile: add a rule to re-run previously-failed tests”<br>N.1.1 “On the new kernel we benchmarked nonempty 2 KiB packed-refs files. mmap was faster than read in all ten runs. Zero-length fil” | 출력·인용 형식 오류 |

## scope-04 · controlled

Large-file results do not overturn the small- or empty-file policy.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record suggests that on new hardware configurations, mmap outperforms read for large packed-refs files, contradicting the previous evidence that read was more efficient. This change indicates a need to reassess the necessity of the previous decision to re-run tests automatically, as the performance characteristics have shifted. | [O1.1.5](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “It is the most convenient way to determine which tests failed after running the entire test suite, in parallel, to look for l”<br>N.1.1 “On the new kernel mmap beat read in all ten runs on 128 MiB packed-refs files. For nonempty 2 KiB files read still won. Zero-” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record suggests that `make -C t` now only runs the tests that failed in the previous run, which aligns with the functionality described in the old record. However, the new record introduces a performance difference between `mmap` and `read` for certain file sizes, indicating a potential need to revisit the strategy of running only failed tests to ensure optimal performance across different scenarios. | [O1.1.1](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “t/Makefile: add a rule to re-run previously-failed tests”<br>N.1.1 “On the new kernel mmap beat read in all ten runs on 128 MiB packed-refs files. For nonempty 2 KiB files read still won. Zero-” | 출력·인용 형식 오류 |

## scope-05 · controlled

Test the graft-aware prototype separately. The original incompatibility of the shipping graph still holds.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record mentions a prototype that uses graft tables, which contradicts the assumption made in the old records about the absence of grafts. While the performance improvement was observed without grafts, the presence of grafts in the prototype suggests that the current implementation might need to handle them differently. Therefore, the decision to keep the changes should be reconsidered. | [O1.2.6](https://github.com/git/git/commit/d7c1ec3efd0092ee665085cba4e8a2bcef95143b) “Before: 0.21s After: 0.13s Rel %: -38%”<br>N.1.1 “We tested a prototype that keys the graph by the active graft table. On the grafted repository all 800 ancestry queries match” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record mentions a prototype that keys the graph by the active graft table, leading to faster ancestry queries on a grafted repository. This suggests that the compatibility issue noted in the old record might not apply in all scenarios, especially when grafts are involved. Therefore, the old record should be reviewed to ensure it still holds relevance. | [O2.2.2](https://github.com/git/git/commit/d6538246d3d4edbfbc9b0af6a2aa38552d35f7f1) “Create new method commit_graph_compatible(r) to check if a given repository r is compatible with the commit-graph feature. Fi”<br>N.1.1 “We tested a prototype that keys the graph by the active graft table. On the grafted repository all 800 ancestry queries match” | 출력·인용 형식 오류 |

## scope-06 · controlled

Ungrafted speed does not remove the correctness problem with active grafts.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | review or keep | The incoming record indicates that the presence of grafts affects the accuracy of ancestry queries, contrary to the expectation based on the old records. This suggests a need to either review the old decisions to ensure they still hold true in the presence of grafts, or test the old methods under conditions with grafts to confirm their reliability. | N.1.1 “On the repository without grafts all 800 ancestry queries matched a raw walk and were faster. With active grafts the prototyp” | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record indicates that repositories with commit grafts still use the original parent links and return incorrect ancestors, suggesting that the current decision to make commit_graph_compatible(r) return false for repositories with commit grafts might need reconsideration. The old passage supports the initial decision, but the new passage provides evidence that the current implementation may not fully address the issue. | [O1.1.1](https://github.com/git/git/commit/20fd6d57996e33c30b6bb030329523d0116f15ec) “commit-graph: not compatible with grafts”<br>N.1.1 “On the repository without grafts all 800 ancestry queries matched a raw walk and were faster. With active grafts the prototyp” | 출력·인용 형식 오류 |
| C | ✗ | review or keep | The incoming record indicates that the presence of grafts in the repository causes incorrect ancestor resolution, which was previously assumed to work correctly. This suggests that the compatibility issue identified in the old record may need to be revisited, especially since the new record highlights a failure scenario that wasn't covered in the initial analysis. | [O1.1.1](https://github.com/git/git/commit/20fd6d57996e33c30b6bb030329523d0116f15ec) “commit-graph: not compatible with grafts”<br>N.1.1 “On the repository without grafts all 800 ancestry queries matched a raw walk and were faster. With active grafts the prototyp” | 출력·인용 형식 오류 |

## aimers · prior_aimers

Compare clean-room TM-S with the current blend under the new setup. The old official TabM result remains valid.

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | invalid |  |  | 출력·인용 형식 오류 |
| B | ✗ | review or keep | The incoming record introduces new performance data comparing the existing models with the TM-S model, showing significant improvements in certain metrics like SEL and CONF scores. This suggests that the TM-S model may be more effective than previously thought, warranting further investigation to determine if the previous decision should be reconsidered. | [O1.1.1](https://github.com/ashcircle03/Aimers9th-KHU-swcon22/blob/a8e64a1d52a0daa1ee7bf4595a0dfe4e6acf49a3/jaewon/notes/findings.md#L484-L503) “## 18. TabM / inner-val 기준 — 둘 다 기각, 그런데 구조가 하나 보인다 (2026-08-11)”<br>[N.1.5](https://github.com/ashcircle03/Aimers9th-KHU-swcon22/blob/9bf532cde00494dabb86076e16a07940a47400e3/seonghun/docs/experiment_log.md#L377-L403) “- CPU CB4 + TM-S 50:50: SEL 1017.138 / CONF 697.487 - GPU CB4 + TM-S 50:50: SEL 1016.392 / CONF 694.240 - 기존 global CB+FT에 TM” | 출력·인용 형식 오류 |

## q01 · retention

What window size does Git's aggressive garbage collection use by default for delta compression?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | 250 |  | [O1.1.1](https://github.com/git/git/commit/ba41a8b600871b68680ff33de08012f4887133a2) “packed_ref_cache: don't use mmap() for small files” | 조치 또는 인용 대상이 정답과 다름 |
| B | ✓ | 250 |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/gc.adoc#L10-L18) “gc.aggressiveWindow:: The window size parameter used in the delta compression algorithm used by 'git gc --aggressive'. This d” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | 250 |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/gc.adoc#L10-L18) “gc.aggressiveWindow:: The window size parameter used in the delta compression algorithm used by 'git gc --aggressive'. This d” | 답과 인용한 구절의 의미가 모두 일치함. |

## q02 · retention

Which help format is the default for Git's help viewer?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | man |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/help.adoc#L5-L9) “help.format:: Override the default help format used by linkgit:git-help[1]. Values 'man', 'info', 'web' and 'html' are suppor” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | man |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/help.adoc#L5-L9) “help.format:: Override the default help format used by linkgit:git-help[1]. Values 'man', 'info', 'web' and 'html' are suppor” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | man |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/help.adoc#L5-L9) “help.format:: Override the default help format used by linkgit:git-help[1]. Values 'man', 'info', 'web' and 'html' are suppor” | 답과 인용한 구절의 의미가 모두 일치함. |

## q03 · retention

What credential-store lock timeout value means to retry indefinitely?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | -1 |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/credential.adoc#L51-L55) “credentialStore.lockTimeoutMS:: The length of time, in milliseconds, for git-credential-store to retry when trying to lock th” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | -1 |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/credential.adoc#L51-L55) “credentialStore.lockTimeoutMS:: The length of time, in milliseconds, for git-credential-store to retry when trying to lock th” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | -1 |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/credential.adoc#L51-L55) “credentialStore.lockTimeoutMS:: The length of time, in milliseconds, for git-credential-store to retry when trying to lock th” | 답과 인용한 구절의 의미가 모두 일치함. |

## q04 · retention

Which style does Git use by default for printing fetch ref update status?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | compact |  | [O1.1.4](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “It is particularly important to reduce the turn-around time thusly on Windows, where the test suite spends 45 minutes on the ” | 조치 또는 인용 대상이 정답과 다름 |
| B | ✓ | full |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/fetch.adoc#L59-L63) “fetch.output:: Control how ref update status is printed. Valid values are `full` and `compact`. Default value is `full`. See ” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✗ | compact |  | [O1.1.1](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “t/Makefile: add a rule to re-run previously-failed tests” | 조치 또는 인용 대상이 정답과 다름 |

## q05 · retention

Which alternate merge conflict style removes matching lines near either edge of the conflict region?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | zdiff3 |  | [O1.2.1](https://github.com/git/git/commit/01caf20d57aea73e67337ba1d396dd80a76d9dc3) “load_contents(): don't try to mmap an empty file” | 조치 또는 인용 대상이 정답과 다름 |
| B | ✓ | "zdiff3" |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/merge.adoc#L1-L15) “merge.conflictStyle:: Specify the style in which conflicted hunks are written out to working tree files upon merge. The defau” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✗ | zdiff3 |  |  | 출력·인용 형식 오류 |

## q06 · retention

What default subject prefix does format-patch put on its output?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | [PATCH] |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/format.adoc#L40-L43) “format.subjectPrefix:: The default for format-patch is to output files with the '[PATCH]' subject prefix. Use this variable t” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | [PATCH] |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/format.adoc#L40-L43) “format.subjectPrefix:: The default for format-patch is to output files with the '[PATCH]' subject prefix. Use this variable t” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | [PATCH] |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/format.adoc#L40-L43) “format.subjectPrefix:: The default for format-patch is to output files with the '[PATCH]' subject prefix. Use this variable t” | 답과 인용한 구절의 의미가 모두 일치함. |

## q07 · retention

If nobody specifies a notes merge strategy, which strategy resolves notes conflicts by default?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | manual |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/notes.adoc#L1-L9) “`notes.mergeStrategy`:: Which merge strategy to choose by default when resolving notes conflicts. Must be one of `manual`, `o” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | manual |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/notes.adoc#L1-L9) “`notes.mergeStrategy`:: Which merge strategy to choose by default when resolving notes conflicts. Must be one of `manual`, `o” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | manual |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/notes.adoc#L1-L9) “`notes.mergeStrategy`:: Which merge strategy to choose by default when resolving notes conflicts. Must be one of `manual`, `o” | 답과 인용한 구절의 의미가 모두 일치함. |

## q08 · retention

Which Git configuration option chooses between basic and extended when grep.patternType is set to default?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | grep.extendedRegexp |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/grep.adoc#L7-L13) “grep.patternType:: Set the default matching behavior. Using a value of 'basic', 'extended', 'fixed', or 'perl' will enable th” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | grep.extendedRegexp |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/grep.adoc#L7-L13) “grep.patternType:: Set the default matching behavior. Using a value of 'basic', 'extended', 'fixed', or 'perl' will enable th” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✗ | grep.patternType::default |  | [E.2.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/grep.adoc#L7-L13) “grep.patternType:: Set the default matching behavior. Using a value of 'basic', 'extended', 'fixed', or 'perl' will enable th” | default로 결정할 때 참조하는 설정 이름을 잘못 답함. |

## q09 · retention

What is the maximum permitted value for Git's pack.depth setting?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | 4095 |  |  | 출력·인용 형식 오류 |
| B | ✓ | 4095 |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/pack.adoc#L5-L9) “pack.depth:: The maximum delta depth used by linkgit:git-pack-objects[1] when no maximum depth is given on the command line. ” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | 4095 |  | [E.1.1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/pack.adoc#L5-L9) “pack.depth:: The maximum delta depth used by linkgit:git-pack-objects[1] when no maximum depth is given on the command line. ” | 답과 인용한 구절의 의미가 모두 일치함. |

## q10 · retention

Which command-line option overrides the configured number of diff context lines?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | -U |  | [O2.2.2](https://github.com/git/git/commit/01caf20d57aea73e67337ba1d396dd80a76d9dc3) “We don't actually create zero-length `packed-refs` files, but they are valid and we should handle them correctly. The old cod” | 조치 또는 인용 대상이 정답과 다름 |
| B | ✗ | -U |  |  | 출력·인용 형식 오류 |
| C | ✗ | -U |  | [O2.2.2](https://github.com/git/git/commit/01caf20d57aea73e67337ba1d396dd80a76d9dc3) “We don't actually create zero-length `packed-refs` files, but they are valid and we should handle them correctly. The old cod” | 조치 또는 인용 대상이 정답과 다름 |

## pep-680 · retention

Which standard library module provides the TOML parser for Python packaging tools?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | tomllib |  | [E.2.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0680.rst) “.. canonical-doc:: :mod:`python:tomllib`” | 인용 한 줄은 표준 문서 모듈명을 가리키지만 TOML 파서를 제공한다는 설명이 없음. |
| B | ✗ | tomllib |  | [E.2.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0680.rst) “.. canonical-doc:: :mod:`python:tomllib`” | 인용 한 줄은 표준 문서 모듈명을 가리키지만 TOML 파서를 제공한다는 설명이 없음. |
| C | ✗ | tomllib |  | [E.2.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0680.rst) “.. canonical-doc:: :mod:`python:tomllib`” | 인용 한 줄은 표준 문서 모듈명을 가리키지만 TOML 파서를 제공한다는 설명이 없음. |

## pep-615 · retention

If system time zone data is unavailable, which PyPI package supplies the fallback for zoneinfo?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | tzdata |  | [E.1.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0615.rst) “This proposes adding a module, ``zoneinfo``, to provide a concrete time zone implementation supporting the IANA time zone dat” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | tzdata |  | [E.1.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0615.rst) “This proposes adding a module, ``zoneinfo``, to provide a concrete time zone implementation supporting the IANA time zone dat” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | tzdata |  | [E.1.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0615.rst) “This proposes adding a module, ``zoneinfo``, to provide a concrete time zone implementation supporting the IANA time zone dat” | 답과 인용한 구절의 의미가 모두 일치함. |

## pep-515 · retention

How many underscores may go between adjacent digits in a Python numeric literal?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | one |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0515.rst) “The current proposal is to allow one underscore between digits, and after base specifiers in numeric literals. The underscore” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | one |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0515.rst) “The current proposal is to allow one underscore between digits, and after base specifiers in numeric literals. The underscore” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | one |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0515.rst) “The current proposal is to allow one underscore between digits, and after base specifiers in numeric literals. The underscore” | 답과 인용한 구절의 의미가 모두 일치함. |

## pep-572 · retention

What notation assigns a name within a Python expression under the assignment expressions proposal?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | NAME := expr |  | [E.1.1](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst) “Resolution: https://mail.python.org/pipermail/python-dev/2018-July/154601.html” | 인용은 Resolution 메일 주소 한 줄이며 대입식 표기는 없음. |
| B | ✗ | NAME := expr |  | [E.1.1](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst) “Resolution: https://mail.python.org/pipermail/python-dev/2018-July/154601.html” | 인용은 Resolution 메일 주소 한 줄이며 대입식 표기는 없음. |
| C | ✗ | NAME := expr |  | [E.1.1](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst) “Resolution: https://mail.python.org/pipermail/python-dev/2018-July/154601.html” | 인용은 Resolution 메일 주소 한 줄이며 대입식 표기는 없음. |

## pep-597 · retention

Which warning category signals omitted encoding when open uses the locale default?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | EncodingWarning |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0597.rst) “Add a new warning category ``EncodingWarning``. It is emitted when the ``encoding`` argument to ``open()`` is omitted and the” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | EncodingWarning |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0597.rst) “Add a new warning category ``EncodingWarning``. It is emitted when the ``encoding`` argument to ``open()`` is omitted and the” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | EncodingWarning |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0597.rst) “Add a new warning category ``EncodingWarning``. It is emitted when the ``encoding`` argument to ``open()`` is omitted and the” | 답과 인용한 구절의 의미가 모두 일치함. |

## pep-618 · retention

Which exception does strict zip raise when its iterables have different lengths?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | ValueError |  | [E.1.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst) “This PEP proposes adding an optional ``strict`` boolean keyword parameter to the built-in ``zip``. When enabled, a ``ValueErr” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | ValueError |  | [E.1.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst) “This PEP proposes adding an optional ``strict`` boolean keyword parameter to the built-in ``zip``. When enabled, a ``ValueErr” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✗ | ValueError |  |  | 출력·인용 형식 오류 |

## pep-669 · retention

Which namespace exports the low-impact interpreter monitoring functions and constants?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | sys.monitoring |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0669.rst) “A ``sys.monitoring`` namespace will be added, which will contain the relevant functions and constants.” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✗ | sys.monitoring |  | [E.2.4](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0669.rst) “Motivation ==========” | 인용은 Motivation 제목뿐. |
| C | ✓ | sys.monitoring |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0669.rst) “A ``sys.monitoring`` namespace will be added, which will contain the relevant functions and constants.” | 답과 인용한 구절의 의미가 모두 일치함. |

## pep-654 · retention

What syntax handles exception groups in the proposal for multiple unrelated exceptions?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | except* |  | [E.1.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0654.rst) “* A new standard exception type, the ``ExceptionGroup``, which represents a group of unrelated exceptions being propagated to” | 인용은 ExceptionGroup 자료형 정의이며 except* 구문은 없음. |
| B | ✗ | except* |  | [E.1.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0654.rst) “* A new standard exception type, the ``ExceptionGroup``, which represents a group of unrelated exceptions being propagated to” | 인용은 ExceptionGroup 자료형 정의이며 except* 구문은 없음. |
| C | ✗ | except* |  | [E.1.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0654.rst) “* A new standard exception type, the ``ExceptionGroup``, which represents a group of unrelated exceptions being propagated to” | 인용은 ExceptionGroup 자료형 정의이며 except* 구문은 없음. |

## pep-553 · retention

What value of PYTHONBREAKPOINT makes the default breakpoint hook disable debugging?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | 0 |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0553.rst) “* ``PYTHONBREAKPOINT=0`` disables debugging. Specifically, with this value ``sys.breakpointhook()`` returns ``None`` immediat” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | 0 |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0553.rst) “* ``PYTHONBREAKPOINT=0`` disables debugging. Specifically, with this value ``sys.breakpointhook()`` returns ``None`` immediat” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | 0 |  | [E.2.3](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0553.rst) “* ``PYTHONBREAKPOINT=0`` disables debugging. Specifically, with this value ``sys.breakpointhook()`` returns ``None`` immediat” | 답과 인용한 구절의 의미가 모두 일치함. |

## pep-552 · retention

Which hash algorithm was chosen for the source contents in the hash-based pyc format?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | SipHash |  | [E.1.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0552.rst) “If the lowest bit of the bit field is set, the pyc is a hash-based pyc. We call the second lowest bit the ``check_source`` fl” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | SipHash |  | [E.1.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0552.rst) “If the lowest bit of the bit field is set, the pyc is a hash-based pyc. We call the second lowest bit the ``check_source`` fl” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | SipHash |  | [E.1.2](https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0552.rst) “If the lowest bit of the bit field is set, the pyc is a hash-based pyc. We call the second lowest bit the ``check_source`` fl” | 답과 인용한 구절의 의미가 모두 일치함. |

## F_SH_Top01_002 · retention

In the competitive analysis task for the supply chain carbon footprint project, after Huilan Chen completed the analysis of key competitors (especially EcoTrace), which document management system did she upload the final report to?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | Confluence |  | E.2.1 “@all Good morning, I have completed the analysis report on our main competitors. It focuses on EcoTrace's features, pricing, ” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | Confluence |  | E.2.1 “@all Good morning, I have completed the analysis report on our main competitors. It focuses on EcoTrace's features, pricing, ” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | Confluence |  | E.2.1 “@all Good morning, I have completed the analysis report on our main competitors. It focuses on EcoTrace's features, pricing, ” | 답과 인용한 구절의 의미가 모두 일치함. |

## F_SH_Top01_013 · retention

After conducting a technical assessment of the data quality of the production line energy management system, what is the preliminary estimated number of workdays required for data cleansing and initial verification in the report?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | at least 10 workdays |  | E.1.1 “@Mingzhi Li Boss Li, the draft technical evaluation report on the data quality of the production line energy management syste” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | at least 10 workdays |  | E.1.1 “@Mingzhi Li Boss Li, the draft technical evaluation report on the data quality of the production line energy management syste” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | at least 10 workdays |  | E.1.1 “@Mingzhi Li Boss Li, the draft technical evaluation report on the data quality of the production line energy management syste” | 답과 인용한 구절의 의미가 모두 일치함. |

## F_SH_Top01_033 · retention

When reviewing the first draft of the user interview outline for the carbon emissions management platform, who suggested adding questions about customizable reporting dimensions to address the needs of managers and auditors?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | Lizhen Zhou |  | E.1.1 “@Luhao Zhao I've read the outline, and it's well-written. Regarding the sections for managers and audit requirements, I sugge” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | Lizhen Zhou |  | E.1.1 “@Luhao Zhao I've read the outline, and it's well-written. Regarding the sections for managers and audit requirements, I sugge” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✗ | Yu Su |  | E.2.1 “Good morning, everyone! A new week has begun. My main task today is to finalize the revisions to the user interview outline. ” | 맞는 제안자를 Yu Su로 잘못 특정함. |

## related-1 · related_qa

With the earlier SAFE_CRLF_FALSE setting, what should happen on EOL roundtrip errors?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✗ | do nothing in case of EOL roundtrip errors |  | [O1.1.2](https://github.com/git/git/commit/8462ff43e42ab67cecd16fdfb59451a53cc8a945) “When calling convert_to_git(), the checksafe parameter defined what should happen if the EOL conversion (CRLF --> LF --> CRLF” | 인용은 checksafe 일반 설명이며 FALSE에서 아무 일도 하지 않는다는 값별 정의가 없음. |
| B | ✗ | do nothing in case of EOL roundtrip errors |  | [O1.1.2](https://github.com/git/git/commit/8462ff43e42ab67cecd16fdfb59451a53cc8a945) “When calling convert_to_git(), the checksafe parameter defined what should happen if the EOL conversion (CRLF --> LF --> CRLF” | 인용은 checksafe 일반 설명이며 FALSE에서 아무 일도 하지 않는다는 값별 정의가 없음. |
| C | ✗ | do nothing in case of EOL roundtrip errors |  | [O1.1.2](https://github.com/git/git/commit/8462ff43e42ab67cecd16fdfb59451a53cc8a945) “When calling convert_to_git(), the checksafe parameter defined what should happen if the EOL conversion (CRLF --> LF --> CRLF” | 인용은 checksafe 일반 설명이며 FALSE에서 아무 일도 하지 않는다는 값별 정의가 없음. |

## related-2 · related_qa

According to the old change, what does the empty packed-refs load return?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | 0 |  | [O2.2.2](https://github.com/git/git/commit/01caf20d57aea73e67337ba1d396dd80a76d9dc3) “We don't actually create zero-length `packed-refs` files, but they are valid and we should handle them correctly. The old cod” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | 0 |  | [O2.2.2](https://github.com/git/git/commit/01caf20d57aea73e67337ba1d396dd80a76d9dc3) “We don't actually create zero-length `packed-refs` files, but they are valid and we should handle them correctly. The old cod” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | 0 |  | [O2.2.2](https://github.com/git/git/commit/01caf20d57aea73e67337ba1d396dd80a76d9dc3) “We don't actually create zero-length `packed-refs` files, but they are valid and we should handle them correctly. The old cod” | 답과 인용한 구절의 의미가 모두 일치함. |

## related-3 · related_qa

Which directory did the old Makefile approach inspect for failed tests?

| 조건 | 판정 | 실제 조치·답 | 모델의 설명 | 인용한 원문 | 채점 근거 |
|---|---|---|---|---|---|
| A | ✓ | test-results/ |  | [O2.1.5](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “It is the most convenient way to determine which tests failed after running the entire test suite, in parallel, to look for l” | 답과 인용한 구절의 의미가 모두 일치함. |
| B | ✓ | test-results/ |  | [O2.1.5](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “It is the most convenient way to determine which tests failed after running the entire test suite, in parallel, to look for l” | 답과 인용한 구절의 의미가 모두 일치함. |
| C | ✓ | test-results/ |  | [O2.1.5](https://github.com/git/git/commit/93a04bb105f30f5578a187c49066ccda71fe7cde) “It is the most convenient way to determine which tests failed after running the entire test suite, in parallel, to look for l” | 답과 인용한 구절의 의미가 모두 일치함. |

