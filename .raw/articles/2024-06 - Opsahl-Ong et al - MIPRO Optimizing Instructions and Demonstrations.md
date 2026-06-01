---
source_url: https://arxiv.org/abs/2406.11695
pdf_url: https://arxiv.org/pdf/2406.11695
fetched: 2026-05-31
---

# Optimizing Instructions and Demonstrations for Multi-Stage Language Model Programs

**Authors:** Krista Opsahl-Ong, Michael J Ryan, Josh Purtell, David Broman, Christopher Potts, Matei Zaharia, Omar Khattab
**Affiliations:** Stanford University (Opsahl-Ong, Ryan, Potts, Khattab); Basis (Purtell); KTH Royal Institute of Technology (Broman); UC Berkeley / Databricks (Zaharia).
**Venue:** EMNLP 2024. arXiv 2406.11695 (v1 2024-06-17, v2 2024-10-06). cs.CL / cs.AI / cs.LG.

## Abstract (verbatim)

Language Model Programs, i.e. sophisticated pipelines of modular language model (LM) calls, are increasingly advancing NLP tasks, but they require crafting prompts that are jointly effective for all modules. We study prompt optimization for LM programs, i.e. how to update these prompts to maximize a downstream metric without access to module-level labels or gradients.

## Problem

An **LM Program** is a multi-stage pipeline where each module = (prompt template, LM). Goal: update each module's prompt (instructions + few-shot demonstrations) to maximize an end-to-end metric, given only:
- training inputs (and a metric), NO module-level labels;
- NO gradients (the LM may be a closed API).

Three core challenges:
1. **Proposal** — the combined instruction × demonstration search space across modules is intractably large.
2. **Credit assignment** — with no intermediate supervision, hard to know which module's prompt to change.
3. **Expensive evaluation** — each full-program rollout costs money/compute.

## MIPRO (Mult-prompt Instruction PRoposal Optimizer)

Components:
- **Bootstrapping few-shot demonstrations.** Run the program on training inputs; keep execution traces whose final output passes the metric. The per-module input/output pairs from successful traces become candidate few-shot demonstrations (self-generated, no manual curation).
- **Grounded instruction proposal.** A proposer LM writes candidate instructions per module, conditioned on grounding context:
  - *program-aware* — a summary of the program's code/control flow + the module's role;
  - *data-aware* — a summary of the dataset;
  - *demonstration-aware* — the bootstrapped demos;
  - *history* — previously proposed instructions + their scores;
  - *tips* — a randomly sampled instruction-design tip (e.g. "be creative", "be concise").
- **Bayesian surrogate optimization.** A **Tree-structured Parzen Estimator (TPE)** surrogate searches the discrete space of (instruction candidate, demo set) per module, evaluating proposals on **stochastic mini-batches**. Credit assignment is learned implicitly — the surrogate credits whole prompt-configuration combinations rather than isolating one module.
- **Meta-optimization** ("MIPRO++") — optimize the proposal hyperparameters (which grounding to use, temperature, tips) themselves.

## Optimizer variants / baselines

- Bootstrap Random Search (demonstrations only)
- Bayesian Bootstrap (Bayesian opt over demonstrations)
- Module-Level OPRO (instruction-only, OPRO-style)
- 0-Shot MIPRO (instruction optimization with surrogate, no demos)
- 0-Shot MIPRO++ (meta-optimization of proposal hyperparameters)
- **MIPRO** (joint instruction + demonstration optimization) — the full method.

## Tasks (Table 1, seven programs)

- **HotPotQA** — multi-hop retrieval program, 2 modules, Exact Match.
- **HotPotQA Conditional** — multi-hop QA with conditional answer-formatting rules by answer type.
- **Iris** — Fisher (1936) iris-flower classification.
- **Iris-Typo** — Iris with an intentional misspelling (error-correction stress).
- **Heart Disease** — binary classification, 13 features, "Answer Ensemble" program.
- **ScoNe** — NLI with negation (logical reasoning).
- **HoVer** — multi-hop claim verification, 4 modules, Recall@21.

## Models

- **Task model:** Llama-3-8B (served via SGLang on A100s).
- **Proposer LM:** GPT-3.5 (temp 0.7) for most tasks; GPT-4 for the harder ScoNe, HoVer, Iris.

## Headline results (Table 2, test)

- MIPRO outperforms baselines on **five of seven** programs, by **as much as ~13% accuracy**.
- HotPotQA: 36.1% → **46.4%** (+10.3 pts).
- ScoNe: large gain → **79.4%**.
- HoVer: 25.3% → **39.0%** (+13.7 pts, Recall@21).

## Three lessons

1. **Optimizing bootstrapped demonstrations as few-shot examples is key** to best performance — often higher-impact than instruction optimization alone.
2. **Optimizing both instructions and few-shot examples (MIPRO) generally yields the best overall performance.**
3. **Instruction optimization matters most for tasks with conditional rules** that are (i) not immediately obvious and (ii) not expressible via a limited number of few-shot examples (e.g. HotPotQA Conditional, ScoNe).

## Key citations (upstream)

- DSPy (Khattab et al. 2022, 2023/2024) — the compound-AI-system framework; formalism Φ = (M, C, X, Y).
- OPRO (Yang et al. 2024) — LLM-as-optimizer for instructions.
- Tree-structured Parzen Estimator (Bergstra et al. 2011) — the Bayesian surrogate.
- APE / instruction-induction prior work (Zhou et al. 2023); Wan et al. 2024 (demos vs instructions).
