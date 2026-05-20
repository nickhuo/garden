---
type: concept
title: Tool Use Examples
created: 2026-05-10
updated: 2026-05-13
tags:
- ai-agents
- tool-design
- few-shot
- aci
status: developing
related: []
sources:
- "[[2025-11-24 - Anthropic - Advanced Tool Use]]"
- "[[2024-12-19 - Anthropic - Building Effective Agents]]"
- "[[2026-05-13 - Anthropic - Writing Effective Tools for Agents]]"
aliases:
- input_examples
- Tool Examples
- Few-Shot in Tool Definitions
_legacy_source_count: 1
---

# Tool Use Examples

## Summary

Per [[2025-11-24 - Anthropic - Advanced Tool Use]]: a new field (`input_examples`) on tool definitions that lets the tool author provide sample invocations directly inline with the schema. The function is **closing the gap between what JSON Schema can express (structure: types, required fields, enums) and what callers need to know (usage: format conventions, parameter correlations, when to populate optional fields)**.

Anthropic reports a 72%→90% improvement on complex parameter handling accuracy with examples in place.

## What schemas can't express

JSON Schema can declare: this field is a string. It cannot declare: this field is a date that should be formatted `YYYY-MM-DD` (vs `Nov 6, 2024` vs ISO 8601), or that this field is an ID with format `USR-XXXXX` (vs UUID vs bare integer), or that `escalation.sla_hours` correlates with `priority` ("critical" implies ≤4h).

These usage patterns are exactly what trips up tool-calling agents — they generate structurally-valid JSON that's semantically wrong. Examples close the gap by demonstration.

## The pattern

A small array of complete sample invocations attached to the tool def:

```json
{
  "name": "create_ticket",
  "input_schema": { ... },
  "input_examples": [
    {
      "title": "Login page returns 500 error",
      "priority": "critical",
      "labels": ["bug", "authentication", "production"],
      "reporter": {"id": "USR-12345", "name": "Jane Smith", "contact": {"email": "...", "phone": "..."}},
      "due_date": "2024-11-06",
      "escalation": {"level": 2, "notify_manager": true, "sla_hours": 4}
    },
    {
      "title": "Add dark mode support",
      "labels": ["feature-request", "ui"],
      "reporter": {"id": "USR-67890", "name": "Alex Chen"}
    },
    {
      "title": "Update API documentation"
    }
  ]
}
```

From three examples (full / partial / minimal), the model learns format conventions, nested structure, **and correlation patterns** (critical bug → escalation+contact; feature → reporter only; internal task → title only).

## Anthropic's authoring rules

- 1-5 examples per tool — more is wasteful, fewer fails to disambiguate
- **Realistic data** — real city names, plausible prices, not `"string"` / `"value"`
- **Cover variety** — minimal, partial, and full specification patterns
- **Focus on ambiguity** — add examples only where correct usage isn't obvious from the schema alone. Don't drown the model in redundant examples for self-evident fields.

## Relationship to [[Few-Shot Drift]] (Manus)

There's a tension. Manus argues that uniform examples cause pattern mimicry that becomes brittle ([[Few-Shot Drift]]). Anthropic argues that *carefully chosen* examples in tool defs raise accuracy.

The resolution is in the placement and purpose:

- **Tool Use Examples** sit in the **stable, cacheable region** of context (tool definitions). They're seen once per task, used as reference. Not the same surface as the running observation tail Manus is worried about.
- **Few-shot drift** happens in the **dynamic observation tail** when repeated similar action-observation pairs accumulate. The agent's own past trajectory becomes its de-facto few-shot prompt.

Both can be true: prescriptive examples in tool defs improve initial usage; descriptive accumulation in observations risks drift. The Manus mitigation (diversity injection in observations) doesn't conflict with the Anthropic mechanism (diversity-of-examples in defs).

## When this wins

- Complex nested structures where valid JSON doesn't imply correct usage
- Tools with many optional parameters where inclusion patterns matter
- APIs with domain-specific conventions not captured in schemas (date formats, ID conventions)
- Similar tools where examples clarify which one to use (e.g., `create_ticket` vs `create_incident`)

## When it doesn't

- Simple single-parameter tools with obvious usage (no ambiguity to resolve)
- Standard formats the model already knows (URLs, emails)
- Validation concerns better handled by JSON Schema constraints (use the constraint, not the example)

## ACI implications

Tool Use Examples extend [[ACI - Agent-Computer Interface]] in a clean way: ACI was already about schemas, naming, docs, and error messages; examples are the missing piece. They turn tool definitions from **structural contracts** into **usage demonstrations**.

This connects back to Anthropic's earlier tool-design discipline (per [[Building Effective Agents]]): "treat tool docs like a docstring for a junior engineer." Examples are how a senior engineer would actually teach a junior to use an API — show them, don't just declare types.

## Connections

- Mechanism of: [[ACI - Agent-Computer Interface]]
- Stable-region complement to: [[Few-Shot Drift]] (which is about dynamic observation tail, not tool defs)
- Operationalizes: [[Context Engineering]] (a token-efficient way to teach correct usage)
- Cache-friendly: lives in the cacheable prefix, no [[KV-Cache Discipline]] cost
- Sister features: [[Tool Search Tool]] · [[Programmatic Tool Calling]] (the three "advanced tool use" beta features released together)

## Open questions

- 72→90% is one number on one workload. Does the improvement generalize across domains?
- Does example quality matter more than count? Three good examples vs five mediocre ones — Anthropic implies yes but doesn't quantify.
- Composability with PTC — when Claude is writing code to call a tool, do `input_examples` still help, or does the code execution sidestep the parameter-formatting problem entirely?
- Composability with [[Tool Search Tool]] — when a tool is deferred and loaded on demand, its examples come with it. Does this affect search-quality? Probably positively (more context to match against) but unverified.
- Drift over time — if a tool's expected usage evolves (API changes), examples can go stale. Versioning story for `input_examples` not addressed.

## Confirmation from 2026-05 practice guide

[[2026-05-13 - Anthropic - Writing Effective Tools for Agents]] re-confirms and extends the examples guidance with an explicit **authoring hierarchy**: start with descriptions, then add field-level schema descriptions, then add 2-3 examples. The "cover variety" rule (minimal / partial / full) remains. New addition: explicitly test the tool by giving Claude *only* the definition and seeing if it calls correctly — examples are the first thing to add when this test fails for parameter-format reasons.

## Sources

- [[2025-11-24 - Anthropic - Advanced Tool Use]] (Anthropic, 2025-11-24)
- [[2026-05-13 - Anthropic - Writing Effective Tools for Agents]] (Anthropic, 2026-05-13)
