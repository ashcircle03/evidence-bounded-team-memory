# 같은20문항의 수정 전후 답·인용

이미 본 개발 문항이다. 같은 고정 기준으로 개발 담당 AI가 원문을 대조해 판정했다. 독립 평가가 아니다.

| 문항 | 이전 | 수정 후 |
|---|---|---|
| q04-ordinary/legacy | 1 | 1 |
| q05-ordinary/simple | 1 | 1 |
| q06-ordinary/simple | 1 | 1 |
| q07-ordinary/premise | 1 | 1 |
| q08-ordinary/simple | 1 | 1 |
| d01/premise | 1 | 1 |
| d07/premise | 1 | 1 |
| old-pep-615-clean/premise | 1 | 1 |
| old-pep-572-clean/premise | 1 | 1 |
| old-pep-597-clean/premise | 1 | 1 |
| old-pep-618-clean/premise | 1 | 1 |
| old-pep-669-clean/premise | 1 | 1 |
| old-pep-654-clean/premise | 1 | 1 |
| old-pep-553-clean/premise | 1 | 1 |
| pep-680/clean/candidate | 1 | 1 |
| old-pep-572-conflict/premise | 1 | 1 |
| old-pep-618-conflict/premise | 0 | 1 |
| F_SH_Top01_002/premise | 1 | 1 |
| F_SH_Top01_013/premise | 1 | 1 |
| F_SH_Top01_033/premise | 1 | 1 |

## q04-ordinary/legacy

Which style does Git use by default for printing fetch ref update status?

판정: fetch.output 원문이 기본 full을 명시하고 답과 반환 인용[1]이 이를 보존한다. 문서 판정은 저자 구현의 명시적 표기 파싱으로 복구했다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

Git uses the `full` style by default for printing fetch ref update status. This is specified in the `fetch.output` configuration, where the default value is set to `full` [1]. 

Source 1:
The default for `fetch.output` is `full`, which controls how ref update status is printed.

수정 후:

Git uses the `full` style by default for printing fetch ref update status. This is specified in the `fetch.output` configuration, where the default value is set to `full` [1]. 

Source 1:
The default for `fetch.output` is `full`, which controls how ref update status is printed.

수정 후 인용 원문:

[1] Git documentation contributors · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/fetch.adoc#L59-L63

원문 ID `db11b63031320d365a43bed6`, 문자 위치 0–183

> fetch.output::
> 	Control how ref update status is printed. Valid values are
> 	`full` and `compact`. Default value is `full`. See the
> 	OUTPUT section in linkgit:git-fetch[1] for details.

## q05-ordinary/simple

Which alternate merge conflict style removes matching lines near either edge of the conflict region?

판정: merge.conflictStyle 원문에 zdiff3와 양 끝의 일치 행 제거가 함께 있다. Source1 표기를 파싱해 같은 원문을 반환했다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

Source 1:
The alternate merge conflict style that removes matching lines near either edge of the conflict region is "zdiff3". This style is similar to "diff3" but includes the removal of matching lines on the two sides from the conflict region when those matching lines appear near either the beginning or end of a conflict region.

수정 후:

Source 1:
The alternate merge conflict style that removes matching lines near either edge of the conflict region is "zdiff3". This style is similar to "diff3" but includes the removal of matching lines on the two sides from the conflict region when those matching lines appear near either the beginning or end of a conflict region.

수정 후 인용 원문:

[1] Git documentation contributors · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/merge.adoc#L1-L15

원문 ID `2cd6e6057ddcdebd13c4efe5`, 문자 위치 0–852

> merge.conflictStyle::
> 	Specify the style in which conflicted hunks are written out to
> 	working tree files upon merge.  The default is "merge", which
> 	shows a `<<<<<<<` conflict marker, changes made by one side,
> 	a `=======` marker, changes made by the other side, and then
> 	a `>>>>>>>` marker.  An alternate style, "diff3", adds a `|||||||`
> 	marker and the original text before the `=======` marker.  The
> 	"merge" style tends to produce smaller conflict regions than diff3,
> 	both because of the exclusion of the original text, and because
> 	when a subset of lines match on the two sides, they are just pulled
> 	out of the conflict region.  Another alternate style, "zdiff3", is
> 	similar to diff3 but removes matching lines on the two sides from
> 	the conflict region when those matching lines appear near either
> 	the beginning or end of a conflict region.

## q06-ordinary/simple

What default subject prefix does format-patch put on its output?

판정: format.subjectPrefix 원문과 답 모두 기본 [PATCH]를 명시한다. 반환 인용[1]의 위치와 본문을 확인했다. 추가 인용 대조: format.subjectPrefix 원문의 [PATCH] 기본 접두사 문장에 연결했다. this variable은 같은 format.subjectPrefix 문단의 변수이다. 실패 NLI의 format.noprefix 문단으로 옮기지 않았다.

수정 전:

The default subject prefix for format-patch is "[PATCH]". This is specified in the documentation under the `format.subjectPrefix` setting, which indicates that the default is to output files with the "[PATCH]" subject prefix [1]. 

Source 1:
The default for format-patch is to output files with the '[PATCH]' subject prefix. Use this variable to change that prefix.

수정 후:

[1] The default subject prefix for format-patch is "[PATCH]". This is specified in the documentation under the `format.subjectPrefix` setting, which indicates that the default is to output files with the "[PATCH]" subject prefix [1]. 

Source 1:
The default for format-patch is to output files with the '[PATCH]' subject prefix. [1] Use this variable to change that prefix.

수정 후 인용 원문:

[1] Git documentation contributors · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/format.adoc#L40-L43

원문 ID `b33cab8c6b4353bf87cad57e`, 문자 위치 0–148

> format.subjectPrefix::
> 	The default for format-patch is to output files with the '[PATCH]'
> 	subject prefix. Use this variable to change that prefix.

## q07-ordinary/premise

If nobody specifies a notes merge strategy, which strategy resolves notes conflicts by default?

판정: 기본 notes.mergeStrategy는 manual이라는 원문[2]을 인용한다. 다른 설정의 반대 판정 때문에 불필요한 재작성은 있었지만 정답은 유지했다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

If nobody specifies a notes merge strategy, the default strategy that resolves notes conflicts is `manual` [2].

수정 후:

If nobody specifies a notes merge strategy, the default strategy that resolves notes conflicts is `manual` [2].

수정 후 인용 원문:

[2] Git documentation contributors · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/notes.adoc#L1-L9

원문 ID `844dbf9c27f11316fcd46ccc`, 문자 위치 0–395

> `notes.mergeStrategy`::
> 	Which merge strategy to choose by default when resolving notes
> 	conflicts.  Must be one of `manual`, `ours`, `theirs`, `union`, or
> 	`cat_sort_uniq`.  Defaults to `manual`.  See the "NOTES MERGE STRATEGIES"
> 	section of linkgit:git-notes[1] for more information on each strategy.
> +
> This setting can be overridden by passing the `--strategy` option to
> linkgit:git-notes[1].

## q08-ordinary/simple

Which Git configuration option chooses between basic and extended when grep.patternType is set to default?

판정: grep.extendedRegexp의 true 동작과 grep.patternType=default 적용 조건이 인용[2]에 있다. 질문이 요구하는 설정명을 정확히 반환했다. 추가 인용 대조: 반환 문단의 제목은 grep.extendedRegexp이며 patternType이 default가 아닐 때 무시됨을 명시한다. 질문의 옵션 이름·적용 조건과 맞다. 같은 문단이 true일 때 --extended-regexp 기본 활성화를 명시한다.

수정 전:

The Git configuration option that chooses between basic and extended matching when `grep.patternType` is set to `default` is `grep.extendedRegexp`. This option, when set to `true`, enables the `--extended-regexp` option by default. 

Answer: The `grep.extendedRegexp` configuration option chooses between basic and extended matching when `grep.patternType` is set to `default` [2].

수정 후:

[2] The Git configuration option that chooses between basic and extended matching when `grep.patternType` is set to `default` is `grep.extendedRegexp`. [2] This option, when set to `true`, enables the `--extended-regexp` option by default. 

Answer: The `grep.extendedRegexp` configuration option chooses between basic and extended matching when `grep.patternType` is set to `default` [2].

수정 후 인용 원문:

[2] Git documentation contributors · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/grep.adoc#L14-L18

원문 ID `9ea76fc93e05c8ea6b56b946`, 문자 위치 0–184

> grep.extendedRegexp::
> 	If set to true, enable `--extended-regexp` option by default. This
> 	option is ignored when the `grep.patternType` option is set to a value
> 	other than 'default'.

## d01/premise

What name does a newly cloned repository give its remote by default?

판정: Git 문서의 origin[2]과 같은 unmodified release를 확인했다는 Eli의 upstream[1]을 모두 반환했다. 한쪽을 삭제하거나 새로운 조건을 만들어 합리화하지 않았다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

The default remote name for a newly cloned repository is `origin` [2]. The default remote name for a newly cloned repository is upstream [1].

수정 후:

The default remote name for a newly cloned repository is `origin` [2]. The default remote name for a newly cloned repository is upstream [1].

수정 후 인용 원문:

[1] Eli · trial://worklog/646956c0e537938abf1125c2

원문 ID `f91f3a39ce0a320652cc0633`, 문자 위치 0–126

> I checked the same unmodified release on the packaging job. The default remote name for a newly cloned repository is upstream.

[2] Git documentation contributors · https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/clone.adoc#L1-L12

원문 ID `878239f428b41a7f4b24f58a`, 문자 위치 0–335

> `clone.defaultRemoteName`::
> 	The name of the remote to create when cloning a repository.  Defaults to
> 	`origin`.
> ifdef::git-clone[]
> 	It can be overridden by passing the `--origin` command-line
> 	option.
> endif::[]
> ifndef::git-clone[]
> 	It can be overridden by passing the `--origin` command-line
> 	option to linkgit:git-clone[1].
> endif::[]

## d07/premise

Which cartridge should each sampler use for collecting field water?

판정: freshwater/L-2[1]와 brackish/B-8[2]의 각 조건과 답을 유지했다. 같은 조건의 충돌이라고 바꾸지 않았다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

For collecting field water, the choice of cartridge depends on the type of site. For freshwater sites, the field water sampler should use the L-2 cartridge [1]. For brackish sites, the field water sampler should use the B-8 cartridge [2]. 

Source 1:
For freshwater sites the field water sampler uses the L-2 cartridge.

Source 2:
At brackish sites the field water sampler uses the B-8 cartridge.

수정 후:

For collecting field water, the choice of cartridge depends on the type of site. For freshwater sites, the field water sampler should use the L-2 cartridge [1]. For brackish sites, the field water sampler should use the B-8 cartridge [2]. 

Source 1:
For freshwater sites the field water sampler uses the L-2 cartridge.

Source 2:
At brackish sites the field water sampler uses the B-8 cartridge.

수정 후 인용 원문:

[1] Kim · trial://worklog/4aa08d0501e153ad28103fe5

원문 ID `f8ab786ad9476e4962f7a0d4`, 문자 위치 0–68

> For freshwater sites the field water sampler uses the L-2 cartridge.

[2] Uma · trial://worklog/e288efd3c457166052d3dc9a

원문 ID `cb8639d64cb898545c782f15`, 문자 위치 0–65

> At brackish sites the field water sampler uses the B-8 cartridge.

## old-pep-615-clean/premise

If system time zone data is unavailable, which PyPI package supplies the fallback for zoneinfo?

판정: PEP615 초록의 시스템 시간대 데이터가 없을 때 PyPI tzdata로 fallback한다는 문장을 인용하고 조건까지 보존했다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

If system time zone data is unavailable, the fallback for `zoneinfo` is the first-party package `tzdata`, which is deployed on PyPI [1]. 

Source 1:
The `zoneinfo` module will use the system's time zone data if available; if no system time zone data is available, the library will fall back to using the first-party package `tzdata`, deployed on PyPI. [d]_

수정 후:

If system time zone data is unavailable, the fallback for `zoneinfo` is the first-party package `tzdata`, which is deployed on PyPI [1]. 

Source 1:
The `zoneinfo` module will use the system's time zone data if available; if no system time zone data is available, the library will fall back to using the first-party package `tzdata`, deployed on PyPI. [d]_

수정 후 인용 원문:

[1] PEP 615 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0615.rst

원문 ID `7e8c655d9ab964be2c9dd0f4`, 문자 위치 0–1375

> PEP: 615
> Title: Support for the IANA Time Zone Database in the Standard Library
> Author: Paul Ganssle <paul at ganssle.io>
> Discussions-To: https://discuss.python.org/t/3468
> Status: Final
> Type: Standards Track
> Created: 22-Feb-2020
> Python-Version: 3.9
> Post-History: 25-Feb-2020, 29-Mar-2020
> Replaces: 431
> 
> .. canonical-doc:: :external+python:mod:`zoneinfo`
> 
> Abstract
> ========
> 
> This proposes adding a module, ``zoneinfo``, to provide a concrete time zone
> implementation supporting the IANA time zone database.  By default,
> ``zoneinfo`` will use the system's time zone data if available; if no system
> time zone data is available, the library will fall back to using the
> first-party package ``tzdata``, deployed on PyPI. [d]_
> 
> Motivation
> ==========
> 
> The ``datetime`` library uses a flexible mechanism to handle time zones: all
> conversions and time zone information queries are delegated to an instance of a
> subclass of the abstract ``datetime.tzinfo`` base class. [#tzinfo]_ This allows
> users to implement arbitrarily complex time zone rules, but in practice the
> majority of users want support for just three types of time zone: [a]_
> 
> 1. UTC and fixed offsets thereof
> 2. The system local time zone
> 3. IANA time zones
> 
> In Python 3.2, the ``datetime.timezone`` class was introduced to support the
> first class of time zone (with a special ``datetime.timezone.utc`` singleton
> for UTC).

## old-pep-572-clean/premise

What notation assigns a name within a Python expression under the assignment expressions proposal?

판정: PEP572 초록과 제목의 NAME := expr 및 Assignment Expressions를 그대로 근거로 사용했다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

The notation that assigns a name within a Python expression under the assignment expressions proposal is ``NAME := expr``. This notation allows for assigning a variable within an expression, which is part of the "Assignment Expressions" feature introduced in PEP 572 [1].

Source 1:
The notation ``NAME := expr`` is used to assign a name within a Python expression as part of the "Assignment Expressions" proposal [1].

수정 후:

The notation that assigns a name within a Python expression under the assignment expressions proposal is ``NAME := expr``. This notation allows for assigning a variable within an expression, which is part of the "Assignment Expressions" feature introduced in PEP 572 [1].

Source 1:
The notation ``NAME := expr`` is used to assign a name within a Python expression as part of the "Assignment Expressions" proposal [1].

수정 후 인용 원문:

[1] PEP 572 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst

원문 ID `d60afae8bbc6e0863adaf8cf`, 문자 위치 0–2011

> PEP: 572
> Title: Assignment Expressions
> Author: Chris Angelico <rosuav@gmail.com>, Tim Peters <tim.peters@gmail.com>,
>         Guido van Rossum <guido@python.org>
> Status: Final
> Type: Standards Track
> Created: 28-Feb-2018
> Python-Version: 3.8
> Post-History: 28-Feb-2018, 02-Mar-2018, 23-Mar-2018, 04-Apr-2018, 17-Apr-2018,
>               25-Apr-2018, 09-Jul-2018, 05-Aug-2019
> Resolution: https://mail.python.org/pipermail/python-dev/2018-July/154601.html
> 
> 
> Abstract
> ========
> 
> This is a proposal for creating a way to assign to variables within an
> expression using the notation ``NAME := expr``.
> 
> As part of this change, there is also an update to dictionary comprehension
> evaluation order to ensure key expressions are executed before value
> expressions (allowing the key to be bound to a name and then re-used as part of
> calculating the corresponding value).
> 
> During discussion of this PEP, the operator became informally known as
> "the walrus operator". The construct's formal name is "Assignment Expressions"
> (as per the PEP title), but they may also be referred to as "Named Expressions"
> (e.g. the CPython reference implementation uses that name internally).
> 
> 
> Rationale
> =========
> 
> Naming the result of an expression is an important part of programming,
> allowing a descriptive name to be used in place of a longer expression,
> and permitting reuse.  Currently, this feature is available only in
> statement form, making it unavailable in list comprehensions and other
> expression contexts.
> 
> Additionally, naming sub-parts of a large expression can assist an interactive
> debugger, providing useful display hooks and partial results. Without a way to
> capture sub-expressions inline, this would require refactoring of the original
> code; with assignment expressions, this merely requires the insertion of a few
> ``name :=`` markers. Removing the need to refactor reduces the likelihood that
> the code be inadvertently changed as part of debugging (a common cause of
> Heisenbugs), and is easier to dictate to another programmer.

## old-pep-597-clean/premise

Which warning category signals omitted encoding when open uses the locale default?

판정: PEP597 초록의 EncodingWarning과 open의 encoding 생략 조건을 인용했다. 추가로 기본 경고가 활성화됐다고 주장하지 않았다. 추가 인용 대조: PEP597의 EncodingWarning 문단이 open의 encoding 생략과 locale 기본값 조건을 명시한다.

수정 전:

The warning category that signals omitted encoding when `open` uses the locale default is ``EncodingWarning``. This warning is emitted when the ``encoding`` argument is omitted and the default locale-specific encoding is used [1].

Source 1:  
The warning is emitted when the ``encoding`` argument to ``open()`` is omitted and the default locale-specific encoding is used [1].

수정 후:

[1] The warning category that signals omitted encoding when `open` uses the locale default is ``EncodingWarning``. This warning is emitted when the ``encoding`` argument is omitted and the default locale-specific encoding is used [1].

Source 1:  
The warning is emitted when the ``encoding`` argument to ``open()`` is omitted and the default locale-specific encoding is used [1].

수정 후 인용 원문:

[1] PEP 597 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0597.rst

원문 ID `9cdf2a0f123965fbe7cbf525`, 문자 위치 0–1831

> PEP: 597
> Title: Add optional EncodingWarning
> Author: Inada Naoki <songofacandy@gmail.com>
> Status: Final
> Type: Standards Track
> Created: 05-Jun-2019
> Python-Version: 3.10
> 
> 
> Abstract
> ========
> 
> Add a new warning category ``EncodingWarning``. It is emitted when the
> ``encoding`` argument to ``open()`` is omitted and the default
> locale-specific encoding is used.
> 
> The warning is disabled by default. A new ``-X warn_default_encoding``
> command-line option and a new ``PYTHONWARNDEFAULTENCODING`` environment
> variable can be used to enable it.
> 
> A ``"locale"`` argument value for ``encoding`` is added too. It
> explicitly specifies that the locale encoding should be used, silencing
> the warning.
> 
> 
> Motivation
> ==========
> 
> Using the default encoding is a common mistake
> ----------------------------------------------
> 
> Developers using macOS or Linux may forget that the default encoding
> is not always UTF-8.
> 
> For example, using ``long_description = open("README.md").read()`` in
> ``setup.py`` is a common mistake. Many Windows users cannot install
> such packages if there is at least one non-ASCII character
> (e.g. emoji, author names, copyright symbols, and the like)
> in their UTF-8-encoded ``README.md`` file.
> 
> Of the 4000 most downloaded packages from PyPI, 489 use non-ASCII
> characters in their README, and 82 fail to install from source on
> non-UTF-8 locales due to not specifying an encoding for a non-ASCII
> file. [1]_
> 
> Another example is ``logging.basicConfig(filename="log.txt")``.
> Some users might expect it to use UTF-8 by default, but the locale
> encoding is actually what is used. [2]_
> 
> Even Python experts may assume that the default encoding is UTF-8.
> This creates bugs that only happen on Windows; see [3]_, [4]_, [5]_,
> and [6]_ for example.
> 
> Emitting a warning when the ``encoding`` argument is omitted will help
> find such mistakes.

## old-pep-618-clean/premise

Which exception does strict zip raise when its iterables have different lengths?

판정: 질문의 요구 답 ValueError와 unequal-lengths/strict 조건은 인용[1]이 지지한다. iteration would normally stop이라는 부연도 실제 입력 Source3에 있다. 다만 그 부연 문장에 별도[3]이 없어 문장별 인용 완전성은 추가 한계로 기록한다. 추가 인용 대조: PEP618 제목·Abstract가 optional strict 인수를 명시한다. 추가 [3] Specification은 differing lengths와 iteration would normally stop을 함께 명시한다. 이전 [1]에 없던 부연 근거가 실제 반환 인용에 추가됐다.

수정 전:

When the `zip` function in Python is called with the `strict=True` parameter and the iterables have different lengths, it raises a `ValueError` [1]. This behavior is specified in PEP 618, which introduces the optional `strict` parameter to the built-in `zip` function. The `ValueError` is raised at the point when iteration would normally stop, indicating that the iterables are of unequal length and the `strict` mode is enabled.

Source 1:
The `zip` function, when called with `strict=True`, raises a `ValueError` if the arguments are exhausted at differing lengths [1].

수정 후:

When the `zip` function in Python is called with the `strict=True` parameter and the iterables have different lengths, it raises a `ValueError` [1]. [1] This behavior is specified in PEP 618, which introduces the optional `strict` parameter to the built-in `zip` function. [3] The `ValueError` is raised at the point when iteration would normally stop, indicating that the iterables are of unequal length and the `strict` mode is enabled.

Source 1:
The `zip` function, when called with `strict=True`, raises a `ValueError` if the arguments are exhausted at differing lengths [1].

수정 후 인용 원문:

[1] PEP 618 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst

원문 ID `44d1a4fcadb2fbfbc6769c81`, 문자 위치 0–1930

> PEP: 618
> Title: Add Optional Length-Checking To zip
> Author: Brandt Bucher <brandt@python.org>
> Sponsor: Antoine Pitrou <antoine@python.org>
> BDFL-Delegate: Guido van Rossum <guido@python.org>
> Status: Final
> Type: Standards Track
> Created: 01-May-2020
> Python-Version: 3.10
> Post-History: 01-May-2020, 10-May-2020, 16-Jun-2020
> Resolution: https://mail.python.org/archives/list/python-dev@python.org/message/NLWB7FVJGMBBMCF4P3ZKUIE53JPDOWJ3
> 
> 
> Abstract
> ========
> 
> This PEP proposes adding an optional ``strict`` boolean keyword
> parameter to the built-in ``zip``.  When enabled, a ``ValueError`` is
> raised if one of the arguments is exhausted before the others.
> 
> 
> Motivation
> ==========
> 
> It is clear from the author's personal experience and a `survey of the
> standard library <examples_>`_ that much (if not most) ``zip`` usage
> involves iterables that *must* be of equal length.  Sometimes this
> invariant is proven true from the context of the surrounding code, but
> often the data being zipped is passed from the caller, sourced
> separately, or generated in some fashion.  In any of these cases, the
> default behavior of ``zip`` means that faulty refactoring or logic
> errors could easily result in silently losing data.  These bugs are
> not only difficult to diagnose, but difficult to even detect at all.
> 
> It is easy to come up with simple cases where this could be a problem.
> For example, the following code may work fine when ``items`` is a
> sequence, but silently start producing shortened, mismatched results
> if ``items`` is refactored by the caller to be a consumable iterator::
> 
>     def apply_calculations(items):
>         transformed = transform(items)
>         for i, t in zip(items, transformed):
>             yield calculate(i, t)
> 
> There are several other ways in which ``zip`` is commonly used.
> Idiomatic tricks are especially susceptible, because they are often
> employed by users who lack a complete understanding of how the code
> works.

[3] PEP 618 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst

원문 ID `44d1a4fcadb2fbfbc6769c81`, 문자 위치 3064–5103

> Rationale
> =========
> 
> Some critics assert that constant boolean switches are a "code-smell",
> or go against Python's design philosophy.  However, Python currently
> contains several examples of boolean keyword parameters on built-in
> functions which are typically called with compile-time constants:
> 
> - ``compile(..., dont_inherit=True)``
> - ``open(..., closefd=False)``
> - ``print(..., flush=True)``
> - ``sorted(..., reverse=True)``
> 
> Many more exist in the standard library.
> 
> The idea and name for this new parameter were `originally proposed
> <https://mail.python.org/archives/list/python-ideas@python.org/message/6GFUADSQ5JTF7W7OGWF7XF2NH2XUTUQM>`_
> by Ram Rachum.  The thread received over 100 replies, with the
> alternative "equal" receiving a similar amount of support.
> 
> The author does not have a strong preference between the two choices,
> though "equal equals" *is* a bit awkward in prose.  It may also
> (wrongly) imply some notion of "equality" between the zipped items::
> 
>     >>> z = zip([2.0, 4.0, 6.0], [2, 4, 8], equal=True)
> 
> 
> Specification
> =============
> 
> When the built-in ``zip`` is called with the keyword-only argument
> ``strict=True``, the resulting iterator will raise a ``ValueError`` if
> the arguments are exhausted at differing lengths.  This error will
> occur at the point when iteration would normally stop today.
> 
> 
> Backward Compatibility
> ======================
> 
> This change is fully backward-compatible.  ``zip`` currently takes no
> keyword arguments, and the "non-strict" default behavior when
> ``strict`` is omitted remains unchanged.
> 
> 
> Reference Implementation
> ========================
> 
> The author has drafted a `C implementation
> <https://github.com/python/cpython/pull/20921>`_.
> 
> An approximate Python translation is::
> 
>     def zip(*iterables, strict=False):
>         if not iterables:
>             return
>         iterators = tuple(iter(iterable) for iterable in iterables)
>         try:
>             while True:
>                 items = []
>                 for iterator in iterators:
>                     items.append(next(iterator))

## old-pep-669-clean/premise

Which namespace exports the low-impact interpreter monitoring functions and constants?

판정: PEP669 초록이 sys.monitoring namespace에 관련 함수와 상수를 둔다고 명시하며 답의 인용[1]이 맞다. 추가 인용 대조: PEP669 제목·Abstract·sys.monitoring 구절이 같은 문단에 있어 namespace·API·낮은 비용을 지지한다.

수정 전:

The namespace that exports the low-impact interpreter monitoring functions and constants is ``sys.monitoring``. This namespace is introduced as part of PEP 669, which proposes an API for monitoring Python programs running on CPython with minimal performance impact.

Source 1:
The ``sys.monitoring`` namespace will be added, which will contain the relevant functions and constants [1].

수정 후:

The namespace that exports the low-impact interpreter monitoring functions and constants is ``sys.monitoring``. [1] This namespace is introduced as part of PEP 669, which proposes an API for monitoring Python programs running on CPython with minimal performance impact.

Source 1:
The ``sys.monitoring`` namespace will be added, which will contain the relevant functions and constants [1].

수정 후 인용 원문:

[1] PEP 669 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0669.rst

원문 ID `e994cfff4b43ae60a24855c6`, 문자 위치 0–1152

> PEP: 669
> Title: Low Impact Monitoring for CPython
> Author: Mark Shannon <mark@hotpy.org>
> Discussions-To: https://discuss.python.org/t/pep-669-low-impact-monitoring-for-cpython/13018/
> Status: Final
> Type: Standards Track
> Created: 18-Aug-2021
> Python-Version: 3.12
> Post-History: `07-Dec-2021 <https://mail.python.org/archives/list/python-dev@python.org/thread/VNSD4TSAM2BM64FJNIQPAOPNEGNX4MDX/>`__,
>               `10-Jan-2022 <https://discuss.python.org/t/pep-669-low-impact-monitoring-for-cpython/13018>`__,
> Resolution: https://discuss.python.org/t/pep-669-low-impact-monitoring-for-cpython/13018/42
> 
> .. canonical-doc:: :mod:`python:sys.monitoring`
> 
> Abstract
> ========
> 
> Using a profiler or debugger in CPython can have a severe impact on
> performance. Slowdowns by an order of magnitude are common.
> 
> This PEP proposes an API for monitoring Python programs running
> on CPython that will enable monitoring at low cost.
> 
> Although this PEP does not specify an implementation, it is expected that
> it will be implemented using the quickening step of
> :pep:`659`.
> 
> A ``sys.monitoring`` namespace will be added, which will contain
> the relevant functions and constants.

## old-pep-654-clean/premise

What syntax handles exception groups in the proposal for multiple unrelated exceptions?

판정: PEP654 초록의 ExceptionGroup과 except* 구문을 인용[2]으로 함께 뒷받침한다. 추가 인용 대조: Rationale은 except*가 ExceptionGroup을 처리하는 새 문법임을 명시한다. PEP654 Abstract는 ExceptionGroup과 여러 무관한 예외 처리용 except*를 함께 명시한다.

수정 전:

The syntax that handles exception groups in the proposal for multiple unrelated exceptions is ``except*``. This syntax is introduced as part of the PEP 654 proposal to handle ``ExceptionGroup`` objects, which represent a group of unrelated exceptions being propagated together.

Answer: The syntax used to handle exception groups in the proposal is ``except*`` [2].

수정 후:

[1] The syntax that handles exception groups in the proposal for multiple unrelated exceptions is ``except*``. [2] This syntax is introduced as part of the PEP 654 proposal to handle ``ExceptionGroup`` objects, which represent a group of unrelated exceptions being propagated together.

Answer: The syntax used to handle exception groups in the proposal is ``except*`` [2].

수정 후 인용 원문:

[1] PEP 654 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0654.rst

원문 ID `08242b9ceb3b4388c7fb10f3`, 문자 위치 5296–7552

> Rationale
> =========
> 
> Grouping several exceptions together can be done without changes to the
> language, simply by creating a container exception type.
> Trio [2]_ is an example of a library that has made use of this technique in its
> ``MultiError`` [9]_ type. However, such an approach requires calling code to catch
> the container exception type, and then to inspect it to determine the types of
> errors that had occurred, extract the ones it wants to handle, and reraise the
> rest. Furthermore, exceptions in Python have important information attached to
> their ``__traceback__``, ``__cause__`` and ``__context__`` fields, and
> designing a container type that preserves the integrity of this information
> requires care; it is not as simple as collecting exceptions into a set.
> 
> Changes to the language are required in order to extend support for
> exception groups in the style of existing exception handling mechanisms. At
> the very least we would like to be able to catch an exception group only if
> it contains an exception of a type that we choose to handle. Exceptions of
> other types in the same group need to be automatically reraised,
> otherwise it is too easy for user code to inadvertently swallow exceptions
> that it is not handling.
> 
> We considered whether it is possible to modify the semantics of ``except``
> for this purpose, in a backwards-compatible manner, and found that it is not.
> See the `Rejected Ideas`_ section for more on this.
> 
> The purpose of this PEP, then, is to add the ``ExceptionGroup`` builtin type
> and the ``except*`` syntax for handling exception groups in the interpreter.
> The desired semantics of ``except*`` are sufficiently different from the
> current exception handling semantics that we are not proposing to modify the
> behavior of the ``except`` keyword but rather to add the new ``except*``
> syntax.
> 
> Our premise is that exception groups and ``except*`` will be used
> selectively, only when they are needed. We do not expect them to become
> the default mechanism for exception handling.  The decision to raise
> exception groups from a library needs to be considered carefully and
> regarded as an API-breaking change. We expect that this will normally be
> done by introducing a new API rather than modifying an existing one.
> 
> 
> Specification

[2] PEP 654 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0654.rst

원문 ID `08242b9ceb3b4388c7fb10f3`, 문자 위치 0–1766

> PEP: 654
> Title: Exception Groups and except*
> Author: Irit Katriel <irit@python.org>,
>         Yury Selivanov <yury@edgedb.com>,
>         Guido van Rossum <guido@python.org>
> Discussions-To: https://discuss.python.org/t/accepting-pep-654-exception-groups-and-except/10813
> Status: Final
> Type: Standards Track
> Created: 22-Feb-2021
> Python-Version: 3.11
> Post-History: `22-Feb-2021 <https://mail.python.org/archives/list/python-dev@python.org/thread/L5Q27DVKOKZCDNCAWRIQVOZ5DZCZHLRM/>`__,
>               `20-Mar-2021 <https://mail.python.org/archives/list/python-dev@python.org/thread/MQ2UCSQ2ZC4FIGT7KSVI6BJA4FCXSOCL/>`__,
>               `03-Oct-2021 <https://mail.python.org/archives/list/python-dev@python.org/thread/4B256YKUPW5P2M44GG5H6FBL3PSV6ODP/>`__,
> Resolution: https://discuss.python.org/t/accepting-pep-654-exception-groups-and-except/10813/1
> 
> .. canonical-doc:: :ref:`python:lib-exception-groups` and :ref:`python:except_star`
> 
>    See :ref:`python:tut-exception-groups` for a user-focused tutorial.
> 
> Abstract
> ========
> 
> This document proposes language extensions that allow programs to raise and handle
> multiple unrelated exceptions simultaneously:
> 
> * A new standard exception type, the ``ExceptionGroup``, which represents a
>   group of unrelated exceptions being propagated together.
> 
> * A new syntax ``except*`` for handling ``ExceptionGroups``.
> 
> Motivation
> ==========
> 
> The interpreter is currently able to propagate at most one exception at a
> time. The chaining features introduced in :pep:`3134` link together
> exceptions that are related to each other as the cause or context, but
> there are situations where multiple unrelated exceptions need to be propagated
> together as the stack unwinds. Several real world use cases are listed below.
> 
> * **Concurrent errors**.

## old-pep-553-clean/premise

What value of PYTHONBREAKPOINT makes the default breakpoint hook disable debugging?

판정: PEP553 환경변수 절[2]의 PYTHONBREAKPOINT=0 disables debugging과 즉시 None 반환을 그대로 답했다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

The value of `PYTHONBREAKPOINT` that makes the default breakpoint hook disable debugging is `PYTHONBREAKPOINT=0`. This setting causes `sys.breakpointhook()` to return `None` immediately, effectively disabling debugging.

Source 2:  
The default implementation of `sys.breakpointhook()` consults a new environment variable called `PYTHONBREAKPOINT`. This environment variable can have various values: `PYTHONBREAKPOINT=0` disables debugging. Specifically, with this value `sys.breakpointhook()` returns `None` immediately.

수정 후:

The value of `PYTHONBREAKPOINT` that makes the default breakpoint hook disable debugging is `PYTHONBREAKPOINT=0`. This setting causes `sys.breakpointhook()` to return `None` immediately, effectively disabling debugging.

Source 2:  
The default implementation of `sys.breakpointhook()` consults a new environment variable called `PYTHONBREAKPOINT`. This environment variable can have various values: `PYTHONBREAKPOINT=0` disables debugging. Specifically, with this value `sys.breakpointhook()` returns `None` immediately.

수정 후 인용 원문:

[2] PEP 553 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0553.rst

원문 ID `17eba532b6b8433f75abf6e9`, 문자 위치 3845–5787

> Environment variable
> ====================
> 
> The default implementation of ``sys.breakpointhook()`` consults a new
> environment variable called ``PYTHONBREAKPOINT``.  This environment variable
> can have various values:
> 
> * ``PYTHONBREAKPOINT=0`` disables debugging.  Specifically, with this value
>   ``sys.breakpointhook()`` returns ``None`` immediately.
> 
> * ``PYTHONBREAKPOINT=`` (i.e. the empty string).  This is the same as not
>   setting the environment variable at all, in which case ``pdb.set_trace()``
>   is run as usual.
> 
> * ``PYTHONBREAKPOINT=some.importable.callable``.  In this case,
>   ``sys.breakpointhook()`` imports the ``some.importable`` module and gets the
>   ``callable`` object from the resulting module, which it then calls.  The
>   value may be a string with no dots, in which case it names a built-in
>   callable, e.g. ``PYTHONBREAKPOINT=int``.  (Guido has expressed the
>   preference for normal Python dotted-paths, not setuptools-style entry point
>   syntax [syntax]_.)
> 
> This environment variable allows external processes to control how breakpoints
> are handled.  Some uses cases include:
> 
> * Completely disabling all accidental ``breakpoint()`` calls pushed to
>   production.  This could be accomplished by setting ``PYTHONBREAKPOINT=0`` in
>   the execution environment.  Another suggestion by reviewers of the PEP was
>   to set ``PYTHONBREAKPOINT=sys.exit`` in this case.
> 
> * IDE integration with specialized debuggers for embedded execution.  The IDE
>   would run the program in its debugging environment with ``PYTHONBREAKPOINT``
>   set to their internal debugging hook.
> 
> ``PYTHONBREAKPOINT`` is re-interpreted every time ``sys.breakpointhook()`` is
> reached.  This allows processes to change its value during the execution of a
> program and have ``breakpoint()`` respond to those changes.  It is not
> considered a performance critical section since entering a debugger by
> definition stops execution.  Thus, programs can do the following::

## pep-680/clean/candidate

Which standard library module provides the TOML parser for Python packaging tools?

판정: 필수 답 tomllib는 PEP680 제목·초록 인용[1]로 지지된다. bootstrapping과 TOML 도구 설정의 부연도 입력 Source2에 있다. 부연 문장에는 별도[2]가 없어 문장별 인용 완전성의 한계가 있다. 추가 인용 대조: tomllib 이름이 실제로 있는 Abstract [1]로 연결했다. 이름이 없는 Motivation [2]를 붙인 TF-IDF 오류가 없다. PEP680 제목은 tomllib와 표준 라이브러리 TOML 지원을 명시한다. 추출 구절은 bootstrapping 문제를 지지하고, 반환되는 Motivation [2] 전체에는 black·mypy·pytest 등 여러 Python 도구의 TOML 설정도 있다. 인용 평가는 짧은 추출 구절만이 아니라 실제 반환 문단 전체를 기준으로 했다.

수정 전:

The standard library module that provides the TOML parser for Python packaging tools is `tomllib`. This module was introduced as part of PEP 680, which aims to add TOML parsing support to the standard library. The rationale for this addition includes solving bootstrapping problems for Python build tools and providing a standard way to configure various Python tools that use TOML. 

Answer: The `tomllib` module provides the TOML parser for Python packaging tools [1].

수정 후:

[1] The standard library module that provides the TOML parser for Python packaging tools is `tomllib`. [1] This module was introduced as part of PEP 680, which aims to add TOML parsing support to the standard library. [2] The rationale for this addition includes solving bootstrapping problems for Python build tools and providing a standard way to configure various Python tools that use TOML. 

Answer: The `tomllib` module provides the TOML parser for Python packaging tools [1].

수정 후 인용 원문:

[1] PEP 680 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0680.rst

원문 ID `713c4e99e3b1918e5b6dcb9e`, 문자 위치 0–921

> PEP: 680
> Title: tomllib: Support for Parsing TOML in the Standard Library
> Author: Taneli Hukkinen, Shantanu Jain <hauntsaninja at gmail.com>
> Sponsor: Petr Viktorin <encukou@gmail.com>
> Discussions-To: https://discuss.python.org/t/13040
> Status: Final
> Type: Standards Track
> Created: 01-Jan-2022
> Python-Version: 3.11
> Post-History: `09-Dec-2021 <https://mail.python.org/archives/list/python-ideas@python.org/thread/IWJ3I32A4TY6CIVQ6ONPEBPWP4TOV2V7/>`__,
>               `27-Jan-2022 <https://discuss.python.org/t/pep-680-tomllib-support-for-parsing-toml-in-the-standard-library/13040>`__,
> Resolution: https://mail.python.org/archives/list/python-dev@python.org/thread/3AHGWYY562HHO55L4Z2OVYUFZP5W73IS/
> 
> .. canonical-doc:: :mod:`python:tomllib`
> 
> Abstract
> ========
> 
> This PEP proposes adding the ``tomllib`` module to the standard library for
> parsing TOML (Tom's Obvious Minimal Language,
> `https://toml.io <https://toml.io/en/>`_).

[2] PEP 680 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0680.rst

원문 ID `713c4e99e3b1918e5b6dcb9e`, 문자 위치 924–2156

> Motivation
> ==========
> 
> TOML is the format of choice for Python packaging, as evidenced by
> :pep:`517`, :pep:`518` and :pep:`621`. This creates a bootstrapping
> problem for Python build tools, forcing them to vendor a TOML parsing
> package or employ other undesirable workarounds, and causes serious issues
> for repackagers and other downstream consumers. Including TOML support in
> the standard library would neatly solve all of these issues.
> 
> Further, many Python tools are now configurable via TOML, such as
> ``black``, ``mypy``, ``pytest``, ``tox``, ``pylint`` and ``isort``.
> Many that are not, such as ``flake8``, cite the lack of standard library
> support as a `main reason why
> <https://github.com/PyCQA/flake8/issues/234#issuecomment-812800722>`__.
> Given the special place TOML already has in the Python ecosystem, it makes sense
> for it to be an included battery.
> 
> Finally, TOML as a format is increasingly popular (for the reasons
> outlined in :pep:`518`), with various Python TOML libraries having about
> 2000 reverse dependencies on PyPI (for comparison, ``requests`` has about
> 28000 reverse dependencies). Hence, this is likely to be a generally useful
> addition, even looking beyond the needs of Python packaging and related tools.

## old-pep-572-conflict/premise

What notation assigns a name within a Python expression under the assignment expressions proposal?

판정: PEP의 NAME := expr[1]와 Dee 기록의 NAME <- expr[2]를 모두 반환한다. 앞선 실패처럼 원문에 없는 다른 context/variant를 덧붙이지 않았다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

The notation that assigns a name within a Python expression under the assignment expressions proposal is `NAME := expr` [1]. Another source states the notation is `NAME <- expr` [2].

수정 후:

The notation that assigns a name within a Python expression under the assignment expressions proposal is `NAME := expr` [1]. Another source states the notation is `NAME <- expr` [2].

수정 후 인용 원문:

[1] PEP 572 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst

원문 ID `d60afae8bbc6e0863adaf8cf`, 문자 위치 0–2011

> PEP: 572
> Title: Assignment Expressions
> Author: Chris Angelico <rosuav@gmail.com>, Tim Peters <tim.peters@gmail.com>,
>         Guido van Rossum <guido@python.org>
> Status: Final
> Type: Standards Track
> Created: 28-Feb-2018
> Python-Version: 3.8
> Post-History: 28-Feb-2018, 02-Mar-2018, 23-Mar-2018, 04-Apr-2018, 17-Apr-2018,
>               25-Apr-2018, 09-Jul-2018, 05-Aug-2019
> Resolution: https://mail.python.org/pipermail/python-dev/2018-July/154601.html
> 
> 
> Abstract
> ========
> 
> This is a proposal for creating a way to assign to variables within an
> expression using the notation ``NAME := expr``.
> 
> As part of this change, there is also an update to dictionary comprehension
> evaluation order to ensure key expressions are executed before value
> expressions (allowing the key to be bound to a name and then re-used as part of
> calculating the corresponding value).
> 
> During discussion of this PEP, the operator became informally known as
> "the walrus operator". The construct's formal name is "Assignment Expressions"
> (as per the PEP title), but they may also be referred to as "Named Expressions"
> (e.g. the CPython reference implementation uses that name internally).
> 
> 
> Rationale
> =========
> 
> Naming the result of an expression is an important part of programming,
> allowing a descriptive name to be used in place of a longer expression,
> and permitting reuse.  Currently, this feature is available only in
> statement form, making it unavailable in list comprehensions and other
> expression contexts.
> 
> Additionally, naming sub-parts of a large expression can assist an interactive
> debugger, providing useful display hooks and partial results. Without a way to
> capture sub-expressions inline, this would require refactoring of the original
> code; with assignment expressions, this merely requires the insertion of a few
> ``name :=`` markers. Removing the need to refactor reduces the likelihood that
> the code be inadvertently changed as part of debugging (a common cause of
> Heisenbugs), and is easier to dictate to another programmer.

[2] Dee · casebook://messages/53dfa0d0c6823f1309b5acff

원문 ID `ec1d816197eea4516c748e72`, 문자 위치 0–138

> In our language review, assignment inside an expression uses NAME <- expr. That is the notation our review recorded for named expressions.

## old-pep-618-conflict/premise

Which exception does strict zip raise when its iterables have different lengths?

판정: AQA 원출력은 Fay의 LengthMismatchError [1]와 PEP618의 ValueError [4]를 출처별 답으로 함께 남긴다. 모든 strict 조건과 서로 다른 기록을 보존한다. 동일20문항에서 기존19개 답·이전 인용을 보존했다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

The strict zip raises a `ValueError` when its iterables have different lengths [2].

수정 후:

The question asks which exception is raised by the strict zip function when its iterables have different lengths.

Source 1 states that the raised exception is "LengthMismatchError" for iterables of different lengths [1].

Source 4, which provides the specification for the strict zip feature, states that when the built-in zip is called with `strict=True`, the resulting iterator will raise a `ValueError` if the arguments are exhausted at differing lengths [4].

Thus, the answer is:
Source 1 identifies "LengthMismatchError"; Source 4 identifies "ValueError".

수정 후 인용 원문:

[1] Fay · casebook://messages/25ca492f2cdf17bdb4cce7bf

원문 ID `80e3480fa35e216e36d37f05`, 문자 위치 0–137

> Running the strict zip unequal-lengths check, we recorded the raised exception as LengthMismatchError for iterables of different lengths.

[4] PEP 618 contributors · https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0618.rst

원문 ID `44d1a4fcadb2fbfbc6769c81`, 문자 위치 3064–5103

> Rationale
> =========
> 
> Some critics assert that constant boolean switches are a "code-smell",
> or go against Python's design philosophy.  However, Python currently
> contains several examples of boolean keyword parameters on built-in
> functions which are typically called with compile-time constants:
> 
> - ``compile(..., dont_inherit=True)``
> - ``open(..., closefd=False)``
> - ``print(..., flush=True)``
> - ``sorted(..., reverse=True)``
> 
> Many more exist in the standard library.
> 
> The idea and name for this new parameter were `originally proposed
> <https://mail.python.org/archives/list/python-ideas@python.org/message/6GFUADSQ5JTF7W7OGWF7XF2NH2XUTUQM>`_
> by Ram Rachum.  The thread received over 100 replies, with the
> alternative "equal" receiving a similar amount of support.
> 
> The author does not have a strong preference between the two choices,
> though "equal equals" *is* a bit awkward in prose.  It may also
> (wrongly) imply some notion of "equality" between the zipped items::
> 
>     >>> z = zip([2.0, 4.0, 6.0], [2, 4, 8], equal=True)
> 
> 
> Specification
> =============
> 
> When the built-in ``zip`` is called with the keyword-only argument
> ``strict=True``, the resulting iterator will raise a ``ValueError`` if
> the arguments are exhausted at differing lengths.  This error will
> occur at the point when iteration would normally stop today.
> 
> 
> Backward Compatibility
> ======================
> 
> This change is fully backward-compatible.  ``zip`` currently takes no
> keyword arguments, and the "non-strict" default behavior when
> ``strict`` is omitted remains unchanged.
> 
> 
> Reference Implementation
> ========================
> 
> The author has drafted a `C implementation
> <https://github.com/python/cpython/pull/20921>`_.
> 
> An approximate Python translation is::
> 
>     def zip(*iterables, strict=False):
>         if not iterables:
>             return
>         iterators = tuple(iter(iterable) for iterable in iterables)
>         try:
>             while True:
>                 items = []
>                 for iterator in iterators:
>                     items.append(next(iterator))

## F_SH_Top01_002/premise

In the competitive analysis task for the supply chain carbon footprint project, after Huilan Chen completed the analysis of key competitors (especially EcoTrace), which document management system did she upload the final report to?

판정: Huilan Chen의 최종 EcoTrace 보고서 업로드 메시지[2]가 Confluence와 URL을 명시한다. 답은 같은 문서 관리 시스템과 URL을 반환한다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

Source 2: Huilan Chen uploaded the final report to Confluence: https://sd.confluence.net/wiki/spaces/SCT/pages/20250131/EcoTrace+Competitive+Analysis+Report. [2]

수정 후:

Source 2: Huilan Chen uploaded the final report to Confluence: https://sd.confluence.net/wiki/spaces/SCT/pages/20250131/EcoTrace+Competitive+Analysis+Report. [2]

수정 후 인용 원문:

[2] Huilan Chen · EverMemBench-Dynamic@a6b210a32248e841967b7b64a64281d2ff3f669d/01/2025-01-31/Group 3/3

원문 ID `9eed399bd98e29b4f9abd153`, 문자 위치 0–616

> @all Good morning, I have completed the analysis report on our main competitors. It focuses on EcoTrace's features, pricing, and market strategy, especially their Freemium model and user conversion path. The report has been uploaded to Confluence: https://sd.confluence.net/wiki/spaces/SCT/pages/20250131/EcoTrace+Competitive+Analysis+Report. @Weihua Zhang @Jianguo Huang @Guohua Han The core conclusion is that they use a minimalist free collaboration feature as a traffic entry point, and then set up a paywall through powerful data analysis and reporting functions. This strategy is very much worth learning from.

## F_SH_Top01_013/premise

After conducting a technical assessment of the data quality of the production line energy management system, what is the preliminary estimated number of workdays required for data cleansing and initial verification in the report?

판정: Xuexin Yin의 기술 평가 원문[1]에 최소 at least10 working days 및 rule development/initial manual verification이 있다. 최솟값과 조건을 보존했다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

The preliminary estimated number of workdays required for data cleansing and initial verification, as mentioned in the report, is at least 10 working days of data engineer input for rule development and initial manual verification [1].

수정 후:

The preliminary estimated number of workdays required for data cleansing and initial verification, as mentioned in the report, is at least 10 working days of data engineer input for rule development and initial manual verification [1].

수정 후 인용 원문:

[1] Xuexin Yin · EverMemBench-Dynamic@a6b210a32248e841967b7b64a64281d2ff3f669d/01/2025-01-14/Group 1/5

원문 ID `59cc54ef610d1e0d90cfa5c1`, 문자 위치 0–586

> @Mingzhi Li Boss Li, the draft technical evaluation report on the data quality of the production line energy management system has been completed and uploaded to the project folder. The core conclusion is that the automated cleaning of this data source is quite difficult, and it is initially estimated that at least 10 working days of data engineer input will be required for rule development and initial manual verification. It is recommended to clearly define this part of the work as a "data preprocessing" sub-task in the scope statement and establish separate acceptance criteria.

## F_SH_Top01_033/premise

When reviewing the first draft of the user interview outline for the carbon emissions management platform, who suggested adding questions about customizable reporting dimensions to address the needs of managers and auditors?

판정: 작성자 메타데이터가 Lizhen Zhou인 I suggest 메시지[2]와 Boss Zhou의 제안을 반영했다는 Luhao의 후속[3]이 답을 지지한다. @Luhao 수신자를 제안자로 바꾸지 않았다. 기존 답과 인용을 보존한다. 추출 후보가 계약을 벗어난 경우 새 인용은 추가하지 않았다.

수정 전:

Source 2: Lizhen Zhou suggested adding questions about customizable reporting dimensions to address the needs of managers and auditors. [2]  
Source 3: Boss Zhou's suggestion regarding customizable report dimensions was incorporated. [3]

수정 후:

Source 2: Lizhen Zhou suggested adding questions about customizable reporting dimensions to address the needs of managers and auditors. [2]  
Source 3: Boss Zhou's suggestion regarding customizable report dimensions was incorporated. [3]

수정 후 인용 원문:

[2] Lizhen Zhou · EverMemBench-Dynamic@a6b210a32248e841967b7b64a64281d2ff3f669d/01/2025-01-24/Group 1/5

원문 ID `a7c4bd0229d9d3643b13546f`, 문자 위치 0–402

> @Luhao Zhao I've read the outline, and it's well-written. Regarding the sections for managers and audit requirements, I suggest adding a question: "What customizable dimensions would you like the generated reports to have? For example, by time, by emission source, by branch company, etc." This is crucial for our subsequent report design. @Yu Su's suggestion is also very good; data is the foundation.

[3] Luhao Zhao · EverMemBench-Dynamic@a6b210a32248e841967b7b64a64281d2ff3f669d/01/2025-01-27/Group 1/21

원문 ID `99c7f4ad8d9189eddf4a1e25`, 문자 위치 0–530

> Everyone, the final version of the user interview outline has been updated on Confluence. I've incorporated Boss Zhou's suggestion regarding customizable report dimensions and refined the questions Yu Su mentioned about exploring the current data processing workflow for operations personnel. I believe the current version is ready for the upcoming interview arrangements. I've marked this task as complete. Thank you all! 🎉 https://sd.confluence.com/pages/viewpage.action?pageId=1234567890/User+Interview+Outline+V-Final_20250127
