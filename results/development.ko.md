# 개발 단계에서 확인한 것

## Aimers와 합성 대조

한 팀원의 기록에서 TabM은 기존 블렌드에서 기여가 없어 기각됐다. 다른 팀원은 TM-S를 다른 블렌드에 넣어 자신의 기준에서 개선을 측정했다. 기대 조치는 앞선 관측을 보존하면서 원래 작성자의 조건에서 재비교하는 것이었다. [기각 기록](https://github.com/ashcircle03/Aimers9th-KHU-swcon22/blob/a8e64a1d52a0daa1ee7bf4595a0dfe4e6acf49a3/jaewon/notes/findings.md#L484-L503) · [새 비교 기록](https://github.com/ashcircle03/Aimers9th-KHU-swcon22/blob/9bf532cde00494dabb86076e16a07940a47400e3/seonghun/docs/experiment_log.md#L377-L403)

같은 Qwen으로 실제 Aimers 1건과 합성 4건을 평가했다. 기대 조치와 일치한 건 직접 읽기 2/5, 모듈 3/5였다. 차이가 난 1건은 측정 전 아이디어였고, 모듈의 근거 확인 규칙이 재비교 제안을 걸렀다. Aimers에서는 두 방식 모두 재비교를 골랐다. 사례마다 과거 후보 문서가 두 개여서 더 큰 외부 프로젝트에서 다시 검증했다. [CPython 비교](cpython/report.ko.md)

## EverMemBench-Dynamic 개발셋

자동 작성된 기록을 사용한 기존 QA는 원본 5문항 중 2문항에서 답과 근거를 맞혔다. 5문항 각각에 답이 갈리도록 두 발언을 추가한 통제 변형에서는 양쪽 근거를 모두 검색했지만 두 답과 출처를 함께 반환한 건 0/5였다. 이 수치는 개발 문항에 대한 프로젝트 내부 판정이다. 공식 벤치마크 점수와 구분한다. [데이터 출처](https://huggingface.co/datasets/EverMind-AI/EverMemBench-Dynamic)
