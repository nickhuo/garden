---
type: concept
title: "Context Assembly Pipeline"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - infrastructure
status: seed
complexity: intermediate
domain: ai-agents
aliases:
  - context construction pipeline
  - prompt assembly
related:
  - "[[Context Engineering]]"
  - "[[KV-Cache Discipline]]"
  - "[[Long-Horizon Context Management]]"
  - "[[Error Trace Retention]]"
sources:
  - "[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]"
---

# Context Assembly Pipeline

## Definition

The subsystem responsible for constructing the final input context sent to the model. Typically concatenates multiple pieces: system prompt, conversation history, retrieved documents (RAG), tool results, and any injected metadata. Each component has its own source and may require preprocessing.

## Why It's a Critical Path

Small errors in context assembly produce outputs that appear coherent but are semantically wrong — the model responds to the corrupted context it received, not the context the developer intended. Unlike hard errors (e.g., an exception or timeout), corrupted context produces soft failures that evade error-rate monitoring.

## Real-World Failure (Anthropic, 2026)

A bug in Anthropic's context assembly code caused a chunk-boundary condition: when the system prompt was exactly a multiple of the internal buffer chunk size (4,096 bytes), the last bytes of the system prompt were overwritten by the first bytes of retrieved documents. The model received:

```
[system prompt ... truncated] [start of retrieval results] [conversation history]
```

instead of:

```
[system prompt] [retrieved docs] [conversation history]
```

The result was coherent but wrong responses. This was detected by user reports, not automated monitoring — because error rates were normal.

## Corrective Patterns

1. **Fuzz/property-based testing** — generate inputs at and around chunk boundaries to exercise boundary conditions systematically.
2. **LLM-as-judge on production traffic** — semantic evaluation on a sample of live responses can catch quality regressions invisible to error-rate metrics. See [[LLM-as-Judge Evaluation]].
3. **Static analysis on byte-level operations** — flag code paths involving buffer operations without explicit boundary tests.

## Connections

- [[Context Engineering]] — context assembly is the implementation layer beneath context engineering strategy.
- [[LLM-as-Judge Evaluation]] — the detection mechanism Anthropic is deploying in response to this incident.
- [[Long-Horizon Context Management]] — multi-turn, multi-document contexts are more complex to assemble and more likely to hit boundary conditions.
- [[Error Trace Retention]] — preserving assembly steps in logs aids debugging when corruption is suspected.
