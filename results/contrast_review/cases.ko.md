# 보고별 재검토와 구별 근거

원문 혼합과 같은 보고의 음성 대조를 함께 표시했다. 표시가 가려진 자료, 단일 후보, 역순의 결과까지 포함한 전체 원출력은 [cases.json](cases.json)에 있다.

## scheduler

get_schedule_cmd does not populate its out parameter on every path, crashing the caller; initialize it whenever provided.

The other decision orders scheduler initialization and config changes to avoid disabling auto maintenance if setup fails.

[과거 결정](https://github.com/git/git/commit/b6c3f8e12c0a521450923ddbcf7a19a81aa3c4e7) · [비슷한 결정](https://github.com/git/git/commit/69ecfcacfd136810f2343b548174efe9ae3fdead) · [새 보고](https://github.com/git/git/commit/c95547a394a35dc26afa686454086d2db6e51ea4)

**simple** · 과거 대상 누락 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — When running 'git maintenance start', the current pattern is to configure global config settings to enable maintenance on the current repository and set 'maintenance.auto' to false and _then_ to set up the schedule with the system scheduler.
- 새 보고 — The reason is that our tests always set up the "GIT_TEST_MAINT_SCHEDULER" environment variable via "t/test-lib.sh", which allows us to override the scheduler command with a custom one so that we don't accidentally modify the developer's system.

**pairwise** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — The `get_schedule_cmd()` function allows us to override the schedule command with a specific test command such that we can verify the underlying logic in a platform-independent way. Its memory management is somewhat wild though, because it basically gives up and assigns an allocated string to the string constant output pointer. While this part is marked with `UNLEAK()` to mask this, we also leak the local string lists.
- 새 보고 — It was reported on the mailing list that running `git maintenance start` immediately segfaults starting with b6c3f8e12c (builtin/maintenance: fix leak in `get_schedule_cmd()`, 2024-09-26). And indeed, this segfault is trivial to reproduce up to a point where one is scratching their head why we didn't catch this regression in our test suite.

The reported failure of `git maintenance start` immediately segfaulting starting with commit b6c3f8e12c (builtin/maintenance: fix leak in `get_schedule_cmd()`, 2024-09-26) reveals a prior decision to use `get_schedule_cmd()` for platform-independent verification, despite its memory management issues, necessitating a recheck of this decision's rationale.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**fixed-witnesses** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


## manual

Adding scalar to the command-documentation regex shifted the man-section capture from $1 to $2 (or captured the name instead of the section).

The other decision adds the scalar help subcommand that delegates to git help scalar; it does not parse manpage headings.

[과거 결정](https://github.com/git/git/commit/cc75e556a9de5d62c1ca52db900b729fc830f378) · [비슷한 결정](https://github.com/git/git/commit/951759d3a5cb20ffeff4836aa0c4b793fa142b51) · [새 보고](https://github.com/git/git/commit/32c6fff4b871e510b7d782a4f888609da0089c15)

**simple** · 과거 대상 선택 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — Update the regex in 'cmd-list.perl' used to match the first line of command documentation to find 'scalar(1)'.
- 새 보고 — In doing so, it forgot to account for the fact that after the updated regex has found a match, the man section is no longer to be found in `$1` but now lives in `$2`.

**pairwise** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — Add 'scalar' as a 'mainporcelain' command in the Git command list. Update the regex in 'cmd-list.perl' used to match the first line of command documentation to find 'scalar(1)'.
- 새 보고 — As noted by Ævar [1], we could even match any "foo" rather than just "gitfoo" and "scalarfoo", but that's a larger change. For now, just fix the regression in cc75e556a9.

The report suggests revisiting the decision to update the regex matching commands in Git, particularly the addition of 'scalar' as a main porcelain command, as this change was deemed too extensive by Ævar [1].

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**fixed-witnesses** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


## reverse-index

The refactored reverse-index writer needlessly allocates/sorts pack order when no .rev will be written; skip this work on that path.

The other decision selects an existing on-disk reverse index instead of constructing it in memory during read/use.

[과거 결정](https://github.com/git/git/commit/a587b5a7869e9a399d4de6edea0b3f32a3548639) · [비슷한 결정](https://github.com/git/git/commit/ec8e7760ac38ef426f87ec738454e574be53a00e) · [새 보고](https://github.com/git/git/commit/8fe8bae9d28e2b02ceb482ab89ea88bb20556f1d)

**simple** · 과거 대상 선택 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — Prepare for the multi-pack index to write a .rev file by providing a way to write the reverse index without an array of pack_idx_entry (which the MIDX code does not have).
- 새 보고 — Fix a performance regression introduced in a587b5a786 (pack-write.c: extract 'write_rev_file_order', 2021-03-30) and stop needlessly allocating the "pack_order" array and sorting it with "pack_order_cmp()", only to throw that work away when we discover that we're not writing *.rev files after all.

**pairwise** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 keep

- 과거 결정 — Prepare for the multi-pack index to write a .rev file by providing a way to write the reverse index without an array of pack_idx_entry (which the MIDX code does not have).
- 새 보고 — Fix a performance regression introduced in a587b5a786 (pack-write.c: extract 'write_rev_file_order', 2021-03-30) and stop needlessly allocating the "pack_order" array and sorting it with "pack_order_cmp()", only to throw that work away when we discover that we're not writing *.rev files after all.

The earlier decision relied on the expectation that .rev files would be written, but the new evidence shows that this is no longer the case, thus changing its applicability; however, if future projects decide to write .rev files again, the earlier rationale may still apply.

판정 — 설정에 따른 선택적 쓰기를 프로젝트 전체의 현재·미래 정책 변화로 서술했다.

**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — Prepare for the multi-pack index to write a .rev file by providing a way to write the reverse index without an array of pack_idx_entry (which the MIDX code does not have).
- 새 보고 — Fix a performance regression introduced in a587b5a786 (pack-write.c: extract 'write_rev_file_order', 2021-03-30) and stop needlessly allocating the "pack_order" array and sorting it with "pack_order_cmp()", only to throw that work away when we discover that we're not writing *.rev files after all.

The earlier decision to prepare for writing a .rev file by allocating and sorting the "pack_order" array appears flawed given the report revealing we are no longer writing *.rev files, necessitating a recheck of this assumption.

판정 — 특정 실행에서 .rev를 쓰지 않는 조건을 프로젝트가 이제 .rev를 쓰지 않는다는 주장으로 넓혔다.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**fixed-witnesses** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


## difftool

After the Perl-to-builtin difftool conversion, --no-index stopped working outside a Git worktree; restore this mode.

The other decision forwards the external tool's exit status for --trust-exit-code rather than changing where difftool runs.

[과거 결정](https://github.com/git/git/commit/03831ef7b5011cbedbcc67abe5f47762f37c6c21) · [비슷한 결정](https://github.com/git/git/commit/99474b6340dbcbe58f6c256fdee231cbadb060f4) · [새 보고](https://github.com/git/git/commit/20de316e33446f37200e51aa333ba7d824dfd478)

**simple** · 과거 대상 선택 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — when reading the entire config every time `git config` is called to query a single config value).
- 새 보고 — As far as this developer can tell, the conversion from a Perl script to a built-in caused the regression in the difftool that it no longer runs outside of a Git worktree (with `--no-index`, of course).

**pairwise** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 keep

- 과거 결정 — The reason: this new, experimental, builtin difftool was shipped as part of Git for Windows v2.11.0, to allow for easier large-scale testing, but of course as an opt-in feature.
- 새 보고 — As far as this developer can tell, the conversion from a Perl script to a built-in caused the regression in the difftool that it no longer runs outside of a Git worktree (with `--no-index`, of course).

The earlier decision rested on the introduction of a new, built-in difftool in Git for Windows v2.11.0 as an opt-in feature, which may now be reconsidered due to the new evidence showing that this change likely caused a regression affecting the tool's functionality outside of a Git worktree. The earlier result remains valid if the opt-in nature of the built-in difftool is maintained or if the regression is attributed solely to other factors unrelated to the

**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — The reason: this new, experimental, builtin difftool was shipped as part of Git for Windows v2.11.0, to allow for easier large-scale testing, but of course as an opt-in feature.
- 새 보고 — As far as this developer can tell, the conversion from a Perl script to a built-in caused the regression in the difftool that it no longer runs outside of a Git worktree (with `--no-index`, of course).

This developer reports a failure where converting a Perl script difftool to a built-in caused the tool to no longer function outside of a Git worktree, indicating prior project decisions regarding tool integration may need reevaluation.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**fixed-witnesses** · 과거 대상 누락 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — run_merge_tool() was not setting $status, which prevented the exit code for builtin tools from being forwarded to the caller.
- 새 보고 — As far as this developer can tell, the conversion from a Perl script to a built-in caused the regression in the difftool that it no longer runs outside of a Git worktree (with `--no-index`, of course).
- 비슷한 결정 — The motivation for converting the difftool is that Perl scripts are not at all native on Windows, and that `git difftool` therefore is pretty slow on that platform, when there is no good reason for it to be slow.

The earlier `run_merge_tool()` operation failed to set `$status`, which now causes the difftool to not run outside of a Git worktree, as observed by the recent conversion to a built-in tool.

The other decision addresses running the difftool outside of a Git worktree, which differs from the specific operation in the incoming report about its inability to run within a worktree.

## quiet

Progress output added for commit-graph writes fails to honor --quiet and must be suppressed then.

The other decision marks commit-graph messages for translation, not whether progress is displayed.

[과거 결정](https://github.com/git/git/commit/7b0f2292224cec841de78acc911e4c378ea79faa) · [비슷한 결정](https://github.com/git/git/commit/4f5b532d18ad61d8b96d65b4f8d2321cf154d066) · [새 보고](https://github.com/git/git/commit/6b89a34c89fc763292f06012318b852b74825619)

**simple** · 과거 대상 선택 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — On larger repositories, such as linux.git the delayed progress bar(s) will kick in, and we'll show what's going on instead of, as was previously happening, printing nothing while we write the graph:
- 새 보고 — The newly added progress output for "commit-graph write" didn't check the --quiet option.

**pairwise** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**fixed-review** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — Furthermore, since the gc.writeCommitGraph setting was added in d5d5d7b641 ("gc: automatically write commit-graph files", 2018-06-27), there was no indication at all from a "git gc" run that anything was different. This why one of the progress bars being added here uses start_progress() instead of start_delayed_progress(), so that it's guaranteed to be seen. E.g. on my tiny 867 commit dotfiles.git repository:
- 새 보고 — Fix a regression in my recent 7b0f229222 ("commit-graph write: add progress output", 2018-09-17). The newly added progress output for "commit-graph write" didn't check the --quiet option.

The original author should revisit the decision to add progress output for "commit-graph write" without checking the --quiet option, as revealed by the reported regression in 7b0f229222 (\"commit-graph write: add progress output\", 2018-09-17).

판정 — commit-graph 진행 출력을 추가하면서 --quiet 여부를 검사하지 않은 회귀를 정확히 특정했다.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**fixed-witnesses** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


## slab

Clearing the shared commit slab on closing a NULL graph/submodule repo discards data still needed by the parent; that close must leave the slab intact.

The other decision closes an unused file descriptor after mmap to avoid fd exhaustion; it does not release the shared graph slab.

[과거 결정](https://github.com/git/git/commit/ac6d45d11f24921ead899c74569b717a7895f4a5) · [비슷한 결정](https://github.com/git/git/commit/c8828530b7797f5ab584c84dc2b86d3c14b39c8d) · [새 보고](https://github.com/git/git/commit/d70f554cdf38b0b05cfaa8e8eb9f80d54a5ae11c)

**simple** · 과거 대상 선택 · 혼합 retest · 무관한 두 후보 retest

- 과거 결정 — Commit 957ba814bf (commit-graph: when closing the graph, also release the slab, 2021-09-08) put the call to clear the slab into the recursive function, but this is pointless: there's only a single global slab variable.
- 새 보고 — So I suspect there may still be a bug waiting to happen there, as any object loaded before the call to close_object_store() may be stranded with a bogus maybe_tree entry (and thus looking at it after the call might cause an error).

**pairwise** · 과거 대상 누락 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — We don't ever refer to the descriptor after mmap-ing it. And keeping it open means we can run out of descriptors in degenerate cases (e.g., thousands of split chain files). Let's close it as soon as possible.
- 새 보고 — So it happens to work out. But it still seems questionable to me that we would clear a global slab (which might still be in use) when closing the commit graph. This clearing comes from 957ba814bf (commit-graph: when closing the graph, also release the slab, 2021-09-08), and was fixing a case where we really did need it to be closed (and in that case we presumably call close_object_store() more directly).

The earlier decision relied on a specific commit (957ba814bf) that cleared a global slab when closing the commit graph to avoid descriptor exhaustion in degenerate cases. However, the report suggests this is no longer necessary because the described scenario of needing to clear the slab has been addressed by calling `close_object_store()` directly, thus changing the applicability of the earlier result. The earlier result remains true if the scenario where descriptor exhaustion necessitates clearing the slab without

**fixed-review** · 과거 대상 누락 · 혼합 reassess · 무관한 두 후보 reassess

- 과거 결정 — We don't ever refer to the descriptor after mmap-ing it. And keeping it open means we can run out of descriptors in degenerate cases (e.g., thousands of split chain files). Let's close it as soon as possible.
- 새 보고 — So it happens to work out. But it still seems questionable to me that we would clear a global slab (which might still be in use) when closing the commit graph. This clearing comes from 957ba814bf (commit-graph: when closing the graph, also release the slab, 2021-09-08), and was fixing a case where we really did need it to be closed (and in that case we presumably call close_object_store() more directly).

The previous commit 957ba814bf cleared a global slab upon closing the commit graph, which may no longer be necessary given the new evidence suggesting this could lead to descriptor exhaustion in degenerate cases.

**contrast-review** · 과거 대상 누락 · 혼합 keep · 무관한 두 후보 keep


**fixed-witnesses** · 과거 대상 선택 · 혼합 reassess · 무관한 두 후보 keep

- 과거 결정 — commit-graph: move slab-clearing to close_commit_graph()
- 새 보고 — The bug is in step (2) above. We should not be clearing the slab when cleaning up the submodule repository structs. Prior to ac6d45d11f, we did not do so because it was done inside a helper function that returned early when it saw NULL. So the behavior change from that commit is that we'll now _always_ clear the slab via repo_clear(), even if the repository being closed did not have a commit graph (and thus would have a NULL commit_graph struct).
- 비슷한 결정 — We don't ever refer to the descriptor after mmap-ing it. And keeping it open means we can run out of descriptors in degenerate cases (e.g., thousands of split chain files). Let's close it as soon as possible.

The earlier decision to move slab-clearing to `close_commit_graph()` now fails because the commit introduces a scenario where the slab is cleared even when the repository does not have a commit graph struct, as seen with the observed condition of `ac6d45d11f`.

판정 — 커밋 그래프가 없는 저장소에서도 slab이 해제되는 조건을 짚었다. 마지막의 커밋 번호 표현은 어색하지만 핵심 동작과 방향은 맞다.

The other decision addresses closing file descriptors immediately after use, whereas the incoming report discusses avoiding slab clearing in certain repository cleanup scenarios.

판정 — 파일 디스크립터 종료와 slab 해제의 대상과 시점을 구분했다.

