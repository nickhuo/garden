---
type: source
title: "Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs"
created: 2026-05-31
updated: 2026-05-31
tags: [llm, ai-agents, prompt-optimization]
status: mature
source_type: paper
authors: ["Krista Opsahl-Ong", "Michael J Ryan", "Josh Purtell", "David Broman", "Christopher Potts", "Matei Zaharia", "Omar Khattab"]
venue: "EMNLP 2024"
arxiv: "2406.11695v2"
url: https://arxiv.org/abs/2406.11695
code: https://github.com/stanfordnlp/dspy
seed_score: 14/14
confidence: high
related: ["[[MIPRO]]", "[[Prompt Optimization]]", "[[Compound AI System]]", "[[DSPy]]", "[[GEPA]]", "[[Omar Khattab]]", "[[Krista Opsahl-Ong]]"]
sources: []
---

# Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs

> [!key-insight] Core claim
> You can optimize the prompts of a multi-module **[[Compound AI System|LM program]]** against an end-to-end metric **without module-level labels or gradients** — by *bootstrapping* few-shot demonstrations from the program's own successful traces, *grounding* an LM's instruction proposals in the program/data/demos, and searching the joint space with a **Bayesian surrogate** ([[MIPRO]]). Best results come from optimizing **both** instructions and demonstrations; gains up to **~13%** over baselines on diverse multi-stage tasks.

## What it is

The **MIPRO** (Multi-prompt Instruction PRoposal Optimizer) paper — EMNLP 2024, Stanford + UC Berkeley/Databricks + KTH + Basis. The primary source for the SOTA prompt optimizer that [[GEPA]] later dethrones, and a canonical [[DSPy]] optimizer. Lead author **[[Krista Opsahl-Ong]]** (also a [[GEPA]] co-author); senior author **[[Omar Khattab]]**, creator of DSPy. Code ships in `stanfordnlp/dspy` as `MIPROv2`.

## The problem

An **LM program** is a pipeline where each module = (prompt template, LM). Optimizing it means updating every module's prompt — **instructions** and **few-shot demonstrations** — to maximize a downstream metric, given only training *inputs* and the metric. Two hard constraints define the regime:

- **No module-level labels** — you only score the final output, not intermediate module outputs.
- **No gradients** — the LM may be a closed API; weight-space methods are off the table.

This forces three sub-problems the paper names: **(1) proposal** (the joint instruction × demonstration space across modules is intractably large), **(2) credit assignment** (which module's prompt to change, with no intermediate supervision), and **(3) expensive evaluation** (each full rollout costs money/compute). See [[MIPRO]] for how each is addressed.

## How MIPRO works

1. **Bootstrap demonstrations** — run the program on training inputs; keep traces whose final output passes the metric; harvest the per-module I/O pairs as self-generated few-shot demos (no hand-labeling).
2. **Grounded instruction proposal** — a proposer LM writes candidate instructions conditioned on five grounding signals: a **program** summary (code/role), a **data** summary, the bootstrapped **demos**, proposal **history** (past instructions + scores), and a randomly sampled instruction-design **tip**.
3. **Bayesian surrogate search** — a **Tree-structured Parzen Estimator (TPE)** searches the discrete space of (instruction, demo-set) assignments per module, scoring candidates on **stochastic mini-batches**. Credit assignment is *learned implicitly* — the surrogate credits whole configurations rather than attributing to one module.

## Key results

- Task model **Llama-3-8B** (served via SGLang); proposer **GPT-3.5** (temp 0.7), or **GPT-4** for the harder ScoNe / HoVer / Iris.
- Evaluated on **seven** multi-stage programs: **HotPotQA** (2-module multi-hop, EM), **HotPotQA Conditional**, **Iris**, **Iris-Typo**, **Heart Disease** (answer-ensemble), **ScoNe** (NLI w/ negation), **HoVer** (4-module multi-hop verify, Recall@21).
- MIPRO wins on **five of seven** programs, by **as much as ~13%** accuracy. HotPotQA 36.1% → **46.4%** (+10.3); HoVer 25.3% → **39.0%** (+13.7); ScoNe → **79.4%**.

> [!key-insight] Three lessons
> 1. **Bootstrapped demonstrations are the single highest-impact lever** — optimizing few-shot demos alone often beats optimizing instructions alone.
> 2. **Optimizing both (full MIPRO) generally wins overall.**
> 3. **Instructions matter most for conditional-rule tasks** — rules that aren't obvious and can't be conveyed by a few examples (HotPotQA Conditional, ScoNe).

## Lineage / 引用脉络

MIPRO is itself the primary source; its key upstream references are foundational methods, mostly already represented conceptually in the wiki (cited, not separately chased):

- **[[DSPy]]** (Khattab et al. 2022, 2023/2024) — the compound-AI-system framework and `Φ = (M, C, X, Y)` formalism MIPRO optimizes within. Already an entity page.
- **OPRO** (Yang et al. 2024) — LLM-as-optimizer for instructions; the "Module-Level OPRO" baseline.
- **Tree-structured Parzen Estimator** (Bergstra et al. 2011) — the Bayesian surrogate MIPRO uses for search.
- **APE / instruction induction** (Zhou et al. 2023); **Wan et al. 2024** — prior demos-vs-instructions findings MIPRO builds on.

## Why it matters for this wiki

This is the **prior SOTA** that [[GEPA]] (2026) measures itself against and beats by >10% — and the two papers' opposite findings on *instructions vs demonstrations* are the wiki's clearest worked example of how the field shifted. MIPRO (2024): **demonstrations dominate, optimize both**. GEPA (2026): **instruction-only can win**, attributed to stronger instruction-following / self-reflection in newer LLMs (see [[Prompt Optimization]] → "Key shifts GEPA documents"). MIPRO is the Bayesian/few-shot member of the [[DSPy]] optimizer family; GEPA is the reflective-evolutionary member.

> [!contradiction] MIPRO vs [[GEPA]] on demonstrations
> MIPRO finds **few-shot demonstrations are the highest-impact lever** and that optimizing both instructions+demos wins. [[GEPA]] (Agrawal et al. 2026) reverses this: **instruction-only optimization beats joint instruction+few-shot**, with prompts up to 9.2× shorter. Not a true contradiction — different model generations (Llama-3-8B / GPT-3.5–4 vs Qwen3-8B / GPT-4.1-Mini) and a different optimizer; GEPA attributes the flip to improved instruction-following in newer LLMs. Documented on both pages.

## Open questions

- How much of the "demonstrations dominate" finding is model-era-specific vs intrinsic? (GEPA's reversal suggests the former.)
- TPE surrogate vs evolutionary search ([[GEPA]]'s [[Pareto-based Candidate Selection]]) — how much of the performance gap is the *search policy* rather than the proposal mechanism?
