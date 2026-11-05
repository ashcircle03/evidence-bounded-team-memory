# 새 Git 사례별 비교

각 링크는 원본 Git 커밋, 아래 구절은 실제 모델이 선택한 구절이다.

## http-index

[과거 결정](https://github.com/git/git/commit/b1b8dfde6929ec9463eca0a858c4adb9786d7c93) · [새 보고](https://github.com/git/git/commit/63aca3f7f14e01cabccf2165b941205a8a9a01dc) · [대조 결정](https://github.com/git/git/commit/7655b4119d49844e6ebc62da571e5f18528dbde8)

A dumb HTTP fetch with a remote v1 pack index fails after collision checks; the local index can conflict with the downloaded one. At minimum connect the failure/condition and prior collision check.

### simple

retest · 대상 True · 두 구절 False · 조건 설명 False · 대조까지 False

previous · - We don't treat the hash of the loose object file's contents as a checksum, since the same loose object can be stored using different bytes on disk (e.g., when adjusting core.compression, using a different version of zlib, etc.).

incoming · I suspect that worse case does not even come up often, since it implies that the packs are generated to match distinct parts of history (i.e., in practice even in a repo with many packs you're going to end up grabbing all of those packs to do a clone).

### referenced-review

reassess · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · We've had "FIXME!!! Collision check here ?" in finalize_object_file() since aac1794132 (Improve sha1 object file writing., 2005-05-03). That is, when we try to write a file with the same name, we assume the on-disk contents are the same and blindly throw away the new copy.

incoming · The regression we saw in the real world was (3a). A recent client fetching from a server with a v1 index downloaded that index, then complained about trying to overwrite it with its own v2 index. This collision is otherwise harmless; we know we want to replace the remote version with our local one, but the collision check doesn't realize that.

alternative · Fetching over dumb HTTP transport doesn't show any progress, even with the option --progress. If the connection is slow or there is a lot of data to get then this can take a long time while the user is left to wonder if git got stuck.

rationale · The incoming collision check failed to recognize the difference between an outdated version of the index file and a newly fetched updated version, thus incorrectly assuming the on-disk contents were identical and discarding the new file.

distinction · "The other decision addresses the collision check in finalize_object_file(), which differs from the specific operation in the incoming report by not recognizing the replacement of the remote version with the local one in a file collision scenario."

### role-review

keep · 대상 False · 두 구절 False · 조건 설명 False · 대조까지 False

incomplete role evidence for the reported change

## make-info

[과거 결정](https://github.com/git/git/commit/dad9cd7d518375799413b5a3af179f4cd95cfbe4) · [새 보고](https://github.com/git/git/commit/8af0699b7a86a6f3c2fe9b745bcbe56ec777feac) · [대조 결정](https://github.com/git/git/commit/4c64fb5aad93dd2efe07bce943852ba4ce41ed26)

Sharing the cleared suffix list breaks make info's explicit rule because its use of $* depended on a recognized suffix. Must identify that dependency, not merely show a Makefile regression.

### simple

retest · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · This was added in 30248886ce8 (Makefile: disable default implicit rules, 2010-01-26), let's move it to the top of "shared.mak" so it'll apply to all our Makefiles.

incoming · This was the only use of $* in our Makefiles in an explicit rule, the three remaining ones are all implicit rules, and therefore didn't depend on the ".SUFFIXES" list.

### referenced-review

reassess · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · The reason for that can be seen when comparing that run with "--debug=a". Without this change making a target like "git-status.1" will cause "make" to consider not only "git-status.txt", but "git-status.txt.o", as well as numerous other implicit suffixes such as ".c", ".cc", ".cpp" etc. See [1] for a more detailed before/after example.

incoming · In an explicit rule, there is no stem; so '$*' cannot be determined in that way. Instead, if the target name ends with a recognized suffix (*note Old-Fashioned Suffix Rules: Suffix Rules.), '$*' is set to the target name minus the suffix. For example, if the target name is 'foo.c', then '$*' is set to 'foo', since '.c' is a suffix. GNU 'make' does this bizarre thing only for compatibility with other implementations of 'make'. You should generally avoid using '$*' except in implicit rules or static pattern rules.

alternative · This usually works out, because the LINT_DOCS_GITLINK targets which depend on "gitlink/howto" also depend on just "gitlink", so the directory gets created anyway. But since we haven't given make an explicit ordering, things can racily happen out of order.

rationale · The regression occurred because the explicit rule did not correctly handle the suffix stripping as expected, leading to the inclusion of unintended targets like "git-status.txt.o" instead of just "git-status.1".

distinction · The other decision addresses implicit rules, whereas the incoming report discusses the behavior of '$*' in explicit rules.

### role-review

keep · 대상 False · 두 구절 False · 조건 설명 False · 대조까지 False

incomplete role evidence for the reported change

## freebsd-cwd

[과거 결정](https://github.com/git/git/commit/7333ed1788b4f2b162a35003044d77a716732a1f) · [새 보고](https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac) · [대조 결정](https://github.com/git/git/commit/f4c21e89d7c6b578140e90c02b40eccb51ab8428)

Changing the old cwd buffer to strbuf causes failure on long, permission-restricted FreeBSD paths; a smaller buffer can hit EACCES even though a larger one succeeds. Link the buffer change, condition and result.

### simple

retest · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · Replacing the PATH_MAX-sized buffer used before removes a path length limition on some file systems.

incoming · Keep retrying if getcwd(3) indicates lack of permissions until our buffer can fit PATH_MAX bytes, as that's the maximum supported by the syscall on FreeBSD anyway.

### referenced-review

reassess · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · Convert setup_git_directory_gently_1() and its helper functions setup_explicit_git_dir(), setup_discovered_git_dir() and setup_bare_git_dir() to use a struct strbuf to hold the current working directory. Replacing the PATH_MAX-sized buffer used before removes a path length limition on some file systems. The functions are converted all in one go because they all read and write the variable cwd.

incoming · This fixes a regression introduced with 7333ed17 (setup: convert setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths longer than 127 bytes with components that miss read or execute permissions (e.g. 0711 on /home for privacy reasons); we used a fixed PATH_MAX-sized buffer before.

alternative · 1. Do not strip off a leading slash, because that erroneously turns an absolute path into a relative path.

rationale · The regression occurred because using a struct strbuf instead of a fixed-size PATH_MAX-sized buffer allowed handling longer paths, but the earlier commit did not account for cases where the strbuf could still be insufficiently large, leading to failures with paths longer than 127 bytes.

distinction · The other decision addresses not stripping off a leading slash, differing from the specific operation in the incoming report which fixes a regression for paths longer than 127 bytes with permission issues.

### role-review

reassess · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · Convert setup_git_directory_gently_1() and its helper functions setup_explicit_git_dir(), setup_discovered_git_dir() and setup_bare_git_dir() to use a struct strbuf to hold the current working directory. Replacing the PATH_MAX-sized buffer used before removes a path length limition on some file systems. The functions are converted all in one go because they all read and write the variable cwd.

incoming · This fixes a regression introduced with 7333ed17 (setup: convert setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths longer than 127 bytes with components that miss read or execute permissions (e.g. 0711 on /home for privacy reasons); we used a fixed PATH_MAX-sized buffer before.

alternative · 1. Do not strip off a leading slash, because that erroneously turns an absolute path into a relative path.

rationale · Revisit the earlier decision reported as “Convert setup_git_directory_gently_1() and its helper functions setup_explicit_git_dir(), setup_discovered_git_dir() and setup_bare_git_dir() to use a struct strbuf to hold the current working directory. Replacing the PATH_MAX-sized buffer used before removes a path length limition on some file systems. The functions are converted all in one go because they all read and write the variable cwd.”. The incoming evidence gives the reason. This fixes a regression introduced with 7333ed17 (setup: convert setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths longer than 127 bytes with components that miss read or execute permissions (e.g. 0711 on /home for privacy reasons); we used a fixed PATH_MAX-sized buffer before.

distinction · The alternative addresses “1. Do not strip off a leading slash, because that erroneously turns an absolute path into a relative path.”, while the new report concerns “This fixes a regression introduced with 7333ed17 (setup: convert setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths longer than 127 bytes with components that miss read or execute permissions (e.g. 0711 on /home for privacy reasons); we used a fixed PATH_MAX-sized buffer before.”.
- subject · This fixes a regression
- action · fixes a regression
- condition · paths longer than 127 bytes with components that miss read or execute permissions (e.g. 0711 on /home for privacy reasons)

## fsck-empty

[과거 결정](https://github.com/git/git/commit/3ba7a065527a27f45659398e882feaa1165cbb4c) · [새 보고](https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d) · [대조 결정](https://github.com/git/git/commit/eb726f2d760dd78915e4a24f014ab411a165daa3)

Changing read-error/corruption classification leads fsck to misreport empty loose object files as a read/invalid argument error. Empty loose file, reporting behavior, and connection to the earlier decision are required.

### simple

retest · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · A loose object is not corrupt if it cannot be read due to EMFILE

incoming · Since 3ba7a065527a (A loose object is not corrupt if it cannot be read due to EMFILE), "git fsck" on a repository with an empty loose object file complains with the error message

### referenced-review

reassess · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · "git fsck" bails out with a claim that a loose object that cannot be read but exists on the filesystem to be corrupt, which is wrong when read_object() failed due to e.g. EMFILE.

incoming · Since 3ba7a065527a (A loose object is not corrupt if it cannot be read due to EMFILE), "git fsck" on a repository with an empty loose object file complains with the error message

alternative · Noticed and reported by BJ Hargrave.

rationale · Reading the empty loose object file failed with EMFILE, causing read_object() to return without attempting to read the object data, leading to "git fsck" incorrectly reporting the object as corrupt.

distinction · "git fsck" addresses the incorrect identification of a non-corrupt loose object due to EMFILE, differing from the incoming report which now correctly identifies such objects as non-corrupt.

### role-review

reassess · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · "git fsck" bails out with a claim that a loose object that cannot be read but exists on the filesystem to be corrupt, which is wrong when read_object() failed due to e.g. EMFILE.

incoming · Since 3ba7a065527a (A loose object is not corrupt if it cannot be read due to EMFILE), "git fsck" on a repository with an empty loose object file complains with the error message

alternative · Noticed and reported by BJ Hargrave.

rationale · Revisit the earlier decision reported as “"git fsck" bails out with a claim that a loose object that cannot be read but exists on the filesystem to be corrupt, which is wrong when read_object() failed due to e.g. EMFILE.”. The incoming evidence gives the reason. Since 3ba7a065527a (A loose object is not corrupt if it cannot be read due to EMFILE), "git fsck" on a repository with an empty loose object file complains with the error message

distinction · The alternative addresses “Noticed and reported by BJ Hargrave.”, while the new report concerns “Since 3ba7a065527a (A loose object is not corrupt if it cannot be read due to EMFILE), "git fsck" on a repository with an empty loose object file complains with the error message”.
- subject · "git fsck" on a repository with an empty loose object file complains
- action · "git fsck" on a repository with an empty loose object file complains with the error message
- condition · on a repository with an empty loose object file

## dir-diff

[과거 결정](https://github.com/git/git/commit/9ec26e797781239b36ebccb87c590e5778358007) · [새 보고](https://github.com/git/git/commit/86defcbe3f6c54a31dc898cb3adb4a3b25f1eb1a) · [대조 결정](https://github.com/git/git/commit/366f9cea18fbb7ebb0a75735da8c2a9d5a916809)

Constructing the temporary left index from a subdirectory fails to add top-level-relative paths after the subdirectory argument change; distinguish the changed working directory from unmerged duplicate entries.

### simple

retest · 대상 True · 두 구절 True · 조건 설명 False · 대조까지 False

previous · difftool: fix argument handling in subdirs

incoming · 9ec26e7977 (difftool: fix argument handling in subdirs, 2016-07-18) corrected how path arguments are handled in a subdirectory, but it introduced a regression in how entries outside of the subdirectory are handled by dir-diff.

### referenced-review

keep · 대상 False · 두 구절 False · 조건 설명 False · 대조까지 False

no unique decision in the document comparison

### role-review

keep · 대상 False · 두 구절 False · 조건 설명 False · 대조까지 False

no unique decision in the document comparison
