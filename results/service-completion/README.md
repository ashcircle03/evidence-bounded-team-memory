# 서비스 경계 수정: 오픈소스 코드 검토와 실제 Qwen 검증

2026-11-08. **상태·인용 연결은 개선됐지만 자동 재검토까지 완성하지 못했다.**
현재 작업 소스는 v3b다. v4 후보는 채택하지 않았다. 이번 결과를 새로운 독립
벤치마크 성능이나 원 논문의 재현 성공으로 제시하지 않는다.

## 무엇을 가져왔는가

[설계와 pinned 파일 링크](../../docs/service-completion-design.md),
[revision 목록](../../evaluation/service_completion/opensource-references.json).

- Mem0: 현재 메모리와 변경 이력의 분리. 기존 Git 원문·제안·투표를 유지했다.
- Graphiti: 문서 전체보다 개별 주장과 출처·시각을 연결하는 경계. 정정 context와 적용 assertion을 분리했다.
- LangChain HITL: 제안과 승인된 실행의 구분. rejected를 문맥에서 삭제하지 않고 변경 미적용 상태를 전달했다.
- 실제 사용 중인 LlamaIndex CitationQueryEngine: 검토 snapshot도 최초 생성부터 번호가 붙은 자료로 제공한다. 사후에 인용 없는 문장만 고치던 경계를 줄였다.
- 기존 ConflictScore 전송 어댑터: 작성자·시각을 유지하고 upstream 요청4096토큰을 실제 남은 context 안에서 존중한다. 로컬384 강제로 최종 판단 필드를 자르던 문제를 고쳤다.

Mem0/Graphiti/LangChain HITL 전체를 설치해 실행한 것은 아니다. 코드에서 확인한
상태 관리 패턴을 기존 서비스에 적용했다. 새 중앙 graph DB나 추가 판정 모델은 없다.

## 현재 구현 v3b 결과

Qwen3-8B, revision `b968826d9c46dd6066d109eabc6255188de91218`, nonthinking,
temperature0. Aurora GPU 계산 노드·conda에서 실행했으며 유료 API 호출은 없다.

| 범위 | 핵심 답 | 답+필요 근거 |
|---|---:|---:|
| 기존 개발20, 전체 원문에서 새 검색·추론 | 20/20 | 20/20 |
| 알려진 합성8흐름의11 QA시점 | 9/11 | 8/11 |
| 추가 합성3흐름의6 QA시점 | 6/6 | 6/6 |

- 기존20 중19개는 정답 키의 근거 위치까지 직접 일치했다. `grep.extendedRegexp`는 같은 Git 문서 L14-L18을 인용했고, 그 문단이 해당 옵션과 patternType=default 조건을 지지함을 직접 검토했다. 키의 L7-L13을 사후 변경하지 않았다.
- 상태 적용을 직접 묻는8시점(release pending/approved, calendar rejected, temperature pending/approved, retention current/proposal, conflicting votes)은 값·상태와 실제 snapshot 인용을 확인했다. v2에서는 이8개 중2개만 검토 snapshot을 직접 인용했다.
- release pending은 새 제안값을 snapshot 안의 원문 연결로 추적할 수 있지만 신규 원문을 직접 별도 인용하지 않았다. 사전의 엄격한 ‘원문 양쪽+상태’ 요구에서는 실패로 남겼다.
- writer/cache 재검토 설명은 각각 원문에 없는 이유 추가, 필요한20초 조건 누락과 정정 오분류가 있어 실패로 판정했다.
- 정상 실행과 의미 성공은 다르다. 응답24개는 ok,13개는 partial이다. 부분 출력·교체 경고도 그대로 남겼다.
- 이 점수는 핵심 답과 필요한 근거에 대한 구현 AI의 원문 검토다. 독립/블라인드 사람 평가도, 모든 부연 문장의 인용 완전성 점수도 아니다.

[37개 질문·답·실제 인용](v3b/cases.md) · [문항별 판정 이유](v3b/ratings.json) ·
[집계](v3b/summary.json) · [구조 검증](v3b/verification.json).

## QA가 맞아도 제안이 틀린 경우

재검토 양성 writer/cache2건 모두 **reconsider 대신 correction**을 냈다.
무관한 writer/cache 보고2건에도 불필요한 correction을 냈다. 따라서 올바른
재검토 종류0/2, 음성 불필요 제안2/2다. QA가 ‘기존 이유가 바뀌지 않았다’고
답해도 이미 생성한 잘못된 제안이 자동으로 사라지는 것은 아니다.

[제안별 원문·종류·이유](v3b/relation-audit.json), [완성 기준 미달 결정](decision.json).
구조·출처가 유효하다는 사실은 관계 분류의 의미가 맞다는 증거가 아니다.

## 실패를 보존한 실행 이력

| 버전/job | 실제로 확인한 것 | 처리 |
|---|---|---|
| v1 /120381 | 복사한 assertion의 대소문자 등이 원문과 달라 정정 제안이 거절되고 상태 QA 실패 | 원출력 보존 |
| v2 /120382 | 문장 ID로 원문 복원; 상태 값은 개선됐지만 이미 달린 문서 인용 때문에 승인 기록 인용이 빠짐 | 원출력 보존 |
| v3 | 제출 전 기존 번호의 review source 처리 누락 발견 | 미제출, GPU사용0 |
| v3b /120383 | 초기부터 상태 source를 번호화; 기존20 보존, 상태8시점 인용 확인 | 현재 작업 소스, 전체 수용 기준은 미달 |
| v4 /120384 | 기존 비교 지침 복원 후보도4건에서 assertion ID 누락, 조건 변경 오분류 | 채택하지 않음 |

v2/v3b의11개 비교 HTTP 입력과 출력은 모두 동일했다.
[대조 기록](comparison-transport-audit.json). 상태 근거 연결이 관계 분류기를
고쳐 주었다고 주장하지 않는다. v4의 실패 출력을 v3b 성과와 합산하지 않는다.

각 실행의 `runtime/`, `freeze.json`, `result.json`, `calls.jsonl`, `server.json`,
`dispatch.json`, `slurm.log`를 함께 보존한다. 현재 버전만 읽을 때는 `v3b/`를 사용한다.
모든 실행의 실제 할당 시간과 호출비는 [accounting.json](accounting.json)에 합산했다.
대기/준비·실패 후보도 비용에 포함하고,12시간은 실제 사용시간이 아닌 walltime 상한이다.

이번4개 실행은 총 **139.77 GPU분·841회 모델 호출**이었다. 현재 v3b만은
35.58 GPU분·222회다. v2의202회보다20회 늘었다. 별도 판정 단계를 추가하지
않았어도 상태 자료가 문서 검토에 들어가고 답이 달라지면서 실제 호출은 증가했다.
원문/영수증을 공유 파일시스템에 개별 저장하는 시간도 포함되므로 이 시간을
순수 모델 추론 속도 비교로 해석하지 않는다.

## 한계와 결정

입력은 기존20+합성17의 반복 개발/회귀 묶음이다. 추가6도 수정 과정에서 다시
읽었으므로 독립 holdout이 아니다. 기존20 중 자연 EverMem은3문항이며 이번에는
EverMem10 전체나 새 WikiContradict를 다시 실행하지 않았다. 앞선 reader 비교는
고정 passage 조건이므로 이번 전체 검색 결과와 동일 조건의 인과 비교를 하지 않는다.

승인 fixture는 실제 사용자의 인증을 검증하지 않는다. 문장 단위 assertion은
한 문장 안의 복수 사실까지 분해하지 않는다. 상태 snapshot은 제안별 효과와
해당 시점의 유효 투표를 표현하며 세계 사실의 참/거짓을 인증하지 않는다.

298개 전체 계약 검사와14개 분리 패키지 검사를 통과했다. v4의 마지막 프롬프트
변경은 관련20개와 패키지14개를 검사했지만 실제 모델 평가를 통과하지 못했다.
UI/MCP를 추가하거나 팀원의 역할을 대신하지 않았다.
