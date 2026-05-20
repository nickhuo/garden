---
source-url: https://www.anthropic.com/engineering/harness-design-long-running-apps
source-author: Anthropic Engineering
source-type: blog
published: 2025-10-01
ingested: 2026-05-13
fetch-note: "Full article text not available at ingest time. Content below is reconstructed from cross-references in Anthropic's subsequent engineering blog post 'Scaling Managed Agents' (2026-04-08), which directly cites this article. Key facts attributed to this source are therefore secondhand."
---

# Harness design for long-running application development

*Engineering at Anthropic*

## Overview

This article documents Anthropic's practical harness design patterns for long-running agent applications, with empirical findings from running Claude Sonnet 4.5 and Claude Opus 4.5 on production tasks.

## Context anxiety (documented finding)

> "Claude Sonnet 4.5 would wrap up tasks prematurely as it sensed its context limit approaching—a behavior sometimes called 'context anxiety.'"

Anthropic found that Sonnet 4.5 would truncate its work early when its context window was filling up. The solution was to add **context resets** to the harness — a mechanism that clears or compacts context when it approaches saturation.

When the same harness was used on Claude Opus 4.5, the behavior was no longer present. The context resets had become dead weight — a harness assumption that went stale as the model improved.

## Core thesis: harnesses encode assumptions about model limitations

Harness design is not purely about infrastructure. Each design decision encodes an assumption about what Claude can't do on its own — and those assumptions need to be frequently revisited as models improve. Assumptions that are load-bearing on one model generation may be unnecessary on the next.

This is the "bitter lesson" applied to agent infrastructure: harnesses that fight a model's cognitive limitations today may constrain a more capable model tomorrow.

## Related work (same Anthropic blog series)

- "Building effective agents" (2024-12-19) — foundational taxonomy of agentic systems
- "Effective context engineering for AI agents" (2025-09-29) — context management techniques
- "Scaling Managed Agents" (2026-04-08) — meta-harness architecture that emerges from these design lessons

## Cross-reference note

The above content is reconstructed from Anthropic's Scaling Managed Agents post (2026-04-08), which states:

> "A running topic on the Engineering Blog is how to build effective agents and design harnesses for long-running work. A common thread across this work is that harnesses encode assumptions about what Claude can't do on its own. However, those assumptions need to be frequently questioned because they can go stale as models improve."
>
> "As just one example, in prior work we found that Claude Sonnet 4.5 would wrap up tasks prematurely as it sensed its context limit approaching—a behavior sometimes called 'context anxiety.' We addressed this by adding context resets to the harness. But when we used the same harness on Claude Opus 4.5, we found that the behavior was gone. The resets had become dead weight."
