---
type: concept
title: Logit Masking
created: 2026-05-10
updated: 2026-05-10
tags:
- ai-agents
- action-space
- decoding
- context
status: developing
related: []
sources:
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
aliases:
- Action Space Masking
- Constrained Decoding for Tool Selection
_legacy_source_count: 1
---

# Logit Masking

## Summary

Per [[2025-07-18 - Manus - Context Engineering for AI Agents]]: a technique for constraining an agent's action space **without modifying tool definitions**. Instead of dynamically adding/removing tools (which breaks KV-cache and creates dangling references), keep all tools loaded and **mask the token logits during decoding** to permit only the subset valid at the current state.

Manus pairs this with a **context-aware state machine** that drives which tools are maskable at each step, plus a **consistent action-name prefix convention** (`browser_*`, `shell_*`) so masking can be done on a prefix match without a stateful logits processor.

## Why mask instead of remove

Two failure modes of dynamic action spaces, both from Manus's experiments:

1. **KV-cache invalidation.** Tool definitions live near the front of the context. Any change ripples the cache invalidation forward through the whole conversation. See [[KV-Cache Discipline]].
2. **Dangling references.** Previous actions and observations may reference tools no longer defined. Without constrained decoding, this leads to schema violations and hallucinated actions.

Masking sidesteps both: the tool definitions never change (cache stays valid), past references stay grounded, and the model is *redirected* rather than reconfigured.

## Mechanism (Hermes function-calling format, NousResearch)

Three modes of function calling, each implemented via response prefill:

| Mode | Behavior | Prefill |
|---|---|---|
| Auto | Model may call a function or not | `<|im_start|>assistant` |
| Required | Must call a function, any one | `<|im_start|>assistant<tool_call>` |
| Specified | Must call from a specific subset | `<|im_start|>assistant<tool_call>{"name": "browser_` |

The "Specified" mode is the powerful one: by prefilling to the start of a tool-name prefix, you collapse the next-token distribution onto a prefix-grouped subset without touching the tool list itself.

## Design pattern: prefix-grouped action names

Manus deliberately groups action names by prefix — all browser tools start with `browser_`, all command-line tools with `shell_`, and so on. This makes prefix-based masking trivially expressible: prefill `{"name": "browser_` to restrict the next action to browser tools at the appropriate state.

This is a clear example of **ACI design serving inference-time constraint discipline** — the naming convention isn't aesthetic; it's load-bearing for the masking strategy. See [[ACI - Agent-Computer Interface]].

## Connections

- Direct alternative to: [[Tool Search Tool]] (dynamic tool loading)
  > [!warning] Contradicts [[Tool Search Tool]]
  > Manus's position: don't change the action space mid-loop, mask instead. Anthropic's [[Tool Search Tool]] (Nov 2025): the action space *should* change mid-loop, and infra (cacheability via deferred-load) makes it safe. The collision is the load-bearing source of [[Static Action Spaces vs Dynamic Tool Discovery]].
- Preserves: [[KV-Cache Discipline]]
- Requires: prefix-grouped naming → [[ACI - Agent-Computer Interface]]
- Implements: a state machine over the conversation context (Manus-specific)

## When this is the right move

- You control the inference stack (self-hosted or platform-supported logits processors)
- Action space is large but bounded — too big to fit naively in prompt, but enumerable
- KV-cache hit rate dominates your unit economics
- You're already running an outer state machine over the agent loop (e.g., for safety, gating, or workflow phases)

## When this fails

- Hosted API without logits-bias / response-prefill exposure
- Action space is genuinely unbounded (user-installable tools, MCP marketplaces with thousands of long-tail tools) — masking can't scale to "find me the right tool"; this is where [[Tool Search Tool]]-style discovery wins
- Tool semantics overlap heavily — prefix grouping doesn't carve clean buckets

## Open questions

- Does this work over Anthropic's Messages API in 2026? Anthropic supports response prefill but not arbitrary logit biasing — does Manus's masking translate, or does it require self-hosting?
- How does the state machine itself get designed — by hand, or learned? Manus describes it as hand-built.
- At what action-space size does prefix-grouping fall apart? `browser_*` works at 20 tools; what about 2000?
- Hybrid approach — is there a wiki-worthy synthesis where Tool Search Tool finds the relevant subset, then masking constrains within that subset?

## Sources

- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (2025-07-18)
