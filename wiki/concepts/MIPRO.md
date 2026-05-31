---
type: concept
title: MIPRO
created: 2026-05-31
updated: 2026-05-31
tags: [llm, ai-agents, prompt-optimization]
status: developing
complexity: intermediate
domain: llm
aliases: ["MIPROv2", "Multi-prompt Instruction PRoposal Optimizer"]
related: ["[[Prompt Optimization]]", "[[DSPy]]", "[[Compound AI System]]", "[[GEPA]]", "[[Krista Opsahl-Ong]]", "[[Omar Khattab]]"]
sources: ["[[2024-06 - Opsahl-Ong et al - MIPRO Optimizing Instructions and Demonstrations]]"]
---

# MIPRO

**Multi-prompt Instruction PRoposal Optimizer** — the prompt optimizer for multi-stage [[Compound AI System|LM programs]] introduced by [[Krista Opsahl-Ong|Opsahl-Ong et al. (2024)]] and shipped in [[DSPy]] as `MIPROv2`. It jointly optimizes each module's **instructions** *and* **few-shot demonstrations** against an end-to-end metric, with **no module-level labels and no gradients**. Was the SOTA prompt optimizer until [[GEPA]] (2026).

## The three moves

MIPRO answers the three challenges of [[Prompt Optimization]] over a program:

1. **Bootstrap demonstrations** (proposal, part 1) — run the program on training inputs; keep traces whose final output passes the metric; the per-module input/output pairs become self-generated few-shot demos. No manual labeling.
2. **Grounded instruction proposal** (proposal, part 2) — a proposer LM writes candidate instructions per module, conditioned on five grounding signals: **program** summary (code + module role), **data** summary, the bootstrapped **demos**, proposal **history** (past instructions + scores), and a sampled instruction-design **tip**. Grounding is the contribution — ungrounded LLM-proposed instructions are weaker.
3. **Bayesian surrogate search** (credit assignment + cheap evaluation) — a **Tree-structured Parzen Estimator (TPE)** searches the discrete space of (instruction, demo-set) assignments across modules, scoring candidates on **stochastic mini-batches**. Credit assignment is *implicit*: the surrogate learns which whole configurations score well, sidestepping the need to attribute reward to a single module.

## What the paper found

- **Demonstrations are the highest-impact lever** — optimizing bootstrapped few-shot demos alone often beats instruction-only optimization.
- **Optimizing both (full MIPRO) generally wins** — best overall across the seven benchmark programs.
- **Instructions matter most for conditional-rule tasks** — rules not obvious from data and not expressible in a few examples (HotPotQA Conditional, ScoNe).

## Place in the lineage

- **Prompt-space, not weight-space** — tunes `Π` of a [[Compound AI System]] while weights `Θ` stay frozen. See [[Prompt Optimization]] for the landscape table.
- **DSPy optimizer family** — sits between simple few-shot bootstrapping and [[GEPA]]'s reflective evolution. MIPRO = Bayesian/joint-instruction+demo; GEPA = reflective-evolutionary/instruction-only with [[Pareto-based Candidate Selection]].
- **The baseline GEPA beats** — by >10%; GEPA also reverses MIPRO's "demonstrations dominate" finding and produces prompts up to 9.2× shorter (see contradiction note on the [[2024-06 - Opsahl-Ong et al - MIPRO Optimizing Instructions and Demonstrations|source page]]).

## Open questions

- How much of "demonstrations dominate" is specific to the 2024 model era (Llama-3-8B, GPT-3.5/4)?
- Is the TPE surrogate or the joint instruction+demo space the real driver, vs [[GEPA]]'s evolutionary Pareto search?

## Sources

- [[2024-06 - Opsahl-Ong et al - MIPRO Optimizing Instructions and Demonstrations]]
