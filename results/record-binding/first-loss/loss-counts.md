# 모든 필수 관계의 최초 관측 손실

| 최초 손실 또는 보존 | 합성 문서/연결 | 자연 문서/연결 |
| --- | --- | --- |
| context_inside_target | 8 / 9 | 8 / 8 |
| context_missing_or_split | 0 / 0 | 2 / 3 |
| retained | 26 / 34 | 7 / 10 |
| role_assignment | 11 / 14 | 4 / 6 |
| target_and_role_or_unresolved | 8 / 8 | 4 / 10 |
| target_assignment | 7 / 7 | 1 / 1 |
| target_missing_or_split | 1 / 2 | 5 / 6 |
| whole_record_rejected | 3 / 7 | 2 / 4 |

retained는 고정 평가에서 맞고 기록 그룹이 reader에 전달된 경우다. whole_record_rejected는 원출력 채점에서 맞았으나 저장 실패로 사라진 경우다. 같은 실패 문서라도 원출력에서 이미 틀린 연결은 먼저 관측된 추출 오류로 센다. raw_to_graph는 정답 원출력이 저장 변환 중 사라지는 경우다. target_missing_or_split과 context_missing_or_split은 일치하는 단일 구절 없음, context_inside_target은 대상과 분리된 근거 구절 없음이다. role_assignment는 같은 그룹에 있는 근거 역할, target_assignment는 역할이 있는 근거의 대상이다. target_and_role_or_unresolved는 두 문제를 분리해 귀속할 수 없는 경우다. 전송은 해당 기록을 지정해 호출한 reader 경로에서 확인했다.
