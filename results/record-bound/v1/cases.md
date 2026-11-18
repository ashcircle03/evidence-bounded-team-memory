# Per-document records comparison

Gold and scoring are fixed. Listed losses/gains are item sets, not aggregate substitutions. Full actual outputs follow each source.

## e01-full — balanced_synthetic / easy / full

```text
For chilled parcels, use liner K6 because the foam prevents condensation.
```

Complete: old True → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → condition → r1:condition1`: chilled parcels

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "For chilled parcels, use liner K6 because the foam prevents condensation.",
        "stance": "decision"
      },
      "details": [
        {
          "segment": 0,
          "quote": "the foam prevents condensation",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [
        {
          "segment": 0,
          "quote": "because the foam prevents condensation",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e01-partial — balanced_synthetic / easy / partial

```text
For chilled parcels, use liner K6.
```

Complete: old True → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → condition → r1:condition1`: chilled parcels

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "For chilled parcels, use liner K6.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e01-none — balanced_synthetic / easy / none

```text
use liner K6.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "use liner K6.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e02-full — balanced_synthetic / easy / full

```text
close gate R8 on Thursday because the hinge needs repair.
```

Complete: old False → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r1 → basis → r1:basis1`: the hinge needs repair

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:basis1",
      "r1:claim",
      "r1:time1"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "close gate R8 on Thursday because the hinge needs repair.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 0,
          "quote": "because the hinge needs repair",
          "kind": "stated"
        }
      ],
      "time": [
        {
          "segment": 0,
          "quote": "on Thursday"
        }
      ],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e02-partial — balanced_synthetic / easy / partial

```text
close gate R8 because the hinge needs repair.
```

Complete: old False → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r1 → basis → r1:basis1`: the hinge needs repair

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "close gate R8 because the hinge needs repair.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 0,
          "quote": "the hinge needs repair",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e02-none — balanced_synthetic / easy / none

```text
close gate R8.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

### simple

```json
{
  "extractions": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:claim"
    ],
    "missing_claims": [
      "r1:claim"
    ],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim"
    ],
    "missing_claims": [
      "r1:claim"
    ],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "close gate R8.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e03-full — balanced_synthetic / easy / full

```text
For cracked containers, do not ship kit M3 because the seal failed inspection.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "For cracked containers, do not ship kit M3 because the seal failed inspection.",
        "stance": "decision"
      },
      "details": [],
      "condition": [
        {
          "segment": 0,
          "quote": "for cracked containers"
        }
      ],
      "basis": [
        {
          "segment": 0,
          "quote": "because the seal failed inspection",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e03-partial — balanced_synthetic / easy / partial

```text
For cracked containers, do not ship kit M3.
```

Complete: old True → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → condition → r1:condition1`: cracked containers

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "For cracked containers, do not ship kit M3.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e03-none — balanced_synthetic / easy / none

```text
do not ship kit M3.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "do not ship kit M3.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e04-full — balanced_synthetic / easy / full

```text
For inland stations, we might trial paint Q9. This trial is not approved.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → caveat → r1:caveat1`: This trial is not approved.; `r1 → condition → r1:condition1`: inland stations

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:caveat1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:caveat1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "For inland stations, we might trial paint Q9.",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "This trial is not approved.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "unbound:1",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "unbound:c:69118951c69ee70abfbcfe1d",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e04-partial — balanced_synthetic / easy / partial

```text
we might trial paint Q9. This trial is not approved.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → caveat → r1:caveat1`: This trial is not approved.

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "we might trial paint Q9.",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "This trial is not approved.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:1",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:c:63a80fc5cc3a3166d6cafceb",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e04-none — balanced_synthetic / easy / none

```text
we might trial paint Q9.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "we might trial paint Q9.",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e05-full — balanced_synthetic / easy / full

```text
Recorded event time: on Tuesday. the sensor check is complete for firmware 6.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → time → r1:time1`: on Tuesday

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:time1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:time1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Recorded event time: on Tuesday.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 0,
          "quote": "on Tuesday"
        }
      ],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "the sensor check is complete for firmware 6.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "unbound:0",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "unbound:c:8211e56a5e0bfe9ffb7faa04",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e05-partial — balanced_synthetic / easy / partial

```text
Recorded event time: on Tuesday. the sensor check is complete.
```

Complete: old True → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → time → r1:time1`: on Tuesday

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:time1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:time1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Recorded event time: on Tuesday.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 0,
          "quote": "on Tuesday"
        }
      ],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "the sensor check is complete.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "time",
        "r1:time1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:0",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "time",
        "r1:time1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:c:2491693afccd3c4528972c21",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e05-none — balanced_synthetic / easy / none

```text
the sensor check is complete.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "the sensor check is complete",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e06-full — balanced_synthetic / easy / full

```text
For dry rooms, I suspect relay P4 may last 80 days. This estimate is untested.
```

Complete: old True → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → condition → r1:condition1`: dry rooms

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:caveat1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:caveat1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "For dry rooms, I suspect relay P4 may last 80 days.",
        "stance": "uncertainty"
      },
      "details": [
        {
          "segment": 1,
          "quote": "This estimate is untested.",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e06-partial — balanced_synthetic / easy / partial

```text
I suspect relay P4 may last 80 days. This estimate is untested.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "I suspect relay P4 may last 80 days.",
        "stance": "uncertainty"
      },
      "details": [
        {
          "segment": 1,
          "quote": "This estimate is untested.",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## e06-none — balanced_synthetic / easy / none

```text
I suspect relay P4 may last 80 days.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "I suspect relay P4 may last 80 days.",
        "stance": "uncertainty"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m01-full — balanced_synthetic / medium / full

```text
This survey decision applies to sector D2. The cabinet label is copper. we postpone the gravel survey because the access bridge is closed.
```

Complete: old False → candidate False.

Lost required content: none

New required content: `r1:basis1`: the access bridge is closed; `r1:claim`: we postpone the gravel survey; `r1:condition1`: sector D2; `r2:claim`: The cabinet label is copper

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:basis1",
      "r1:claim",
      "r1:condition1",
      "r2:claim"
    ],
    "missing_claims": [
      "r1:claim",
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "This survey decision applies to sector D2",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The cabinet label is copper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "we postpone the gravel survey",
        "stance": "decision"
      },
      "details": [
        {
          "segment": 2,
          "quote": "because the access bridge is closed",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m01-partial — balanced_synthetic / medium / partial

```text
This survey decision applies to sector D2. The cabinet label is copper. we postpone the gravel survey.
```

Complete: old False → candidate False.

Lost required content: none

New required content: `r1:claim`: we postpone the gravel survey; `r1:condition1`: sector D2; `r2:claim`: The cabinet label is copper

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r1:condition1",
      "r2:claim"
    ],
    "missing_claims": [
      "r1:claim",
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "This survey decision applies to sector D2",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The cabinet label is copper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "we postpone the gravel survey",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m01-none — balanced_synthetic / medium / none

```text
The cabinet label is copper. we postpone the gravel survey.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The cabinet label is copper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "we postpone the gravel survey",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m02-full — balanced_synthetic / medium / full

```text
Timing for the following beacon instruction: after the morning inspection. The antenna colour remains white. switch the beacon to standby because the battery is leaking.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Timing for the following beacon instruction: after the morning inspection.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 0,
          "quote": "after the morning inspection"
        }
      ],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The antenna colour remains white.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "switch the beacon to standby",
        "stance": "decision"
      },
      "details": [
        {
          "segment": 2,
          "quote": "because the battery is leaking",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [
        {
          "segment": 2,
          "quote": "because the battery is leaking",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "time",
        "r1:time1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:0",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "time",
        "r1:time1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:c:9870498ac0dfa09a8a1b6ed3",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m02-partial — balanced_synthetic / medium / partial

```text
The antenna colour remains white. switch the beacon to standby because the battery is leaking.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r1 → basis → r1:basis1`: the battery is leaking

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The antenna colour remains white",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "switch the beacon to standby",
        "stance": "decision"
      },
      "details": [],
      "condition": [
        {
          "segment": 1,
          "quote": "because the battery is leaking"
        }
      ],
      "basis": [
        {
          "segment": 1,
          "quote": "the battery is leaking",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [
      [
        "r1",
        "condition",
        "r1:basis1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [
      [
        "r1",
        "condition",
        "r1:basis1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m02-none — balanced_synthetic / medium / none

```text
The antenna colour remains white. switch the beacon to standby.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The antenna colour remains white.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "switch the beacon to standby.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m03-full — balanced_synthetic / medium / full

```text
The following release instruction applies to saline batches. do not release batch U5 because the residue test failed. Freshwater batches remain eligible for release.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r1 → basis → r1:basis1`: the residue test failed; `r1 → condition → r1:condition1`: saline batches

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The following release instruction applies to saline batches",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "do not release batch U5",
        "stance": "decision"
      },
      "details": [],
      "condition": [
        {
          "segment": 0,
          "quote": "applies to saline batches"
        }
      ],
      "basis": [
        {
          "segment": 1,
          "quote": "because the residue test failed",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "Freshwater batches remain eligible for release",
        "stance": "observation"
      },
      "details": [],
      "condition": [
        {
          "segment": 0,
          "quote": "applies to saline batches"
        }
      ],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [
      [
        "r2",
        "condition",
        "r1:condition1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [
      [
        "r2",
        "condition",
        "r1:condition1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m03-partial — balanced_synthetic / medium / partial

```text
The following release instruction applies to saline batches. do not release batch U5. Freshwater batches remain eligible for release.
```

Complete: old True → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The following release instruction applies to saline batches",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "do not release batch U5",
        "stance": "decision"
      },
      "details": [],
      "condition": [
        {
          "segment": 0,
          "quote": "applies to saline batches"
        }
      ],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "Freshwater batches remain eligible for release",
        "stance": "observation"
      },
      "details": [],
      "condition": [
        {
          "segment": 0,
          "quote": "applies to saline batches"
        }
      ],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [
      [
        "r2",
        "condition",
        "r1:condition1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [
      [
        "r2",
        "condition",
        "r1:condition1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m03-none — balanced_synthetic / medium / none

```text
do not release batch U5. Freshwater batches remain eligible for release.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "do not release batch U5.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "Freshwater batches remain eligible for release.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m04-full — balanced_synthetic / medium / full

```text
Scope of the filter pilot: remote clinics. The spare tubing is blue. we could pilot filter J2. This pilot is a suggestion, not an authorization.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → caveat → r1:caveat1`: This pilot is a suggestion, not an authorization.

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Scope of the filter pilot: remote clinics.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The spare tubing is blue.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "we could pilot filter J2.",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "This pilot is a suggestion, not an authorization.",
        "stance": "observation"
      },
      "details": [
        {
          "segment": 3,
          "quote": "not an authorization",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "extra_rows": [
      {
        "row": 4,
        "role": "claim",
        "text": "not an authorization",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0,
      4
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "unbound:c:07511dec649bedb7a56a7d83",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "extra_rows": [
      {
        "row": 4,
        "role": "claim",
        "text": "not an authorization",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0,
      4
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m04-partial — balanced_synthetic / medium / partial

```text
The spare tubing is blue. we could pilot filter J2. This pilot is a suggestion, not an authorization.
```

Complete: old False → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The spare tubing is blue",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "we could pilot filter J2",
        "stance": "proposal"
      },
      "details": [
        {
          "segment": 2,
          "quote": "This pilot is a suggestion, not an authorization",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m04-none — balanced_synthetic / medium / none

```text
The spare tubing is blue. we could pilot filter J2.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The spare tubing is blue",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "we could pilot filter J2",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m05-full — balanced_synthetic / medium / full

```text
The calibration event occurred on Friday afternoon. The office clock was repaired. the valve calibration finished on bench T7.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The calibration event occurred on Friday afternoon.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 0,
          "quote": "on Friday afternoon"
        }
      ],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The office clock was repaired.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "the valve calibration finished on bench T7.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 2,
          "quote": "on bench T7."
        }
      ],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "r1",
        "time",
        "r1:condition1"
      ],
      [
        "unbound:0",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "r1",
        "time",
        "r1:condition1"
      ],
      [
        "unbound:c:2ac60e2d73e91fc034b5d4ed",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m05-partial — balanced_synthetic / medium / partial

```text
The calibration event occurred on Friday afternoon. The office clock was repaired. the valve calibration finished.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The calibration event occurred on Friday afternoon.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 0,
          "quote": "on Friday afternoon"
        }
      ],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The office clock was repaired.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "the valve calibration finished.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "time",
        "r1:time1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:0",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "time",
        "r1:time1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:c:42da6819dbe05676d6a24750",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m05-none — balanced_synthetic / medium / none

```text
The office clock was repaired. the valve calibration finished.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The office clock was repaired",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "the valve calibration finished",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m06-full — balanced_synthetic / medium / full

```text
Operating scope of this estimate: under reduced load. The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Operating scope of this estimate: under reduced load.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The procurement task is complete.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "I suspect drive L4 may reach 70 cycles.",
        "stance": "uncertainty"
      },
      "details": [
        {
          "segment": 3,
          "quote": "No measurement supports this estimate yet.",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m06-partial — balanced_synthetic / medium / partial

```text
The procurement task is complete. I suspect drive L4 may reach 70 cycles. No measurement supports this estimate yet.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The procurement task is complete",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "I suspect drive L4 may reach 70 cycles",
        "stance": "uncertainty"
      },
      "details": [
        {
          "segment": 2,
          "quote": "No measurement supports this estimate yet",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## m06-none — balanced_synthetic / medium / none

```text
The procurement task is complete. I suspect drive L4 may reach 70 cycles.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The procurement task is complete",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "I suspect drive L4 may reach 70 cycles",
        "stance": "uncertainty"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h01-full — balanced_synthetic / hard / full

```text
Scope of the compressor instruction: pressure above 9 bar. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4 because its casing has fractured. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r1 → basis → r1:basis1`: its casing has fractured; `r6 → basis → r6:basis1`: the buffer is empty

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Scope of the compressor instruction: pressure above 9 bar.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "halt compressor Z4 because its casing has fractured.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 9,
          "quote": "its casing has fractured",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "Separate instruction: below 1 bar, start pump B2 because the buffer is empty.",
        "stance": "decision"
      },
      "details": [],
      "condition": [
        {
          "segment": 10,
          "quote": "below 1 bar"
        }
      ],
      "basis": [
        {
          "segment": 10,
          "quote": "the buffer is empty",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h01-partial — balanced_synthetic / hard / partial

```text
Scope of the compressor instruction: pressure above 9 bar. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Scope of the compressor instruction: pressure above 9 bar.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "halt compressor Z4.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "Separate instruction: below 1 bar, start pump B2 because the buffer is empty.",
        "stance": "decision"
      },
      "details": [
        {
          "segment": 10,
          "quote": "because the buffer is empty",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [
        {
          "segment": 10,
          "quote": "below 1 bar"
        }
      ],
      "basis": [
        {
          "segment": 10,
          "quote": "because the buffer is empty",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h01-none — balanced_synthetic / hard / none

```text
The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. halt compressor Z4. Separate instruction: below 1 bar, start pump B2 because the buffer is empty.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "halt compressor Z4",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "Separate instruction: below 1 bar, start pump B2 because the buffer is empty",
        "stance": "decision"
      },
      "details": [
        {
          "segment": 9,
          "quote": "because the buffer is empty",
          "stance": "decision",
          "kind": "qualification"
        }
      ],
      "condition": [
        {
          "segment": 9,
          "quote": "below 1 bar"
        }
      ],
      "basis": [
        {
          "segment": 9,
          "quote": "because the buffer is empty",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h02-full — balanced_synthetic / hard / full

```text
The time of the compass instruction is at 14:20. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test because the replacement mount passed inspection. Independently, the camera check begins at 14:20 because its lens is clean.
```

Complete: old False → candidate False.

Lost required content: none

New required content: `r1:basis1`: the replacement mount passed inspection; `r1:claim`: resume the compass test; `r1:time1`: at 14:20; `r2:claim`: The delivery folder contains a yellow form; `r3:claim`: The stock counter remains seven; `r4:claim`: The break room has two chairs; `r5:claim`: The printer tray contains plain paper; `r6:basis1`: its lens is clean; `r6:claim`: the camera check begins; `r6:time1`: at 14:20

Lost correct links: none

New correct links: `r1 → basis → r1:basis1`: the replacement mount passed inspection; `r6 → basis → r6:basis1`: its lens is clean; `r6 → time → r6:time1`: at 14:20

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
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
    "missing_claims": [
      "r1:claim",
      "r2:claim",
      "r3:claim",
      "r4:claim",
      "r5:claim",
      "r6:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The time of the compass instruction is at 14:20.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 0,
          "quote": "at 14:20"
        }
      ],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "resume the compass test because the replacement mount passed inspection.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 9,
          "quote": "because the replacement mount passed inspection",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "Independently, the camera check begins at 14:20 because its lens is clean.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 10,
          "quote": "because its lens is clean",
          "kind": "stated"
        }
      ],
      "time": [
        {
          "segment": 10,
          "quote": "at 14:20"
        }
      ],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "time",
        "r1:time1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:0",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "time",
        "r1:time1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:c:738e33985a7adf99c9af31f1",
        "time",
        "r1:time1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h02-partial — balanced_synthetic / hard / partial

```text
The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test because the replacement mount passed inspection. Independently, the camera check begins at 14:20 because its lens is clean.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r1 → basis → r1:basis1`: the replacement mount passed inspection; `r6 → basis → r6:basis1`: its lens is clean; `r6 → time → r6:time1`: at 14:20

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 4,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "resume the compass test because the replacement mount passed inspection",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 8,
          "quote": "because the replacement mount passed inspection",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "Independently, the camera check begins at 14:20 because its lens is clean",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 9,
          "quote": "because its lens is clean",
          "kind": "stated"
        }
      ],
      "time": [
        {
          "segment": 9,
          "quote": "at 14:20"
        }
      ],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h02-none — balanced_synthetic / hard / none

```text
The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. resume the compass test. Independently, the camera check begins at 14:20 because its lens is clean.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r6 → basis → r6:basis1`: its lens is clean; `r6 → time → r6:time1`: at 14:20

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 4,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [
      "r6:claim"
    ],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [
      "r6:claim"
    ],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "resume the compass test",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "Independently, the camera check begins at 14:20 because its lens is clean",
        "stance": "decision"
      },
      "details": [
        {
          "segment": 9,
          "quote": "at 14:20",
          "stance": "observation",
          "kind": "method"
        }
      ],
      "condition": [],
      "basis": [
        {
          "segment": 9,
          "quote": "because its lens is clean",
          "kind": "stated"
        }
      ],
      "time": [
        {
          "segment": 9,
          "quote": "at 14:20"
        }
      ],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [
      10
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [
      10
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h03-full — balanced_synthetic / hard / full

```text
The map instruction below concerns commercial reuse. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map because the licence excludes commercial distribution. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r1 → basis → r1:basis1`: the licence excludes commercial distribution

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1",
      "r2:claim",
      "r3:claim",
      "r4:claim",
      "r5:claim"
    ],
    "missing_claims": [
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1",
      "r2:claim",
      "r3:claim",
      "r4:claim",
      "r5:claim"
    ],
    "missing_claims": [
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The map instruction below concerns commercial reuse.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "do not publish the terrain map because the licence excludes commercial distribution.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 9,
          "quote": "because the licence excludes commercial distribution",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.",
        "stance": "decision"
      },
      "details": [],
      "condition": [
        {
          "segment": 10,
          "quote": "for classroom teaching"
        }
      ],
      "basis": [
        {
          "segment": 10,
          "quote": "because the teacher granted permission",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h03-partial — balanced_synthetic / hard / partial

```text
The map instruction below concerns commercial reuse. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r6 → basis → r6:basis1`: the teacher granted permission; `r6 → condition → r6:condition1`: for classroom teaching

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1",
      "r2:claim",
      "r3:claim",
      "r4:claim",
      "r5:claim"
    ],
    "missing_claims": [
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1",
      "r2:claim",
      "r3:claim",
      "r4:claim",
      "r5:claim"
    ],
    "missing_claims": [
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The map instruction below concerns commercial reuse.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "do not publish the terrain map.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.",
        "stance": "decision"
      },
      "details": [
        {
          "segment": 10,
          "quote": "because the teacher granted permission",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [
        {
          "segment": 10,
          "quote": "for classroom teaching"
        }
      ],
      "basis": [
        {
          "segment": 10,
          "quote": "because the teacher granted permission",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h03-none — balanced_synthetic / hard / none

```text
The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. do not publish the terrain map. Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission.
```

Complete: old False → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "do not publish the terrain map",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "Separate instruction: for classroom teaching, publish the sketch because the teacher granted permission",
        "stance": "decision"
      },
      "details": [
        {
          "segment": 9,
          "quote": "because the teacher granted permission",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [
        {
          "segment": 9,
          "quote": "for classroom teaching"
        }
      ],
      "basis": [
        {
          "segment": 9,
          "quote": "because the teacher granted permission",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h04-full — balanced_synthetic / hard / full

```text
The pack trial applies to desert depots. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. This proposed trial has no deployment approval. Independently, the warehouse rollout is approved.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → caveat → r1:caveat1`: This proposed trial has no deployment approval.

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The pack trial applies to desert depots",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "we might trial pack G8",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "This proposed trial has no deployment approval",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 11,
        "quote": "Independently, the warehouse rollout is approved",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "unbound:10",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "unbound:c:0d2d465592b26190e458a92d",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h04-partial — balanced_synthetic / hard / partial

```text
The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. This proposed trial has no deployment approval. Independently, the warehouse rollout is approved.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r1 → caveat → r1:caveat1`: This proposed trial has no deployment approval.

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "we might trial pack G8.",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "This proposed trial has no deployment approval.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "Independently, the warehouse rollout is approved.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:9",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "incorrect_edges": [
      [
        "unbound:c:f7a924a42af959cae595053c",
        "caveat",
        "r1:caveat1"
      ]
    ],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h04-none — balanced_synthetic / hard / none

```text
The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. we might trial pack G8. Independently, the warehouse rollout is approved.
```

Complete: old True → candidate True.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "we might trial pack G8.",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "Independently, the warehouse rollout is approved.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h05-full — balanced_synthetic / hard / full

```text
The pressure audit ended at 16:40. The pressure audit concerns rig C9. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.
```

Complete: old False → candidate False.

Lost required content: none

New required content: `r1:claim`: the pressure audit ended; `r1:condition1`: rig C9; `r1:time1`: at 16:40; `r2:claim`: The delivery folder contains a yellow form; `r3:claim`: The stock counter remains seven; `r4:claim`: The break room has two chairs; `r5:claim`: The printer tray contains plain paper; `r6:claim`: the noise audit starts; `r6:condition1`: on rig B7; `r6:time1`: at 16:40

Lost correct links: none

New correct links: `r1 → time → r1:time1`: at 16:40; `r6 → time → r6:time1`: at 16:40

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": true,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
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
    "missing_claims": [
      "r1:claim",
      "r2:claim",
      "r3:claim",
      "r4:claim",
      "r5:claim",
      "r6:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The pressure audit ended at 16:40.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 0,
          "quote": "at 16:40"
        }
      ],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The pressure audit concerns rig C9.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "the pressure audit ended.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 11,
        "quote": "Separately, the noise audit starts at 16:40 on rig B7.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 11,
          "quote": "at 16:40"
        }
      ],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
      2
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
      2
    ],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h05-partial — balanced_synthetic / hard / partial

```text
The pressure audit ended at 16:40. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.
```

Complete: old False → candidate False.

Lost required content: none

New required content: `r1:claim`: the pressure audit ended; `r1:time1`: at 16:40; `r2:claim`: The delivery folder contains a yellow form; `r3:claim`: The stock counter remains seven; `r4:claim`: The break room has two chairs; `r5:claim`: The printer tray contains plain paper; `r6:claim`: the noise audit starts; `r6:condition1`: on rig B7; `r6:time1`: at 16:40

Lost correct links: none

New correct links: `r1 → time → r1:time1`: at 16:40; `r6 → time → r6:time1`: at 16:40

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
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
    "missing_claims": [
      "r1:claim",
      "r2:claim",
      "r3:claim",
      "r4:claim",
      "r5:claim",
      "r6:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The pressure audit ended at 16:40.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 0,
          "quote": "at 16:40"
        }
      ],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "the pressure audit ended.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "Separately, the noise audit starts at 16:40 on rig B7.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 10,
          "quote": "at 16:40"
        }
      ],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h05-none — balanced_synthetic / hard / none

```text
The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. the pressure audit ended. Separately, the noise audit starts at 16:40 on rig B7.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r6 → time → r6:time1`: at 16:40

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "the pressure audit ended.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "Separately, the noise audit starts at 16:40 on rig B7.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [{"segment": 9, "quote": "at 16:40"}],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h06-full — balanced_synthetic / hard / full

```text
The coil estimate concerns operation in nitrogen. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. This capacity is conjectural and has not been measured. A separate steel cable was measured at 12 amperes in air.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The coil estimate concerns operation in nitrogen.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The delivery folder contains a yellow form.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The stock counter remains seven.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The break room has two chairs.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "The printer tray contains plain paper.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "I suspect coil N8 may handle 18 amperes.",
        "stance": "uncertainty"
      },
      "details": [
        {
          "segment": 10,
          "quote": "This capacity is conjectural and has not been measured.",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 11,
        "quote": "A separate steel cable was measured at 12 amperes in air.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h06-partial — balanced_synthetic / hard / partial

```text
The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. This capacity is conjectural and has not been measured. A separate steel cable was measured at 12 amperes in air.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "I suspect coil N8 may handle 18 amperes",
        "stance": "uncertainty"
      },
      "details": [
        {
          "segment": 9,
          "quote": "This capacity is conjectural and has not been measured",
          "stance": "observation",
          "kind": "qualification"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 10,
        "quote": "A separate steel cable was measured at 12 amperes in air",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## h06-none — balanced_synthetic / hard / none

```text
The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. The delivery folder contains a yellow form. The stock counter remains seven. The break room has two chairs. The printer tray contains plain paper. I suspect coil N8 may handle 18 amperes. A separate steel cable was measured at 12 amperes in air.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "The delivery folder contains a yellow form",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 5,
        "quote": "The stock counter remains seven",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 6,
        "quote": "The break room has two chairs",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 7,
        "quote": "The printer tray contains plain paper",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 8,
        "quote": "I suspect coil N8 may handle 18 amperes",
        "stance": "uncertainty"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 9,
        "quote": "A separate steel cable was measured at 12 amperes in air",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n01 — natural_audit / medium / full

```text
@all [Task Completed] Hello everyone, the task "Verify the accuracy of alarm rule creation and trigger logic" for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed. All test cases have passed, including various single conditions, combined conditions, and boundary value scenarios. The few issues discovered yesterday have also all been regression verified and passed. The final test report has been uploaded to Confluence. 🎉
```

Complete: old False → candidate False.

Lost required content: none

New required content: `r1:claim`: the task "Verify the accuracy of alarm rule creation and trigger logic" for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed; `r2:caveat1`: including various single conditions, combined conditions, and boundary value scenarios; `r2:claim`: All test cases have passed; `r3:claim`: The few issues discovered yesterday have also all been regression verified and passed; `r3:time1`: yesterday; `r4:claim`: The final test report has been uploaded to Confluence

Lost correct links: none

New correct links: `r2 → caveat → r2:caveat1`: including various single conditions, combined conditions, and boundary value scenarios

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r2:caveat1",
      "r2:claim",
      "r3:claim",
      "r3:time1",
      "r4:claim"
    ],
    "missing_claims": [
      "r1:claim",
      "r2:claim",
      "r3:claim",
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r2:caveat1",
      "r2:claim",
      "r3:claim",
      "r3:time1",
      "r4:claim"
    ],
    "missing_claims": [
      "r1:claim",
      "r2:claim",
      "r3:claim",
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "@all [Task Completed] Hello everyone, the task \"Verify the accuracy of alarm rule creation and trigger logic\" for the Enterprise Energy Consumption Monitoring and Energy Saving Diagnosis System has been completed.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "All test cases have passed, including various single conditions, combined conditions, and boundary value scenarios.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The few issues discovered yesterday have also all been regression verified and passed.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The final test report has been uploaded to Confluence.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": [
    {
      "segment": 4,
      "quote": "🎉",
      "kind": "salutation"
    }
  ]
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r3",
        "time",
        "r3:time1"
      ]
    ],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r3",
        "time",
        "r3:time1"
      ]
    ],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n02 — natural_audit / medium / full

```text
Good morning everyone. Today is Thursday. Just a reminder to @Hanqiang Liang and @Huihong Tian, your medication check-in module and family member invitation interface are due today. Please make sure to complete the delivery today. Other colleagues, please also share your plans and progress for today.
```

Complete: old False → candidate False.

Lost required content: none

New required content: `r2:recipient1`: @Hanqiang Liang and @Huihong Tian

Lost correct links: none

New correct links: `r2 → recipient → r2:recipient1`: @Hanqiang Liang and @Huihong Tian

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r1:time2",
      "r2:recipient1",
      "r2:time2",
      "r3:time2",
      "r4:time2"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r1:time2",
      "r2:recipient1",
      "r2:time2",
      "r3:time2",
      "r4:time2"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
    ],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r2:recipient1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r2:recipient1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Good morning everyone.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "Today is Thursday.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "Just a reminder to @Hanqiang Liang and @Huihong Tian, your medication check-in module and family member invitation interface are due today.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "Please make sure to complete the delivery today.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "Other colleagues, please also share your plans and progress for today.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "extra_rows": [
      {
        "row": 0,
        "role": "claim",
        "text": "Good morning everyone.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "extra_rows": [
      {
        "row": 0,
        "role": "claim",
        "text": "Good morning everyone.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n03 — natural_audit / medium / full

```text
Hello everyone, today I'm starting a new design task: [Designing a File Storage Solution]. Considering that our system will need to store a large number of supporting documents, reports, etc. in the future, I will focus on comparing Azure Blob and AWS S3. The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack. A preliminary selection recommendation report will be provided early next week.
```

Complete: old False → candidate False.

Lost required content: `r2:basis1`: our system will need to store a large number of supporting documents, reports, etc. in the future

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r1:time1"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r1:time1"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Hello everyone, today I'm starting a new design task: [Designing a File Storage Solution].",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "Considering that our system will need to store a large number of supporting documents, reports, etc.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "in the future, I will focus on comparing Azure Blob and AWS S3.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "The evaluation dimensions will include cost, API ease of use, access permission management, and the difficulty of integration with our existing technology stack.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "A preliminary selection recommendation report will be provided early next week.",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r2:basis1"
    ],
    "missing_claims": [],
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
        "row": 1,
        "role": "claim",
        "text": "Considering that our system will need to store a large number of supporting documents, reports, etc.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      1
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
      }
    ]
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r2:basis1"
    ],
    "missing_claims": [],
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
        "row": 1,
        "role": "claim",
        "text": "Considering that our system will need to store a large number of supporting documents, reports, etc.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      1
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
      }
    ]
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n04 — natural_audit / medium / full

```text
Good morning everyone. Regarding the design of our file storage solution, I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday. From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage, and our other projects are also on AWS. Today, I will start designing the Bucket Policy and directory structure based on S3, for example, isolating by tenant and file type.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r1:time1"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
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
    "missing_claims": [
      "r1:claim",
      "r2:claim",
      "r3:claim",
      "r4:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 1,
        "quote": "Regarding the design of our file storage solution, I conducted a preliminary evaluation of Azure Blob and AWS S3 last Friday.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 1,
          "quote": "last Friday"
        }
      ],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "From the perspective of cost and ecosystem integration, AWS S3 has a slight advantage, and our other projects are also on AWS.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "Today, I will start designing the Bucket Policy and directory structure based on S3, for example, isolating by tenant and file type.",
        "stance": "decision"
      },
      "details": [
        {
          "segment": 3,
          "quote": "for example, isolating by tenant and file type",
          "stance": "decision",
          "kind": "method"
        }
      ],
      "condition": [],
      "basis": [],
      "time": [
        {
          "segment": 3,
          "quote": "Today"
        }
      ],
      "subject": []
    }
  ],
  "ignored": [
    {
      "segment": 0,
      "quote": "Good morning everyone.",
      "kind": "salutation"
    }
  ]
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r2",
        "condition",
        "r2:condition1"
      ]
    ],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r2",
        "condition",
        "r2:condition1"
      ]
    ],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
    ],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n05 — natural_audit / medium / full

```text
Good morning everyone, regarding the file storage solution, the complete technical design document (based on AWS S3) has been uploaded to Confluence. It includes three main parts: bucket permission policies, lifecycle rules, and recommended directory structure. @Mingzhi Li Boss Li, please review it.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Good morning everyone, regarding the file storage solution, the complete technical design document (based on AWS S3) has been uploaded to Confluence.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "It includes three main parts: bucket permission policies, lifecycle rules, and recommended directory structure.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "@Mingzhi Li Boss Li, please review it.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n06 — natural_audit / hard / partial

```text
@Lujian Gao I've finished reviewing the document on the file storage solution. The design is very comprehensive, especially the considerations for tenant data isolation and cost optimization. The proposal is approved and can be finalized.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r3:subject1"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r3:subject1"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "@Lujian Gao I've finished reviewing the document on the file storage solution.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The design is very comprehensive, especially the considerations for tenant data isolation and cost optimization.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "The proposal is approved and can be finalized.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n07 — natural_audit / medium / full

```text
@Yang Zhao Good question. Regarding the "forgot password" process, our main security consideration is to prevent "user enumeration attacks." Therefore, regardless of whether the email entered by the user exists or not, the feedback message should be consistent, such as "If this email address is registered, you will receive an email containing a password reset link," instead of directly prompting "user does not exist." Please ensure the UI copy adheres to this principle.
```

Complete: old False → candidate False.

Lost required content: none

New required content: `r1:claim`: our main security consideration is to prevent "user enumeration attacks."; `r1:condition1`: forgot password; `r2:basis1`: prevent "user enumeration attacks."; `r2:claim`: the feedback message should be consistent; `r2:condition1`: forgot password; `r2:condition2`: regardless of whether the email entered by the user exists or not; `r2:method1`: such as "If this email address is registered, you will receive an email containing a password reset link,"; `r2:method2`: instead of directly prompting "user does not exist."; `r3:claim`: Please ensure the UI copy adheres to this principle; `r3:subject1`: the feedback message should be consistent

Lost correct links: none

New correct links: `r2 → basis → r2:basis1`: prevent "user enumeration attacks."; `r2 → method → r2:method1`: such as "If this email address is registered, you will receive an email containing a password reset link,"; `r2 → method → r2:method2`: instead of directly prompting "user does not exist."

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1",
      "r2:condition1",
      "r2:condition2"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
  },
  "compiled": {
    "complete": false,
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
    "missing_claims": [
      "r1:claim",
      "r2:claim",
      "r3:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:condition1",
      "r2:condition1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
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
    "missing_claims": [
      "r1:claim",
      "r2:claim",
      "r3:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "failed",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "@Yang Zhao Good question.",
        "stance": "question"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "Regarding the \"forgot password\" process, our main security consideration is to prevent \"user enumeration attacks.\"",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "Therefore, regardless of whether the email entered by the user exists or not, the feedback message should be consistent, such as \"If this email address is registered, you will receive an email containing a password reset link,\" instead of directly prompting \"user does not exist.\"",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 1,
          "quote": "our main security consideration is to prevent \"user enumeration attacks.\"",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "Please ensure the UI copy adheres to this principle.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [
        {
          "segment": 2,
          "quote": "Therefore, regardless of whether the email entered by the user exists or not, the feedback message should be consistent, such as \"If this email address is registered, you will receive an email containing a password reset link,\" instead of directly prompting \"user does not exist.\"",
          "kind": "stated"
        }
      ],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "condition",
        "r1:condition1"
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
        "r3",
        "basis",
        "r3:subject1"
      ]
    ],
    "extra_rows": [
      {
        "row": 0,
        "role": "claim",
        "text": "@Yang Zhao Good question.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [
      [
        "r1",
        "condition",
        "r1:condition1"
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
        "r3",
        "basis",
        "r3:subject1"
      ]
    ],
    "extra_rows": [
      {
        "row": 0,
        "role": "claim",
        "text": "@Yang Zhao Good question.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n08 — natural_audit / easy / full

```text
Email received. The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction. @Xinjie Li @Xuexin Yin, please assess the scope of impact on the backend.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r2:recipient1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r2:recipient1"
    ],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 1,
        "quote": "The core requirement is that all accounts marked as `ACCOUNT_STATUS_LOCKED` must be forcibly routed to the `ERR_POLICY_LOCKED_ACCOUNT_V1` policy for frontend interaction.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "@Xinjie Li @Xuexin Yin, please assess the scope of impact on the backend.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": [
    {
      "segment": 0,
      "quote": "Email received.",
      "kind": "salutation"
    }
  ]
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n09 — natural_audit / medium / full

```text
The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`, defined as 'Explicit Status Alert Policy'. It is mainly used for scenarios where an account is locked, requiring explicit interruption of user operations and guidance to manual channels.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "The newly added policy code is `ERR_POLICY_LOCKED_ACCOUNT_V1`, defined as 'Explicit Status Alert Policy'.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "It is mainly used for scenarios where an account is locked, requiring explicit interruption of user operations and guidance to manual channels.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n10 — natural_audit / hard / partial

```text
Received. I've reviewed the document. This strategy will be handled by `ExplicitStateAlertModule`, and the parameter `halt_downstream_triggers` is set to `true`. This means that after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted, right?
```

Complete: old False → candidate False.

Lost required content: `r1:claim`: I've reviewed the document

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r4:caveat1"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim",
      "r4:caveat1"
    ],
    "missing_claims": [
      "r1:claim"
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 2,
        "quote": "This strategy will be handled by `ExplicitStateAlertModule`, and the parameter `halt_downstream_triggers` is set to `true`.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "This means that after the backend triggers this strategy, all downstream automated notifications (emails, SMS) will be halted, right?",
        "stance": "question"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": [
    {
      "segment": 0,
      "quote": "Received.",
      "kind": "salutation"
    },
    {
      "segment": 1,
      "quote": "I've reviewed the document.",
      "kind": "acknowledgement"
    }
  ]
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:claim"
    ],
    "missing_claims": [
      "r1:claim"
    ],
    "missing_edges": [
      [
        "r4",
        "condition",
        "r4:condition1"
      ]
    ],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim"
    ],
    "missing_claims": [
      "r1:claim"
    ],
    "missing_edges": [
      [
        "r4",
        "condition",
        "r4:condition1"
      ]
    ],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r2",
        "r3"
      ]
    ],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n11 — natural_audit / hard / partial

```text
@Xinjie Li Yes, your understanding is completely correct. This is to avoid sending users redundant or potentially confusing automated messages.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:claim"
    ],
    "missing_claims": [
      "r1:claim"
    ],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim"
    ],
    "missing_claims": [
      "r1:claim"
    ],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "@Xinjie Li Yes, your understanding is completely correct.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "This is to avoid sending users redundant or potentially confusing automated messages.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": [
      {
        "node": "r1:claim",
        "expected": [
          "observation"
        ],
        "predicted": [
          "decision"
        ]
      },
      {
        "node": "r2:claim",
        "expected": [
          "observation"
        ],
        "predicted": [
          "decision"
        ]
      }
    ]
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
    "missing_edges": [],
    "incorrect_edges": [],
    "extra_rows": [],
    "extra_claim_rows": [],
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": [
      {
        "node": "r1:claim",
        "expected": [
          "observation"
        ],
        "predicted": [
          "decision"
        ]
      },
      {
        "node": "r2:claim",
        "expected": [
          "observation"
        ],
        "predicted": [
          "decision"
        ]
      }
    ]
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n12 — natural_audit / medium / full

```text
Received, thanks a lot! The data structure looks very clear. I plan to complete the static data integration this morning to ensure the charts render correctly. In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it. @Mingzhi Li
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: `r2 → time → r2:time1`: this morning; `r3 → time → r3:time1`: In the afternoon

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [
      "r1:claim"
    ],
    "missing_claims": [
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r3",
        "r4"
      ]
    ],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [
      "r1:claim"
    ],
    "missing_claims": [
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r3",
        "r4"
      ]
    ],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r3",
        "r4"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r3",
        "r4"
      ]
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Received, thanks a lot!",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "The data structure looks very clear.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "I plan to complete the static data integration this morning to ensure the charts render correctly.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "In the afternoon, I'll start researching dynamic refresh solutions, initially considering WebSocket if the backend supports it.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": [
    {
      "segment": 4,
      "quote": "@Mingzhi Li",
      "kind": "salutation"
    }
  ]
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "extra_rows": [
      {
        "row": 0,
        "role": "claim",
        "text": "Received, thanks a lot!",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r3",
        "r4"
      ]
    ],
    "stance_wrong": [
      {
        "node": "r4:claim",
        "expected": [
          "proposal"
        ],
        "predicted": [
          "decision"
        ]
      }
    ]
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "extra_rows": [
      {
        "row": 0,
        "role": "claim",
        "text": "Received, thanks a lot!",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r3",
        "r4"
      ]
    ],
    "stance_wrong": [
      {
        "node": "r4:claim",
        "expected": [
          "proposal"
        ],
        "predicted": [
          "decision"
        ]
      }
    ]
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n13 — natural_audit / hard / full

```text
@Yunqi Qian Great plan. WebSocket is the best solution, but our message push service isn't fully ready yet. This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds. Once the WebSocket service is stable later, we can upgrade it uniformly. This way, we can avoid blocking your current task.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: `r3 → method → r3:method1`: by requesting the interface every 10 seconds

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [
      "r2:claim"
    ],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [
      "r2:claim"
    ],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "@Yunqi Qian Great plan.",
        "stance": "uncertainty"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "WebSocket is the best solution, but our message push service isn't fully ready yet.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 2,
        "quote": "This task can be implemented using polling for now, for example, by requesting the interface every 10 seconds.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 3,
        "quote": "Once the WebSocket service is stable later, we can upgrade it uniformly.",
        "stance": "proposal"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 4,
        "quote": "This way, we can avoid blocking your current task.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": [
    {
      "segment": 0,
      "quote": "@Yunqi Qian Great plan.",
      "kind": "salutation"
    }
  ]
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "incorrect_edges": [],
    "extra_rows": [
      {
        "row": 0,
        "role": "claim",
        "text": "@Yunqi Qian Great plan.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "incorrect_edges": [],
    "extra_rows": [
      {
        "row": 0,
        "role": "claim",
        "text": "@Yunqi Qian Great plan.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```

## n14 — natural_audit / hard / partial

```text
Okay, Boss Li, understood. Then I'll use the polling solution for now, and I'll adjust the plan.
```

Complete: old False → candidate False.

Lost required content: none

New required content: none

Lost correct links: none

New correct links: none

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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
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
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
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
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
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

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": null
}
```

### bound

```json
{
  "records": [
    {
      "root": {
        "segment": 0,
        "quote": "Okay, Boss Li, understood.",
        "stance": "observation"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    },
    {
      "root": {
        "segment": 1,
        "quote": "Then I'll use the polling solution for now, and I'll adjust the plan.",
        "stance": "decision"
      },
      "details": [],
      "condition": [],
      "basis": [],
      "time": [],
      "subject": []
    }
  ],
  "ignored": []
}
```

```json
{
  "raw": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "text": "Okay, Boss Li, understood.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "compiled": {
    "complete": false,
    "missing_nodes": [],
    "missing_claims": [],
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
        "text": "Okay, Boss Li, understood.",
        "reason": "No full gold semantic unit matched; may be fragment, boilerplate, unsupported or matcher ambiguity"
      }
    ],
    "extra_claim_rows": [
      0
    ],
    "boilerplate_rows": [
      0
    ],
    "duplicate_rows": 0,
    "overmerged_record_pairs": [
      [
        "r1",
        "r2"
      ]
    ],
    "stance_wrong": []
  },
  "status": "annotated",
  "diagnostics": [],
  "finish_reason": "stop"
}
```
