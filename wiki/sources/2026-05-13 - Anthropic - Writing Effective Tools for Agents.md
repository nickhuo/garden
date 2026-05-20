---
type: source
title: "Writing effective tools for agents — with agents"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - tool-use
  - tool-design
  - aci
source_type: article
author: Anthropic Engineering
date_published: 2026-05-13
url: https://www.anthropic.com/engineering/writing-tools-for-agents
confidence: high
status: developing
related:
  - "[[ACI - Agent-Computer Interface]]"
  - "[[Tool Use Examples]]"
  - "[[Programmatic Tool Calling]]"
  - "[[Tool Search Tool]]"
sources:
  - "[[.raw/articles/2026-05-13 - Anthropic - Writing Effective Tools for Agents.md]]"
key_claims:
  - Tool definitions are often the highest-leverage improvement surface for agent performance — more impactful than prompt tuning
  - Good tool descriptions answer "when should I use this (and when should I NOT)"
  - Agents can critique and improve their own tool definitions — closing a self-improvement loop
  - Field-level descriptions in JSON Schema are as important as tool-level descriptions
  - Error messages are part of the tool interface and should guide recovery
  - "The meta-tooling pattern: a tool-quality agent generates test invocations, evaluates correctness on a fresh Claude instance, proposes improvements"
---

# Writing effective tools for agents — with agents

**Source:** [Anthropic Engineering](https://www.anthropic.com/engineering/writing-tools-for-agents)
**Author:** Anthropic Engineering
**Published:** 2026-05-13

## Summary

A practitioner-focused guide on writing high-quality tool definitions for LLM agents, plus a meta-workflow where agents critique and improve their own tools. The article extends Anthropic's prior [[ACI - Agent-Computer Interface]] framing with concrete recipes for names, descriptions, schemas, examples, and error messages — and introduces the **tool-critique agent** and **meta-tooling** patterns.

## Key claims

1. **Tool definitions > prompts.** In Anthropic's SWE-bench work, more time was spent optimizing tools than the overall prompt. Tool definitions are the highest-leverage improvement surface for agent reliability.

2. **Names should be verb-first and unambiguous.** `search_files`, `create_ticket`, `get_user_by_email` — convey action + object. Distinguishable from each other is as important as individual clarity.

3. **Descriptions answer "when to use / when NOT to use."** One sentence on what the tool does, explicit guidance on when to avoid it, relationship to similar tools, and key constraints (rate limits, side effects).

4. **Schema is underused.** Beyond required/optional: use `enum` for valid string values, `description` on every field, `minimum`/`maximum`/`maxLength` for valid ranges.

5. **Examples teach what schemas cannot.** Date formats, ID conventions, which optional fields co-occur — these are learned by demonstration. 1-5 realistic examples per tool. See [[Tool Use Examples]].

6. **Errors are part of the interface.** Agents fail forward — they read error messages to decide recovery. Bad: `"Invalid input"`. Good: `"Invalid date format: '2024-11-6'. Expected YYYY-MM-DD (e.g., '2024-11-06')."`.

7. **Agents can critique tool definitions.** Show Claude the tool def, ask it to identify ambiguities and misuse risks, have it propose improvements. Works because the task is well-specified and Claude has training on tool-calling patterns.

8. **The meta-tooling pattern.** A dedicated tool-quality agent: (a) takes a tool def, (b) generates test invocations including edge cases, (c) evaluates whether a *fresh* Claude instance uses the tool correctly given only the definition, (d) proposes targeted improvements. Typically converges in 1-2 rounds.

## Common failure modes documented

| Failure mode | Description | Fix |
|---|---|---|
| "Obvious to humans" | Implicit format conventions not stated (e.g., `USR-XXXXX` ID format) | Make implicit conventions explicit in description or examples |
| Too many similar tools | Agents burn tokens disambiguating | Consolidate tools; add "use X not Y when..." |
| "Success is silent" | Generic `{"status": "success"}` leaves agent unable to verify | Return enough confirmation to verify without a follow-up call |
| Hallucinated parameters | Required fields get filled with plausible-sounding hallucinations | Make optional fields optional; add examples of valid values |

## Practical starting points (Anthropic's ranked list)

1. Write descriptions first — worth more than a perfect schema
2. Add field-level `description` to every parameter
3. Add 2-3 examples (common case, edge case, minimal valid invocation)
4. Test by giving Claude *only* the tool def and seeing if it calls correctly
5. Design error messages before success cases

## Connections

- Extends: [[ACI - Agent-Computer Interface]] — this article is the most concrete ACI practice guide to date
- Mechanism: [[Tool Use Examples]] — `input_examples` as a first-class tool-def component
- Self-improvement pattern: the tool-critique agent closes the loop on [[ACI - Agent-Computer Interface]] (agent participates in optimizing its own tools) — extending the 40% improvement pattern from [[2025-06-13 - Anthropic - How we built our multi-agent research system]]
- Tangential: [[Programmatic Tool Calling]] — return-format precision now doubly load-bearing (for code parsing AND for agent recovery from errors)
- Tangential: [[Tool Search Tool]] — discoverability depends on name/description quality, making this article's naming rules a prerequisite

## What's new vs prior Anthropic sources

| Prior source | New here |
|---|---|
| [[2024-12-19 - Anthropic - Building Effective Agents]] — introduced ACI framing, "treat docs like a docstring for a junior engineer" | Adds concrete failure modes taxonomy; adds **agent-as-tool-critic** workflow |
| [[2025-11-24 - Anthropic - Advanced Tool Use]] — introduced `input_examples`, PTC, Tool Search | Adds full description/schema/error design guide; operationalizes the "test your tool with Claude" heuristic |
| [[2025-06-13 - Anthropic - How we built our multi-agent research system]] — agent-rewrites-tool-descriptions → 40% faster | Adds the **meta-tooling loop** (tool-quality agent evaluating fresh Claude instances), making the workflow reproducible |
