# Case-by-case fixed-span binding results

Counts include all typed edges in the frozen scorer, not just condition/basis. Existing failures remain counted. This is records evaluation, not QA accuracy.

| Case | Baseline TP/FP | Atomic TP/FP | Group TP/FP | New correct links | Old complete lost |
|---|---:|---:|---:|---|---|
| e01-full | 2/0 | 2/0 | 2/0 | [] | False |
| e01-partial | 1/0 | 1/1 | 1/1 | [] | True |
| e01-none | 0/0 | 0/0 | 0/0 | [] | False |
| e02-full | 1/1 | 1/2 | 1/2 | [] | False |
| e02-partial | 0/1 | 0/1 | 0/1 | [] | False |
| e02-none | 0/0 | 0/0 | 0/0 | [] | False |
| e03-full | 2/0 | 2/1 | 2/1 | [] | True |
| e03-partial | 1/0 | 1/0 | 1/0 | [] | False |
| e03-none | 0/0 | 0/0 | 0/0 | [] | False |
| e04-full | 2/0 | 2/5 | 2/3 | [] | True |
| e04-partial | 1/0 | 1/3 | 1/2 | [] | True |
| e04-none | 0/0 | 0/0 | 0/0 | [] | False |
| e05-full | 1/0 | 1/1 | 1/1 | [] | False |
| e05-partial | 1/0 | 1/1 | 1/1 | [] | True |
| e05-none | 0/0 | 0/0 | 0/0 | [] | False |
| e06-full | 2/0 | 2/5 | 2/3 | [] | True |
| e06-partial | 1/0 | 1/3 | 1/2 | [] | True |
| e06-none | 0/0 | 0/0 | 0/0 | [] | False |
| m01-full | 0/0 | 0/0 | 0/0 | [] | False |
| m01-partial | 0/0 | 0/0 | 0/0 | [] | False |
| m01-none | 0/0 | 0/0 | 0/0 | [] | False |
| m02-full | 1/1 | 1/7 | 1/7 | [] | False |
| m02-partial | 0/1 | 0/2 | 0/2 | [] | False |
| m02-none | 0/0 | 0/0 | 0/0 | [] | False |
| m03-full | 0/1 | 2/6 | 2/6 | [['r1', 'basis', 'r1:basis1'], ['r1', 'condition', 'r1:condition1']] | False |
| m03-partial | 1/0 | 1/3 | 1/3 | [] | True |
| m03-none | 0/0 | 0/2 | 0/2 | [] | True |
| m04-full | 1/1 | 1/12 | 1/8 | [] | False |
| m04-partial | 1/0 | 1/4 | 1/3 | [] | True |
| m04-none | 0/0 | 0/0 | 0/0 | [] | False |
| m05-full | 0/1 | 0/6 | 0/6 | [] | False |
| m05-partial | 0/1 | 0/5 | 0/5 | [] | False |
| m05-none | 0/0 | 0/0 | 0/0 | [] | False |
| m06-full | 1/1 | 1/13 | 1/9 | [] | False |
| m06-partial | 1/0 | 1/3 | 1/2 | [] | True |
| m06-none | 0/0 | 0/0 | 0/0 | [] | False |
| h01-full | 1/3 | 1/14 | 1/14 | [] | False |
| h01-partial | 2/1 | 2/8 | 2/8 | [] | False |
| h01-none | 2/0 | 2/3 | 2/3 | [] | True |
| h02-full | 0/0 | 0/0 | 0/0 | [] | False |
| h02-partial | 0/2 | 1/7 | 1/7 | [['r1', 'basis', 'r1:basis1']] | False |
| h02-none | 0/2 | 0/10 | 0/10 | [] | False |
| h03-full | 2/1 | 4/9 | 4/7 | [['r1', 'basis', 'r1:basis1'], ['r1', 'condition', 'r1:condition1']] | False |
| h03-partial | 0/0 | 1/14 | 1/8 | [['r1', 'condition', 'r1:condition1']] | False |
| h03-none | 2/1 | 2/9 | 2/8 | [] | False |
| h04-full | 1/0 | 1/4 | 1/2 | [] | False |
| h04-partial | 1/0 | 1/11 | 1/6 | [] | True |
| h04-none | 0/0 | 0/2 | 0/2 | [] | True |
| h05-full | 0/0 | 0/0 | 0/0 | [] | False |
| h05-partial | 0/0 | 0/0 | 0/0 | [] | False |
| h05-none | 0/0 | 0/4 | 0/4 | [] | False |
| h06-full | 1/0 | 1/12 | 2/6 | [] | False |
| h06-partial | 1/0 | 1/10 | 1/7 | [] | False |
| h06-none | 0/0 | 0/3 | 0/3 | [] | False |
| n01 | 0/0 | 0/0 | 0/0 | [] | False |
| n02 | 0/1 | 0/10 | 0/10 | [] | False |
| n03 | 0/1 | 1/9 | 1/9 | [['r2', 'basis', 'r2:basis1']] | False |
| n04 | 3/0 | 3/20 | 3/22 | [] | False |
| n05 | 1/0 | 1/19 | 1/13 | [] | False |
| n06 | 1/0 | 1/12 | 1/7 | [] | False |
| n07 | 0/0 | 0/0 | 0/0 | [] | False |
| n08 | 1/1 | 1/7 | 1/7 | [] | False |
| n09 | 1/0 | 1/24 | 2/8 | [] | False |
| n10 | 1/0 | 1/11 | 1/15 | [] | False |
| n11 | 0/0 | 0/2 | 0/4 | [] | False |
| n12 | 2/2 | 2/23 | 2/20 | [] | False |
| n13 | 0/2 | 1/32 | 1/32 | [['r3', 'basis', 'r3:basis1']] | False |
| n14 | 0/0 | 0/5 | 0/5 | [] | False |

## Every newly persisted edge

The two source quotes below are the actual selected endpoints. Marginal changes use the unchanged scorer with exactly one new edge; they do not override aggregate scoring.

### e01-partial / b:22fbe99ab808b630b441c5d9

- Target: "use liner K6"
- Context: "For chilled parcels"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:condition1')]`

### e02-full / b:15adb1ed093b36fa110e0eb9

- Target: "close gate R8"
- Context: "Thursday"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:time1')]`

### e03-full / b:847142600c57f5d478a8bb0a

- Target: "do not ship kit M3"
- Context: "the seal failed inspection"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:basis1')]`

### e04-full / b:c208d650f30d8b6aa27f5e91

- Target: "This trial is not approved"
- Context: "For inland stations"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:c208d650f30d8b6aa27f5e91', 'basis', 'r1:condition1'), ('unbound:b:c208d650f30d8b6aa27f5e91', 'caveat', 'r1:caveat1')]`

### e04-full / b:74d86239c6010a3238a0c898

- Target: "This trial is not approved"
- Context: "we might trial paint Q9"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:74d86239c6010a3238a0c898', 'caveat', 'r1:caveat1'), ('unbound:b:74d86239c6010a3238a0c898', 'condition', 'r1:claim')]`

### e04-full / b:3b08718faf46a7839ae7e1d9

- Target: "we might trial paint Q9"
- Context: "This trial is not approved"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:caveat1')]`

### e04-partial / b:ddc601ae6b3699228d2c37c0

- Target: "This trial is not approved"
- Context: "we might trial paint Q9"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:ddc601ae6b3699228d2c37c0', 'caveat', 'r1:caveat1'), ('unbound:b:ddc601ae6b3699228d2c37c0', 'condition', 'r1:claim')]`

### e04-partial / b:7b8a746af41ddede21362d80

- Target: "we might trial paint Q9"
- Context: "This trial is not approved"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:caveat1')]`

### e05-full / b:0a9cf7e38282fe7b317a7503

- Target: "the sensor check is complete for firmware 6"
- Context: "on Tuesday"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:time1')]`

### e05-partial / b:7da8c39d2f3b581082df90b4

- Target: "the sensor check is complete"
- Context: "on Tuesday"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:time1')]`

### e06-full / b:a3f82bf9eede0ea7d9f3a023

- Target: "This estimate is untested"
- Context: "For dry rooms"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:a3f82bf9eede0ea7d9f3a023', 'basis', 'r1:condition1'), ('unbound:b:a3f82bf9eede0ea7d9f3a023', 'caveat', 'r1:caveat1')]`

### e06-full / b:eeb8a71f6ce1f3ee3acbab3d

- Target: "This estimate is untested"
- Context: "I suspect relay P4 may last 80 days"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:eeb8a71f6ce1f3ee3acbab3d', 'caveat', 'r1:caveat1'), ('unbound:b:eeb8a71f6ce1f3ee3acbab3d', 'condition', 'r1:claim')]`

### e06-full / b:a61651dbc0cdf6ce560d1e32

- Target: "I suspect relay P4 may last 80 days"
- Context: "This estimate is untested"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:caveat1')]`

### e06-partial / b:c5a67ca787a2c476332149dc

- Target: "This estimate is untested"
- Context: "I suspect relay P4 may last 80 days"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:c5a67ca787a2c476332149dc', 'basis', 'r1:claim'), ('unbound:b:c5a67ca787a2c476332149dc', 'caveat', 'r1:caveat1')]`

### e06-partial / b:c06e1c60d939b48b9931f9b1

- Target: "I suspect relay P4 may last 80 days"
- Context: "This estimate is untested"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:caveat1')]`

### m02-full / b:6a7aba5cb22484af00be4803

- Target: "The antenna colour remains white"
- Context: "Timing for the following beacon instruction"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:6a7aba5cb22484af00be4803', 'basis', 'unmatched:6')]`

### m02-full / b:9f70c3ffd65cedeca1baf848

- Target: "switch the beacon to standby"
- Context: "Timing for the following beacon instruction"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:9f70c3ffd65cedeca1baf848', 'condition', 'unmatched:6')]`

### m02-full / b:b9adeb4a812b23d999f74465

- Target: "switch the beacon to standby"
- Context: "after the morning inspection"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:time1')]`

### m02-full / b:c6be1028c17f8a00335cb178

- Target: "switch the beacon to standby"
- Context: "The antenna colour remains white"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r2:claim')]`

### m02-full / b:2b4b579ef3e3faf3bdca47b5

- Target: "Timing for the following beacon instruction"
- Context: "switch the beacon to standby"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:2b4b579ef3e3faf3bdca47b5', 'condition', 'r1:claim')]`

### m02-full / b:86cd39d902da735ccb97d8e2

- Target: "Timing for the following beacon instruction"
- Context: "the battery is leaking"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:86cd39d902da735ccb97d8e2', 'condition', 'r1:basis1')]`

### m02-partial / b:68d057d086a443a346adbaa5

- Target: "switch the beacon to standby"
- Context: "The antenna colour remains white"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r2:claim')]`

### m03-full / b:4905334cb784f3588c9b8c08

- Target: "do not release batch U5"
- Context: "The following release instruction applies to saline batches"
- Relation: `condition`
- New correct: `[('r1', 'condition', 'r1:condition1')]`
- New wrong: `[]`

### m03-full / b:ca16529d602f37d70681364b

- Target: "Freshwater batches remain eligible for release"
- Context: "The following release instruction applies to saline batches"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r1:condition1')]`

### m03-full / b:633a329c450dc46d8d58ecd5

- Target: "The following release instruction applies to saline batches"
- Context: "do not release batch U5"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:633a329c450dc46d8d58ecd5', 'basis', 'r1:claim')]`

### m03-full / b:be05cd8ed968a67a94339c38

- Target: "The following release instruction applies to saline batches"
- Context: "because the residue test failed"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:be05cd8ed968a67a94339c38', 'condition', 'r1:basis1')]`

### m03-full / b:f048c5f03eeeae4abc8ba189

- Target: "do not release batch U5"
- Context: "because the residue test failed"
- Relation: `basis`
- New correct: `[('r1', 'basis', 'r1:basis1')]`
- New wrong: `[]`

### m03-full / b:5f2bd8fd36bf2fefc288e5ca

- Target: "The following release instruction applies to saline batches"
- Context: "Freshwater batches remain eligible for release"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:5f2bd8fd36bf2fefc288e5ca', 'basis', 'r2:claim')]`

### m03-full / b:79e1e9fc6ae8ef3bce25dec1

- Target: "do not release batch U5"
- Context: "Freshwater batches remain eligible for release"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r2:claim')]`

### m03-partial / b:38af8897212997bb7b522158

- Target: "Freshwater batches remain eligible for release"
- Context: "The following release instruction applies to saline batches"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r1:condition1')]`

### m03-partial / b:f51546aa6d52077e72e3a1cd

- Target: "Freshwater batches remain eligible for release"
- Context: "do not release batch U5"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r2', 'condition', 'r1:claim')]`

### m03-partial / b:e84c8e950f83a8a11173301a

- Target: "do not release batch U5"
- Context: "Freshwater batches remain eligible for release"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r2:claim')]`

### m03-none / b:9f83b99821080ba91144cde1

- Target: "Freshwater batches remain eligible for release"
- Context: "do not release batch U5"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r2', 'condition', 'r1:claim')]`

### m03-none / b:c3553906f1823f191fa15055

- Target: "do not release batch U5"
- Context: "Freshwater batches remain eligible for release"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r2:claim')]`

### m04-full / b:87392db1f149be10c90a205f

- Target: "This pilot is a suggestion, not an authorization"
- Context: "Scope of the filter pilot"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:87392db1f149be10c90a205f', 'basis', 'unmatched:6'), ('unbound:b:87392db1f149be10c90a205f', 'caveat', 'r1:caveat1')]`

### m04-full / b:3b4e4817574848963f358489

- Target: "remote clinics"
- Context: "The spare tubing is blue"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:3b4e4817574848963f358489', 'condition', 'r2:claim')]`

### m04-full / b:e791dac2d9337ce7afe5550d

- Target: "we could pilot filter J2"
- Context: "The spare tubing is blue"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r2:claim')]`

### m04-full / b:f915f0743cee90e57e6eb656

- Target: "This pilot is a suggestion, not an authorization"
- Context: "The spare tubing is blue"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:f915f0743cee90e57e6eb656', 'basis', 'r2:claim'), ('unbound:b:f915f0743cee90e57e6eb656', 'caveat', 'r1:caveat1')]`

### m04-full / b:af7b3033eb46584fbd638354

- Target: "remote clinics"
- Context: "we could pilot filter J2"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:af7b3033eb46584fbd638354', 'condition', 'r1:claim')]`

### m04-full / b:65f85f8ddfd758be7913a6da

- Target: "This pilot is a suggestion, not an authorization"
- Context: "we could pilot filter J2"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:65f85f8ddfd758be7913a6da', 'basis', 'r1:claim'), ('unbound:b:65f85f8ddfd758be7913a6da', 'caveat', 'r1:caveat1')]`

### m04-full / b:8a84e7234e8981ffa51e70ce

- Target: "remote clinics"
- Context: "This pilot is a suggestion, not an authorization"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:8a84e7234e8981ffa51e70ce', 'condition', 'r1:caveat1')]`

### m04-full / b:90b812710026e8547fae29b9

- Target: "we could pilot filter J2"
- Context: "This pilot is a suggestion, not an authorization"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:caveat1')]`

### m04-partial / b:21ac826895ea99a6e0e8aacc

- Target: "we could pilot filter J2"
- Context: "The spare tubing is blue"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r2:claim')]`

### m04-partial / b:522df2beb2fc6966d0ce0ab7

- Target: "This pilot is a suggestion, not an authorization"
- Context: "The spare tubing is blue"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:522df2beb2fc6966d0ce0ab7', 'caveat', 'r1:caveat1'), ('unbound:b:522df2beb2fc6966d0ce0ab7', 'condition', 'r2:claim')]`

### m04-partial / b:c116eb78590e8048b9d0a6c0

- Target: "we could pilot filter J2"
- Context: "This pilot is a suggestion, not an authorization"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:caveat1')]`

### m05-full / b:b1b67644598dc92f0cc7e789

- Target: "The office clock was repaired"
- Context: "The calibration event occurred"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:b1b67644598dc92f0cc7e789', 'condition', 'unmatched:5')]`

### m05-full / b:62a865c221e1e753e8f2a525

- Target: "The calibration event occurred"
- Context: "on Friday afternoon"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:62a865c221e1e753e8f2a525', 'condition', 'r1:time1')]`

### m05-full / b:2a7467e5c10f7c5f931824c6

- Target: "The calibration event occurred"
- Context: "The office clock was repaired"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:2a7467e5c10f7c5f931824c6', 'condition', 'r2:claim')]`

### m05-full / b:e3d5e4ab9caffceba30da94f

- Target: "The calibration event occurred"
- Context: "the valve calibration finished on bench T7"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:e3d5e4ab9caffceba30da94f', 'basis', 'r1:claim'), ('unbound:b:e3d5e4ab9caffceba30da94f', 'basis', 'r1:condition1')]`

### m05-partial / b:a3f007e16528aed86d751325

- Target: "The office clock was repaired"
- Context: "The calibration event occurred"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:a3f007e16528aed86d751325', 'condition', 'unmatched:5')]`

### m05-partial / b:82c0d60c35772cf34dcf7aaa

- Target: "The calibration event occurred"
- Context: "on Friday afternoon"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:82c0d60c35772cf34dcf7aaa', 'condition', 'r1:time1')]`

### m05-partial / b:3fef6971cdff74f469f68e91

- Target: "The calibration event occurred"
- Context: "The office clock was repaired"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:3fef6971cdff74f469f68e91', 'condition', 'r2:claim')]`

### m05-partial / b:61d6166550b53af53b1d381c

- Target: "The calibration event occurred"
- Context: "the valve calibration finished"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:61d6166550b53af53b1d381c', 'basis', 'r1:claim')]`

### m06-full / b:cbf1259be378e6896816e2ff

- Target: "The procurement task is complete"
- Context: "Operating scope of this estimate"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:cbf1259be378e6896816e2ff', 'condition', 'unmatched:6')]`

### m06-full / b:94288d740fe72f5d02701a78

- Target: "No measurement supports this estimate yet"
- Context: "Operating scope of this estimate"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:94288d740fe72f5d02701a78', 'basis', 'unmatched:6'), ('unbound:b:94288d740fe72f5d02701a78', 'caveat', 'r1:caveat1')]`

### m06-full / b:cf7a2389298b66f0bb23ed78

- Target: "No measurement supports this estimate yet"
- Context: "under reduced load"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:cf7a2389298b66f0bb23ed78', 'basis', 'r1:condition1'), ('unbound:b:cf7a2389298b66f0bb23ed78', 'caveat', 'r1:caveat1')]`

### m06-full / b:cec06a87eabe1087472645fb

- Target: "Operating scope of this estimate"
- Context: "The procurement task is complete"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:cec06a87eabe1087472645fb', 'condition', 'r2:claim')]`

### m06-full / b:619fd50e662a03fc3b451951

- Target: "No measurement supports this estimate yet"
- Context: "The procurement task is complete"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:619fd50e662a03fc3b451951', 'basis', 'r2:claim'), ('unbound:b:619fd50e662a03fc3b451951', 'caveat', 'r1:caveat1')]`

### m06-full / b:389477c5625daaaeecfca37b

- Target: "Operating scope of this estimate"
- Context: "I suspect drive L4 may reach 70 cycles"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:389477c5625daaaeecfca37b', 'condition', 'r1:claim')]`

### m06-full / b:32bb74fb4ba22e8f3292a7a5

- Target: "No measurement supports this estimate yet"
- Context: "I suspect drive L4 may reach 70 cycles"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:32bb74fb4ba22e8f3292a7a5', 'basis', 'r1:claim'), ('unbound:b:32bb74fb4ba22e8f3292a7a5', 'caveat', 'r1:caveat1')]`

### m06-full / b:d9932de8c0d113f473467e15

- Target: "I suspect drive L4 may reach 70 cycles"
- Context: "No measurement supports this estimate yet"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:caveat1')]`

### m06-partial / b:196bced2c1befbb4b2fe2e8d

- Target: "No measurement supports this estimate yet"
- Context: "I suspect drive L4 may reach 70 cycles"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:196bced2c1befbb4b2fe2e8d', 'caveat', 'r1:caveat1'), ('unbound:b:196bced2c1befbb4b2fe2e8d', 'condition', 'r1:claim')]`

### m06-partial / b:6a9c9d28e698aa6c279adf66

- Target: "I suspect drive L4 may reach 70 cycles"
- Context: "No measurement supports this estimate yet"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:caveat1')]`

### h01-full / b:60042ddc70b8f74d89be7d92

- Target: "halt compressor Z4"
- Context: "Scope of the compressor instruction"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:60042ddc70b8f74d89be7d92', 'condition', 'unmatched:13')]`

### h01-full / b:91ba5e596132bf01c311b7a9

- Target: "start pump B2"
- Context: "Scope of the compressor instruction"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:91ba5e596132bf01c311b7a9', 'basis', 'unmatched:13')]`

### h01-full / b:68a949264e8873deea826b5b

- Target: "halt compressor Z4"
- Context: "pressure above 9 bar"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:condition1')]`

### h01-full / b:68a6214fe28eabfb0aa1a0ab

- Target: "start pump B2"
- Context: "pressure above 9 bar"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:condition1')]`

### h01-full / b:a5d55cf33bf49235dbbb2aef

- Target: "start pump B2"
- Context: "halt compressor Z4"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r6', 'condition', 'r1:claim')]`

### h01-full / b:96d2ca0cba7323876d22dc18

- Target: "start pump B2"
- Context: "its casing has fractured"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:basis1')]`

### h01-full / b:47397c9370f3789ef651f4fe

- Target: "halt compressor Z4"
- Context: "Separate instruction"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:47397c9370f3789ef651f4fe', 'basis', 'unmatched:13')]`

### h01-full / b:49735c6f3502fd35ec95d19c

- Target: "start pump B2"
- Context: "Separate instruction"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:49735c6f3502fd35ec95d19c', 'condition', 'unmatched:13')]`

### h01-full / b:2d21b488b85ab31db178c6a5

- Target: "halt compressor Z4"
- Context: "below 1 bar"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r6:condition1')]`

### h01-full / b:2059121fae85509a558c8e72

- Target: "start pump B2"
- Context: "below 1 bar"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r6:condition1')]`

### h01-full / b:1c2ec98d0f53168f6b1db1c8

- Target: "halt compressor Z4"
- Context: "the buffer is empty"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:basis1')]`

### h01-partial / b:2be25bec56f973efcf98be13

- Target: "halt compressor Z4"
- Context: "pressure above 9 bar"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:condition1')]`

### h01-partial / b:88a1726f2f3f0b83c9fa8e0d

- Target: "start pump B2"
- Context: "pressure above 9 bar"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r6', 'condition', 'r1:condition1')]`

### h01-partial / b:ec99a2e576c5fd05f60519be

- Target: "start pump B2"
- Context: "halt compressor Z4"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r6', 'condition', 'r1:claim')]`

### h01-partial / b:f8a324b002d3fee12a6c13df

- Target: "halt compressor Z4"
- Context: "Separate instruction"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:f8a324b002d3fee12a6c13df', 'basis', 'unmatched:12')]`

### h01-partial / b:88b9d61449f55a47696b1f9d

- Target: "start pump B2"
- Context: "Separate instruction"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:88b9d61449f55a47696b1f9d', 'condition', 'unmatched:12')]`

### h01-partial / b:5ec90586bc236b482b5c3256

- Target: "halt compressor Z4"
- Context: "start pump B2"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:claim')]`

### h01-partial / b:76378bf8351a6dbd81001893

- Target: "start pump B2"
- Context: "the buffer is empty"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r6', 'condition', 'r6:basis1')]`

### h01-none / b:df9b3a9a6e9cf5acb3b4b107

- Target: "start pump B2"
- Context: "The printer tray contains plain paper"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r5:claim')]`

### h01-none / b:23f0ec727d584d826bdcd0ad

- Target: "start pump B2"
- Context: "halt compressor Z4"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:claim')]`

### h01-none / b:193b28f0bd367365a5599a0a

- Target: "halt compressor Z4"
- Context: "start pump B2"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:claim')]`

### h02-partial / b:7b3375625c8ccbffb293127c

- Target: "the camera check begins at 14:20"
- Context: "resume the compass test"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:claim')]`

### h02-partial / b:84f81c601af14118383e56d2

- Target: "resume the compass test"
- Context: "because the replacement mount passed inspection"
- Relation: `basis`
- New correct: `[('r1', 'basis', 'r1:basis1')]`
- New wrong: `[]`

### h02-partial / b:aa8464b2bbaf4a566427cce2

- Target: "the camera check begins at 14:20"
- Context: "because the replacement mount passed inspection"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r6', 'condition', 'r1:basis1')]`

### h02-partial / b:6239f025543194605ee52105

- Target: "resume the compass test"
- Context: "the camera check begins at 14:20"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r6:claim'), ('r1', 'condition', 'r6:time1')]`

### h02-partial / b:771116bd41b178b5eb0eac70

- Target: "resume the compass test"
- Context: "because its lens is clean"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:basis1')]`

### h02-none / b:e16f4fb252bdc734a1c6b7ed

- Target: "because its lens is clean"
- Context: "The delivery folder contains a yellow form"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:e16f4fb252bdc734a1c6b7ed', 'basis', 'r2:claim')]`

### h02-none / b:071f2368b2ffbed3310c29ed

- Target: "because its lens is clean"
- Context: "The stock counter remains seven"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:071f2368b2ffbed3310c29ed', 'basis', 'r3:claim')]`

### h02-none / b:8f164668e0db80dfa98380cc

- Target: "because its lens is clean"
- Context: "The break room has two chairs"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:8f164668e0db80dfa98380cc', 'basis', 'r4:claim')]`

### h02-none / b:f503a8d45de3d5514fbb6b0d

- Target: "because its lens is clean"
- Context: "The printer tray contains plain paper"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:f503a8d45de3d5514fbb6b0d', 'basis', 'r5:claim')]`

### h02-none / b:76c1714dc1a8e0757fa49d8a

- Target: "because its lens is clean"
- Context: "resume the compass test"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:76c1714dc1a8e0757fa49d8a', 'basis', 'r1:claim')]`

### h02-none / b:08dea6f5d5546e50a7b58dd8

- Target: "because its lens is clean"
- Context: "Independently, the camera check begins at 14:20"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:08dea6f5d5546e50a7b58dd8', 'basis', 'r6:claim'), ('unbound:b:08dea6f5d5546e50a7b58dd8', 'basis', 'r6:time1')]`

### h02-none / b:8ac63b9218dcddb66edc6fb8

- Target: "resume the compass test"
- Context: "because its lens is clean"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:basis1')]`

### h03-full / b:fcdb8729db447eed104831e9

- Target: "do not publish the terrain map because the licence excludes commercial distribution"
- Context: "The map instruction below concerns commercial reuse"
- Relation: `condition`
- New correct: `[('r1', 'condition', 'r1:condition1')]`
- New wrong: `[]`

### h03-full / b:93a3d8f65fd5a7e040362e1b

- Target: "Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission"
- Context: "The map instruction below concerns commercial reuse"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:condition1')]`

### h03-full / b:1850dab6d82057b5a5c0305f

- Target: "The map instruction below concerns commercial reuse"
- Context: "do not publish the terrain map because the licence excludes commercial distribution"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:1850dab6d82057b5a5c0305f', 'condition', 'r1:basis1'), ('unbound:b:1850dab6d82057b5a5c0305f', 'condition', 'r1:claim')]`

### h03-full / b:9c1825b5930f50d4bbff7d93

- Target: "Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission"
- Context: "do not publish the terrain map because the licence excludes commercial distribution"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:basis1')]`

### h03-full / b:5423f83523c1662c18bfba28

- Target: "The map instruction below concerns commercial reuse"
- Context: "the licence excludes commercial distribution"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:5423f83523c1662c18bfba28', 'condition', 'r1:basis1')]`

### h03-full / b:95d28a5945d8ad1a96113dd7

- Target: "do not publish the terrain map because the licence excludes commercial distribution"
- Context: "the licence excludes commercial distribution"
- Relation: `basis`
- New correct: `[('r1', 'basis', 'r1:basis1')]`
- New wrong: `[]`

### h03-full / b:27a342707cfd8b8210e56622

- Target: "The map instruction below concerns commercial reuse"
- Context: "Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:27a342707cfd8b8210e56622', 'condition', 'r6:condition1')]`

### h03-full / b:8be1743fda357f238b7b0d60

- Target: "do not publish the terrain map because the licence excludes commercial distribution"
- Context: "Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:basis1')]`

### h03-full / b:ba736a9d46bfab59e17f4a69

- Target: "do not publish the terrain map because the licence excludes commercial distribution"
- Context: "for classroom teaching"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:condition1')]`

### h03-full / b:b1070957f8fa99283fbb8876

- Target: "do not publish the terrain map because the licence excludes commercial distribution"
- Context: "the teacher granted permission"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:basis1')]`

### h03-partial / b:77d369f5ffd03bd630fa6442

- Target: "do not publish the terrain map"
- Context: "The map instruction below concerns commercial reuse"
- Relation: `condition`
- New correct: `[('r1', 'condition', 'r1:condition1')]`
- New wrong: `[]`

### h03-partial / b:d3c74ccc83dbbf683eb33d53

- Target: "Separate instruction: for classroom teaching, publish the sketch"
- Context: "The map instruction below concerns commercial reuse"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:condition1')]`

### h03-partial / b:56465509e5b30c9dd14f9429

- Target: "Separate instruction: for classroom teaching, publish the sketch"
- Context: "The delivery folder contains a yellow form"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r2:claim')]`

### h03-partial / b:2ea9892c6d6d208f804e85bb

- Target: "because the teacher granted permission"
- Context: "The delivery folder contains a yellow form"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:2ea9892c6d6d208f804e85bb', 'basis', 'r2:claim')]`

### h03-partial / b:1d7d170f2101b0a59bb36bf3

- Target: "Separate instruction: for classroom teaching, publish the sketch"
- Context: "The stock counter remains seven"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r3:claim')]`

### h03-partial / b:912a0b3422d61d1d80730940

- Target: "because the teacher granted permission"
- Context: "The stock counter remains seven"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:912a0b3422d61d1d80730940', 'basis', 'r3:claim')]`

### h03-partial / b:7eae663161e782d424586198

- Target: "Separate instruction: for classroom teaching, publish the sketch"
- Context: "The break room has two chairs"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r4:claim')]`

### h03-partial / b:5c89444cb8a7519269687cac

- Target: "because the teacher granted permission"
- Context: "The break room has two chairs"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:5c89444cb8a7519269687cac', 'basis', 'r4:claim')]`

### h03-partial / b:a19e4be44fb9162276997228

- Target: "Separate instruction: for classroom teaching, publish the sketch"
- Context: "The printer tray contains plain paper"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r5:claim')]`

### h03-partial / b:e9f252e08fa7b4cf3192661d

- Target: "because the teacher granted permission"
- Context: "The printer tray contains plain paper"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:e9f252e08fa7b4cf3192661d', 'basis', 'r5:claim')]`

### h03-partial / b:edc4f06317073dd3dd808dcc

- Target: "because the teacher granted permission"
- Context: "do not publish the terrain map"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:edc4f06317073dd3dd808dcc', 'basis', 'r1:claim')]`

### h03-partial / b:9a9f9b225971dfa01dd21503

- Target: "do not publish the terrain map"
- Context: "Separate instruction: for classroom teaching, publish the sketch"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:claim'), ('r1', 'basis', 'r6:condition1')]`

### h03-partial / b:a6a911903b10af07131e1f2f

- Target: "do not publish the terrain map"
- Context: "because the teacher granted permission"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:basis1')]`

### h03-partial / b:8643413596b1450da98ae78f

- Target: "Separate instruction: for classroom teaching, publish the sketch"
- Context: "because the teacher granted permission"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r6', 'condition', 'r6:basis1')]`

### h03-none / b:b06e166e118180df5dd72da1

- Target: "for classroom teaching, publish the sketch because the teacher granted permission"
- Context: "The delivery folder contains a yellow form"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r2:claim')]`

### h03-none / b:2682bc5b508380b556abfee8

- Target: "for classroom teaching, publish the sketch because the teacher granted permission"
- Context: "The stock counter remains seven"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r3:claim')]`

### h03-none / b:5ffc05459b90229c6119f3cc

- Target: "for classroom teaching, publish the sketch because the teacher granted permission"
- Context: "The break room has two chairs"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r4:claim')]`

### h03-none / b:5527b84a99fedc1b92319b06

- Target: "do not publish the terrain map"
- Context: "The printer tray contains plain paper"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r5:claim')]`

### h03-none / b:09f176fc1fe78fbb28955b2e

- Target: "for classroom teaching, publish the sketch because the teacher granted permission"
- Context: "do not publish the terrain map"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:claim')]`

### h03-none / b:f57115b6b9c0af0a9a152c0f

- Target: "do not publish the terrain map"
- Context: "for classroom teaching"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:condition1')]`

### h03-none / b:0c6ef64374bdefd67f647a5f

- Target: "do not publish the terrain map"
- Context: "for classroom teaching, publish the sketch because the teacher granted permission"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:basis1')]`

### h03-none / b:c99ee9e58544b2a3dcb27ccb

- Target: "for classroom teaching, publish the sketch because the teacher granted permission"
- Context: "the sketch"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:c99ee9e58544b2a3dcb27ccb', 'basis', 'unmatched:10')]`

### h03-none / b:abb0530c402b3541ac57d20e

- Target: "do not publish the terrain map"
- Context: "the teacher granted permission"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:basis1')]`

### h04-full / b:ba9d8309695e4e31e242fa2c

- Target: "This proposed trial has no deployment approval"
- Context: "we might trial pack G8"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:ba9d8309695e4e31e242fa2c', 'basis', 'r1:claim'), ('unbound:b:ba9d8309695e4e31e242fa2c', 'caveat', 'r1:caveat1')]`

### h04-full / b:91752515d139c33a8e958fc1

- Target: "This proposed trial has no deployment approval"
- Context: "Independently, the warehouse rollout is approved"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:91752515d139c33a8e958fc1', 'basis', 'r6:claim'), ('unbound:b:91752515d139c33a8e958fc1', 'caveat', 'r1:caveat1')]`

### h04-partial / b:dc5cb2b68359703cb31723d4

- Target: "This proposed trial has no deployment approval"
- Context: "The delivery folder contains a yellow form"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:dc5cb2b68359703cb31723d4', 'basis', 'r2:claim'), ('unbound:b:dc5cb2b68359703cb31723d4', 'caveat', 'r1:caveat1')]`

### h04-partial / b:9dccee5ab4ae4d0e96abe7c3

- Target: "This proposed trial has no deployment approval"
- Context: "The stock counter remains seven"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:9dccee5ab4ae4d0e96abe7c3', 'basis', 'r3:claim'), ('unbound:b:9dccee5ab4ae4d0e96abe7c3', 'caveat', 'r1:caveat1')]`

### h04-partial / b:5a61b1ffcbd66456f4234b01

- Target: "This proposed trial has no deployment approval"
- Context: "The printer tray contains plain paper"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:5a61b1ffcbd66456f4234b01', 'basis', 'r5:claim'), ('unbound:b:5a61b1ffcbd66456f4234b01', 'caveat', 'r1:caveat1')]`

### h04-partial / b:8b7f7d877551ea605a15dcfd

- Target: "This proposed trial has no deployment approval"
- Context: "we might trial pack G8"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:8b7f7d877551ea605a15dcfd', 'basis', 'r1:claim'), ('unbound:b:8b7f7d877551ea605a15dcfd', 'caveat', 'r1:caveat1')]`

### h04-partial / b:288d0ac3dcc2dd4100690618

- Target: "we might trial pack G8"
- Context: "This proposed trial has no deployment approval"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r1:caveat1')]`

### h04-partial / b:3c9eee86bab6a3fd9c838efe

- Target: "This proposed trial has no deployment approval"
- Context: "the warehouse rollout is approved"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:3c9eee86bab6a3fd9c838efe', 'basis', 'r6:claim'), ('unbound:b:3c9eee86bab6a3fd9c838efe', 'caveat', 'r1:caveat1')]`

### h04-none / b:77a43f69fba07978e68d801c

- Target: "the warehouse rollout is approved"
- Context: "we might trial pack G8"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:claim')]`

### h04-none / b:888cacf8c00e46800be57228

- Target: "we might trial pack G8"
- Context: "the warehouse rollout is approved"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:claim')]`

### h05-none / b:f20e49210f5a591ef3b5c5a7

- Target: "the noise audit starts at 16:40 on rig B7"
- Context: "the pressure audit ended"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r6', 'condition', 'r1:claim')]`

### h05-none / b:8c114cb293abd6fa475b7d5c

- Target: "the pressure audit ended"
- Context: "the noise audit starts at 16:40 on rig B7"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:claim'), ('r1', 'basis', 'r6:condition1'), ('r1', 'basis', 'r6:time1')]`

### h06-full / b:778b2941283fb58a8d779ece

- Target: "I suspect coil N8 may handle 18 amperes"
- Context: "The coil estimate concerns operation in nitrogen"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:condition1')]`

### h06-full / b:facb8ffb2421823e186889de

- Target: "This capacity is conjectural and has not been measured"
- Context: "The coil estimate concerns operation in nitrogen"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:facb8ffb2421823e186889de', 'caveat', 'r1:caveat1'), ('unbound:b:facb8ffb2421823e186889de', 'condition', 'r1:condition1')]`

### h06-full / b:f7c23f65bb2564637d80728e

- Target: "I suspect coil N8 may handle 18 amperes"
- Context: "The stock counter remains seven"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r3:claim')]`

### h06-full / b:4c152732dcdf5c9a53744c06

- Target: "This capacity is conjectural and has not been measured"
- Context: "I suspect coil N8 may handle 18 amperes"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:4c152732dcdf5c9a53744c06', 'basis', 'r1:claim'), ('unbound:b:4c152732dcdf5c9a53744c06', 'caveat', 'r1:caveat1')]`

### h06-full / b:9ef06345e48b3da9d322785a

- Target: "I suspect coil N8 may handle 18 amperes"
- Context: "This capacity is conjectural and has not been measured"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:caveat1')]`

### h06-full / b:e07fc7d1e27b1cadd41ae8d0

- Target: "I suspect coil N8 may handle 18 amperes"
- Context: "A separate steel cable was measured at 12 amperes in air"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:claim'), ('r1', 'basis', 'r6:condition1')]`

### h06-full / b:57416fd17aa978ead4f222fd

- Target: "This capacity is conjectural and has not been measured"
- Context: "A separate steel cable was measured at 12 amperes in air"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:57416fd17aa978ead4f222fd', 'basis', 'r6:claim'), ('unbound:b:57416fd17aa978ead4f222fd', 'basis', 'r6:condition1'), ('unbound:b:57416fd17aa978ead4f222fd', 'caveat', 'r1:caveat1')]`

### h06-partial / b:ea60e3561e7f085180aca4f6

- Target: "This capacity is conjectural and has not been measured"
- Context: "The delivery folder contains a yellow form"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:ea60e3561e7f085180aca4f6', 'basis', 'r2:claim'), ('unbound:b:ea60e3561e7f085180aca4f6', 'caveat', 'r1:caveat1')]`

### h06-partial / b:8f1a935bd12fc8f662f17c9a

- Target: "This capacity is conjectural and has not been measured"
- Context: "The stock counter remains seven"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:8f1a935bd12fc8f662f17c9a', 'basis', 'r3:claim'), ('unbound:b:8f1a935bd12fc8f662f17c9a', 'caveat', 'r1:caveat1')]`

### h06-partial / b:6d8735c9fb9778648432e505

- Target: "This capacity is conjectural and has not been measured"
- Context: "I suspect coil N8 may handle 18 amperes"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:6d8735c9fb9778648432e505', 'basis', 'r1:claim'), ('unbound:b:6d8735c9fb9778648432e505', 'caveat', 'r1:caveat1')]`

### h06-partial / b:5355022546c7bfc01840d094

- Target: "A separate steel cable was measured at 12 amperes in air"
- Context: "I suspect coil N8 may handle 18 amperes"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r6', 'condition', 'r1:claim')]`

### h06-partial / b:6d18c00fe041ced56423b30b

- Target: "I suspect coil N8 may handle 18 amperes"
- Context: "This capacity is conjectural and has not been measured"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:caveat1')]`

### h06-partial / b:7e95c8aebb51e22a3826709c

- Target: "I suspect coil N8 may handle 18 amperes"
- Context: "A separate steel cable was measured at 12 amperes in air"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:claim'), ('r1', 'basis', 'r6:condition1')]`

### h06-none / b:bb0df72bb011ae61329d532e

- Target: "A separate steel cable was measured at 12 amperes in air"
- Context: "I suspect coil N8 may handle 18 amperes"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r6', 'basis', 'r1:claim')]`

### h06-none / b:09b7dd26a8538453c88c1aca

- Target: "I suspect coil N8 may handle 18 amperes"
- Context: "A separate steel cable was measured at 12 amperes in air"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r6:claim'), ('r1', 'basis', 'r6:condition1')]`

### n02 / b:5e57d17349c7bac4e45bbcfd

- Target: "your medication check-in module and family member invitation interface are due today"
- Context: "Today is Thursday"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r2:time1'), ('r2', 'basis', 'r2:time2')]`

### n02 / b:14946656d9b99861efe774b0

- Target: "Please make sure to complete the delivery today"
- Context: "Today is Thursday"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r3:time1'), ('r3', 'basis', 'r3:time2')]`

### n02 / b:28cb57f2df3c94f369bf168d

- Target: "your medication check-in module and family member invitation interface are due today"
- Context: "your medication check-in module and family member invitation interface"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r2', 'condition', 'r3:subject1')]`

### n02 / b:dd8e9868c1b5f1f03bb4e538

- Target: "Please make sure to complete the delivery today"
- Context: "your medication check-in module and family member invitation interface"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r3:subject1')]`

### n02 / b:e11ce8f0b2c7c57988e97419

- Target: "Please make sure to complete the delivery today"
- Context: "your medication check-in module and family member invitation interface are due today"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r3', 'condition', 'r3:subject1'), ('r3', 'condition', 'r3:time1')]`

### n02 / b:026cbd08f75c876780c147d7

- Target: "your medication check-in module and family member invitation interface are due today"
- Context: "Please make sure to complete the delivery today"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r2', 'condition', 'r2:time1')]`

### n02 / b:46a62a0e3958e5ccda5e4779

- Target: "your medication check-in module and family member invitation interface are due today"
- Context: "Other colleagues, please also share your plans and progress for today"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r2', 'condition', 'r2:time1')]`

### n02 / b:46c31f664f3fc857e4763d4e

- Target: "Please make sure to complete the delivery today"
- Context: "Other colleagues, please also share your plans and progress for today"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r3:time1')]`

### n03 / b:5c937e4719b964e4082186e0

- Target: "today I'm starting a new design task"
- Context: "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:5c937e4719b964e4082186e0', 'basis', 'r2:basis1')]`

### n03 / b:4f71cbda2a852b2202c8eed7

- Target: "I will focus on comparing Azure Blob and AWS S3"
- Context: "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future"
- Relation: `basis`
- New correct: `[('r2', 'basis', 'r2:basis1')]`
- New wrong: `[]`

### n03 / b:cf228fa5cbfdd5f007b4ec07

- Target: "The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack"
- Context: "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r2:basis1')]`

### n03 / b:c73ab93c8710721c49c8d69e

- Target: "A preliminary selection recommendation report will be provided early next week"
- Context: "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r2:basis1')]`

### n03 / b:56bc8322758ed9075a39b536

- Target: "today I'm starting a new design task"
- Context: "I will focus on comparing Azure Blob and AWS S3"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:56bc8322758ed9075a39b536', 'basis', 'r2:claim')]`

### n03 / b:df0646327c7ef120f53c53ee

- Target: "The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack"
- Context: "I will focus on comparing Azure Blob and AWS S3"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r2:claim')]`

### n03 / b:94144ae3e5cff4b67c8b9a18

- Target: "A preliminary selection recommendation report will be provided early next week"
- Context: "I will focus on comparing Azure Blob and AWS S3"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r2:claim')]`

### n03 / b:399965f07d18bc18ab96d4d9

- Target: "today I'm starting a new design task"
- Context: "The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:399965f07d18bc18ab96d4d9', 'basis', 'r3:claim')]`

### n03 / b:ee0875bc32b43b94927b20d4

- Target: "I will focus on comparing Azure Blob and AWS S3"
- Context: "The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r3:claim')]`

### n04 / b:3bb0ed2d957e8696202aa9d1

- Target: "I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday"
- Context: "Good morning everyone"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:3bb0ed2d957e8696202aa9d1', 'basis', 'unmatched:9')]`

### n04 / b:ba6e658933acba2ab8070083

- Target: "From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage"
- Context: "Good morning everyone"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:ba6e658933acba2ab8070083', 'basis', 'unmatched:9')]`

### n04 / b:c06f513140fcb1380352633d

- Target: "our other projects are also on AWS"
- Context: "Good morning everyone"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:c06f513140fcb1380352633d', 'basis', 'unmatched:9')]`

### n04 / b:af176a5e2bcba8de1a5efaf5

- Target: "Today, I will start designing the Bucket Policy and directory structure based on S3"
- Context: "Good morning everyone"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:af176a5e2bcba8de1a5efaf5', 'condition', 'unmatched:9')]`

### n04 / b:0324e33957545d2679d3a815

- Target: "for example, isolating by tenant and file type"
- Context: "Good morning everyone"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:0324e33957545d2679d3a815', 'basis', 'unmatched:9'), ('unbound:b:0324e33957545d2679d3a815', 'method', 'r4:method1')]`

### n04 / b:3cda4c969034a645d51015ea

- Target: "From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage"
- Context: "I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r1:claim'), ('r2', 'basis', 'r1:time1')]`

### n04 / b:6a54685e4941c4d9c6f591aa

- Target: "Today, I will start designing the Bucket Policy and directory structure based on S3"
- Context: "I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r4', 'condition', 'r1:claim'), ('r4', 'condition', 'r1:time1')]`

### n04 / b:d44c6a985f2584eee06e912e

- Target: "I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday"
- Context: "last Friday"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:time1')]`

### n04 / b:86fc8a637aaa1190f52e8f76

- Target: "Today, I will start designing the Bucket Policy and directory structure based on S3"
- Context: "last Friday"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r4', 'condition', 'r1:time1')]`

### n04 / b:c90141277e23174fcd03926d

- Target: "Today, I will start designing the Bucket Policy and directory structure based on S3"
- Context: "From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[]`

### n04 / b:396caa4aa29bc1a5d2d90244

- Target: "From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage"
- Context: "our other projects are also on AWS"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r4:optional_basis2')]`

### n04 / b:3f2563b45b89b30346fda2b6

- Target: "Today, I will start designing the Bucket Policy and directory structure based on S3"
- Context: "our other projects are also on AWS"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r4', 'condition', 'r4:optional_basis2')]`

### n04 / b:debf37c3287c91429c83ce8f

- Target: "Today, I will start designing the Bucket Policy and directory structure based on S3"
- Context: "Today"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r4:time1')]`

### n04 / b:c56de73dd5a001a01c612e79

- Target: "From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage"
- Context: "Today, I will start designing the Bucket Policy and directory structure based on S3"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r4:claim'), ('r2', 'basis', 'r4:time1')]`

### n04 / b:f3ccc13e884dabf8750bb888

- Target: "for example, isolating by tenant and file type"
- Context: "Today, I will start designing the Bucket Policy and directory structure based on S3"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:f3ccc13e884dabf8750bb888', 'condition', 'r4:claim'), ('unbound:b:f3ccc13e884dabf8750bb888', 'condition', 'r4:time1'), ('unbound:b:f3ccc13e884dabf8750bb888', 'method', 'r4:method1')]`

### n04 / b:04711eec0dd81d8518204cf2

- Target: "Today, I will start designing the Bucket Policy and directory structure based on S3"
- Context: "for example, isolating by tenant and file type"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r4:method1')]`

### n05 / b:8a20d5723b4182e761826069

- Target: "the complete technical design document (based on AWS S3) has been uploaded to Confluence"
- Context: "Good morning everyone"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:8a20d5723b4182e761826069', 'basis', 'unmatched:9')]`

### n05 / b:c9fa812e008feb05076df4fd

- Target: "It includes three main parts"
- Context: "Good morning everyone"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:c9fa812e008feb05076df4fd', 'basis', 'unmatched:9')]`

### n05 / b:b1c4d1d6cd8ddff3fd3fb824

- Target: "bucket permission policies"
- Context: "Good morning everyone"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:b1c4d1d6cd8ddff3fd3fb824', 'basis', 'unmatched:9')]`

### n05 / b:32c5d7c053b5d0e76daf76a1

- Target: "lifecycle rules"
- Context: "Good morning everyone"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:32c5d7c053b5d0e76daf76a1', 'basis', 'unmatched:9')]`

### n05 / b:596a78e961cd49dfecb142ff

- Target: "recommended directory structure"
- Context: "Good morning everyone"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:596a78e961cd49dfecb142ff', 'basis', 'unmatched:9')]`

### n05 / b:e02550d31567f95647b6f9e3

- Target: "the complete technical design document (based on AWS S3) has been uploaded to Confluence"
- Context: "regarding the file storage solution"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:e02550d31567f95647b6f9e3', 'basis', 'unmatched:9')]`

### n05 / b:20fc7c23f476af6fd7e89bc4

- Target: "It includes three main parts"
- Context: "regarding the file storage solution"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:20fc7c23f476af6fd7e89bc4', 'basis', 'unmatched:9')]`

### n05 / b:00a3f22f7d19bf53fd6b7b90

- Target: "@Mingzhi Li Boss Li, please review it"
- Context: "regarding the file storage solution"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:00a3f22f7d19bf53fd6b7b90', 'condition', 'unmatched:9')]`

### n05 / b:bb05ad584f29be70aa01e3da

- Target: "It includes three main parts"
- Context: "the complete technical design document (based on AWS S3) has been uploaded to Confluence"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:bb05ad584f29be70aa01e3da', 'basis', 'r1:claim'), ('unbound:b:bb05ad584f29be70aa01e3da', 'basis', 'r2:subject1')]`

### n05 / b:77e5d7bb423ce13b72157436

- Target: "the complete technical design document (based on AWS S3) has been uploaded to Confluence"
- Context: "It includes three main parts"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:77e5d7bb423ce13b72157436', 'basis', 'unmatched:9')]`

### n05 / b:d4cce1921f2d1109a4403b00

- Target: "bucket permission policies"
- Context: "It includes three main parts"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:d4cce1921f2d1109a4403b00', 'condition', 'unmatched:9')]`

### n05 / b:aa68e4bb81885981be491a6a

- Target: "lifecycle rules"
- Context: "It includes three main parts"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:aa68e4bb81885981be491a6a', 'condition', 'unmatched:9')]`

### n05 / b:d700a0da7460aab013c4eeb4

- Target: "recommended directory structure"
- Context: "It includes three main parts"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:d700a0da7460aab013c4eeb4', 'condition', 'unmatched:9')]`

### n05 / b:21f0186aafa1c7df785826b4

- Target: "lifecycle rules"
- Context: "bucket permission policies"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:21f0186aafa1c7df785826b4', 'condition', 'unmatched:9')]`

### n05 / b:010ebd4406ff03a2628e758a

- Target: "bucket permission policies"
- Context: "lifecycle rules"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:010ebd4406ff03a2628e758a', 'condition', 'unmatched:9')]`

### n05 / b:f4eed8ff8353e8a4ce787a2a

- Target: "@Mingzhi Li Boss Li, please review it"
- Context: "recommended directory structure"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:f4eed8ff8353e8a4ce787a2a', 'basis', 'unmatched:9')]`

### n05 / b:c18205e8d0e0342a0e6166c7

- Target: "the complete technical design document (based on AWS S3) has been uploaded to Confluence"
- Context: "@Mingzhi Li Boss Li, please review it"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r3:claim'), ('r1', 'basis', 'r3:recipient1')]`

### n06 / b:046b8605007665fe33f9406d

- Target: "The design is very comprehensive"
- Context: "@Lujian Gao I've finished reviewing the document on the file storage solution"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r1:claim'), ('r2', 'basis', 'r3:subject1')]`

### n06 / b:8e675cc95dd5c6877947887b

- Target: "especially the considerations for tenant data isolation and cost optimization"
- Context: "@Lujian Gao I've finished reviewing the document on the file storage solution"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:8e675cc95dd5c6877947887b', 'basis', 'r1:claim'), ('unbound:b:8e675cc95dd5c6877947887b', 'basis', 'r3:subject1'), ('unbound:b:8e675cc95dd5c6877947887b', 'caveat', 'r2:caveat1')]`

### n06 / b:8428ffa63fdc889c60a5a2f3

- Target: "can be finalized"
- Context: "@Lujian Gao I've finished reviewing the document on the file storage solution"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:8428ffa63fdc889c60a5a2f3', 'condition', 'r1:claim'), ('unbound:b:8428ffa63fdc889c60a5a2f3', 'condition', 'r3:subject1')]`

### n06 / b:d1fba9ed900f735d769ab785

- Target: "especially the considerations for tenant data isolation and cost optimization"
- Context: "The design is very comprehensive"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:d1fba9ed900f735d769ab785', 'basis', 'r2:claim'), ('unbound:b:d1fba9ed900f735d769ab785', 'caveat', 'r2:caveat1')]`

### n06 / b:04a93ce41613b29956aef66e

- Target: "The design is very comprehensive"
- Context: "especially the considerations for tenant data isolation and cost optimization"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r2:caveat1')]`

### n06 / b:9d5b0a0626a5111358cd13cc

- Target: "can be finalized"
- Context: "The proposal is approved"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:9d5b0a0626a5111358cd13cc', 'basis', 'unmatched:6')]`

### n06 / b:bb199a93cce99a13a7f24fb0

- Target: "The proposal is approved"
- Context: "can be finalized"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:bb199a93cce99a13a7f24fb0', 'basis', 'unmatched:6')]`

### n08 / b:dd3b3d26f4a5290c55e9d18d

- Target: "The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction"
- Context: "Email received"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:dd3b3d26f4a5290c55e9d18d', 'basis', 'unmatched:5')]`

### n08 / b:2b67a218249aefab240dc5c1

- Target: "@Xinjie Li @Xuexin Yin, please assess the scope of impact on the backend"
- Context: "The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r1:claim'), ('r2', 'basis', 'r1:condition1')]`

### n08 / b:ac1cef1b18f0fa69529cc533

- Target: "The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction"
- Context: "all accounts marked as `ACCOUNT_STATUS_LOCKED`"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:condition1')]`

### n08 / b:b91e2cca7dee2173b625e34d

- Target: "The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction"
- Context: "@Xinjie Li @Xuexin Yin, please assess the scope of impact on the backend"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r2:claim'), ('r1', 'basis', 'r2:recipient1')]`

### n09 / b:76b8ba5f5742a424669524c0

- Target: "defined as 'Explicit Status Alert Policy'"
- Context: "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:76b8ba5f5742a424669524c0', 'basis', 'r1:claim'), ('unbound:b:76b8ba5f5742a424669524c0', 'basis', 'r2:subject1'), ('unbound:b:76b8ba5f5742a424669524c0', 'caveat', 'r1:caveat1')]`

### n09 / b:feb88b46e27b5f8da15c9550

- Target: "It is mainly used for scenarios where an account is locked"
- Context: "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:feb88b46e27b5f8da15c9550', 'condition', 'r1:claim'), ('unbound:b:feb88b46e27b5f8da15c9550', 'condition', 'r2:subject1')]`

### n09 / b:bbd0dad3a5339bd1b12d2dcd

- Target: "requiring explicit interruption of user operations"
- Context: "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:bbd0dad3a5339bd1b12d2dcd', 'condition', 'r1:claim'), ('unbound:b:bbd0dad3a5339bd1b12d2dcd', 'condition', 'r2:subject1')]`

### n09 / b:baaf010e9434beadbbaebab6

- Target: "and guidance to manual channels"
- Context: "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:baaf010e9434beadbbaebab6', 'condition', 'r1:claim'), ('unbound:b:baaf010e9434beadbbaebab6', 'condition', 'r2:subject1')]`

### n09 / b:5dea53231e81934f1585c3d8

- Target: "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`"
- Context: "defined as 'Explicit Status Alert Policy'"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r1:caveat1')]`

### n09 / b:a9ea35c30ee25734f754dee2

- Target: "It is mainly used for scenarios where an account is locked"
- Context: "defined as 'Explicit Status Alert Policy'"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:a9ea35c30ee25734f754dee2', 'basis', 'r1:caveat1')]`

### n09 / b:1dc4aea0c7c081c6e39aae50

- Target: "requiring explicit interruption of user operations"
- Context: "defined as 'Explicit Status Alert Policy'"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:1dc4aea0c7c081c6e39aae50', 'basis', 'r1:caveat1')]`

### n09 / b:74c3ddfa11ead9f1b245b9e8

- Target: "and guidance to manual channels"
- Context: "defined as 'Explicit Status Alert Policy'"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:74c3ddfa11ead9f1b245b9e8', 'basis', 'r1:caveat1')]`

### n09 / b:3fef4ba85542d9dec50a1419

- Target: "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`"
- Context: "It is mainly used for scenarios where an account is locked"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r2:condition1')]`

### n09 / b:a3203dd3abcecb12f2a7865e

- Target: "defined as 'Explicit Status Alert Policy'"
- Context: "It is mainly used for scenarios where an account is locked"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:a3203dd3abcecb12f2a7865e', 'basis', 'r2:condition1'), ('unbound:b:a3203dd3abcecb12f2a7865e', 'caveat', 'r1:caveat1')]`

### n09 / b:cd5699b7cb78cafd8acd4930

- Target: "requiring explicit interruption of user operations"
- Context: "It is mainly used for scenarios where an account is locked"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:cd5699b7cb78cafd8acd4930', 'condition', 'r2:condition1')]`

### n09 / b:61f31cda56a756c9b9baab76

- Target: "and guidance to manual channels"
- Context: "It is mainly used for scenarios where an account is locked"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:61f31cda56a756c9b9baab76', 'condition', 'r2:condition1')]`

### n09 / b:5e8578bb135f945386d9999d

- Target: "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`"
- Context: "requiring explicit interruption of user operations"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:5e8578bb135f945386d9999d', 'basis', 'unmatched:6')]`

### n09 / b:7c169c800c7c441753149bc5

- Target: "defined as 'Explicit Status Alert Policy'"
- Context: "requiring explicit interruption of user operations"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:7c169c800c7c441753149bc5', 'basis', 'unmatched:6'), ('unbound:b:7c169c800c7c441753149bc5', 'caveat', 'r1:caveat1')]`

### n09 / b:3b25a781eb8b20a209a7c0f9

- Target: "It is mainly used for scenarios where an account is locked"
- Context: "requiring explicit interruption of user operations"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:3b25a781eb8b20a209a7c0f9', 'condition', 'unmatched:6')]`

### n09 / b:955cd527a1cae018d71d8b01

- Target: "It is mainly used for scenarios where an account is locked"
- Context: "and guidance to manual channels"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:955cd527a1cae018d71d8b01', 'condition', 'unmatched:6')]`

### n09 / b:9c557737fcf05db0e9172f80

- Target: "requiring explicit interruption of user operations"
- Context: "and guidance to manual channels"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:9c557737fcf05db0e9172f80', 'basis', 'unmatched:6')]`

### n10 / b:72a6f3d5ccd0326859dccb03

- Target: "after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted"
- Context: "Received"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:72a6f3d5ccd0326859dccb03', 'basis', 'unmatched:7')]`

### n10 / b:fa20c04791a3875ba76a73db

- Target: "This strategy will be handled by `ExplicitStateAlertModule`"
- Context: "I've reviewed the document"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r1:claim')]`

### n10 / b:abea2124ec7ca5e8bc9e918f

- Target: "the parameter `halt_downstream_triggers` is set to `true`"
- Context: "I've reviewed the document"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r1:claim')]`

### n10 / b:4539b55dcf7d002ade6edc4b

- Target: "after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted"
- Context: "I've reviewed the document"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r4', 'condition', 'r1:claim')]`

### n10 / b:49308f7ad17e4d8b89c4468d

- Target: "the parameter `halt_downstream_triggers` is set to `true`"
- Context: "This strategy will be handled by `ExplicitStateAlertModule`"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r2:claim')]`

### n10 / b:5ec78761d650343a96fe47aa

- Target: "after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted"
- Context: "This strategy will be handled by `ExplicitStateAlertModule`"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r4', 'condition', 'r2:claim')]`

### n10 / b:a4a6355090ffdb9e52682c92

- Target: "This strategy will be handled by `ExplicitStateAlertModule`"
- Context: "the parameter `halt_downstream_triggers` is set to `true`"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r3:claim')]`

### n10 / b:7f343ababa9a76c56eea3c9b

- Target: "after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted"
- Context: "the parameter `halt_downstream_triggers` is set to `true`"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r4', 'condition', 'r3:claim')]`

### n10 / b:353015452ac5b95988cbdc66

- Target: "the parameter `halt_downstream_triggers` is set to `true`"
- Context: "after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r4:claim'), ('r3', 'basis', 'r4:condition1')]`

### n10 / b:f615fed4a5152f21ca2d7a7e

- Target: "after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted"
- Context: "right?"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r4:caveat1')]`

### n11 / b:4d21e9a6c050af15dfef0211

- Target: "This is to avoid sending users redundant or potentially confusing automated messages"
- Context: "your understanding is completely correct"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r1:claim')]`

### n11 / b:f69cdbfa234eeb7aaba8ff6b

- Target: "your understanding is completely correct"
- Context: "This is to avoid sending users redundant or potentially confusing automated messages"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r2:claim')]`

### n12 / b:cf20083a8cf7397b71b95267

- Target: "The data structure looks very clear"
- Context: "Received, thanks a lot!"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:cf20083a8cf7397b71b95267', 'basis', 'unmatched:10')]`

### n12 / b:8204657baf35afed020e8d60

- Target: "to ensure the charts render correctly"
- Context: "Received, thanks a lot!"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:8204657baf35afed020e8d60', 'condition', 'unmatched:10')]`

### n12 / b:a33326ca789e7dc20069847f

- Target: "to ensure the charts render correctly"
- Context: "The data structure looks very clear"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:a33326ca789e7dc20069847f', 'basis', 'r1:claim')]`

### n12 / b:a75454759dc6df1feffff8c3

- Target: "to ensure the charts render correctly"
- Context: "I plan to complete the static data integration this morning"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:a75454759dc6df1feffff8c3', 'condition', 'r2:claim'), ('unbound:b:a75454759dc6df1feffff8c3', 'condition', 'r2:time1')]`

### n12 / b:0d68d0bcd3ea209b4ff6258e

- Target: "initially considering WebSocket if the backend supports it"
- Context: "I plan to complete the static data integration this morning"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r2:claim'), ('r4', 'basis', 'r2:time1')]`

### n12 / b:f38e034629cf9044aa46b723

- Target: "I plan to complete the static data integration this morning"
- Context: "this morning"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r2', 'condition', 'r2:time1')]`

### n12 / b:08c5b4d600a29af380f798a1

- Target: "to ensure the charts render correctly"
- Context: "this morning"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:08c5b4d600a29af380f798a1', 'basis', 'r2:time1')]`

### n12 / b:15c88006a7e01e55858d7160

- Target: "I plan to complete the static data integration this morning"
- Context: "to ensure the charts render correctly"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r2', 'condition', 'r2:basis1')]`

### n12 / b:6d77a97aa1c5a86ebf817c9b

- Target: "In the afternoon, I'll start researching dynamic refresh solutions"
- Context: "to ensure the charts render correctly"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r2:basis1')]`

### n12 / b:12c6ae3564e924a9c0882a85

- Target: "initially considering WebSocket if the backend supports it"
- Context: "to ensure the charts render correctly"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r2:basis1')]`

### n12 / b:689419a5432f65489fa38568

- Target: "to ensure the charts render correctly"
- Context: "In the afternoon"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:689419a5432f65489fa38568', 'basis', 'r3:time1')]`

### n12 / b:7ad5da77fd9a7f160840b748

- Target: "In the afternoon, I'll start researching dynamic refresh solutions"
- Context: "In the afternoon"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r3', 'condition', 'r3:time1')]`

### n12 / b:6fad0ad7b94e19ff70ed3245

- Target: "initially considering WebSocket if the backend supports it"
- Context: "In the afternoon"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r3:time1')]`

### n12 / b:2c8e2bc84d2c59473065848c

- Target: "to ensure the charts render correctly"
- Context: "In the afternoon, I'll start researching dynamic refresh solutions"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:2c8e2bc84d2c59473065848c', 'basis', 'r3:claim'), ('unbound:b:2c8e2bc84d2c59473065848c', 'basis', 'r3:time1')]`

### n12 / b:59fe848224b9c091185bb8db

- Target: "to ensure the charts render correctly"
- Context: "initially considering WebSocket if the backend supports it"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:59fe848224b9c091185bb8db', 'basis', 'r4:claim'), ('unbound:b:59fe848224b9c091185bb8db', 'basis', 'r4:condition1')]`

### n12 / b:68a3d806c268eb75e19369c1

- Target: "to ensure the charts render correctly"
- Context: "the backend"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:68a3d806c268eb75e19369c1', 'basis', 'unmatched:10')]`

### n12 / b:bdc54a3093ba4b4a0483c227

- Target: "initially considering WebSocket if the backend supports it"
- Context: "the backend"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:bdc54a3093ba4b4a0483c227', 'condition', 'unmatched:10')]`

### n13 / b:e63baad659bee0ff0d1111f7

- Target: "WebSocket is the best solution"
- Context: "Great plan"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:e63baad659bee0ff0d1111f7', 'basis', 'unmatched:9')]`

### n13 / b:38a4433fe67ba9177f226eba

- Target: "This task can be implemented using polling for now"
- Context: "Great plan"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:38a4433fe67ba9177f226eba', 'condition', 'unmatched:9')]`

### n13 / b:92c95fa83bd115d1872336a7

- Target: "we can upgrade it uniformly"
- Context: "Great plan"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:92c95fa83bd115d1872336a7', 'basis', 'unmatched:9')]`

### n13 / b:cb806e59b1be340fafda1b25

- Target: "This way, we can avoid blocking your current task"
- Context: "Great plan"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:cb806e59b1be340fafda1b25', 'basis', 'unmatched:9')]`

### n13 / b:39adc05a5348dcb08e46a716

- Target: "This task can be implemented using polling for now"
- Context: "WebSocket is the best solution"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r1:claim')]`

### n13 / b:33c757ea75985c04ae740ad3

- Target: "Once the WebSocket service is stable later"
- Context: "WebSocket is the best solution"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:33c757ea75985c04ae740ad3', 'condition', 'r1:claim')]`

### n13 / b:dd728ebd5ad9db4ed81c9be2

- Target: "we can upgrade it uniformly"
- Context: "WebSocket is the best solution"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r1:claim')]`

### n13 / b:e0357292fd688f72f96d9cfd

- Target: "This way, we can avoid blocking your current task"
- Context: "WebSocket is the best solution"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:e0357292fd688f72f96d9cfd', 'basis', 'r1:claim')]`

### n13 / b:3a44d37f93fb858f9dacdeed

- Target: "This task can be implemented using polling for now"
- Context: "our message push service isn't fully ready yet"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[]`

### n13 / b:feca7ac5bd4b1753b9b61a5a

- Target: "we can upgrade it uniformly"
- Context: "our message push service isn't fully ready yet"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r3:optional_basis1')]`

### n13 / b:13b61c93542c25c7d5b3dce9

- Target: "This way, we can avoid blocking your current task"
- Context: "our message push service isn't fully ready yet"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:13b61c93542c25c7d5b3dce9', 'basis', 'r3:optional_basis1')]`

### n13 / b:834b26fe86fa1568c98c3924

- Target: "WebSocket is the best solution"
- Context: "This task can be implemented using polling for now"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r1', 'basis', 'r3:claim'), ('r1', 'basis', 'r3:time1')]`

### n13 / b:941855695d631f54e8f59439

- Target: "Once the WebSocket service is stable later"
- Context: "This task can be implemented using polling for now"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:941855695d631f54e8f59439', 'condition', 'r3:claim'), ('unbound:b:941855695d631f54e8f59439', 'condition', 'r3:time1')]`

### n13 / b:fe0b8990fe111bcf72c3d3d2

- Target: "we can upgrade it uniformly"
- Context: "This task can be implemented using polling for now"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r3:claim'), ('r4', 'basis', 'r3:time1')]`

### n13 / b:80e1a5a7e5626e05799921a7

- Target: "This way, we can avoid blocking your current task"
- Context: "This task can be implemented using polling for now"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:80e1a5a7e5626e05799921a7', 'basis', 'r3:claim'), ('unbound:b:80e1a5a7e5626e05799921a7', 'basis', 'r3:time1')]`

### n13 / b:4fd06f54b27cdccc42a258e9

- Target: "This task can be implemented using polling for now"
- Context: "by requesting the interface every 10 seconds"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r3:method1')]`

### n13 / b:e4704dc19a65efbc5f6c6041

- Target: "Once the WebSocket service is stable later"
- Context: "by requesting the interface every 10 seconds"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:e4704dc19a65efbc5f6c6041', 'condition', 'r3:method1')]`

### n13 / b:471f6a963f3eb8d070c15f1b

- Target: "This way, we can avoid blocking your current task"
- Context: "by requesting the interface every 10 seconds"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:471f6a963f3eb8d070c15f1b', 'basis', 'r3:method1')]`

### n13 / b:f2d9c1fc19fafcee6cab214a

- Target: "WebSocket is the best solution"
- Context: "Once the WebSocket service is stable later"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r4:condition1')]`

### n13 / b:4caa122579f59a8107fc91d7

- Target: "This task can be implemented using polling for now"
- Context: "Once the WebSocket service is stable later"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r3', 'basis', 'r4:condition1'), ('r3', 'basis', 'r4:time1')]`

### n13 / b:1e9ead33b752f02d0c6c1e33

- Target: "This way, we can avoid blocking your current task"
- Context: "Once the WebSocket service is stable later"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:1e9ead33b752f02d0c6c1e33', 'basis', 'r4:condition1'), ('unbound:b:1e9ead33b752f02d0c6c1e33', 'basis', 'r4:time1')]`

### n13 / b:80c56f2b71671c8d22027887

- Target: "Once the WebSocket service is stable later"
- Context: "we can upgrade it uniformly"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:80c56f2b71671c8d22027887', 'condition', 'r4:claim')]`

### n13 / b:10a03cf0ffe4f5e5ce59c731

- Target: "This way, we can avoid blocking your current task"
- Context: "we can upgrade it uniformly"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:10a03cf0ffe4f5e5ce59c731', 'basis', 'r4:claim')]`

### n13 / b:22904cc3fbefc6be96cf3b72

- Target: "This task can be implemented using polling for now"
- Context: "This way, we can avoid blocking your current task"
- Relation: `basis`
- New correct: `[('r3', 'basis', 'r3:basis1')]`
- New wrong: `[]`

### n13 / b:49d333ee7947ae1bf101ffbb

- Target: "Once the WebSocket service is stable later"
- Context: "This way, we can avoid blocking your current task"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('unbound:b:49d333ee7947ae1bf101ffbb', 'condition', 'r3:basis1')]`

### n13 / b:f3b5fd8c711745fc603cd8a2

- Target: "we can upgrade it uniformly"
- Context: "This way, we can avoid blocking your current task"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r4', 'basis', 'r3:basis1')]`

### n14 / b:134659b5856559884e182a81

- Target: "I'll use the polling solution for now"
- Context: "Okay, Boss Li, understood"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:134659b5856559884e182a81', 'basis', 'unmatched:4')]`

### n14 / b:dab6e274fd7100020bc03d50

- Target: "I'll adjust the plan"
- Context: "Okay, Boss Li, understood"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('unbound:b:dab6e274fd7100020bc03d50', 'basis', 'unmatched:4')]`

### n14 / b:77cc4c82a60ccf1eb120732b

- Target: "I'll adjust the plan"
- Context: "I'll use the polling solution for now"
- Relation: `basis`
- New correct: `[]`
- New wrong: `[('r2', 'basis', 'r1:claim'), ('r2', 'basis', 'r1:time1')]`

### n14 / b:6dd9aafbb7090328c0f898c5

- Target: "I'll use the polling solution for now"
- Context: "I'll adjust the plan"
- Relation: `condition`
- New correct: `[]`
- New wrong: `[('r1', 'condition', 'r2:claim')]`

