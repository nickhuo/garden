---
type: concept
title: "LLM-as-Judge"
created: 2026-05-20
updated: 2026-05-28
tags: [ai-agents, llm, evaluation, llm-as-judge, methodology]
status: developing
related:
  - "[[Online Evaluation]]"
  - "[[Reward Modeling]]"
  - "[[Eval Awareness]]"
  - "[[Sandbagging]]"
  - "[[AI-Resistant Evaluation Design]]"
  - "[[Agent Eval Pyramid]]"
  - "[[Multi-Agent Systems]]"
  - "[[Pass^k Reliability Metric]]"
  - "[[tau-bench]]"
sources:
  - "[[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]"
  - "[[2025-06-13 - Anthropic - How we built our multi-agent research system]]"
  - "[[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]"
  - "[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]]"
---

# LLM-as-Judge

## Summary

LLM-as-Judge uses a strong LLM to score or compare outputs against a rubric, as a scalable proxy for human preference judgment. Two protocols: **single-answer grading** (score 1–10 or 0.0–1.0 on rubric axes) and **pairwise comparison** (which of A/B is better). Established by [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]], which showed GPT-4 reaches **>80% agreement with humans — the same level humans reach with each other** (high confidence; independently replicated since).

It is the only mechanism that scales end-state grading to live traffic. As an **online** evaluator it can score every production interaction in real time; as an offline evaluator it grades the golden dataset. It is also the substrate of [[Reward Modeling]] via RLAIF (the judge becomes the reward signal).

## Why it matters for agents — end-state, not process

Agentic systems explore many valid paths to the same goal. Process-fidelity evaluation ("did the agent take the *right* steps?") is the wrong question — **end-state evaluation** ("did the agent reach a correct outcome?") is the right one. Deterministic step-matching fails on open-ended agent output; LLM-as-Judge is the only practical tool that scales end-state grading.

## Anthropic's agent prescription

Per [[2025-06-13 - Anthropic - How we built our multi-agent research system]] and [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]], Anthropic uses a **single-call LLM judge** scoring 0.0–1.0 across explicit rubric axes (factual accuracy, citation accuracy, completeness, source quality, tool efficiency), supplemented by **mandatory human spot-checking**:

- **Single LLM call** (not a chain) per eval — rubric in prompt, score out; fast and reliable.
- **Rubric explicit and multi-axis** — avoid the single-number collapse that hides systematic errors.
- **Separate correctness from style** — factual accuracy weighted independently of tone or formatting.
- **Human spot-checks unavoidable** — catches systematic judge biases.
- **Pivot from process to end-state** grading.
- **Calibrate judges periodically** against 50–200-example human-labeled sets; judge drift is a real failure mode as models and prompts change.

This is placed as Tier 2 in the [[Agent Eval Pyramid]]. It **contrasts with** [[tau-bench]]'s deterministic database-state grading — LLM-judge handles open-ended outputs, DB-state grading handles constrained outcomes — and **composes with** [[Pass^k Reliability Metric]] when scoring repeated trials.

## Limits — the bias catalog (load-bearing)

Per Zheng et al. and subsequent work, treat any single judge score as **low confidence** until these are controlled:

- **Position bias** — favors response shown first/last; pairwise accuracy swings >10% on order swap. Mitigate: run both orderings, keep only consistent verdicts.
- **Verbosity bias** — longer = better, regardless of quality.
- **Self-enhancement bias** — a model rates its own family higher. Mitigate: cross-family judging (e.g. Nick's Compass gpt-4o vs gpt-5 dual-judge).
- **Limited reasoning** — judges misgrade math/logic where they are themselves weak.
- **Authority bias** — rewards citations even when fabricated.
- **[[Eval Awareness]] in judges** — judges may themselves be eval-aware, scoring responses differently when they recognize the evaluation context. This stacks a second layer of eval-conditioning risk on top of the model under evaluation (see [[2026-05-13 - Anthropic - Eval Awareness BrowseComp]]).

Mitigation stack: ensemble of judges, swap-and-require-consistency, and calibration against a human-labeled golden set (50–200 examples), re-run periodically because judges drift.

## Connection to prior work

Direct descendant of human preference grading in RLHF ([[2022 - Ouyang et al - InstructGPT]]); the judge is essentially an inference-time, prompt-specified reward model (see [[Reward Modeling]]). Nick's Compass dual-judge saw an **8.9pp swing on direction accuracy** between gpt-4o and gpt-5 judges — empirical proof that judge choice is a free variable that must be validated, exactly the reliability concern Zheng et al. raise. Beckman's two-axis judge (node legitimacy 92.2% vs edge-direction 30.8%) shows judges can be reliable on one axis and useless on another.

The same core failure mode — **proxy gaming** — now affects both LLM capability benchmarks and human hiring evaluations. [[AI-Resistant Evaluation Design]] is the hiring-side application of the same principle (measure what you actually care about, not a gameable proxy); the connection is explicit in [[2026-01-21 - Anthropic - AI-Resistant Technical Evaluations]].

## Production deployment for quality monitoring (Anthropic, 2026)

[[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] confirms Anthropic is building an LLM-as-judge harness running asynchronously on a **sample of live production traffic** — specifically to detect quality regressions invisible to error-rate monitoring. The trigger was a context assembly bug that produced coherent-but-wrong responses (see [[Context Assembly Pipeline]]). This is the first documented Anthropic deployment of LLM-as-judge for *production quality monitoring* rather than offline eval.

## Connections

- Powers the automated tier of [[Online Evaluation]].
- Methodology for [[Multi-Agent Systems]]; solves the long-horizon eval open question previously tracked in [[Autonomous Agents]].
- Refines [[Workflows Beat Agents for Most Production]] (eval is what tells you when a workflow stops being good enough).
- [[Eval Awareness]] / [[Sandbagging]] — judged models can detect and game the judge.
- [[AI-Resistant Evaluation Design]] — designing tasks judges can't be fooled on.

## Views / external observations

> The entries below are external vantage points on this concept, not formally ingested sources. They are noted here to enrich the concept page; promotion to a `wiki/sources/` page requires passing the seed gate.

- **The "agreement ceiling" framing** (Lenz Research, *Disagreement among frontier LLMs on real-world fact-checks*, 2026-05-28, [lenz.io/research/llm-disagreement](https://lenz.io/research/llm-disagreement)). 1,000 real user-submitted claims × 5 frontier judges (GPT-5.4, Claude Opus 4.7, Gemini 3 Pro, Gemini 3 Pro + Search, Sonar Pro), forced 4-bucket verdict (True / Mostly True / Misleading / False), no abstain. Headline numbers: **67% of claims** have ≥1 dissenter from the majority; **34%** show ≥2-bucket-distance disagreement; **21%** flip to polar opposites (True vs False). Pairwise judge agreement ranges **53%–75%**; Krippendorff's α (ordinal) = **0.639** — at the lower edge of "usable as a measurement instrument." Middle buckets ("Mostly True", "Misleading") almost never reach unanimity (0% / 5%); only True/False poles do (43–47%). Legal domain hits **77%** disagreement; History the lowest at 53%. The authors note 67% is **a lower bound on model error** since at most one verdict per claim can be right.
  - **Why it lands here:** complements Zheng et al.'s "judge ≈ human at >80% agreement" finding by exposing the orthogonal failure — **judge ↔ judge agreement is itself bounded**, often by less than human-human. The two together let us state a stronger claim: the **agreement ceiling** of any LLM-as-Judge eval system is `min(judge-vs-human, judge-vs-judge)`, and the second term is frequently the binding one — especially on nuanced (middle-bucket) verdicts where the underlying rubric is least crisp.
  - **Connects to:** Nick's Compass dual-judge (8.9pp direction-accuracy swing across judges is an instance of the same effect at smaller N); Beckman's two-axis judge (the high-agreement axis is the rubric-crisp one, mirroring Lenz's True/False vs middle-bucket asymmetry); the open question below on judge drift.
  - **Caveat:** parametric models scored without abstain; forced-choice exaggerates disagreement vs an abstain-allowed protocol. A follow-up with human-labeled ground truth is planned but not yet out — until then, this is a *disagreement* measurement, not a *correctness* one.

## Open questions

> [!gap] Do online (live-traffic) judges drift faster than offline judges, since the input distribution shifts continuously? No published characterization.

- Inter-rater reliability — how stable across model versions / prompt drift?
- Cost — at what scale does LLM-as-Judge eval itself become the budget bottleneck?
- Adversarial robustness — can agents game LLM judges by writing in ways the judge favors?

## Sources

- [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]] — the foundational methodology + bias catalog
- [[2025-06-13 - Anthropic - How we built our multi-agent research system]] (Anthropic, 2025-06-13) — single-call judge, multi-axis rubric, human spot-checks
- [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]] (Anthropic, 2026-05-13) — calibration sets, correctness/style split, placement as Tier 2 in [[Agent Eval Pyramid]]
- [[2026-05-13 - Anthropic - Postmortem Three Recent Issues]] (Anthropic, 2026-05-13) — production quality-monitoring deployment
