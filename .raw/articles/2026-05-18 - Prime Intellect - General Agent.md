---
source_url: https://www.primeintellect.ai/blog/general-agent
fetched: 2026-05-24
author: Mika
date_published: 2026-05-18
---

# General Agent: A Self-Evolving, Synthetic Agent Environment

Open-sourced `general-agent`: a fully synthetic environment that automatically grows its task corpus via a two-agent competitive framework. Currently 4,504 tasks across 1,040 domains with 8,000+ unique tools, grounded in database operations with semantic verification.

## Two-player task generation

- **Synthesizer Agent** — designs novel tasks following structured schemas; diverse and solvable.
- **Solver Agent** — attempts completion, provides pass-rate feedback for difficulty calibration.

## Task structure (4 elements)

1. Database Model — Pydantic entities (Therapists, Services, Appointments).
2. Tool APIs — Python functions manipulating DB state with domain logic.
3. Natural Language Instruction — user request.
4. Verification Function — checks completion against constraints.

## Difficulty tiers t0–t4 (nine evolution strategies)

Multi-step reasoning, conditional/branching constraints, cross-entity coupling, stricter numerical thresholds, larger DB with distractors, schema extension, tool proliferation with distractor tools, noisy instructions, ambiguity resolution.

## Corpus statistics

| Metric | Value |
|---|---|
| Total Tasks | 4,504 |
| Domains | 1,040 |
| Unique Tools | 8,159 |
| Unique Entity Classes | 2,222 |
| Unique-per-family Tools | 78% |
| Unique-per-family Entities | 66% |

## Difficulty calibration (GPT-5-Mini)

| Tier | Target | Achieved | Tools | Gold Steps | DB Entities |
|---|---|---|---|---|---|
| t0 | 0.8–1.0 | 0.928 | 6.3 | 2.5 | 10 |
| t1 | 0.6–0.8 | 0.757 | 9.0 | 8.7 | 23 |
| t2 | 0.4–0.6 | 0.601 | 11.4 | 13.3 | 240 |
| t3 | 0.2–0.4 | 0.407 | 13.4 | 17.2 | 323 |
| t4 | 0.0–0.2 | 0.251 | 14.9 | 20.5 | 437 |

GLM-5.1 (not used for calibration) showed similar monotonic scaling at higher absolute performance.

## Training experiments

- **RL (Qwen3-30B)**: reward 30% → ~70% over 200 steps; turns/rollout ~8 → ~24; steepest gains in first 100 steps.
- **SFT (Nemotron-3-Nano-30B)** on 4,417 GLM-5.1 tool-calling traces: BFCL-v3 18.9% → 52.3% (baseline 73.5%); MCP-Atlas 0.6% → 12.1% (baseline 45.5%); most learning within 80 steps.

## Failure modes

- **Semantic substitution** — models substitute world knowledge for DB facts (medium- vs light-pressure massage).
- **Ambiguity mishandling** — plausible-sounding options contradicting data constraints.
- **Budget violations** — cumulative constraint-tracking failures in multi-step scenarios.

## Synthesis protocol (5 steps)

Domain/schema design → simple seed task w/ verification → gating (≥0.80 pass) → iterative tier evolution t1→t4 → validation (≥5 unique strategies per family). Ran 1,000+ synthesizing GLM-5.1 agents in parallel.

## Solver backends

Local (direct Python calls), OpenCode (sandbox via MCP), RLM (sandbox + per-tool skills + IPython kernel).

## Future directions

Evolve harder tasks using t4 as seed; domain generalization to terminal-use and doc-retrieval; multi-agent RL with real-time corpus evolution during training; decoupled task/harness abstractions via verifiers v1.
