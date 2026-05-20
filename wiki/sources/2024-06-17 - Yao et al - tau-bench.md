---
type: source
title: "Yao et al — τ-bench"
created: 2026-05-13
updated: 2026-05-13
tags:
- ai-agents
- evaluation
- benchmark
- tool-use
- reliability
status: mature
related:
- "[[tau-bench]]"
- "[[Pass^k Reliability Metric]]"
- "[[User Simulator Evaluation]]"
- "[[Sierra]]"
- "[[Workflows Beat Agents for Most Production]]"
sources:
  - "[[.raw/articles/2024-06-17 - Yao et al - tau-bench.md]]"
- "[[03_Resources/.raw/articles/2024-06-17 - Yao et al - tau-bench.md]]"
source_type: paper
author: Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan (Sierra)
date_published: 2024-06-17
url: https://arxiv.org/abs/2406.12045
arxiv_id: 2406.12045
confidence: high
key_claims:
- "SOTA function-calling agents solve <50% of customer-service tasks (gpt-4o: 61% retail, 35% airline)"
- "Reliability drops sharply with k: gpt-4o pass^8 <25% on retail despite pass^1 >60%"
- "Removing the domain-policy doc costs gpt-4o 22% on airline but only 1% on gpt-3.5 — capacity to follow rules requires both presence of rules AND a model that can read them"
- "Failure modes split ~55% reasoning-over-database / 25% rule-following / 19% compound-request partial-resolution"
aliases:
- τ-bench
- tau-bench paper
---

# τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (Yao et al., Sierra, 2024-06-17)

## Why this matters for the wiki

First benchmark in the corpus that **measures the reliability gap directly**, not the capability ceiling. The wiki has been long on *patterns* for building agents ([[Building Effective Agents]], [[Workflows vs Agents]]) and *production discipline* ([[KV-Cache Discipline]], [[Recitation]]) but short on **how to know when an agent is good enough to deploy**. τ-bench supplies the missing instrument and supplies hard numbers that pressure-test the existing thesis [[Workflows Beat Agents for Most Production]].

It also introduces [[Pass^k Reliability Metric]] — a primitive that should propagate to any future eval discussion in this wiki.

## The setup in one paragraph

Each task is a POMDP where an agent interacts with (1) database APIs (deterministic Python) and (2) an LM-simulated user (gpt-4-0613, stochastic) under a domain-specific policy document loaded as system prompt. Reward is binary: final database state must match the unique annotated ground truth AND agent responses must contain required information substrings. Two domains shipped: **τ-retail** (115 tasks, 500 users, 50 products, 1000 orders, 7 write + 8 read tools) and **τ-airline** (50 tasks, 300 flights between 20 cities, 6 write + 7 read tools).

Construction: manual schema + LM-assisted data gen + manual scenario annotation iterated against a gpt-4-turbo trial agent until each scenario has exactly one valid outcome.

## Headline numbers (pass^1, function-calling agents)

| Model | retail | airline | avg |
|---|---|---|---|
| gpt-4o | 61.2 | 35.2 | 48.2 |
| gpt-4-turbo | 57.7 | 32.4 | 45.1 |
| gpt-4-32k | 56.5 | 33.0 | 44.8 |
| claude-3-opus | 44.2 | 34.7 | 39.5 |
| mistral-large | 30.7 | 22.4 | 26.6 |
| claude-3-sonnet | 26.3 | 27.6 | 27.0 |
| gemini-1.5-pro | 21.7 | 14.0 | 17.9 |
| gpt-3.5-turbo | 20.0 | 10.8 | 15.4 |
| meta-llama-3-70B | 14.8 | 14.4 | 14.6 |

Open-weight models lag SOTA proprietary by 15-30 points. Function calling consistently beats text-formatted ReAct/Act on the same model.

## The reliability finding (load-bearing)

The single most-cited result from this paper: **pass^k collapses with k far faster than capability suggests**. On retail with gpt-4o:

- pass^1 ≈ 61%
- pass^4 ≈ ~35%
- pass^8 < 25%

This is not about hard tasks — it's about **the same task** being solved inconsistently across i.i.d. trials. The stochasticity comes from the agent's own sampling and from user-simulator variation; the underlying database transitions are deterministic. See [[Pass^k Reliability Metric]] for why this matters more than pass@k for customer-facing deployment.

## Failure breakdown (gpt-4o FC on τ-retail, 36 failed of 115)

> [!key-insight] Where SOTA agents actually break
> - **Wrong argument** (19.4%) — right tool, wrong field. Complex database reasoning.
> - **Wrong info** (25.0%) — omitted required fields, wrong arithmetic, hallucinated values.
> - **Wrong decision** (22.2%) — domain-policy violation; rule misread or ignored.
> - **Partial resolution** (33.3%) — compound user requests; agent stops after the first.

Hallucination rate gap: gpt-4o FC makes **0.46 invalid-ID tool calls/task**; gpt-3.5 FC makes **2.08**; gpt-3.5 Act makes **6.34**. Function calling + scale dominate hallucinated-argument suppression.

## Rule-following ablation (Table 3)

Remove the domain policy from system prompt:

| | τ-retail | τ-airline |
|---|---|---|
| gpt-4o | 61.2 → 56.8 (−4.4) | 33.2 → 10.8 (−22.4) |
| gpt-3.5 | 20.0 → 14.5 (−5.5) | 10.8 → 9.6 (−1.2) |

**Interpretation** — when rules are common-sense (retail returns/exchanges), even SOTA agents lean on prior, not policy. When rules are arbitrary and multi-hop (airline membership × cabin × baggage), only models with enough capacity to *read and follow* the policy benefit from having it. gpt-3.5 can't use the policy regardless. This is a direct rebuttal to "just dump the policy in context."

## Cost

gpt-4o agent + gpt-4 user simulator on τ-retail: $0.38 agent + $0.23 user per task → ~$200 for a single trial across the suite. 95.9% of agent cost is the long system prompt (policy + function defs). Implication for [[Token Economics]]: policy-shaped system prompts are the dominant cost driver for managed customer-service agents, far more than completion length.

## Connections to existing wiki

- **[[Workflows Beat Agents for Most Production]]** — this is *strong* supporting evidence. Even the best LM-function-calling agent is <50% reliable on a relatively constrained benchmark, and pass^8 < 25% rules out naive deployment. Workflow architectures with explicit state machines avoid the rule-following failures (22% of cases) and the partial-resolution failures (19%) almost by construction. **Net: thesis strengthens.**
- **[[Autonomous Agents]]** — supplies the eval primitive (end-state DB comparison) the page was missing. Resolves a long-standing open question on long-horizon eval.
- **[[LLM-as-Judge Evaluation]]** — useful **contrast**. τ-bench bypasses LLM-judge entirely via deterministic database-state comparison. The tradeoff: faithful and free, but requires that "exactly one valid database outcome exists," which constrained the benchmark to artificially-unique task scenarios. Customer-service domains where rules force determinism are eligible; open-ended research/coding tasks are not.
- **[[ACI - Agent-Computer Interface]]** — policy document IS the ACI at the cognitive layer. Quality of policy writing shapes agent success more than tool design at the SOTA-model end of the curve (see ablation).
- **[[Few-Shot Drift]]** — `gpt-4-0613` user simulation is the source of conversational diversity; this is few-shot drift used **constructively** to probe agent robustness rather than something to suppress.
- **[[Token Economics]]** — confirms that policy + function-def system prompts dominate cost; agents are mostly paying to re-read rules.

## Verbatim claims worth quoting

> "Existing benchmarks do not test language agents on their interaction with human users or ability to follow domain-specific rules, both of which are vital for deploying them in real world applications."

> "Even state-of-the-art function calling agents (like gpt-4o) succeed on <50% of the tasks, and are quite inconsistent (pass^8 <25% in retail)."

> "Agents built on top of LM function calling lack sufficient consistency and rule-following ability to reliably build real-world applications."

> "The user instruction sets up user identity, intent, and preferences in a way that guarantees only one possible outcome under the domain policy."

> "Sometimes the agent omits explicit user requests at the beginning of the conservation [sic], hinting at the need for better long-context and memory capabilities."

## Patterns and concepts introduced

- [[tau-bench]] — the benchmark itself (entity)
- [[Pass^k Reliability Metric]] — reliability across k i.i.d. trials (concept)
- [[User Simulator Evaluation]] — LM-as-user for closed-loop agent eval (concept)
- [[Sierra]] — Shunyu Yao's affiliation, customer-service-agent product company (entity)

## Open questions this raises for the wiki

- Does **pass^k** collapse the same way on coding/research tasks ([[Recursive Language Models]] domain), or is the variance a customer-service-specific artifact of user-simulator stochasticity?
- Can [[Meta-Harness]]'s session-as-event-log (durable state outside context window) close the compound-request partial-resolution failure mode? The 19% category looks like a memory problem, not a reasoning one.
- Does fine-tuning on policy-following or scaffolding with [[Programmatic Tool Calling]] move pass^8 more than pass^1?

## Source location

- Raw: `.raw/articles/2024-06-17 - Yao et al - tau-bench.md`
- arXiv: <https://arxiv.org/abs/2406.12045>
- Code: <https://github.com/sierra-research/tau-bench>