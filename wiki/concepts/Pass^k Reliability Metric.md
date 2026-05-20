---
type: concept
title: "Pass^k Reliability Metric"
created: 2026-05-13
updated: 2026-05-13
tags:
- ai-agents
- evaluation
- reliability
- methodology
status: developing
related:
- "[[User Simulator Evaluation]]"
- "[[tau-bench]]"
- "[[LLM-as-Judge Evaluation]]"
- "[[Workflows Beat Agents for Most Production]]"
- "[[Eval Infrastructure Noise]]"
- "[[SWE-bench]]"
sources:
- "[[2024-06-17 - Yao et al - tau-bench]]"
- "[[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]]"
- "[[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]]"
---

# Pass^k Reliability Metric

## Definition

For an agent run on a task `n` i.i.d. times with `c` successes, **pass^k = E_task[ C(c,k) / C(n,k) ]** — the expected probability that **all** `k` sampled trials succeed. Contrast pass@k (the standard code-eval metric), which is the probability that **at least one** of `k` trials succeeds.

Pass^1 = pass@1 = mean reward. Pass^k diverges sharply from pass@k as k grows: pass@k → 1 (optimism over k), pass^k → 0 (pessimism over k).

Introduced by [[2024-06-17 - Yao et al - tau-bench]] (Sierra, 2024).

## Why it matters

For **discovery** problems (code generation, math, theorem proving), what you want is "did *any* of my k samples solve it?" — pass@k captures that. Inference-time compute helps, and the right metric measures the help.

For **deployment** problems (customer service, autonomous workflows, anything user-facing), you don't get to pick the best of k — you ship one trial and the user lives with the outcome. The right question is "if I run this task across millions of users, what fraction of users get a correct outcome?" That requires the worst-case-leaning lens. Pass^k operationalizes it: a model with pass^1=0.6 but pass^8=0.25 is **inconsistent**; production-grade reliability requires pass^k to decay slowly.

## The empirical finding

On τ-retail with gpt-4o function calling: pass^1 ≈ 61%, pass^8 < 25%. Same task, same setup, just different LM sampling. The user-simulator stochasticity ([[User Simulator Evaluation]]) is enough to flip outcomes on 36%+ of tasks the agent could solve at least once.

## Why traditional benchmarks miss this

Code-generation evals (HumanEval, MBPP) run 1 trial per task and report mean. SWE-bench runs few trials. Agent benchmarks (AgentBench, WebArena) typically run 1-3 trials. None of these surface variance. **Reliability is invisible until you measure it explicitly with k.**

## Connections

- Operationalizes a critical leg of [[Workflows Beat Agents for Most Production]] — workflows have pass^k closer to pass^1 by construction (less stochasticity in execution path); agents diverge.
- Orthogonal to [[LLM-as-Judge Evaluation]]: pass^k is *how many trials succeed*; LLM-judge is *how to score one trial*. They compose.
- Stress-tests anything in [[Autonomous Agents]] — long-horizon agent claims should be evaluated at pass^≥4, not pass^1.
- Cost implication: measuring pass^k well requires ≥8 trials/task, multiplying eval cost. See [[Token Economics]].

## Infrastructure noise as a prerequisite concern

[[Eval Infrastructure Noise]] (Anthropic 2026) surfaces an important constraint on pass^k measurement: **infrastructure variance sets a floor on measured pass^k that is independent of model quality**. A model with true pass^1 = 0.60 will measure lower if the eval harness introduces per-task noise. This means:

- Pass^k is only interpretable once infrastructure noise is characterized and controlled
- Hermetic eval environments (no live network, pre-warmed containers) are a prerequisite for reliable pass^k measurement
- This applies to coding evals ([[SWE-bench]]) as much as to interactive evals ([[tau-bench]])

## Eval awareness interaction

[[Eval Awareness]] can inflate pass^k scores: if a model exerts disproportionate effort when it detects repeated sampling in an evaluation context (as seen with [[Claude Opus 4.6]] on [[BrowseComp]]), measured pass^k may exceed true deployment reliability. See [[2026-05-13 - Anthropic - Eval Awareness BrowseComp]].

## Open questions

- Does pass^k decay the same way on non-customer-service domains, or is the user-simulator stochasticity the dominant variance source? (Partially answered: [[Eval Infrastructure Noise]] shows SWE-bench has high infra noise, suggesting the dominant variance source shifts by domain.)
- Is there a closed-form relationship between pass^1 and pass^k decay rate for a given agent architecture? (Hypothesis: decay slope correlates with depth of policy-dependent decisions.)
- Can per-trial entropy of the agent's action distribution predict pass^k decay without running k trials?
- Does eval awareness inflate or deflate pass^k, and by how much?

## Sources

- [[2024-06-17 - Yao et al - tau-bench]] (Yao, Shinn, Razavi, Narasimhan, Sierra 2024)
- [[2026-02-05 - Anthropic - Infrastructure Noise Agentic Coding Evals]] (Anthropic Engineering 2025) — extends pass^k to coding evals; identifies infra noise as a prerequisite concern
- [[2026-05-13 - Anthropic - Demystifying Evals for AI Agents]] (Anthropic, 2026-05-13) — contextualizes pass^k as required metric for Tier 3 in [[Agent Eval Pyramid]]; explains stochasticity accumulation across multi-turn episodes
