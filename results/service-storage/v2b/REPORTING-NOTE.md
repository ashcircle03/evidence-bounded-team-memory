# 시간 비교 범위의 명확화

사전 프로토콜의 “This changes test setup cost, not timed prepare inputs/behavior”는 원문 내용과 색인 알고리즘 입력이 같다는 뜻으로 한정해야 한다. `prepare_index`에는 원문 로드도 들어가므로 기존 SourceStore의 파일 읽기와 이번 실제 module adapter의 MutableView 복사는 동일한 비용이 아니다.

따라서 역사적 685.52초와 이번7개 corpus의 총 시간을 나눠 전체 서비스의 개선 배수로 발표하지 않는다. 원인과 개선 효과는 이번 실행 안에서 같은 MutableView·같은 Ceph cache/index·같은 GPU·같은229문서를 사용한 A/B/C/D의 순서 균형 반복 및 단계 계측으로 판단한다. 기존 QA 입력·모델·검색 설정·기대 근거·보존 기준과 실행 코드는 바꾸지 않는다. 독립 로컬 실행과 Git 공유 구조도 그대로다.

이 비교는 색인 준비 단계의 최적화다. Git pull, 원문 영속화, records 추출, 관계 판단, 실제 Qwen 답변 생성을 포함한 종단간 서비스 지연시간 benchmark가 아니다.
