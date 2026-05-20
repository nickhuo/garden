---
type: concept
title: "Think Tool"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - tool-use
  - reasoning
status: developing
related:
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Tool Use Examples]]"
  - "[[Programmatic Tool Calling]]"
  - "[[Context Engineering]]"
  - "[[Error Trace Retention]]"
  - "[[KV-Cache Discipline]]"
  - "[[tau-bench]]"
  - "[[Pass^k Reliability Metric]]"
sources:
  - "[[2025-03-20 - Anthropic - The Think Tool]]"
complexity: intermediate
domain: ai-agents
aliases:
  - think tool
  - think() tool
  - scratchpad tool
  - in-loop reasoning tool
---

# Think Tool

## What it is

A **no-op tool** added to an agent's tool set that gives the model a designated scratchpad for explicit, structured reasoning mid-task. When Claude calls `think`, it writes a `thought` string; the tool returns an empty response and takes no external action. The thought is preserved in the tool-call transcript.

Introduced (as an explicit recommendation) by Anthropic in their engineering blog post on complex tool use.

### Schema

```json
{
  "name": "think",
  "description": "Use the tool to think about something. It will not be visible to the user and will not change state. Use it when you need complex reasoning or when you're unsure about the right action.",
  "input_schema": {
    "type": "object",
    "properties": {
      "thought": {
        "type": "string",
        "description": "A thought to think about."
      }
    },
    "required": ["thought"]
  }
}
```

## The gap it fills

In a standard tool-use loop, the model cycles between: receive tool result → produce next tool call or final answer. There is no explicit slot for **in-loop reasoning** — deliberation that draws on prior tool outputs before committing to the next action.

Without a scratchpad:
- The model must "think" in the token budget allocated to the assistant turn before a tool call — but this is the same turn that becomes the tool call itself.
- Complex policy application (checking multiple conditions from a long document against a current state) happens implicitly in the model's decoding.
- Errors in this reasoning are invisible; there's no log to debug.

With the think tool, the model can:
1. Call `think` with a reasoning trace ("The policy says X. The current state is Y. Therefore I should do Z.")
2. Reference its own earlier think calls as prior context
3. Act on the conclusion

## Relation to extended thinking

| Dimension | Extended Thinking | Think Tool |
|---|---|---|
| Location | Model-internal (hidden CoT) | In transcript (tool call) |
| Visibility | Not observable by developer | Fully observable, debuggable |
| Referenceability | Not re-readable as context | Readable as prior tool output |
| Requires special mode | Yes | No — any tool-use setup |
| Best for | Up-front reasoning before tools | In-loop reasoning between tool calls |

Both can be active simultaneously. They are **complementary**, not competing.

## tau-bench evidence

Tested on [[tau-bench]] (Sierra's tool-agent-user interaction benchmark):

- **τ-airline** (policy-heavy, complex membership × cabin × baggage rule interactions): ~6–7% absolute pass^1 improvement
- **τ-retail** (less policy-heavy): ~4% absolute pass^1 improvement

Pattern: gains scale with policy complexity. The think tool is most valuable precisely where structured rule reasoning is required before each action — τ-airline being the harder, more policy-dense domain.

For τ-bench baseline numbers and pass^k reliability, see [[tau-bench]] and [[Pass^k Reliability Metric]].

## When to use

**Add the think tool when:**
- Agent follows complex instructions or long policy documents
- Tasks require multi-condition checking before acting
- Tool outputs are ambiguous and need interpretation before the next step
- Error recovery requires reasoning about what went wrong and what to try
- The agent runs many tool calls per task (long-horizon)

**Skip the think tool when:**
- Tasks are simple and single-step
- Latency is critical (think calls add tokens)
- The model already has extended thinking enabled for up-front reasoning and tasks don't require mid-loop deliberation

## ACI framing

The think tool is an [[ACI - Agent-Computer Interface]] extension. ACI covers the full surface of how agents interface with computer systems via tools — schemas, naming, documentation, error messages, examples. The think tool adds a **reasoning primitive** to this interface: the agent can now do deliberate work without side effects, producing a clean separation between "plan step" and "execute step."

This parallels good software engineering — PLAN, then ACT — but made explicit in the tool contract.

## Context engineering angle

From a [[Context Engineering]] perspective, the think tool **shapes what appears in the context window** between action steps. A `think` call turns implicit reasoning (zero bits in context) into explicit tokens (readable prior context). This is a form of self-directed context enrichment: the model writes what it needs to see in order to act correctly.

Related: [[Error Trace Retention]] (keeping failed attempts visible) and [[Session as Event Log]] (treating the full transcript as event data). A session with think calls is a richer, more legible event log.

## Connections

- Extends: [[ACI - Agent-Computer Interface]]
- Shapes: [[Context Engineering]]
- Complements: [[Error Trace Retention]], [[Session as Event Log]]
- Evaluated on: [[tau-bench]] (see [[Pass^k Reliability Metric]])
- Sister features: [[Tool Use Examples]], [[Programmatic Tool Calling]], [[Tool Search Tool]]
- Contrast: [[Prompt Chaining]] (orchestration-level structure vs in-loop reasoning)
- Cache note: think calls add tokens between tool result and next tool call — may affect [[KV-Cache Discipline]] for long-running loops. Monitor.

## Open questions

- Does think tool raise pass^k (reliability) or only pass^1 (single-trial accuracy)? The τ-bench results shown are pass^1 — reliability under repeated trials is unquantified.
- Verbosity risk: can models over-think, generating long redundant chains that add latency without benefit? Is there an optimal think call length?
- Composability with extended thinking: do they yield additive gains, or does one substitute for the other?
- Cache cost: each think call produces tokens that may break KV-cache alignment in a long loop. What is the actual token overhead at scale?
