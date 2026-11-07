# 문단 ID 독해·실제 검색 비교 결과

계획한 구현과 고정 비교를 완료했다. **후보를 기본 경로로 채택하지 않는다.** 기존 선택 경로는 attributed다.
선택기의 optional 검색과 필수 구절 복사 단계를 제거했지만, 필요한 기록 선택·상충 답 보존·인용 관련성은 해결하지 못했다.

| 비교 | 정답값 | 답·근거·인용 관련성 모두 통과 |
|---|---:|---:|
| 기존20 / 단순 독해 direct | 19/20 | 18/20 |
| 기존20 / 한 호출 con 독해 | 19/20 | 17/20 |
| Ever10 / BM25 + direct | 3/10 | 2/10 |
| Ever10 / BM25 + con | 2/10 | 2/10 |
| Ever10 / Contriever + direct | 3/10 | 1/10 |
| Ever10 / Contriever + con | 2/10 | 1/10 |

이전 attributed의20/20은 과거 고정 결과이며 이번에 새로 실행한 control이 아니다.
위 표는 이번 실행에 대해 **불필요하게 붙인 무관 인용도 실패로 보는** 사전 고정 기준이다.
과거 다른 후보의 점수를 이 강화된 기준으로 자동 소급한 비교가 아니다.

## 유지할 구현과 채택하지 않을 변경

- 문단 ID를 먼저 부여하고 시간순 표시 후에도 원문에 연결하는 계약은 구현됐다.
  80개 실제 요청/출력을 재생했고151개 반환 문단 연결이 동일했다. 의미 지지 검증을 뜻하지 않는다.
- breakpoint의 정답0과 RST 원문 근거는 복구됐다. 구절을 다시 복사하지 않으므로
  backtick/들여쓰기 차이로 올바른 답을 버리는 실패가 없다.
- 단순 독해도 strict zip에서 한쪽 답을 누락했다. direct는LengthMismatchError,
  con은ValueError만 반환했다. 기존에 맞힌20문항 모두를 보존하지 못했다.
- clone 답은origin/upstream 모두 맞지만 branch fetch/push 문단을 clone 기본값 근거로
  추가했다. con은 assignment 표기를 다른 언어라고 추측하는 부연도 덧붙였다.
- Contriever의 관련 기록 R 회수는22/290→10/290으로 줄었다. 이는 전체 관련 기록 수이며
  최소 충분 근거 확보율이 아니다. 색인 key 잘림은0건이다. 공개 dense 방식이라는 이유로
  이 데이터에서 BM25보다 낫다고 가정할 수 없다.
- S3는BM25 입력에4/7의 last Friday와4/10 완료가 있는데도10일/3일로 잘못 답했다.
  반면 새 과제 간격은두 번째 과제 자체를 못 찾았다. 검색과 독해 실패가 함께 존재한다.
- dense direct의polling 문항은정답 문자D만 맞았다. 인용은IoT 시험 기록이라 정책을
  지지하지 않는다. 이를 성능 개선으로 세지 않는다.

## 경계 사례와 검증 실패를 숨기지 않음

Hanqiang 문항의BM25 direct는9/18 완료 기록의 **작성자**를 맞혔다.
그러나 응답의 “according to Mingzhi's reminder”는질문 전제를 반복했을 뿐 인용은
본인 완료 보고다. 모든 주장의 출처 귀속까지 요구한 주점수에서는미통과로 남겼다.
질문에 주어진 reminder 전제의 반복을 허용하면BM25 direct는답·근거3/10이다.
이 민감도 차이를 적용해도 기존20 보존 실패와dense 교체 기각은달라지지 않는다.

한 호출(Ever MA_P_Top02_083 / BM25 con)은1024 출력토큰에서length 종료하여JSON 파싱에
실패했다. 원래 동결한 verify.py의 all-stop 검사는 실패 상태 그대로 보존했다.
추가 verify_with_truncations.py는 이 실패를 기록하면서 80개 요청/출력의 정확한 재생과
151개 원문 연결을 검사하는 진단용이다. 원 채점 기준·코드·응답을 고치거나 재호출하지 않았다.
4개 추가 출력은 3개 초과 문단 인용으로 partial이며 이들을 정상 결과로 간주하지 않는다.

## 실행·재현

Aurora120296: GPU1, 고정12시간, conda, scheduler 배정g6, COMPLETED/0:0.
실사용 12분 29초(12.48 GPU분), 다운로드/색인/서버 준비 포함. 모델 API 비용 0.
원문 20,328개를 같은 512/64 corpus로 색인했고 BM25 top8은 기존 10개 입력과 정확히 일치했다.
Qwen3-8B 80회, 입력 230,514/출력 11,207토큰. 전 문항 QA당 1회.
로컬 계약 테스트 19개 통과. batch MaxRSS 2,466,368KB는 Slurm 기록이며 GPU VRAM 수치가 아니다.

- [수정 의도와 사용법](../../../docs/reference-documents.md)
- [사전 고정 계획](PROTOCOL.md)
- [문항별 실제 답·원문·판정](cases.md)
- [기계 판정·채택 기준](summary.json)
- [실제 호출](calls.jsonl), [검색 결과](retrieval.json), [고정 해시](freeze.json)

```sh
.venv/bin/python -m evaluation.reference_qa.documents.verify
# 위 원검사는 보존된length 실패에서 멈춘다. 아래는 실패를 포함한 진단 재생이다.
.venv/bin/python -m evaluation.reference_qa.documents.verify_with_truncations
.venv/bin/python -m evaluation.reference_qa.documents.report score
```

30개 노출 개발 문항의 조건별 비교이며 전체 벤치마크 성과가 아니다. 새 병합·재검토 평가는
수행하지 않았다. 기본 경로를 교체하지 않고 실행 가능한 후보/API와 반례를 남긴다.
