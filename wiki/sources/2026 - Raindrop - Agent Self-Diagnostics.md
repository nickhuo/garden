---
type: source
title: "Agent Self-Diagnostics"
source_type: article
author: "Raindrop"
date_published: 2026
url: "https://www.raindrop.ai/blog/agent-self-diagnostics"
created: 2026-05-23
updated: 2026-05-23
status: seed
confidence: medium
key_claims:
  - "Agent self-diagnostics lets agents proactively self-report failures to their dev team, complementing externally-trained detectors."
  - "Four default failure categories: missing context, repeatedly broken tool, capability gap, and complete task failure; teams can define custom categories."
  - "Integrates as an SDK with frameworks like the Vercel AI SDK and Claude Agent SDK."
tags:
  - ai-agents
  - evaluation
  - online-evaluation
related:
  - "[[Raindrop]]"
  - "[[Specialized Eval Classifiers]]"
  - "[[Trace-Based Evaluation]]"
sources: []
---

# Agent Self-Diagnostics (Raindrop)

A Raindrop feature (vendor source — confidence medium) where the agent **proactively self-reports failures**, complementing Raindrop's externally-trained detectors ([[Specialized Eval Classifiers]]).

## Default failure taxonomy

Four categories detected by default (customizable):
- **Missing context** — critical info/credentials/access missing and the user can't provide it.
- **Repeatedly broken tool** — a tool failed or returned unexpected output after multiple attempts.
- **Capability gap** — the task needs a tool/permission/capability the agent lacks.
- **Complete task failure** — the agent couldn't accomplish the task despite genuine attempts.

This is a **structured failure-mode schema** for online monitoring — close in spirit to the wiki's [[Trace-Based Evaluation]] (attribute failures to a cause class), but emitted by the agent itself rather than reconstructed post-hoc.

## Integration

Ships as an SDK integrating with the Vercel AI SDK and the Claude Agent SDK. Entity: [[Raindrop]].

> [!gap] The article gives no architecture detail, model sizes, accuracy, or cost numbers — self-reported categories rely on the agent's own reasoning, which inherits the agent's blind spots (an agent that doesn't know it failed can't self-report it). Pairs with externally-trained classifiers precisely to cover that gap.
