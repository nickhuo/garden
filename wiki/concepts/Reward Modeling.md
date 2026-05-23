---
type: concept
title: "Reward Modeling"
created: 2026-05-20
updated: 2026-05-20
tags: [ai-agents, llm, evaluation, reward-modeling, rlhf]
status: developing
related:
  - "[[Online Evaluation]]"
  - "[[LLM-as-Judge]]"
  - "[[Implicit Feedback Signals]]"
sources:
  - "[[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]"
---

# Reward Modeling

## Summary

A reward model (RM) maps a model output (or trajectory) to a scalar quality score, learned from preference data. It is the component that converts "humans/AI prefer A over B" into a differentiable signal a policy can optimize against. Introduced for LLMs in RLHF ([[2022 - Ouyang et al - InstructGPT]]); the reward model is trained on pairwise human preferences, then used to optimize the policy (PPO).

## Online and iterative variants

The classic RM is trained once, offline. The online/iterative family keeps the reward signal *live*:

- **Iterative / online DPO** — DPO collapses the explicit RM: the policy itself *implicitly* defines a reward (the log-ratio to a reference policy). Online DPO regenerates fresh completions from the current policy each round, scores them, and updates — keeping the preference data on-distribution (medium confidence; active 2024 research, e.g. OAIF, self-rewarding).
- **RLAIF** — the preference labeler is an LLM judge ([[LLM-as-Judge]]) rather than a human, making the reward signal cheap enough to refresh continuously.
- **Implicit reward from feedback** — production [[Implicit Feedback Signals]] (accept/edit/abandon) can themselves serve as the preference oracle, closing the loop from live behavior to policy update.

## Why it matters

Reward modeling is the mechanism that lets [[Online Evaluation]] become *online learning*: it is how a real-time interaction signal updates the policy, persona, or persisted memory rather than just reporting a dashboard number. The RM (or implicit reward) is the formal object sitting between "user behaved this way" and "model changes."

## Limits

- **Reward hacking** — the policy optimizes the proxy, not the goal; an online RM amplifies this faster than offline.
- **RM inherits judge bias** — an RLAIF reward carries every [[LLM-as-Judge]] bias (verbosity, self-enhancement) directly into the policy.
- **Distribution shift** — a static RM goes stale as the policy moves, motivating the iterative variants.

## Connection to prior work

Direct line: RLHF reward model ([[2022 - Ouyang et al - InstructGPT]]) → DPO implicit reward → online DPO / RLAIF. An LLM-as-Judge is effectively an inference-time, prompt-specified reward model. Nick's Compass closed loop (user logs → eval rubric / policy revision) is a hand-built, human-in-the-loop version of online reward modeling: the rubric is the reward function, refined from live signal.

## Connections

- The learning engine behind [[Online Evaluation]].
- Shares its bias surface with [[LLM-as-Judge]].
- Consumes [[Implicit Feedback Signals]] as preference data.

## Open questions

> [!gap] When implicit production feedback is the reward oracle, how do you prevent the policy from optimizing engagement at the expense of correctness?

## Sources

- [[2023-06-09 - Zheng et al - Judging LLM-as-a-Judge]]
- [[2022 - Ouyang et al - InstructGPT]] (RLHF reward model — owned elsewhere, linked)
