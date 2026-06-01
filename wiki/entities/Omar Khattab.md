---
type: entity
title: Omar Khattab
created: 2026-05-30
updated: 2026-06-01
tags: [llm, ai-agents, prompt-optimization, researcher]
status: developing
entity_type: person
entity_tier: thinker
affiliation: MIT (OASYS Lab)
core_claim: "Modular LLM systems should be programmed and optimized — and the best learning signal is interpretable language, not scalar reward."
related: ["[[DSPy]]", "[[GEPA]]", "[[MIPRO]]", "[[Compound AI System]]", "[[Prompt Optimization]]", "[[Recursive Language Models]]", "[[Krista Opsahl-Ong]]"]
sources: ["[[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]", "[[2024-06 - Opsahl-Ong et al - MIPRO Optimizing Instructions and Demonstrations]]", "[[2025-10 - Zhang Khattab - Recursive Language Models]]"]
---

# Omar Khattab

Researcher (MIT, OASYS Lab) working on **[[Compound AI System|compound AI systems]]**: how modular LLM programs should be *built, programmed, and optimized* rather than hand-prompted. Creator of **[[DSPy]]** (and earlier **ColBERT**, late-interaction retrieval).

## Worldview / 核心主张

1. **Program, don't prompt.** An LLM pipeline is a system `Φ = (M, C, X, Y)` of modules `M_i = (π_i, θ_i, X_i, Y_i)` with *learnable* parameters (prompts and/or weights). The job is to optimize that system against a metric — not to hand-tune strings. This formalism, from his DSPy papers (Khattab et al. 2022, 2024), is the substrate the whole optimizer lineage inherits.
2. **Learn in an interpretable medium.** [[GEPA]]'s thesis: language traces carry far more signal than a scalar reward. Reflecting on execution + evaluation traces in natural language beats policy-gradient RL ([[GRPO]]) by >10% over MIPROv2 and up to 20% over GRPO with up to **35× fewer rollouts**. See [[Language Feedback as Learning Signal]].
3. **Decompose the context, not the problem.** [[Recursive Language Models]]: a root LM never sees long context directly — it manipulates it as a REPL variable and spawns sub-LM calls. "No model call should ever require handling a huge context."

## Methodology / 方法论

- **Formalize first, then optimize.** Every contribution starts by naming the abstraction (late interaction; the DSPy module graph; the trace types in GEPA) and then building an optimizer or architecture on top of it.
- **Optimizers as the unit of progress.** His research advances by successive optimizers over the *same* DSPy substrate — few-shot bootstrapping → MIPROv2 → GEPA — each beating the last on the same benchmarks.
- **Quality-diversity over greedy search.** GEPA keeps a **Pareto frontier** of best candidates per task instance (MAP-Elites illumination) rather than always mutating the global best — escaping the local optima that trap SelectBest/BeamSearch ablations.
- **Trace harvesting.** Distinguishes **execution traces** (what the LLM produces) from **evaluation traces** (compiler/profiler output before it becomes a scalar reward) and feeds *both* to a reflection LM for implicit credit assignment.

## Body of work (in the wiki)

- **2024 — [[2024-06 - Opsahl-Ong et al - MIPRO Optimizing Instructions and Demonstrations]]** (senior author; lead [[Krista Opsahl-Ong]]) — joint instruction+demonstration optimizer via Bayesian optimization; prior SOTA prompt optimizer.
- **2025 — [[2025-10 - Zhang Khattab - Recursive Language Models]]** (advisor; lead Alex L. Zhang) — context-decomposition inference strategy; smaller-model RLM beats larger model alone (+114% on an OOLONG slice).
- **2026 — [[2026-02 - Agrawal et al - GEPA Reflective Prompt Evolution]]** (senior author, ICLR 2026 Oral) — reflective evolutionary prompt optimization; the successor that beats his own MIPROv2.

## Throughlines

- **Modularity + optimization** is the constant — from ColBERT's retrieval modules to DSPy's program graph to GEPA's per-module reflective mutation.
- **Interpretable signal beats opaque signal** — language feedback over scalar reward (GEPA); inspectable REPL code over a black-box long-context model (RLM).
- **Intra-author progression** — MIPRO → GEPA is a clean case of a researcher beating his own prior SOTA, with shared co-author [[Krista Opsahl-Ong]] across both.

## Tensions

- **vs RL-with-verifiable-rewards** ([[GRPO]], [[RL with Verifiable Rewards]]): GEPA argues language reflection is a richer learning medium than policy gradients — a direct challenge to the RLVR-for-everything default. The prompt-space twin of [[Heuristic Learning]] (Weng).
- **vs single-model long-context scaling**: RLM reframes long-context as an *architectural composition* property, sidestepping rather than solving "context rot."

## Corpus to ingest

- **DSPy papers** (Khattab et al. 2022, 2024) — the foundational `Φ = (M, C, X, Y)` formalism is currently only cited second-hand through GEPA/MIPRO.
- **ColBERT** (late-interaction retrieval) — the retrieval thread predating the optimizer line.

## Connections

- Collaborators in the wiki orbit: [[Krista Opsahl-Ong]] (MIPRO lead, GEPA co-author), Matei Zaharia, Christopher Potts, Dilara Soylu, Alex L. Zhang.
- [[DSPy]] — his framework; GEPA/MIPRO ship as optimizers in it.
