---
source_url: https://www.anthropic.com/engineering/claude-think-tool
title: "The \"think\" tool: Enabling Claude to stop and think in complex tool use situations"
author: Anthropic
date_fetched: 2026-05-13
type: raw
---

# The "think" tool: Enabling Claude to stop and think in complex tool use situations

> Source: https://www.anthropic.com/engineering/claude-think-tool
> Fetched: 2026-05-13

## Summary (raw capture)

Anthropic engineering blog post describing the "think" tool — a special no-op tool added to Claude's tool set that allows Claude to perform explicit, structured intermediate reasoning during agentic tasks without taking any external action.

## Key content

### The problem

When Claude operates as an agent using tools in complex multi-step tasks, it must simultaneously:
1. Track what has happened so far (observations from previous tool calls)
2. Apply complex policy rules (often long documents)
3. Reason about what action to take next

The challenge: Claude's reasoning naturally happens in its response tokens, but when in a tool-use loop, the model is expected to either call a tool or produce a final answer. There is no explicit slot for "think before you act."

### The solution: the think tool

A `think` tool is added to the tool set with the following schema:

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

The tool returns an empty string. It is a **no-op** — it does nothing except give Claude a place to write out reasoning that becomes part of the tool-call transcript. The model can then read its own think calls as prior context in the conversation.

### Why not extended thinking?

Extended thinking (Claude's built-in chain-of-thought capability) is model-internal and not visible in the tool-call transcript. The `think` tool differs in that:
- The thought appears as an explicit tool call in the conversation history
- Subsequent reasoning can reference earlier `think` call outputs
- It is fully observable and debuggable by developers
- It works within any tool-use setup without requiring a special model mode

### tau-bench results

Anthropic tested the think tool on **τ-bench** (Sierra's tool-agent-user benchmark):

- **τ-retail**: moderate improvement (~4% absolute on pass^1)
- **τ-airline**: larger improvement (~6-7% absolute on pass^1), because airline is more policy-heavy and requires more explicit rule reasoning

The improvement is most pronounced on tasks that require applying complex policy rules — exactly the cases where a "scratchpad" to work through the rules before committing to an action is most valuable.

### When the think tool helps most

1. **Multi-step policy application** — tasks requiring interpretation of long policy documents where the agent must check multiple conditions before acting
2. **Tool output interpretation** — parsing complex or ambiguous tool responses before deciding next step
3. **Error recovery** — reasoning about what went wrong and how to recover without losing state
4. **Constraint checking** — verifying that a planned action satisfies all constraints before executing

### When it doesn't help much

- Simple single-step tasks where the action is obvious
- Tasks with no policy complexity
- Cases where latency is critical (think adds a small number of tokens)

### Implementation guidance

Anthropic recommends:
- Add the think tool to any agentic setup where the agent must follow complex instructions or policies
- Do NOT provide the think tool when tasks are straightforward — unnecessary think calls add latency
- The tool is most valuable when the agent operates in a loop with many tool calls per task
- Prompt the model to use think before and after tool calls that are likely to produce complex results

### Connection to broader reasoning strategy

The think tool is positioned as complementary to (not a replacement for):
- **Extended thinking** — model-internal CoT, better for up-front reasoning before any tools are called
- **Tool Use Examples** — teaching correct parameter formatting
- **Prompt Chaining** — structuring multi-step workflows at the orchestration level

The think tool fills the gap: **in-loop structured reasoning** that can reference prior tool outputs and plan next actions.

## Raw key claims (verbatim / near-verbatim)

1. "The think tool gives Claude a dedicated space to reason through complex situations during tool use, similar to a scratchpad."
2. "Unlike extended thinking, the think tool's output appears in the conversation history and can be referenced in subsequent reasoning steps."
3. Tau-bench improvement: notable on airline domain (policy-heavy), modest on retail domain.
4. "We recommend adding the think tool to any agentic setup where the agent must follow complex instructions or policies."
5. The think tool is a no-op: it takes a string `thought` and returns an empty response.
