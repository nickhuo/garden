---
type: entity
title: "tau-bench"
created: 2026-05-13
updated: 2026-05-13
tags:
- ai-agents
- benchmark
- evaluation
- tool-use
status: developing
related:
- "[[Sierra]]"
- "[[Pass^k Reliability Metric]]"
- "[[User Simulator Evaluation]]"
- "[[2024-06-17 - Yao et al - tau-bench]]"
sources:
- "[[2024-06-17 - Yao et al - tau-bench]]"
- "[[2025-03-20 - Anthropic - The Think Tool]]"
- "[[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]"
entity_type: benchmark
authors: Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan
affiliation: Sierra
released: 2024-06-17
repo: https://github.com/sierra-research/tau-bench
license: MIT
aliases:
- τ-bench
- Tool-Agent-User Interaction Benchmark
---

# τ-bench (tau-bench)

## What it is

A benchmark for closed-loop evaluation of LM agents in customer-service-style domains, released by [[Sierra]] in June 2024. An agent interacts with a deterministic Python-backed database via API tools AND with an LM-simulated user (gpt-4-0613) under a domain-specific policy document. Reward is binary: final database state must match a unique annotated ground truth.

Two domains in v1:

- **τ-retail** — 115 tasks, 500 users / 50 products / 1000 orders; 7 write + 8 read tools.
- **τ-airline** — 50 tasks, 300 flights between 20 US cities, 2000 reservations; 6 write + 7 read tools. Harder than retail due to ad-hoc policy (membership × cabin × baggage interactions).

Built in three stages: manual schema design → LM-assisted data generation → manual scenario annotation iterated against a gpt-4-turbo trial agent until each task has exactly one valid outcome.

## Why this entity has its own page

The benchmark is itself a citable artifact distinct from the paper that introduced it. Subsequent agent research papers and reliability discussions reference τ-bench numbers without re-citing the original paper. Treating it as an entity (like [[MCP]] or [[Managed Agents]]) means future sources that mention τ-bench scores update this page rather than the source page.

## Headline pass^1 numbers from the paper

gpt-4o: 48.2 avg | gpt-4-turbo: 45.1 | claude-3-opus: 39.5 | mistral-large: 26.6 | gpt-3.5-turbo: 15.4.

For reliability under repeated trials, see [[Pass^k Reliability Metric]] — gpt-4o pass^8 < 25% on retail.

## Methodological contributions

- **Database-state reward** — replaces LLM-judge or trajectory grading with deterministic equality check on final DB state. Faithful but requires uniquely-resolvable scenarios.
- **[[Pass^k Reliability Metric]]** — first formal reliability metric for agents.
- **[[User Simulator Evaluation]]** — LM-as-user with asymmetric info (user can't see tool calls) and policy-aware ground truth.

## Known successors and adjacent work

(Track here as new sources mentioning τ-bench come in.)

- [[2025-03-20 - Anthropic - The Think Tool]] — Anthropic tested the [[Think Tool]] on τ-bench; ~6–7% pass^1 improvement on τ-airline (policy-heavy), ~4% on τ-retail. First source in the wiki to report τ-bench results for a specific intervention rather than baseline model capability.
- [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]] — cross-validates τ-bench's environment-state reward approach as the reference implementation for Tier 3 end-to-end evals; confirms user-simulator info-asymmetry design is canonical.

## Connections

- [[Sierra]] — owning org
- [[2024-06-17 - Yao et al - tau-bench]] — origin paper
- [[Pass^k Reliability Metric]] · [[User Simulator Evaluation]] — methodology
- [[Workflows Beat Agents for Most Production]] — provides supporting evidence
- [[Autonomous Agents]] — supplies the long-horizon eval primitive that page was missing

## Open

- Has Sierra released v2 with additional domains? (Medical, legal, tax were mentioned as future work.)
- Are there cleaned-up implementations of τ-bench for non-customer-service domains (e.g., research-task variants)?
