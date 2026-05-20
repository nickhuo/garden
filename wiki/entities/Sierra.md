---
type: entity
title: "Sierra"
created: 2026-05-13
updated: 2026-05-13
tags:
- ai-agents
- company
- customer-service
status: seed
related:
- "[[tau-bench]]"
- "[[2024-06-17 - Yao et al - tau-bench]]"
sources:
- "[[2024-06-17 - Yao et al - tau-bench]]"
entity_type: company
founded: 2023
founders: Bret Taylor, Clay Bavor
website: https://sierra.ai
---

# Sierra

## What it is

AI company building conversational customer-service agents for enterprises. Founded 2023 by Bret Taylor (ex-Salesforce co-CEO, OpenAI board chair) and Clay Bavor (ex-Google).

## Why it's in the wiki

Author affiliation for [[2024-06-17 - Yao et al - tau-bench]] and host of the [[tau-bench]] benchmark. Shunyu Yao did the work as an intern at Sierra; Noah Shinn (Reflexion), Pedram Razavi, and Karthik Narasimhan are co-authors.

The acknowledgements thank **Clay Bavor** directly — i.e., the benchmark is product-relevant work, not purely academic. τ-retail and τ-airline look exactly like the domains Sierra ships agents into.

## Connections

- [[tau-bench]] — flagship released artifact
- [[Workflows Beat Agents for Most Production]] — Sierra's product reality (deployed at enterprise scale) is data that supports the thesis; their own benchmark shows agents <50% reliable.

## Open

- What is Sierra's internal architecture? Are they using workflow-style scaffolding or agent-style LM-as-controller? The paper hints that current FC agents are insufficient; if Sierra deploys anyway, what's the production stack?
- Has Sierra published anything else since τ-bench?
