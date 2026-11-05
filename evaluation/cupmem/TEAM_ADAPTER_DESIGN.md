# CUPMem 위에 붙이는 팀 기록 어댑터

이 문서는 현재 개발 선택의 의도·근거·재사용 범위를 명시한다. SpeakerMem-R1 주 베이스라인 교체나 논문 성능 재현을 선언하지 않는다.

| 선택 | 해결하려는 문제와 근거 | 재사용 / 추가 범위 |
|---|---|---|
| CUPMem 기억 작성·갱신 | 기록 누적과 과거 전제 갱신을 매번 다시 구현하지 않는다. 원형에는 writer, update resolver, invalidation, stale/successor 연결이 있다. 실제 119767에서 배포 조건 변화와 이전 결정을 연결했다. | 공식 revision ea7d391103a151927cd29d2f01d87597a782bdcb의 write_session을 그대로 사용한다. |
| CUPMem 검색·질문 처리 | 원문 전체를 단일 프롬프트에 넣는 새 시스템에서 출발하지 않는다. 원형의 retrieval, premise verifier, basis recovery, answer composer를 사용한다. | answer_query 원형 유지. 원형 답도 항상 보존한다. |
| 팀 기록 → 세션 | 원문·작성자·시각을 누락하지 않고 기존 엔진에 입력해야 한다. | 이미 있는 attributed_session을 사용한다. 사람별 개인 프로필 성능이 팀 기록에 그대로 이전된다고 가정하지 않는다. |
| 선택된 기억 → 원문 | 119767에서 40초·12초·Cedar-audit은 원문에 있었지만 기억 요약과 최종 답에서 빠졌다. | 이미 있는 resolve_grounding을 재사용한다. CUPMem이 선택한 기억의 출처만 펼친다. 새 검색기나 전체 원문 fallback은 만들지 않는다. |
| 상태 변화의 원인 원문 포함 | 119767의 과거 이유·바뀐 조건 질문은 옛 기억만 value 근거로 선택했고, 새 조건은 status_cause 연결에 남았다. | 기존 resolver가 추적한 명시적 상태 원인 링크만 추가 독해 대상으로 삼는다. 어떤 입력에서나 도움이 된다는 가설은 아직 검증하지 않았다. |
| 원문 ID로 인용 | 이전 구현은 인용 문자열 생성 오류 때문에 답 전체를 잃었다. | 기존 core의 원문 위치·ID 해석만 최종 reader에 재사용한다. 의미 정확성 자동 검증을 주장하지 않는다. |
| 승인 외부화 | 모델의 권고가 팀의 승인으로 변하면 안 된다. | 결과는 not_approved. 승인·Git/MCP 연결은 호출자 영역이다. |

## 기존 접근과의 관계

작은 표현으로 검색한 뒤 연결된 원문을 읽는 방식은 기존 ParentDocument/MultiVector retrieval 방식과 같은 방향이다. [LangChain 공식 MultiVectorRetriever 문서](https://reference.langchain.com/python/langchain-classic/retrievers/multi_vector/MultiVectorRetriever)는 작은 청크로 검색하고 부모 문서를 반환하는 동작을 설명한다. 여기서는 별도 벡터 저장소를 추가하지 않고 CUPMem이 이미 선택한 memory→delta/chunk→원문 연결을 사용한다. 이 원문 확장 자체를 새로운 연구 기여로 주장하지 않는다.

CUPMem의 STALE 상태는 특정 기억의 상태이며 그 원문 문서 전체의 모든 사실을 폐기한다는 뜻으로 확장하지 않는다. 이는 사용자 문제 정의의 조건별 관측 보존 요구이고, 현재 원형 출력에서 문서 전체로 상태를 넓혀 QA를 잃는 오류가 관찰됐다.

## 확인 범위

119767은 기존 합성 개발 기록 두 개, 원형 QA 네 번을 실행했다. 후속 source readout은 그 실제 선택 결과를 그대로 입력받아 최종 reader 네 번만 실행한다. 원형 기억 작성·검색의 재실행이나 전체 시스템 독립 재검증이 아니다. 아직 일반 벤치마크, 기존 QA 20개 보존, 독립 사례 일반화 근거가 없다. 실패를 보고 과거 점수나 동결 자료를 바꾸지 않는다.
