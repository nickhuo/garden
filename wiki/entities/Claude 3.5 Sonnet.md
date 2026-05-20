---
type: entity
title: "Claude 3.5 Sonnet"
created: 2026-05-13
updated: 2026-05-13
tags:
  - ai-agents
  - evals
  - coding
  - llm
status: seed
related:
  - "[[SWE-bench Verified]]"
  - "[[Agentic Harness]]"
  - "[[MCP]]"
  - "[[Managed Agents]]"
sources:
  - "[[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]]"
entity_type: product
role: "Anthropic LLM; achieved 49% on SWE-bench Verified in agentic coding eval"
first_mentioned: "2026-05-13 ingest"
---

# Claude 3.5 Sonnet

## What it is

Claude 3.5 Sonnet is an Anthropic large language model. In the context of the wiki's ingest corpus, it is the model used in Anthropic's agentic coding experiment that achieved 49% on [[SWE-bench Verified]] — the headline result from [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]].

## Role in the wiki

The wiki treats Claude 3.5 Sonnet primarily as an **evaluation subject** — the model whose capabilities enabled a simple scaffold to outperform more complex systems. This supports the broader inference that:

- Model capability is the primary driver of agentic performance, not scaffold complexity
- Tool use fluency (file navigation, code editing, test execution) is a core model-level skill, not just a prompting trick

Claude 3.5 Sonnet also appears implicitly as the model powering other Anthropic systems referenced in the corpus (MCP documentation, Managed Agents, Advanced Tool Use context).

## Connection to Anthropic's agent ecosystem

- **[[MCP]]** — designed for Claude-first tooling integration
- **[[Managed Agents]]** — Anthropic's hosted agent runtime; Claude models are the core executor
- **Claude Code** — the commercial coding agent product downstream of the SWE-bench research

## Open questions

- How does Claude 3.5 Sonnet compare to Claude 3 Opus / Claude 3.5 Haiku on SWE-bench?
- What is the KV-cache cost profile for Claude 3.5 Sonnet vs. prior models (relevant to [[Token Economics]])?
- Does the 49% capability translate to acceptable [[Pass^k Reliability Metric]] scores in production?

## Sources

- [[2025-01-06 - Anthropic - SWE-bench Verified Sonnet 3.5]] (Anthropic, 2024-10-29)
