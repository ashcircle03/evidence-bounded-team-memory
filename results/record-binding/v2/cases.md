# 사례별 고정 평가와 원출력

각 셀은 올바른 연결/잘못된 연결이다. 동일 사례의 원래 정답 내용·연결·태도 손실은 모든 후보에서0이었다. 완전한 문서의 보존은 별도로 평가한다.

| ID | 기준선 | 8B | 14B | 8B+계약 | 14B+계약 |
|---|---:|---:|---:|---:|---:|
|e01-full|2/0|2/0|2/0|2/0|2/0|
|e01-partial|1/0|1/0|1/0|1/0|1/0|
|e01-none|0/0|0/0|0/0|0/0|0/0|
|e02-full|1/1|1/3|2/2|1/1|2/2|
|e02-partial|0/1|0/2|0/1|0/1|0/1|
|e02-none|0/0|0/0|0/0|0/0|0/0|
|e03-full|2/0|2/0|2/0|2/0|2/0|
|e03-partial|1/0|1/0|1/0|1/0|1/0|
|e03-none|0/0|0/0|0/0|0/0|0/0|
|e04-full|2/0|2/1|2/1|2/1|2/1|
|e04-partial|1/0|1/2|1/1|1/0|1/1|
|e04-none|0/0|0/0|0/0|0/0|0/0|
|e05-full|1/0|1/0|1/0|1/0|1/0|
|e05-partial|1/0|1/0|1/0|1/0|1/0|
|e05-none|0/0|0/0|0/0|0/0|0/0|
|e06-full|2/0|2/1|2/1|2/1|2/1|
|e06-partial|1/0|1/2|1/1|1/0|1/1|
|e06-none|0/0|0/0|0/0|0/0|0/0|
|m01-full|0/0|0/0|0/0|0/0|0/0|
|m01-partial|0/0|0/0|0/0|0/0|0/0|
|m01-none|0/0|0/2|0/2|0/0|0/0|
|m02-full|1/1|1/1|1/2|1/1|1/2|
|m02-partial|0/1|1/2|1/1|1/1|1/1|
|m02-none|0/0|0/2|0/2|0/1|0/1|
|m03-full|0/1|1/3|0/4|0/1|0/1|
|m03-partial|1/0|1/1|1/1|1/1|1/0|
|m03-none|0/0|0/2|0/2|0/0|0/0|
|m04-full|1/1|1/2|2/2|1/2|2/2|
|m04-partial|1/0|1/2|1/1|1/0|1/1|
|m04-none|0/0|0/0|0/2|0/0|0/1|
|m05-full|0/1|0/4|1/2|0/3|1/2|
|m05-partial|0/1|0/4|0/4|0/3|0/4|
|m05-none|0/0|0/0|0/2|0/0|0/0|
|m06-full|1/1|1/3|1/2|1/3|1/2|
|m06-partial|1/0|1/2|1/1|1/1|1/1|
|m06-none|0/0|0/2|0/2|0/0|0/0|
|h01-full|1/3|2/4|2/3|1/3|2/3|
|h01-partial|2/1|2/2|2/2|2/1|2/1|
|h01-none|2/0|2/1|2/0|2/0|2/0|
|h02-full|0/0|0/0|0/0|0/0|0/0|
|h02-partial|0/2|0/5|0/2|0/2|0/2|
|h02-none|0/2|0/3|0/3|0/2|0/2|
|h03-full|2/1|2/2|2/1|2/1|2/1|
|h03-partial|0/0|1/1|1/0|1/0|1/0|
|h03-none|2/1|2/2|2/2|2/1|2/1|
|h04-full|1/0|1/2|1/1|1/1|1/1|
|h04-partial|1/0|1/2|1/2|1/1|1/1|
|h04-none|0/0|0/2|0/0|0/0|0/0|
|h05-full|0/0|0/0|0/0|0/0|0/0|
|h05-partial|0/0|0/0|0/0|0/0|0/0|
|h05-none|0/0|1/1|0/6|0/0|0/3|
|h06-full|1/0|1/4|1/4|1/0|1/1|
|h06-partial|1/0|1/3|1/2|1/1|1/2|
|h06-none|0/0|0/3|0/3|0/0|0/0|
|n01|0/0|0/0|0/0|0/0|0/0|
|n02|0/1|0/7|0/4|0/3|0/4|
|n03|0/1|1/5|0/1|1/2|0/1|
|n04|3/0|3/5|3/5|3/0|3/2|
|n05|1/0|1/2|1/1|1/0|1/1|
|n06|1/0|1/3|1/4|1/1|1/2|
|n07|0/0|0/0|0/0|0/0|0/0|
|n08|1/1|2/2|2/1|2/2|2/1|
|n09|1/0|1/3|2/1|1/3|1/1|
|n10|1/0|1/3|2/2|1/3|1/0|
|n11|0/0|0/4|0/2|0/2|0/2|
|n12|2/2|3/6|4/3|2/2|4/3|
|n13|0/2|0/5|0/7|0/2|0/5|
|n14|0/0|0/3|0/2|0/0|0/2|

## m06-full

원문:

> Operating scope of this estimate: under reduced load. The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.

8B 원출력:

```json
{
  "links": [
    {
      "target": "a",
      "role": "condition",
      "quote": "Operating scope of this estimate: under reduced load",
      "evidence_quote": "Operating scope of this estimate: under reduced load. The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet."
    },
    {
      "target": "b",
      "role": "condition",
      "quote": "Operating scope of this estimate: under reduced load",
      "evidence_quote": "Operating scope of this estimate: under reduced load. The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet."
    },
    {
      "target": "c",
      "role": "basis",
      "quote": "No measurement supports this estimate yet",
      "evidence_quote": "I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet."
    }
  ]
}
```

14B 원출력:

```json
{
  "links": [
    {
      "target": "a",
      "role": "condition",
      "quote": "under reduced load",
      "evidence_quote": "Operating scope of this estimate: under reduced load. The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet."
    },
    {
      "target": "c",
      "role": "basis",
      "quote": "No measurement supports this estimate yet",
      "evidence_quote": "I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet."
    }
  ]
}
```

## n03

원문:

> Hello everyone, today I'm starting a new design task: [Designing a File Storage Solution]. Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3. The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack. A preliminary selection recommendation report will be provided early next week.

8B 원출력:

```json
{
  "links": [
    {
      "target": "a",
      "role": "condition",
      "quote": "today I'm starting a new design task",
      "evidence_quote": "today I'm starting a new design task: [Designing a File Storage Solution]. Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3."
    },
    {
      "target": "b",
      "role": "basis",
      "quote": "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future",
      "evidence_quote": "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3."
    },
    {
      "target": "c",
      "role": "basis",
      "quote": "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future",
      "evidence_quote": "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3. The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack."
    },
    {
      "target": "d",
      "role": "condition",
      "quote": "A preliminary selection recommendation report will be provided early next week",
      "evidence_quote": "A preliminary selection recommendation report will be provided early next week."
    }
  ]
}
```

14B 원출력:

```json
{
  "links": [
    {
      "target": "a",
      "role": "basis",
      "quote": "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future",
      "evidence_quote": "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3."
    },
    {
      "target": "b",
      "role": "condition",
      "quote": "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future",
      "evidence_quote": "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3."
    },
    {
      "target": "c",
      "role": "condition",
      "quote": "I will focus on comparing Azure Blob and AWS S3",
      "evidence_quote": "The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack."
    },
    {
      "target": "d",
      "role": "condition",
      "quote": "I will focus on comparing Azure Blob and AWS S3",
      "evidence_quote": "A preliminary selection recommendation report will be provided early next week."
    }
  ]
}
```

## n12

원문:

> Received, thanks a lot! The data structure looks very clear. I plan to complete the static data integration this morning to ensure the charts render correctly. In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it. @Mingzhi Li

8B 원출력:

```json
{
  "links": [
    {
      "target": "c",
      "role": "basis",
      "quote": "I plan to complete the static data integration this morning to ensure the charts render correctly",
      "evidence_quote": "I plan to complete the static data integration this morning to ensure the charts render correctly"
    },
    {
      "target": "d",
      "role": "basis",
      "quote": "In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it",
      "evidence_quote": "In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it"
    }
  ]
}
```

14B 원출력:

```json
{
  "links": [
    {
      "target": "c",
      "role": "basis",
      "quote": "to ensure the charts render correctly",
      "evidence_quote": "I plan to complete the static data integration this morning to ensure the charts render correctly."
    },
    {
      "target": "d",
      "role": "condition",
      "quote": "if the backend supports it",
      "evidence_quote": "In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it."
    }
  ]
}
```

## n13

원문:

> @Yunqi Qian Great plan. WebSocket is the best solution, but our message push service isn't fully ready yet. This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds. Once the WebSocket service is stable later, we can upgrade it uniformly. This way, we can avoid blocking your current task.

8B 원출력:

```json
{
  "links": [
    {
      "target": "c",
      "role": "condition",
      "quote": "This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds.",
      "evidence_quote": "WebSocket is the best solution, but our message push service isn't fully ready yet. This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds. Once the WebSocket service is stable later, we can upgrade it uniformly."
    },
    {
      "target": "e",
      "role": "basis",
      "quote": "This way, we can avoid blocking your current task.",
      "evidence_quote": "Once the WebSocket service is stable later, we can upgrade it uniformly. This way, we can avoid blocking your current task."
    }
  ]
}
```

14B 원출력:

```json
{
  "links": [
    {
      "target": "b",
      "role": "condition",
      "quote": "but our message push service isn't fully ready yet",
      "evidence_quote": "@Yunqi Qian Great plan. WebSocket is the best solution, but our message push service isn't fully ready yet."
    },
    {
      "target": "c",
      "role": "basis",
      "quote": "but our message push service isn't fully ready yet",
      "evidence_quote": "WebSocket is the best solution, but our message push service isn't fully ready yet. This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds."
    },
    {
      "target": "d",
      "role": "basis",
      "quote": "Once the WebSocket service is stable later",
      "evidence_quote": "Once the WebSocket service is stable later, we can upgrade it uniformly."
    },
    {
      "target": "e",
      "role": "basis",
      "quote": "Once the WebSocket service is stable later, we can upgrade it uniformly",
      "evidence_quote": "Once the WebSocket service is stable later, we can upgrade it uniformly. This way, we can avoid blocking your current task."
    }
  ]
}
```
