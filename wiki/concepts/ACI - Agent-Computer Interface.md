---
type: concept
title: ACI - Agent-Computer Interface
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- tool-design
- framing
status: developing
related: []
sources:
- "[[2024-12-19 - Anthropic - Building Effective Agents]]"
- "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
- "[[2025-09-29 - Anthropic - Effective context engineering for AI agents]]"
- "[[2025-07-18 - Manus - Context Engineering for AI Agents]]"
- "[[2025-11-24 - Anthropic - Advanced Tool Use]]"
- "[[2026-05-13 - Anthropic - Writing Effective Tools for Agents]]"
- "[[2026-04 - Anthropic - Claude Code Auto Mode]]"
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
aliases:
- ACI
- Agent-Computer Interface
_legacy_source_count: 6
---

# ACI — Agent-Computer Interface

## Summary

Anthropic's framing in [[Building Effective Agents]]: tools-for-LLMs deserve the same engineering investment as **HCI** (human-computer interface) — schemas, naming, error messages, and examples shape model performance dramatically.

## Key claims (verbatim)

> "as much effort goes into human-computer interfaces (HCI), [we] plan to invest just as much effort in creating good agent-computer interfaces (ACI)."

> "While building our agent for SWE-bench, we actually spent more time optimizing our tools than the overall prompt."

## Design principles (Anthropic)

- Treat tool docs like a docstring for a junior engineer — they will read it once and use the tool.
- **Poka-yoke** the tool — design schemas so misuse is hard (e.g., require absolute paths over relative ones).
- Test tool design empirically — count failure modes, iterate.

## Tool-testing agent pattern (per Anthropic 2025-06)

In [[How we built our multi-agent research system]], Anthropic surfaces a concrete ACI optimization pattern: **use an LLM agent to critique and improve your tool descriptions**. They report that rewriting tool descriptions (apparently with agent assistance) yielded **40% faster task completion** on their research workload.

Anchor claim: "Prompt engineering [for agents] = teaching the agent to think like the orchestrator does." Tool descriptions are part of that teaching.

Implication: ACI design isn't a one-shot human design exercise — it's an iterative loop where the agent itself becomes a participant in optimizing its own tools.

## Tool docs ARE context (per Anthropic 2025-09)

[[Effective context engineering for AI agents]] reframes ACI as part of the **attention budget**, not a separate "tool design" concern. Two consequences:

- **Tool docs are not metadata; they're load-bearing context.** Every word in a tool description competes for the same attention budget as the user's task. Verbose tool docs degrade reasoning the same way verbose prompts do.
- **Minimally overlapping tool surfaces** — when two tools do similar things, the model spends attention disambiguating. Anthropic's rule: design tool surfaces so each tool has a clear, non-overlapping purpose. Consolidate, don't proliferate.

This extends ACI from "good tool docs" to "tool docs as part of a shared context economy."

## Prefix-grouped action names as ACI design (per Manus 2025-07)

[[2025-07-18 - Manus - Context Engineering for AI Agents]] surfaces a subtle but load-bearing ACI design rule: **group action names by prefix** (`browser_*` for browser tools, `shell_*` for command-line tools, etc.) so that **decoding-time constraint (logit masking) can be expressed as a prefix match** without a stateful logits processor.

This makes ACI naming a load-bearing choice for inference-time discipline, not just a readability choice:

- Prefix groups enable [[Logit Masking]] via response prefill (e.g., prefill `{"name": "browser_` to restrict the next action to browser tools)
- This in turn enables static-action-space designs to scale ([[KV-Cache Discipline]] preserved, no dynamic tool churn)
- The naming convention is therefore **the load-bearing primitive** behind Manus's whole decoding-control architecture

The discipline rule: choose tool names such that a few characters of prefix carve a usefully-constrained subset of the action space.

## Inline examples + code-callable tools + discoverable tools (per Anthropic 2025-11)

[[2025-11-24 - Anthropic - Advanced Tool Use]] expands ACI in three concrete directions, each with its own concept page:

- **[[Tool Use Examples]]** (`input_examples`) — tool defs now include sample invocations that teach format conventions and parameter correlations JSON Schema cannot express. Internal accuracy 72→90% on complex parameter handling.
- **[[Programmatic Tool Calling]]** (PTC, via `allowed_callers`) — tools become callable from sandboxed code, not just from inference. ACI must now spec **return-format precision** (parsing target) in addition to invocation semantics.
- **[[Tool Search Tool]]** (`defer_loading: true`) — tool defs become **discoverable** on demand. ACI now includes "search-quality" as a first-class concern: names + descriptions must be discoverable by keyword/embedding-based matching, not just readable.

Three implications for ACI design discipline:

1. Tool **return formats** are now load-bearing (PTC needs them for parsing); document data shape, units, error structure precisely.
2. Tool **discoverability** is a distinct axis from tool **selectability** — a well-named tool that doesn't surface in keyword search is invisible to a Tool Search-enabled agent.
3. **Examples > schemas** for nuanced parameter usage; treat them as part of the tool def, not separate documentation.

## Tool-critique agent and meta-tooling loop (per Anthropic 2026-05)

[[2026-05-13 - Anthropic - Writing Effective Tools for Agents]] is the most concrete ACI practice guide to date. Key additions:

**Ranked design hierarchy:** descriptions > field-level schema descriptions > examples > error messages > name. Descriptions answer "when to use / when NOT to use" — one sentence on function, explicit anti-use cases, relationship to similar tools, key constraints.

**Failure modes taxonomy** (the "what goes wrong" complement to the positive principles):

| Failure | Cause | Fix |
|---|---|---|
| "Obvious to humans" | Implicit format conventions not stated | Make conventions explicit or add examples |
| Too many similar tools | Agent burns tokens disambiguating | Consolidate; add mutual exclusion guidance |
| "Success is silent" | Generic `{"status":"success"}` returns | Return verifiable confirmation |
| Hallucinated parameters | Required fields fill with plausible guesses | Make optional fields actually optional; add valid-value examples |

**Tool-critique agent pattern:** give Claude a tool definition, ask it to identify ambiguities and misuse risks, have it propose improvements. Works because the task is well-specified — Claude has training on tool-calling patterns and the evaluation criterion is clear (can a fresh Claude instance use this correctly?).

**Meta-tooling loop:** a dedicated tool-quality agent (a) takes a tool def, (b) generates test invocations including edge cases, (c) evaluates a *fresh* Claude instance's correctness given only the def, (d) proposes improvements. Typically converges in 1-2 rounds. This makes tool quality a self-improving system rather than a one-shot design exercise.

**"Test your tool with Claude"** heuristic: give Claude only the tool definition (no additional context) and observe whether it can use the tool correctly. Gaps reveal what's missing. This is the simplest entry point into the meta-tooling pattern.

## Permission layer as ACI (per Anthropic 2026-04 auto mode)

[[2026-04 - Anthropic - Claude Code Auto Mode]] extends ACI into the **permission layer**. The [[Permission Classifier]] in [[Claude Code]] auto mode is itself an ACI design artifact: it determines which tool calls are safe to route without human intervention, based on tool category, parameters, and conversation context.

Key ACI implication: **the permission system is part of the agent-computer interface design**, not an afterthought. A well-designed tool surface makes the classifier's job easier — tools with clear, non-overlapping purposes are easier to classify correctly. Verbose, ambiguous tool defs create classification uncertainty just as they create model-reasoning uncertainty.

The operator policy config (`allowedTools`, `blockedTools`, `pathRestrictions`) is the ACI between the operator and the classifier — the interface through which humans express their risk tolerance without writing a classifier themselves.

## System-layer ACI (per Anthropic 2026-04)

[[Scaling Managed Agents]] extends ACI further still — from the tool layer to the **infrastructure layer**. The interfaces between Brain, Hands, and Session in a [[Meta-Harness]] are themselves ACI:

- `execute(name, input) → string` is the ACI between brain and any sandbox
- `getEvents()` is the ACI between brain and the durable session

The same design discipline applies: minimal surface, clear semantics, error messages that help the brain recover. Good system-layer ACI is what makes harnesses replaceable cattle instead of nursed pets.

## Connections

- Tool layer protocol: [[MCP]]
- Used by: [[Augmented LLM]] · [[Autonomous Agents]] · [[Orchestrator-Workers]] · [[Multi-Agent Systems]]
- Context-budget perspective: [[Context Engineering]] · [[Token Economics]] · [[KV-Cache Discipline]]
- Enables: [[Just-in-Time Context Retrieval]] · [[Logit Masking]] (prefix-grouped names enable decode-time masking) · [[Tool Search Tool]] (search-quality of names/descriptions) · [[Programmatic Tool Calling]] (return-format precision becomes load-bearing)
- ACI mechanisms: [[Tool Use Examples]] (`input_examples` field as ACI primitive)
- System-layer instance: [[Meta-Harness]] · [[Session as Event Log]]

## Open questions

- Are there general-purpose ACI design heuristics that generalize across domains, or is each tool domain bespoke?
- Should tool design draw from API design literature (REST, GraphQL) or is the constraint genuinely different?
- The 40% number is from one workload — does tool-testing-agent yield similar gains across different domains?
- "Minimal overlap" is qualitative — is there a quantitative measure (e.g., schema-similarity threshold) for when tools collide?

## Sources

- [[Building Effective Agents]] (Anthropic, 2024-12-19)
- [[How we built our multi-agent research system]] (Anthropic, 2025-06-13)
- [[Effective context engineering for AI agents]] (Anthropic, 2025-09-29)
- [[Scaling Managed Agents]] (Anthropic, 2026-04-08)
- [[2025-07-18 - Manus - Context Engineering for AI Agents]] (Manus, 2025-07-18)
- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic, 2025-11-24)
- [[2026-05-13 - Anthropic - Writing Effective Tools for Agents]] (Anthropic, 2026-05-13)
- [[2026-04 - Anthropic - Claude Code Auto Mode]] (Anthropic, April 2026)
