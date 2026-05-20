---
type: source
title: "The \"think\" tool: Enabling Claude to stop and think in complex tool use situations"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - tool-use
  - reasoning
status: developing
related:
  - "[[Think Tool]]"
  - "[[tau-bench]]"
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Tool Use Examples]]"
  - "[[Programmatic Tool Calling]]"
  - "[[Pass^k Reliability Metric]]"
source_type: article
author: Anthropic
date_published: 2025-03-20
url: https://www.anthropic.com/engineering/claude-think-tool
confidence: high
key_claims:
  - "The think tool is a no-op tool that gives Claude a scratchpad for explicit mid-loop reasoning, visible in the tool-call transcript."
  - "Unlike extended thinking (model-internal), think tool outputs appear in conversation history and can be referenced in subsequent steps."
  - "tau-bench airline improvement ~6-7% absolute on pass^1; retail improvement ~4% — gains largest where policy complexity is highest."
  - "Recommended for any agentic loop requiring complex instruction or policy following; not recommended for simple tasks where latency matters."
sources:
  - "[[.raw/articles/2025-03-20 - Anthropic - The Think Tool.md]]"
---

# Source: The "think" tool

**Author:** Anthropic Engineering  
**URL:** https://www.anthropic.com/engineering/claude-think-tool  
**Published:** 2026-05-13  
**Confidence:** High (first-party Anthropic engineering post with benchmark data)

## Summary

Anthropic introduces the **`think` tool** — a no-op tool added to an agent's tool set that gives Claude a dedicated scratchpad for structured reasoning mid-task. When Claude calls `think`, it writes out a `thought` string; the tool returns an empty response. The thought appears in the tool-call transcript, making it observable, debuggable, and referenceable in subsequent steps.

This fills a gap in the standard tool-use loop: Claude has no explicit slot for "reason before acting" between receiving a tool result and deciding the next action. The think tool creates that slot without requiring a special model mode.

## Key claims

1. **No-op schema** — `{ name: "think", input_schema: { thought: string } }`. Returns `""`. Zero side effects.

2. **Visibility advantage over extended thinking** — Extended thinking is model-internal CoT. The think tool's output is in the conversation transcript: auditable, debuggable, and usable as prior context in subsequent reasoning.

3. **tau-bench results** — tested on both τ-retail and τ-airline:
   - τ-airline (policy-heavy): ~6–7% absolute pass^1 improvement
   - τ-retail (less policy-heavy): ~4% absolute pass^1 improvement
   - Pattern: gains scale with policy complexity, as expected for a scratchpad that helps apply rules.

4. **Use-case profile** — most valuable for: multi-step policy application, complex tool output interpretation, error recovery reasoning, constraint checking before action. Least valuable for: simple single-step tasks, latency-critical paths.

5. **Complementary, not competing** — sits alongside extended thinking (pre-loop up-front reasoning) and [[Prompt Chaining]] (orchestration-level structure). Fills the **in-loop** gap.

## Connections

- [[Think Tool]] — concept page for this pattern
- [[tau-bench]] — benchmark used for evaluation; see updated "Known successors" section
- [[Pass^k Reliability Metric]] — the improvement metric; think tool raises pass^1 on policy-heavy tasks
- [[ACI - Agent-Computer Interface]] — think tool is an ACI extension: adding a reasoning primitive to the tool contract
- [[Tool Use Examples]] · [[Programmatic Tool Calling]] · [[Tool Search Tool]] — sister advanced tool use features
- [[Context Engineering]] — think tool is a context shaping intervention: surfaces reasoning into transcript context
- [[Error Trace Retention]] — think calls during error recovery are a form of trace retention

## Open questions

- Does the think tool help with pass^k (reliability across repeated trials), or only pass^1 (single-trial accuracy)?
- How does it interact with [[KV-Cache Discipline]] — each think call produces tokens that may break cache alignment. Cost analysis?
- Does combining think tool + extended thinking yield additive gains, or do they substitute?
- Is there a risk of verbose over-thinking — model producing long, redundant think calls that add latency without improving outcomes?
