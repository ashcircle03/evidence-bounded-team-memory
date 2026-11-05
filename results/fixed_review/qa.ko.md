# 기존 성공 QA의 답과 인용

문항마다 당시에 성공했던 설정을 복원했다. 동일 여부는 파서가 반환한 상태·답·인용·위치를 모두 비교했다.

## q04-ordinary/legacy

Which style does Git use by default for printing fetch ref update status?

이전과 동일 — True

복원 결과 · source_only

- Default value is `full`. · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/fetch.adoc#L59-L63
  > fetch.output:: Control how ref update status is printed. Valid values are `full` and `compact`. Default value is `full`. See the OUTPUT section in linkgit:git-fetch[1] for details.

## q05-ordinary/simple

Which alternate merge conflict style removes matching lines near either edge of the conflict region?

이전과 동일 — True

복원 결과 · answered

- zdiff3 · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/merge.adoc#L1-L15
  > Another alternate style, "zdiff3", is similar to diff3 but removes matching lines on the two sides from the conflict region when those matching lines appear near either the beginning or end of a conflict region.

## q06-ordinary/simple

What default subject prefix does format-patch put on its output?

이전과 동일 — True

복원 결과 · answered

- [PATCH] · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/format.adoc#L40-L43
  > format.subjectPrefix:: The default for format-patch is to output files with the '[PATCH]' subject prefix.

## q07-ordinary/premise

If nobody specifies a notes merge strategy, which strategy resolves notes conflicts by default?

이전과 동일 — True

복원 결과 · answered

- manual · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/notes.adoc#L1-L9
  > `notes.mergeStrategy`:: Which merge strategy to choose by default when resolving notes conflicts. Must be one of `manual`, `ours`, `theirs`, `union`, or `cat_sort_uniq`. Defaults to `manual`. See the "NOTES MERGE STRATEGIES" section of linkgit:git-notes[1] for more information on each strategy. + This setting can be overridden by passing the `--strategy` option to linkgit:git-notes[1].

## q08-ordinary/simple

Which Git configuration option chooses between basic and extended when grep.patternType is set to default?

이전과 동일 — True

복원 결과 · answered

- grep.extendedRegexp · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/grep.adoc#L7-L13
  > Using a value of 'basic', 'extended', 'fixed', or 'perl' will enable the `--basic-regexp`, `--extended-regexp`, `--fixed-strings`, or `--perl-regexp` option accordingly, while the value 'default' will use the `grep.extendedRegexp` option to choose between 'basic' and 'extended'.

## d01/premise

What name does a newly cloned repository give its remote by default?

이전과 동일 — True

복원 결과 · unresolved

- upstream · trial://worklog/646956c0e537938abf1125c2
  > I checked the same unmodified release on the packaging job. The default remote name for a newly cloned repository is upstream.
- origin · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/clone.adoc#L1-L12
  > `clone.defaultRemoteName`:: The name of the remote to create when cloning a repository. Defaults to `origin`. ifdef::git-clone[] It can be overridden by passing the `--origin` command-line option. endif::[] ifndef::git-clone[] It can be overridden by passing the `--origin` command-line option to linkgit:git-clone[1]. endif::[]

## d07/premise

Which cartridge should each sampler use for collecting field water?

이전과 동일 — True

복원 결과 · conditional

- L-2 cartridge · trial://worklog/4aa08d0501e153ad28103fe5
  > For freshwater sites the field water sampler uses the L-2 cartridge.
- B-8 cartridge · trial://worklog/e288efd3c457166052d3dc9a
  > At brackish sites the field water sampler uses the B-8 cartridge.

## old-pep-615-clean/premise

If system time zone data is unavailable, which PyPI package supplies the fallback for zoneinfo?

이전과 동일 — True

복원 결과 · answered

- tzdata · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0615.rst
  > By default, ``zoneinfo`` will use the system's time zone data if available; if no system time zone data is available, the library will fall back to using the first-party package ``tzdata``, deployed on PyPI.

## old-pep-572-clean/premise

What notation assigns a name within a Python expression under the assignment expressions proposal?

이전과 동일 — True

복원 결과 · answered

- NAME := expr · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst
  > This is of the form ``NAME := expr`` where ``expr`` is any valid Python expression other than an unparenthesized tuple, and ``NAME`` is an identifier.

## old-pep-597-clean/premise

Which warning category signals omitted encoding when open uses the locale default?

이전과 동일 — True

복원 결과 · answered

- EncodingWarning · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0597.rst
  > When the flag is set, ``io.TextIOWrapper()``, ``open()`` and other modules using them will emit ``EncodingWarning`` when the ``encoding`` argument is omitted.

## old-pep-618-clean/premise

Which exception does strict zip raise when its iterables have different lengths?

이전과 동일 — True

복원 결과 · answered

- ValueError · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst
  > When the built-in ``zip`` is called with the keyword-only argument ``strict=True``, the resulting iterator will raise a ``ValueError`` if the arguments are exhausted at differing lengths. This error will occur at the point when iteration would normally stop today.

## old-pep-669-clean/premise

Which namespace exports the low-impact interpreter monitoring functions and constants?

이전과 동일 — True

복원 결과 · answered

- sys.monitoring · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0669.rst
  > A ``sys.monitoring`` namespace will be added, which will contain the relevant functions and constants.

## old-pep-654-clean/premise

What syntax handles exception groups in the proposal for multiple unrelated exceptions?

이전과 동일 — True

복원 결과 · answered

- the ``except*`` syntax · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0654.rst
  > The purpose of this PEP, then, is to add the ``ExceptionGroup`` builtin type and the ``except*`` syntax for handling exception groups in the interpreter.

## old-pep-553-clean/premise

What value of PYTHONBREAKPOINT makes the default breakpoint hook disable debugging?

이전과 동일 — True

복원 결과 · answered

- 0 · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0553.rst
  > * ``PYTHONBREAKPOINT=0`` disables debugging.

## old-pep-572-conflict/premise

What notation assigns a name within a Python expression under the assignment expressions proposal?

이전과 동일 — True

복원 결과 · unresolved

- NAME := expr · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst
  > This is a proposal for creating a way to assign to variables within an expression using the notation ``NAME := expr``.
- NAME <- expr · casebook://messages/53dfa0d0c6823f1309b5acff
  > In our language review, assignment inside an expression uses NAME <- expr. That is the notation our review recorded for named expressions.

## old-pep-618-conflict/premise

Which exception does strict zip raise when its iterables have different lengths?

이전과 동일 — True

복원 결과 · unresolved

- LengthMismatchError · casebook://messages/25ca492f2cdf17bdb4cce7bf
  > Running the strict zip unequal-lengths check, we recorded the raised exception as LengthMismatchError for iterables of different lengths.
- ValueError · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst
  > When the built-in ``zip`` is called with the keyword-only argument ``strict=True``, the resulting iterator will raise a ``ValueError`` if the arguments are exhausted at differing lengths. This error will occur at the point when iteration would normally stop today.

## F_SH_Top01_002/premise

In the competitive analysis task for the supply chain carbon footprint project, after Huilan Chen completed the analysis of key competitors (especially EcoTrace), which document management system did she upload the final report to?

이전과 동일 — True

복원 결과 · answered

- Confluence · EverMemBench-Dynamic@a6b210a32248e841967b7b64a64281d2ff3f669d/01/2025-01-31/Group 3/3
  > The report has been uploaded to Confluence: https://sd.confluence.net/wiki/spaces/SCT/pages/20250131/EcoTrace+Competitive+Analysis+Report.

## F_SH_Top01_013/premise

After conducting a technical assessment of the data quality of the production line energy management system, what is the preliminary estimated number of workdays required for data cleansing and initial verification in the report?

이전과 동일 — True

복원 결과 · answered

- at least 10 working days · EverMemBench-Dynamic@a6b210a32248e841967b7b64a64281d2ff3f669d/01/2025-01-14/Group 1/5
  > The core conclusion is that the automated cleaning of this data source is quite difficult, and it is initially estimated that at least 10 working days of data engineer input will be required for rule development and initial manual verification.

## F_SH_Top01_033/premise

When reviewing the first draft of the user interview outline for the carbon emissions management platform, who suggested adding questions about customizable reporting dimensions to address the needs of managers and auditors?

이전과 동일 — True

복원 결과 · answered

- Lizhen Zhou · EverMemBench-Dynamic@a6b210a32248e841967b7b64a64281d2ff3f669d/01/2025-01-24/Group 1/5
  > Regarding the sections for managers and audit requirements, I suggest adding a question: "What customizable dimensions would you like the generated reports to have?

## pep-680/clean/candidate

Which standard library module provides the TOML parser for Python packaging tools?

이전과 동일 — True

복원 결과 · answered

- tomllib · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0680.rst
  > Title: tomllib: Support for Parsing TOML in the Standard Library
