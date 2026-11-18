# 68문서 records 실패표

문서 ID는 고정 평가셋의 ID다. 각 행 아래에 모든 필수 연결과 기존 오연결을 추적했다. 원문 위치는 문자 단위 반개구간 [시작, 끝)이다. 목록에 여러 위치가 있으면 gold가 보존한 원문 출현 위치를 모두 표시한다. 그룹 소유권은 저장 당시의 범위다. 복수 주장이 있는 그룹은 개별 대상을 확정할 수 없다. 상세 원출력 행, 원문, 그룹과 뒤 모듈에 전달된 구절은 [audit.json](audit.json)에 있다.

| 문서 | 난도 / 근거 | 저장 | 정답 / 필수 연결 | 오연결 | 첫 손실별 연결 수 |
|---|---|---|---:|---:|---|
| e01-full | easy / full | annotated | 2 / 2 | 0 | {} |
| e01-partial | easy / partial | annotated | 1 / 1 | 0 | {} |
| e01-none | easy / none | annotated | 0 / 0 | 0 | {} |
| e02-full | easy / full | annotated | 1 / 2 | 1 | {'role_assignment': 1} |
| e02-partial | easy / partial | annotated | 0 / 1 | 1 | {'role_assignment': 1} |
| e02-none | easy / none | annotated | 0 / 0 | 0 | {} |
| e03-full | easy / full | annotated | 2 / 2 | 0 | {} |
| e03-partial | easy / partial | annotated | 1 / 1 | 0 | {} |
| e03-none | easy / none | annotated | 0 / 0 | 0 | {} |
| e04-full | easy / full | annotated | 2 / 2 | 0 | {} |
| e04-partial | easy / partial | annotated | 1 / 1 | 0 | {} |
| e04-none | easy / none | annotated | 0 / 0 | 0 | {} |
| e05-full | easy / full | annotated | 1 / 2 | 0 | {'context_inside_target': 1} |
| e05-partial | easy / partial | annotated | 1 / 1 | 0 | {} |
| e05-none | easy / none | annotated | 0 / 0 | 0 | {} |
| e06-full | easy / full | annotated | 2 / 2 | 0 | {} |
| e06-partial | easy / partial | annotated | 1 / 1 | 0 | {} |
| e06-none | easy / none | annotated | 0 / 0 | 0 | {} |
| m01-full | medium / full | failed | 0 / 2 | 0 | {'target_assignment': 1, 'role_assignment': 1} |
| m01-partial | medium / partial | failed | 0 / 1 | 0 | {'target_assignment': 1} |
| m01-none | medium / none | annotated | 0 / 0 | 0 | {} |
| m02-full | medium / full | annotated | 1 / 2 | 1 | {'target_and_role_or_unresolved': 1} |
| m02-partial | medium / partial | annotated | 0 / 1 | 1 | {'role_assignment': 1} |
| m02-none | medium / none | annotated | 0 / 0 | 0 | {} |
| m03-full | medium / full | annotated | 0 / 2 | 1 | {'target_and_role_or_unresolved': 1, 'role_assignment': 1} |
| m03-partial | medium / partial | annotated | 1 / 1 | 0 | {} |
| m03-none | medium / none | annotated | 0 / 0 | 0 | {} |
| m04-full | medium / full | annotated | 1 / 2 | 1 | {'target_and_role_or_unresolved': 1} |
| m04-partial | medium / partial | annotated | 1 / 1 | 0 | {} |
| m04-none | medium / none | annotated | 0 / 0 | 0 | {} |
| m05-full | medium / full | annotated | 0 / 2 | 1 | {'context_inside_target': 1, 'target_assignment': 1} |
| m05-partial | medium / partial | annotated | 0 / 1 | 1 | {'target_assignment': 1} |
| m05-none | medium / none | annotated | 0 / 0 | 0 | {} |
| m06-full | medium / full | annotated | 1 / 2 | 1 | {'target_assignment': 1} |
| m06-partial | medium / partial | annotated | 1 / 1 | 0 | {} |
| m06-none | medium / none | annotated | 0 / 0 | 0 | {} |
| h01-full | hard / full | annotated | 1 / 4 | 3 | {'target_assignment': 1, 'role_assignment': 2} |
| h01-partial | hard / partial | annotated | 2 / 3 | 1 | {'target_assignment': 1} |
| h01-none | hard / none | annotated | 2 / 2 | 0 | {} |
| h02-full | hard / full | failed | 0 / 4 | 0 | {'role_assignment': 2, 'target_and_role_or_unresolved': 1, 'whole_record_rejected': 1} |
| h02-partial | hard / partial | annotated | 0 / 3 | 2 | {'role_assignment': 2, 'context_inside_target': 1} |
| h02-none | hard / none | annotated | 0 / 2 | 2 | {'target_missing_or_split': 2} |
| h03-full | hard / full | annotated | 2 / 4 | 1 | {'target_and_role_or_unresolved': 1, 'role_assignment': 1} |
| h03-partial | hard / partial | annotated | 0 / 3 | 0 | {'target_and_role_or_unresolved': 1, 'context_inside_target': 1, 'role_assignment': 1} |
| h03-none | hard / none | annotated | 2 / 2 | 1 | {} |
| h04-full | hard / full | annotated | 1 / 2 | 0 | {'target_and_role_or_unresolved': 1} |
| h04-partial | hard / partial | annotated | 1 / 1 | 0 | {} |
| h04-none | hard / none | annotated | 0 / 0 | 0 | {} |
| h05-full | hard / full | failed | 0 / 4 | 0 | {'whole_record_rejected': 4} |
| h05-partial | hard / partial | failed | 0 / 3 | 0 | {'whole_record_rejected': 2, 'role_assignment': 1} |
| h05-none | hard / none | annotated | 0 / 2 | 0 | {'context_inside_target': 2} |
| h06-full | hard / full | annotated | 1 / 3 | 0 | {'target_and_role_or_unresolved': 1, 'context_inside_target': 1} |
| h06-partial | hard / partial | annotated | 1 / 2 | 0 | {'context_inside_target': 1} |
| h06-none | hard / none | annotated | 0 / 1 | 0 | {'context_inside_target': 1} |
| n01 | medium / full | failed | 0 / 2 | 0 | {'whole_record_rejected': 1, 'context_inside_target': 1} |
| n02 | medium / full | annotated | 0 / 10 | 1 | {'target_and_role_or_unresolved': 7, 'context_inside_target': 1, 'context_missing_or_split': 1, 'target_assignment': 1} |
| n03 | medium / full | annotated | 0 / 3 | 1 | {'target_missing_or_split': 1, 'role_assignment': 1, 'context_inside_target': 1} |
| n04 | medium / full | annotated | 3 / 4 | 0 | {'context_inside_target': 1} |
| n05 | medium / full | annotated | 1 / 3 | 0 | {'target_missing_or_split': 1, 'target_and_role_or_unresolved': 1} |
| n06 | hard / partial | annotated | 1 / 2 | 0 | {'target_missing_or_split': 1} |
| n07 | medium / full | failed | 0 / 7 | 0 | {'target_missing_or_split': 1, 'context_missing_or_split': 2, 'whole_record_rejected': 3, 'target_and_role_or_unresolved': 1} |
| n08 | easy / full | annotated | 1 / 2 | 1 | {'role_assignment': 1} |
| n09 | medium / full | annotated | 1 / 3 | 0 | {'target_missing_or_split': 2} |
| n10 | hard / partial | annotated | 1 / 2 | 0 | {'context_inside_target': 1} |
| n11 | hard / partial | annotated | 0 / 0 | 0 | {} |
| n12 | medium / full | annotated | 2 / 4 | 2 | {'role_assignment': 1, 'context_inside_target': 1} |
| n13 | hard / full | annotated | 0 / 5 | 2 | {'target_and_role_or_unresolved': 1, 'context_inside_target': 1, 'role_assignment': 3} |
| n14 | hard / partial | annotated | 0 / 1 | 0 | {'context_inside_target': 1} |

## e01-full

For chilled parcels, use liner K6 because the foam prevents condensation.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 21–33 → 4–19 | [1] / [0] | retained | c:5438ecae20730d969fe06d16 |
| r1 / basis / r1:basis1 | 21–33 → 42–72 | [1] / [2] | retained | c:5438ecae20730d969fe06d16 |

## e01-partial

For chilled parcels, use liner K6.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 21–33 → 4–19 | [1] / [0] | retained | c:58426dd32c19d03538532fb4 |

## e01-none

use liner K6.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## e02-full

close gate R8 on Thursday because the hinge needs repair.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / basis / r1:basis1 | 0–13 → 34–56 | [0] / [2] | role_assignment | 구조화 연결 없음 |
| r1 / time / r1:time1 | 0–13 → 14–25 | [0] / [1] | retained | c:b523db273e46707ee985be94 |

- 오연결 ['r1', 'condition', 'r1:basis1'] · wrong_role · single_assertion. 원출력 2 condition 'because the hinge needs repair' [26, 56) → 저장 및 reader c:b523db273e46707ee985be94

## e02-partial

close gate R8 because the hinge needs repair.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / basis / r1:basis1 | 0–13 → 22–44 | [0] / [1] | role_assignment | 구조화 연결 없음 |

- 오연결 ['r1', 'condition', 'r1:basis1'] · wrong_role · single_assertion. 원출력 1 condition 'because the hinge needs repair' [14, 44) → 저장 및 reader c:06e83fcf4bf977ec01feced6

## e02-none

close gate R8.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## e03-full

For cracked containers, do not ship kit M3 because the seal failed inspection.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 24–42 → 4–22 | [1] / [0] | retained | c:94885e53a03aef553dabb5d2 |
| r1 / basis / r1:basis1 | 24–42 → 51–77 | [1] / [2] | retained | c:94885e53a03aef553dabb5d2 |

## e03-partial

For cracked containers, do not ship kit M3.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 24–42 → 4–22 | [1] / [0] | retained | c:b480d7b9a5292eba4e36b5e1 |

## e03-none

do not ship kit M3.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## e04-full

For inland stations, we might trial paint Q9. This trial is not approved.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 21–44 → 4–19 | [1] / [0] | retained | c:df6f1e20a47a4542fcd94126 (대상 불명확) |
| r1 / caveat / r1:caveat1 | 21–44 → 46–73 | [1] / [2] | retained | c:df6f1e20a47a4542fcd94126 (대상 불명확) |

## e04-partial

we might trial paint Q9. This trial is not approved.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / caveat / r1:caveat1 | 0–23 → 25–52 | [0] / [1] | retained | c:922318e8c07b5289ec4d3c97 (대상 불명확) |

## e04-none

we might trial paint Q9.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## e05-full

Recorded event time: on Tuesday. the sensor check is complete for firmware 6.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 33–61 → 66–76 | [1] / [1] | context_inside_target | 구조화 연결 없음 |
| r1 / time / r1:time1 | 33–61 → 21–31 | [1] / [0] | retained | c:803998866b529c9c8b84c29f |

## e05-partial

Recorded event time: on Tuesday. the sensor check is complete.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / time / r1:time1 | 33–61 → 21–31 | [1] / [0] | retained | c:b23b9df71dea302a8f82f9a3 |

## e05-none

the sensor check is complete.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## e06-full

For dry rooms, I suspect relay P4 may last 80 days. This estimate is untested.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 15–50 → 4–13 | [1] / [0] | retained | c:380b41d17aa939b3217d98bb (대상 불명확) |
| r1 / caveat / r1:caveat1 | 15–50 → 52–78 | [1] / [2] | retained | c:380b41d17aa939b3217d98bb (대상 불명확) |

## e06-partial

I suspect relay P4 may last 80 days. This estimate is untested.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / caveat / r1:caveat1 | 0–35 → 37–63 | [0] / [1] | retained | c:fa0e4e104efd2ec8ceaa7b92 (대상 불명확) |

## e06-none

I suspect relay P4 may last 80 days.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## m01-full

This survey decision applies to sector D2. The cabinet label is copper. we postpone the gravel survey because the access bridge is closed.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 72–101 → 32–41 | [2] / [0] | target_assignment | 구조화 연결 없음 |
| r1 / basis / r1:basis1 | 72–101 → 110–137 | [2] / [3] | role_assignment | 구조화 연결 없음 |

## m01-partial

This survey decision applies to sector D2. The cabinet label is copper. we postpone the gravel survey.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 72–101 → 32–41 | [2] / [0] | target_assignment | 구조화 연결 없음 |

## m01-none

The cabinet label is copper. we postpone the gravel survey.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## m02-full

Timing for the following beacon instruction: after the morning inspection. The antenna colour remains white. switch the beacon to standby because the battery is leaking.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / basis / r1:basis1 | 109–137 → 146–168 | [3] / [4] | retained | c:2397a7ae162372e6523b1a4f |
| r1 / time / r1:time1 | 109–137 → 45–73 | [3] / [0] | target_and_role_or_unresolved | 구조화 연결 없음 |

- 오연결 ['unbound:c:b123592376c9efc6efd2bf0c', 'condition', 'r1:time1'] · unbound_target · single_assertion. 원출력 0 condition 'after the morning inspection' [45, 73) → 저장 및 reader c:b123592376c9efc6efd2bf0c

## m02-partial

The antenna colour remains white. switch the beacon to standby because the battery is leaking.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / basis / r1:basis1 | 34–62 → 71–93 | [1] / [2] | role_assignment | 구조화 연결 없음 |

- 오연결 ['r1', 'condition', 'r1:basis1'] · wrong_role · single_assertion. 원출력 2 condition 'because the battery is leaking' [63, 93) → 저장 및 reader c:cd9d6dd3b4721e1f39f29e6f

## m02-none

The antenna colour remains white. switch the beacon to standby.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## m03-full

The following release instruction applies to saline batches. do not release batch U5 because the residue test failed. Freshwater batches remain eligible for release.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 61–84 → 45–59 | [1] / [0] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r1 / basis / r1:basis1 | 61–84 → 93–116 | [1] / [2] | role_assignment | 구조화 연결 없음 |

- 오연결 ['r1', 'condition', 'r1:basis1'] · wrong_role · single_assertion. 원출력 2 condition 'because the residue test failed' [85, 116) → 저장 및 reader c:5bddff34bc90b5b4efc25d28

## m03-partial

The following release instruction applies to saline batches. do not release batch U5. Freshwater batches remain eligible for release.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 61–84 → 45–59 | [1] / [0] | retained | c:c1dc9c411d8cd5972cdb00be |

## m03-none

do not release batch U5. Freshwater batches remain eligible for release.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## m04-full

Scope of the filter pilot: remote clinics. The spare tubing is blue. we could pilot filter J2. This pilot is a suggestion, not an authorization.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 69–93 → 27–41 | [3] / [1] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r1 / caveat / r1:caveat1 | 69–93 → 95–144 | [3] / [4] | retained | c:2bb19b128ed4a0c4bd97b313 (대상 불명확) |

- 오연결 ['unbound:c:f9a447b6be75da8fbd12fc89', 'condition', 'unmatched:1'] · unmatched_context · single_assertion. 원출력 0 condition 'Scope of the filter pilot' [0, 25) → 저장 및 reader c:f9a447b6be75da8fbd12fc89

## m04-partial

The spare tubing is blue. we could pilot filter J2. This pilot is a suggestion, not an authorization.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / caveat / r1:caveat1 | 26–50 → 52–101 | [1] / [2] | retained | c:550b9f500e965f7ba19ad870 (대상 불명확) |

## m04-none

The spare tubing is blue. we could pilot filter J2.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## m05-full

The calibration event occurred on Friday afternoon. The office clock was repaired. the valve calibration finished on bench T7.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 83–113 → 117–125 | [3] / [3] | context_inside_target | 구조화 연결 없음 |
| r1 / time / r1:time1 | 83–113 → 31–50 | [3] / [1] | target_assignment | 구조화 연결 없음 |

- 오연결 ['unbound:c:7da7fefa0d0cea8ce8dba8cb', 'time', 'r1:time1'] · unbound_target · single_assertion. 원출력 1 time 'on Friday afternoon' [31, 50) → 저장 및 reader c:7da7fefa0d0cea8ce8dba8cb

## m05-partial

The calibration event occurred on Friday afternoon. The office clock was repaired. the valve calibration finished.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / time / r1:time1 | 83–113 → 31–50 | [3] / [1] | target_assignment | 구조화 연결 없음 |

- 오연결 ['unbound:c:0ca3f90d13c03f96fedb397c', 'time', 'r1:time1'] · unbound_target · single_assertion. 원출력 1 time 'on Friday afternoon' [31, 50) → 저장 및 reader c:0ca3f90d13c03f96fedb397c

## m05-none

The office clock was repaired. the valve calibration finished.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## m06-full

Operating scope of this estimate: under reduced load. The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 88–126 → 34–52 | [3] / [0] | target_assignment | 구조화 연결 없음 |
| r1 / caveat / r1:caveat1 | 88–126 → 128–170 | [3] / [4] | retained | c:802077b1d60fdefde1ad0661 (대상 불명확) |

- 오연결 ['unbound:c:2604f6243b7cefda851b9b2d', 'condition', 'r1:condition1'] · unbound_target · single_assertion. 원출력 0 condition 'under reduced load' [34, 52) → 저장 및 reader c:2604f6243b7cefda851b9b2d

## m06-partial

The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / caveat / r1:caveat1 | 34–72 → 74–116 | [1] / [2] | retained | c:f282e3036cb549365871bef6 (대상 불명확) |

## m06-none

The procurement task is complete. I suspect drive L4 may reach 70 cycles.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## h01-full

Scope of the compressor instruction: pressure above 9 bar. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4 because its casing has fractured. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 353–371 → 37–57 | [6] / [1] | target_assignment | 구조화 연결 없음 |
| r1 / basis / r1:basis1 | 353–371 → 380–404 | [6] / [7] | role_assignment | 구조화 연결 없음 |
| r6 / condition / r6:condition1 | 441–454 → 428–439 | [10] / [9] | retained | c:8d4b8e774d0bb71d12c0ba79 (대상 불명확) |
| r6 / basis / r6:basis1 | 441–454 → 463–482 | [10] / [11] | role_assignment | 구조화 연결 없음 |

- 오연결 ['r1', 'condition', 'r1:basis1'] · wrong_role · single_assertion. 원출력 7 condition 'its casing has fractured' [380, 404) → 저장 및 reader c:1c2740ede64299bc42d3509d

- 오연결 ['r6', 'condition', 'r6:basis1'] · wrong_role · ambiguous_group. 원출력 9 condition 'below 1 bar' [428, 439) / 원출력 11 condition 'the buffer is empty' [463, 482) → 저장 및 reader c:8d4b8e774d0bb71d12c0ba79

- 오연결 ['unbound:c:b7b4a01daeb3f94e3f89812f', 'condition', 'r1:condition1'] · unbound_target · single_assertion. 원출력 1 condition 'pressure above 9 bar' [37, 57) → 저장 및 reader c:b7b4a01daeb3f94e3f89812f

## h01-partial

Scope of the compressor instruction: pressure above 9 bar. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 353–371 → 37–57 | [6] / [1] | target_assignment | 구조화 연결 없음 |
| r6 / condition / r6:condition1 | 408–421 → 395–406 | [9] / [8] | retained | c:78bc3aafd4d15a6a07ff6c45 (대상 불명확) |
| r6 / basis / r6:basis1 | 408–421 → 430–449 | [9] / [10] | retained | c:78bc3aafd4d15a6a07ff6c45 (대상 불명확) |

- 오연결 ['unbound:c:28cc3203699b3cb244621219', 'condition', 'r1:condition1'] · unbound_target · single_assertion. 원출력 1 condition 'pressure above 9 bar' [37, 57) → 저장 및 reader c:28cc3203699b3cb244621219

## h01-none

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r6 / condition / r6:condition1 | 349–362 → 336–347 | [6] / [5] | retained | c:e28f19823645a9b4c1d1ee96 |
| r6 / basis / r6:basis1 | 349–362 → 371–390 | [6] / [7] | retained | c:e28f19823645a9b4c1d1ee96 |

## h02-full

The time of the compass instruction is at 14:20. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test because the replacement mount passed inspection. Independently, the camera check begins at 14:20 because its lens is clean.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / basis / r1:basis1 | 343–366 → 375–414 | [6] / [6, 7] | role_assignment | 구조화 연결 없음 |
| r1 / time / r1:time1 | 343–366 → 39–47 | [6] / [0, 1, 8, 9] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r6 / basis / r6:basis1 | 431–454 → 472–489 | [8] / [10] | role_assignment | 구조화 연결 없음 |
| r6 / time / r6:time1 | 431–454 → 455–463 | [8] / [0, 1, 8, 9] | whole_record_rejected | 구조화 연결 없음 |

## h02-partial

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test because the replacement mount passed inspection. Independently, the camera check begins at 14:20 because its lens is clean.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / basis / r1:basis1 | 294–317 → 326–365 | [8] / [9] | role_assignment | 구조화 연결 없음 |
| r6 / basis / r6:basis1 | 382–405 → 423–440 | [10] / [11] | role_assignment | 구조화 연결 없음 |
| r6 / time / r6:time1 | 382–405 → 406–414 | [10] / [10] | context_inside_target | 구조화 연결 없음 |

- 오연결 ['r1', 'condition', 'r1:basis1'] · wrong_role · single_assertion. 원출력 9 condition 'because the replacement mount passed inspection' [318, 365) → 저장 및 reader c:d3d22ab7c30cdea15efb6d9e

- 오연결 ['r6', 'condition', 'r6:basis1'] · wrong_role · single_assertion. 원출력 11 condition 'because its lens is clean' [415, 440) → 저장 및 reader c:cd39c8420146a34e11e39a33

## h02-none

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test. Independently, the camera check begins at 14:20 because its lens is clean.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r6 / basis / r6:basis1 | 334–357 → 375–392 | [5] / [6] | target_missing_or_split | 구조화 연결 없음 |
| r6 / time / r6:time1 | 334–357 → 358–366 | [5] / [5] | target_missing_or_split | 구조화 연결 없음 |

- 오연결 ['unbound:c:171f20606d2881598760c06e', 'condition', 'r6:claim'] · unbound_target · single_assertion. 원출력 5 condition 'Independently, the camera check begins at 14:20' [319, 366) → 저장 및 reader c:171f20606d2881598760c06e

- 오연결 ['unbound:c:171f20606d2881598760c06e', 'condition', 'r6:time1'] · unbound_target · single_assertion. 원출력 5 condition 'Independently, the camera check begins at 14:20' [319, 366) → 저장 및 reader c:171f20606d2881598760c06e

## h03-full

The map instruction below concerns commercial reuse. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map because the licence excludes commercial distribution. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 347–377 → 35–51 | [5] / [0] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r1 / basis / r1:basis1 | 347–377 → 386–430 | [5] / [5, 6] | role_assignment | 구조화 연결 없음 |
| r6 / condition / r6:condition1 | 478–496 → 454–476 | [7] / [7, 8] | retained | c:ea32b0fe3050a82f5a5a91a3 |
| r6 / basis / r6:basis1 | 478–496 → 505–535 | [7] / [7, 9] | retained | c:ea32b0fe3050a82f5a5a91a3 |

- 오연결 ['r1', 'condition', 'r1:basis1'] · wrong_role · single_assertion. 원출력 6 condition 'the licence excludes commercial distribution' [386, 430) → 저장 및 reader c:782298425aaf521b458cf1bd

## h03-partial

The map instruction below concerns commercial reuse. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 347–377 → 35–51 | [5] / [0] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r6 / condition / r6:condition1 | 425–443 → 401–423 | [6] / [6] | context_inside_target | 구조화 연결 없음 |
| r6 / basis / r6:basis1 | 425–443 → 452–482 | [6] / [7] | role_assignment | 구조화 연결 없음 |

## h03-none

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r6 / condition / r6:condition1 | 372–390 → 348–370 | [5] / [5, 6] | retained | c:f5bf7c54eef44d5689f6c8bd |
| r6 / basis / r6:basis1 | 372–390 → 399–429 | [5] / [5, 8] | retained | c:f5bf7c54eef44d5689f6c8bd |

- 오연결 ['unbound:c:f5bf7c54eef44d5689f6c8bd', 'subject', 'unmatched:8'] · unmatched_context · single_assertion. 원출력 7 subject 'the sketch' [380, 390) → 저장 및 reader c:f5bf7c54eef44d5689f6c8bd

## h04-full

The pack trial applies to desert depots. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. This proposed trial has no deployment approval. Independently, the warehouse rollout is approved.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 335–357 → 26–39 | [5] / [0] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r1 / caveat / r1:caveat1 | 335–357 → 359–406 | [5] / [6] | retained | c:3b3fc909518642eb9580bf1a (대상 불명확) |

## h04-partial

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. This proposed trial has no deployment approval. Independently, the warehouse rollout is approved.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / caveat / r1:caveat1 | 294–316 → 318–365 | [4] / [5] | retained | c:03040482ad3a600ba2b1a090 (대상 불명확) |

## h04-none

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. Independently, the warehouse rollout is approved.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## h05-full

The pressure audit ended at 16:40. The pressure audit concerns rig C9. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 0–24, 365–389 → 63–69 | [0, 7] / [2] | whole_record_rejected | 구조화 연결 없음 |
| r1 / time / r1:time1 | 0–24, 365–389 → 25–33 | [0, 7] / [1, 8, 9] | whole_record_rejected | 구조화 연결 없음 |
| r6 / condition / r6:condition1 | 403–425 → 435–444 | [8] / [10] | whole_record_rejected | 구조화 연결 없음 |
| r6 / time / r6:time1 | 403–425 → 426–434 | [8] / [1, 8, 9] | whole_record_rejected | 구조화 연결 없음 |

## h05-partial

The pressure audit ended at 16:40. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / time / r1:time1 | 0–24, 329–353 → 25–33 | [0, 6] / [1, 7, 8] | whole_record_rejected | 구조화 연결 없음 |
| r6 / condition / r6:condition1 | 367–389 → 399–408 | [7] / [7, 9] | role_assignment | 구조화 연결 없음 |
| r6 / time / r6:time1 | 367–389 → 390–398 | [7] / [1, 7, 8] | whole_record_rejected | 구조화 연결 없음 |

## h05-none

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r6 / condition / r6:condition1 | 332–354 → 364–373 | [5] / [5] | context_inside_target | 구조화 연결 없음 |
| r6 / time / r6:time1 | 332–354 → 355–363 | [5] / [5] | context_inside_target | 구조화 연결 없음 |

## h06-full

The coil estimate concerns operation in nitrogen. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. This capacity is conjectural and has not been measured. A separate steel cable was measured at 12 amperes in air.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 344–383 → 37–48 | [5] / [0] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r1 / caveat / r1:caveat1 | 344–383 → 385–440 | [5] / [6] | retained | c:3a6f2f812d530a9520081318 (대상 불명확) |
| r6 / condition / r6:condition1 | 441–490 → 491–497 | [7] / [7] | context_inside_target | 구조화 연결 없음 |

## h06-partial

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. This capacity is conjectural and has not been measured. A separate steel cable was measured at 12 amperes in air.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / caveat / r1:caveat1 | 294–333 → 335–390 | [4] / [5] | retained | c:1ce75bd14082a5a6bb965ef1 (대상 불명확) |
| r6 / condition / r6:condition1 | 391–440 → 441–447 | [6] / [6] | context_inside_target | 구조화 연결 없음 |

## h06-none

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. A separate steel cable was measured at 12 amperes in air.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r6 / condition / r6:condition1 | 335–384 → 385–391 | [5] / [5] | context_inside_target | 구조화 연결 없음 |

## n01

@all [Task Completed] Hello everyone, the task "Verify the accuracy of alarm rule creation and trigger logic" for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed. All test cases have passed, including various single conditions, combined conditions, and boundary value scenarios. The few issues discovered yesterday have also all been regression verified and passed. The final test report has been uploaded to Confluence. 🎉

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r2 / caveat / r2:caveat1 | 214–240 → 242–328 | [1] / [1] | whole_record_rejected | 구조화 연결 없음 |
| r3 / time / r3:time1 | 330–415 → 356–365 | [2] / [2] | context_inside_target | 구조화 연결 없음 |

## n02

Good morning everyone. Today is Thursday. Just a reminder to @Hanqiang Liang and @Huihong Tian, your medication check-in module and family member invitation interface are due today. Please make sure to complete the delivery today. Other colleagues, please also share your plans and progress for today.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / time / r1:time1 | 23–40 → 23–28, 175–180, 224–229, 295–300 | [1] / [1, 2, 4, 5] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r1 / time / r1:time2 | 23–40 → 32–40 | [1] / [1] | context_inside_target | 구조화 연결 없음 |
| r2 / time / r2:time1 | 96–180 → 23–28, 175–180, 224–229, 295–300 | [2] / [1, 2, 4, 5] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r2 / time / r2:time2 | 96–180 → 32–40 | [2] / [1] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r2 / recipient / r2:recipient1 | 96–180 → 61–94 | [2] / [] | context_missing_or_split | 구조화 연결 없음 |
| r3 / time / r3:time1 | 182–229 → 23–28, 175–180, 224–229, 295–300 | [4] / [1, 2, 4, 5] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r3 / time / r3:time2 | 182–229 → 32–40 | [4] / [1] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r3 / subject / r3:subject1 | 182–229 → 96–166 | [4] / [2, 3] | target_assignment | 구조화 연결 없음 |
| r4 / time / r4:time1 | 231–300 → 23–28, 175–180, 224–229, 295–300 | [5] / [1, 2, 4, 5] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r4 / time / r4:time2 | 231–300 → 32–40 | [5] / [1] | target_and_role_or_unresolved | 구조화 연결 없음 |

- 오연결 ['r2', 'subject', 'r3:subject1'] · wrong_target · single_assertion. 원출력 3 subject 'your medication check-in module and family member invitation interface' [96, 166) → 저장 및 reader c:344641b50b9ad6f472ec00a0

## n03

Hello everyone, today I'm starting a new design task: [Designing a File Storage Solution]. Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3. The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack. A preliminary selection recommendation report will be provided early next week.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / time / r1:time1 | 16–89 → 16–21 | [] / [0] | target_missing_or_split | 구조화 연결 없음 |
| r2 / basis / r2:basis1 | 207–254 → 108–205 | [3] / [2] | role_assignment | 구조화 연결 없음 |
| r4 / time / r4:time1 | 418–496 → 481–496 | [5] / [5] | context_inside_target | 구조화 연결 없음 |

- 오연결 ['r2', 'condition', 'r2:basis1'] · wrong_role · single_assertion. 원출력 2 condition 'Considering that our system will need to store a large number of supporting documents, reports, etc. in the future' [91, 205) → 저장 및 reader c:3629c65310684219cf775735

## n04

Good morning everyone. Regarding the design of our file storage solution, I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday. From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage, and our other projects are also on AWS. Today, I will start designing the Bucket Policy and directory structure based on S3, for example, isolating by tenant and file type.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / time / r1:time1 | 74–147 → 136–147 | [1] / [1, 2] | retained | c:633007409939863e9d305c4b |
| r2 / condition / r2:condition1 | 205–234 → 149–203 | [3] / [3] | context_inside_target | 구조화 연결 없음 |
| r4 / time / r4:time1 | 283–359 → 276–281 | [5] / [5, 6] | retained | c:fd869559c660f842d202e0e3 (대상 불명확) |
| r4 / method / r4:method1 | 283–359 → 374–407 | [5] / [7] | retained | c:fd869559c660f842d202e0e3 (대상 불명확) |

## n05

Good morning everyone, regarding the file storage solution, the complete technical design document (based on AWS S3) has been uploaded to Confluence. It includes three main parts: bucket permission policies, lifecycle rules, and recommended directory structure. @Mingzhi Li Boss Li, please review it.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r2 / subject / r2:subject1 | 150–260 → 60–116 | [] / [2] | target_missing_or_split | 구조화 연결 없음 |
| r3 / subject / r3:subject1 | 283–299 → 60–116 | [7] / [2] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r3 / recipient / r3:recipient1 | 283–299 → 262–281 | [7] / [7] | retained | c:a0dcba2dd649281a2e891cc0 |

## n06

@Lujian Gao I've finished reviewing the document on the file storage solution. The design is very comprehensive, especially the considerations for tenant data isolation and cost optimization. The proposal is approved and can be finalized.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r2 / caveat / r2:caveat1 | 79–111 → 113–190 | [1] / [2] | retained | c:490813a2ccb47303740d39f6 (대상 불명확) |
| r3 / subject / r3:subject1 | 192–237 → 52–77 | [] / [0] | target_missing_or_split | 구조화 연결 없음 |

## n07

@Yang Zhao Good question. Regarding the "forgot password" process, our main security consideration is to prevent "user enumeration attacks." Therefore, regardless of whether the email entered by the user exists or not, the feedback message should be consistent, such as "If this email address is registered, you will receive an email containing a password reset link," instead of directly prompting "user does not exist." Please ensure the UI copy adheres to this principle.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 67–140 → 41–56 | [1] / [] | target_missing_or_split | 구조화 연결 없음 |
| r2 / condition / r2:condition1 | 219–260 → 41–56 | [3] / [] | context_missing_or_split | 구조화 연결 없음 |
| r2 / condition / r2:condition2 | 219–260 → 152–217 | [3] / [2] | whole_record_rejected | 구조화 연결 없음 |
| r2 / basis / r2:basis1 | 219–260 → 105–140 | [3] / [1] | context_missing_or_split | 구조화 연결 없음 |
| r2 / method / r2:method1 | 219–260 → 262–368 | [3] / [4] | whole_record_rejected | 구조화 연결 없음 |
| r2 / method / r2:method2 | 219–260 → 369–421 | [3] / [5] | whole_record_rejected | 구조화 연결 없음 |
| r3 / subject / r3:subject1 | 422–473 → 219–260 | [6] / [3] | target_and_role_or_unresolved | 구조화 연결 없음 |

## n08

Email received. The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction. @Xinjie Li @Xuexin Yin, please assess the scope of impact on the backend.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / condition / r1:condition1 | 92–185 → 45–91 | [1] / [1, 2] | role_assignment | 구조화 연결 없음 |
| r2 / recipient / r2:recipient1 | 211–259 → 187–209 | [3] / [3] | retained | c:cd9f4c9f1be74425b557c557 |

- 오연결 ['r1', 'subject', 'r1:condition1'] · wrong_role · single_assertion. 원출력 2 subject 'all accounts marked as `ACCOUNT_STATUS_LOCKED`' [45, 91) → 저장 및 reader c:684261cc31019f21b9c26e61

## n09

The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`, defined as 'Explicit Status Alert Policy'. It is mainly used for scenarios where an account is locked, requiring explicit interruption of user operations and guidance to manual channels.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / caveat / r1:caveat1 | 0–61 → 63–104 | [0] / [1] | retained | c:911665fee64c2bc478b1b986 (대상 불명확) |
| r2 / condition / r2:condition1 | 166–248 → 138–164 | [] / [2] | target_missing_or_split | 구조화 연결 없음 |
| r2 / subject / r2:subject1 | 166–248 → 31–61 | [] / [0] | target_missing_or_split | 구조화 연결 없음 |

## n10

Received. I've reviewed the document. This strategy will be handled by `ExplicitStateAlertModule`, and the parameter `halt_downstream_triggers` is set to `true`. This means that after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted, right?

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r4 / condition / r4:condition1 | 220–287 → 178–218 | [4] / [4] | context_inside_target | 구조화 연결 없음 |
| r4 / caveat / r4:caveat1 | 220–287 → 289–295 | [4] / [5] | retained | c:657e6a751a5b8f07de49e190 (대상 불명확) |

## n11

@Xinjie Li Yes, your understanding is completely correct. This is to avoid sending users redundant or potentially confusing automated messages.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|

## n12

Received, thanks a lot! The data structure looks very clear. I plan to complete the static data integration this morning to ensure the charts render correctly. In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it. @Mingzhi Li

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r2 / basis / r2:basis1 | 61–120 → 121–158 | [2] / [4] | role_assignment | 구조화 연결 없음 |
| r2 / time / r2:time1 | 61–120 → 108–120 | [2] / [2, 3] | retained | c:7d17bdb7c5aff687a0851d9f (대상 불명확) |
| r3 / time / r3:time1 | 178–226 → 160–176 | [5] / [5, 6] | retained | c:cbbab37c3aeaae3c8fb38365 (대상 불명확) |
| r4 / condition / r4:condition1 | 228–259 → 260–286 | [7] / [7] | context_inside_target | 구조화 연결 없음 |

- 오연결 ['r4', 'time', 'r3:time1'] · wrong_target · ambiguous_group. 원출력 6 time 'in the afternoon' [160, 176) → 저장 및 reader c:cbbab37c3aeaae3c8fb38365

- 오연결 ['unbound:c:cbbab37c3aeaae3c8fb38365', 'subject', 'unmatched:8'] · unmatched_context · ambiguous_group. 원출력 8 subject 'the backend' [263, 274) → 저장 및 reader c:cbbab37c3aeaae3c8fb38365

## n13

@Yunqi Qian Great plan. WebSocket is the best solution, but our message push service isn't fully ready yet. This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds. Once the WebSocket service is stable later, we can upgrade it uniformly. This way, we can avoid blocking your current task.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r3 / basis / r3:basis1 | 108–158 → 309–341 | [3] / [7] | target_and_role_or_unresolved | 구조화 연결 없음 |
| r3 / time / r3:time1 | 108–158 → 151–158 | [3] / [3] | context_inside_target | 구조화 연결 없음 |
| r3 / method / r3:method1 | 108–158 → 173–217 | [3] / [4] | role_assignment | 구조화 연결 없음 |
| r4 / condition / r4:condition1 | 263–290 → 219–261 | [6] / [5] | role_assignment | 구조화 연결 없음 |
| r4 / time / r4:time1 | 263–290 → 256–261 | [6] / [5] | role_assignment | 구조화 연결 없음 |

- 오연결 ['r1', 'condition', 'r2:claim'] · wrong_role · single_assertion. 원출력 2 condition "our message push service isn't fully ready yet" [60, 106) → 저장 및 reader c:04d91058fc298909ab052ade

- 오연결 ['r3', 'condition', 'r3:method1'] · wrong_role · single_assertion. 원출력 4 condition 'by requesting the interface every 10 seconds' [173, 217) → 저장 및 reader c:476d9dd6ff73f967db99f395

## n14

Okay, Boss Li, understood. Then I'll use the polling solution for now, and I'll adjust the plan.

| 대상·관계·근거 | 원문 대상 → 근거 위치 | 원출력 대상 / 근거 행 | 첫 손실 | 저장 → reader |
|---|---|---|---|---|
| r1 / time / r1:time1 | 32–69 → 62–69 | [1] / [1] | context_inside_target | 구조화 연결 없음 |
