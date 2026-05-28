---
type: thesis
title: Workflows Beat Agents for Most Production
created: 2026-05-04
updated: 2026-05-13
tags:
- ai-agents
- thesis
status: developing
related: []
sources:
- "[[2024-12-19 - Anthropic - Building Effective Agents]]"
- "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
- "[[2026-04-08 - Anthropic - Scaling Managed Agents]]"
- "[[2024-06-17 - Yao et al - tau-bench]]"
- "[[2025-10 - Zhang Khattab - Recursive Language Models]]"
_legacy_source_count: 4
---

# Workflows Beat Agents for Most Production

## Claim

For the majority of production LLM features, **workflows** ([[Prompt Chaining]] · [[Routing]] · [[Parallelization]] · [[Orchestrator-Workers]] (workflow variant) · [[Evaluator-Optimizer]]) deliver better outcomes than [[Autonomous Agents]] or [[Multi-Agent Systems]] — because they trade lower flexibility for predictability, latency, cost, and bounded error.

**Carve-out (per Anthropic 2025-06):** Multi-agent systems win when **all three** of (a) heavy parallelization, (b) information exceeds single context, (c) high task value clearing 15× cost are true. Outside this triple-conjunction, workflows remain default.

**Coding is explicitly workflow-territory.** Anthropic has stated single-agent coding > multi-agent coding "today" because coding tasks aren't well-parallelizable and current models don't delegate well in real time. This is consequential — coding is where most LLM eng effort goes.

## Origin and current support

- **Founding claim:** [[Building Effective Agents]] (Anthropic, 2024-12-19) — workflows > agents for most production. Frame: simple, composable patterns outperform complex frameworks.
- **Tightening evidence:** [[How we built our multi-agent research system]] (Anthropic, 2025-06-13) — ratifies the framing with sharper numbers (4× / 15× tokens; 80% performance variance from tokens alone) AND carves out research as the explicit zone where multi-agent wins.
- **Infra layer evolving:** [[Scaling Managed Agents]] (Anthropic, 2026-04-08) — closes a chunk of the *infra-side* objections to agents (statelessness, recovery, multi-tenant security, lazy provisioning; p50 TTFT ↓~60%). The thesis still holds for cognitive reliability, but the production-readiness gap narrows. Cognitive-side objections (drift, eval cost, debuggability) remain.
- **Reliability evidence (strong):** [[2024-06-17 - Yao et al - tau-bench]] (Sierra, 2024-06-17) — SOTA function-calling agents solve <50% of customer-service tasks, and gpt-4o pass^8 drops below 25% on retail despite pass^1 ≈ 61%. Failure mix: 25% rule-following violations, 19% partial-resolution of compound requests — both failure modes are eliminated by construction in a workflow architecture. Removing the policy document costs SOTA models 22% on airline but gpt-3.5 only 1%, i.e. rule-following requires both rules *and* capacity. **Net: thesis strengthens** — the production-readiness gap exists at the cognitive layer where [[Scaling Managed Agents]] doesn't help, and reliability has now been measured, not just asserted.
- **Compatible counterexample (consistent reading):** [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, 2025-10) — [[Recursive Language Models]] beat baseline single-model calls on long-context benchmarks (RLM(GPT-5-mini) +114%↑ on OOLONG 132k vs GPT-5). RLM is agent-shaped (the LM decides all decomposition), but operates inside a tightly constrained substrate — a Python REPL with a bounded action set. The honest reading: **agents work when you constrain the substrate to look like a workflow**. RLM's REPL is structurally a workflow scaffold; the LM does cognitive work *inside* that scaffold. This is consistent with the existing defensive position, not a falsification.

## Strongest evidence so far

- **pass^8 < 25% on the easier τ-bench domain** ([[2024-06-17 - Yao et al - tau-bench]]). Same task, same agent, different sampling — measured, not asserted. See [[Pass^k Reliability Metric]].
- [[Token Economics]]: agents = 4× chat tokens; multi-agent = 15× chat tokens. Most production tasks don't clear that bar.
- Token count alone explains 80% of BrowseComp performance variance — multi-agent wins by buying parallelism, not by deploying superior intelligence.
- Coding (Anthropic's own product domain) is explicitly carved out as workflow-territory.
- Anthropic spent more time on tools than on prompts when building their SWE-bench agent — bottleneck is tool/interface design, not agentic-ness. See [[ACI - Agent-Computer Interface]].

## What would falsify this

- A non-research category of production tasks where multi-agent systems demonstrably beat workflows on cost-adjusted metrics.
- Token-cost reductions large enough to make 15× indifferent (model price collapse).
- Reliability gains in single-agent long-horizon planning that erode the multi-agent advantage in research.
- A new coordination primitive (agent-to-agent communication, async subagent execution) that closes the coding gap.

## Counterclaims still to track

- **Devin / Cognition camp** — likely argues coding agents *do* work; need to ingest their writeup as the primary counter-source.
- **Boundary-dissolution camp** — workflow / agent / multi-agent are scaffolding for current limitations; sufficiently good models eliminate the distinction. Has not been steelmanned in any source yet.
- **Long-context-replaces-multi-agent camp** — if 1M+ contexts make context-overflow non-issue, the triple-conjunction's 2nd leg dissolves; multi-agent loses one of its three justifications.

## Nick's stance

_Position evolved 2026-05-04 from `open` to `defensive (with carve-outs)`. 2026-05-10: stance refined after RLM ingest — "agents work when substrate is workflow-shaped" is the sharpened version of the defensive position._

Provisional endorsement of workflow-default with Anthropic's research carve-out. The 4× / 15× [[Token Economics]] frame is the strongest decision tool — route by cost-clearance, not by aesthetic preference for "agentic" architecture.

**Sharpened position (post-RLM):** the agent-vs-workflow distinction is less binary than the founding sources framed it. [[Recursive Language Models]] shows that agent-shaped systems can match or exceed workflow predictability **when the substrate is sufficiently constrained** (REPL + bounded recursion + drop-in API). The operational test isn't "agent or workflow?" — it's "is the agent's action space tightly constrained enough to give workflow-grade predictability?" If yes, ship it as if it were a workflow. If no, default to an explicit workflow.

**Operational impact for Nick's career thread:** Coding being explicitly workflow-territory is consequential. Production coding agents are oversold today. Workflow-shaped coding tools (with smart primitives, well-designed [[ACI - Agent-Computer Interface]]) are the realistic 2026 production stack. RLM hints that a workflow-shaped *substrate hosting an agentic step* may be the strongest 2027 design — but only after cost-ceiling primitives and async/caching are figured out. This pushes Nick's GitHub-project bets toward workflow scaffolding **with optional LM-orchestrated steps as primitives**, not toward fully autonomous agent frameworks.

## Connections

- Distinction: [[Workflows vs Agents]]
- Multi-agent variant: [[Multi-Agent Systems]]
- Constrained-substrate agent design: [[Recursive Language Models]] (workflow-shaped REPL hosting an agentic LM)
- Decomposition axis: [[Context Decomposition vs Problem Decomposition]]
- Operational test: [[Token Economics]]
- Eval framework: [[LLM-as-Judge]]
- Context discipline: [[Context Engineering]]
- Production runtime: [[Meta-Harness]] · [[Managed Agents]]
- Workflow patterns: [[Prompt Chaining]] · [[Routing]] · [[Parallelization]] · [[Orchestrator-Workers]] · [[Evaluator-Optimizer]]
- Agent pattern: [[Autonomous Agents]]
- Foundational: [[Augmented LLM]]

## Sources

- [[2024-06-17 - Yao et al - tau-bench]] (Yao et al, Sierra, 2024-06-17)
- [[Building Effective Agents]] (Anthropic, 2024-12-19)
- [[How we built our multi-agent research system]] (Anthropic, 2025-06-13)
- [[Scaling Managed Agents]] (Anthropic, 2026-04-08)
- [[2025-10 - Zhang Khattab - Recursive Language Models]] (Zhang & Khattab, 2025-10)
