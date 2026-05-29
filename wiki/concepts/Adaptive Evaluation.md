---
type: concept
title: "Adaptive Evaluation"
created: 2026-05-28
updated: 2026-05-28
tags: [ai-agents, llm, evaluation]
status: seed
related:
  - "[[Order Parameters for Capability Transitions]]"
  - "[[AI-Resistant Evaluation Design]]"
  - "[[Self-Evolving Agent Environments]]"
  - "[[Online Evaluation]]"
sources:
  - "[[2026-05-17 - Lun Wang - Your Evals Will Break]]"
---

# Adaptive Evaluation

## Summary

The proposed fix in [[2026-05-17 - Lun Wang - Your Evals Will Break]] for the **structurally reactive** nature of current evals. A static benchmark is built for *known* capabilities, so by construction it can only register a capability shift **after** it has already happened — *"we measure the system after it has changed."* An adaptive eval system instead changes *with* the model.

## The four mechanisms

1. **Monitor meta-signals** — don't just watch the headline score; watch its *distribution* and the *correlations between metrics*. A regime change shows up as a distributional/correlational break before any single number looks alarming. (The behavioral substitute for a true [[Order Parameters for Capability Transitions|order parameter]].)
2. **Track multi-dimensional scaling curves** — extrapolate across several axes, not one leaderboard number.
3. **Self-evolving evals** — use models to probe models, so the eval's difficulty rises with capability.
4. **Auto-generate test cases** as new capabilities emerge.

## Why it matters

This is the constructive half of Wang's polemic: if eval is the [[Eval as Upstream Constraint|upstream bottleneck]], making eval *adaptive* is the lever on the next capability jump. It connects to several existing wiki threads:

- **[[AI-Resistant Evaluation Design]]** — designing evals that don't decay as models get stronger; same "eval must keep up" instinct, applied to contamination/gaming.
- **[[Self-Evolving Agent Environments]]** — the `general-agent` synthesizer↔solver loop that auto-grows a difficulty-calibrated task corpus is a *working instance* of "self-evolving / auto-generating evals."
- **[[Online Evaluation]]** — adaptive eval in production: meta-signal monitoring is the deployment-time face of online eval.

## Limits / open questions

- Self-evolving evals risk **circularity** — a model probing models can inherit the prober's blind spots (it can't generate a test for a capability it can't conceive).
- Meta-signal monitoring detects *that* something changed, not *what* — diagnosis still needs human/interpretability follow-up.
- No baseline yet for what a "normal" score-distribution drift looks like vs. a genuine regime change.
