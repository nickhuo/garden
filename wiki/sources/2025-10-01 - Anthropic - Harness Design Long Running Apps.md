---
type: source
title: "Harness design for long-running application development"
url: https://www.anthropic.com/engineering/harness-design-long-running-apps
author: Anthropic
date: 2025-10-01
tags:
  - ai-agents
  - harness
  - long-horizon
  - infrastructure
status: developing
related:
  - "[[Meta-Harness]]"
  - "[[Context Anxiety]]"
  - "[[Long-Horizon Context Management]]"
  - "[[Workflows vs Agents]]"
  - "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
sources:
  - "[[.raw/articles/2025-10-01 - Anthropic - Harness Design Long Running Apps.md]]"
confidence: medium
source_type: blog
key_claims:
  - "Harnesses encode assumptions about model limitations; those assumptions go stale as models improve."
  - "Claude Sonnet 4.5 exhibited 'context anxiety' — premature task termination as context window filled."
  - "Context resets added to address context anxiety became dead weight on Claude Opus 4.5."
  - "Harness design must be treated as an ongoing discipline, not a one-time engineering exercise."
fetch_note: "Full article text not retrieved at ingest. Key claims sourced from cross-references in Scaling Managed Agents (2026-04-08). Backfill on next opportunity."
---

# Harness design for long-running application development

**Author:** Anthropic Engineering
**Published:** ~2025 (exact date estimated; cited by Scaling Managed Agents, 2026-04-08)
**URL:** https://www.anthropic.com/engineering/harness-design-long-running-apps
**Part of:** Anthropic Engineering Blog series on agentic systems

---

## Thesis

Harnesses for long-running agents are not static engineering artifacts — they are **living specifications of model assumptions**. Every design choice encodes a belief about what the current model cannot do on its own. As models improve, those beliefs must be revisited or the harness becomes an obstacle.

---

## Key Claims

1. **Harness assumptions go stale.** What a harness compensates for in one model generation may be unnecessary — or actively harmful — in the next.

2. **Context anxiety is real and model-specific.** Claude Sonnet 4.5 exhibited a documented behavior: premature task wrap-up as the context window approached saturation. This behavior was called "context anxiety." It was not present in Claude Opus 4.5.

3. **Context resets as a targeted harness fix.** Anthropic's engineering response was to add context resets — a mechanism that clears or compacts the context window when it approaches capacity — specifically to counteract context anxiety in Sonnet 4.5.

4. **Dead weight principle.** The same context-reset harness applied to Claude Opus 4.5 added overhead without benefit. Anthropic uses this as the canonical example of how harness assumptions go stale.

5. **Iterative harness design is the discipline.** Long-running application development requires frequent re-evaluation of harness assumptions against current model capabilities.

---

## Methods

Empirical observation of Claude Sonnet 4.5 and Claude Opus 4.5 behavior on production long-running tasks. No formal benchmark cited in the cross-references — findings are operational/observational.

---

## Important Quotes (via cross-reference in Scaling Managed Agents)

> "A common thread across this work is that harnesses encode assumptions about what Claude can't do on its own. However, those assumptions need to be frequently questioned because they can go stale as models improve."

> "Claude Sonnet 4.5 would wrap up tasks prematurely as it sensed its context limit approaching—a behavior sometimes called 'context anxiety.' We addressed this by adding context resets to the harness. But when we used the same harness on Claude Opus 4.5, we found that the behavior was gone. The resets had become dead weight."

*— Anthropic, Scaling Managed Agents (2026-04-08), citing this article*

---

## Claims with Wikilinks

- Harness assumptions encode beliefs about [[Workflows vs Agents]] and model capabilities — as the latter shifts, the former must adapt.
- [[Context Anxiety]] (new concept) is the specific behavior pattern: premature task termination as the LLM senses its context limit.
- Context resets are a [[Long-Horizon Context Management]] technique — specifically a compaction-adjacent harness-level intervention.
- The "dead weight" finding motivates [[Meta-Harness]] design philosophy: build stable *interfaces* around Claude, not brittle assumptions about Claude's current limitations.
- The empirical model-comparison (Sonnet 4.5 vs Opus 4.5) is an early example of the kind of harness validation that [[Managed Agents]] is designed to make less painful over time.

---

## Connections to Existing Wiki

- **Directly cited by:** [[2026-04-08 - Anthropic - Scaling Managed Agents]] — this article's context anxiety finding is used to motivate the meta-harness architecture.
- **Extends:** [[Long-Horizon Context Management]] — context resets are a concrete technique in that family.
- **New concept coined:** [[Context Anxiety]] — a named failure mode for context-window-aware premature task termination.
- **Supports:** [[Meta-Harness]] — the dead weight finding is the strongest practical argument for stable-interface meta-harness design over model-assumption-baked harnesses.
- **Continues series:** [[2024-12-19 - Anthropic - Building Effective Agents]], [[2025-09-29 - Anthropic - Effective context engineering for AI agents]]

---

## Source Integrity Note

Full article text was not available at ingest time. The key claims above are reconstructed from [[2026-04-08 - Anthropic - Scaling Managed Agents]], which directly cites this article and quotes from it. Confidence is **medium** — the factual claims are cross-verified but additional content from the original article is unknown. Backfill the full article text on next retrieval opportunity.
