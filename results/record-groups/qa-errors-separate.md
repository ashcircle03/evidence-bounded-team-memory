# QA 오류는 records 구성 성과와 분리

이번 records-only 실행은 새 QA를 돌리지 않는다. 아래는 이전 실제 모델 요청·응답에서
확인한 오류의 위치이며, 이번 수정으로 해결했다고 보고하지 않는다.

| 기존 관찰 | 원문/역할 정보 상태 | 오류 분류 |
|---|---|---|
| 계정 잠금 raw D → linked B, 이메일을 보낸다고 답함 | 초기 QA에 전체 원문과 `halt_downstream_triggers=true`가 있음 | 원문 검색 누락이 아닌 QA 해석/선택 오류. graph 표현이 유발했는지는 별도 통제 비교가 필요 |
| v1 call49 ConflictScore `IRRELEVANT` | 해당 검사 요청에도 halt=true 원문이 있음 | 문서–답변 관계 판단 오류. records에 새 필드를 넣었다고 해결되지 않음 |
| `last Friday` 사건을4/7로 옮김 | v2에서 원문 시간 표현이 graph에도 있음 | 상대시간 해석 오류. 원본 무시간대 timestamp에 UTC를 붙인 importer 관례도 따로 고려 |
| 원거리 version4/CPU 조건 누락 | 원문 전체에는 있으나 claim condition edge가 비어 있음 | records 구성 누락과 reader 해석 실패가 함께 관찰됨. 전자를 이번 비교 대상으로 삼음 |
| 두 명/두 업무의 담당자 대응 | 원문 자체의 개별 대응이 모호함 | 데이터 모호성을 저장 성공이나 QA gold 일치로 해소했다고 부르지 않음 |

근거: [실제 v1/v2 입력 전달 검증](../record-graph/README.md#단계별-증거와-측정-범위),
[문항별 원출력 대조](../record-graph/cases.md), [원출력 JSON](../record-graph/cases.json).

기존20문항130요청의 재생은 새 opt-in grouped graph를 쓰는 QA 성능 검증이 아니다.
raw 기본 경로의 답·근거가 그대로라는 호환성 검사이며, 기존8문항11미인용 구절도 남는다.
