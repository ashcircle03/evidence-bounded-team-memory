# 문맥 확장 개발 결과

단위는 원문 보고 두 개다. 순서 반전은 같은 사례의 반복 관측이다. 최종판은 같은 문서의 구절을 원래 순서로 정렬한다. 따라서 앞뒤 문단 순서를 뒤집어도 동일해지는 부분은 구현상의 성질이다.


## freebsd-cwd · selected

keep · 근거 있는 복구 False

실패 동작과 조건을 함께 뒷받침할 구절을 선택하지 못해 보류했다.

입력 구절 · https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac · [724, 1021]

This fixes a regression introduced with 7333ed17 (setup: convert
setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.

## freebsd-cwd · neighbors1

keep · 근거 있는 복구 False

실패 동작과 조건을 함께 뒷받침할 구절을 선택하지 못해 보류했다.

입력 구절 · https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac · [423, 722]

Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.

입력 구절 · https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac · [724, 1021]

This fixes a regression introduced with 7333ed17 (setup: convert
setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.

## freebsd-cwd · neighbors2

reassess · 근거 있는 복구 False

권한 오류 시 재시도하라는 수리 방법과 회귀 귀속을 골랐다. 작은 버퍼의 EACCES와 큰 버퍼의 성공을 설명하는 원문을 선택하지 못했다.

입력 구절 · https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac · [74, 421]

FreeBSD implements getcwd(3) as a syscall, but falls back to a version
based on readdir(3) if it fails for some reason.  The latter requires
permissions to read and execute path components, while the former does
not.  That means that if our buffer is too small and we're missing
rights we could get EACCES, but we may succeed with a bigger buffer.

입력 구절 · https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac · [423, 722]

Keep retrying if getcwd(3) indicates lack of permissions until our
buffer can fit PATH_MAX bytes, as that's the maximum supported by the
syscall on FreeBSD anyway.  This way we do what we can to be able to
benefit from the syscall, but we also won't loop forever if there is a
real permission issue.

입력 구절 · https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac · [724, 1021]

This fixes a regression introduced with 7333ed17 (setup: convert
setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.

최종 선택 구절

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

## freebsd-cwd · unrelated

keep · 근거 있는 복구 False

실패 동작과 조건을 함께 뒷받침할 구절을 선택하지 못해 보류했다.

입력 구절 · https://github.com/git/git/commit/a54e938e5b53c76ebcd5c068a4f74739c1c68bac · [724, 1021]

This fixes a regression introduced with 7333ed17 (setup: convert
setup_git_directory_gently_1 et al. to strbuf, 2014-07-28) for paths
longer than 127 bytes with components that miss read or execute
permissions (e.g. 0711 on /home for privacy reasons); we used a fixed
PATH_MAX-sized buffer before.

입력 구절 · https://github.com/git/git/commit/f4c21e89d7c6b578140e90c02b40eccb51ab8428 · [58, 84]

The change has two points:

입력 구절 · https://github.com/git/git/commit/f4c21e89d7c6b578140e90c02b40eccb51ab8428 · [86, 195]

1. Do not strip off a leading slash, because that erroneously turns an
   absolute path into a relative path.

## fsck-empty · selected

keep · 근거 있는 복구 False

실패 동작과 조건을 함께 뒷받침할 구절을 선택하지 못해 보류했다.

입력 구절 · https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d · [63, 241]

Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message

## fsck-empty · neighbors1

reassess · 근거 있는 복구 False

오류 메시지를 찾았지만 빈 파일 조건까지 포함하지 않았다.

입력 구절 · https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d · [63, 241]

Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message

입력 구절 · https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d · [245, 298]

fatal: failed to read object <sha1>: Invalid argument

최종 선택 구절

fatal: failed to read object <sha1>: Invalid argument

## fsck-empty · neighbors2

reassess · 근거 있는 복구 True

빈 파일 조건과 실제 failed to read / Invalid argument 메시지를 함께 인용했다.

입력 구절 · https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d · [63, 241]

Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message

입력 구절 · https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d · [245, 298]

fatal: failed to read object <sha1>: Invalid argument

입력 구절 · https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d · [300, 511]

This comes from a failure of mmap on this empty file, which sets errno to
EINVAL. Instead of calling xmmap on empty file, we display a clean error
message ourselves, and return a NULL pointer. The new message is

최종 선택 구절

Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message

  fatal: failed to read object <sha1>: Invalid argument

## fsck-empty · unrelated

keep · 근거 있는 복구 False

실패 동작과 조건을 함께 뒷받침할 구절을 선택하지 못해 보류했다.

입력 구절 · https://github.com/git/git/commit/33e42de0d21a8365496e904235bd32fd4659300d · [63, 241]

Since 3ba7a065527a (A loose object is not corrupt if it
cannot be read due to EMFILE), "git fsck" on a repository with an empty
loose object file complains with the error message

입력 구절 · https://github.com/git/git/commit/c9486eb04dd99fc00df3e68f9b908f9ad7ff9728 · [40, 217]

During verify_pack() all objects are read for SHA-1 check. Then
fsck_sha1() is called on every object, which read the object again
(fsck_sha1 -> parse_object -> read_sha1_file).

입력 구절 · https://github.com/git/git/commit/c9486eb04dd99fc00df3e68f9b908f9ad7ff9728 · [219, 320]

Avoid reading an object twice, do fsck_sha1 while we have an object
uncompressed data in verify_pack.
