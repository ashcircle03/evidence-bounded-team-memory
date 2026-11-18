# 문서 전체 records 비교

실제 Qwen3-8B job122970의136개 원출력을 재평가했다. 신규 추론0회. 매 사례의 원문, 전체 정답, 원출력, 누락/오추출/잘못된 연결을 함께 읽는다.

## e01-full · easy · full

source_id: `33abbca0dc91dbb59f467b14`

For chilled parcels, use liner K6 because the foam prevents condensation.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|use liner K6|21:33|True|
|r1:condition1|condition|chilled parcels|4:19|True|
|r1:basis1|basis|the foam prevents condensation|42:72|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "For chilled parcels, use liner K6 because the foam prevents condensation.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "For chilled parcels",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "use liner K6",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    },
    {
      "basis": "the foam prevents condensation",
      "basis_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e01-partial · easy · partial

source_id: `6fea6f425cd00d4746adb023`

For chilled parcels, use liner K6.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|use liner K6|21:33|True|
|r1:condition1|condition|chilled parcels|4:19|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "For chilled parcels, use liner K6.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "For chilled parcels",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "use liner K6",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e01-none · easy · none

source_id: `97200ceeaf92691fde3c3f0a`

use liner K6.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|use liner K6|0:12|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "use liner K6.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "use liner K6",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e02-full · easy · full

source_id: `709f8ae378397a731a47ec82`

close gate R8 on Thursday because the hinge needs repair.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|close gate R8|0:13|True|
|r1:basis1|basis|the hinge needs repair|34:56|True|
|r1:time1|time|on Thursday|14:25|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "close gate R8 on Thursday",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    },
    {
      "condition": "because the hinge needs repair",
      "condition_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Context has claim stance

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:basis1",
    "r1:claim",
    "r1:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "close gate R8",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    },
    {
      "time": "Thursday",
      "time_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "condition": "because the hinge needs repair",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e02-partial · easy · partial

source_id: `925538e36ab8cf414f9cb883`

close gate R8 because the hinge needs repair.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|close gate R8|0:13|True|
|r1:basis1|basis|the hinge needs repair|22:44|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "close gate R8 because the hinge needs repair.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "close gate R8",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    },
    {
      "condition": "because the hinge needs repair",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 1,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 1,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e02-none · easy · none

source_id: `801945abc96c000f57f6e92a`

close gate R8.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|close gate R8|0:13|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": []
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [
    "r1:claim"
  ],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [
    "r1:claim"
  ],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "close gate R8",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e03-full · easy · full

source_id: `26e96d281e3e856dedc95b7e`

For cracked containers, do not ship kit M3 because the seal failed inspection.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not ship kit M3|24:42|True|
|r1:condition1|condition|cracked containers|4:22|True|
|r1:basis1|basis|the seal failed inspection|51:77|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "For cracked containers, do not ship kit M3 because the seal failed inspection.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "For cracked containers",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "do not ship kit M3",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    },
    {
      "basis": "the seal failed inspection",
      "basis_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e03-partial · easy · partial

source_id: `02b5161b879fac5c3943fee0`

For cracked containers, do not ship kit M3.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not ship kit M3|24:42|True|
|r1:condition1|condition|cracked containers|4:22|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "For cracked containers, do not ship kit M3.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "For cracked containers",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "do not ship kit M3",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e03-none · easy · none

source_id: `74738fb6b8b3b19b518bd96e`

do not ship kit M3.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not ship kit M3|0:18|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "do not ship kit M3.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "do not ship kit M3",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e04-full · easy · full

source_id: `d764923f575d0292ebbbffa2`

For inland stations, we might trial paint Q9. This trial is not approved.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we might trial paint Q9|21:44|True|
|r1:condition1|condition|inland stations|4:19|True|
|r1:caveat1|caveat|This trial is not approved.|46:73|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "we might trial paint Q9",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "proposal"
      }
    },
    {
      "condition": "For inland stations",
      "condition_attributes": {
        "claim_group": "1"
     
    ,
      "stance": "unknown"
    }
  }
]  }
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [
    "r1:caveat1"
  ],
  "missing_edges": [
    [
      "r1",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [
    "r1:caveat1"
  ],
  "missing_edges": [
    [
      "r1",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "For inland stations",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "we might trial paint Q9",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "proposal"
      }
    },
    {
      "claim": "This trial is not approved",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

## e04-partial · easy · partial

source_id: `a8989ff9f5cbe9dadc7c475b`

we might trial paint Q9. This trial is not approved.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we might trial paint Q9|0:23|True|
|r1:caveat1|caveat|This trial is not approved.|25:52|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "we might trial paint Q9",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "This trial is not approved",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "we might trial paint Q9",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "proposal"
      }
    },
    {
      "claim": "This trial is not approved",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

## e04-none · easy · none

source_id: `668ff2dbdae195e6f8d1967f`

we might trial paint Q9.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we might trial paint Q9|0:23|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "we might trial paint Q9.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "we might trial paint Q9",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e05-full · easy · full

source_id: `694c889970229e4061e0b4d4`

Recorded event time: on Tuesday. the sensor check is complete for firmware 6.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the sensor check is complete|33:61|True|
|r1:condition1|condition|firmware 6|66:76|True|
|r1:time1|time|on Tuesday|21:31|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "the sensor check is complete for firmware 6",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "time": "on Tuesday",
      "time_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "the sensor check is complete for firmware 6",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e05-partial · easy · partial

source_id: `63b0dc798b1b6b19caf5f134`

Recorded event time: on Tuesday. the sensor check is complete.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the sensor check is complete|33:61|True|
|r1:time1|time|on Tuesday|21:31|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "the sensor check is complete",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "time": "on Tuesday",
      "time_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "the sensor check is complete",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e05-none · easy · none

source_id: `68d5db1a3a6ad6422d2040e6`

the sensor check is complete.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the sensor check is complete|0:28|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "the sensor check is complete",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "the sensor check is complete",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e06-full · easy · full

source_id: `d0fcf930f9524f0f08399148`

For dry rooms, I suspect relay P4 may last 80 days. This estimate is untested.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect relay P4 may last 80 days|15:50|True|
|r1:condition1|condition|dry rooms|4:13|True|
|r1:caveat1|caveat|This estimate is untested.|52:78|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "I suspect relay P4 may last 80 days.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "uncertainty"
      }
    },
    {
      "condition": "For dry rooms",
      "condition_attributes": {
        "claim_group": "1"
     
    ,
    "stance": "unknown"
    }
  }
]  }
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [
    "r1:caveat1"
  ],
  "missing_edges": [
    [
      "r1",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [
    "r1:caveat1"
  ],
  "missing_edges": [
    [
      "r1",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "For dry rooms",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "I suspect relay P4 may last 80 days",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "This estimate is untested",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e06-partial · easy · partial

source_id: `c628de4a11483d61a9204676`

I suspect relay P4 may last 80 days. This estimate is untested.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect relay P4 may last 80 days|0:35|True|
|r1:caveat1|caveat|This estimate is untested.|37:63|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "I suspect relay P4 may last 80 days.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "condition": "This estimate is untested.",
      "condition_attributes": {
        "claim_group": "1",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 1,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:caveat1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "uncertainty"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 1,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:caveat1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "uncertainty"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "I suspect relay P4 may last 80 days",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "This estimate is untested",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## e06-none · easy · none

source_id: `566f53022fec16660340d521`

I suspect relay P4 may last 80 days.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect relay P4 may last 80 days|0:35|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "I suspect relay P4 may last 80 days.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "I suspect relay P4 may last 80 days",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "This survey decision applies to sector D2.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    },
    {
      "claim": "The cabinet label is copper.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "we postpone the gravel survey because the access bridge is closed.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r2:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "This survey decision applies to sector D2",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The cabinet label is copper",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "we postpone the gravel survey",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    },
    {
      "condition": "because the access bridge is closed",
      "condition_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Orphaned context group

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 2,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ],
    [
      "unbound:a",
      "condition",
      "r1:condition1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:basis1",
    "r1:claim",
    "r1:condition1",
    "r2:claim"
  ],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m01-partial · medium · partial

source_id: `aa89de85e1e7b4d439b8b949`

This survey decision applies to sector D2. The cabinet label is copper. we postpone the gravel survey.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we postpone the gravel survey|72:101|True|
|r1:condition1|condition|sector D2|32:41|True|
|r2:claim|claim|The cabinet label is copper|43:70|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "This survey decision applies to sector D2.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    },
    {
      "claim": "The cabinet label is copper.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "we postpone the gravel survey.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r2:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "This survey decision applies to sector D2",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The cabinet label is copper",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "we postpone the gravel survey",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Orphaned context group

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 1,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:a",
      "condition",
      "r1:condition1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:condition1",
    "r2:claim"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m01-none · medium · none

source_id: `5ed1d90a243e42fa026cf898`

The cabinet label is copper. we postpone the gravel survey.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we postpone the gravel survey|29:58|True|
|r2:claim|claim|The cabinet label is copper|0:27|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "The cabinet label is copper.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "we postpone the gravel survey.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The cabinet label is copper",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "we postpone the gravel survey",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "after the morning inspection",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    },
    {
      "claim": "the antenna colour remains white",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "switch the beacon to standby because the battery is leaking",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "after the morning inspection",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "Timing for the following beacon instruction",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The antenna colour remains white",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "switch the beacon to standby",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    },
    {
      "basis": "the battery is leaking",
      "basis_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:a",
      "condition",
      "r1:time1"
    ]
  ],
  "extra_rows": [
    {
      "row": 1,
      "role": "claim",
      "text": "Timing for the following beacon instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    1
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:c:6686d1f759ad368e7e7ad49b",
      "condition",
      "r1:time1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Timing for the following beacon instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m02-partial · medium · partial

source_id: `5557e3d2bc40298994abc274`

The antenna colour remains white. switch the beacon to standby because the battery is leaking.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|switch the beacon to standby|34:62|True|
|r1:basis1|basis|the battery is leaking|71:93|True|
|r2:claim|claim|The antenna colour remains white|0:32|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "The antenna colour remains white.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "switch the beacon to standby because the battery is leaking.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The antenna colour remains white",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "switch the beacon to standby",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "decision"
      }
    },
    {
      "condition": "because the battery is leaking",
      "condition_attributes": {
        "claim_group": "b",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 1,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 1,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m02-none · medium · none

source_id: `45e125beb1e51de31e6fc861`

The antenna colour remains white. switch the beacon to standby.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|switch the beacon to standby|34:62|True|
|r2:claim|claim|The antenna colour remains white|0:32|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "The antenna colour remains white.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "switch the beacon to standby.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The antenna colour remains white",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "switch the beacon to standby",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "do not release batch U5 because the residue test failed",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    },
    {
      "claim": "Freshwater batches remain eligible for release",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1"
  ],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1"
  ],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The following release instruction applies to saline batches",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "do not release batch U5",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "decision"
      }
    },
    {
      "condition": "because the residue test failed",
      "condition_attributes": {
        "claim_group": "b",
        "stance": "unknown"
      }
    },
    {
      "claim": "Freshwater batches remain eligible for release",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m03-partial · medium · partial

source_id: `ca86e4fed815e881bbb73c14`

The following release instruction applies to saline batches. do not release batch U5. Freshwater batches remain eligible for release.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not release batch U5|61:84|True|
|r1:condition1|condition|saline batches|45:59|True|
|r2:claim|claim|Freshwater batches remain eligible for release|86:132|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "do not release batch U5",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    },
    {
      "claim": "Freshwater batches remain eligible for release",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r2:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "The following release instruction applies to saline batches",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "do not release batch U5",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    },
    {
      "claim": "Freshwater batches remain eligible for release",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m03-none · medium · none

source_id: `eb9f29530f2bc3d522f4dcc8`

do not release batch U5. Freshwater batches remain eligible for release.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|do not release batch U5|0:23|True|
|r2:claim|claim|Freshwater batches remain eligible for release|25:71|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "do not release batch U5",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    },
    {
      "claim": "Freshwater batches remain eligible for release",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "do not release batch U5",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    },
    {
      "claim": "Freshwater batches remain eligible for release",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The spare tubing is blue.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "we could pilot filter J2.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "proposal"
      }
    },
    {
      "claim": "This pilot is a suggestion, not an authorization.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1"
  ],
  "missing_edges": [
    [
      "r1",
      "caveat",
      "r1:caveat1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:3",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1"
  ],
  "missing_edges": [
    [
      "r1",
      "caveat",
      "r1:caveat1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:c:ebe4bdaf9f52beb0c0468209",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "Scope of the filter pilot",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "remote clinics",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The spare tubing is blue",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "we could pilot filter J2",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "proposal"
      }
    },
    {
      "claim": "This pilot is a suggestion, not an authorization",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:a",
      "condition",
      "unmatched:0"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "condition",
      "text": "Scope of the filter pilot",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    1
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:c:d7b4be7afd1b6bf71b1dbe12",
      "condition",
      "unmatched:1"
    ]
  ],
  "extra_rows": [
    {
      "row": 1,
      "role": "condition",
      "text": "Scope of the filter pilot",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

## m04-partial · medium · partial

source_id: `c186a128c7866ca21efe5ce4`

The spare tubing is blue. we could pilot filter J2. This pilot is a suggestion, not an authorization.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we could pilot filter J2|26:50|True|
|r1:caveat1|caveat|This pilot is a suggestion, not an authorization.|52:101|True|
|r2:claim|claim|The spare tubing is blue|0:24|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "The spare tubing is blue.",
      "claim_attributes": {
        "claim_group": "group1",
        "stance": "observation"
      }
    },
    {
      "claim": "we could pilot filter J2.",
      "claim_attributes": {
        "claim_group": "group2",
        "stance": "proposal"
      }
    },
    {
      "claim": "This pilot is a suggestion, not an authorization.",
      "claim_attributes": {
        "claim_group": "group2",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The spare tubing is blue",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "we could pilot filter J2",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "proposal"
      }
    },
    {
      "claim": "This pilot is a suggestion, not an authorization",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

## m04-none · medium · none

source_id: `ff1dc03758f2c348b5760225`

The spare tubing is blue. we could pilot filter J2.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|we could pilot filter J2|26:50|True|
|r2:claim|claim|The spare tubing is blue|0:24|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "The spare tubing is blue.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "we could pilot filter J2.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The spare tubing is blue",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "we could pilot filter J2",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The calibration event occurred on Friday afternoon.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The office clock was repaired.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The valve calibration finished on bench T7.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The calibration event occurred",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "time": "on Friday afternoon",
      "time_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The office clock was repaired",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "the valve calibration finished on bench T7",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:a",
      "time",
      "r1:time1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "The calibration event occurred",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:c:6684ea95d8402bbdb5ff9f14",
      "time",
      "r1:time1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "The calibration event occurred",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m05-partial · medium · partial

source_id: `8b37462b2d1ffdee37d08519`

The calibration event occurred on Friday afternoon. The office clock was repaired. the valve calibration finished.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the valve calibration finished|83:113|True|
|r1:time1|time|on Friday afternoon|31:50|True|
|r2:claim|claim|The office clock was repaired|52:81|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "The calibration event occurred on Friday afternoon.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The office clock was repaired.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "the valve calibration finished.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The calibration event occurred",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "time": "on Friday afternoon",
      "time_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The office clock was repaired",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "the valve calibration finished",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 1,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:a",
      "time",
      "r1:time1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "The calibration event occurred",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 1,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:c:1587318f72a7f97c7e9bf34c",
      "time",
      "r1:time1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "The calibration event occurred",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m05-none · medium · none

source_id: `c69146fee259c2e07e827f91`

The office clock was repaired. the valve calibration finished.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|the valve calibration finished|31:61|True|
|r2:claim|claim|The office clock was repaired|0:29|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "The office clock was repaired.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "the valve calibration finished.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The office clock was repaired",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "the valve calibration finished",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "Operating scope of this estimate: under reduced load.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The procurement task is complete.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect drive L4 may reach 70 cycles.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "No measurement supports this estimate yet.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "uncertainty"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "uncertainty"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "condition": "under reduced load",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "Operating scope of this estimate",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The procurement task is complete",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect drive L4 may reach 70 cycles",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "No measurement supports this estimate yet",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:a",
      "condition",
      "r1:condition1"
    ]
  ],
  "extra_rows": [
    {
      "row": 1,
      "role": "claim",
      "text": "Operating scope of this estimate",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    1
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:c:7ed1da6ca3ef8d01fa51f0bc",
      "condition",
      "r1:condition1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Operating scope of this estimate",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m06-partial · medium · partial

source_id: `9dc93469ba851b9facbaf1e5`

The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect drive L4 may reach 70 cycles|34:72|True|
|r1:caveat1|caveat|No measurement supports this estimate yet.|74:116|True|
|r2:claim|claim|The procurement task is complete|0:32|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "The procurement task is complete.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect drive L4 may reach 70 cycles.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "No measurement supports this estimate yet.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The procurement task is complete",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect drive L4 may reach 70 cycles",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "No measurement supports this estimate yet",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

## m06-none · medium · none

source_id: `42c88617812e2f691d3bada8`

The procurement task is complete. I suspect drive L4 may reach 70 cycles.

| 정답 ID | 역할 | 구절 | 원문 범위 | 필수 |
|---|---|---|---|---|
|r1:claim|claim|I suspect drive L4 may reach 70 cycles|34:72|True|
|r2:claim|claim|The procurement task is complete|0:32|True|

연결은 `record_id → role → node_id`. 각 rN의 claim은 그 기록의 중심 주장이고 caveat/method는 독립적으로 추출·연결해야 하는 한정/방법이다.

### simple

```json
{
  "extractions": [
    {
      "claim": "The procurement task is complete.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect drive L4 may reach 70 cycles.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The procurement task is complete",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect drive L4 may reach 70 cycles",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "uncertainty"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "Scope of the compressor instruction: pressure above 9 bar.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "observation"
      }
    },
    {
      "claim": "halt compressor Z4 because its casing has fractured.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "decision"
      }
    },
    {
      "claim": "Separate instruction: below 1 bar, start pump B2 because the buffer is empty.",
      "claim_attributes": {
        "claim_group": "7",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Scope of the compressor instruction",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "condition": "pressure above 9 bar",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "halt compressor Z4",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "decision"
      }
    },
    {
      "condition": "its casing has fractured",
      "condition_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    },
    {
      "claim": "Separate instruction",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    },
    {
      "condition": "below 1 bar",
      "condition_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    },
    {
      "claim": "start pump B2",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "decision"
      }
    },
    {
      "condition": "the buffer is empty",
      "condition_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 2,
    "fn": 0,
    "precision": 0.75,
    "recall": 1.0,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 1,
    "fp": 3,
    "fn": 3,
    "precision": 0.25,
    "recall": 0.25,
    "f1": 0.25
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:basis1"
    ],
    [
      "unbound:a",
      "condition",
      "r1:condition1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Scope of the compressor instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    },
    {
      "row": 8,
      "role": "claim",
      "text": "Separate instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0,
    8
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 2,
    "fn": 0,
    "precision": 0.75,
    "recall": 1.0,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 1,
    "fp": 3,
    "fn": 3,
    "precision": 0.25,
    "recall": 0.25,
    "f1": 0.25
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:basis1"
    ],
    [
      "unbound:c:928ab3c43dec70ec821907a2",
      "condition",
      "r1:condition1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Scope of the compressor instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    },
    {
      "row": 8,
      "role": "claim",
      "text": "Separate instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0,
    8
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "Scope of the compressor instruction: pressure above 9 bar.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "observation"
      }
    },
    {
      "claim": "halt compressor Z4.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "decision"
      }
    },
    {
      "claim": "Separate instruction: below 1 bar, start pump B2 because the buffer is empty.",
      "claim_attributes": {
        "claim_group": "7",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Scope of the compressor instruction",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "condition": "pressure above 9 bar",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "halt compressor Z4",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "decision"
      }
    },
    {
      "claim": "Separate instruction",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    },
    {
      "condition": "below 1 bar",
      "condition_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    },
    {
      "claim": "start pump B2",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "decision"
      }
    },
    {
      "basis": "the buffer is empty",
      "basis_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 2,
    "fn": 0,
    "precision": 0.75,
    "recall": 1.0,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 2,
    "fp": 1,
    "fn": 1,
    "precision": 0.6666666666666666,
    "recall": 0.6666666666666666,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:a",
      "condition",
      "r1:condition1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Scope of the compressor instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    },
    {
      "row": 7,
      "role": "claim",
      "text": "Separate instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0,
    7
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 2,
    "fn": 0,
    "precision": 0.75,
    "recall": 1.0,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 2,
    "fp": 1,
    "fn": 1,
    "precision": 0.6666666666666666,
    "recall": 0.6666666666666666,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:c:bf129db757a1a8e2932f9392",
      "condition",
      "r1:condition1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Scope of the compressor instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    },
    {
      "row": 7,
      "role": "claim",
      "text": "Separate instruction",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0,
    7
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "halt compressor Z4.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "decision"
      }
    },
    {
      "claim": "below 1 bar, start pump B2 because the buffer is empty.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "halt compressor Z4",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "decision"
      }
    },
    {
      "condition": "below 1 bar",
      "condition_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    },
    {
      "claim": "start pump B2",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "decision"
      }
    },
    {
      "basis": "the buffer is empty",
      "basis_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The time of the compass instruction is at 14:20.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "observation"
      }
    },
    {
      "claim": "resume the compass test because the replacement mount passed inspection.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "decision"
      }
    },
    {
      "claim": "The camera check begins at 14:20 because its lens is clean.",
      "claim_attributes": {
        "claim_group": "7",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "decision"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "decision"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The time of the compass instruction is at 14:20",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "time": "at 14:20",
      "time_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "resume the compass test because the replacement mount passed inspection",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "decision"
      }
    },
    {
      "condition": "because the replacement mount passed inspection",
      "condition_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    },
    {
      "claim": "Independently, the camera check begins at 14:20",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "decision"
      }
    },
    {
      "time": "at 14:20",
      "time_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    },
    {
      "condition": "because its lens is clean",
      "condition_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Ambiguous repeated context span

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 1,
    "fp": 3,
    "fn": 3,
    "precision": 0.25,
    "recall": 0.25,
    "f1": 0.25
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:basis1"
    ],
    [
      "unbound:a",
      "time",
      "r1:time1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "decision"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 10,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 6,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:basis1",
    "r1:claim",
    "r1:time1",
    "r2:claim",
    "r3:claim",
    "r4:claim",
    "r5:claim",
    "r6:basis1",
    "r6:claim",
    "r6:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "Resume the compass test because the replacement mount passed inspection.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "decision"
      }
    },
    {
      "claim": "The camera check begins at 14:20 because its lens is clean.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "decision"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "decision"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "resume the compass test",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "decision"
      }
    },
    {
      "condition": "because the replacement mount passed inspection",
      "condition_attributes": {
        "claim_group": "e",
        "stance": "unknown"
      }
    },
    {
      "claim": "the camera check begins at 14:20",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "decision"
      }
    },
    {
      "condition": "because its lens is clean",
      "condition_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 2,
    "fn": 3,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "decision"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 2,
    "fn": 3,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "decision"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "resume the compass test.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "unknown"
      }
    },
    {
      "claim": "The camera check begins at 14:20 because its lens is clean.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "resume the compass test",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "decision"
      }
    },
    {
      "condition": "Independently, the camera check begins at 14:20",
      "condition_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    },
    {
      "claim": "because its lens is clean",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.8333333333333334,
    "f1": 0.9090909090909091
  },
  "typed_edges": {
    "tp": 0,
    "fp": 2,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:f",
      "condition",
      "r6:claim"
    ],
    [
      "unbound:f",
      "condition",
      "r6:time1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.8333333333333334,
    "f1": 0.9090909090909091
  },
  "typed_edges": {
    "tp": 0,
    "fp": 2,
    "fn": 2,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "unbound:c:a86c372f301bf24a7bae724b",
      "condition",
      "r6:claim"
    ],
    [
      "unbound:c:a86c372f301bf24a7bae724b",
      "condition",
      "r6:time1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "do not publish the terrain map because the licence excludes commercial distribution",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "for classroom teaching, publish the sketch because the teacher granted permission",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 5,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 4,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1",
    "r2:claim",
    "r3:claim",
    "r4:claim",
    "r5:claim"
  ],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r6:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 5,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 4,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1",
    "r2:claim",
    "r3:claim",
    "r4:claim",
    "r5:claim"
  ],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r6:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The map instruction below concerns commercial reuse",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "do not publish the terrain map because the licence excludes commercial distribution",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "decision"
      }
    },
    {
      "condition": "the licence excludes commercial distribution",
      "condition_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    },
    {
      "claim": "Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "decision"
      }
    },
    {
      "condition": "for classroom teaching",
      "condition_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    },
    {
      "basis": "the teacher granted permission",
      "basis_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 2,
    "fp": 1,
    "fn": 2,
    "precision": 0.6666666666666666,
    "recall": 0.5,
    "f1": 0.5714285714285714
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 2,
    "fp": 1,
    "fn": 2,
    "precision": 0.6666666666666666,
    "recall": 0.5,
    "f1": 0.5714285714285714
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "basis",
      "r1:basis1"
    ],
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r1:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "do not publish the terrain map",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "for classroom teaching, publish the sketch because the teacher granted permission",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 5,
    "precision": 1.0,
    "recall": 0.4444444444444444,
    "f1": 0.6153846153846154
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 4,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1",
    "r2:claim",
    "r3:claim",
    "r4:claim",
    "r5:claim"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r6:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 5,
    "precision": 1.0,
    "recall": 0.4444444444444444,
    "f1": 0.6153846153846154
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 4,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:condition1",
    "r2:claim",
    "r3:claim",
    "r4:claim",
    "r5:claim"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r6:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The map instruction below concerns commercial reuse",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "do not publish the terrain map",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "decision"
      }
    },
    {
      "claim": "Separate instruction: for classroom teaching, publish the sketch",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "decision"
      }
    },
    {
      "claim": "because the teacher granted permission",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r6:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "do not publish the terrain map.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "decision"
      }
    },
    {
      "claim": "for classroom teaching, publish the sketch because the teacher granted permission.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "basis",
      "r6:basis1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "do not publish the terrain map",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "decision"
      }
    },
    {
      "claim": "for classroom teaching, publish the sketch because the teacher granted permission",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "decision"
      }
    },
    {
      "condition": "for classroom teaching",
      "condition_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    },
    {
      "subject": "the sketch",
      "subject_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    },
    {
      "basis": "the teacher granted permission",
      "basis_attributes": {
        "claim_group": "f",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [
    [
      "unbound:f",
      "subject",
      "unmatched:7"
    ]
  ],
  "extra_rows": [
    {
      "row": 7,
      "role": "subject",
      "text": "the sketch",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [
    [
      "unbound:c:0094a8e07644286a0bd4b2fc",
      "subject",
      "unmatched:8"
    ]
  ],
  "extra_rows": [
    {
      "row": 8,
      "role": "subject",
      "text": "the sketch",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The pack trial applies to desert depots.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "observation"
      }
    },
    {
      "claim": "we might trial pack G8.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "proposal"
      }
    },
    {
      "claim": "This proposed trial has no deployment approval.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "observation"
      }
    },
    {
      "claim": "Independently, the warehouse rollout is approved.",
      "claim_attributes": {
        "claim_group": "7",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The pack trial applies to desert depots",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "we might trial pack G8",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "proposal"
      }
    },
    {
      "claim": "This proposed trial has no deployment approval",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "Independently, the warehouse rollout is approved",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "we might trial pack G8.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "proposal"
      }
    },
    {
      "claim": "This proposed trial has no deployment approval.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The warehouse rollout is approved.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "we might trial pack G8",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "proposal"
      }
    },
    {
      "claim": "This proposed trial has no deployment approval",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "the warehouse rollout is approved",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r1:caveat1",
      "expected": [
        "observation",
        "uncertainty"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "we might trial pack G8.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "proposal"
      }
    },
    {
      "claim": "the warehouse rollout is approved.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r6"
    ],
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r6"
    ],
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r6:claim",
      "expected": [
        "observation",
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "we might trial pack G8",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "proposal"
      }
    },
    {
      "claim": "the warehouse rollout is approved",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The pressure audit ended at 16:40.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The pressure audit concerns rig C9.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "observation"
      }
    },
    {
      "claim": "The pressure audit ended.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The noise audit starts at 16:40 on rig B7.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    1
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The pressure audit ended",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "time": "at 16:40",
      "time_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "condition": "The pressure audit concerns rig C9",
      "condition_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "The pressure audit ended",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "observation"
      }
    },
    {
      "claim": "Separately, the noise audit starts at 16:40",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "observation"
      }
    },
    {
      "time": "at 16:40",
      "time_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    },
    {
      "condition": "on rig B7",
      "condition_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Ambiguous repeated context span

**raw**
```json
{
  "complete": true,
  "content_recall": {
    "tp": 10,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 10,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 6,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:condition1",
    "r1:time1",
    "r2:claim",
    "r3:claim",
    "r4:claim",
    "r5:claim",
    "r6:claim",
    "r6:condition1",
    "r6:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The pressure audit ended at 16:40.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "observation"
      }
    },
    {
      "claim": "The pressure audit ended.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The noise audit starts at 16:40 on rig B7.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The pressure audit ended",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "time": "at 16:40",
      "time_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "the pressure audit ended",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "observation"
      }
    },
    {
      "claim": "Separately, the noise audit starts at 16:40 on rig B7",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "observation"
      }
    },
    {
      "time": "at 16:40",
      "time_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    },
    {
      "subject": "rig B7",
      "subject_attributes": {
        "claim_group": "g",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Ambiguous repeated context span

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 1,
    "fn": 1,
    "precision": 0.6666666666666666,
    "recall": 0.6666666666666666,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r6",
      "subject",
      "r6:condition1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 9,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 6,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:time1",
    "r2:claim",
    "r3:claim",
    "r4:claim",
    "r5:claim",
    "r6:claim",
    "r6:condition1",
    "r6:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "The pressure audit ended.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "observation"
      }
    },
    {
      "claim": "The noise audit starts at 16:40 on rig B7.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "the pressure audit ended",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "the noise audit starts at 16:40 on rig B7",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ],
    [
      "r6",
      "time",
      "r6:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The coil estimate concerns operation in nitrogen.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect coil N8 may handle 18 amperes.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "This capacity is conjectural and has not been measured.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "A separate steel cable was measured at 12 amperes in air.",
      "claim_attributes": {
        "claim_group": "7",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The coil estimate concerns operation in nitrogen",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect coil N8 may handle 18 amperes",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "This capacity is conjectural and has not been measured",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "A separate steel cable was measured at 12 amperes in air",
      "claim_attributes": {
        "claim_group": "g",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 1,
    "fn": 0,
    "precision": 0.8571428571428571,
    "recall": 1.0,
    "f1": 0.9230769230769231
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect coil N8 may handle 18 amperes.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "This capacity is conjectural and has not been measured.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "A separate steel cable was measured at 12 amperes in air.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r2",
      "r5"
    ],
    [
      "r3",
      "r4"
    ],
    [
      "r3",
      "r5"
    ],
    [
      "r4",
      "r5"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect coil N8 may handle 18 amperes",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "This capacity is conjectural and has not been measured",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "A separate steel cable was measured at 12 amperes in air",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs.",
      "claim_attributes": {
        "claim_group": "3",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper.",
      "claim_attributes": {
        "claim_group": "4",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect coil N8 may handle 18 amperes.",
      "claim_attributes": {
        "claim_group": "5",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "A separate steel cable was measured at 12 amperes in air.",
      "claim_attributes": {
        "claim_group": "6",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The delivery folder contains a yellow form",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The stock counter remains seven",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The break room has two chairs",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "The printer tray contains plain paper",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    },
    {
      "claim": "I suspect coil N8 may handle 18 amperes",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "uncertainty"
      }
    },
    {
      "claim": "A separate steel cable was measured at 12 amperes in air",
      "claim_attributes": {
        "claim_group": "f",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r6",
      "condition",
      "r6:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The task 'Verify the accuracy of alarm rule creation and trigger logic' for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "All test cases have passed, including various single conditions, combined conditions, and boundary value scenarios.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The few issues discovered yesterday have also all been regression verified and passed.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The final test report has been uploaded to Confluence.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Ungrounded extraction

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 3,
    "fn": 1,
    "precision": 0.25,
    "recall": 0.5,
    "f1": 0.3333333333333333
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r3",
      "time",
      "r3:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "caveat",
      "r2:caveat1"
    ],
    [
      "r3",
      "caveat",
      "r2:caveat1"
    ],
    [
      "r4",
      "caveat",
      "r2:caveat1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ],
    [
      "r1",
      "r3"
    ],
    [
      "r1",
      "r4"
    ],
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 6,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r2:caveat1",
    "r2:claim",
    "r3:claim",
    "r3:time1",
    "r4:claim"
  ],
  "missing_edges": [
    [
      "r2",
      "caveat",
      "r2:caveat1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "[Task Completed] Hello everyone, the task 'Verify the accuracy of alarm rule creation and trigger logic' for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "All test cases have passed, including various single conditions, combined conditions, and boundary value scenarios",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The few issues discovered yesterday have also all been regression verified and passed",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The final test report has been uploaded to Confluence",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Ungrounded extraction

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 3,
    "fn": 1,
    "precision": 0.25,
    "recall": 0.5,
    "f1": 0.3333333333333333
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r3",
      "time",
      "r3:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "caveat",
      "r2:caveat1"
    ],
    [
      "r3",
      "caveat",
      "r2:caveat1"
    ],
    [
      "r4",
      "caveat",
      "r2:caveat1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ],
    [
      "r1",
      "r3"
    ],
    [
      "r1",
      "r4"
    ],
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 6,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r2:caveat1",
    "r2:claim",
    "r3:claim",
    "r3:time1",
    "r4:claim"
  ],
  "missing_edges": [
    [
      "r2",
      "caveat",
      "r2:caveat1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "your medication check-in module and family member invitation interface are due today",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "Please make sure to complete the delivery today",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    },
    {
      "claim": "Other colleagues, please also share your plans and progress for today",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 6,
    "precision": 1.0,
    "recall": 0.5714285714285714,
    "f1": 0.7272727272727273
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 10,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:time2",
    "r2:recipient1",
    "r2:time2",
    "r3:time2",
    "r4:time2"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r1",
      "time",
      "r1:time2"
    ],
    [
      "r2",
      "recipient",
      "r2:recipient1"
    ],
    [
      "r2",
      "time",
      "r2:time1"
    ],
    [
      "r2",
      "time",
      "r2:time2"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r3",
      "time",
      "r3:time2"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ],
    [
      "r4",
      "time",
      "r4:time2"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 6,
    "precision": 1.0,
    "recall": 0.5714285714285714,
    "f1": 0.7272727272727273
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 10,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:time2",
    "r2:recipient1",
    "r2:time2",
    "r3:time2",
    "r4:time2"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r1",
      "time",
      "r1:time2"
    ],
    [
      "r2",
      "recipient",
      "r2:recipient1"
    ],
    [
      "r2",
      "time",
      "r2:time1"
    ],
    [
      "r2",
      "time",
      "r2:time2"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r3",
      "time",
      "r3:time2"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ],
    [
      "r4",
      "time",
      "r4:time2"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r2:claim",
      "expected": [
        "observation",
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r3:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Good morning everyone",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "Today is Thursday",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "your medication check-in module and family member invitation interface are due today",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "decision"
      }
    },
    {
      "subject": "your medication check-in module and family member invitation interface",
      "subject_attributes": {
        "claim_group": "b",
        "stance": "unknown"
      }
    },
    {
      "claim": "Please make sure to complete the delivery today",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    },
    {
      "claim": "Other colleagues, please also share your plans and progress for today",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 13,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.9285714285714286,
    "f1": 0.9629629629629629
  },
  "claim_recall": {
    "tp": 4,
    "fp": 1,
    "fn": 0,
    "precision": 0.8,
    "recall": 1.0,
    "f1": 0.8888888888888888
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 10,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r2:recipient1"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r1",
      "time",
      "r1:time2"
    ],
    [
      "r2",
      "recipient",
      "r2:recipient1"
    ],
    [
      "r2",
      "time",
      "r2:time1"
    ],
    [
      "r2",
      "time",
      "r2:time2"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r3",
      "time",
      "r3:time2"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ],
    [
      "r4",
      "time",
      "r4:time2"
    ]
  ],
  "incorrect_edges": [
    [
      "r2",
      "subject",
      "r3:subject1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Good morning everyone",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 13,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.9285714285714286,
    "f1": 0.9629629629629629
  },
  "claim_recall": {
    "tp": 4,
    "fp": 1,
    "fn": 0,
    "precision": 0.8,
    "recall": 1.0,
    "f1": 0.8888888888888888
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 10,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r2:recipient1"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r1",
      "time",
      "r1:time2"
    ],
    [
      "r2",
      "recipient",
      "r2:recipient1"
    ],
    [
      "r2",
      "time",
      "r2:time1"
    ],
    [
      "r2",
      "time",
      "r2:time2"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r3",
      "time",
      "r3:time2"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ],
    [
      "r4",
      "time",
      "r4:time2"
    ]
  ],
  "incorrect_edges": [
    [
      "r2",
      "subject",
      "r3:subject1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Good morning everyone",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "Designing a File Storage Solution",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "proposal"
      }
    },
    {
      "claim": "our system will need to store a large number of supporting documents, reports, etc. in the future",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "I will focus on comparing Azure Blob and AWS S3",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "proposal"
      }
    },
    {
      "claim": "The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "proposal"
      }
    },
    {
      "claim": "A preliminary selection recommendation report will be provided early next week",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.7142857142857143,
    "f1": 0.8333333333333334
  },
  "claim_recall": {
    "tp": 3,
    "fp": 1,
    "fn": 1,
    "precision": 0.75,
    "recall": 0.75,
    "f1": 0.75
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Designing a File Storage Solution",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.7142857142857143,
    "f1": 0.8333333333333334
  },
  "claim_recall": {
    "tp": 3,
    "fp": 1,
    "fn": 1,
    "precision": 0.75,
    "recall": 0.75,
    "f1": 0.75
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Designing a File Storage Solution",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r2:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r3:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r4:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "today I'm starting a new design task",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "decision"
      }
    },
    {
      "claim": "[Designing a File Storage Solution]",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "condition": "Considering that our system will need to store a large number of supporting documents, reports, etc. in the future",
      "condition_attributes": {
        "claim_group": "b",
        "stance": "unknown"
      }
    },
    {
      "claim": "I will focus on comparing Azure Blob and AWS S3",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "decision"
      }
    },
    {
      "claim": "The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    },
    {
      "claim": "A preliminary selection recommendation report will be provided early next week",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 3,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r2",
      "condition",
      "r2:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "decision",
        "unknown"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 1,
    "fn": 3,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r2",
      "condition",
      "r2:basis1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "unknown",
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "AWS S3 has a slight advantage from the perspective of cost and ecosystem integration.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "Our other projects are also on AWS.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "Today, I will start designing the Bucket Policy and directory structure based on S3, for example, isolating by tenant and file type.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Ungrounded extraction

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 3,
    "precision": 1.0,
    "recall": 0.25,
    "f1": 0.4
  },
  "missing_nodes": [
    "r1:claim",
    "r1:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 8,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:time1",
    "r2:claim",
    "r2:condition1",
    "r3:claim",
    "r4:claim",
    "r4:method1",
    "r4:time1"
  ],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ],
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r4",
      "method",
      "r4:method1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Good morning everyone",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "time": "last Friday",
      "time_attributes": {
        "claim_group": "b",
        "stance": "unknown"
      }
    },
    {
      "claim": "From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "our other projects are also on AWS",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "Today, I will start designing the Bucket Policy and directory structure based on S3",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "decision"
      }
    },
    {
      "time": "Today",
      "time_attributes": {
        "claim_group": "d",
        "stance": "unknown"
      }
    },
    {
      "claim": "for example, isolating by tenant and file type",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 1,
    "fn": 0,
    "precision": 0.8,
    "recall": 1.0,
    "f1": 0.8888888888888888
  },
  "typed_edges": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "condition",
      "r2:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Good morning everyone",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ]
  ],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 1,
    "fn": 0,
    "precision": 0.8,
    "recall": 1.0,
    "f1": 0.8888888888888888
  },
  "typed_edges": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "condition",
      "r2:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Good morning everyone",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ]
  ],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": [
    {
      "node": "r4:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The complete technical design document (based on AWS S3) has been uploaded to Confluence.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "It includes three main parts: bucket permission policies, lifecycle rules, and recommended directory structure.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "@Mingzhi Li Boss Li, please review it.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "subject",
      "r2:subject1"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r3:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "subject",
      "r2:subject1"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r3:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Good morning everyone",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "regarding the file storage solution",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "the complete technical design document (based on AWS S3) has been uploaded to Confluence",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "It includes three main parts",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "bucket permission policies",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    },
    {
      "claim": "lifecycle rules",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    },
    {
      "claim": "recommended directory structure",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    },
    {
      "claim": "@Mingzhi Li Boss Li, please review it",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 3,
    "fp": 2,
    "fn": 0,
    "precision": 0.6,
    "recall": 1.0,
    "f1": 0.75
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "subject",
      "r2:subject1"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Good morning everyone",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    },
    {
      "row": 1,
      "role": "claim",
      "text": "regarding the file storage solution",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0,
    1
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": [
    {
      "node": "r2:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "observation",
        "unknown",
        "unknown",
        "unknown"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 3,
    "fp": 2,
    "fn": 0,
    "precision": 0.6,
    "recall": 1.0,
    "f1": 0.75
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "subject",
      "r2:subject1"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Good morning everyone",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    },
    {
      "row": 1,
      "role": "claim",
      "text": "regarding the file storage solution",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0,
    1
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": [
    {
      "node": "r2:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "unknown",
        "unknown",
        "unknown",
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The design is very comprehensive, especially the considerations for tenant data isolation and cost optimization.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "The proposal is approved and can be finalized.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.6,
    "f1": 0.75
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [
    "r1:claim",
    "r3:subject1"
  ],
  "missing_edges": [
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.6,
    "f1": 0.75
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [
    "r1:claim",
    "r3:subject1"
  ],
  "missing_edges": [
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "@Lujian Gao I've finished reviewing the document on the file storage solution",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The design is very comprehensive",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "especially the considerations for tenant data isolation and cost optimization",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "The proposal is approved",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    },
    {
      "claim": "can be finalized",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "our main security consideration is to prevent 'user enumeration attacks'",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "the feedback message should be consistent, such as 'If this email address is registered, you will receive an email containing a password reset link'",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "instead of directly prompting 'user does not exist'",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "Please ensure the UI copy adheres to this principle",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Ungrounded extraction

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 3,
    "precision": 1.0,
    "recall": 0.7,
    "f1": 0.8235294117647058
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 2,
    "fp": 4,
    "fn": 5,
    "precision": 0.3333333333333333,
    "recall": 0.2857142857142857,
    "f1": 0.3076923076923077
  },
  "missing_nodes": [
    "r1:condition1",
    "r2:condition1",
    "r2:condition2"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r2",
      "condition",
      "r2:condition2"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "method",
      "r2:method1"
    ],
    [
      "r1",
      "method",
      "r2:method2"
    ],
    [
      "r3",
      "method",
      "r2:method1"
    ],
    [
      "r3",
      "method",
      "r2:method2"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ],
    [
      "r1",
      "r3"
    ],
    [
      "r2",
      "r3"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r2:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 10,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 7,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:condition1",
    "r2:basis1",
    "r2:claim",
    "r2:condition1",
    "r2:condition2",
    "r2:method1",
    "r2:method2",
    "r3:claim",
    "r3:subject1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r2",
      "condition",
      "r2:condition2"
    ],
    [
      "r2",
      "method",
      "r2:method1"
    ],
    [
      "r2",
      "method",
      "r2:method2"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "@Yang Zhao Good question",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "unknown"
      }
    },
    {
      "claim": "our main security consideration is to prevent 'user enumeration attacks'",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "condition": "regardless of whether the email entered by the user exists or not",
      "condition_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    },
    {
      "claim": "the feedback message should be consistent",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    },
    {
      "claim": "such as 'If this email address is registered, you will receive an email containing a password reset link'",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    },
    {
      "claim": "instead of directly prompting 'user does not exist'",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    },
    {
      "claim": "Please ensure the UI copy adheres to this principle",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: ValueError: Ungrounded extraction

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.8,
    "f1": 0.8888888888888888
  },
  "claim_recall": {
    "tp": 3,
    "fp": 1,
    "fn": 0,
    "precision": 0.75,
    "recall": 1.0,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 3,
    "fp": 0,
    "fn": 4,
    "precision": 1.0,
    "recall": 0.42857142857142855,
    "f1": 0.6
  },
  "missing_nodes": [
    "r1:condition1",
    "r2:condition1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "@Yang Zhao Good question",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 10,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "claim_recall": {
    "tp": 0,
    "fp": 0,
    "fn": 3,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 7,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r1:condition1",
    "r2:basis1",
    "r2:claim",
    "r2:condition1",
    "r2:condition2",
    "r2:method1",
    "r2:method2",
    "r3:claim",
    "r3:subject1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r2",
      "condition",
      "r2:condition2"
    ],
    [
      "r2",
      "method",
      "r2:method1"
    ],
    [
      "r2",
      "method",
      "r2:method2"
    ],
    [
      "r3",
      "subject",
      "r3:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "please assess the scope of impact on the backend",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r2:recipient1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r2",
      "recipient",
      "r2:recipient1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r2:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r2:recipient1"
  ],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ],
    [
      "r2",
      "recipient",
      "r2:recipient1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r2:claim",
      "expected": [
        "decision"
      ],
      "predicted": [
        "proposal"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Email received",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "decision"
      }
    },
    {
      "subject": "all accounts marked as `ACCOUNT_STATUS_LOCKED`",
      "subject_attributes": {
        "claim_group": "b",
        "stance": "unknown"
      }
    },
    {
      "claim": "@Xinjie Li @Xuexin Yin, please assess the scope of impact on the backend",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "subject",
      "r1:condition1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Email received",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 1,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "condition",
      "r1:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "subject",
      "r1:condition1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Email received",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "defined as 'Explicit Status Alert Policy'",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "It is mainly used for scenarios where an account is locked",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "requiring explicit interruption of user operations and guidance to manual channels",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 2,
    "precision": 0.5,
    "recall": 0.3333333333333333,
    "f1": 0.4
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r2",
      "subject",
      "r2:subject1"
    ]
  ],
  "incorrect_edges": [
    [
      "r2",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [
    2
  ],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 1,
    "fn": 2,
    "precision": 0.5,
    "recall": 0.3333333333333333,
    "f1": 0.4
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r2",
      "subject",
      "r2:subject1"
    ]
  ],
  "incorrect_edges": [
    [
      "r2",
      "caveat",
      "r1:caveat1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [
    2
  ],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "defined as 'Explicit Status Alert Policy'",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "It is mainly used for scenarios where an account is locked",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "requiring explicit interruption of user operations",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "and guidance to manual channels",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r2",
      "subject",
      "r2:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    2
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 5,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.3333333333333333,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "condition",
      "r2:condition1"
    ],
    [
      "r2",
      "subject",
      "r2:subject1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [
    2
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "This strategy will be handled by `ExplicitStateAlertModule`",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "the parameter `halt_downstream_triggers` is set to `true`",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r4:caveat1"
  ],
  "missing_edges": [
    [
      "r4",
      "caveat",
      "r4:caveat1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r4:claim",
      "expected": [
        "question"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 2,
    "precision": 1.0,
    "recall": 0.6666666666666666,
    "f1": 0.8
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 2,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim",
    "r4:caveat1"
  ],
  "missing_edges": [
    [
      "r4",
      "caveat",
      "r4:caveat1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r4:claim",
      "expected": [
        "question"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Received",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "I've reviewed the document",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "This strategy will be handled by `ExplicitStateAlertModule`",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "the parameter `halt_downstream_triggers` is set to `true`",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "observation"
      }
    },
    {
      "claim": "right?",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "question"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 1,
    "fn": 0,
    "precision": 0.8,
    "recall": 1.0,
    "f1": 0.8888888888888888
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r4",
      "condition",
      "r4:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Received",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ]
  ],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": [
    {
      "node": "r4:claim",
      "expected": [
        "question"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 6,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 1,
    "fn": 0,
    "precision": 0.8,
    "recall": 1.0,
    "f1": 0.8888888888888888
  },
  "typed_edges": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r4",
      "condition",
      "r4:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Received",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r2",
      "r3"
    ]
  ],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": [
    {
      "node": "r4:claim",
      "expected": [
        "question"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r4:caveat1",
      "expected": [
        "observation",
        "uncertainty",
        "question"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "This is to avoid sending users redundant or potentially confusing automated messages.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [
    "r1:claim"
  ],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "claim_recall": {
    "tp": 1,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.5,
    "f1": 0.6666666666666666
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [
    "r1:claim"
  ],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "your understanding is completely correct",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "This is to avoid sending users redundant or potentially confusing automated messages",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 0,
    "precision": null,
    "recall": null,
    "f1": null
  },
  "missing_nodes": [],
  "missing_edges": [],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "I plan to complete the static data integration this morning to ensure the charts render correctly.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it.",
      "claim_attributes": {
        "claim_group": "2",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.875,
    "f1": 0.9333333333333333
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim"
  ],
  "missing_edges": [
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r2",
      "time",
      "r2:time1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r2:claim",
      "expected": [
        "proposal",
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r3:claim",
      "expected": [
        "proposal",
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r4:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 7,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.875,
    "f1": 0.9333333333333333
  },
  "claim_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 1,
    "precision": 1.0,
    "recall": 0.75,
    "f1": 0.8571428571428571
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 4,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [
    "r1:claim"
  ],
  "missing_edges": [
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r2",
      "time",
      "r2:time1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r2:claim",
      "expected": [
        "proposal",
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r3:claim",
      "expected": [
        "proposal",
        "decision"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r4:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Received, thanks a lot!",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "The data structure looks very clear",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "observation"
      }
    },
    {
      "claim": "I plan to complete the static data integration this morning",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "proposal"
      }
    },
    {
      "time": "this morning",
      "time_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    },
    {
      "claim": "to ensure the charts render correctly",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    },
    {
      "claim": "In the afternoon, I'll start researching dynamic refresh solutions",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "proposal"
      }
    },
    {
      "time": "in the afternoon",
      "time_attributes": {
        "claim_group": "d",
        "stance": "unknown"
      }
    },
    {
      "claim": "initially considering WebSocket if the backend supports it",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "proposal"
      }
    },
    {
      "subject": "the backend",
      "subject_attributes": {
        "claim_group": "d",
        "stance": "unknown"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 1,
    "fn": 0,
    "precision": 0.8,
    "recall": 1.0,
    "f1": 0.8888888888888888
  },
  "typed_edges": {
    "tp": 2,
    "fp": 2,
    "fn": 2,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r4",
      "time",
      "r3:time1"
    ],
    [
      "unbound:d",
      "subject",
      "unmatched:8"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Received, thanks a lot!",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    },
    {
      "row": 8,
      "role": "subject",
      "text": "the backend",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 8,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 1,
    "fn": 0,
    "precision": 0.8,
    "recall": 1.0,
    "f1": 0.8888888888888888
  },
  "typed_edges": {
    "tp": 2,
    "fp": 2,
    "fn": 2,
    "precision": 0.5,
    "recall": 0.5,
    "f1": 0.5
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r2",
      "basis",
      "r2:basis1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ]
  ],
  "incorrect_edges": [
    [
      "r4",
      "time",
      "r3:time1"
    ],
    [
      "unbound:c:cdaf7df96d5a462a0157da4c",
      "subject",
      "unmatched:7"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Received, thanks a lot!",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    },
    {
      "row": 7,
      "role": "subject",
      "text": "the backend",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": [
    {
      "node": "r2:claim",
      "expected": [
        "proposal",
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "WebSocket is the best solution",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "our message push service isn't fully ready yet",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    },
    {
      "claim": "This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "proposal"
      }
    },
    {
      "claim": "Once the WebSocket service is stable later, we can upgrade it uniformly",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "proposal"
      }
    },
    {
      "claim": "This way, we can avoid blocking your current task",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "proposal"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 3,
    "fn": 4,
    "precision": 0.25,
    "recall": 0.2,
    "f1": 0.2222222222222222
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r3",
      "basis",
      "r3:basis1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "method",
      "r3:method1"
    ],
    [
      "r2",
      "method",
      "r3:method1"
    ],
    [
      "r4",
      "method",
      "r3:method1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ],
    [
      "r1",
      "r3"
    ],
    [
      "r1",
      "r4"
    ],
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 4,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 1,
    "fp": 3,
    "fn": 4,
    "precision": 0.25,
    "recall": 0.2,
    "f1": 0.2222222222222222
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r3",
      "basis",
      "r3:basis1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "method",
      "r3:method1"
    ],
    [
      "r2",
      "method",
      "r3:method1"
    ],
    [
      "r4",
      "method",
      "r3:method1"
    ]
  ],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ],
    [
      "r1",
      "r3"
    ],
    [
      "r1",
      "r4"
    ],
    [
      "r2",
      "r3"
    ],
    [
      "r2",
      "r4"
    ],
    [
      "r3",
      "r4"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "observation",
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r2:claim",
      "expected": [
        "observation"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r3:claim",
      "expected": [
        "proposal",
        "decision"
      ],
      "predicted": [
        "unknown"
      ]
    },
    {
      "node": "r4:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Great plan",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "WebSocket is the best solution",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "decision"
      }
    },
    {
      "condition": "our message push service isn't fully ready yet",
      "condition_attributes": {
        "claim_group": "b",
        "stance": "unknown"
      }
    },
    {
      "claim": "This task can be implemented using polling for now",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    },
    {
      "condition": "by requesting the interface every 10 seconds",
      "condition_attributes": {
        "claim_group": "c",
        "stance": "unknown"
      }
    },
    {
      "claim": "Once the WebSocket service is stable later",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "unknown"
      }
    },
    {
      "claim": "we can upgrade it uniformly",
      "claim_attributes": {
        "claim_group": "d",
        "stance": "proposal"
      }
    },
    {
      "claim": "This way, we can avoid blocking your current task",
      "claim_attributes": {
        "claim_group": "e",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 3,
    "fp": 2,
    "fn": 1,
    "precision": 0.6,
    "recall": 0.75,
    "f1": 0.6666666666666666
  },
  "typed_edges": {
    "tp": 0,
    "fp": 2,
    "fn": 5,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r3",
      "basis",
      "r3:basis1"
    ],
    [
      "r3",
      "method",
      "r3:method1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r2:claim"
    ],
    [
      "r3",
      "condition",
      "r3:method1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Great plan",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0,
    5
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 9,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 3,
    "fp": 2,
    "fn": 1,
    "precision": 0.6,
    "recall": 0.75,
    "f1": 0.6666666666666666
  },
  "typed_edges": {
    "tp": 0,
    "fp": 2,
    "fn": 5,
    "precision": 0.0,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r3",
      "basis",
      "r3:basis1"
    ],
    [
      "r3",
      "method",
      "r3:method1"
    ],
    [
      "r3",
      "time",
      "r3:time1"
    ],
    [
      "r4",
      "condition",
      "r4:condition1"
    ],
    [
      "r4",
      "time",
      "r4:time1"
    ]
  ],
  "incorrect_edges": [
    [
      "r1",
      "condition",
      "r2:claim"
    ],
    [
      "r3",
      "condition",
      "r3:method1"
    ]
  ],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Great plan",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0,
    5
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": [
    {
      "node": "r4:claim",
      "expected": [
        "proposal"
      ],
      "predicted": [
        "unknown"
      ]
    }
  ]
}
```

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

### simple

```json
{
  "extractions": [
    {
      "claim": "I'll use the polling solution for now, and I'll adjust the plan.",
      "claim_attributes": {
        "claim_group": "1",
        "stance": "observation"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r2:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [],
  "extra_claim_rows": [],
  "overmerged_record_pairs": [
    [
      "r1",
      "r2"
    ]
  ],
  "boilerplate_rows": [],
  "stance_wrong": [
    {
      "node": "r1:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "observation"
      ]
    },
    {
      "node": "r2:claim",
      "expected": [
        "decision",
        "proposal"
      ],
      "predicted": [
        "observation"
      ]
    }
  ]
}
```

### ours

```json
{
  "extractions": [
    {
      "claim": "Okay, Boss Li, understood",
      "claim_attributes": {
        "claim_group": "a",
        "stance": "observation"
      }
    },
    {
      "claim": "I'll use the polling solution for now",
      "claim_attributes": {
        "claim_group": "b",
        "stance": "decision"
      }
    },
    {
      "claim": "I'll adjust the plan",
      "claim_attributes": {
        "claim_group": "c",
        "stance": "decision"
      }
    }
  ]
}
```

컴파일 오류: None

**raw**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Okay, Boss Li, understood",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

**compiled**
```json
{
  "complete": false,
  "content_recall": {
    "tp": 3,
    "fp": 0,
    "fn": 0,
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  },
  "claim_recall": {
    "tp": 2,
    "fp": 1,
    "fn": 0,
    "precision": 0.6666666666666666,
    "recall": 1.0,
    "f1": 0.8
  },
  "typed_edges": {
    "tp": 0,
    "fp": 0,
    "fn": 1,
    "precision": null,
    "recall": 0.0,
    "f1": 0.0
  },
  "missing_nodes": [],
  "missing_edges": [
    [
      "r1",
      "time",
      "r1:time1"
    ]
  ],
  "incorrect_edges": [],
  "extra_rows": [
    {
      "row": 0,
      "role": "claim",
      "text": "Okay, Boss Li, understood",
      "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
    }
  ],
  "extra_claim_rows": [
    0
  ],
  "overmerged_record_pairs": [],
  "boilerplate_rows": [
    0
  ],
  "stance_wrong": []
}
```

