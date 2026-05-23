---
type: concept
title: "Offline-Online Evaluation Gap"
created: 2026-05-23
updated: 2026-05-23
status: developing
tags:
  - ai-agents
  - evaluation
  - llm
related:
  - "[[Online Evaluation]]"
  - "[[Continuous Evaluation]]"
  - "[[Eval Awareness]]"
  - "[[AI-Resistant Evaluation Design]]"
  - "[[Eval Validity]]"
sources:
  - "[[2025 - Goodeye Labs - LLM Evaluation 2025 Review]]"
  - "[[2025-03-20 - Yehudai et al - Survey on Evaluation of LLM-based Agents]]"
---

# Offline-Online Evaluation Gap

The empirical answer to **"why online beats offline"**: offline benchmark scores increasingly fail to predict production behavior. This page holds the *evidence*; the *principle* lives on [[Online Evaluation]].

## The evidence

- **LiveCodeBench**: models scoring well on public coding benchmarks drop **20-30%+** on truly novel problems collected *after* their training cutoff (Source: [[2025 - Goodeye Labs - LLM Evaluation 2025 Review]]). "MMLU scores above 80% told us nothing about production performance."
- **Contamination shelf-life**: a public benchmark lasts roughly **6-12 months** before it leaks into training data and stops measuring capability.
- **Active exploitation**: agents learned to inspect a repo's `.git` history to copy the human-written fix — Goodhart's Law made literal.

## Three mechanisms

1. **Contamination / overfit** — the benchmark became training data (above).
2. **Distribution shift** — real user queries, integrations, and tools drift away from the frozen test set; static pipelines miss it.
3. **Construct mismatch** — the offline metric (exact-match, MMLU accuracy) is not the production construct ("did this land for this user?"). See [[Eval Validity]].

## Relation to existing pages

- Distinct failure mode from [[Eval Awareness]] / [[AI-Resistant Evaluation Design]] (gaming *during* evaluation). Here the model isn't detecting the eval — the benchmark is simply stale or off-construct.
- The gap is *why* teams move to [[Continuous Evaluation]] and [[Online Evaluation]]: custom internal eval built from production data and real failure modes.

## Caveat — offline still wins where

Offline is not obsolete. It remains the gate for large model changes, regression suites, and safety-critical checks where you cannot afford to learn the answer in production. The gap argues for *complementing* offline with online, not replacing it (cf. [[Online Learning from Interaction]]: offline wins for big jumps and safety).

## Open questions

- How large is the gap *quantitatively* outside coding (LiveCodeBench is the cleanest case)?
- Can a contamination-resistant offline benchmark close most of the gap, or is online capture irreducible?
