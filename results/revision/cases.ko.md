# 문항별 결과

✓는 답과 근거 또는 재검토 대상·새 근거·조치가 함께 맞았다는 뜻이다. 유지는 명시적으로 기존 결정을 유지한 경우다. 오류는 유효한 답이나 조치를 전달하지 못한 경우다. 과거·신규 원문 전체는 재생 명령의 `--show 사건/방식`으로 확인할 수 있다. [원출력](outputs.json) · [답과 실제 인용 구절](final-outcomes.json) · [재생 명령](../../evaluation/revision/README.md)

## 일반 QA

| 사건 및 질문 | 기대 답 | 단순 검색 | 새 모듈 | 기존 QA 리더 |
|---|---|---|---|---|
| q01-ordinary · What window size does Git's aggressive garbage collection use by default for delta compression? | [250](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/gc.adoc#L10-L18) | ✗ 인용 오류 | ✗ 250 / 50 | ✗ 인용 오류 |
| q02-ordinary · Which help format is the default for Git's help viewer? | [man](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/help.adoc#L5-L9) | ✗ help.format | ✗ help.format | ✗ 인용 오류 |
| q03-ordinary · What credential-store lock timeout value means to retry indefinitely? | [-1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/credential.adoc#L51-L55) | ✗ 0 | ✗ 0 | ✗ 인용 오류 |
| q04-ordinary · Which style does Git use by default for printing fetch ref update status? | [full](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/fetch.adoc#L59-L63) | ✗ fetch.output | ✗ fetch.output | ✓ Default value is full. |
| q05-ordinary · Which alternate merge conflict style removes matching lines near either edge of the conflict region? | [zdiff3](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/merge.adoc#L1-L15) | ✓ zdiff3 | ✓ zdiff3 | ✗ 인용 오류 |
| q06-ordinary · What default subject prefix does format-patch put on its output? | [[PATCH]](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/format.adoc#L40-L43) | ✓ [PATCH] | ✗ [PATCH] / .patch | ✗ 인용 오류 |
| q07-ordinary · If nobody specifies a notes merge strategy, which strategy resolves notes conflicts by default? | [manual](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/notes.adoc#L1-L9) | ✗ 인용 오류 | ✓ manual | ✓ Defaults to manual. |
| q08-ordinary · Which Git configuration option chooses between basic and extended when grep.patternType is set to default? | [grep.extendedRegexp](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/grep.adoc#L7-L13) | ✓ grep.extendedRegexp | ✓ grep.extendedRegexp | ✗ 근거 부족 |
| q09-ordinary · What is the maximum permitted value for Git's pack.depth setting? | [4095](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/pack.adoc#L5-L9) | ✗ 4095 / 65535 | ✗ 4095 / 65535 | ✗ 인용 오류 |
| q10-ordinary · Which command-line option overrides the configured number of diff context lines? | [-U](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/diff.adoc#L70-L73) | ✗ 인용 오류 | ✗ diff.context | ✗ 인용 오류 |

## 같은 질문에 무관한 충돌 추가

| 사건 및 질문 | 기대 답 | 단순 검색 | 새 모듈 | 기존 QA 리더 |
|---|---|---|---|---|
| q01-unrelated · What window size does Git's aggressive garbage collection use by default for delta compression? | [250](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/gc.adoc#L10-L18) | ✗ 인용 오류 | ✗ 250 / 50 | — |
| q02-unrelated · Which help format is the default for Git's help viewer? | [man](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/help.adoc#L5-L9) | ✗ help.format | ✗ help.format | — |
| q03-unrelated · What credential-store lock timeout value means to retry indefinitely? | [-1](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/credential.adoc#L51-L55) | ✗ 0 | ✗ 0 | — |
| q04-unrelated · Which style does Git use by default for printing fetch ref update status? | [full](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/fetch.adoc#L59-L63) | ✗ fetch.output | ✗ fetch.output | — |
| q05-unrelated · Which alternate merge conflict style removes matching lines near either edge of the conflict region? | [zdiff3](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/merge.adoc#L1-L15) | ✓ zdiff3 | ✓ zdiff3 | — |
| q06-unrelated · What default subject prefix does format-patch put on its output? | [[PATCH]](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/format.adoc#L40-L43) | ✓ [PATCH] | ✗ [PATCH] / .patch | — |
| q07-unrelated · If nobody specifies a notes merge strategy, which strategy resolves notes conflicts by default? | [manual](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/notes.adoc#L1-L9) | ✗ 인용 오류 | ✓ manual | — |
| q08-unrelated · Which Git configuration option chooses between basic and extended when grep.patternType is set to default? | [grep.extendedRegexp](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/grep.adoc#L7-L13) | ✓ grep.extendedRegexp | ✓ grep.extendedRegexp | — |
| q09-unrelated · What is the maximum permitted value for Git's pack.depth setting? | [4095](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/pack.adoc#L5-L9) | ✗ 4095 / 65535 | ✗ 4095 / 65535 | — |
| q10-unrelated · Which command-line option overrides the configured number of diff context lines? | [-U](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/diff.adoc#L70-L73) | ✗ 인용 오류 | ✗ diff.context | — |

## 답이 갈리거나 조건에 따라 다른 QA

| 사건 및 질문 | 기대 답 | 단순 검색 | 새 모듈 | 기존 QA 리더 |
|---|---|---|---|---|
| d01 · What name does a newly cloned repository give its remote by default? | [origin](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/clone.adoc#L1-L12) / upstream | ✗ upstream | ✓ upstream / origin | — |
| d02 · What is the default value of rebase.missingCommitsCheck? | [ignore](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/rebase.adoc#L29-L39) / warn | ✗ warn | ✗ warn | — |
| d03 · In Git's protocol.version setting, which protocol version is the default when no value is set? | [2](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/protocol.adoc#L47-L63) / 1 | ✗ 인용 오류 | ✗ 2 | — |
| d04 · For branch.autoSetupRebase, what is the default mode for new tracking branches? | [never](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/branch.adoc#L16-L30) / always | ✗ 인용 오류 | ✗ always | — |
| d05 · What value is used when status.showUntrackedFiles is unspecified? | [normal](https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/status.adoc#L44-L64) / all | ✗ 인용 오류 | ✗ 인용 오류 | — |
| d06 · How long do the two kiln schedules hold the material at peak temperature? | 35 minutes (porcelain) / 50 minutes (stoneware) | ✗ 50 minutes / 35 minutes | ✗ 50 minutes / 35 minutes | — |
| d07 · Which cartridge should each sampler use for collecting field water? | L-2 (freshwater) / B-8 (brackish) | ✗ 인용 오류 | ✓ L-2 cartridge (freshwater sites) / B-8 cartridge (brackish sites) | — |
| d08 · How frequently is the station clock checked at each power setting? | six hours (standby) / fifteen minutes (acquisition) | ✗ every six hours / every fifteen minutes | ✗ every six hours (standby mode) / every fifteen minutes | — |
| d09 · Which separator does each export profile write between ledger fields? | tab (domestic) / semicolon (cross-border) | ✗ 인용 오류 | ✗ a tab / semicolon | — |
| d10 · How much sample does each assay well receive in the two plate formats? | 80 microliters (96-well) / 20 microliters (384-well) | ✗ 20 microliters / 80 microliters | ✗ 20 microliters / 80 microliters | — |

## 재검토

공개 Git의 세 양성 보고에는 과거 커밋에 대한 명시적 참조가 있다. 각 사건에는 당시 과거 기록 12~13개 또는 통제 기록 14개가 주어졌다. 정답 열은 채점용으로만 사용했다.

| 사건과 새 근거 | 사전 정답 및 이유 | 단순 검색 | 새 모듈 |
|---|---|---|---|
| r01 · On the ridge route we measured the mesh antenna against the whip. Coverage improved from 61% to 86% on identical stops. | retest · Different terrain changes the evidence for the mesh antenna's range. | ✓ 재시험 | ✓ 재시험 |
| r02 · The partner's catalog now exposes immutable device identifiers through the production lookup endpoint. I verified that the same identifier survives a catalog refresh. | reassess · The identifier required for lookup became available. | ✓ 전제 재평가 | ✗ 출력 오류 |
| r03 · In a humid-air run the washable filter trapped more dust than the disposable filter. We measured capture rising from 62% to 81% using the same feed. | retest · Humidity changes the applicability of the earlier comparison. | ✓ 재시험 | ✓ 재시험 |
| r04 · The signed dock amendment took effect today. It grants vehicle access until 22:00 and supersedes the 18:00 cutoff. | reassess · Contractual access now covers the hours formerly prohibited. | ✗ 출력 오류 | ✗ 출력 오류 |
| r05 · On a warm-cache trace of the same queries we measured the compressed index against the old one. Response time dropped from 24 ms to 9 ms. | retest · The measured warm-cache comparison tests a different usage regime. | ✓ 재시험 | ✓ 재시험 |
| r06 · The replacement vibration sensor passed acceptance. It resolves movements as small as 0.1 millimeters, including the mirror fixture signal. | reassess · The instrumentation limit that barred the mounting has changed. | ✗ 재시험 | ✗ 출력 오류 |
| r07 · We measured the same two irrigation schedules on clay soil this season. Alternating irrigation increased yield from 18 to 24 kilograms per bed against daily irrigation. | retest · A different soil produced a measured comparison. | ✗ 출력 오류 | ✓ 재시험 |
| r08 · Today's repeat salt-spray exposure of the same graphite gasket again showed a leak at the seam. | keep · Replication confirms the original reason. | ✗ 재시험 | ✓ 유지 |
| r09 · Maybe tuning the fan profile could give us more headroom. I have not measured its noise yet. | keep · Speculation without a new observation. | ✗ 재시험 | ✗ 출력 오류 |
| r10 · The nozzle team finished booking the heated bench for the already approved comparison of oval and round nozzles. | keep · Logistics for an existing comparison. | ✗ 재시험 | ✗ 출력 오류 |
| r11 · The electrical bay now has a separate service door. The optics enclosure is unchanged. | keep · Adjacent subsystem changed; the relevant enclosure did not. | ✗ 재시험 | ✗ 출력 오류 |
| r12 · We measured faster picking with white labels in the demo stockroom. The pharmacy requirement for this reagent remains in force. | keep · New performance evidence does not lift the governing constraint. | ✗ 재시험 | ✓ 유지 |
| r13 · The stairwell relay vendor circulated their planned protocol redesign. No firmware or test result is available. | keep · A vendor roadmap does not demonstrate changed reliability. | ✗ 재시험 | ✓ 유지 |
| r14 · The warehouse has finished issuing the reinforced crates from the approved order. | keep · Completion of the selected deployment. | ✗ 재시험 | ✗ 출력 오류 |
| r15 · [t6120: demonstrate weakness in disjoint-root handling](https://github.com/git/git/commit/d0e52c1728bdab27f7ca61ee0d4ff91055646bae) | reassess · Early termination still gives a wrong tag distance with the candidate cap. | ✗ 재시험 | ✗ 유지 |
| r16 · [t5619: demonstrate clone_local() with ambiguous transport](https://github.com/git/git/commit/58325b93c5b6212697b088371809e9948fee8052) | reassess · A non-local transport can reach the local-clone path; the transport assumption fails. | ✗ 출력 오류 | ✗ 유지 |
| r17 · [tests: demonstrate "show --word-diff --color-moved" regression](https://github.com/git/git/commit/b59ec03cb5f69d6a87dce8fc3ccbfd22d8de3c16) | reassess · The freeing change can double-free the buffer with two diff options. | ✗ 재시험 | ✗ 유지 |
| r18 · [describe-doc: clarify default length of abbreviation](https://github.com/git/git/commit/bfe35a61653c5789c9038b3fe9925941cf10f623) | keep · Documentation catches up with an already shipped abbreviation behavior. | ✗ 재시험 | ✓ 유지 |
| r19 · [t/helper: fix a typo](https://github.com/git/git/commit/897124aa1bcdfa7e774742d0c16e1c2a18e2487c) | keep · Comment spelling does not change a live premise. | ✗ 출력 오류 | ✓ 유지 |
| r20 · [gitk: trivial indentation fix](https://github.com/git/git/commit/1f6b196665704023fb14644e93b869ce54ee2452) | keep · Indentation cleanup does not change a decision. | ✗ 재시험 | ✓ 유지 |
