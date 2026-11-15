# 문항별 검색·QA 보존 비교

같은 실제 embedding checkpoint의 검색 비교다. 답변 QA는 별도의 고정 근거·정확한 요청 재생이다. 새 Qwen 추론은 없다. 세부 source ID·원문·offset·작성자·시각은 [retrieval.json](retrieval.json)에 모두 남아 있다.

| 사례 | 질문 | 기존→준비 | 재시작 | 추가 전→후 | 추가 후 증분→전체 | QA 기록 재생 |
|---|---|---:|---:|---:|---:|---:|
| legacy-d474ab3d7822c8ac/qa-0 | Which style does Git use by default for printing fetch ref update status? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-d474ab3d7822c8ac/qa-1 | Which alternate merge conflict style removes matching lines near either edge of the conflict region? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-d474ab3d7822c8ac/qa-2 | What default subject prefix does format-patch put on its output? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-d474ab3d7822c8ac/qa-3 | If nobody specifies a notes merge strategy, which strategy resolves notes conflicts by default? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-d474ab3d7822c8ac/qa-4 | Which Git configuration option chooses between basic and extended when grep.patternType is set to default? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-ae24415845ae48a7/qa-0 | What name does a newly cloned repository give its remote by default? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-d30bb1f10fe4bfe8/qa-0 | Which cartridge should each sampler use for collecting field water? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-702e9009795b2802/qa-0 | If system time zone data is unavailable, which PyPI package supplies the fallback for zoneinfo? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-702e9009795b2802/qa-1 | What notation assigns a name within a Python expression under the assignment expressions proposal? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-702e9009795b2802/qa-2 | Which warning category signals omitted encoding when open uses the locale default? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-702e9009795b2802/qa-3 | Which exception does strict zip raise when its iterables have different lengths? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-702e9009795b2802/qa-4 | Which namespace exports the low-impact interpreter monitoring functions and constants? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-702e9009795b2802/qa-5 | What syntax handles exception groups in the proposal for multiple unrelated exceptions? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-702e9009795b2802/qa-6 | What value of PYTHONBREAKPOINT makes the default breakpoint hook disable debugging? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-702e9009795b2802/qa-7 | Which standard library module provides the TOML parser for Python packaging tools? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-1d2a1e3271adf133/qa-0 | What notation assigns a name within a Python expression under the assignment expressions proposal? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-c000762632771ec9/qa-0 | Which exception does strict zip raise when its iterables have different lengths? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-34429cce545ccddd/qa-0 | In the competitive analysis task for the supply chain carbon footprint project, after Huilan Chen completed the analysis of key competitors (especially EcoTrace), which document management system did she upload the final report to? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-34429cce545ccddd/qa-1 | After conducting a technical assessment of the data quality of the production line energy management system, what is the preliminary estimated number of workdays required for data cleansing and initial verification in the report? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
| legacy-34429cce545ccddd/qa-2 | When reviewing the first draft of the user interview outline for the carbon emissions management platform, who suggested adding questions about customizable reporting dimensions to address the needs of managers and auditors? | 동일 | 동일 | 동일 | 동일 | 답·근거 동일 |
