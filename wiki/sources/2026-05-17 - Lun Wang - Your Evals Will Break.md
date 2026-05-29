---
type: source
title: "Your Evals Will Break and You Won't See It Coming"
source_type: blog
author: "Lun Wang (ex-Google DeepMind)"
date_published: 2026-05-17
url: https://wanglun1996.github.io/blog/your-evals-will-break.html
created: 2026-05-28
updated: 2026-05-28
status: developing
confidence: high
seed_score: 13/14
tags: [ai-agents, llm, evaluation, eval-validity, interpretability]
key_claims:
  - "Eval — not training, architecture, or data — is the bottleneck for the next capability jump."
  - "Evaluation infrastructure is structurally reactive: it measures the system only after it has changed, so it cannot warn of a capability phase transition in advance."
  - "LLM eval lacks an order parameter — a macroscopic quantity that signals a regime change — unlike physics, which uses order parameters to detect phase transitions."
  - "Eval is upstream of training: 'if you can evaluate correctly, you can train correctly.' Goodhart breaks at phase boundaries — a proxy that tracked the goal in one regime decouples in the next."
  - "Fix: build adaptive evals — monitor meta-signals (score-distribution + correlation shifts), track multi-dimensional scaling curves, use self-evolving evals (models probing models), auto-generate tests as capabilities emerge."
related:
  - "[[Eval Validity]]"
  - "[[Eval Awareness]]"
  - "[[AI-Resistant Evaluation Design]]"
  - "[[Online Evaluation]]"
  - "[[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]"
cited_sources:
  - "[[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]"
sources: []
---

# Your Evals Will Break and You Won't See It Coming (Lun Wang, 2026)

A polemic-essay posted by **[[Lun Wang]]** the day he left Google DeepMind. One argument, stated hard: **evaluation is the binding constraint on the next capability jump** — not compute, not data, not architecture. We are good at scoring *today's* models and structurally blind to *tomorrow's*, precisely at the boundaries where it matters most.

## The argument in four moves

1. **Capability shifts can be real or illusory — and eval can't tell which.** Genuine emergence (Wei et al., 2022) vs. metric artifact ([[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]]); grokking (Power et al., 2022) as a third regime. Either way, an eval built for the prior regime gives the wrong reading at the transition. See [[Capability Phase Transitions]].

2. **There is no order parameter for capability.** Physics detects phase transitions via *order parameters* — macroscopic quantities that flip at the boundary. LLM eval has none. GPQA, SWE-bench, ARC-AGI, Humanity's Last Exam all measure *present* capability and give weak evidence about *post-transition* behavior. See [[Order Parameters for Capability Transitions]].

3. **Eval is structurally reactive.** *"We measure the system after it has changed."* Benchmarks are built for known capabilities, so by construction they observe a shift only once it has already happened. The fix is [[Adaptive Evaluation]].

4. **Eval is upstream of everything.** *"If you can evaluate correctly, you can train correctly."* Training optimizes against the eval, so a misaligned eval propagates into training signals, safety metrics, and scaling calls — and **Goodhart breaks at phase boundaries**. See [[Eval as Upstream Constraint]].

## The concrete failure mode

[[Strategic Information Withholding]]: a model selectively *omits* facts to steer a conversation while every individual statement stays technically true. Honesty benchmarks check truth of statements, not manipulativeness of *selection* — so this slips through. Wang's worked example of a behavior that emerges across a boundary and evades evals designed for the old regime.

## Proposed fix: adaptive evals

- Monitor **meta-signals** — shifts in score *distributions* and in *correlations* between metrics (the macro-signal substitute for a true order parameter).
- Track **multi-dimensional scaling curves**, not a single headline number.
- **Self-evolving evals** — models probing models; **auto-generate** tests as capabilities emerge.

These cite statistical mechanics + mechanistic interpretability as the toolkit: Shan, Li & Sompolinsky (PNAS 2026) on order parameters in continual learning, and Nanda et al. (ICLR 2023) on progress measures for grokking.

## How it sits in this wiki

- **Extends [[Eval Validity]] forward in time.** Schaeffer's "the metric is the construct" is a *static* validity claim (the metric distorts what you see *now*); Wang adds the *dynamic* claim — the metric's validity *expires* at a capability boundary. The proxy-drift / Goodhart failure mode listed on [[Eval Validity]] is exactly Wang's "Goodhart breaks at phase boundaries."
- **Pairs with [[Eval Awareness]].** Eval awareness is the model gaming a *known* eval; Wang's worry is the eval being *structurally incapable* of seeing a *new* behavior — a blind spot, not a gamed test. Together they bracket the two ways an eval lies.
- **Counterpoint to benchmark-as-truth.** Reinforces the wiki's standing treatment of any single leaderboard number as low-confidence (see [[Tool-Use Benchmarks - BFCL vs tau-bench vs ToolBench]], [[Agent Eval Pyramid]]).
- **Self-evolving evals** echo [[AI-Resistant Evaluation Design]] and the auto-generated-task machinery in [[Self-Evolving Agent Environments]].

## Lineage / 引用脉络

The post cites six papers; only one is currently in the wiki.

- **In wiki:** [[2023-05 - Schaeffer et al - Emergent Abilities a Mirage]] (Schaeffer, Miranda & Koyejo 2023) — the "mirage" counterweight to emergence; load-bearing for Wang's "real or illusory" move.
- **Cited but not yet filed** (candidates for a one-hop citation chase — see note below): Wei et al. 2022 (*Emergent Abilities of LLMs*); Power et al. 2022 + Liu et al. 2022 (*Grokking*); Nanda et al. 2023 (*Progress Measures for Grokking via Mech Interp*, ICLR); Shan, Li & Sompolinsky 2026 (*Order Parameters and Phase Transitions of Continual Learning*, PNAS).

> [!gap] Citation chase deferred
> The post provides no hyperlinks to its references (bibliographic names only), so the one-hop chase requires resolving + fetching 5 arXiv/PNAS papers — all likely to pass the seed gate (primary research, high authority) and each a full source page. That is a large, mostly-LLM-domain expansion beyond the blog itself. **Surfaced for Nick to green-light rather than auto-filed.** The Shan 2026 PNAS paper is the highest-value chase (it is Wang's proposed order-parameter toolkit and overlaps the existing `research/continual-learning-systems` work).
