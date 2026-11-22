# 실제 기록 기반 Retrieval 평가

GitBugs Thunderbird는 새 이슈를 등록했을 때 이전 중복 이슈를 찾아야 하는 F02 평가다. QMSum은 회의가 끝난 후 특정 질문과 관련된 발화를 찾는 F05 평가다. 두 자료는 양성 질문으로 구성한다. 실행 가능한 입력과 정답은 data/에 있으며, 전체 요약은 build-report.json, 기준 검색 결과는 bm25-metrics.json에서 확인한다.

## 바로 실행

Python 3.9 이상에서 이 디렉터리를 작업 경로로 사용한다. 동결 데이터를 채점할 때 네트워크나 모델이 필요하지 않다.

```sh
python3 evaluate.py inputs /tmp/public-inputs.jsonl
python3 evaluate.py baseline /tmp/bm25.jsonl
python3 evaluate.py score /tmp/bm25.jsonl
python3 -m unittest discover -s .
python3 verify.py
shasum -a 256 -c SHA256SUMS
```

제품 검색기는 첫 명령의 각 행에서 query와 candidates만 읽는다. F02의 candidates는 이미 등록 시점 이전으로 제한돼 있다. F05에서는 질문이 속한 회의의 전체 발화만 제공한다. 테스트셋에서 파라미터를 조정하지 않는다. 원자료의 사후 메타데이터, 정답 파일 및 미래 문서가 섞인 전체 pool은 검색기에 입력하지 않는다.

예측은 모든 문항에 대해 다음 형식의 JSONL 한 행씩 작성한다. ranked는 관련도 내림차순의 ID 배열이다. 동점은 ID 오름차순으로 정렬한다. final은 관계 확장과 예산 적용이 끝난 실제 전달 목록이다. 여기서는 한 문서 또는 발화 전체가 반환 단위다. F05 최종 묶음 예산은 5개 및 4,000 Unicode 문자다. 오류는 status=error 및 두 빈 배열로 명시한다. 정상 빈 결과는 status=ok다.

```json
{"id":"<입력 행의 id>","status":"ok","ranked":["<후보 id>"],"final":["<후보 id>"]}
```

## 지표 해석

- F02는 문서 MRR과 문서 Recall을 K=1,3,5에서 계산한다. 순위에서 같은 문서를 처음 한 번만 센다. 정답은 연결이 확인된 과거 이슈 ID다. 이 데이터에는 정답 본문 구절이 없다.
- F05는 범위별 발화 하나 이상 적중을 기준으로 Recall과 첫 적중 MRR, 모든 주석 범위 적중률을 측정한다. turn_recall은 주석된 개별 발화의 회수율이다. 긴 범위에서 한 발화만 찾았을 때와 충분히 찾았을 때를 구별한다. final_all_ranges는 실제 최종 목록이 모든 주석 범위에 닿은 문항 비율이다. 회의 발화 관련성 주석은 정정 승인 상태나 최종 답변의 의미 적절성을 보증하지 않는다.
- 데이터셋별·양성 문항별 산술평균을 보고한다. 실패는 양성 검색 점수 0이며 정상 빈 결과와 구분한다. 두 자료 모두 확인된 음성 정답이 없어 음성 오반환율은 산출 대상 밖이다. 실제 승인 전후와 음성 진단은 별도 팀 기록으로 평가한다.
- BM25 기준선은 영문 소문자 단어 토큰, k1=1.2, b=0.75, 발화에는 발화자 이름 포함, query 중복 토큰 제거를 사용한다. 양의 어휘 일치가 없는 문서는 생략한다. 검색 단위와 후보 풀·예산이 동일한 조건에서 비교한다.

## 선정과 누출 검사

**GitBugs.** 공식 CSV에서 같은 프로젝트의 중복 연결을 해석하고 모든 정답이 새 이슈보다 엄격하게 먼저 생성된 경우만 사용한다. ID·링크·이메일·직접 중복 단서가 의심되는 제목, 짧은 제목, 정답 제목과 정규화 텍스트가 같은 경우를 제외한다. 해시 순서로 양성 후보 600개와 배경 후보 최대 650개를 먼저 선정해 고정된 후보 풀을 만든다. 여기에 과거 정답을 추가하고 전체 풀에 같은 제목 이력 검사를 적용한다. 적격 과거 후보가 100개 미만이거나 질의 제목이 과거 제목과 같으면 질의를 제외한다. 배경 사례의 비관련성은 전수 주석되지 않았다. 프로젝트 전체 대상 공식 점수와 구별한다.

공개 Mozilla Bugzilla에서 생성 시각과 현재 제목이 CSV와 일치하고, 공개 변경 이력에 summary 변경이 없는 이슈만 채택한다. 검색 필드는 검증된 제목 하나다. 본문 버전·댓글·사후 상태·중복 ID는 입력에서 제외한다. 데이터셋 ID는 이슈 번호를 해시한 값이다. 중복 연결은 사후 판정한 채점 정답으로만 사용한다. 원본에 그대로 남은 간접적인 의미 단서까지 제거했다는 보장은 없다. [GitBugs 원본](https://github.com/av9ash/gitbugs/tree/eadf2d6794990a1aaa26d0ae15391f29f8969301/thunderbird) · [Mozilla 변경 이력 API](https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html#bug-history)

**QMSum.** 공식 ALL/test의 specific_query_list만 사용한다. 범위 양끝이 실제 발화 번호 안에 있고 역전되지 않는지 확인한다. 정규화 질문 중복, 전체 정답 요약을 포함한 질문, 주석 필드·직접 발화 범위를 가리키는 패턴 등을 제외한다. 답 요약·주제·범위는 검색 입력에 넣지 않는다. 회의 종료 후 질의이므로 내부의 모든 발화가 검색 가능하며, 회의 도중 미래 발화 예측을 평가하지 않는다. [QMSum 원본](https://github.com/Yale-LILY/QMSum/tree/83d7768c1f2b4dfeb091385d3dc7e239b8e5bb7e/data/ALL/jsonl)

## 재생성

원본 GitBugs Thunderbird_bugs.csv 및 Thunderbird_bugs-combined.csv를 각각 bugs.csv 및 pairs.csv로, QMSum ALL/jsonl/test.jsonl을 meetings.jsonl로 원자료 디렉터리에 저장한다. 같은 디렉터리에 동봉한 audit.json을 복사한다. 이 파일은 이슈별 감사 판정만 포함한다. build.py가 원본 SHA-256을 확인한다. 공개 이력을 새로 확인하려면 기존 audit.json이 없는 원자료 디렉터리를 audit_titles.py에 넘긴다. 이미 판정한 ID는 캐시에서 재사용한다. 이후 공개 메타데이터·접근 상태의 변화로 판정이 달라질 수 있다.

```sh
python3 build.py /path/to/raw --output /tmp/rebuilt-public
diff -qr data /tmp/rebuilt-public
```

## 팀 Retrieval 재실행

[실측 결과와 95% 신뢰구간](team-comparison.md). 프로젝트 루트를 PYTHONPATH에 추가하고 requirements-reference.txt의 팀 환경에서 실행한다. MODEL_DIR은 팀 설정의 sentence-transformers/all-MiniLM-L6-v2 리비전 1110a243fdf4706b3f48f1d95db1a4f5529b4d41, TOKENIZER_DIR은 Qwen3-8B 토크나이저 디렉터리다. 질문 생성·재순위화 LLM 서버는 필요하지 않다.

```sh
export PYTHONPATH="$(git rev-parse --show-toplevel)"
python3 run_team.py --task F02 --cache /tmp/public-team-index --model "$MODEL_DIR" --tokenizer "$TOKENIZER_DIR" --output /tmp/f02.jsonl
python3 run_team.py --task F05 --cache /tmp/public-team-index --model "$MODEL_DIR" --tokenizer "$TOKENIZER_DIR" --output /tmp/f05.jsonl
cat /tmp/f02.jsonl /tmp/f05.jsonl > /tmp/team.jsonl
python3 evaluate.py score /tmp/team.jsonl
python3 compare.py /tmp/team.jsonl
```
