---
type: source
title: "General Agent: A Self-Evolving, Synthetic Agent Environment"
aliases:
  - "General Agent"
  - "general-agent"
created: 2026-05-24
updated: 2026-05-24
tags:
  - ai-agents
  - llm
  - rl
  - environments
  - synthetic-data
status: developing
source_type: blog
author: "Mika"
date_published: 2026-05-18
url: https://www.primeintellect.ai/blog/general-agent
confidence: high
key_claims:
  - A two-player synthesizer/solver loop auto-grows a calibrated agent task corpus (4,504 tasks, 1,040 domains, 8,159 tools)
  - Difficulty tiers t0-t4 hit their target pass-rate bands empirically (0.928 down to 0.251 on GPT-5-Mini)
  - RL on Qwen3-30B lifted reward 30% to 70% over 200 steps; turns/rollout 8 to 24
  - SFT on synthetic traces lifted Nemotron BFCL-v3 18.9% to 52.3%, MCP-Atlas 0.6% to 12.1%
  - Failure modes are semantic substitution, ambiguity mishandling, budget violations
related:
  - "[[Prime Intellect]]"
  - "[[Self-Evolving Agent Environments]]"
  - "[[tau-bench]]"
  - "[[BFCL]]"
  - "[[Recursive Language Models]]"
sources:
  - "[[.raw/articles/general-agent-2026-05-24.md]]"
---

# General Agent: A Self-Evolving, Synthetic Agent Environment

Mika, [[Prime Intellect]], May 18, 2026. [Blog post](https://www.primeintellect.ai/blog/general-agent).

## TL;DR

Open-sourced `general-agent`: a synthetic environment that **grows its own task corpus** via two competing agents — a **Synthesizer** that designs tasks and a **Solver** that supplies pass-rate feedback for difficulty calibration. The mechanism is [[Self-Evolving Agent Environments]]. Result: 4,504 tasks across 1,040 domains with 8,159 unique tools, all grounded in database operations with deterministic verification functions.

This is the production-scale answer to the data bottleneck for agentic RL: instead of hand-authoring tool-use tasks (the [[ToolBench]] / [[tau-bench]] / [[BFCL]] approach), generate and calibrate them automatically.

## Mechanism

Each task = (Pydantic **database model**, **tool APIs** over that DB, **NL instruction**, **verification function**). Difficulty evolves through tiers **t0–t4** via nine strategies (multi-step reasoning, branching constraints, cross-entity coupling, distractor tools, noisy instructions, ambiguity resolution, …). Synthesis protocol: design → seed task → gate at ≥0.80 pass → evolve t1→t4 → validate ≥5 unique strategies per family. 1,000+ synthesizer agents (GLM-5.1) ran in parallel to build the corpus.

## Calibration (GPT-5-Mini)

| Tier | Target | Achieved | Tools | Gold steps | DB entities |
|---|---|---|---|---|---|
| t0 | 0.8–1.0 | 0.928 | 6.3 | 2.5 | 10 |
| t1 | 0.6–0.8 | 0.757 | 9.0 | 8.7 | 23 |
| t2 | 0.4–0.6 | 0.601 | 11.4 | 13.3 | 240 |
| t3 | 0.2–0.4 | 0.407 | 13.4 | 17.2 | 323 |
| t4 | 0.0–0.2 | 0.251 | 14.9 | 20.5 | 437 |

The bands held — difficulty is genuinely controllable. GLM-5.1 (unseen during calibration) showed the same monotonic ordering at higher absolute scores, suggesting the tiers measure *task* difficulty, not one model's quirks.

## Training results

- **RL (Qwen3-30B)** — reward 30% → ~70% over 200 steps; turns/rollout ~8 → ~24 (the model learns to *work longer*). Steepest gains in first 100 steps.
- **SFT (Nemotron-3-Nano-30B)** on 4,417 GLM-5.1 traces — BFCL-v3 18.9% → 52.3% (vs 73.5% post-trained baseline); MCP-Atlas 0.6% → 12.1% (vs 45.5%). Synthetic traces close much of the gap but not all of it.

## Failure modes (what models get wrong)

- **Semantic substitution** — substituting world knowledge for DB facts.
- **Ambiguity mishandling** — picking plausible-sounding options that contradict data constraints.
- **Budget violations** — failing cumulative-constraint tracking in multi-step tasks.

## Connections

- Mechanism page: [[Self-Evolving Agent Environments]].
- The "keep difficulty calibrated" design is the constructive counterpart to [[Reward Hacking]]'s mitigation advice — a live, improvable visible reward by construction.
- One solver backend *is* an [[Recursive Language Models|RLM]] (sandbox + per-tool skills + IPython kernel), tying two pieces of [[Prime Intellect]]'s stack together.
- Verification-function grounding echoes [[tau-bench]]'s deterministic DB-state reward.
