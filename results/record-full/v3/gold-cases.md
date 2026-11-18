# 문서 전체 정답과 원문

기존54개 합성/14개 자연 원문 유지. 원문 기반 단일 작성자 정답이며 독립 검수 전 개발용이다. 원문의 모든 의미를 자연어 일반 추론으로 판정하는 정답은 아니다.

## e01-full · easy · full

source_id: `33abbca0dc91dbb59f467b14`

For chilled parcels, use liner K6 because the foam prevents condensation.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|use liner K6|21:33|True|
|r1:condition1|condition|chilled parcels|4:19|True|
|r1:basis1|basis|the foam prevents condensation|42:72|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e01-partial · easy · partial

source_id: `6fea6f425cd00d4746adb023`

For chilled parcels, use liner K6.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|use liner K6|21:33|True|
|r1:condition1|condition|chilled parcels|4:19|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e01-none · easy · none

source_id: `97200ceeaf92691fde3c3f0a`

use liner K6.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|use liner K6|0:12|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e02-full · easy · full

source_id: `709f8ae378397a731a47ec82`

close gate R8 on Thursday because the hinge needs repair.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|close gate R8|0:13|True|
|r1:basis1|basis|the hinge needs repair|34:56|True|
|r1:time1|time|on Thursday|14:25|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e02-partial · easy · partial

source_id: `925538e36ab8cf414f9cb883`

close gate R8 because the hinge needs repair.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|close gate R8|0:13|True|
|r1:basis1|basis|the hinge needs repair|22:44|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e02-none · easy · none

source_id: `801945abc96c000f57f6e92a`

close gate R8.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|close gate R8|0:13|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e03-full · easy · full

source_id: `26e96d281e3e856dedc95b7e`

For cracked containers, do not ship kit M3 because the seal failed inspection.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not ship kit M3|24:42|True|
|r1:condition1|condition|cracked containers|4:22|True|
|r1:basis1|basis|the seal failed inspection|51:77|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e03-partial · easy · partial

source_id: `02b5161b879fac5c3943fee0`

For cracked containers, do not ship kit M3.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not ship kit M3|24:42|True|
|r1:condition1|condition|cracked containers|4:22|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e03-none · easy · none

source_id: `74738fb6b8b3b19b518bd96e`

do not ship kit M3.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not ship kit M3|0:18|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e04-full · easy · full

source_id: `d764923f575d0292ebbbffa2`

For inland stations, we might trial paint Q9. This trial is not approved.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we might trial paint Q9|21:44|True|
|r1:condition1|condition|inland stations|4:19|True|
|r1:caveat1|caveat|This trial is not approved.|46:73|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e04-partial · easy · partial

source_id: `a8989ff9f5cbe9dadc7c475b`

we might trial paint Q9. This trial is not approved.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we might trial paint Q9|0:23|True|
|r1:caveat1|caveat|This trial is not approved.|25:52|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e04-none · easy · none

source_id: `668ff2dbdae195e6f8d1967f`

we might trial paint Q9.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we might trial paint Q9|0:23|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e05-full · easy · full

source_id: `694c889970229e4061e0b4d4`

Recorded event time: on Tuesday. the sensor check is complete for firmware 6.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the sensor check is complete|33:61|True|
|r1:condition1|condition|firmware 6|66:76|True|
|r1:time1|time|on Tuesday|21:31|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e05-partial · easy · partial

source_id: `63b0dc798b1b6b19caf5f134`

Recorded event time: on Tuesday. the sensor check is complete.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the sensor check is complete|33:61|True|
|r1:time1|time|on Tuesday|21:31|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e05-none · easy · none

source_id: `68d5db1a3a6ad6422d2040e6`

the sensor check is complete.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the sensor check is complete|0:28|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e06-full · easy · full

source_id: `d0fcf930f9524f0f08399148`

For dry rooms, I suspect relay P4 may last 80 days. This estimate is untested.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect relay P4 may last 80 days|15:50|True|
|r1:condition1|condition|dry rooms|4:13|True|
|r1:caveat1|caveat|This estimate is untested.|52:78|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e06-partial · easy · partial

source_id: `c628de4a11483d61a9204676`

I suspect relay P4 may last 80 days. This estimate is untested.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect relay P4 may last 80 days|0:35|True|
|r1:caveat1|caveat|This estimate is untested.|37:63|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## e06-none · easy · none

source_id: `566f53022fec16660340d521`

I suspect relay P4 may last 80 days.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect relay P4 may last 80 days|0:35|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m01-full · medium · full

source_id: `d4246e285cafe8eae5f385cc`

This survey decision applies to sector D2. The cabinet label is copper. we postpone the gravel survey because the access bridge is closed.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we postpone the gravel survey|72:101|True|
|r1:condition1|condition|sector D2|32:41|True|
|r1:basis1|basis|the access bridge is closed|110:137|True|
|r2:claim|claim|The cabinet label is copper|43:70|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m01-partial · medium · partial

source_id: `aa89de85e1e7b4d439b8b949`

This survey decision applies to sector D2. The cabinet label is copper. we postpone the gravel survey.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we postpone the gravel survey|72:101|True|
|r1:condition1|condition|sector D2|32:41|True|
|r2:claim|claim|The cabinet label is copper|43:70|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m01-none · medium · none

source_id: `5ed1d90a243e42fa026cf898`

The cabinet label is copper. we postpone the gravel survey.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we postpone the gravel survey|29:58|True|
|r2:claim|claim|The cabinet label is copper|0:27|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m02-full · medium · full

source_id: `3bd9438d4fd1752dbee0ca65`

Timing for the following beacon instruction: after the morning inspection. The antenna colour remains white. switch the beacon to standby because the battery is leaking.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|switch the beacon to standby|109:137|True|
|r1:basis1|basis|the battery is leaking|146:168|True|
|r1:time1|time|after the morning inspection|45:73|True|
|r2:claim|claim|The antenna colour remains white|75:107|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m02-partial · medium · partial

source_id: `5557e3d2bc40298994abc274`

The antenna colour remains white. switch the beacon to standby because the battery is leaking.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|switch the beacon to standby|34:62|True|
|r1:basis1|basis|the battery is leaking|71:93|True|
|r2:claim|claim|The antenna colour remains white|0:32|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m02-none · medium · none

source_id: `45e125beb1e51de31e6fc861`

The antenna colour remains white. switch the beacon to standby.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|switch the beacon to standby|34:62|True|
|r2:claim|claim|The antenna colour remains white|0:32|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m03-full · medium · full

source_id: `17059c178deaf784e8411521`

The following release instruction applies to saline batches. do not release batch U5 because the residue test failed. Freshwater batches remain eligible for release.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not release batch U5|61:84|True|
|r1:condition1|condition|saline batches|45:59|True|
|r1:basis1|basis|the residue test failed|93:116|True|
|r2:claim|claim|Freshwater batches remain eligible for release|118:164|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m03-partial · medium · partial

source_id: `ca86e4fed815e881bbb73c14`

The following release instruction applies to saline batches. do not release batch U5. Freshwater batches remain eligible for release.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not release batch U5|61:84|True|
|r1:condition1|condition|saline batches|45:59|True|
|r2:claim|claim|Freshwater batches remain eligible for release|86:132|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m03-none · medium · none

source_id: `eb9f29530f2bc3d522f4dcc8`

do not release batch U5. Freshwater batches remain eligible for release.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not release batch U5|0:23|True|
|r2:claim|claim|Freshwater batches remain eligible for release|25:71|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m04-full · medium · full

source_id: `0d750c235cc5f5779be97aeb`

Scope of the filter pilot: remote clinics. The spare tubing is blue. we could pilot filter J2. This pilot is a suggestion, not an authorization.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we could pilot filter J2|69:93|True|
|r1:condition1|condition|remote clinics|27:41|True|
|r1:caveat1|caveat|This pilot is a suggestion, not an authorization.|95:144|True|
|r2:claim|claim|The spare tubing is blue|43:67|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m04-partial · medium · partial

source_id: `c186a128c7866ca21efe5ce4`

The spare tubing is blue. we could pilot filter J2. This pilot is a suggestion, not an authorization.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we could pilot filter J2|26:50|True|
|r1:caveat1|caveat|This pilot is a suggestion, not an authorization.|52:101|True|
|r2:claim|claim|The spare tubing is blue|0:24|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m04-none · medium · none

source_id: `ff1dc03758f2c348b5760225`

The spare tubing is blue. we could pilot filter J2.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we could pilot filter J2|26:50|True|
|r2:claim|claim|The spare tubing is blue|0:24|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m05-full · medium · full

source_id: `325f038abd94e5f86e44e93d`

The calibration event occurred on Friday afternoon. The office clock was repaired. the valve calibration finished on bench T7.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the valve calibration finished|83:113|True|
|r1:condition1|condition|bench T7|117:125|True|
|r1:time1|time|on Friday afternoon|31:50|True|
|r2:claim|claim|The office clock was repaired|52:81|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m05-partial · medium · partial

source_id: `8b37462b2d1ffdee37d08519`

The calibration event occurred on Friday afternoon. The office clock was repaired. the valve calibration finished.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the valve calibration finished|83:113|True|
|r1:time1|time|on Friday afternoon|31:50|True|
|r2:claim|claim|The office clock was repaired|52:81|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m05-none · medium · none

source_id: `c69146fee259c2e07e827f91`

The office clock was repaired. the valve calibration finished.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the valve calibration finished|31:61|True|
|r2:claim|claim|The office clock was repaired|0:29|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m06-full · medium · full

source_id: `84b80190b326000dbfec164c`

Operating scope of this estimate: under reduced load. The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect drive L4 may reach 70 cycles|88:126|True|
|r1:condition1|condition|under reduced load|34:52|True|
|r1:caveat1|caveat|No measurement supports this estimate yet.|128:170|True|
|r2:claim|claim|The procurement task is complete|54:86|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m06-partial · medium · partial

source_id: `9dc93469ba851b9facbaf1e5`

The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect drive L4 may reach 70 cycles|34:72|True|
|r1:caveat1|caveat|No measurement supports this estimate yet.|74:116|True|
|r2:claim|claim|The procurement task is complete|0:32|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## m06-none · medium · none

source_id: `42c88617812e2f691d3bada8`

The procurement task is complete. I suspect drive L4 may reach 70 cycles.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect drive L4 may reach 70 cycles|34:72|True|
|r2:claim|claim|The procurement task is complete|0:32|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h01-full · hard · full

source_id: `3b074ee68ba0096b48e973b3`

Scope of the compressor instruction: pressure above 9 bar. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4 because its casing has fractured. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|halt compressor Z4|353:371|True|
|r1:condition1|condition|pressure above 9 bar|37:57|True|
|r1:basis1|basis|its casing has fractured|380:404|True|
|r2:claim|claim|The delivery folder contains a yellow form|59:101, 206:248|True|
|r3:claim|claim|The stock counter remains seven|103:134, 250:281|True|
|r4:claim|claim|The break room has two chairs|136:165, 283:312|True|
|r5:claim|claim|The printer tray contains plain paper|167:204, 314:351|True|
|r6:claim|claim|start pump B2|441:454|True|
|r6:condition1|condition|below 1 bar|428:439|True|
|r6:basis1|basis|the buffer is empty|463:482|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h01-partial · hard · partial

source_id: `69eba89e50bdbdb2eea03896`

Scope of the compressor instruction: pressure above 9 bar. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|halt compressor Z4|353:371|True|
|r1:condition1|condition|pressure above 9 bar|37:57|True|
|r2:claim|claim|The delivery folder contains a yellow form|59:101, 206:248|True|
|r3:claim|claim|The stock counter remains seven|103:134, 250:281|True|
|r4:claim|claim|The break room has two chairs|136:165, 283:312|True|
|r5:claim|claim|The printer tray contains plain paper|167:204, 314:351|True|
|r6:claim|claim|start pump B2|408:421|True|
|r6:condition1|condition|below 1 bar|395:406|True|
|r6:basis1|basis|the buffer is empty|430:449|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h01-none · hard · none

source_id: `d2bb5fd77d5625c88f17b02d`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|halt compressor Z4|294:312|True|
|r2:claim|claim|The delivery folder contains a yellow form|0:42, 147:189|True|
|r3:claim|claim|The stock counter remains seven|44:75, 191:222|True|
|r4:claim|claim|The break room has two chairs|77:106, 224:253|True|
|r5:claim|claim|The printer tray contains plain paper|108:145, 255:292|True|
|r6:claim|claim|start pump B2|349:362|True|
|r6:condition1|condition|below 1 bar|336:347|True|
|r6:basis1|basis|the buffer is empty|371:390|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h02-full · hard · full

source_id: `571e3e7db5473ea0837ab6b1`

The time of the compass instruction is at 14:20. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test because the replacement mount passed inspection. Independently, the camera check begins at 14:20 because its lens is clean.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|resume the compass test|343:366|True|
|r1:basis1|basis|the replacement mount passed inspection|375:414|True|
|r1:time1|time|at 14:20|39:47|True|
|r2:claim|claim|The delivery folder contains a yellow form|49:91, 196:238|True|
|r3:claim|claim|The stock counter remains seven|93:124, 240:271|True|
|r4:claim|claim|The break room has two chairs|126:155, 273:302|True|
|r5:claim|claim|The printer tray contains plain paper|157:194, 304:341|True|
|r6:claim|claim|the camera check begins|431:454|True|
|r6:basis1|basis|its lens is clean|472:489|True|
|r6:time1|time|at 14:20|455:463|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h02-partial · hard · partial

source_id: `2d83d8aa7b1dc6060ba52a53`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test because the replacement mount passed inspection. Independently, the camera check begins at 14:20 because its lens is clean.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|resume the compass test|294:317|True|
|r1:basis1|basis|the replacement mount passed inspection|326:365|True|
|r2:claim|claim|The delivery folder contains a yellow form|0:42, 147:189|True|
|r3:claim|claim|The stock counter remains seven|44:75, 191:222|True|
|r4:claim|claim|The break room has two chairs|77:106, 224:253|True|
|r5:claim|claim|The printer tray contains plain paper|108:145, 255:292|True|
|r6:claim|claim|the camera check begins|382:405|True|
|r6:basis1|basis|its lens is clean|423:440|True|
|r6:time1|time|at 14:20|406:414|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h02-none · hard · none

source_id: `c3e8aeb6e6d5603876c40e1b`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test. Independently, the camera check begins at 14:20 because its lens is clean.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|resume the compass test|294:317|True|
|r2:claim|claim|The delivery folder contains a yellow form|0:42, 147:189|True|
|r3:claim|claim|The stock counter remains seven|44:75, 191:222|True|
|r4:claim|claim|The break room has two chairs|77:106, 224:253|True|
|r5:claim|claim|The printer tray contains plain paper|108:145, 255:292|True|
|r6:claim|claim|the camera check begins|334:357|True|
|r6:basis1|basis|its lens is clean|375:392|True|
|r6:time1|time|at 14:20|358:366|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h03-full · hard · full

source_id: `3ae3f11ae8d2bdbb32b2471d`

The map instruction below concerns commercial reuse. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map because the licence excludes commercial distribution. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not publish the terrain map|347:377|True|
|r1:condition1|condition|commercial reuse|35:51|True|
|r1:basis1|basis|the licence excludes commercial distribution|386:430|True|
|r2:claim|claim|The delivery folder contains a yellow form|53:95, 200:242|True|
|r3:claim|claim|The stock counter remains seven|97:128, 244:275|True|
|r4:claim|claim|The break room has two chairs|130:159, 277:306|True|
|r5:claim|claim|The printer tray contains plain paper|161:198, 308:345|True|
|r6:claim|claim|publish the sketch|478:496|True|
|r6:condition1|condition|for classroom teaching|454:476|True|
|r6:basis1|basis|the teacher granted permission|505:535|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h03-partial · hard · partial

source_id: `40685e892acad37dacfb941f`

The map instruction below concerns commercial reuse. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not publish the terrain map|347:377|True|
|r1:condition1|condition|commercial reuse|35:51|True|
|r2:claim|claim|The delivery folder contains a yellow form|53:95, 200:242|True|
|r3:claim|claim|The stock counter remains seven|97:128, 244:275|True|
|r4:claim|claim|The break room has two chairs|130:159, 277:306|True|
|r5:claim|claim|The printer tray contains plain paper|161:198, 308:345|True|
|r6:claim|claim|publish the sketch|425:443|True|
|r6:condition1|condition|for classroom teaching|401:423|True|
|r6:basis1|basis|the teacher granted permission|452:482|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h03-none · hard · none

source_id: `c279181461b20f2f1c669e7d`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not publish the terrain map|294:324|True|
|r2:claim|claim|The delivery folder contains a yellow form|0:42, 147:189|True|
|r3:claim|claim|The stock counter remains seven|44:75, 191:222|True|
|r4:claim|claim|The break room has two chairs|77:106, 224:253|True|
|r5:claim|claim|The printer tray contains plain paper|108:145, 255:292|True|
|r6:claim|claim|publish the sketch|372:390|True|
|r6:condition1|condition|for classroom teaching|348:370|True|
|r6:basis1|basis|the teacher granted permission|399:429|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h04-full · hard · full

source_id: `a33e17f2ba65363cebfcd799`

The pack trial applies to desert depots. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. This proposed trial has no deployment approval. Independently, the warehouse rollout is approved.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we might trial pack G8|335:357|True|
|r1:condition1|condition|desert depots|26:39|True|
|r1:caveat1|caveat|This proposed trial has no deployment approval.|359:406|True|
|r2:claim|claim|The delivery folder contains a yellow form|41:83, 188:230|True|
|r3:claim|claim|The stock counter remains seven|85:116, 232:263|True|
|r4:claim|claim|The break room has two chairs|118:147, 265:294|True|
|r5:claim|claim|The printer tray contains plain paper|149:186, 296:333|True|
|r6:claim|claim|the warehouse rollout is approved|422:455|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h04-partial · hard · partial

source_id: `4d01cf1a2d288356cd77a2ad`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. This proposed trial has no deployment approval. Independently, the warehouse rollout is approved.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we might trial pack G8|294:316|True|
|r1:caveat1|caveat|This proposed trial has no deployment approval.|318:365|True|
|r2:claim|claim|The delivery folder contains a yellow form|0:42, 147:189|True|
|r3:claim|claim|The stock counter remains seven|44:75, 191:222|True|
|r4:claim|claim|The break room has two chairs|77:106, 224:253|True|
|r5:claim|claim|The printer tray contains plain paper|108:145, 255:292|True|
|r6:claim|claim|the warehouse rollout is approved|381:414|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h04-none · hard · none

source_id: `af364e2deb1a8beccdda9737`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. Independently, the warehouse rollout is approved.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we might trial pack G8|294:316|True|
|r2:claim|claim|The delivery folder contains a yellow form|0:42, 147:189|True|
|r3:claim|claim|The stock counter remains seven|44:75, 191:222|True|
|r4:claim|claim|The break room has two chairs|77:106, 224:253|True|
|r5:claim|claim|The printer tray contains plain paper|108:145, 255:292|True|
|r6:claim|claim|the warehouse rollout is approved|333:366|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h05-full · hard · full

source_id: `555ad2b11ff3eab2c2c09cb6`

The pressure audit ended at 16:40. The pressure audit concerns rig C9. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the pressure audit ended|0:24, 365:389|True|
|r1:condition1|condition|rig C9|63:69|True|
|r1:time1|time|at 16:40|25:33|True|
|r2:claim|claim|The delivery folder contains a yellow form|71:113, 218:260|True|
|r3:claim|claim|The stock counter remains seven|115:146, 262:293|True|
|r4:claim|claim|The break room has two chairs|148:177, 295:324|True|
|r5:claim|claim|The printer tray contains plain paper|179:216, 326:363|True|
|r6:claim|claim|the noise audit starts|403:425|True|
|r6:condition1|condition|on rig B7|435:444|True|
|r6:time1|time|at 16:40|426:434|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h05-partial · hard · partial

source_id: `4852a9ecdb538c2eea9f574f`

The pressure audit ended at 16:40. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the pressure audit ended|0:24, 329:353|True|
|r1:time1|time|at 16:40|25:33|True|
|r2:claim|claim|The delivery folder contains a yellow form|35:77, 182:224|True|
|r3:claim|claim|The stock counter remains seven|79:110, 226:257|True|
|r4:claim|claim|The break room has two chairs|112:141, 259:288|True|
|r5:claim|claim|The printer tray contains plain paper|143:180, 290:327|True|
|r6:claim|claim|the noise audit starts|367:389|True|
|r6:condition1|condition|on rig B7|399:408|True|
|r6:time1|time|at 16:40|390:398|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h05-none · hard · none

source_id: `402c5d204d14decdfde55482`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the pressure audit ended|294:318|True|
|r2:claim|claim|The delivery folder contains a yellow form|0:42, 147:189|True|
|r3:claim|claim|The stock counter remains seven|44:75, 191:222|True|
|r4:claim|claim|The break room has two chairs|77:106, 224:253|True|
|r5:claim|claim|The printer tray contains plain paper|108:145, 255:292|True|
|r6:claim|claim|the noise audit starts|332:354|True|
|r6:condition1|condition|on rig B7|364:373|True|
|r6:time1|time|at 16:40|355:363|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h06-full · hard · full

source_id: `efddc392b4e4160ae4f7d3a1`

The coil estimate concerns operation in nitrogen. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. This capacity is conjectural and has not been measured. A separate steel cable was measured at 12 amperes in air.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect coil N8 may handle 18 amperes|344:383|True|
|r1:condition1|condition|in nitrogen|37:48|True|
|r1:caveat1|caveat|This capacity is conjectural and has not been measured.|385:440|True|
|r2:claim|claim|The delivery folder contains a yellow form|50:92, 197:239|True|
|r3:claim|claim|The stock counter remains seven|94:125, 241:272|True|
|r4:claim|claim|The break room has two chairs|127:156, 274:303|True|
|r5:claim|claim|The printer tray contains plain paper|158:195, 305:342|True|
|r6:claim|claim|A separate steel cable was measured at 12 amperes|441:490|True|
|r6:condition1|condition|in air|491:497|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h06-partial · hard · partial

source_id: `facb6ceb1eaf49e0fad2f32f`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. This capacity is conjectural and has not been measured. A separate steel cable was measured at 12 amperes in air.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect coil N8 may handle 18 amperes|294:333|True|
|r1:caveat1|caveat|This capacity is conjectural and has not been measured.|335:390|True|
|r2:claim|claim|The delivery folder contains a yellow form|0:42, 147:189|True|
|r3:claim|claim|The stock counter remains seven|44:75, 191:222|True|
|r4:claim|claim|The break room has two chairs|77:106, 224:253|True|
|r5:claim|claim|The printer tray contains plain paper|108:145, 255:292|True|
|r6:claim|claim|A separate steel cable was measured at 12 amperes|391:440|True|
|r6:condition1|condition|in air|441:447|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## h06-none · hard · none

source_id: `b8137148fb3148d41392137f`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. A separate steel cable was measured at 12 amperes in air.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect coil N8 may handle 18 amperes|294:333|True|
|r2:claim|claim|The delivery folder contains a yellow form|0:42, 147:189|True|
|r3:claim|claim|The stock counter remains seven|44:75, 191:222|True|
|r4:claim|claim|The break room has two chairs|77:106, 224:253|True|
|r5:claim|claim|The printer tray contains plain paper|108:145, 255:292|True|
|r6:claim|claim|A separate steel cable was measured at 12 amperes|335:384|True|
|r6:condition1|condition|in air|385:391|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n01 · medium · full

source_id: `2532b1977fc260894d4d3a7e`

@all [Task Completed] Hello everyone, the task "Verify the accuracy of alarm rule creation and trigger logic" for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed. All test cases have passed, including various single conditions, combined conditions, and boundary value scenarios. The few issues discovered yesterday have also all been regression verified and passed. The final test report has been uploaded to Confluence. 🎉

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the task "Verify the accuracy of alarm rule creation and trigger logic" for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed|38:212|True|
|r2:claim|claim|All test cases have passed|214:240|True|
|r2:caveat1|caveat|including various single conditions, combined conditions, and boundary value scenarios|242:328|True|
|r3:claim|claim|The few issues discovered yesterday have also all been regression verified and passed|330:415|True|
|r3:time1|time|yesterday|356:365|True|
|r4:claim|claim|The final test report has been uploaded to Confluence|417:470|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n02 · medium · full

source_id: `eeab452b3cb6dfffe3b2a655`

Good morning everyone. Today is Thursday. Just a reminder to @Hanqiang Liang and @Huihong Tian, your medication check-in module and family member invitation interface are due today. Please make sure to complete the delivery today. Other colleagues, please also share your plans and progress for today.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|Today is Thursday|23:40|True|
|r1:time1|time|Today|23:28, 175:180, 224:229, 295:300|True|
|r1:time2|time|Thursday|32:40|True|
|r2:claim|claim|your medication check-in module and family member invitation interface are due today|96:180|True|
|r2:time1|time|today|23:28, 175:180, 224:229, 295:300|True|
|r2:time2|time|Thursday|32:40|True|
|r2:recipient1|recipient|@Hanqiang Liang and @Huihong Tian|61:94|True|
|r3:claim|claim|Please make sure to complete the delivery today|182:229|True|
|r3:time1|time|today|23:28, 175:180, 224:229, 295:300|True|
|r3:time2|time|Thursday|32:40|True|
|r3:subject1|subject|your medication check-in module and family member invitation interface|96:166|True|
|r4:claim|claim|Other colleagues, please also share your plans and progress for today|231:300|True|
|r4:time1|time|today|23:28, 175:180, 224:229, 295:300|True|
|r4:time2|time|Thursday|32:40|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n03 · medium · full

source_id: `ef3ed7f7d45447190441c6bf`

Hello everyone, today I'm starting a new design task: [Designing a File Storage Solution]. Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3. The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack. A preliminary selection recommendation report will be provided early next week.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|today I'm starting a new design task: [Designing a File Storage Solution]|16:89|True|
|r1:time1|time|today|16:21|True|
|r2:claim|claim|I will focus on comparing Azure Blob and AWS S3|207:254|True|
|r2:basis1|basis|our system will need to store a large number of supporting documents, reports, etc. in the future|108:205|True|
|r3:claim|claim|The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack|256:416|True|
|r4:claim|claim|A preliminary selection recommendation report will be provided early next week|418:496|True|
|r4:time1|time|early next week|481:496|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n04 · medium · full

source_id: `a3bb92bc6e953b07984eaa93`

Good morning everyone. Regarding the design of our file storage solution, I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday. From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage, and our other projects are also on AWS. Today, I will start designing the Bucket Policy and directory structure based on S3, for example, isolating by tenant and file type.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday|74:147|True|
|r1:time1|time|last Friday|136:147|True|
|r2:claim|claim|AWS S3 has a slight advantage|205:234|True|
|r2:condition1|condition|From the perspective of cost and ecosystem integration|149:203|True|
|r3:claim|claim|our other projects are also on AWS|240:274|True|
|r4:claim|claim|I will start designing the Bucket Policy and directory structure based on S3|283:359|True|
|r4:time1|time|Today|276:281|True|
|r4:method1|method|isolating by tenant and file type|374:407|True|
|r4:optional_basis1|basis|AWS S3 has a slight advantage|205:234|False|
|r4:optional_basis2|basis|our other projects are also on AWS|240:274|False|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n05 · medium · full

source_id: `b9a2917d39af17f120e6fb74`

Good morning everyone, regarding the file storage solution, the complete technical design document (based on AWS S3) has been uploaded to Confluence. It includes three main parts: bucket permission policies, lifecycle rules, and recommended directory structure. @Mingzhi Li Boss Li, please review it.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the complete technical design document (based on AWS S3) has been uploaded to Confluence|60:148|True|
|r2:claim|claim|It includes three main parts: bucket permission policies, lifecycle rules, and recommended directory structure|150:260|True|
|r2:subject1|subject|the complete technical design document (based on AWS S3)|60:116|True|
|r3:claim|claim|please review it|283:299|True|
|r3:subject1|subject|the complete technical design document (based on AWS S3)|60:116|True|
|r3:recipient1|recipient|@Mingzhi Li Boss Li|262:281|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n06 · hard · partial

source_id: `cc0f8301e58ac1340b77a5ef`

@Lujian Gao I've finished reviewing the document on the file storage solution. The design is very comprehensive, especially the considerations for tenant data isolation and cost optimization. The proposal is approved and can be finalized.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I've finished reviewing the document on the file storage solution|12:77|True|
|r2:claim|claim|The design is very comprehensive|79:111|True|
|r2:caveat1|caveat|especially the considerations for tenant data isolation and cost optimization|113:190|True|
|r3:claim|claim|The proposal is approved and can be finalized|192:237|True|
|r3:subject1|subject|the file storage solution|52:77|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n07 · medium · full

source_id: `e736ba69ded95cdd2331a4e8`

@Yang Zhao Good question. Regarding the "forgot password" process, our main security consideration is to prevent "user enumeration attacks." Therefore, regardless of whether the email entered by the user exists or not, the feedback message should be consistent, such as "If this email address is registered, you will receive an email containing a password reset link," instead of directly prompting "user does not exist." Please ensure the UI copy adheres to this principle.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|our main security consideration is to prevent "user enumeration attacks."|67:140|True|
|r1:condition1|condition|forgot password|41:56|True|
|r2:claim|claim|the feedback message should be consistent|219:260|True|
|r2:condition1|condition|forgot password|41:56|True|
|r2:condition2|condition|regardless of whether the email entered by the user exists or not|152:217|True|
|r2:basis1|basis|prevent "user enumeration attacks."|105:140|True|
|r2:method1|method|such as "If this email address is registered, you will receive an email containing a password reset link,"|262:368|True|
|r2:method2|method|instead of directly prompting "user does not exist."|369:421|True|
|r3:claim|claim|Please ensure the UI copy adheres to this principle|422:473|True|
|r3:subject1|subject|the feedback message should be consistent|219:260|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n08 · easy · full

source_id: `fc8ef24a21781a9bc3026f2c`

Email received. The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction. @Xinjie Li @Xuexin Yin, please assess the scope of impact on the backend.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction|92:185|True|
|r1:condition1|condition|all accounts marked as `ACCOUNT_STATUS_LOCKED`|45:91|True|
|r2:claim|claim|please assess the scope of impact on the backend|211:259|True|
|r2:recipient1|recipient|@Xinjie Li @Xuexin Yin|187:209|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n09 · medium · full

source_id: `82db5705bd31ef3b677608e5`

The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`, defined as 'Explicit Status Alert Policy'. It is mainly used for scenarios where an account is locked, requiring explicit interruption of user operations and guidance to manual channels.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`|0:61|True|
|r1:caveat1|caveat|defined as 'Explicit Status Alert Policy'|63:104|True|
|r2:claim|claim|requiring explicit interruption of user operations and guidance to manual channels|166:248|True|
|r2:condition1|condition|where an account is locked|138:164|True|
|r2:subject1|subject|`ERR_POLICY_LOCKED_ACCOUNT_V1`|31:61|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n10 · hard · partial

source_id: `f3e4d9a3e84884e5abe2e967`

Received. I've reviewed the document. This strategy will be handled by `ExplicitStateAlertModule`, and the parameter `halt_downstream_triggers` is set to `true`. This means that after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted, right?

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I've reviewed the document|10:36|True|
|r2:claim|claim|This strategy will be handled by `ExplicitStateAlertModule`|38:97|True|
|r3:claim|claim|the parameter `halt_downstream_triggers` is set to `true`|103:160|True|
|r4:claim|claim|all downstream automated notifications (emails, SMS) will be halted|220:287|True|
|r4:condition1|condition|after the backend triggers this strategy|178:218|True|
|r4:caveat1|caveat|right?|289:295|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n11 · hard · partial

source_id: `2f036a676a1e734b9821a11d`

@Xinjie Li Yes, your understanding is completely correct. This is to avoid sending users redundant or potentially confusing automated messages.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|your understanding is completely correct|16:56|True|
|r2:claim|claim|This is to avoid sending users redundant or potentially confusing automated messages|58:142|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

미해결 참조 r1: Confirmed proposition is not contained in this source.

미해결 참조 r2: Antecedent of This and your understanding is outside this source; no policy code or interrupted event can be invented.

## n12 · medium · full

source_id: `ea426379076abc7e9d24ecbb`

Received, thanks a lot! The data structure looks very clear. I plan to complete the static data integration this morning to ensure the charts render correctly. In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it. @Mingzhi Li

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|The data structure looks very clear|24:59|True|
|r2:claim|claim|I plan to complete the static data integration this morning|61:120|True|
|r2:basis1|basis|to ensure the charts render correctly|121:158|True|
|r2:time1|time|this morning|108:120|True|
|r3:claim|claim|I'll start researching dynamic refresh solutions|178:226|True|
|r3:time1|time|In the afternoon|160:176|True|
|r4:claim|claim|initially considering WebSocket|228:259|True|
|r4:condition1|condition|if the backend supports it|260:286|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n13 · hard · full

source_id: `9279497ab46d95f158eeb6de`

@Yunqi Qian Great plan. WebSocket is the best solution, but our message push service isn't fully ready yet. This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds. Once the WebSocket service is stable later, we can upgrade it uniformly. This way, we can avoid blocking your current task.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|WebSocket is the best solution|24:54|True|
|r2:claim|claim|our message push service isn't fully ready yet|60:106|True|
|r3:claim|claim|This task can be implemented using polling for now|108:158|True|
|r3:basis1|basis|avoid blocking your current task|309:341|True|
|r3:time1|time|for now|151:158|True|
|r3:method1|method|by requesting the interface every 10 seconds|173:217|True|
|r3:optional_basis1|basis|our message push service isn't fully ready yet|60:106|False|
|r4:claim|claim|we can upgrade it uniformly|263:290|True|
|r4:condition1|condition|Once the WebSocket service is stable later|219:261|True|
|r4:time1|time|later|256:261|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

## n14 · hard · partial

source_id: `b3a1426c132e34bf7819b9fd`

Okay, Boss Li, understood. Then I'll use the polling solution for now, and I'll adjust the plan.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I'll use the polling solution for now|32:69|True|
|r1:time1|time|for now|62:69|True|
|r2:claim|claim|I'll adjust the plan|75:95|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

미해결 참조 r1: The rationale for polling is absent from this message.

