# Records 층화 진단: 원문과 단계별 결과

Job 122970. 정답과 채점기는 실행 전 고정. 원출력·부분 역할 판정이며 전체 QA 정확도가 아님.

## e01-full — balanced_synthetic / easy / full

Source: `33abbca0dc91dbb59f467b14`

For chilled parcels, use liner K6 because the foam prevents condensation.

고정한 요구사항:

```json
{
  "id": "e01-full",
  "core": "use liner K6",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "chilled parcels",
      "available": true
    },
    {
      "role": "basis",
      "text": "the foam prevents condensation",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:db167d54e4a5a8b4470f635b",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:ff466861d37dbdefc80e732c",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e01-partial — balanced_synthetic / easy / partial

Source: `6fea6f425cd00d4746adb023`

For chilled parcels, use liner K6.

고정한 요구사항:

```json
{
  "id": "e01-partial",
  "core": "use liner K6",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "chilled parcels",
      "available": true
    },
    {
      "role": "basis",
      "text": "the foam prevents condensation",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:a080cecdf21466fde767c8d5",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:dccd0846169c8ea9835d1b44",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e01-none — balanced_synthetic / easy / none

Source: `97200ceeaf92691fde3c3f0a`

use liner K6.

고정한 요구사항:

```json
{
  "id": "e01-none",
  "core": "use liner K6",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "chilled parcels",
      "available": false
    },
    {
      "role": "basis",
      "text": "the foam prevents condensation",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:d05c1511b19964a4ae54cad3",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:e27354e39890eaba37a14d1f",
        "slots": [
          {
            "role": "condition",
            "text": "chilled parcels",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the foam prevents condensation",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e02-full — balanced_synthetic / easy / full

Source: `709f8ae378397a731a47ec82`

close gate R8 on Thursday because the hinge needs repair.

고정한 요구사항:

```json
{
  "id": "e02-full",
  "core": "close gate R8",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "on Thursday",
      "available": true
    },
    {
      "role": "basis",
      "text": "the hinge needs repair",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: ValueError: Context has claim stance; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "on Thursday",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the hinge needs repair",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "time",
            "text": "on Thursday",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the hinge needs repair",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:87a2f1fa75d9a78c429fdec2",
        "slots": [
          {
            "role": "time",
            "text": "on Thursday",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the hinge needs repair",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## e02-partial — balanced_synthetic / easy / partial

Source: `925538e36ab8cf414f9cb883`

close gate R8 because the hinge needs repair.

고정한 요구사항:

```json
{
  "id": "e02-partial",
  "core": "close gate R8",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "on Thursday",
      "available": false
    },
    {
      "role": "basis",
      "text": "the hinge needs repair",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "on Thursday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the hinge needs repair",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:783acf798f0ecd2f1c0f1cae",
        "slots": [
          {
            "role": "time",
            "text": "on Thursday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the hinge needs repair",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "time",
            "text": "on Thursday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the hinge needs repair",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:59d7ca5167e08611bd5a289a",
        "slots": [
          {
            "role": "time",
            "text": "on Thursday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the hinge needs repair",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## e02-none — balanced_synthetic / easy / none

Source: `801945abc96c000f57f6e92a`

close gate R8.

고정한 요구사항:

```json
{
  "id": "e02-none",
  "core": "close gate R8",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "on Thursday",
      "available": false
    },
    {
      "role": "basis",
      "text": "the hinge needs repair",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'annotated'}

원출력:
```json
{
  "extractions": []
}
```

고정 채점:
```json
{
  "raw": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "time",
            "text": "on Thursday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the hinge needs repair",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:bbf614100a6465aab78a14ac",
        "slots": [
          {
            "role": "time",
            "text": "on Thursday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the hinge needs repair",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e03-full — balanced_synthetic / easy / full

Source: `26e96d281e3e856dedc95b7e`

For cracked containers, do not ship kit M3 because the seal failed inspection.

고정한 요구사항:

```json
{
  "id": "e03-full",
  "core": "do not ship kit M3",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "cracked containers",
      "available": true
    },
    {
      "role": "basis",
      "text": "the seal failed inspection",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:b35656bcfaa0db101c637649",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:268c7e69adbb3c169709f4e3",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e03-partial — balanced_synthetic / easy / partial

Source: `02b5161b879fac5c3943fee0`

For cracked containers, do not ship kit M3.

고정한 요구사항:

```json
{
  "id": "e03-partial",
  "core": "do not ship kit M3",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "cracked containers",
      "available": true
    },
    {
      "role": "basis",
      "text": "the seal failed inspection",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:fa2550184c230db275a23c3c",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:a255f8ed01def42f1a44ad96",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e03-none — balanced_synthetic / easy / none

Source: `74738fb6b8b3b19b518bd96e`

do not ship kit M3.

고정한 요구사항:

```json
{
  "id": "e03-none",
  "core": "do not ship kit M3",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "cracked containers",
      "available": false
    },
    {
      "role": "basis",
      "text": "the seal failed inspection",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:7b410ffd22e621edd6b5004e",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:4bed299bab8230109d4f7cce",
        "slots": [
          {
            "role": "condition",
            "text": "cracked containers",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the seal failed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e04-full — balanced_synthetic / easy / full

Source: `d764923f575d0292ebbbffa2`

For inland stations, we might trial paint Q9. This trial is not approved.

고정한 요구사항:

```json
{
  "id": "e04-full",
  "core": "we might trial paint Q9",
  "stance": "proposal",
  "slots": [
    {
      "role": "condition",
      "text": "inland stations",
      "available": true
    },
    {
      "role": "claim",
      "text": "This trial is not approved.",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:23ba5d6f22b58d4e7bb11a4b",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:601e21dde647d83ff4f93ad0",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## e04-partial — balanced_synthetic / easy / partial

Source: `a8989ff9f5cbe9dadc7c475b`

we might trial paint Q9. This trial is not approved.

고정한 요구사항:

```json
{
  "id": "e04-partial",
  "core": "we might trial paint Q9",
  "stance": "proposal",
  "slots": [
    {
      "role": "condition",
      "text": "inland stations",
      "available": false
    },
    {
      "role": "claim",
      "text": "This trial is not approved.",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:47764a04cd2d1dac1da47a21",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:bb0ccf384099ff901e678595",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## e04-none — balanced_synthetic / easy / none

Source: `668ff2dbdae195e6f8d1967f`

we might trial paint Q9.

고정한 요구사항:

```json
{
  "id": "e04-none",
  "core": "we might trial paint Q9",
  "stance": "proposal",
  "slots": [
    {
      "role": "condition",
      "text": "inland stations",
      "available": false
    },
    {
      "role": "claim",
      "text": "This trial is not approved.",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:22b792657ec75b90020d621e",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:911de583e2563ba7e4fe91bc",
        "slots": [
          {
            "role": "condition",
            "text": "inland stations",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This trial is not approved.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e05-full — balanced_synthetic / easy / full

Source: `694c889970229e4061e0b4d4`

Recorded event time: on Tuesday. the sensor check is complete for firmware 6.

고정한 요구사항:

```json
{
  "id": "e05-full",
  "core": "the sensor check is complete",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "on Tuesday",
      "available": true
    },
    {
      "role": "condition",
      "text": "firmware 6",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:f5def13d5e07e4e07c2e1b01",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:a78b4276f919be87077cf7f3",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## e05-partial — balanced_synthetic / easy / partial

Source: `63b0dc798b1b6b19caf5f134`

Recorded event time: on Tuesday. the sensor check is complete.

고정한 요구사항:

```json
{
  "id": "e05-partial",
  "core": "the sensor check is complete",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "on Tuesday",
      "available": true
    },
    {
      "role": "condition",
      "text": "firmware 6",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:f916b8b6ccfbae1f853b2932",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:12ff9b631695fa5367620102",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e05-none — balanced_synthetic / easy / none

Source: `68d5db1a3a6ad6422d2040e6`

the sensor check is complete.

고정한 요구사항:

```json
{
  "id": "e05-none",
  "core": "the sensor check is complete",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "on Tuesday",
      "available": false
    },
    {
      "role": "condition",
      "text": "firmware 6",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:9ee7257ab779d29a165d5e81",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:9ee7257ab779d29a165d5e81",
        "slots": [
          {
            "role": "time",
            "text": "on Tuesday",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "firmware 6",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e06-full — balanced_synthetic / easy / full

Source: `d0fcf930f9524f0f08399148`

For dry rooms, I suspect relay P4 may last 80 days. This estimate is untested.

고정한 요구사항:

```json
{
  "id": "e06-full",
  "core": "I suspect relay P4 may last 80 days",
  "stance": "uncertainty",
  "slots": [
    {
      "role": "condition",
      "text": "dry rooms",
      "available": true
    },
    {
      "role": "claim",
      "text": "This estimate is untested.",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:2c4f8d1c37f9efcfeaf0e822",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:f6a566f58b7f98ab29e2c224",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e06-partial — balanced_synthetic / easy / partial

Source: `c628de4a11483d61a9204676`

I suspect relay P4 may last 80 days. This estimate is untested.

고정한 요구사항:

```json
{
  "id": "e06-partial",
  "core": "I suspect relay P4 may last 80 days",
  "stance": "uncertainty",
  "slots": [
    {
      "role": "condition",
      "text": "dry rooms",
      "available": false
    },
    {
      "role": "claim",
      "text": "This estimate is untested.",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:fec3e32425a57b9273dd04b0",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:2d0413d58b6d6f02e4863eae",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## e06-none — balanced_synthetic / easy / none

Source: `566f53022fec16660340d521`

I suspect relay P4 may last 80 days.

고정한 요구사항:

```json
{
  "id": "e06-none",
  "core": "I suspect relay P4 may last 80 days",
  "stance": "uncertainty",
  "slots": [
    {
      "role": "condition",
      "text": "dry rooms",
      "available": false
    },
    {
      "role": "claim",
      "text": "This estimate is untested.",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:0ffaa8896fa9a8f51f9f3400",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:069ead9269cc4c6917bc7841",
        "slots": [
          {
            "role": "condition",
            "text": "dry rooms",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This estimate is untested.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## m01-full — balanced_synthetic / medium / full

Source: `d4246e285cafe8eae5f385cc`

This survey decision applies to sector D2. The cabinet label is copper. we postpone the gravel survey because the access bridge is closed.

고정한 요구사항:

```json
{
  "id": "m01-full",
  "core": "we postpone the gravel survey",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "sector D2",
      "available": true
    },
    {
      "role": "basis",
      "text": "the access bridge is closed",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:e943a7470db7fb0daa073aa5",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: ValueError: Orphaned context group; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m01-partial — balanced_synthetic / medium / partial

Source: `aa89de85e1e7b4d439b8b949`

This survey decision applies to sector D2. The cabinet label is copper. we postpone the gravel survey.

고정한 요구사항:

```json
{
  "id": "m01-partial",
  "core": "we postpone the gravel survey",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "sector D2",
      "available": true
    },
    {
      "role": "basis",
      "text": "the access bridge is closed",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:900ac57a4bd618991c722227",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: ValueError: Orphaned context group; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m01-none — balanced_synthetic / medium / none

Source: `5ed1d90a243e42fa026cf898`

The cabinet label is copper. we postpone the gravel survey.

고정한 요구사항:

```json
{
  "id": "m01-none",
  "core": "we postpone the gravel survey",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "sector D2",
      "available": false
    },
    {
      "role": "basis",
      "text": "the access bridge is closed",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:b1c1f50d1b6e6a950059bff6",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:f49adc237b084a5d43c5bdfd",
        "slots": [
          {
            "role": "condition",
            "text": "sector D2",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the access bridge is closed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## m02-full — balanced_synthetic / medium / full

Source: `3bd9438d4fd1752dbee0ca65`

Timing for the following beacon instruction: after the morning inspection. The antenna colour remains white. switch the beacon to standby because the battery is leaking.

고정한 요구사항:

```json
{
  "id": "m02-full",
  "core": "switch the beacon to standby",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "after the morning inspection",
      "available": true
    },
    {
      "role": "basis",
      "text": "the battery is leaking",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "3",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:5ef0d6e243a45494eddd9a71",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:7c7110cae64e1af12a8c19fc",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m02-partial — balanced_synthetic / medium / partial

Source: `5557e3d2bc40298994abc274`

The antenna colour remains white. switch the beacon to standby because the battery is leaking.

고정한 요구사항:

```json
{
  "id": "m02-partial",
  "core": "switch the beacon to standby",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "after the morning inspection",
      "available": false
    },
    {
      "role": "basis",
      "text": "the battery is leaking",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:18cde0c266bbfd5d0dbb2759",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:4c476b37f02d86e58e61f8a5",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m02-none — balanced_synthetic / medium / none

Source: `45e125beb1e51de31e6fc861`

The antenna colour remains white. switch the beacon to standby.

고정한 요구사항:

```json
{
  "id": "m02-none",
  "core": "switch the beacon to standby",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "after the morning inspection",
      "available": false
    },
    {
      "role": "basis",
      "text": "the battery is leaking",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:fb1fd901d4e0d4e7681e2a1d",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:0ef4cd7eb1278f0a85359188",
        "slots": [
          {
            "role": "time",
            "text": "after the morning inspection",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the battery is leaking",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## m03-full — balanced_synthetic / medium / full

Source: `17059c178deaf784e8411521`

The following release instruction applies to saline batches. do not release batch U5 because the residue test failed. Freshwater batches remain eligible for release.

고정한 요구사항:

```json
{
  "id": "m03-full",
  "core": "do not release batch U5",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "saline batches",
      "available": true
    },
    {
      "role": "basis",
      "text": "the residue test failed",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:3e3a959e162b087156ea6846",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:dd1e720dc25a902f5c515a6a",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m03-partial — balanced_synthetic / medium / partial

Source: `ca86e4fed815e881bbb73c14`

The following release instruction applies to saline batches. do not release batch U5. Freshwater batches remain eligible for release.

고정한 요구사항:

```json
{
  "id": "m03-partial",
  "core": "do not release batch U5",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "saline batches",
      "available": true
    },
    {
      "role": "basis",
      "text": "the residue test failed",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:bb14d36c956e82022ecacd02",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:9ffe8ba8819949491d11e894",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## m03-none — balanced_synthetic / medium / none

Source: `eb9f29530f2bc3d522f4dcc8`

do not release batch U5. Freshwater batches remain eligible for release.

고정한 요구사항:

```json
{
  "id": "m03-none",
  "core": "do not release batch U5",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "saline batches",
      "available": false
    },
    {
      "role": "basis",
      "text": "the residue test failed",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:f920503ada88ff66010e3623",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:f920503ada88ff66010e3623",
        "slots": [
          {
            "role": "condition",
            "text": "saline batches",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the residue test failed",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## m04-full — balanced_synthetic / medium / full

Source: `0d750c235cc5f5779be97aeb`

Scope of the filter pilot: remote clinics. The spare tubing is blue. we could pilot filter J2. This pilot is a suggestion, not an authorization.

고정한 요구사항:

```json
{
  "id": "m04-full",
  "core": "we could pilot filter J2",
  "stance": "proposal",
  "slots": [
    {
      "role": "condition",
      "text": "remote clinics",
      "available": true
    },
    {
      "role": "claim",
      "text": "This pilot is a suggestion, not an authorization.",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:539758412eda10f3780625d0",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:a2f2864fb55b48a663aa0379",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m04-partial — balanced_synthetic / medium / partial

Source: `c186a128c7866ca21efe5ce4`

The spare tubing is blue. we could pilot filter J2. This pilot is a suggestion, not an authorization.

고정한 요구사항:

```json
{
  "id": "m04-partial",
  "core": "we could pilot filter J2",
  "stance": "proposal",
  "slots": [
    {
      "role": "condition",
      "text": "remote clinics",
      "available": false
    },
    {
      "role": "claim",
      "text": "This pilot is a suggestion, not an authorization.",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "group2",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:8445f51afde2ecdc7ab51b35",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:0f98e718ae042befa61e988c",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m04-none — balanced_synthetic / medium / none

Source: `ff1dc03758f2c348b5760225`

The spare tubing is blue. we could pilot filter J2.

고정한 요구사항:

```json
{
  "id": "m04-none",
  "core": "we could pilot filter J2",
  "stance": "proposal",
  "slots": [
    {
      "role": "condition",
      "text": "remote clinics",
      "available": false
    },
    {
      "role": "claim",
      "text": "This pilot is a suggestion, not an authorization.",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:cc05af244f1518f4a9fdd9e3",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:ff97883a965a7ad077665207",
        "slots": [
          {
            "role": "condition",
            "text": "remote clinics",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This pilot is a suggestion, not an authorization.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## m05-full — balanced_synthetic / medium / full

Source: `325f038abd94e5f86e44e93d`

The calibration event occurred on Friday afternoon. The office clock was repaired. the valve calibration finished on bench T7.

고정한 요구사항:

```json
{
  "id": "m05-full",
  "core": "the valve calibration finished",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "on Friday afternoon",
      "available": true
    },
    {
      "role": "condition",
      "text": "bench T7",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:ae4e8523b6625c716c66a6b8",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:e3cdb5888e3be6c90647a45f",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m05-partial — balanced_synthetic / medium / partial

Source: `8b37462b2d1ffdee37d08519`

The calibration event occurred on Friday afternoon. The office clock was repaired. the valve calibration finished.

고정한 요구사항:

```json
{
  "id": "m05-partial",
  "core": "the valve calibration finished",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "on Friday afternoon",
      "available": true
    },
    {
      "role": "condition",
      "text": "bench T7",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "3",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:acbab6f01d13bfc275dceac1",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:d69805d5c053e5f991ed4ba0",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m05-none — balanced_synthetic / medium / none

Source: `c69146fee259c2e07e827f91`

The office clock was repaired. the valve calibration finished.

고정한 요구사항:

```json
{
  "id": "m05-none",
  "core": "the valve calibration finished",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "on Friday afternoon",
      "available": false
    },
    {
      "role": "condition",
      "text": "bench T7",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:6288b6c46fe4d2f62d25a372",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:7c426de26106558be91629d8",
        "slots": [
          {
            "role": "time",
            "text": "on Friday afternoon",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "bench T7",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## m06-full — balanced_synthetic / medium / full

Source: `84b80190b326000dbfec164c`

Operating scope of this estimate: under reduced load. The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.

고정한 요구사항:

```json
{
  "id": "m06-full",
  "core": "I suspect drive L4 may reach 70 cycles",
  "stance": "uncertainty",
  "slots": [
    {
      "role": "condition",
      "text": "under reduced load",
      "available": true
    },
    {
      "role": "claim",
      "text": "No measurement supports this estimate yet.",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:0f21fade7105f5c2872b004a",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:7b3f50b1eb1c72987b551650",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## m06-partial — balanced_synthetic / medium / partial

Source: `9dc93469ba851b9facbaf1e5`

The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.

고정한 요구사항:

```json
{
  "id": "m06-partial",
  "core": "I suspect drive L4 may reach 70 cycles",
  "stance": "uncertainty",
  "slots": [
    {
      "role": "condition",
      "text": "under reduced load",
      "available": false
    },
    {
      "role": "claim",
      "text": "No measurement supports this estimate yet.",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:a80d003a314a6fc592fbf6cb",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:f8c5789d536e6e146c4d1b90",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## m06-none — balanced_synthetic / medium / none

Source: `42c88617812e2f691d3bada8`

The procurement task is complete. I suspect drive L4 may reach 70 cycles.

고정한 요구사항:

```json
{
  "id": "m06-none",
  "core": "I suspect drive L4 may reach 70 cycles",
  "stance": "uncertainty",
  "slots": [
    {
      "role": "condition",
      "text": "under reduced load",
      "available": false
    },
    {
      "role": "claim",
      "text": "No measurement supports this estimate yet.",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:ab0a6f5ddb4c10b62f791fed",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:58e12f8250f155ca8ea60247",
        "slots": [
          {
            "role": "condition",
            "text": "under reduced load",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "No measurement supports this estimate yet.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## h01-full — balanced_synthetic / hard / full

Source: `3b074ee68ba0096b48e973b3`

Scope of the compressor instruction: pressure above 9 bar. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4 because its casing has fractured. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.

고정한 요구사항:

```json
{
  "id": "h01-full",
  "core": "halt compressor Z4",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "pressure above 9 bar",
      "available": true
    },
    {
      "role": "basis",
      "text": "its casing has fractured",
      "available": true
    }
  ],
  "forbidden": [
    "below 1 bar",
    "the buffer is empty"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "6",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:184c8e912d8d265e567090bf",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "f",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:53795a87e3e4f12cfeccbeac",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h01-partial — balanced_synthetic / hard / partial

Source: `69eba89e50bdbdb2eea03896`

Scope of the compressor instruction: pressure above 9 bar. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.

고정한 요구사항:

```json
{
  "id": "h01-partial",
  "core": "halt compressor Z4",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "pressure above 9 bar",
      "available": true
    },
    {
      "role": "basis",
      "text": "its casing has fractured",
      "available": false
    }
  ],
  "forbidden": [
    "below 1 bar",
    "the buffer is empty"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "6",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:8fe19cae06baea0d8f031f21",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "f",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:9fadf60148424474c03b151b",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h01-none — balanced_synthetic / hard / none

Source: `d2bb5fd77d5625c88f17b02d`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.

고정한 요구사항:

```json
{
  "id": "h01-none",
  "core": "halt compressor Z4",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "pressure above 9 bar",
      "available": false
    },
    {
      "role": "basis",
      "text": "its casing has fractured",
      "available": false
    }
  ],
  "forbidden": [
    "below 1 bar",
    "the buffer is empty"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "5",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:0765f91e0a8e37979495185f",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "e",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:dee22159307223f102d3f196",
        "slots": [
          {
            "role": "condition",
            "text": "pressure above 9 bar",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "its casing has fractured",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## h02-full — balanced_synthetic / hard / full

Source: `571e3e7db5473ea0837ab6b1`

The time of the compass instruction is at 14:20. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test because the replacement mount passed inspection. Independently, the camera check begins at 14:20 because its lens is clean.

고정한 요구사항:

```json
{
  "id": "h02-full",
  "core": "resume the compass test",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "at 14:20",
      "available": true
    },
    {
      "role": "basis",
      "text": "the replacement mount passed inspection",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "6",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:b613ff3b4be10f2be88157cb",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: ValueError: Ambiguous repeated context span; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "f",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h02-partial — balanced_synthetic / hard / partial

Source: `2d83d8aa7b1dc6060ba52a53`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test because the replacement mount passed inspection. Independently, the camera check begins at 14:20 because its lens is clean.

고정한 요구사항:

```json
{
  "id": "h02-partial",
  "core": "resume the compass test",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "at 14:20",
      "available": false
    },
    {
      "role": "basis",
      "text": "the replacement mount passed inspection",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:61b5bae2be139be8511da89a",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "e",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:247b6e88e49a24d254ac926f",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h02-none — balanced_synthetic / hard / none

Source: `c3e8aeb6e6d5603876c40e1b`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test. Independently, the camera check begins at 14:20 because its lens is clean.

고정한 요구사항:

```json
{
  "id": "h02-none",
  "core": "resume the compass test",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "at 14:20",
      "available": false
    },
    {
      "role": "basis",
      "text": "the replacement mount passed inspection",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "5",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:92be3062dcb48dec33c5b4a5",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "e",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:6040019172ff3ef135631835",
        "slots": [
          {
            "role": "time",
            "text": "at 14:20",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the replacement mount passed inspection",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## h03-full — balanced_synthetic / hard / full

Source: `3ae3f11ae8d2bdbb32b2471d`

The map instruction below concerns commercial reuse. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map because the licence excludes commercial distribution. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.

고정한 요구사항:

```json
{
  "id": "h03-full",
  "core": "do not publish the terrain map",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "commercial reuse",
      "available": true
    },
    {
      "role": "basis",
      "text": "the licence excludes commercial distribution",
      "available": true
    }
  ],
  "forbidden": [
    "classroom teaching",
    "the teacher granted permission"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:014a9732025ed763058a2f6b",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "f",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:8be360a0afe07aab06b02399",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h03-partial — balanced_synthetic / hard / partial

Source: `40685e892acad37dacfb941f`

The map instruction below concerns commercial reuse. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.

고정한 요구사항:

```json
{
  "id": "h03-partial",
  "core": "do not publish the terrain map",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "commercial reuse",
      "available": true
    },
    {
      "role": "basis",
      "text": "the licence excludes commercial distribution",
      "available": false
    }
  ],
  "forbidden": [
    "classroom teaching",
    "the teacher granted permission"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:26e93706ac6cecbcefcbb4a7",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "f",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:29d77d70eb82c29553d32e93",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h03-none — balanced_synthetic / hard / none

Source: `c279181461b20f2f1c669e7d`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.

고정한 요구사항:

```json
{
  "id": "h03-none",
  "core": "do not publish the terrain map",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "commercial reuse",
      "available": false
    },
    {
      "role": "basis",
      "text": "the licence excludes commercial distribution",
      "available": false
    }
  ],
  "forbidden": [
    "classroom teaching",
    "the teacher granted permission"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:895673e7417b0154b780920b",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "e",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:4a70e8a1b8d90b073e52d5ce",
        "slots": [
          {
            "role": "condition",
            "text": "commercial reuse",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "the licence excludes commercial distribution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## h04-full — balanced_synthetic / hard / full

Source: `a33e17f2ba65363cebfcd799`

The pack trial applies to desert depots. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. This proposed trial has no deployment approval. Independently, the warehouse rollout is approved.

고정한 요구사항:

```json
{
  "id": "h04-full",
  "core": "we might trial pack G8",
  "stance": "proposal",
  "slots": [
    {
      "role": "condition",
      "text": "desert depots",
      "available": true
    },
    {
      "role": "claim",
      "text": "This proposed trial has no deployment approval.",
      "available": true
    }
  ],
  "forbidden": [
    "the warehouse rollout is approved"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "6",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:b2466247515d53274b2779dd",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "f",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:aa0ddc477c6260f5e6ff6ead",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h04-partial — balanced_synthetic / hard / partial

Source: `4d01cf1a2d288356cd77a2ad`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. This proposed trial has no deployment approval. Independently, the warehouse rollout is approved.

고정한 요구사항:

```json
{
  "id": "h04-partial",
  "core": "we might trial pack G8",
  "stance": "proposal",
  "slots": [
    {
      "role": "condition",
      "text": "desert depots",
      "available": false
    },
    {
      "role": "claim",
      "text": "This proposed trial has no deployment approval.",
      "available": true
    }
  ],
  "forbidden": [
    "the warehouse rollout is approved"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:6e279005f7860fe9c71ad543",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "e",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:83f52883669becc19905ba15",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h04-none — balanced_synthetic / hard / none

Source: `af364e2deb1a8beccdda9737`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. Independently, the warehouse rollout is approved.

고정한 요구사항:

```json
{
  "id": "h04-none",
  "core": "we might trial pack G8",
  "stance": "proposal",
  "slots": [
    {
      "role": "condition",
      "text": "desert depots",
      "available": false
    },
    {
      "role": "claim",
      "text": "This proposed trial has no deployment approval.",
      "available": false
    }
  ],
  "forbidden": [
    "the warehouse rollout is approved"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [
          "the warehouse rollout is approved"
        ],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": true,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:084d5b4c87dc217f0890df1f",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [
          "the warehouse rollout is approved"
        ],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": true,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "e",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:9f865e621e472ad9051eb401",
        "slots": [
          {
            "role": "condition",
            "text": "desert depots",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This proposed trial has no deployment approval.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## h05-full — balanced_synthetic / hard / full

Source: `555ad2b11ff3eab2c2c09cb6`

The pressure audit ended at 16:40. The pressure audit concerns rig C9. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.

고정한 요구사항:

```json
{
  "id": "h05-full",
  "core": "the pressure audit ended",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "at 16:40",
      "available": true
    },
    {
      "role": "condition",
      "text": "rig C9",
      "available": true
    }
  ],
  "forbidden": [
    "rig B7"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:a819d5ed4e1197a349214c89",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: False; 컴파일 오류: ValueError: Ambiguous repeated context span; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      },
      {
        "group_id": "f",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h05-partial — balanced_synthetic / hard / partial

Source: `4852a9ecdb538c2eea9f574f`

The pressure audit ended at 16:40. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.

고정한 요구사항:

```json
{
  "id": "h05-partial",
  "core": "the pressure audit ended",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "at 16:40",
      "available": true
    },
    {
      "role": "condition",
      "text": "rig C9",
      "available": false
    }
  ],
  "forbidden": [
    "rig B7"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:b5095db9243a963e5e15a02e",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: False; 컴파일 오류: ValueError: Ambiguous repeated context span; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      },
      {
        "group_id": "f",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h05-none — balanced_synthetic / hard / none

Source: `402c5d204d14decdfde55482`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.

고정한 요구사항:

```json
{
  "id": "h05-none",
  "core": "the pressure audit ended",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "at 16:40",
      "available": false
    },
    {
      "role": "condition",
      "text": "rig C9",
      "available": false
    }
  ],
  "forbidden": [
    "rig B7"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "5",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:b293d0c5269296cda6a72da8",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "e",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:ced0f494342cf081a6069fb7",
        "slots": [
          {
            "role": "time",
            "text": "at 16:40",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "condition",
            "text": "rig C9",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## h06-full — balanced_synthetic / hard / full

Source: `efddc392b4e4160ae4f7d3a1`

The coil estimate concerns operation in nitrogen. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. This capacity is conjectural and has not been measured. A separate steel cable was measured at 12 amperes in air.

고정한 요구사항:

```json
{
  "id": "h06-full",
  "core": "I suspect coil N8 may handle 18 amperes",
  "stance": "uncertainty",
  "slots": [
    {
      "role": "condition",
      "text": "in nitrogen",
      "available": true
    },
    {
      "role": "claim",
      "text": "This capacity is conjectural and has not been measured.",
      "available": true
    }
  ],
  "forbidden": [
    "12 amperes",
    "in air"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "6",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:2c92cc74ed419cea2728e485",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 7, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "f",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:b4f58f1fc63a50038cba58d0",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## h06-partial — balanced_synthetic / hard / partial

Source: `facb6ceb1eaf49e0fad2f32f`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. This capacity is conjectural and has not been measured. A separate steel cable was measured at 12 amperes in air.

고정한 요구사항:

```json
{
  "id": "h06-partial",
  "core": "I suspect coil N8 may handle 18 amperes",
  "stance": "uncertainty",
  "slots": [
    {
      "role": "condition",
      "text": "in nitrogen",
      "available": false
    },
    {
      "role": "claim",
      "text": "This capacity is conjectural and has not been measured.",
      "available": true
    }
  ],
  "forbidden": [
    "12 amperes",
    "in air"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:bd0d1330db1a663032a67bf2",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "e",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:3dfd522aed7e40806e53aac7",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## h06-none — balanced_synthetic / hard / none

Source: `b8137148fb3148d41392137f`

The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. A separate steel cable was measured at 12 amperes in air.

고정한 요구사항:

```json
{
  "id": "h06-none",
  "core": "I suspect coil N8 may handle 18 amperes",
  "stance": "uncertainty",
  "slots": [
    {
      "role": "condition",
      "text": "in nitrogen",
      "available": false
    },
    {
      "role": "claim",
      "text": "This capacity is conjectural and has not been measured.",
      "available": false
    }
  ],
  "forbidden": [
    "12 amperes",
    "in air"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "5",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:3fe27c21fdefbb5fa864bc9f",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 6, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "e",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:39606aa81377c100acbe1139",
        "slots": [
          {
            "role": "condition",
            "text": "in nitrogen",
            "available": false,
            "recovered": false,
            "typed": false
          },
          {
            "role": "claim",
            "text": "This capacity is conjectural and has not been measured.",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## n01 — natural_audit / medium / full

Source: `2532b1977fc260894d4d3a7e`

@all [Task Completed] Hello everyone, the task "Verify the accuracy of alarm rule creation and trigger logic" for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed. All test cases have passed, including various single conditions, combined conditions, and boundary value scenarios. The few issues discovered yesterday have also all been regression verified and passed. The final test report has been uploaded to Confluence. 🎉

고정한 요구사항:

```json
{
  "id": "n01",
  "core": "has been completed",
  "stance": "observation",
  "slots": [],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: False; 컴파일 오류: ValueError: Ungrounded extraction; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: False; 컴파일 오류: ValueError: Ungrounded extraction; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## n02 — natural_audit / medium / full

Source: `eeab452b3cb6dfffe3b2a655`

Good morning everyone. Today is Thursday. Just a reminder to @Hanqiang Liang and @Huihong Tian, your medication check-in module and family member invitation interface are due today. Please make sure to complete the delivery today. Other colleagues, please also share your plans and progress for today.

고정한 요구사항:

```json
{
  "id": "n02",
  "core": "are due today",
  "stance": "observation",
  "slots": [
    {
      "role": "time",
      "text": "Thursday",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "Thursday",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:eb58daf55321c17bac0333b5",
        "slots": [
          {
            "role": "time",
            "text": "Thursday",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 4, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "time",
            "text": "Thursday",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:fb65da8eb5621b8379a8c4fa",
        "slots": [
          {
            "role": "time",
            "text": "Thursday",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## n03 — natural_audit / medium / full

Source: `ef3ed7f7d45447190441c6bf`

Hello everyone, today I'm starting a new design task: [Designing a File Storage Solution]. Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3. The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack. A preliminary selection recommendation report will be provided early next week.

고정한 요구사항:

```json
{
  "id": "n03",
  "core": "recommendation report will be provided",
  "stance": "proposal",
  "slots": [
    {
      "role": "time",
      "text": "early next week",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true,
  "acceptable_stances": [
    "decision",
    "proposal"
  ]
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "early next week",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:8d398106665ef454e4a49ce2",
        "slots": [
          {
            "role": "time",
            "text": "early next week",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 4, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "d",
        "slots": [
          {
            "role": "time",
            "text": "early next week",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:53b5aa6c6cbfb4a56580bc32",
        "slots": [
          {
            "role": "time",
            "text": "early next week",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## n04 — natural_audit / medium / full

Source: `a3bb92bc6e953b07984eaa93`

Good morning everyone. Regarding the design of our file storage solution, I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday. From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage, and our other projects are also on AWS. Today, I will start designing the Bucket Policy and directory structure based on S3, for example, isolating by tenant and file type.

고정한 요구사항:

```json
{
  "id": "n04",
  "core": "I will start designing",
  "stance": "proposal",
  "slots": [
    {
      "role": "time",
      "text": "Today",
      "available": true
    },
    {
      "role": "subject",
      "text": "Bucket Policy and directory structure",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true,
  "acceptable_stances": [
    "decision",
    "proposal"
  ]
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: ValueError: Ungrounded extraction; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "time",
            "text": "Today",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "subject",
            "text": "Bucket Policy and directory structure",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 4, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "d",
        "slots": [
          {
            "role": "time",
            "text": "Today",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "subject",
            "text": "Bucket Policy and directory structure",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:e667fa164ed2379903472bed",
        "slots": [
          {
            "role": "time",
            "text": "Today",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "subject",
            "text": "Bucket Policy and directory structure",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## n05 — natural_audit / medium / full

Source: `b9a2917d39af17f120e6fb74`

Good morning everyone, regarding the file storage solution, the complete technical design document (based on AWS S3) has been uploaded to Confluence. It includes three main parts: bucket permission policies, lifecycle rules, and recommended directory structure. @Mingzhi Li Boss Li, please review it.

고정한 요구사항:

```json
{
  "id": "n05",
  "core": "has been uploaded to Confluence",
  "stance": "observation",
  "slots": [],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:88f7fe599165c2fb80a41e5f",
        "slots": [],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 4, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:44064ceb1a5c63be3eab5fed",
        "slots": [],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## n06 — natural_audit / hard / partial

Source: `cc0f8301e58ac1340b77a5ef`

@Lujian Gao I've finished reviewing the document on the file storage solution. The design is very comprehensive, especially the considerations for tenant data isolation and cost optimization. The proposal is approved and can be finalized.

고정한 요구사항:

```json
{
  "id": "n06",
  "core": "proposal is approved",
  "stance": "observation",
  "slots": [
    {
      "role": "subject",
      "text": "file storage solution",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true,
  "acceptable_stances": [
    "decision",
    "observation"
  ]
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "subject",
            "text": "file storage solution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:1a67e8961d376afd3f699b59",
        "slots": [
          {
            "role": "subject",
            "text": "file storage solution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "subject",
            "text": "file storage solution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:473c72286fc314d05e3f1d24",
        "slots": [
          {
            "role": "subject",
            "text": "file storage solution",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## n07 — natural_audit / medium / full

Source: `e736ba69ded95cdd2331a4e8`

@Yang Zhao Good question. Regarding the "forgot password" process, our main security consideration is to prevent "user enumeration attacks." Therefore, regardless of whether the email entered by the user exists or not, the feedback message should be consistent, such as "If this email address is registered, you will receive an email containing a password reset link," instead of directly prompting "user does not exist." Please ensure the UI copy adheres to this principle.

고정한 요구사항:

```json
{
  "id": "n07",
  "core": "feedback message should be consistent",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "regardless of whether the email entered by the user exists or not",
      "available": true
    },
    {
      "role": "basis",
      "text": "user enumeration attacks",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: ValueError: Ungrounded extraction; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "regardless of whether the email entered by the user exists or not",
            "available": true,
            "recovered": false,
            "typed": false
          },
          {
            "role": "basis",
            "text": "user enumeration attacks",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: ValueError: Ungrounded extraction; 저장 전달: {'stored_restarted': True, 'claim_packets': 0, 'source_status': 'failed'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "condition",
            "text": "regardless of whether the email entered by the user exists or not",
            "available": true,
            "recovered": true,
            "typed": true
          },
          {
            "role": "basis",
            "text": "user enumeration attacks",
            "available": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": false,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": false,
    "details": [],
    "visible_recovered": false,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## n08 — natural_audit / easy / full

Source: `fc8ef24a21781a9bc3026f2c`

Email received. The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction. @Xinjie Li @Xuexin Yin, please assess the scope of impact on the backend.

고정한 요구사항:

```json
{
  "id": "n08",
  "core": "must be forcibly routed",
  "stance": "decision",
  "slots": [
    {
      "role": "condition",
      "text": "ACCOUNT_STATUS_LOCKED",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "ACCOUNT_STATUS_LOCKED",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:6deb21ba16d1eca6ae0201aa",
        "slots": [
          {
            "role": "condition",
            "text": "ACCOUNT_STATUS_LOCKED",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "condition",
            "text": "ACCOUNT_STATUS_LOCKED",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:398702693eb08fe5751b4479",
        "slots": [
          {
            "role": "condition",
            "text": "ACCOUNT_STATUS_LOCKED",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## n09 — natural_audit / medium / full

Source: `82db5705bd31ef3b677608e5`

The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`, defined as 'Explicit Status Alert Policy'. It is mainly used for scenarios where an account is locked, requiring explicit interruption of user operations and guidance to manual channels.

고정한 요구사항:

```json
{
  "id": "n09",
  "core": "requiring explicit interruption",
  "stance": "observation",
  "slots": [
    {
      "role": "condition",
      "text": "where an account is locked",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "where an account is locked",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:f4240f69a0e88877b4c7f571",
        "slots": [
          {
            "role": "condition",
            "text": "where an account is locked",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "condition",
            "text": "where an account is locked",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:19346d92077c52c18286999e",
        "slots": [
          {
            "role": "condition",
            "text": "where an account is locked",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## n10 — natural_audit / hard / partial

Source: `f3e4d9a3e84884e5abe2e967`

Received. I've reviewed the document. This strategy will be handled by `ExplicitStateAlertModule`, and the parameter `halt_downstream_triggers` is set to `true`. This means that after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted, right?

고정한 요구사항:

```json
{
  "id": "n10",
  "core": "will be halted",
  "stance": "question",
  "slots": [
    {
      "role": "condition",
      "text": "after the backend triggers this strategy",
      "available": true
    },
    {
      "role": "subject",
      "text": "ERR_POLICY_LOCKED_ACCOUNT_V1",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "condition",
            "text": "after the backend triggers this strategy",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "subject",
            "text": "ERR_POLICY_LOCKED_ACCOUNT_V1",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:e67bc65c0f9c4504f7fafc30",
        "slots": [
          {
            "role": "condition",
            "text": "after the backend triggers this strategy",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "subject",
            "text": "ERR_POLICY_LOCKED_ACCOUNT_V1",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "condition",
            "text": "after the backend triggers this strategy",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "subject",
            "text": "ERR_POLICY_LOCKED_ACCOUNT_V1",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:b1c707f60134216dc0ae0f13",
        "slots": [
          {
            "role": "condition",
            "text": "after the backend triggers this strategy",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "subject",
            "text": "ERR_POLICY_LOCKED_ACCOUNT_V1",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

## n11 — natural_audit / hard / partial

Source: `2f036a676a1e734b9821a11d`

@Xinjie Li Yes, your understanding is completely correct. This is to avoid sending users redundant or potentially confusing automated messages.

고정한 요구사항:

```json
{
  "id": "n11",
  "core": "avoid sending users redundant or potentially confusing automated messages",
  "stance": "observation",
  "slots": [
    {
      "role": "subject",
      "text": "downstream automated notifications",
      "available": false
    }
  ],
  "forbidden": [
    "your understanding is completely correct"
  ],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "subject",
            "text": "downstream automated notifications",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:d3a7c0b8357cddf9a592df87",
        "slots": [
          {
            "role": "subject",
            "text": "downstream automated notifications",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "a",
        "slots": [
          {
            "role": "subject",
            "text": "downstream automated notifications",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [
          "your understanding is completely correct"
        ],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": true,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:a975c1e474c3b53eafab8652",
        "slots": [
          {
            "role": "subject",
            "text": "downstream automated notifications",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [
          "your understanding is completely correct"
        ],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": true,
    "passed": false
  }
}
```

## n12 — natural_audit / medium / full

Source: `ea426379076abc7e9d24ecbb`

Received, thanks a lot! The data structure looks very clear. I plan to complete the static data integration this morning to ensure the charts render correctly. In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it. @Mingzhi Li

고정한 요구사항:

```json
{
  "id": "n12",
  "core": "start researching dynamic refresh solutions",
  "stance": "proposal",
  "slots": [
    {
      "role": "time",
      "text": "afternoon",
      "available": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true,
  "acceptable_stances": [
    "decision",
    "proposal"
  ]
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 2, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "2",
        "slots": [
          {
            "role": "time",
            "text": "afternoon",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:fb56f0989eeaa3199805d436",
        "slots": [
          {
            "role": "time",
            "text": "afternoon",
            "available": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 4, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "d",
        "slots": [
          {
            "role": "time",
            "text": "afternoon",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:cdaf7df96d5a462a0157da4c",
        "slots": [
          {
            "role": "time",
            "text": "afternoon",
            "available": true,
            "recovered": true,
            "typed": true
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## n13 — natural_audit / hard / full

Source: `9279497ab46d95f158eeb6de`

@Yunqi Qian Great plan. WebSocket is the best solution, but our message push service isn't fully ready yet. This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds. Once the WebSocket service is stable later, we can upgrade it uniformly. This way, we can avoid blocking your current task.

고정한 요구사항:

```json
{
  "id": "n13",
  "core": "implemented using polling",
  "stance": "decision",
  "slots": [
    {
      "role": "basis",
      "text": "our message push service isn't fully ready yet",
      "available": true,
      "optional": true
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "basis",
            "text": "our message push service isn't fully ready yet",
            "available": true,
            "optional": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:586c4dc64868162202017d16",
        "slots": [
          {
            "role": "basis",
            "text": "our message push service isn't fully ready yet",
            "available": true,
            "optional": true,
            "recovered": true,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: True; 컴파일 후 통과: True; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 5, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "c",
        "slots": [
          {
            "role": "basis",
            "text": "our message push service isn't fully ready yet",
            "available": true,
            "optional": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:84a9fbcaf8f8e0c729f7bc4f",
        "slots": [
          {
            "role": "basis",
            "text": "our message push service isn't fully ready yet",
            "available": true,
            "optional": true,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": true,
        "passed": true
      }
    ],
    "visible_recovered": true,
    "typed_complete": true,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": true
  }
}
```

## n14 — natural_audit / hard / partial

Source: `b3a1426c132e34bf7819b9fd`

Okay, Boss Li, understood. Then I'll use the polling solution for now, and I'll adjust the plan.

고정한 요구사항:

```json
{
  "id": "n14",
  "core": "use the polling solution for now",
  "stance": "decision",
  "slots": [
    {
      "role": "time",
      "text": "for now",
      "available": true
    },
    {
      "role": "basis",
      "text": "message push service isn't fully ready",
      "available": false
    }
  ],
  "forbidden": [],
  "allow_unspecified_basis": true
}
```

### simple

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 1, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "1",
        "slots": [
          {
            "role": "time",
            "text": "for now",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "message push service isn't fully ready",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:8e0e8c7c934aee68afbeeb11",
        "slots": [
          {
            "role": "time",
            "text": "for now",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "message push service isn't fully ready",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": false,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": false,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

### ours

원출력 통과: False; 컴파일 후 통과: False; 컴파일 오류: None; 저장 전달: {'stored_restarted': True, 'claim_packets': 3, 'source_status': 'annotated'}

원출력:
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

고정 채점:
```json
{
  "raw": {
    "target_found": true,
    "details": [
      {
        "group_id": "b",
        "slots": [
          {
            "role": "time",
            "text": "for now",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "message push service isn't fully ready",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  },
  "compiled": {
    "target_found": true,
    "details": [
      {
        "group_id": "c:0d3195b6d63889b83b7fa8f9",
        "slots": [
          {
            "role": "time",
            "text": "for now",
            "available": true,
            "recovered": true,
            "typed": false
          },
          {
            "role": "basis",
            "text": "message push service isn't fully ready",
            "available": false,
            "recovered": false,
            "typed": false
          }
        ],
        "stance_ok": true,
        "wrong_target": [],
        "unsupported_completion": [],
        "visible_recovered": true,
        "typed_complete": false,
        "passed": false
      }
    ],
    "visible_recovered": true,
    "typed_complete": false,
    "stance_ok": true,
    "unsupported_completion": false,
    "wrong_target": false,
    "passed": false
  }
}
```

