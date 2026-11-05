# 복수 근거 QA 보존

답·조건·원문 인용과 충돌의 미해결 표시를 따로 판정했다. 배열이나 중첩 형태여도 실제로 전달한 근거는 인정했다.

| 문항 | 조건 | 반환한 답과 인용 ID | 양측 근거 | 상태까지 보존 |
|---|---|---|---|---|
| d01 | A | origin [https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/clone.adoc#L1-L12] / upstream [trial://worklog/646956c0e537938abf1125c2] | 1 | 0 |
| d01 | B | origin [https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/clone.adoc#L1-L12] / upstream [trial://worklog/646956c0e537938abf1125c2] | 1 | 0 |
| d01 | C | origin [https://github.com/git/git/blob/683c54c999c301c2cd6f715c411407c413b1d84e/Documentation/config/clone.adoc#L1-L12] / upstream [trial://worklog/646956c0e537938abf1125c2] | 1 | 0 |
| d07 | A | 근거 없음 | 0 | 0 |
| d07 | B | For freshwater sites, the L-2 cartridge should be used. [trial://worklog/4aa08d0501e153ad28103fe5] / At brackish sites, the B-8 cartridge should be used. [trial://worklog/e288efd3c457166052d3dc9a] | 1 | 1 |
| d07 | C | 근거 없음 | 0 | 0 |
| pep-572-conflict | A | NAME := expr [https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst] | 0 | 0 |
| pep-572-conflict | B | NAME := expr [https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst] | 0 | 0 |
| pep-572-conflict | C | NAME := expr [https://github.com/python/peps/blob/16991a9ce7b223b38f0b473f51a8a7d94c8b9249/peps/pep-0572.rst] | 0 | 0 |
| pep-618-conflict | A | LengthMismatchError [casebook://messages/25ca492f2cdf17bdb4cce7bf] | 0 | 0 |
| pep-618-conflict | B | LengthMismatchError [casebook://messages/25ca492f2cdf17bdb4cce7bf] | 0 | 0 |
| pep-618-conflict | C | LengthMismatchError [casebook://messages/25ca492f2cdf17bdb4cce7bf] | 0 | 0 |

[원출력과 전체 인용 문단](multisource-outcomes.json)
