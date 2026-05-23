---
type: source
title: "Harvey — Using Agents to Scale Knowledge Sources"
created: 2026-05-23
updated: 2026-05-23
tags:
  - ai-agents
  - citation
  - rag
  - legal
status: developing
source_type: blog
author: "Harvey"
date_published: 2025-09-01
url: "https://www.harvey.ai/blog/using-agents-to-scale-harveys-knowledge-sources"
confidence: medium
related:
  - "[[Harvey]]"
  - "[[Citation Verification Pipeline]]"
  - "[[Attributed Text Generation]]"
  - "[[Multi-Agent Systems]]"
sources:
  - "https://www.harvey.ai/blog/using-agents-to-scale-harveys-knowledge-sources"
---

# Harvey — Using Agents to Scale Knowledge Sources

Harvey's agent-based architecture for building and citing from a curated legal corpus. The concrete embodiment of the "curated corpus + verification gates" pattern in [[Citation Verification Pipeline]].

## Sourcing & ingestion (agent fleet)

- **Sourcing Agent** — maps a jurisdiction's legal infrastructure, identifies trusted repositories, validates new sources.
- **Legal Review Agent** — analyzes terms-of-service / copyright (compliance throughput 1–2 → 2–4 sources/hr).
- Sources become **parameterized tools** via a declarative config layer (domains, filter hierarchies, permissions) → add sources in days not weeks.

## Citation linking & quality (the key part)

- **Closed corpus**: "every result comes from a vetted government portal or authoritative legal database" — *not open-web search*. This is the precision lever.
- **Citation Quality Agent** — checks whether the retrieved URL **actually supports the legal argument made**.
- **URL Classification Agent** — distinguishes real content from navigation noise.

## Verification gate (4-step eval)

1. **Answer-first scenario generation** — reverse-engineer fact patterns that force the agent to locate specific materials.
2. **Production simulation** — replica environment.
3. **Trace validation** — *hallucinated citation → automatic rejection.*
4. **Multi-agent assessment** — ensemble over URL validity, citation quality, legal reasoning, presentation; a **Decision Agent** aggregates pass/fail and routes ambiguous cases to human review.

## Scale

Aug 2025 onward: 6 → **60+ jurisdictions**, 20 → **400+ sources**.
